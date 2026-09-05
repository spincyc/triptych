# Research brief: Sixteenth Sunday after Pentecost

## Scope, inputs, and disposition

Provider: GPT. Collection: Roman Rite, 1962 Missal, temporal proper 56,
Sixteenth Sunday after Pentecost. Genre: English study companion governed by
`guidance/liturgy/roman-1962-propers.md` and the universal editorial, source,
repository, and Scripture-chronology guidance. This brief belongs to the
canonical leaf and its mechanically derived synthesis companion. It is an
authoring audit, not reader-facing prose or a translation.

Disposition settled before writing: **PASS**. The complete fresh seven-lane
join supplies direct reception for every appointed biblical passage, checked
liturgical antecedents, five selected cultural afterlives, and six exploratory
conjunctions actually reached by the precedent lane. The evidence deficiencies
recorded below constrain claims rather than requiring another sweep before
this bounded guide can be authored.

Inputs: all 116 findings in the `proper` v25 research-synthesis iteration 1
packet, run `8c6ccce8314da5fa`, seed commit
`b66eb4b44d8e76801a86275b19c3a2e45713b4ab`; the prescribed standing-finding and
prior-production records; and the complete generated `research/chronology.toml`.
`CARRIED_FINDINGS` is empty. The packet's SHA-256 is
`6db346628d743babdb13be9ea0e3d5755f3709f42571f650e1cb4926fb64a94c`.
All seven lanes' reported rechecks are dated 2026-09-05. Synthesis performed
no original research, new retrieval, source collation, or precedent search.

The accepted source audit controls the *Missale Romanum* (Vatican, 1962),
*Dominica decima sexta post Pentecosten*, printed pp. 397–398, marginal
nos. 1592–1601; the Collect is no. 1593. The complete appointed Latin and its
accents, English controls, rubrical particulars, and boundaries remain those
in `propers/verified.md`. No quotation of the appointed Latin may silently
normalize that collation. COV-001–002 and COV-009 report the accepted control;
older source-library OCR limitations do not invalidate it.

### Evidence classes and use

| Evidence class | Material available | Authoring disposition |
| --- | --- | --- |
| Textual observation | SCR-001–019; the text-level observations in THE-001–012; appointed-text control reported by COV-001–002, COV-007, COV-009 | Supports literal context, grammar, distinctions between selected clauses and their source verses, and restrained relations among the texts. |
| Documented historical orientation | LIT-001–004; attributed historical judgments in LIT-005–008; the chronology projection below | State the witness and the actual extent of its assertion. A sacramentary antecedent is not the first use of the complete 1962 formulary. |
| Documented reception | PAT-001–029; LIT-007; the external witnesses in PRE-005–006; verified CUL candidates | Attribute each interpretive move, distinguishing direct exegesis, later spiritual application, liturgical interpretation, and cultural redirection. |
| Source-grounded synthesis | SG-1–SG-5 below, supported by multiple texts and multiple reception witnesses in each unit | Supports Themes and Movement, integrated commentary, source-grounded synthesis, and the four senses at their stated extent. |
| Exploratory proposal | IP-1–IP-6, selected from PRE-007–012 | Interpretive Possibilities only. The received reasoning supports the anchors; the distinctive extension remains a proposal. |
| Unverified or record-only lead | The source and search limits below; unselected THE-009–011; Gardner, Bullock, and the mock-Gospel leads | Supplies no unsupported quotation, attribution, historical intent, or novelty assertion. |

The author inherits the findings and their material qualifications, not this
audit's register. Evidence-class labels, method, search mechanics, and process
commentary belong here or in terminal apparatus. A source's actual theological
reading should be stated affirmatively and attributed. A necessary textual or
historical difference stays beside its claim. Secular and hostile afterlives
belong in the gallery. No compiler's intention is established.

## Prior-production carry-forward

The three prescribed sources were checked in order. The tracked
`evaluations/blocking-findings-v1.toml` now records six standing findings from
this run's content-evaluation iteration 0. The search of matching
`build/tpt-runs/*/state.json` returned only `8c6ccce8314da5fa`; there is no
other surviving matching run from which to read last synthesis/evaluation
results or escalations. The inherited brief's carry-forward section says that,
at synthesis iteration 0, the tracked record was absent, only this run was
present, and no inherited brief existed. That earlier report of silence is
preserved as a report of its earlier state; it is superseded concerning the
now-present tracked record. No older production or deleted findings can be
ruled out from those silences. No recoverable prior-run escalation was supplied.

Every standing finding below comes from run `8c6ccce8314da5fa`,
`proper` v25, content-evaluation iteration 0. The current join answers the
research questions but does not itself repair the reader-facing files.

| Finding | What the evaluation required | Present disposition and evidence |
| --- | --- | --- |
| CON-EVI-001 | Restore the collated accents in four quotations: Dóminus in the appointed-text Alleluia explanation and Alleluia commentary; omnis patérnitas in the Epistle commentary; in maiestáte sua in the Gradual commentary. Exact original locations: `sections/05-appointed-text.tex:118`; `sections/30-commentary.tex:21,34,41`. | Unresolved authoring repair. The source audit is already sufficient; COV-001–002, COV-009 preserve its authority. This brief explicitly carries the orthographic control. No retrieval is required. |
| CON-SYN-001 | Each resulting source-grounded synthesis unit must develop more than one checked reception witness. The first two units in `sections/35-source-grounded-synthesis.tex` previously developed only Augustine and only Francis de Sales respectively. | Unresolved authoring repair; adequate evidence confirmed. SG-1 joins Augustine, Psalm 70 §§18–21, to Aquinas, *Super Ephesios* 3.4 (PAT-007–008). SG-2 joins Cyril, Sermon CII, to Francis de Sales III.5 (PAT-011, PAT-023). Their distinct reasoning must contribute to the conclusions within those units, not merely appear elsewhere or in appended references. |
| CON-CIT-001a | Resolve the 03738a Nativity source ID to an intelligible checked article citation, preserving the immutable assertion and its reported-traditional qualification. | Answered by SCR-023 and COV-010. The full John Gerard, “General Chronology,” *Catholic Encyclopedia* III (1908), “Christian era” bundle is carried immediately below and beside the chronology audit, including the registered access date and separate recheck date. |
| CON-CIT-001b | Replace “Christmas” in `sections/02-scriptural-date-location.tex:9` and `sections/99-references.tex:22` with the actual 03738a article, retaining the second Nativity alternative and all chronology values. | Unresolved authoring repair, now supplied with sufficient evidence by SCR-023 and COV-010. “Christmas” is not the checked witness for this assertion. |
| CON-CIT-002a | Supply complete reproducible Latin-edition citation bundles for Anthony's XVI and XVII sermons, with institution, routes, dates, and exact sections; preserve the differing reading pairs. | Answered by PAT-027–028, COV-011–012, PRE-005. The merged two-sermon citation bundle below preserves all metadata, including the indispensable `?latin=1` selector. |
| CON-CIT-002b | Make both Anthony references reproducible in `sections/99-references.tex:28` and the proposal references at `sections/50-interpretive.tex:9,54`, using the supplied bundles. | Unresolved authoring repair. The citation input is now complete; the reference must identify both sermons and their distinct checked sections. |

### Recovered citation identities

**Gerard / 03738a — scripture-context SCR-023 and source-citation-coverage
COV-010.** John Gerard, “General Chronology,” *The Catholic Encyclopedia*,
vol. 3 (New York: Robert Appleton Company, 1908), section “Christian era,” first
paragraph, sentence beginning “It is supposed by many”; New Advent
transcription by Rick McCarty. Stable public article:
https://www.newadvent.org/cathen/03738a.htm ; section route supplied by COV-010:
https://www.newadvent.org/cathen/03738a.htm#Christian . Registered access date:
2026-08-26; direct recheck: 2026-09-05. The retained article-text derivative's
physical lines 31–33 contain the heading and paragraph. The paragraph reports
an opinion held by others; the chronology label remains “the year of Rome 750
which he styles 3 B.C.”, disposition `disputed`, basis `reported-traditional`.
The source is *General Chronology*, not *Christmas*. The registered parent
SHA-256 is `5eb03e5b5707514be6a0075d41f99970fd38a2dffe9c157191fa2fe3666c1dd0`
(44,502 bytes); the retained derivative SHA-256 is
`dea165f13c912bb66bb1bc30fae59d6a7aa732750427da1343e746582698d10d`.
The new response has different bytes and its own receipt in the evidence
register. It does not replace those registered identities.

**Anthony / XVI and XVII — patristic-reception PAT-027–028,
source-citation-coverage COV-011–012, precedent-search PRE-005.** Responsible
author: Saint Anthony of Padua (Antonius Patavinus), *Sermones dominicales*.
Responsible host: Basilica of Saint Anthony of Padua (Basilica del Santo),
*Sermoni Domenicali*, santantonio.org; the footer identifies PISAPFMC,
Provincia Italiana di S. Antonio di Padova dei Frati Minori Conventuali.
These are Latin digital sermon texts selected by `?latin=1` despite the `/en/`
interface. The checked pages supply no printed base edition, named modern
textual editor, translation credit, or critical-edition date: the Latin web
edition is undated, with separate page-publication and update metadata below.
Access date for both: 2026-09-05. The web timestamps are not composition dates.

| Sermon and exact page identity | Stable Latin route and web metadata | Checked locus and material pairing |
| --- | --- | --- |
| *Dominica XVI post Pentecosten*; Latin heading DOMINICA XVI POST PENTECOSTEN; HTML title “DOMENICA XVI DOPO PENTECOSTE \| Saint Anthony of Padua” | https://www.santantonio.org/en/node/869?latin=1 ; `article:published_time=2016-01-02T00:00:00+01:00`; `article:modified_time` and `og:updated_time=2016-03-04T10:46:31+01:00`. | Complete served sermon §§1–12, outline and four panels. PAT and COV inspected §§2,7,12; PRE checked those sections with surrounding paragraphs and searched the complete page. §2 pairs Ephesians 3 and Luke 7/Nain; §7 treats 3:13–17; §12 treats 3:17–18 beside Luke 7:14–16. This is not the present Luke 14 pairing. |
| *Dominica XVII post Pentecosten*; Latin heading DOMINICA XVII POST PENTECOSTEN; HTML title “DOMENICA XVII DOPO PENTECOSTE \| Saint Anthony of Padua” | https://www.santantonio.org/en/sermons/sermoni-domenicali/domenica-xvii-dopo-pentecoste?latin=1 ; `article:published_time=2016-02-11T09:37:44+01:00`; `article:modified_time` and `og:updated_time=2016-03-04T10:47:14+01:00`. | Complete served sermon §§1–16, outline and five panels. Checked §§2,6,8–16; PRE also describes the surrounding §§7–12 treatment. §2 divides Luke 14 and identifies Ephesians 4; §6 treats 4:1–2; §§8–12 treat dropsy, healing, unity and 4:3–4; §§13–16 join humility, Luke 14:10 and 4:5–6. This is not Ephesians 3 as its Epistle. |

The plausible named XVI route returned a sermon index, not the sermon; the
node route above identifies the checked text. XVII without the selector serves
Italian. The modern page apparatus has no located redistribution grant; this
limits retention or reproduction of whole HTML, not ordinary citation and
attributed paraphrase of the checked sermon. No new English prayer translation
is authorized. Anthony's own citations of earlier writers do not independently
verify those underlying works. Fresh exact response hashes remain separate
from the already registered earlier response hashes, as the lane receipts show.

## Reconciled evidence and material differences

Each entry joins overlapping accounts while preserving every contributing
lane's evidence in the complete register below. Identical bytes or related
interpretations are not counted as independent corroboration merely because
several lanes read them.

| Shared subject | Contributing lanes and findings | Integrated decision |
| --- | --- | --- |
| Appointed text and translation | scripture-context SCR-001–019; theological-synthesis THE-001–012; source-citation-coverage COV-001–002,007,009 | The settled facsimile audit controls the selected Latin, including accents. Registered Challoner Scripture and Cummiskey's 1861 XVI-Sunday orations control English. The project-created postconciliar Collect rendering and normalized calendar projections are not replacement witnesses. |
| Ephesians: knees, Father, indwelling, dimensions, fullness, Church | SCR-002,008,016,018–019; PAT-002–003,008–009,024,026–027; THE-001–004,006,008; COV-003,006; PRE-005–006,009–010 | Chrysostom's immeasurable love, Augustine's Cross reading, and Aquinas's two explanations remain distinct. Verse 18 has no explicit object; supplying love from verse 19 is a contextual inference. Aquinas's fatherhood account does not efface the heavenly-family alternative. Neither divine identity nor measurable geometry follows from fullness. |
| Individual and ecclesial Psalm voices | SCR-001,003–004,006–007,011–015,017–019; PAT-001,004–007,013–022; THE-004,006–007; COV-004 | All five psalms have direct Augustine and Theodoret reception; Bellarmine or Aquinas adds later development. Their personal, corporate, conversional, and salvation-historical subjects are not silently made one. Bellarmine develops Augustine explicitly on Introit poverty. |
| Healing, silence, table honor | SCR-005,009–010; PAT-010–012,023,025,028; THE-002–003,005,009–012; COV-003; PRE-005,010–011,014 | The Sabbath meal is the narrative setting; the wedding is the parable. The man is healed and dismissed before the seating instruction. Luke gives no cause of his illness or account of his character. Cyril's son/ox witness differs from the appointed ass/ox; his parental-affection reasoning belongs to his text. Ambrose's and Anthony's moralized dropsy remains their spiritual reading. |
| Shame, threatened life, humility | SCR-006,010,017–018; PAT-006,011–013,017,023–025; THE-002,005–006; PRE-011,013 | Real danger and the request for enemies' shame remain. Augustine develops conversion from the omitted backward-turning clause; Theodoret emphasizes frustrated persecution; Aquinas permits penitence or punishment. Received honor is distinct from self-exaltation. The threatened singer is not blamed or identified with the guests. |
| Oration antecedents and chant group | LIT-001–004,008; THE-001,008; COV-005,007,009 | Old Gelasian III.XII has the Secret/Postcommunion pair with different opening prayers. Gregorian supplement XXXV has the triad at XVII; p.173 note c groups four matching chant incipits under a different ordinal and different prayers, with later-added Laudate dominum rather than Cantate Domino. This establishes antecedents, not an unchanged whole Mass. |
| *The Liturgical Year* continuation | LIT-007–008; PRE-006,009,014; COV-014 | The checked exact PDF is the 1909 second edition, translated by Dom Laurence Shepherd, *Time after Pentecost* II (complete-series XI), Stanbrook/London; its preface identifies a continuation after Guéranger without naming the continuator. All current lanes agree. The stale Duffy/1900 machine path is not its imprint, and personal Guéranger authorship is not established. The chapter's actual argument is usable. |
| Schuster and seasonal history | LIT-005–006,008; COV-005; SCR-002; THE-004 | Attribute the Cyprian/autumn account to Schuster, not a fresh Würzburg collation. His p.142 Ephesians-series endpoint conflicts with his own Philippians comments on pp.183,186 and must not be repeated. Distinguish his “similar” Offertory comparison from his “identical” Communion comparison. |
| New song and Nain | SCR-004,013; PAT-005,016,021,027; LIT-007; THE-003,007; PRE-004–005,012 | Augustine's heard Gospel is Luke 7; the continuation recalls the preceding Sunday's Nain Gospel; Anthony XVI pairs Ephesians 3 with Nain. These are three specific source relationships, none changing today's Luke 14 scene. |
| Gerard and Anthony digital identity | SCR-023; PAT-027–028; COV-010–012; PRE-005 | The complete reconciled bundles above resolve the two research citation findings. The registered artifact's access date and the fresh response's retrieval date remain separate; changed bytes are not silently substituted. |
| Cultural witnesses and bibliographic corrections | cultural-afterlife CUL-001–007; source-citation-coverage COV-013–014 | The five selected examples below have primary controls. Fitzgerald is the novelist, Dickens the journal conductor and attribution witness. Dickens's letter is to Mrs. James T. Fields, in Chapman and Hall's 1882 volume III; stale Macmillan paths and “letter to Fitzgerald” metadata do not govern. Folger's Sonnets download is FDT 0.9.0.1; *Love's Labor's Lost* is FDT 0.9.2. |
| Library state and evidence sufficiency | COV-001–014; all receipting lanes | Earlier absence of direct registered reception has been superseded by inspected loci. A failed non-indexable corpus search proves no absence. COV's record inspections are not fresh substantive source checks. A checked work/edition/locus is citable without a new library ID; source-registration owns supported metadata changes. |

### Appointed boundaries that control every section

The Introit selects Psalm 85 (86):3,5 with verse 1. The Gradual's Vulgate
101:16–17 corresponds to common modern English 102:15–16; the Offertory's
Vulgate 39:14–15 corresponds to modern 40:13–14. The Alleluia selects the
opening of Psalm 97 (98):1 and adds explicit *Dóminus*. The Offertory repeats
the petition and omits other clauses; the Communion clips Psalm 70 (71):16–18,
omitting the wonderful-works clause in verse 17 and the coming-generation
purpose clause in verse 18. Those clauses remain useful context only.
Liturgical incipits do not authorize invented English equivalents.

Gutenberg 1581 is an ebook number, not a printing date. Its composite
Challoner electronic text is not exactly identified with the 1899/1914 American
printing. Cummiskey's first revised edition (Philadelphia, 1861), *The Roman
Missal translated into the English language for the use of the laity*, XVI.
Sunday after Pentecost, pp.429–431, has an unnamed historical translator. It
is not an approved 1962 liturgical translation. Preserve its abbreviated
conclusions unless the accepted same-witness control supplies an expansion.

## Passage-by-passage reception matrix

Every distinct appointed biblical passage appears once. Exact works, editions,
public links, locus systems, and complete qualifications under the cited IDs
are retained in the evidence register. All checks are the lanes' reported
checks; the synthesis has not independently reverified them.

| Passage and proper | Complete context and canonical comparisons | Ancient direct exegesis checked | Medieval, Doctoral, or later reception | Use, disagreement, and negative boundary |
| --- | --- | --- | --- | --- |
| Psalm 85 (86):1,3,5 — Introit | Whole 1–17; Exodus 34:1–35, especially 5–10; SCR-001,011,017,019. | Augustine, *Enarrationes* 85, NPNF “Psalm LXXXVI” §§1–3,5,7; Theodoret, Ps.85:1–5, PG80 1553C–1556B; PAT-001,014. | Bellarmine, O'Sullivan 1866, Ps.LXXXV:1,3–5, pp.259–260; PAT-019. | Augustine hears Christ and Church and interprets all-day prayer through generations. Theodoret attends to variant Greek vocabulary; Bellarmine explicitly develops Augustine on humility rather than trust in wealth. No named crisis is supplied by the Davidic title. English, paired Greek/Latin facsimile; direct reception located, no author-wide absence claim. |
| Ephesians 3:13–21 — Epistle | All six chapters; continuous 2–4; Colossians 1–2 and John 14; SCR-002,008,016,018–019. | Chrysostom, *Homilies on Ephesians* VII, 3:13–21; Augustine, Letter 140, §§60–67, especially 25.62–26.64; PAT-002–003,024. | Aquinas, *Super Ephesios* 3 lect.4–5; Anthony XVI §§2,7,12 with Luke 7; Benedict XVI, 14 January 2009 audience; PAT-008–009,026–027. | Chrysostom: immense love and alternative readings of fullness/families. Aquinas: weakness acknowledged in knees, perseverance gifted, two readings of dimensions. Augustine: Cross, good works, perseverance, hope, hidden grace. Latin and English translations; Jerome's Ephesians commentary remains uninspected, not absent. The modern chapter notes do not supply a complete composition-introduction dossier. |
| Psalm 101 (102):16–17 — Gradual | Whole 1–29; Isaias 60; Hebrews 1:10–12 quotes the psalm's end rather than this chant; SCR-003,012,018–019. | Augustine, *Enarrationes* 101, NPNF “Psalm CII” §§16–18; Theodoret, Ps.101:14–19, PG80 1679B–1682B; PAT-004,015. | Bellarmine Ps.CI, p.317, the “Gentiles” and “built up Sion” lemmas; *Liturgical Year* continuation pp.359,363; PAT-020, PRE-006,009. | Theodoret explains the restored city, then why universal conversion exceeds that return; Augustine and Bellarmine develop present Church-building and final judgment. Preserve this difference. Bellarmine's local verse labels 15–16 do not renumber the Missal. Greek/Latin facsimile and English; no securely assigned individual psalm occasion or first-use date. |
| Psalm 97 (98):1, opening — Alleluia | Whole 1–9; Isaias 52:7–10, Luke 2:22–39, Exodus 15:1–21; SCR-004,013. | Augustine, *Enarrationes* 97, NPNF “Psalm XCVIII” §1; Theodoret Ps.97:1, PG80 1657C–1658D; PAT-005,016. | Bellarmine Ps.XCVII:1, p.306; PAT-021. | New life and Church peace in Augustine, a new way of worship at the Savior's advent in Theodoret, Christ's wonders and victory through humility and Cross in Bellarmine. The arm/right-hand interpretation uses the unappointed continuation. Augustine's Nain allusion is Luke 7. The corpus's Nativity relation is prophetic-referent, not a narrated event or composition date. |
| Luke 14:1–11 — Gospel | Luke 13–15; Proverbs 25:1–28, especially 6–7; Luke 18:9–14,22:24–30,1:46–55; Deut.22:1–8 and Exod.23:1–13; SCR-005,009–010. | Cyril, *Commentary on Luke* CI–CII, Payne Smith 1859, pp.471–479; Ambrose, *Expositio in Lucam* VII.195, PL15 1752A–B; PAT-010–012. | Anthony XVII §§2,6,8–16 with Ephesians 4; Francis de Sales III.5; Benedict XVI Angelus 29 August 2010 on overlapping postconciliar verses; PAT-023,025,028. | Cyril: merciful law, holy works, truthful lowliness and God-given honor; his son/ox differs from the appointed text. Ambrose: moralized excess and gentle persuasion. Sales rejects acted humility. Latin, French, Syriac-based English and official modern English; no fresh Syriac/Greek collation. No town, host's name, event date, or healed man's banquet place is supplied. |
| Psalm 39 (40):14–15, selected — Offertory | Whole 1–18; Psalm 69:1–6; Hebrews 10:5–10 uses earlier 39:7–9, with body/ears wording difference; SCR-006,014,017. | Augustine, *Enarrationes* 39 §§21–25, especially 22–24; Theodoret Ps.39:13–17, PG80 1159A–1160D; PAT-006,017. | Aquinas, *Super Psalmo* 39 n.7, unit 87202, Parma 1863 reportatio; PAT-013. | Augustine's suffering members need the physician; conversion is developed from an omitted continuation. Theodoret stresses thwarted persecution; Aquinas gives penitence or punishment and help to do good as well as escape evil. English, Greek/Latin facsimile, Latin. The full Aquinas delivery reaches Psalms 1–54 only; no negative about later psalms follows. |
| Psalm 70 (71):16–18, selected — Communion | Whole 1–24; Psalm 30:1–5 and 77:1–8; SCR-007,015,017,019. | Augustine, *Enarrationes* 70, NPNF “Psalm LXXI” §§18–21; Theodoret Ps.70:15–19, PG80 1423B–1426C; PAT-007,018. | Bellarmine Ps.LXX:16–18, pp.212–213; *Liturgical Year* continuation pp.370–371; PAT-022, LIT-007. | Augustine: conversion and enduring grace for person and Church. Theodoret: schooling through Moses and the law's oldness, with edition brackets material. Bellarmine: David's continued testimony. The psalm narrates no Eucharistic meal. English and Greek/Latin facsimile; different interpretive subjects remain distinct. |

### Composed prayers and ritual action

| Proper | Textual and ritual contribution | Documented historical or liturgical reception | Evidence limit |
| --- | --- | --- | --- |
| Collect | Grace precedes and follows, making constant good works possible; THE-001,005,006; Cummiskey p.429. | Wilson 1915 pp.133–135, especially p.135 evening/morning collection, and supplement XXXV p.174 Sunday XVII; LIT-002–003. Aquinas's prayer for gifted perseverance (PAT-008) is doctrinal illumination, not direct commentary on the Collect. | No original composer or transfer date established. No technical account of every category of grace follows from the oration alone. |
| Secret | Purification through the present sacrifice and mercy making participation worthy; THE-001,008; Cummiskey p.431. | Wilson 1894 III.XII p.231; Wilson 1915 supplement XXXV p.174; *Liturgical Year* continuation pp.370–371 relates it to consecration and Communion; LIT-001,003,007. | The ancient prayer grouping has different ordinals and surrounding texts. Worthiness is prayed for, not self-certified; no complete sacramental causal timetable is supplied. |
| Postcommunion | Purification of minds, renewal by heavenly mysteries, present and future help for bodies; THE-003,007–008; Cummiskey p.431. | The same Gelasian pair and Gregorian triad; *Liturgical Year* continuation pp.370–371 develops bodily effects now and hereafter; LIT-001,003,007. | Preserve the Latin's explicit bodies and the historical English's different expression. Sacramental renewal does not guarantee medical cure or longevity; the prayer alone is not a complete exposition of resurrection doctrine. |

## Organized cross-proper argument

The strongest supported argument is that dependence on God's continuing gift
makes active mercy, truthful humility, common praise, and embodied renewal
possible. Grace does not become dispensable once good works or inner strength
appear. Its gifts enlarge the Church's life while the faithful continue to ask
for help. This is a conclusion from the appointed texts and their checked
reception, not a historical theory of selection.

The five units below are functional, not a procession through the ten propers.
Each already combines multiple appointed elements, canonical contexts, and
more than one reception witness. The integrated commentary should develop
them independently of the full element-by-element sweep. The source-grounded
synthesis must also develop multiple witnesses within each of its own units,
as CON-SYN-001 requires. Citations elsewhere cannot supply a missing argument.
Themes and Movement may condense these five units into three to five developed
movements across its two pages; avoid merely repeating the same paragraph in
several components.

### SG-1 — Grace enables and sustains responsible action

**Elements:** Collect, Epistle, Secret, Communion, with the Gospel specifying
concrete good works. **Evidence:** THE-001,005,008; SCR-002,007,016;
PAT-007–008,013; LIT-007. **Class:** source-grounded synthesis.

The Collect's constant good works and the Secret's worthy participation are
effects sought from God's grace and mercy. Ephesians 3 asks for inward
strength and Christ's indwelling; its whole-letter context at 2:8–10 makes
grace and actual good works complementary. Augustine on Psalm 70 §§18–21
denies that God merely teaches a route and then becomes unnecessary: the
beginning and the continuing life both require him. Aquinas, *Super Ephesios*
3.4, interprets bent knees as acknowledgement of weakness and perseverance as
God's gift. His account makes the Epistle's strong inner person compatible
with the Communion's continued need. Aquinas on Psalm 39 n.7 adds that help
is requested for doing good as well as escaping evil. The Gospel's immediate
relief and relinquished precedence give the Collect's requested activity
specific moral content.

The conjunction supports grace-enabled action and gratitude. It does not
establish every distinction concerning first grace, merit, final perseverance,
or justification. COV-006's doctrinal passage records are record-level
coverage; do not turn them into newly checked technical arguments. Good works
are neither erased nor treated as an unaided purchase of grace.

### SG-2 — Mercy and humility order the reception of honor

**Elements:** Gospel, Epistle, Communion, Introit, Offertory.
**Evidence:** THE-002,005–006; SCR-001,005–010,017–018; PAT-001,006,
011–013,017,023–025. **Class:** source-grounded synthesis.

Luke condemns selecting the first place for oneself while retaining the good
of honor bestowed by another. Cyril, Sermon CII, moves from misplaced rank to
truthful self-knowledge, mortality, and willingness to relinquish even honor
one could claim without blame. Francis de Sales III.5 tests the corresponding
interior desire: selecting the last place as a performance to obtain promotion
reproduces the ambition it pretends to abandon. Together they establish a
substantial account of humility, rather than a clever seating strategy.
The Epistle's glory through apostolic tribulation and final doxology, and the
Communion's remembrance of God's justice, make received good compatible with
continued suffering and dependence. Augustine's Introit exposition admits
humility amid material wealth; the issue is reliance and self-estimation.

The Offertory's enemies and their shame must receive full treatment in this
argument. Augustine's physician and suffering members, Theodoret's frustrated
persecutors, and Aquinas's penitence-or-punishment alternative show why rescue
cannot be dissolved into generic peaceful feeling. Their different readings
remain attributed. The further proposal that the singer's plea should turn
into self-examination belongs to IP-5, not a literal identification of enemies
with guests. Neither worldly promotion nor the invalidation of all honor
follows from the Gospel.

### SG-3 — Inner strengthening opens into a people of praise

**Elements:** Epistle, Gradual, Alleluia, Introit.
**Evidence:** THE-004,006–007; SCR-001–004,008,011–013,016,018;
PAT-001–005,009,015–016,020–021,024,026; LIT-007; PRE-006,009.
**Class:** source-grounded synthesis.

Ephesians asks the Father to strengthen through the Spirit for Christ's
indwelling and shared knowledge with all saints, and its doxology names the
Church. The wider letter has already described both peoples as God's common
dwelling. The Gradual's rebuilt Sion and acknowledged glory meet this communal
horizon without erasing the psalm's afflicted petitioner and restored city.
Theodoret explains why the universal conversion of nations exceeds the return
from captivity; Augustine and Bellarmine develop present Church-building
toward Christ's glorious judgment. Chrysostom locates the four dimensions in
immeasurable love and sees the Church's praise enduring; Augustine's Letter
140 also connects common sainthood with one bread, one body, and love of
enemies. The Alleluia's new song becomes renewed life and Church peace in
Augustine and new worship in Theodoret, while its whole psalm calls nations
and creation to praise. The Introit's whole psalm also anticipates all nations.

The *Liturgical Year* continuation pp.359,363 supplies an actual liturgical
precedent for the indwelling/building/praise relation. The further move to
Gospel table space belongs to IP-3. Preserve Chrysostom's, Augustine's, and
Aquinas's distinct explanations of dimensions; God is not a measurable
object, and created persons do not become identical with his essence. Neither
political program nor wholesale rejection of Israel is established.

### SG-4 — Purification and help concern the embodied person

**Elements:** Gospel, Epistle, Secret, Postcommunion, Alleluia.
**Evidence:** THE-003,007–008; SCR-002,004–005,009; PAT-005,010,012,
016,021,028; LIT-001,003,007; PRE-014.
**Class:** source-grounded synthesis.

Jesus cures an actual bodily affliction; the Epistle asks for inner strength;
the Secret and Postcommunion ask purification and renewal through the present
sacrifice and heavenly mysteries. Cyril, Sermon CI, interprets merciful Sabbath
action as holy works joined to cessation from sin. Augustine on Psalm 97
distinguishes recovered bodily health from being healed inwardly for God.
These are related goods with different objects and effects. The *Liturgical
Year* continuation pp.370–371 develops the Secret as preparation for
participation and the Postcommunion as renewal reaching bodily life now and
hereafter. Together the witnesses support attending to the person as body
and soul without reducing one form of help to another.

Ambrose's and Anthony's spiritual dropsy can deepen the Gospel commentary
when attributed; it is not Luke's explanation of the man's illness. The man
is dismissed; the text does not take him through Communion or a higher seat.
Eucharistic reception does not promise immediate medical cure, and indwelling
through faith is not simply another wording for sacramental reception. The
future bodily-help clause allows an eschatological horizon without silently
importing an unexamined technical doctrine.

### SG-5 — Praise and dependence continue across a lifetime

**Elements:** Introit, Epistle, Offertory, Communion, Postcommunion, Alleluia.
**Evidence:** THE-006–007; SCR-001–004,006–007,015,017–019;
PAT-001,003,007,018,022; LIT-007; PRE-008,012.
**Class:** source-grounded synthesis at the restrained extent stated here.

Daily supplication, remembered teaching from youth into old age, and glory
through all generations are different textual spans. Augustine's Introit
exposition hears the Church praying through successive generations;
Chrysostom on the Epistle sees the Church's thanksgiving extending into
eternity. Augustine's Psalm 70 interpretation rejects any life stage at which
divine assistance becomes dispensable; Bellarmine emphasizes continuing
personal testimony to God's power. The full Communion psalm directs that
testimony to a coming generation, although the chant stops before the purpose
clause. The Offertory's present danger and the Postcommunion's renewed
petition prevent the progression of the Mass from being treated as the end
of all need. New praise can coexist with aged dependence.

Theodoret's Moses/law account of Psalm 70 is a distinct corporate reading,
not simply Augustine's personal ages under another name. A single speaker
across all source psalms, a timetable of grace, or promised longevity is not
established. The stronger account of one aging worshipper singing a new song
and carrying received history through renewal is explicitly exploratory in
IP-6; SG-5 retains only the supported coexistence and reception.

### Page-1 four-senses evidence

| Sense | Supported synthesis and evidence |
| --- | --- |
| Literal | Needy prayer and divine help; Paul prays amid tribulation; Jesus heals and teaches guests; prayers ask grace, purification, participation and help. SCR-001–007; THE-001–008. |
| Allegorical | Christ and Church pray together (Augustine Ps.85); Sion built as the Church (Augustine Ps.101 and Bellarmine, with Theodoret's distinct development); Cross dimensions in Augustine Letter 140 and Aquinas. PAT-001,004,009,015,020,024. Do not hide a new table/heart geometry here. |
| Moral | Grace sustains good works; mercy acts promptly; humility is truthful rather than performed; dependence renounces self-grounded righteousness. THE-001,005; PAT-007–008,010–011,023. |
| Anagogical | Church-building toward Christ's glorious judgment, doxology enduring, and help now and hereafter. PAT-003–004,020,025; LIT-007; THE-003. The sources support this horizon without a guaranteed earthly rank, cure, or lifespan. |

## Corpora, languages, and material search boundaries

**Scripture-context (SCR-001–026).** The registered Douay–Rheims/Challoner
Gutenberg 1581 verse artifacts were read across Psalms 39:1–18, 70:1–24,
85:1–17, 97:1–9, 101:1–29, all Ephesians 1:1–6:24, and Luke 13:1–15:32.
The named canonical comparisons in SCR-010–016 were also inspected at their
reported extents: Proverbs 25; Deuteronomy 22:1–8; Exodus 15, 23:1–13, 34;
Isaias 52 and 60; Hebrews 1 and 10; Psalms 30,69,77; Colossians 1–2; John 14;
the specified additional Lukan passages. Clementine Latin and modern USCCB
Ephesians 3/Luke 14 chapter pages supply wording comparisons; each complete
chapter and its notes was read. The modern pages are not appointed English
and no Greek manuscript collation is claimed. The chronology record was read
as the sole dating source, not supplemented from biblical context.

**Patristic and saintly reception (PAT-001–029).** Passage-led checks cover
Augustine's NPNF I.8 English and Letter 140 Latin; Chrysostom's NPNF I.13
English; Theodoret PG80 paired Greek/Latin facsimile; Cyril's Payne Smith
Syriac-based English in Pearse's modernized web presentation; Ambrose's Latin
Book VII; Aquinas's Latin Ephesians lectures and Psalm 39 exposition;
Bellarmine's O'Sullivan English; Francis de Sales's Perisse 1832 French;
Anthony's two Latin sermons; and Benedict XVI's two official English texts.
The PG80 detail was read principally through its Latin translation with Greek
phrases cross-checked. No fresh Greek collation is claimed for Chrysostom or
Syriac collation for Cyril. Complete NPNF delivery remains abridged; Bellarmine's
English is also expressly abridged (COV-004). Aquinas's entire served Psalm
collection was acquired, but detailed inspection in this join is Psalm 39 n.7
and its masthead, not every acquired psalm. Jerome's Ephesians commentary
was not inspected. These limits preserve a discoverable omission without
claiming every Father or saint has been searched.

**Liturgical history (LIT-001–008).** Wilson's complete Gelasian 1894 IA OCR
and Gregorian 1915 edition/text extraction were searched for the reported
prayer incipits and variants; positive loci and the specified introductions
were checked on images. Schuster III was searched for the Sunday and
post-Cyprian heading; pp.142–145,183,186 were checked on images. The
*Liturgical Year* continuation's Sixteenth-Sunday chapter pp.356–372 was read,
with the recorded image checks and front matter. Latin and English were used.
The three discovery queries in LIT-008 led to those editions; devotional pages
and snippets were not controls. No original manuscripts, all eighth-century
Gelasian books, Ambrosian books, or exhaustive medieval series were examined.
The older eight-artifact/six-edition ancient-sacramentary corpus's three
searches failed because of non-indexable material (COV-005), and are not
zero-match evidence. The history lane's independent searchable OCR and page
checks do not make that registered corpus executable.

**Theological synthesis (THE-001–012).** All ten settled texts, the three
Cummiskey rows, complete Ephesians, the named Psalms, and Luke 13–14 were
inspected. The lane offered textual candidates, not newly verified doctrinal
definitions. COV-006 inspected the records for Trent VI.16 and XXII.2, Aquinas
I–II q.114 a.8, and Catechism 1362–1377/1402–1405 only. Their stated loci remain
doctrinal record coverage, not a substitute for an underlying check beyond
the theological lane's claims.

**Citation coverage (COV-001–014).** This is an identity, artifact, binding,
rights, and extent diagnostic across the sources the findings name. Positive
direct rereading is separately identified for Gerard and Anthony, and title/
preface checks for the continuation and Dickens. The distinction between
reading a record and rechecking a source's substantive argument remains
controlling. The accepted appointed-text audit was not repeated.

**Cultural afterlife (CUL-001–013).** English phrases from every appointed
scriptural element and the named Latin incipits were searched on 2026-09-05,
then the literary and political witnesses were checked at the stated primary
loci. The full records below preserve the actual queries, exact checked
extent, unverified leads, and excluded ordinary devotional or musical reuse.
This is not an exhaustive search of all literature, languages, music, visual
art, or print archives. Seven qualifying candidates were supplied; five are
selected. The gallery need not invent a candidate for every chant.

**Precedent (PRE-001–014).** The lane replayed the 328-file snapshot of
`*.tex` and `research/scope.md` under both providers' liturgy/propers trees,
excluding both current proper-56 leaves. Corpus manifest SHA-256:
`43ed2e1592bbd72360538c2374ce43b7bf69b0142674f43e6ed41e59c342179c`.
Complete-file case-insensitive DOTALL conjunction searches returned C1 0,
C2 41, C3 110, C4 39, C5 16, C6 20, C7 56, C8 62 file co-occurrences. These
counts are hits, not semantic precedents. English/Latin lexical families and
a second old-age/new-song search were followed by the identified passage
checks. The two complete Anthony sermon pages and the continuation's full
Sixteenth-Sunday chapter supplemented that corpus; the complete external
author collections were not searched. Other publication genres received
incipit searches only. Other checkouts, branches, paywalled material,
unsearched languages and synonym/markup/OCR failures remain outside the
negative boundary. Prior Triptych prose supplies structural or analogue
evidence, not independent theological authority. PRE-001's direct opening is
usable; the rhetorical wrappers identified in PRE-002 are not.

### Missing, rejected, and unresolved evidence

| Evidence limitation | What the evidence in hand supports | Constraint or disposition |
| --- | --- | --- |
| No named compiler, exact first use, or dated transfer record for the complete 1962 conjunction; LIT-008 | Specific Gelasian pair, Gregorian triad and separate chant group; later Schuster and continuation interpretations. | Keep first-use/selection intent unstated. The continuation's “anticipated by eight days” p.372 remains its attributed claim, not a dated transfer record. |
| No complete critical geography/authorship dossier for all seven Scriptures in this join; SCR and COV-008 | Literal settings and audiences explicitly stated in the inspected text; received attribution where reported; exact corpus dates below. | Page 2 must state the bounded missing fields, not invent a modern horizon, town, composition place, first audience, or biography. Modern chapter-note comparisons are not whole-book introductions. |
| Jerome's Ephesians commentary uninspected; Jerome's Matthew prologue recorded but not freshly read here; COV-008 | Direct Ephesians reception already exists in Chrysostom, Augustine, and Aquinas. Gadenz's publisher excerpt is known to cover introduction/chapter 1, not Luke 14. | No negative about Jerome's exegesis; no new claim of Lukan provenance from the record alone; no uninspected Gadenz Luke 14 quotation. |
| Broad doctrinal assertions exceed fresh checks; COV-006, THE-001,003–004,008 | Sustained grace, actual works, mercy, purification, faith, charity, and present/future help in the appointed texts and direct reception. | Do not extend a record of q.114 a.8's increase of existing grace to first grace or final perseverance. Do not infer every technical doctrine of sacrifice, validity, presence, reception, or resurrection from these prayers alone. |
| Failed ancient-sacramentary corpus searches; COV-005 | Positive facsimile loci checked separately by LIT. | Failure is not absence; there is no exhaustive early-history claim. |
| Older library imprints/locators conflict with checked witnesses; COV-001,014 | Correct Collect no.1593; continuation 1909 second edition; Dickens Chapman and Hall 1882, letter to Mrs. Fields. | Use correct intelligible citations. Library repair is source-registration's scope; it is no authoring prerequisite and the stale ID is not a competing historical edition. |
| Whole modern presentations have unresolved or restricted redistribution rights; PAT, COV, CUL receipts | Ordinary citations, attributed paraphrases, and the focused short extracts within the stated rights basis. | Whole USCCB/Vatican/Anthony/Esquire/Batchelor presentations are not cleared for republication. Source-registration or the maintainer owns any unresolved artifact-retention control; citation and bounded paraphrase remain usable meanwhile. The congressional page has its own government-text basis; the complete parent also contains protected reprints. |
| Gardner's original satire unavailable in the checked public publisher view; CUL-013 | Bibliographic lead and a prior excerpt report in Rucker. | Excluded from gallery; full narrative unverified. No need to fill this optional lead because five independently qualifying candidates remain. |
| Bullock's full thesis returned 403; CUL-010 | Exact title, institutional record, and complete author abstract. | Excluded from selected gallery; title/abstract alone did not establish the original argument or precise psalm dependence. |
| Mock-Gospel *Evangelium secundum marcas argenti* not checked in an underlying edition; CUL-008 | English secondary discovery lead, with egenus rather than the Introit's inops. | Unverified lead only, not an Introit afterlife. |
| THE-009 attention, THE-010 guest/host/Secret, THE-011 silence/learning lack a precedent-lane check of their distinctive conjunctions | They remain theological-lane exploratory candidates. | Not retained as additional published proposals. IP-3 uses the reached Epistle–Gradual–Gospel conjunction, not THE-010's distinct unsearched construction. THE-012's lowering/raising field is reached by PRE-010 and used only within that bound. |

None of these rows makes an absent machine ID a publication control. The brief
carries checked work, edition, and locus evidence wherever a retained substantial
claim is asserted. The complete source strings and receipts below preserve
what can be cited and what was only cataloged. No new evidence is to be
silently supplied from a neighboring source, an anthology heading, or memory.

## Scriptural chronology audit

Sole input: the complete generated `research/chronology.toml`, schema 2,
`proper-chronology`, calendar `roman-1962`, mass `pentecost-16`, system
`vulgate`, requested profile `catholic-comprehensive-v1`, formulary `appointed`.
The record was read without change. All seven scriptural elements below have
identical `claims` and `publication_claims` arrays: each assertion listed is
common to every appointed locus named for its element. No partial-locus
assertion has been promoted to the complete element. The claim's leaf profile
names the resolved evidence profile for its relation. The normalized `date`
field is not a second source of printable wording; the source's `label` is
copied below unchanged. The generated annotations remain the controlled
publication interface under chronology guidance §14.1.

No scriptural element in this record has status `undated-in-tradition` or
`research-pending`, and no scriptural element is assertion-free. Five are
`composition-only`; the Alleluia and Communion are `dated` because their
additional typed relations apply. In particular, `dated` does not turn either
Psalm into a narration of the related event. The three composed orations have
no directly appointed Scripture loci and no chronology assertion; they are not
missing biblical dossiers.

### Introit — `introit`

Appointed references: Psalm 85:3, 5; Psalm 85:1.

Loci: `Ps.85.3`, `Ps.85.5`, `Ps.85.1`.

Corpus status: `composition-only`. Publication status: `composition-only`. Requested profile: `catholic-comprehensive-v1`.

Assertion 1:

- `subject`: `critical.psalms.latest-composition-boundary`
- `title`: “The latest composition boundary shared by the Psalms”
- `relation`: `composition`
- `profile`: `catholic-critical-v1`
- `label`: “before the Maccabean period, around 165 B.C.; no individual psalm can be dated securely”
- `disposition`: `preferred`
- `answerability`: `answerable`
- `basis_class`: `catholic-critical`
- `precision`: `boundary`
- Source IDs: `passage.united-states-conference-of-catholic-bishops.new-american-bible-revised-edition.english-usccb-web-2026-07-28.psalms-introduction`.
- Source reach: `Ps.85.1` from `Ps`, inherited `true`; `Ps.85.3` from `Ps`, inherited `true`; `Ps.85.5` from `Ps`, inherited `true`.

### Epistle — `epistle`

Appointed references: Ephesians 3:13-21.

Loci: `Eph.3.13`, `Eph.3.14`, `Eph.3.15`, `Eph.3.16`, `Eph.3.17`, `Eph.3.18`, `Eph.3.19`, `Eph.3.20`, `Eph.3.21`.

Corpus status: `composition-only`. Publication status: `composition-only`. Requested profile: `catholic-comprehensive-v1`.

Assertion 1:

- `subject`: `composition.epistle-to-the-ephesians`
- `title`: “The Epistle to the Ephesians”
- `relation`: `composition`
- `profile`: `catholic-traditional-v1`
- `label`: “a period between 58 and 63”
- `disposition`: `disputed`
- `answerability`: `answerable`
- `basis_class`: `traditional-catholic`
- `precision`: `interval`
- Source IDs: `artifact.catholic-encyclopedia.volume-5.new-york-1909.newadvent-05485a-66d722ae`.
- Source reach: `Eph.3.13` from `Eph`, inherited `true`; `Eph.3.14` from `Eph`, inherited `true`; `Eph.3.15` from `Eph`, inherited `true`; `Eph.3.16` from `Eph`, inherited `true`; `Eph.3.17` from `Eph`, inherited `true`; `Eph.3.18` from `Eph`, inherited `true`; `Eph.3.19` from `Eph`, inherited `true`; `Eph.3.20` from `Eph`, inherited `true`; `Eph.3.21` from `Eph`, inherited `true`.

Assertion 2:

- `subject`: `composition.epistle-to-the-ephesians`
- `title`: “The Epistle to the Ephesians”
- `relation`: `composition`
- `profile`: `catholic-traditional-v1`
- `label`: “(Philemon; Colossians; Ephesians; Philippians), 61”
- `disposition`: `disputed`
- `answerability`: `answerable`
- `basis_class`: `traditional-catholic`
- `precision`: `year`
- Source IDs: `artifact.catholic-encyclopedia.volume-11.new-york-1911.newadvent-11567b-bff0dda8`.
- Source reach: `Eph.3.13` from `Eph`, inherited `true`; `Eph.3.14` from `Eph`, inherited `true`; `Eph.3.15` from `Eph`, inherited `true`; `Eph.3.16` from `Eph`, inherited `true`; `Eph.3.17` from `Eph`, inherited `true`; `Eph.3.18` from `Eph`, inherited `true`; `Eph.3.19` from `Eph`, inherited `true`; `Eph.3.20` from `Eph`, inherited `true`; `Eph.3.21` from `Eph`, inherited `true`.

### Gradual — `gradual`

Appointed references: Psalm 101:16-17.

Loci: `Ps.101.16`, `Ps.101.17`.

Corpus status: `composition-only`. Publication status: `composition-only`. Requested profile: `catholic-comprehensive-v1`.

Assertion 1:

- `subject`: `critical.psalms.latest-composition-boundary`
- `title`: “The latest composition boundary shared by the Psalms”
- `relation`: `composition`
- `profile`: `catholic-critical-v1`
- `label`: “before the Maccabean period, around 165 B.C.; no individual psalm can be dated securely”
- `disposition`: `preferred`
- `answerability`: `answerable`
- `basis_class`: `catholic-critical`
- `precision`: `boundary`
- Source IDs: `passage.united-states-conference-of-catholic-bishops.new-american-bible-revised-edition.english-usccb-web-2026-07-28.psalms-introduction`.
- Source reach: `Ps.101.16` from `Ps`, inherited `true`; `Ps.101.17` from `Ps`, inherited `true`.

### Alleluia — `alleluia`

Appointed references: Psalm 97:1.

Loci: `Ps.97.1`.

Corpus status: `dated`. Publication status: `dated`. Requested profile: `catholic-comprehensive-v1`.

Assertion 1:

- `subject`: `critical.psalms.latest-composition-boundary`
- `title`: “The latest composition boundary shared by the Psalms”
- `relation`: `composition`
- `profile`: `catholic-critical-v1`
- `label`: “before the Maccabean period, around 165 B.C.; no individual psalm can be dated securely”
- `disposition`: `preferred`
- `answerability`: `answerable`
- `basis_class`: `catholic-critical`
- `precision`: `boundary`
- Source IDs: `passage.united-states-conference-of-catholic-bishops.new-american-bible-revised-edition.english-usccb-web-2026-07-28.psalms-introduction`.
- Source reach: `Ps.97.1` from `Ps`, inherited `true`.

Assertion 2:

- `subject`: `life-of-christ.nativity`
- `title`: “The Nativity of Our Lord”
- `relation`: `prophetic-referent`
- `profile`: `catholic-traditional-v1`
- `label`: “the year of Rome 750 which he styles 3 B.C.”
- `disposition`: `disputed`
- `answerability`: `answerable`
- `basis_class`: `reported-traditional`
- `precision`: `year`
- Source IDs: `artifact.catholic-encyclopedia.volume-3.new-york-1908.newadvent-03738a-5eb03e5b`.
- Source reach: `Ps.97.1` from `Ps.67 Ps.95 Ps.96 Ps.97`, inherited `true`.

Assertion 3:

- `subject`: `life-of-christ.nativity`
- `title`: “The Nativity of Our Lord”
- `relation`: `prophetic-referent`
- `profile`: `catholic-traditional-v1`
- `label`: “probably the year 7 B.C.”
- `disposition`: `disputed`
- `answerability`: `answerable`
- `basis_class`: `traditional-catholic`
- `precision`: `approximate-year`
- Source IDs: `artifact.catholic-encyclopedia.volume-3.new-york-1908.newadvent-03731a-f5f96f04`.
- Source reach: `Ps.97.1` from `Ps.67 Ps.95 Ps.96 Ps.97`, inherited `true`.

The two Nativity labels are competing `prophetic-referent` assertions, not
dates of Psalm composition. The first remains `reported-traditional` and
`disputed`. Its checked citation is John Gerard, “General Chronology,” *The
Catholic Encyclopedia*, vol.3 (New York: Robert Appleton Company, 1908),
“Christian era,” first paragraph, sentence beginning “It is supposed by many”;
New Advent transcription by Rick McCarty,
https://www.newadvent.org/cathen/03738a.htm#Christian . Registered access
2026-08-26; direct recheck 2026-09-05. SCR-023 and COV-010 supply the full
bundle and exact registered/fresh artifact distinction above and below.
“Christmas” does not identify this witness. The second label and its separate
03731a source remain unchanged; no merged Nativity date is inferred.

### Gospel — `gospel`

Appointed references: Luke 14:1-11.

Loci: `Luke.14.1`, `Luke.14.2`, `Luke.14.3`, `Luke.14.4`, `Luke.14.5`, `Luke.14.6`, `Luke.14.7`, `Luke.14.8`, `Luke.14.9`, `Luke.14.10`, `Luke.14.11`.

Corpus status: `composition-only`. Publication status: `composition-only`. Requested profile: `catholic-comprehensive-v1`.

Assertion 1:

- `subject`: `composition.gospel-of-luke`
- `title`: “The Gospel of St Luke”
- `relation`: `composition`
- `profile`: `catholic-traditional-v1`
- `label`: “About the year 70”
- `disposition`: `disputed`
- `answerability`: `answerable`
- `basis_class`: `traditional-catholic`
- `precision`: `approximate-year`
- Source IDs: `artifact.catholic-encyclopedia.volume-14.new-york-1912.newadvent-14530a-0a19aa2c`.
- Source reach: `Luke.14.1` from `Luke`, inherited `true`; `Luke.14.10` from `Luke`, inherited `true`; `Luke.14.11` from `Luke`, inherited `true`; `Luke.14.2` from `Luke`, inherited `true`; `Luke.14.3` from `Luke`, inherited `true`; `Luke.14.4` from `Luke`, inherited `true`; `Luke.14.5` from `Luke`, inherited `true`; `Luke.14.6` from `Luke`, inherited `true`; `Luke.14.7` from `Luke`, inherited `true`; `Luke.14.8` from `Luke`, inherited `true`; `Luke.14.9` from `Luke`, inherited `true`.

Assertion 2:

- `subject`: `composition.gospel-of-luke`
- `title`: “The Gospel of St Luke”
- `relation`: `composition`
- `profile`: `catholic-traditional-v1`
- `label`: “before the end of the Roman imprisonment, when the Acts was finished”
- `disposition`: `disputed`
- `answerability`: `answerable`
- `basis_class`: `traditional-catholic`
- `precision`: `relative`
- Source IDs: `passage.pontifical-biblical-commission.de-auctore-tempore-et-veritate-evangeliorum-marci-et-lucae.latin-aas-4-1912.responsa-i-ix`.
- Source reach: `Luke.14.1` from `Luke`, inherited `true`; `Luke.14.10` from `Luke`, inherited `true`; `Luke.14.11` from `Luke`, inherited `true`; `Luke.14.2` from `Luke`, inherited `true`; `Luke.14.3` from `Luke`, inherited `true`; `Luke.14.4` from `Luke`, inherited `true`; `Luke.14.5` from `Luke`, inherited `true`; `Luke.14.6` from `Luke`, inherited `true`; `Luke.14.7` from `Luke`, inherited `true`; `Luke.14.8` from `Luke`, inherited `true`; `Luke.14.9` from `Luke`, inherited `true`.

Only composition assertions are supplied. The record carries no narrated-event
date for Luke 14:1–11. An event row must state the absence, retaining the
Sabbath-meal and journey context established by SCR-005, not borrow a date from
Nain, a commentary, or another Gospel episode. The two composition alternatives
remain `disputed` rather than being averaged or silently preferred.

### Offertory — `offertory`

Appointed references: Psalm 39:14-15.

Loci: `Ps.39.14`, `Ps.39.15`.

Corpus status: `composition-only`. Publication status: `composition-only`. Requested profile: `catholic-comprehensive-v1`.

Assertion 1:

- `subject`: `critical.psalms.latest-composition-boundary`
- `title`: “The latest composition boundary shared by the Psalms”
- `relation`: `composition`
- `profile`: `catholic-critical-v1`
- `label`: “before the Maccabean period, around 165 B.C.; no individual psalm can be dated securely”
- `disposition`: `preferred`
- `answerability`: `answerable`
- `basis_class`: `catholic-critical`
- `precision`: `boundary`
- Source IDs: `passage.united-states-conference-of-catholic-bishops.new-american-bible-revised-edition.english-usccb-web-2026-07-28.psalms-introduction`.
- Source reach: `Ps.39.14` from `Ps`, inherited `true`; `Ps.39.15` from `Ps`, inherited `true`.

### Communion — `communion`

Appointed references: Psalm 70:16-18.

Loci: `Ps.70.16`, `Ps.70.17`, `Ps.70.18`.

Corpus status: `dated`. Publication status: `dated`. Requested profile: `catholic-comprehensive-v1`.

Assertion 1:

- `subject`: `critical.psalms.latest-composition-boundary`
- `title`: “The latest composition boundary shared by the Psalms”
- `relation`: `composition`
- `profile`: `catholic-critical-v1`
- `label`: “before the Maccabean period, around 165 B.C.; no individual psalm can be dated securely”
- `disposition`: `preferred`
- `answerability`: `answerable`
- `basis_class`: `catholic-critical`
- `precision`: `boundary`
- Source IDs: `passage.united-states-conference-of-catholic-bishops.new-american-bible-revised-edition.english-usccb-web-2026-07-28.psalms-introduction`.
- Source reach: `Ps.70.16` from `Ps`, inherited `true`; `Ps.70.17` from `Ps`, inherited `true`; `Ps.70.18` from `Ps`, inherited `true`.

Assertion 2:

- `subject`: `israel.monarchy.david-flight-from-absalom`
- `title`: “David's flight from the face of Absalom”
- `relation`: `historical-setting`
- `profile`: `catholic-traditional-v1`
- `label`: “when he fled from the face of his son Absalom”
- `disposition`: `preferred`
- `answerability`: `answerable`
- `basis_class`: `scripture`
- `precision`: `relative`
- Source IDs: `bible:douay-rheims:Ps.3.1`.
- Source reach: `Ps.70.16` from `Ps.62 Ps.70`, inherited `true`; `Ps.70.17` from `Ps.62 Ps.70`, inherited `true`; `Ps.70.18` from `Ps.62 Ps.70`, inherited `true`.

Assertion 3:

- `subject`: `israel.exile.first-captivity`
- `title`: “The first captivity of Juda, under Joakim”
- `relation`: `superscription-setting`
- `profile`: `catholic-traditional-v1`
- `label`: “A.M. 3398”
- `disposition`: `alternate`
- `answerability`: `answerable`
- `basis_class`: `reported-excluded`
- `precision`: `year`
- Source IDs: `passage.george-leo-haydock.douay-rheims-with-haydock-commentary.2014-loreto-feeney-memorial.psalm-70-captivities-usher-chronology`.
- Source reach: `Ps.70.16` from `Ps.70`, inherited `true`; `Ps.70.17` from `Ps.70`, inherited `true`; `Ps.70.18` from `Ps.70`, inherited `true`.

Assertion 4:

- `subject`: `israel.exile.first-captivity`
- `title`: “The first captivity of Juda, under Joakim”
- `relation`: `superscription-setting`
- `profile`: `catholic-traditional-v1`
- `label`: “In the third year of the reign of Joakim, king of Juda”
- `disposition`: `preferred`
- `answerability`: `answerable`
- `basis_class`: `scripture`
- `precision`: `relative`
- Source IDs: `bible:douay-rheims:Dan.1.1`.
- Source reach: `Ps.70.16` from `Ps.70`, inherited `true`; `Ps.70.17` from `Ps.70`, inherited `true`; `Ps.70.18` from `Ps.70`, inherited `true`.

The David/Absalom `historical-setting`, first-captivity `superscription-setting`,
and Psalter `composition` boundary answer different questions. The A.M. label
remains `alternate`, `reported-excluded`, and `answerable` exactly as recorded;
it is not promoted to the preferred setting or converted to a B.C. year.
The scriptural Joakim label remains the preferred assertion of its setting.
Theodoret's Moses/law reading and Bellarmine's personal David reading are
reception, not replacements for these corpus assertions.

### Page-2 orientation and bounded missing fields

The page inventories the seven distinct direct scriptural selections once in
Catholic canonical order, keeping composition separate from a narrated event.
The five psalms precede Luke and Ephesians; their internal order follows the
appointed Psalm loci. The table below states what this join supports beyond
the immutable chronology. It does not manufacture a historical dossier where
the lanes supplied only literary context.

| Dossier | Supported orientation | Missing evidence and the bound to carry |
| --- | --- | --- |
| Offertory, Ps.39:14–15 | Remembered deliverance, obedient thanksgiving and renewed threatened life; SCR-006,014. Reception applies the suffering voice to Christ and his members; PAT-006,013,017. | No source in the join identifies a composition place, named enemies, or precise first audience of these selected verses. The corpus supplies the common composition boundary only. |
| Communion, Ps.70:16–18 | Aging petitioner instructed from youth, with testimony to a coming generation in the continuation; SCR-007,015. Distinct personal and corporate interpretations; PAT-007,018,022. | The record's attributed settings remain typed; do not infer a composition place or conflate David, first captivity, and Moses/law reception. No independent current critical dossier was supplied. |
| Introit, Ps.85:1,3,5 | Davidic title; needy but trusting servant, continuing danger and all-nations horizon; SCR-001,011. | Title is attribution, not a named historical crisis. No composed-at location or precise audience was established in the whole-psalm and received-commentary checks. |
| Alleluia, Ps.97:1 | Israel's salvation made manifest to nations and all creation; SCR-004,013. | No particular rescue event is explicitly named. Neither Red Sea nor Presentation is a narrated episode in the psalm; the Nativity is only the inherited prophetic-referent relationship. |
| Gradual, Ps.101:16–17 | Afflicted person and restored Sion, peoples and kings gathered for worship; SCR-003,012. | Restored Sion/Jerusalem is the poem's referent, not a demonstrated location of composition. No precise rebuilding date or writer's biography was established by these sources. |
| Gospel, Luke 14:1–11 | Unnamed leading Pharisee's house on a Sabbath; surrounding journey toward Jerusalem at Luke 13:22; Luke 13–15 read, SCR-005,009–010. | No town, named host, or event date was supplied. COV-008 reports the extent of Gadenz's introduction and a direct Jerome record with competing ancient testimony, but does not freshly verify that provenance: no new Achaia/Boeotia composition claim is authorized from the record alone. The join does not supply a complete modern authorship/introduction dossier. |
| Epistle, Ephesians 3:13–21 | Paul's Gentile mission, imprisonment/affliction for recipients, shared access and divine dwelling, continued exhortation to unity; all six chapters read, SCR-002,008,016. | The join does not establish the place of imprisonment or a full modern authorship/first-recipient/geography dossier. The inspected USCCB chapter notes concern the prayer, not a complete introduction. Preserve the corpus's traditional composition alternatives and state missing precision rather than adding a critical date from elsewhere. |

The bounded missing modern-introduction and geography coverage is legitimate
section evidence, not permission to omit the page or fill it from memory. The
corpora actually checked were the complete selected biblical contexts in
English, the appointed-locus Latin/English comparisons, the passage-led
patristic and saintly witnesses in the matrix, and the source records named by
COV-008. No exhaustive critical-introduction search or fresh Gadenz/Jerome
provenance collation is claimed. Full human bibliographic metadata for
chronology-source IDs not expanded by the joined lanes is not reconstructed
from their hashes; the projection and supplied source labels remain the exact
chronological evidence carried here.

## Interpretive-proposal audit

Select six proposals, IP-1–IP-6, from PRE-007–012. Each names at least two
appointed elements, a connecting mechanism, fruit, what separate exposition
misses, and its strongest limit. These are proposals even where their anchors
have documented reception. Their novelty classifications below reproduce the
precedent lane's words without upgrading a near analogue into exact precedent
or a bounded negative into universal originality. The shared search boundary
is PRE-003 as stated above, with each proposal's targeted family preserved in
its exact PRE finding. Use one compact exploratory notice in the reader-facing
section; retain substantive field labels, especially its final Strongest limit.

### IP-1 — Distorted fullness and receptive plenitude

**Selected lane finding:** PRE-007

**Anchors:** Gospel Luke 14:2–4; Epistle Ephesians 3:19–20; Secret purification for participation.

**Mechanism:** Compare the dropsical body, spiritual readings of disordered desire, and the Epistle’s fullness received from God, with the Secret asking cleansing rather than securing capacity by accumulation. The contrast makes receptivity, not mere expansion, the criterion of fruitful fullness.

**Fruit and what separate exposition misses:** A spiritual examination of acquisitiveness and the capacity to receive a gift; the repeated image of being full links ritual moments that isolated exposition would leave unrelated.

**Nearest precedent or analogue:** GPT 51, “From unvoid grace to heavenly fullness,” sections/50-interpretive.tex:80–92; Anthony XVII §§8–12 has the same Gospel but Ephesians 4. No checked precedent supplied this exact three-element contrast.

**Novelty classification:** near analogue located

**Strongest limit:** The man’s disease is no evidence of personal sin. Divine fullness is not a fluid, quantity, or physiological cure, and the spiritual reading must remain attributed to Ambrose or Anthony rather than asserted as Luke’s diagnosis.

The following complete finding preserves the exact targeted search family, external comparison boundary, qualification, and classification supplied by precedent-search.

#### PRE-007 — precedent-search

Claim: For C1, pathological swelling beside divine plenitude has a near analogue in an earlier guide’s contrast between fruitful abundance and accumulated surplus.

Evidence:

- src/gpt/liturgy/roman-rite/1962/propers/temporal/51-eleventh-after-pentecost/sections/50-interpretive.tex, From unvoid grace to heavenly fullness, lines 80–92: surplus is followed through reception, opened senses, offering, and heavenly remedy rather than stockpiling.
- Anthony, Dominica XVII, §§8–12 (PRE-005 receipt): an older same-Gospel treatment of distorted desire; its paired Pauline reading is Ephesians 4, not Ephesians 3.

Notes and limits: Classification: near analogue located. Conjunction searched: Gospel’s dropsical man (Luke 14:2–4), Epistle’s filling with divine fullness (Eph. 3:19–20), and Secret’s cleansing for participation. Corpus: PRE-003, plus both acquired Anthony sermons and The Liturgical Year continuation’s Sixteenth-Sunday chapter. Search families: hydrop-/dropsy/swelling/inflation with fullness/plenitudo/abundance. No inspected precedent supplied this exact three-element contrast. Its possible fruit is distinguishing receptivity from acquisitive expansion; separate commentary misses the two different images of being full. Disease must not be treated as proof of personal sin or divine plenitude as a physiological quantity; analogy is not a clinical explanation. Re-entry on 2026-09-05: the unchanged corpus and all eight search families were replayed, the named nearest passages re-inspected, and the two Anthony pages and complete Liturgical Year volume freshly retrieved. PRE-005 now supplies complete Anthony citation metadata; PRE-006 supplies the corrected 1909 continuation identity. No novel universal-priority claim is made.

### IP-2 — Grace across daily, lifelong, and final horizons

**Selected lane finding:** PRE-008

**Anchors:** Collect praeveniat/sequatur/semper; Communion Psalm 70:17–18, youth to old age; Postcommunion praesens/futurum; the Introit’s all-day cry falls within the reached field.

**Mechanism:** Coordinate assistance that precedes and follows action with a lifetime of teaching and the prayer for bodily help now and hereafter. The different scales of time overlap in worship rather than forming stages on one clock.

**Fruit and what separate exposition misses:** Lifelong dependence can hold daily fidelity and ultimate hope together. Separate commentary misses how remembered youth and anticipated bodily help qualify the meaning of constant present activity.

**Nearest precedent or analogue:** GPT 55, “The proper’s several clocks,” sections/50-interpretive.tex and scope IP-3:678–693; GPT 52, “Mercy’s longer clock,” sections/50-interpretive.tex:40–53. No inspected predecessor coordinates these present three texts.

**Novelty classification:** near analogue located

**Strongest limit:** No timetable of grace, longevity, uninterrupted health, or sequence of medical effects follows. These temporal expressions are not biblical dates, and the source psalms do not establish one historical speaker.

The following complete finding preserves the exact targeted search family, external comparison boundary, qualification, and classification supplied by precedent-search.

#### PRE-008 — precedent-search

Claim: For C2, grace going before and following, youth through old age, and help now and hereafter have near precedents in liturgical treatments of several simultaneous kinds of time.

Evidence:

- src/gpt/liturgy/roman-rite/1962/propers/temporal/55-fifteenth-after-pentecost/sections/50-interpretive.tex, The proper’s several clocks; research/scope.md, IP-3, lines 678–693: daily, seasonal, opportune, and awaited time are coordinated without becoming a timetable.
- src/gpt/liturgy/roman-rite/1962/propers/temporal/52-twelfth-after-pentecost/sections/50-interpretive.tex, Mercy’s longer clock, lines 40–53: continuing praise, day/night prayer, continuing care, and anticipated return.

Notes and limits: Classification: near analogue located. Conjunction searched: Collect praeveniat/sequatur/semper, Communion youth/old age (Ps. 70:17–18), and Postcommunion praesens/futurum; the Introit’s all-day cry may be included within this reached temporal field. Corpus and external chapter boundary: PRE-003. Terms included before/follow/preven-/praeven-/sequa-, youth/iuvent-/senect-/old age, present/future and clocks. No inspected predecessor coordinates the present three texts. Its possible fruit is lifelong dependence crossing the daily and eschatological horizons; it must not promise longevity, uninterrupted health, or a timetable of grace. Re-entry on 2026-09-05: the unchanged corpus and all eight search families were replayed, the named nearest passages re-inspected, and the two Anthony pages and complete Liturgical Year volume freshly retrieved. PRE-005 now supplies complete Anthony citation metadata; PRE-006 supplies the corrected 1909 continuation identity. No novel universal-priority claim is made.

### IP-3 — Interior hospitality and room for another

**Selected lane finding:** PRE-009

**Anchors:** Epistle Christ dwelling in hearts and rooted/founded charity; Gradual God building Sion; Gospel disputed table places, da huic locum/recumbe.

**Mechanism:** Extend the documented inward-dwelling and common-building relation to the way guests yield social room. Receiving Christ in the heart can be considered beside receiving one’s place among others, rather than treating inwardness as possession of a private religious space.

**Fruit and what separate exposition misses:** Hospitality and ecclesial humility receive a concrete social question: how does common life change the way a person occupies a place? Element-by-element reading misses the transition from inner dwelling to room shared with others.

**Nearest precedent or analogue:** PRE-009 separately says “precedent located” for Epistle–Gradual–Alleluia indwelling/building/praise in the 1909 Liturgical Year continuation, pp.359,363; its classification for the fuller Epistle–Gradual–Gospel proposal retained here is “near analogue located.” Nearest further analogues: GPT 54 “The protective camp opens toward the desired courts,” sections/50-interpretive.tex:20–31; GPT 41 Secret commentary, main.tex:245–260.

**Novelty classification:** near analogue located

**Strongest limit:** Psalmic Sion, Pauline hearts and the Gospel dining room have different referents. No architectural code, compiler’s program, identification of the meal as Eucharist, or narrative seating of the dismissed man follows. This proposal does not add THE-010’s unsearched Secret/guest-host conjunction.

The following complete finding preserves the exact targeted search family, external comparison boundary, qualification, and classification supplied by precedent-search.

#### PRE-009 — precedent-search

Claim: For C3, Christ dwelling in hearts and God building Sion have a located prior liturgical relation; adding the Gospel’s contested table places is a further extension with a near analogue.

Evidence:

- The Liturgical Year continuation, XI, Sixteenth Sunday, pp. 359 and 363 (PRE-006 receipt): interior indwelling develops toward the Church’s divine construction and common praise.
- src/gpt/liturgy/roman-rite/1962/propers/temporal/54-fourteenth-after-pentecost/sections/50-interpretive.tex, The protective camp opens toward the desired courts, lines 20–31: divine protection orders desire toward God’s dwelling rather than possession.
- src/gpt/liturgy/roman-rite/1962/propers/temporal/41-second-after-pentecost/main.tex, Secret commentary, lines 245–260: invited guests receive purification and progressive transformation instead of certifying their own worthiness.

Notes and limits: Classification: precedent located for Epistle–Gradual–Alleluia indwelling/building/praise; near analogue located for the fuller Epistle–Gradual–Gospel relation. Conjunction searched: habitare in cordibus, radicati/fundati, aedificavit Sion, and da huic locum/recumbe at the banquet. PRE-003 corpus plus the two Antonian sermons and The Liturgical Year continuation chapter; lexical families dwelling/building/Sion, heart, house/table/room/place. A proposal involving shared space can ask how interior hospitality changes social room-making, a relation separate expositions may miss. The psalm’s Zion, Pauline heart, and Gospel dining room remain different referents; no architectural code or established compiler programme follows. Re-entry on 2026-09-05: the unchanged corpus and all eight search families were replayed, the named nearest passages re-inspected, and the two Anthony pages and complete Liturgical Year volume freshly retrieved. PRE-005 now supplies complete Anthony citation metadata; PRE-006 supplies the corrected 1909 continuation identity. No novel universal-priority claim is made.

### IP-4 — Lowliness compatible with enlargement

**Selected lane finding:** PRE-010

**Anchors:** Introit inclined divine ear and needy petitioner; Epistle bent knees and height/depth; Gospel lower place, ascende superius, humiliation/exaltation.

**Mechanism:** Compare divine inclination to hear, bodily acknowledgment of weakness in prayer, growth in charity and honor received through invitation. Lowering and raising do different work in these texts: lowliness need not mean worthlessness, and enlargement need not be self-promotion.

**Fruit and what separate exposition misses:** A bodily imagination of prayer can connect humility with readiness to receive and act. Separate exposition may make low position and height into a single moral ranking and miss their different functions.

**Nearest precedent or analogue:** GPT 50, “Downcast eyes can accompany a lifted soul,” main.tex:80–81; GPT 55 Themes unit 1, divine inclination and raised appeal. Anthony XVI §§7,12 and XVII §§13–16 were checked, but no inspected text joins all four motions. THE-012 contributes only within this reached field.

**Novelty classification:** near analogue located

**Strongest limit:** Posture does not prove virtue. An anthropomorphic ear, human knees, dimensions and a seating parable are different kinds of speech. Paul does not map his four dimensions onto ritual gestures; neither numerology nor liturgical choreography is established.

The following complete finding preserves the exact targeted search family, external comparison boundary, qualification, and classification supplied by precedent-search.

#### PRE-010 — precedent-search

Claim: For C4, downward bodily posture and upward Godward movement have a close Triptych precedent, while the present combination of divine inclination, kneeling, dimensions, and the host’s invitation extends it.

Evidence:

- src/gpt/liturgy/roman-rite/1962/propers/temporal/50-tenth-after-pentecost/main.tex:80–81, Downcast eyes can accompany a lifted soul: the publican’s lowered eyes are joined to the Offertory’s lifted soul and the Gradual’s petition about the eye.
- src/gpt/liturgy/roman-rite/1962/propers/temporal/55-fifteenth-after-pentecost/sections/synthesis/10-themes-and-movement.tex, unit 1: the Lord’s inclined ear answers the servant’s raised appeal.

Notes and limits: Classification: near analogue located. Conjunction searched: Introit inclina/inops, Epistle flecto genua and sublimitas/profundum, Gospel recumbe/ascende superius and humiliation/exaltation. PRE-003 corpus, Anthony XVI §§7,12 and XVII §§13–16, and The Liturgical Year continuation chapter were checked within this field. Terms included kneel/genua, downcast/lower/humil-, height/sublim-/ascen-/exalt-/lift. No inspected text joins all four motions. Possible fruit: honor received from the host can differ from self-promotion, while kneeling remains compatible with enlargement in charity. Bodily posture alone neither establishes virtue nor licenses mapping Paul’s four dimensions to ritual gestures. Re-entry on 2026-09-05: the unchanged corpus and all eight search families were replayed, the named nearest passages re-inspected, and the two Anthony pages and complete Liturgical Year volume freshly retrieved. PRE-005 now supplies complete Anthony citation metadata; PRE-006 supplies the corrected 1909 continuation identity. No novel universal-priority claim is made.

### IP-5 — The petitioner also receives correction

**Selected lane finding:** PRE-011

**Anchors:** Offertory Psalm 39:14–15, shame for those seeking the singer’s life; Gospel Luke 14:9–11, shame at displaced precedence and exaltation of the humble.

**Mechanism:** Place the justified plea for deliverance beside the possibility that the praying person must relinquish pride. The return of shame toward self-examination can prevent reliance on God from becoming a certificate of superiority over others.

**Fruit and what separate exposition misses:** Prayer for protection and willingness to be corrected can coexist. Separate reading misses that the worshipper who rightly asks rescue also hears a warning about self-exaltation.

**Nearest precedent or analogue:** GPT 50 “Divine leveling without competitive self-ranking,” main.tex:76–77 and the first two paragraphs of sections/35-source-grounded-synthesis.tex. No exact Psalm 39–Luke 14 relation was located. The continuation’s chapter was included in the targeted check.

**Novelty classification:** near analogue located

**Strongest limit:** The threatened singer is not to blame for the threat; real harm remains real. Enemies are not simply fellow guests or modern opponents. This is a proposal about the worshipper’s response, not a new literal identity of the biblical characters or a denial of justice.

The following complete finding preserves the exact targeted search family, external comparison boundary, qualification, and classification supplied by precedent-search.

#### PRE-011 — precedent-search

Claim: For C5, enemy-directed humiliation returned upon the praying self has a particularly close analogue in the Tenth-Sunday guide’s Divine leveling without competitive self-ranking.

Evidence:

- src/gpt/liturgy/roman-rite/1962/propers/temporal/50-tenth-after-pentecost/main.tex:76–77: the Introit’s humbled adversaries are compared with the Gospel’s self-exalters to distinguish protection from moral scorekeeping.
- src/gpt/liturgy/roman-rite/1962/propers/temporal/50-tenth-after-pentecost/sections/35-source-grounded-synthesis.tex, opening two paragraphs: religious goods cannot become self-grounded verdicts of superiority.

Notes and limits: Classification: near analogue located. Conjunction searched: Offertory confundantur/revereantur against those seeking the singer’s life, and Gospel cum rubore/da huic locum before fellow guests. Corpus PRE-003 and The Liturgical Year continuation chapter checked with shame/confund-/rubor, enemy/adversary, and humility/rank/self terms. The exact Psalm 39–Luke 14 relation was not located. Possible fruit: the person seeking deliverance also submits to correction of pride, a reversal missed if prayer and banquet are read independently. The threatened singer must not be blamed for the threat, and concrete enemies cannot simply be identified with fellow guests or modern opponents. Re-entry on 2026-09-05: the unchanged corpus and all eight search families were replayed, the named nearest passages re-inspected, and the two Anthony pages and complete Liturgical Year volume freshly retrieved. PRE-005 now supplies complete Anthony citation metadata; PRE-006 supplies the corrected 1909 continuation identity. No novel universal-priority claim is made.

### IP-6 — A new song in an aging voice

**Selected lane finding:** PRE-012

**Anchors:** Alleluia Psalm 97:1, canticum novum; Communion Psalm 70:17–18, youth and old age; Postcommunion renova.

**Mechanism:** Consider fresh praise and sacramental renewal in the same aging worshipper whose life depends on remembered divine teaching. The conjunction proposes that renewal need not erase a received history or imitate chronological youth.

**Fruit and what separate exposition misses:** Hope for older worshippers and intergenerational praise: the new can be sung through an old voice. Separate commentaries can leave newness, remembrance and aging in different compartments and miss their coexistence.

**Nearest precedent or analogue:** Nearest partial relations: GPT 55 “Speech received, song supplied”; its Psalm 91 old-age context in sections/30-commentary.tex:80–82; GPT 48’s Psalm 70 old-age context in scope:21 and main.tex:59. None forms this conjunction. PRE-012 records both the primary co-occurrence search and the second targeted age/song check; unsearched psalm homilies, poetry, music, and other sermon collections remain outside it.

**Novelty classification:** not located in the checked corpus

**Strongest limit:** The chants do not identify one original historical speaker. Renewal promises no reversal of biological aging, and shared novum/renova does not establish intentional textual design, musical innovation, initiation, or a theory of liturgical reform.

The following complete finding preserves the exact targeted search family, external comparison boundary, qualification, and classification supplied by precedent-search.

#### PRE-012 — precedent-search

Claim: For C6, the Alleluia’s new song, the Communion’s old-age singer, and the Postcommunion’s renewal were not located as a combined interpretation in the checked corpus.

Evidence:

- src/gpt/liturgy/roman-rite/1962/propers/temporal/55-fifteenth-after-pentecost/sections/50-interpretive.tex, Speech received, song supplied: restored speech is joined to a new canticle; this is a different relation.
- src/gpt/liturgy/roman-rite/1962/propers/temporal/55-fifteenth-after-pentecost/sections/30-commentary.tex:80–82: Psalm 91’s broader context includes fruitfulness in old age, without making an old-age/new-song conjunction.
- src/gpt/liturgy/roman-rite/1962/propers/temporal/48-eighth-after-pentecost/research/scope.md:21 and main.tex:59: Psalm 70’s old-age speaker is noticed as canonical context, without the target’s Alleluia or Postcommunion.

Notes and limits: Classification: not located in the checked corpus. Conjunction searched: Alleluia Ps. 97:1 canticum novum, Communion Ps. 70:17–18 youth/old age, Postcommunion renova. PRE-003 corpus plus both Anthony sermons and the complete 1909 Liturgical Year continuation’s Sixteenth-Sunday chapter were searched and the nearest age/song hits inspected. A second targeted ripgrep used old.age, senect-, grey/gray hair and youth, then checked new.song/new.canticle/canticum.novum/renew in the resulting guide contexts. This bound excludes unsearched psalm homilies, later poetry and music, and other sermon collections. Possible fruit: renewal and fresh praise need not imply chronological youth; separate commentary misses their coexistence in the same ageing worshipper. The chants do not identify their historical speakers, and spiritual renewal promises no reversal of biological ageing. Re-entry on 2026-09-05: the unchanged corpus and all eight search families were replayed, the named nearest passages re-inspected, and the two Anthony pages and complete Liturgical Year volume freshly retrieved. PRE-005 now supplies complete Anthony citation metadata; PRE-006 supplies the corrected 1909 continuation identity. No novel universal-priority claim is made.

PRE-013 and PRE-014 remain useful corroborating analogue records, but are not
seventh and eighth proposals. Their action/justice and bodily-help relations
already contribute to the source-grounded argument; selecting them again as
additional proposals would exceed the six-proposal scope and risk recap.
THE-009–011 are unselected for the precise precedent-coverage reasons recorded
above, rather than being silently represented as searched.

## Notable-and-quotable audit

Select CUL-001, CUL-003, CUL-004, CUL-005, and CUL-006. Their five changes of
register are ironic lyric time, hostile moral reversal, love poetry, comic
social satire, and political reversal. This meets the three-to-five gallery
requirement through verified wording and context rather than exegesis or bare
titles. Each complete lane entry below carries both texts and loci,
relationship strength, wording check, later context, translation/rights,
cultural payoff, and its controlling limit. All online primary witnesses and
necessary corroborants retain their exact title, responsible creator or body,
edition/date, public route, access date, and usable locus in the entry itself.

The common scriptural English is *The Bible, Douay-Rheims, Complete*,
Challoner revision, Project Gutenberg ebook 1581, released 1998-12-01, updated
2023-09-23; Richard Challoner, revision; Dennis McCarthy and Tad Book,
electronic production; https://www.gutenberg.org/ebooks/1581 ; consulted in
the registered verse artifacts on 2026-09-05. Its ebook number is not a year.
The extracts remain that historical English, not translations newly supplied
for the gallery. The following entries repeat their exact biblical loci so
that the pairings remain independently intelligible.

### CUL-001 — cultural-afterlife

Claim: Shakespeare redirects the Epistle’s “world without end” into the seemingly endless time a jealous lover spends waiting in Sonnet 57.

Evidence:

- The Bible, Douay-Rheims, Complete, Challoner revision, Project Gutenberg eBook 1581, released 1998-12-01, updated 2023-09-23; Richard Challoner (revision), Dennis McCarthy and Tad Book (electronic production); https://www.gutenberg.org/ebooks/1581 ; consulted in registered repository verse artifacts on 2026-09-05. Ephesians 3:21, src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-56-ephesians-10c79be0/56-ephesians.tsv, physical line 67: “world without end”.
- William Shakespeare, Shakespeare’s Sonnets, Sonnet 57, line 5: “Nor dare I chide the world-without-end hour”; read all fourteen lines, with particular context in lines 1–6 and 9–14. Folger Shakespeare Library edition, edited by Barbara A. Mowat and Paul Werstine with Michael Poston and Rebecca Niles; FDT 0.9.0.1, created 2015-07-31; https://www.folger.edu/explore/shakespeares-works/shakespeares-sonnets/read/57/ ; complete text https://folger-main-site-assets.s3.amazonaws.com/uploads/2022/11/shakespeares-sonnets_TXT_FolgerShakespeare.txt ; accessed 2026-09-05, physical text lines 964–979.

Notes and limits: Qualifying literary and ironic candidate. Relationship: exact English idiom, hyphenated into an adjective; a biblical/liturgical echo, with no documentary proof of dependence specifically on Ephesians 3:21 or this Mass. Wording checked directly in the Folger edited primary text and the registered Challoner artifact. The phrase moves from doxological eternity to the oppressive subjective length of one hour, while the speaker presents himself as the beloved’s slave. Shakespeare’s original English is public domain in the United States; Folger’s modern editorial material and presentation have separate rights and are not declared public domain here. No new translation is needed; quote only the short line supplied. The identity of the beloved is unnecessary and not inferred. This iteration freshly retrieved and inspected the complete Folger text, including Sonnet 57 and its edition header; the sonnet webpage is supplied as the stable reader route, not a claim of a second fresh retrieval.

Exact acquisition receipts: see the public-identity receipt register below under CUL-001. Machine-local storage paths are omitted from this tracked brief.

### CUL-003 — cultural-afterlife

Claim: Nietzsche deliberately changes the Gospel’s promised exaltation of the humble into an accusation that humility desires exaltation.

Evidence:

- The Bible, Douay-Rheims, Complete, Challoner revision, Project Gutenberg eBook 1581, released 1998-12-01, updated 2023-09-23; Richard Challoner (revision), Dennis McCarthy and Tad Book (electronic production); https://www.gutenberg.org/ebooks/1581 ; consulted in registered repository verse artifacts on 2026-09-05. Luke 14:11, src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-49-luke-d8269c33/49-luke.tsv, physical line 672: “he that humbleth himself shall be exalted”.
- Friedrich Nietzsche, Human, All Too Human: A Book for Free Spirits, translated by Alexander Harvey (Chicago: Charles H. Kerr & Company, 1908), History of the Moral Feelings, aphorism 87, printed p. 109: heading “Luke 18:14 Improved.” and text “He that humbleth himself wisheth to be exalted.” Project Gutenberg eBook 38145, released 2011-11-26; https://www.gutenberg.org/files/38145/38145-h/38145-h.htm ; accessed 2026-09-05; HTML physical lines 2477–2479, with aphorisms 82–89 inspected.
- This iteration inspected the retained full HTML at src/sources/works/friedrich-nietzsche/menschliches-allzumenschliches/editions/1908-harvey-english-gutenberg/artifacts/gutenberg-38145-html-7ba12804/source.html, including 1908 Chicago/Kerr title page, Alexander Harvey translation credit, and aphorisms 82–89; no new remote bytes retrieved.

Notes and limits: Qualifying hostile, ironic reversal with explicit scriptural dependence. Essential limit: Nietzsche names Luke 18:14, the parallel saying, not the appointed Luke 14:11; the exact saying is shared, so present this as an afterlife of wording heard in today’s Gospel, never as Nietzsche commenting on this pericope or Mass. The shift from “shall” to “wisheth” turns divine vindication into a psychological diagnosis of concealed ambition. The English quotation is Harvey’s 1908 translation, not a new translation and not the wording of Helen Zimmern or Walter Kaufmann. The 1908 edition is public domain in the United States by publication date; Project Gutenberg host boilerplate is distinct. Underlying work, named section and printed page checked in the full available Gutenberg edition; this electronic witness contains the three divisions listed in its own contents through aphorism 144, not every division of Nietzsche’s complete work.

### CUL-004 — cultural-afterlife

Claim: Elizabeth Barrett Browning echoes the Epistle’s spatial language for Christ’s charity when she measures her love for a human beloved in Sonnet 43.

Evidence:

- The Bible, Douay-Rheims, Complete, Challoner revision, Project Gutenberg eBook 1581, released 1998-12-01, updated 2023-09-23; Richard Challoner (revision), Dennis McCarthy and Tad Book (electronic production); https://www.gutenberg.org/ebooks/1581 ; registered repository text inspected 2026-09-05. Ephesians 3:18–19, src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-56-ephesians-10c79be0/56-ephesians.tsv, physical lines 64–65: ‘the breadth and length and height and depth’; the following verse names Christ’s charity. Complete appointed Ephesians 3:13–21 inspected.
- Elizabeth Barrett Browning, Sonnets from the Portuguese, sonnet XLIII, lines 2–3: ‘I love thee to the depth and breadth and height / My soul can reach’. The Caradoc Press, Bedford Park, 1906; transcription by David Price, Project Gutenberg eBook 2002, released 1999-12-01, updated 2026-08-20; https://www.gutenberg.org/cache/epub/2002/pg2002.txt ; accessed as registered artifact 2026-09-05. Complete sonnet inspected at physical lines 994–1007 of src/sources/works/elizabeth-barrett-browning/sonnets-from-the-portuguese/editions/1906-caradoc-press-gutenberg/artifacts/gutenberg-2002-text-b193a12e/source.txt (SHA-256 b193a12e83b20378cb0d25e97468ef0ed915b760732b8c1deeb3d6fe5d7ed65d).

Notes and limits: Qualifying literary echo, not a verbatim quotation or documented direct dependence. Browning reorders the dimensional nouns and omits length; the conjunction of love with the dimensional list makes the echo distinctive. The turn is toward a human beloved while soul, grace, faith, saints and God remain in the poem: do not describe it as eliminating religion. Original English; poem and 1906 printing have a United States public-domain basis, with Gutenberg boilerplate distinct. No new translation. No authorial acknowledgment of Ephesians was established. Registered exact source text and complete fourteen-line context re-inspected on this iteration; no fresh remote bytes fetched.

### CUL-005 — cultural-afterlife

Claim: Percy Fitzgerald’s Fatal Zero turns “Go up higher” into a joke about a dean’s social climbing among aristocrats.

Evidence:

- The Bible, Douay-Rheims, Complete, Challoner revision, Project Gutenberg eBook 1581, released 1998-12-01, updated 2023-09-23; Richard Challoner (revision), Dennis McCarthy and Tad Book (electronic production); https://www.gutenberg.org/ebooks/1581 ; consulted in registered repository verse artifacts on 2026-09-05. Luke 14:10–11, registered Luke TSV physical lines 671–672: “Friend, go up higher” and “he that humbleth himself shall be exalted”.
- Percy Fitzgerald, Fatal Zero, serial installment in All the Year Round, new series, volume I, 16 January 1869, printed p. 163, left column, paragraph beginning “Of course he had not heard of my fall in the world”; journal conducted by Charles Dickens (London, 1869). Exact words “Go up higher” and “he that humbleth himself” were visually collated on the original page. Facsimile volume https://upload.wikimedia.org/wikipedia/commons/0/04/All_the_Year_Round_-_Series_2_-_Volume_1.djvu ; page image https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/All_the_Year_Round_-_Series_2_-_Volume_1.djvu/page173-1920px-All_the_Year_Round_-_Series_2_-_Volume_1.djvu.jpg ; accessed 2026-09-05; digital leaf 173 = printed p. 163. Both columns read.
- Charles Dickens, letter to Mrs. James T. Fields, Glasgow, Wednesday 16 December 1868, paragraph identifying Fatal Zero as “by Percy Fitzgerald”; The Letters of Charles Dickens, edited by Mamie Dickens and Georgina Hogarth, volume III, 1836 to 1870 (London: Chapman and Hall, 1882), letter containing the Oliver Twist murder-reading discussion. Project Gutenberg eBook 25854, released 2008-06-20, https://www.gutenberg.org/cache/epub/25854/pg25854.txt ; accessed 2026-09-05, physical lines 7797–7798; header and surrounding letter inspected.
- This iteration visually re-inspected the whole registered p. 163 image at src/sources/works/all-the-year-round/new-series-volume-1/editions/1869-london-1869-facsimile/artifacts/commons-page-163-jpeg-5a4e3fe7/source.jpg. The complete controlling DjVu is held beside it at src/sources/works/all-the-year-round/new-series-volume-1/editions/1869-london-1869-facsimile/artifacts/commons-volume-djvu-ee0e25d7/source.djvu. Dickens’s title page and the 16 December 1868 letter were directly re-inspected in src/sources/works/charles-dickens/letters/editions/1882-macmillan-volume-3-gutenberg/artifacts/gutenberg-25854-text-dbc34492/source.txt; both source witnesses were read from registered bytes, with no new retrieval.

Notes and limits: Qualifying humorous, literary and social satire. The narrator recalls the dean preaching on “Go up higher”, then interprets his humility as a hope for promotion while watching him seek a place beside a lord. Thus the same banquet vocabulary becomes an accusation of status-seeking, with the theological maxim itself turned inside out. The verbal reuse is explicit; dependence on Luke’s saying is stronger than an independently similar phrase, but no dependence on this Mass or on the Douay-Rheims translation is asserted. These are a fictional narrator’s judgments, not verified events in a real dean’s biography; the narrator also concedes that he may be unfair. Original English, public-domain 1869 printing in the United States; modern Wikisource markup has separate licensing. Source attribution trap resolved: “Charles Dickens” in the running head names the journal’s conductor, not Fatal Zero’s author; Dickens’s own letter identifies Fitzgerald. The Gutenberg item’s currently retrieved title page says volume III, although some search metadata calls it volume II; cite the actual 1882 volume III title page. The separate volume-index webpage is unnecessary to this claim and is not a retained corroborant in this iteration.

### CUL-006 — cultural-afterlife

Claim: Senator Riegle reverses the Gospel’s rescue image during a 1977 gas-pricing debate by arguing that an ox sometimes belongs in its ditch.

Evidence:

- The Bible, Douay-Rheims, Complete, Challoner revision, Project Gutenberg eBook 1581, released 1998-12-01, updated 2023-09-23; Richard Challoner (revision), Dennis McCarthy and Tad Book (electronic production); https://www.gutenberg.org/ebooks/1581 ; consulted in registered repository verse artifacts on 2026-09-05. Luke 14:5, registered Luke verse artifact physical line 666: “an ox fall into a pit”; the complete verse asks whether one would immediately draw it out even on the sabbath.
- United States Congress, Congressional Record—Senate, 4 October 1977, printed p. 32287, right column, Mr. Riegle’s speech continuing from the left column; exact sentence: “Sometimes you have to leave the ox in the ditch, if that is where it belongs.” Government Publishing Office bound-record PDF, https://www.congress.gov/95/crecb/1977/10/04/GPO-CRECB-1977-pt25-5-2.pdf ; original registered retrieval dated 2026-09-05; this iteration visually checked the registered derivative of PDF page 90 / printed p. 32287, src/sources/works/united-states-congress/congressional-record-1977-10-04/editions/1977-10-04-gpo-1977-part25-segment5-2/artifacts/government-page-32287-6c95835b/source.jpg, reading all three columns. No fresh 139-page Record retrieval is claimed.
- Doug Batchelor, How to Keep the Sabbath Holy (Roseville, California: Amazing Facts, Inc., 2014), ISBN 978-1-58019-618-5, “The Ox in the Ditch,” printed p. 78 (PDF page 77), first paragraph explicitly links “an ox in the ditch” to Luke 14:5. Publisher’s complete PDF https://www.amazingfacts.org/wp-content/uploads/2025/06/BK-HKSH.pdf ; accessed 2026-09-05; title/copyright text and p. 78 image inspected on this iteration. Used only as a primary modern witness to the idiom’s consciously biblical association, not for the theology of Sabbath observance or for earliest origin.

Notes and limits: Qualifying political and deliberately reversing idiom. Riegle is opposing natural-gas deregulation and costly higher prices; the “ox” is the legislative predicament, and rescuing it is no longer automatically the right action. His surrounding speech attributes risks to consumers and criticizes treating a substantive dispute as merely keeping Senate business moving. The gospel anchor must remain “an ox fall into a pit”; “ditch” belongs to the later English idiom and is not the Challoner wording. Relationship: recognizable biblical idiom, corroborated in an explicit modern Luke 14:5 usage; direct reading of Luke by Riegle is not established. The intervention is not an argument about animal welfare or Christ’s healing. Original English. Riegle’s official congressional speech and the GPO record have a United States federal-government public-domain basis; Batchelor’s 2014 book remains protected, with only a six-word idiom needed from it and no permission inferred to republish its pages. The GPO PDF is a complete 139-page downloadable record segment, not the entire 1977 Congressional Record. The congressional image is held in the registered source library; the Batchelor PDF was freshly fetched and its exact checksum matches the registered publisher artifact. The official speech is continuing at the foot of p. 32287, so the inspection is of all speech on the cited page rather than the entire multi-page speech.

Exact acquisition receipts: see the public-identity receipt register below under CUL-006. Machine-local storage paths are omitted from this tracked brief.

### Gallery selection, negative results, and rejected leads

CUL-002 (*Love’s Labor’s Lost*) is a qualifying spare, omitted to avoid a
second Shakespeare/world-without-end example; its corrected FDT 0.9.2 edition
and exact Folger 5.2.865–866 locus remain in its full register entry. CUL-007
(Corker) is also qualifying but unselected because Riegle supplies the stronger
deliberate political reversal of the same ox idiom. Neither exclusion is a
negative verdict on the candidate's verification.

CUL-008–012 establish no selected afterlife for the Introit, Gradual, Alleluia,
Offertory, or Communion within the stated English/Latin phrase searches and
primary works inspected. Ordinary Scripture reproduction, exposition,
devotional prayer, generic likeness, bare settings and incipits do not meet the
gallery rule. The mock-Gospel, Bullock thesis, Adiemus/advertisement and Gardner
leads are not promoted; their precise missing underlying checks, access
limits, alternative wording, and protected source status remain in the
complete CUL findings below. An unappointed new-song verse from Psalm 39
cannot supply this Offertory's afterlife.

Citation-bundle comparison completed against all five selected lane findings:
the brief contains every supplied evidence string and note for CUL-001,
003–006 without dropping the Dickens attribution corroborant or Batchelor's
separate idiom witness. The literary and congressional primary sources,
translators/editors, imprint/date and access information, exact page/line
loci, stable links, extent limits and rights distinctions are retained.
No necessary selected-candidate citation field is missing from the lane join.
The five source pairings are publishable at the short quoted extent stated;
the whole modern delivery artifacts are not thereby cleared for distribution.

## Section-by-section evidence coverage

This certification covers every reader-facing position in the profile's
Reader-Facing Order, including both commentary forms. “Supplied” means the
brief supplies evidence for the section at its stated limits, not that an
author has already written or verified a rendered edition. The record of
missing evidence is itself required content where it materially bounds a
section; silence must not be substituted for it.

| Reader-facing section | Evidence position | Required use or stated absence |
| --- | --- | --- |
| Page 1: Propers map and four senses | Supplied for all ten elements and exactly four senses. | Accepted appointed-text audit via COV/THE; full matrix and four-senses table; SG-1–SG-5. No unsearched exploratory analogy belongs in the four-senses rows. |
| Page 2: Scriptural Date and Location | Chronology supplied for all seven Scriptures; literary contexts supplied; modern composition-introduction/geography coverage remains partial. | Exact fourteen assertions and their IDs/relations/profiles/labels above; dossier-specific missing fields are explicitly stated. No Gospel event date, precise town, or independently established composition location is supplied. The named English/Latin and passage-led Greek/Latin/Syriac-translation corpora bound the outcome. State these local absences rather than filling them. |
| The Propers: Themes and Movement, pages 3–4 | Supplied. | Five functional cross-proper units account for all ten elements, with multiple reception witnesses; a direct prose opening and three-to-five developed movements. Two substantive pages remain authoring/layout work. |
| Complete appointed text, research edition only | Supplied through the accepted source-audit control reported by COV-001–002,009 and THE-001–008. | Use `propers/verified.md` and its registered historical English exactly. Do not normalize away collated Latin accents; CON-EVI-001 remains to be repaired. |
| The Propers: Detailed Commentary — full element-by-element form | Supplied for every scriptural element and composed prayer. | Complete-context matrix, all PAT witnesses and their differences, oration antecedents and later liturgical reception. No exhaustive patristic census, Greek/Syriac re-collation, or exact whole-formulary origin is claimed. |
| The Propers: Detailed Commentary — synthesis integrated form | Supplied. | SG-1–SG-5 supply independently integrated arguments with multiple appointed elements and multiple witnesses per unit, rather than an abridged procession through the propers. |
| Source-Grounded Synthesis Across the Propers | Supplied; current authoring defect still stands. | Develop the witnesses within every resulting unit. CON-SYN-001 identifies the two prior single-witness units; SG-1 and SG-2 now state the additional reasoning explicitly. |
| The Propers: Notable and Quotable | Supplied. | Five selected, fully cited qualifying entries; exact paired wording, register change, and limits. Negatives for the five chants are bounded, not padded by an unsupported gallery item. |
| The Propers: Interpretive Possibilities | Supplied. | Six proposals selected from actual PRE-007–012 conjunction searches. Every proposal has anchors, mechanism, fruit, what separate reading misses, classification, and strongest limit. Anthony's reproducible Latin citations are now present. |
| Sacramental Appendix when required | Not applicable to this ordinary temporal-Sunday formulary. | No ritual Mass celebrated specifically for a non-Eucharistic sacrament or additional such appendix is identified by the supplied inputs. Do not invent one. |
| Appendix: Scope and Qualifications | Supplied. | Edition and historical-English identity, source/language/chronology bounds, rights distinctions, source-state limits, lack of exact complete-formulary first-use evidence, and honest review state. Keep operational mechanics in this brief. |
| References | Supplied for retained direct reception, liturgical argument, gallery, and precedent witnesses; exact corpus source IDs and labels retained for chronology. | Use the complete work/edition/locus bundles below and the two recovered citations above. CON-CIT-001b and CON-CIT-002b remain authoring repairs. Record-only leads do not become used references. Chronology-source metadata not supplied by the lanes is not invented from IDs. |
| Generation Metadata | Production identity supplied by the packet; finalized render timestamp and actual later contribution/review facts are not research evidence. | The author records actual production facts under the metadata guidance. This synthesis does not claim completed authoring, render review, installation, or publication. |

Every required section has an evidence position stated. The material section
shortfall is the partial historical/geographical and modern-introduction
dossier evidence on page 2, whose precise bounds are named. The absent Gospel
event date is the corpus's answer, not a gap any lane may fill. No other section
depends on a missing selected cultural witness, unchecked distinctive proposal,
or unavailable mandatory authority.

## Detailed evidence register

The register preserves the complete fresh join: each finding's ID, lane,
claim, every evidence string, and notes. Selected PRE-007–012 and CUL-001,
003–006 have their complete entries in their audit sections above; all other
findings appear here. Those earlier complete entries are part of this same
register, not omitted findings. Substantive source text has not been acquired
or changed by synthesis. Acquisition receipt metadata follows separately,
without the lanes' machine-local storage paths. The register preserves all
field wording and qualifications, trimming trailing whitespace, even when
the organized argument uses only part of a finding.

### scripture-context

#### SCR-001 — scripture-context

Claim: The Introit selects the opening supplication of Psalm 85 (86), whose needy servant appeals to God’s abundant mercy amid continuing danger.

Evidence:

- Douay–Rheims, Challoner revision, Project Gutenberg eBook 1581, Psalm 85:1–17, especially 1–7, 9–10, 14–17; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-21-psalms-578f023d/21-psalms.tsv
- Appointed boundaries taken as settled from propers/verified.md: Psalm 85:3, 5, then verse 1.

Notes and limits: Textual observation; the complete seventeen-verse psalm was inspected. Verses 1–7 repeatedly ask God to hear and help; verses 8–13 join the servant’s praise to the future worship of all nations; verses 14–17 return to attackers and the request for help. The selected poverty is compatible with the servant’s fidelity and trust in verse 2, rather than being an assertion that God has abandoned him. The liturgical order 3, 5, 1 puts the reason for confident petition before the statement of need. The title supplies a Davidic attribution, not an independently inferred date or named crisis. No claim of historical selection intent is made. Primary scriptural loci and stated context re-inspected for research iteration 1 on 2026-09-05. Iteration-1 direct-context reading extent: Psalm 85:1–17. Source files already held by src/sources; no new retrieval for these biblical bytes.

#### SCR-002 — scripture-context

Claim: Ephesians 3:13–21 joins encouragement about Paul’s afflictions to a prayer that the Gentile recipients share, with all the saints, the Spirit’s strength, Christ’s indwelling, and the fullness of God.

Evidence:

- Douay–Rheims, Challoner/Gutenberg 1581, Ephesians 1–6, especially 2:11–22; 3:1–21; 4:1–16; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-56-ephesians-10c79be0/56-ephesians.tsv

Notes and limits: Textual observation based on the whole epistle, with chapters 2–4 reread continuously. The opening appointed verse completes the account of the imprisoned apostle’s Gentile mission in 3:1–12; 3:14 resumes the “for this cause” movement of 3:1. The double “for you” of 3:1,13 explains how the sufferings can be the readers’ glory. The prayer has an explicitly communal horizon: 2:18–22 gives both peoples access in one Spirit to the Father and builds them into God’s dwelling; 3:17–19 asks indwelling and knowledge with all the saints; 3:21 gives glory in the Church; 4:1–6 immediately requires humility, patience, peace, and unity. Roots and foundations are the prayer’s own paired organic and architectural images, and do not license an independently invented architectural measurement. Primary scriptural loci and stated context re-inspected for research iteration 1 on 2026-09-05. Iteration-1 direct-context reading extent: Ephesians 1:1–6:24, all six chapters. Source files already held by src/sources; no new retrieval for these biblical bytes.

#### SCR-003 — scripture-context

Claim: The Gradual’s nations, kings, rebuilt Sion, and manifested glory stand at the center of Psalm 101 (102), where the afflicted person’s lament opens into the restoration and common worship of God’s people.

Evidence:

- Douay–Rheims, Challoner/Gutenberg 1581, Psalm 101:1–29, especially 13–23; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-21-psalms-578f023d/21-psalms.tsv
- Appointed Psalm 101:16–17 and modern-English verse offset are settled in propers/verified.md.

Notes and limits: Textual observation; the complete twenty-nine-verse psalm was inspected. The opening names an afflicted poor man and describes bodily wasting, sleeplessness, reproach, and short life. Verse 13 contrasts God’s permanence and remembrance through generations with that frailty. Mercy for Sion and concern for its stones and dust (14–15) lead to nations and kings fearing God (16–17); God regards the humble prayer (18), writes for a future people (19), hears prisoners (20–21), and gathers peoples and kings to worship in Jerusalem (22–23). Verses 24–29 return to short human life, divine constancy, and the continuing children of God’s servants. The rebuilding wording supports restored Sion as the literal horizon; it supplies no independently assignable historical date. Primary scriptural loci and stated context re-inspected for research iteration 1 on 2026-09-05. Iteration-1 direct-context reading extent: Psalm 101:1–29. Source files already held by src/sources; no new retrieval for these biblical bytes.

#### SCR-004 — scripture-context

Claim: Psalm 97 (98):1 begins a nine-verse summons in which God’s victorious salvation of Israel becomes manifest to all nations and all creation welcomes his just judgment.

Evidence:

- Douay–Rheims, Challoner/Gutenberg 1581, Psalm 97:1–9; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-21-psalms-578f023d/21-psalms.tsv
- Alleluia selection and addition of the explicit Latin Dominus are settled in propers/verified.md.

Notes and limits: Textual observation; the complete psalm was inspected. The unappointed continuation of verse 1 identifies the wonders with God’s saving right hand and holy arm; verses 2–3 join justice revealed before the Gentiles, fidelity to Israel, and salvation seen by the ends of the earth. The summons moves from earth’s singers and instruments (4–6) to sea, rivers, and mountains (7–8), ending in the Lord’s equitable judgment (9). “New canticle” is not on its own a statement about a new musical composition or an exclusively private inner state. The Nativity association returned by chronology belongs to its typed prophetic-referent record; it is not a historical event explicitly named by this psalm. Primary scriptural loci and stated context re-inspected for research iteration 1 on 2026-09-05. Iteration-1 direct-context reading extent: Psalm 97:1–9. Source files already held by src/sources; no new retrieval for these biblical bytes.

#### SCR-005 — scripture-context

Claim: Luke 14:1–11 combines a Sabbath healing and a parable for guests within a single meal at a leading Pharisee’s house, while the ensuing meal discourse extends through verse 24.

Evidence:

- Douay–Rheims, Challoner/Gutenberg 1581, Luke 13–15 read continuously, especially 13:10–17,22–35 and 14:1–35; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-49-luke-d8269c33/49-luke.tsv

Notes and limits: Textual observation. The observers’ silence frames the healing (14:3–6); Jesus then notices their choice of the first places and addresses them as guests (7). The actual meal is described as a Sabbath meal; the wedding of verses 8–10 is the parable’s imagined situation, not a statement that this meal is a wedding. The healed man is dismissed before the seating instruction, and the text does not show him taking the last place, receiving the higher place, or joining the feast. The host is unnamed and this scene has no named town. Luke 13:22 locates the surrounding narrative in the journey to Jerusalem without locating this house more precisely. Following context addresses the host’s invitation of people unable to repay (12–14), then a guest’s blessing about bread in the kingdom leads to the great-supper parable (15–24). These are context, not additional verses appointed here; 14:25 changes to the traveling crowds. Primary scriptural loci and stated context re-inspected for research iteration 1 on 2026-09-05. Iteration-1 direct-context reading extent: Luke 13:1–15:32, all three chapters. Source files already held by src/sources; no new retrieval for these biblical bytes.

#### SCR-006 — scripture-context

Claim: The Offertory draws from the plea for rescue in the latter part of Psalm 39 (40), a psalm that moves from remembered deliverance and obedient thanksgiving back into present need.

Evidence:

- Douay–Rheims, Challoner/Gutenberg 1581, Psalm 39:1–18, especially 2–13 and 14–18; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-21-psalms-578f023d/21-psalms.tsv
- The appointed selection and repeated petition are established in propers/verified.md: Psalm 39:14–15 in the Missal’s numbering.

Notes and limits: Textual observation; the complete eighteen-verse psalm was inspected. Verses 2–4 remember rescue from a pit into firm footing and a new song; 6–11 speak of wonders, obedience to God’s will, and public proclamation of justice, salvation, mercy, and truth. Verse 12 asks continuing mercy; verse 13 names both surrounding evils and the speaker’s iniquities; 14–16 ask rescue and the frustration of those seeking his life; 17 calls seekers of God to rejoice; 18 ends with the poor petitioner’s confidence in his helper. The appointed words concern a threatened life and God’s assistance. The wider psalm contains explicit sacrificial language, but the chant itself selects the plea, and its enemies cannot simply be named as a particular historical group from these verses. Primary scriptural loci and stated context re-inspected for research iteration 1 on 2026-09-05. Iteration-1 direct-context reading extent: Psalm 39:1–18. Source files already held by src/sources; no new retrieval for these biblical bytes.

#### SCR-007 — scripture-context

Claim: The Communion’s memory of God’s justice from youth to old age belongs to Psalm 70 (71), whose aging petitioner asks for continued help so that he can proclaim God’s power to the coming generation.

Evidence:

- Douay–Rheims, Challoner/Gutenberg 1581, Psalm 70:1–24, especially 5–6,9–18,20–24; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-21-psalms-578f023d/21-psalms.tsv
- The chant’s three clipped clauses and its stopping point in verse 18 are established in propers/verified.md.

Notes and limits: Textual observation; the complete twenty-four-verse psalm was inspected. Trust reaches back to the womb (5–6); failing strength and enemies who claim God has abandoned the speaker create the crisis (9–11); his answer is urgent help and continued hope and praise (12–16). Instruction from youth (17) becomes a commission to tell the coming generation of God’s arm and power (18). The chant stops before that purpose clause; retaining it as context prevents “forsake me not” from being treated solely as the preservation of a private life. God’s justice is repeatedly linked with rescue, salvation, and praise (2,15–16,19,24); “thy justice alone” refers expressly to God’s justice and does not by itself state a later account of justification. No literal Eucharistic meal is narrated by the psalm. Primary scriptural loci and stated context re-inspected for research iteration 1 on 2026-09-05. Iteration-1 direct-context reading extent: Psalm 70:1–24. Source files already held by src/sources; no new retrieval for these biblical bytes.

#### SCR-008 — scripture-context

Claim: Ephesians 3:14–19 names Father, Spirit, and Christ within one prayer, while its four dimensions have no explicit object within verse 18 and its paternity wording admits a family-oriented contextual comparison.

Evidence:

- Douay–Rheims, Challoner/Gutenberg 1581, Ephesians 2:18–22; 3:14–21; 4:1–16; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-56-ephesians-10c79be0/56-ephesians.tsv
- Clementine Vulgate, eBible latVUC edition, Ephesians 3:14–21; src/sources/works/catholic-church/vulgata-clementina/editions/ebible-latvuc/artifacts/verse-text-56-ephesians-d9b55031/56-ephesians.tsv
- USCCB, New American Bible Revised Edition, Ephesians 3, notes on 3:14–21 and 3:14–15, https://bible.usccb.org/bible/ephesians/3; complete chapter response read locally.
- Responsible institution: United States Conference of Catholic Bishops; New American Bible Revised Edition, official chapter web text, undated chapter page; accessed 2026-09-05. Exact bytes are identified by this finding’s retrieval receipt.

Notes and limits: Direct textual observations: the Father grants strength through his Spirit; Christ dwells through faith; knowledge of Christ’s love leads to fullness of God. Verse 18 does not itself say “of the cross,” “of a building,” or “of the universe.” Christ’s love is named in verse 19, so supplying it as the dimensions’ referent is a contextual inference. The USCCB note preserves love and the universe as alternatives, and explains the Father/family wordplay with “every family” or “God’s whole family.” These notes support a textual qualification, not a replacement for the Missal’s omnis paternitas or an independently checked Greek manuscript claim. Its full prayer has no request for suffering simply to be removed. Direct HTTPS retrieval and browser access both succeeded for this iteration; all 21 verses plus notes were inspected in the exact retained response. Primary scriptural loci and stated context re-inspected for research iteration 1 on 2026-09-05. USCCB text and notes are a modern comparison witness, not the appointed translation. Exact HTML retained only in lane scratch; no republication licence is inferred.

Exact acquisition receipts: see the public-identity receipt register below under SCR-008. Machine-local storage paths are omitted from this tracked brief.

#### SCR-009 — scripture-context

Claim: Luke 14:1–6 depicts Jesus healing before eliciting assent, and its received Latin ass-or-ox wording must remain distinct from the son-or-ox wording in the modern USCCB edition.

Evidence:

- Douay–Rheims, Challoner/Gutenberg 1581, Luke 14:1–11; 6:6–11; 13:10–17; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-49-luke-d8269c33/49-luke.tsv
- Clementine Vulgate, eBible latVUC edition, Luke 14:1–11; src/sources/works/catholic-church/vulgata-clementina/editions/ebible-latvuc/artifacts/verse-text-49-luke-28ae5d9a/49-luke.tsv
- USCCB, New American Bible Revised Edition, Luke 14:5 and note on 14:5, https://bible.usccb.org/bible/luke/14; complete chapter response read locally.
- Responsible institution: United States Conference of Catholic Bishops; New American Bible Revised Edition, official chapter web text, undated chapter page; accessed 2026-09-05. Exact bytes are identified by this finding’s retrieval receipt.

Notes and limits: Textual observation. Jesus poses the permissibility question, receives silence, takes hold of the man, heals and dismisses him, and only then asks the rescue question; a second silence follows. The man has no recorded petition or speech, and Luke supplies no cause of the illness or diagnosis of his character. The USCCB text reads son/ox and its note discusses an ass/ox variant; the appointed Latin and the checked Clementine read asinus/bos. Manuscript priority is attributed to that note, not independently established by this lane. The modern wording does not correct the settled appointed text. Primary scriptural loci and stated context re-inspected for research iteration 1 on 2026-09-05. USCCB text and notes are a modern comparison witness, not the appointed translation. Exact HTML retained only in lane scratch; no republication licence is inferred.

Exact acquisition receipts: see the public-identity receipt register below under SCR-009. Machine-local storage paths are omitted from this tracked brief.

#### SCR-010 — scripture-context

Claim: The Gospel’s low-seat instruction has a close wisdom parallel in Proverbs 25:6–7, and Luke repeats its concluding reversal in a prayer about justification while elsewhere making service the measure of table greatness.

Evidence:

- Douay–Rheims, Challoner/Gutenberg 1581, Proverbs 25:1–28, especially 6–7; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-22-proverbs-e8c05f66/22-proverbs.tsv
- Douay–Rheims, Challoner/Gutenberg 1581, Luke 14:7–14; 18:1–14, especially 9–14; 22:24–30; 1:46–55; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-49-luke-d8269c33/49-luke.tsv
- For the Sabbath rescue comparison: Douay–Rheims, Challoner/Gutenberg 1581, Deuteronomy 22:1–8, especially 4; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-05-deuteronomy-c99711de/05-deuteronomy.tsv; Douay–Rheims, Challoner/Gutenberg 1581, Exodus 23:1–13, especially 4–5,12; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-02-exodus-56072879/02-exodus.tsv; Douay–Rheims, Challoner/Gutenberg 1581, Luke 6:6–11 and 13:10–17; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-49-luke-d8269c33/49-luke.tsv

Notes and limits: The Proverbs comparison is close verbal and situational correspondence, not a quotation formally introduced by Luke. Luke 18:14 repeats the entire exalted/humbled reversal and 18:9 identifies self-trust in righteousness and contempt for others as its target. Luke 22 places disciples’ competition over greatness beside Jesus’ table-service and his promise of a kingdom table; Luke 1:51–53 places exaltation of the lowly within praise of God. These canonical parallels support a reading beyond social maneuvering, but identifying the parable’s host directly as Christ is a further interpretive move. Deuteronomy commands aid to a fallen ass or ox, Exodus includes even an enemy’s animal and Sabbath rest for animals and servants, and Luke 13 compares animal watering with a daughter of Abraham’s liberation. Neither Torah passage explicitly resolves the whole later Sabbath debate or names this healing. Primary scriptural loci and stated context re-inspected for research iteration 1 on 2026-09-05.

#### SCR-011 — scripture-context

Claim: Psalm 85’s appeal to abundant mercy is continuous with the divine mercy formula in Exodus 34:6–9 and with the psalm’s own expectation of worship by every nation.

Evidence:

- Douay–Rheims, Challoner/Gutenberg 1581, Psalm 85:1–17, especially 5,9–10,15; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-21-psalms-578f023d/21-psalms.tsv
- Douay–Rheims, Challoner/Gutenberg 1581, Exodus 34:1–35, especially 5–10; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-02-exodus-56072879/02-exodus.tsv

Notes and limits: Textual comparison. The direct formula appears most closely in Psalm 85:15, outside the appointed excerpt, while verse 5 shares its abundant-mercy rationale. Exodus 34 follows the replacement of the broken tablets and joins proclamation of God’s merciful character, Moses’ prostration, forgiveness, renewed divine accompaniment, and covenant; the formula includes judgment as well as mercy. The shared vocabulary is observable, but this lane does not infer a specific compositional date, prove a literary borrowing direction, or call the appointed verse an exact quotation of Exodus. Primary scriptural loci and stated context re-inspected for research iteration 1 on 2026-09-05.

#### SCR-012 — scripture-context

Claim: Psalm 101’s ending receives an explicit christological reuse in Hebrews 1:10–12, while its restoration of Sion and gathering of nations has a close canonical counterpart in Isaias 60.

Evidence:

- Douay–Rheims, Challoner/Gutenberg 1581, Psalm 101:13–29, especially 16–23 and 26–28; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-21-psalms-578f023d/21-psalms.tsv
- Douay–Rheims, Challoner/Gutenberg 1581, Hebrews 1:1–14, especially 8–12; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-65-hebrews-78520956/65-hebrews.tsv
- Douay–Rheims, Challoner/Gutenberg 1581, Isaias 60:1–22, especially 1–3,10–15,18–22; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-27-isaias-7c9a1228/27-isaias.tsv

Notes and limits: Hebrews 1 places the Psalm 101:26–28 wording in its scriptural sequence about the Son, providing an explicit canonical christological relationship to the psalm. Those are the psalm’s concluding verses, not the Gradual’s appointed 16–17, so the citation must not be represented as Hebrews directly quoting this chant. Isaias 60 likewise juxtaposes the Lord’s glory upon Jerusalem, nations and kings approaching, rebuilt walls, and enduring generations; the similarity supplies a canonical comparison rather than an established claim of direct textual dependence. No date is inferred from either restoration account. Primary scriptural loci and stated context re-inspected for research iteration 1 on 2026-09-05.

#### SCR-013 — scripture-context

Claim: The saving arm, public revelation, and worldwide salvation in Psalm 97 have close wording parallels in Isaias 52:7–10 and a corresponding christological declaration in Simeon’s canticle.

Evidence:

- Douay–Rheims, Challoner/Gutenberg 1581, Psalm 97:1–9, especially 1–3; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-21-psalms-578f023d/21-psalms.tsv
- Douay–Rheims, Challoner/Gutenberg 1581, Isaias 52:1–15, especially 7–10; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-27-isaias-7c9a1228/27-isaias.tsv
- Douay–Rheims, Challoner/Gutenberg 1581, Luke 2:22–39, especially 28–32; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-49-luke-d8269c33/49-luke.tsv
- Douay–Rheims, Challoner/Gutenberg 1581, Exodus 15:1–21, especially 2,6,11–18; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-02-exodus-56072879/02-exodus.tsv

Notes and limits: Textual comparison. Psalm 97:3 and Isaias 52:10 both speak of the ends of the earth seeing God’s salvation, alongside his holy arm and the nations; Simeon names salvation seen, revelation to the Gentiles, and Israel’s glory while holding the child Jesus. Exodus 15 supplies an earlier canonical constellation of song, saving right hand, wonders, mercy, nations’ fear, divine dwelling, and reign. The particular rescue celebrated by Psalm 97 is not named as the Red Sea event, nor does the Psalm explicitly narrate the presentation of Jesus. Connecting those deliverances typologically is therefore a canonical inference, whereas the repeated vocabulary is textual observation. Primary scriptural loci and stated context re-inspected for research iteration 1 on 2026-09-05.

#### SCR-014 — scripture-context

Claim: The Offertory psalm’s final plea closely parallels Psalm 69, and Hebrews 10 explicitly places its earlier words about coming to do God’s will on Christ’s lips.

Evidence:

- Douay–Rheims, Challoner/Gutenberg 1581, Psalm 39:7–18 and Psalm 69:1–6; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-21-psalms-578f023d/21-psalms.tsv
- Douay–Rheims, Challoner/Gutenberg 1581, Hebrews 10:1–39, especially 5–10 and 19–25; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-65-hebrews-78520956/65-hebrews.tsv

Notes and limits: Textual comparison and explicit canonical reuse. Psalm 69:2–6 substantially repeats the petitions and contrasts of Psalm 39:14–18, so rescue, shame for enemies, joy for God-seekers, and the needy petitioner form a recognisable shared unit. Hebrews 10:5–10 applies Psalm 39:7–9 to Christ’s obedient bodily offering, but Hebrews’ “a body thou hast fitted to me” differs from the Psalter’s “thou hast pierced ears for me.” The difference was checked in the same registered edition and must be acknowledged if both forms are used. Hebrews does not quote the appointed Offertory verses. The canonical connection is therefore through the whole source psalm, not direct evidence that the chant itself says “Behold I come” or that its historical choice had a particular intent. Primary scriptural loci and stated context re-inspected for research iteration 1 on 2026-09-05.

#### SCR-015 — scripture-context

Claim: Psalm 70’s prayer for lifelong help repeats the refuge language of Psalm 30 and shares with Psalm 77 a specific duty to pass knowledge of God’s saving works to coming generations.

Evidence:

- Douay–Rheims, Challoner/Gutenberg 1581, Psalm 70:1–24; Psalm 30:1–5; Psalm 77:1–8; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-21-psalms-578f023d/21-psalms.tsv

Notes and limits: Textual comparison. Psalm 70:1–3 and Psalm 30:2–4 share trust against shame, deliverance in divine justice, the inclined ear, and a strong refuge. Psalm 70:17–18 joins instruction already received to teaching God’s arm and power to the generation to come; Psalm 77:3–7 makes fathers’ testimony, children yet to be born, remembered wonders, and hope in God a public transmission of faith. The same vocabulary does not prove which text borrowed from which. The Communion’s omitted continuation provides the intergenerational link; it should not be printed as though the complete purpose clause were appointed. Primary scriptural loci and stated context re-inspected for research iteration 1 on 2026-09-05.

#### SCR-016 — scripture-context

Claim: Colossians 1–2 and John 14 provide direct canonical parallels to the Epistle’s affliction for others, divine indwelling, strengthening, roots and foundations, love, and fullness.

Evidence:

- Douay–Rheims, Challoner/Gutenberg 1581, Ephesians 3:13–21; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-56-ephesians-10c79be0/56-ephesians.tsv
- Douay–Rheims, Challoner/Gutenberg 1581, Colossians 1:1–29 and 2:1–23, especially 1:9–12,24–29 and 2:2–10; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-58-colossians-d17592ce/58-colossians.tsv
- Douay–Rheims, Challoner/Gutenberg 1581, John 14:1–31, especially 15–26; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-50-john-27b8f3ed/50-john.tsv

Notes and limits: Textual comparison, without a claim about literary dependence or authorship chronology. Colossians prays for fruitful conduct and strengthening (1:9–12), links the apostle’s sufferings to Christ’s body the Church (1:24), and names Christ among the Gentiles, the hope of glory (1:27). Its rooted/built-up pairing and distinction between fullness dwelling bodily in Christ and believers being filled in him (2:7–10) materially illuminate the wording of Ephesians 3. John 14 ties love and keeping Christ’s word to the Father and Son making their abode with the believer, with the Spirit abiding and teaching. The parallel holds without equating these passages’ immediate settings or importing later doctrinal formulations into their wording. Primary scriptural loci and stated context re-inspected for research iteration 1 on 2026-09-05.

#### SCR-017 — scripture-context

Claim: The Introit and Offertory share an explicit dependence on divine help, while their complete psalms and the Communion psalm also share the language of poverty, threatened life, and God’s refusal to abandon the petitioner.

Evidence:

- Douay–Rheims, Challoner/Gutenberg 1581, Appointed Psalm 85:1,3,5 and Psalm 39:14–15; contextual Psalm 85:14–17,39:12–18,70:9–18; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-21-psalms-578f023d/21-psalms.tsv
- The repeated appointed Offertory appeal and selected Communion petition are controlled by propers/verified.md.

Notes and limits: The direct appointed links are the needy/poor petitioner of the Introit, the Offertory request for aid against those seeking his life, and the Communion request not to be forsaken. Psalm 39:18 supplies the Offertory psalm’s own needy/poor self-description; Psalm 85:14 supplies the Introit psalm’s own threat against the speaker’s life; Psalm 70:9–13 supplies both failing strength and hostile observers. This is an evidence map of textual recurrence. Reading the three ritual moments as a single developing subject or as a specific spiritual itinerary is a further cross-proper synthesis, not asserted here. Primary scriptural loci and stated context re-inspected for research iteration 1 on 2026-09-05.

#### SCR-018 — scripture-context

Claim: The appointed Gradual, Epistle, and Gospel all speak of glory but assign it to distinct recipients and settings, while their scriptural contexts repeatedly widen the horizon from individual persons to gathered communities and nations.

Evidence:

- Douay–Rheims, Challoner/Gutenberg 1581, Appointed Psalm 101:16–17; contextual Psalm 101:18–23,85:9–10,97:2–9; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-21-psalms-578f023d/21-psalms.tsv
- Douay–Rheims, Challoner/Gutenberg 1581, Appointed Ephesians 3:13,16,21; contextual 2:18–22 and 3:6–12; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-56-ephesians-10c79be0/56-ephesians.tsv
- Douay–Rheims, Challoner/Gutenberg 1581, Appointed Luke 14:7–11; contextual 14:12–24; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-49-luke-d8269c33/49-luke.tsv

Notes and limits: Direct textual distinctions: the Gradual gives God glory recognized by kings; the Epistle calls the apostle’s tribulations the readers’ glory, asks according to God’s glorious riches, and ends in glory to God in the Church and Christ; the Gospel permits the honor conferred by the host before fellow diners. Luke therefore does not condemn every received honor; it condemns self-exaltation. Psalm 101’s assembled peoples, Ephesians’ fellow heirs and common dwelling, and Luke’s invited company supply distinct communal settings. A unified account of rightly received glory or the identification of Sion with the Church is an interpretive synthesis beyond the mere recurrence and is not attributed to these words as an explicit statement. Primary scriptural loci and stated context re-inspected for research iteration 1 on 2026-09-05.

#### SCR-019 — scripture-context

Claim: The appointed Introit, Communion, and Epistle use distinct spans of time—persistent daily appeal, a life from youth into old age, and glory across all generations—and the surrounding psalms explicitly connect praise with future hearers.

Evidence:

- Douay–Rheims, Challoner/Gutenberg 1581, Appointed Psalm 85:3 and Psalm 70:16–18; contextual Psalm 85:12,70:8,15,18,24 and Psalm 101:13,19,25,29; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-21-psalms-578f023d/21-psalms.tsv
- Douay–Rheims, Challoner/Gutenberg 1581, Ephesians 3:21; registered verse artifact src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-56-ephesians-10c79be0/56-ephesians.tsv

Notes and limits: Textual observation. The Introit’s tota die concerns ongoing supplication; the Communion’s a iuventute through senectam et senium spans the petitioner’s lived dependence; the Epistle’s in omnes generationes extends its ecclesial doxology. Psalm 70’s unappointed continuation promises testimony to the coming generation, and Psalm 101 asks that the work be written for another generation and ends with enduring descendants. These are textual temporal horizons, not biblical dates and not proof of a deliberate formulary design. An analogy that makes these spans into stages of one liturgical life would be the later synthesist’s inference. Primary scriptural loci and stated context re-inspected for research iteration 1 on 2026-09-05.

#### SCR-020 — scripture-context

Claim: Introit chronology is the exact corpus answer below, retaining the distinct relations and recorded qualifications.

Evidence:

- src/gpt/liturgy/roman-rite/1962/propers/temporal/56-sixteenth-after-pentecost/research/chronology.toml; element introit; requested profile catholic-comprehensive-v1; status composition-only; publication_status composition-only.
- {"subject": "critical.psalms.latest-composition-boundary", "relation": "composition", "profile": "catholic-critical-v1", "label": "before the Maccabean period, around 165 B.C.; no individual psalm can be dated securely", "disposition": "preferred", "basis_class": "catholic-critical", "answerability": "answerable", "sources": ["passage.united-states-conference-of-catholic-bishops.new-american-bible-revised-edition.english-usccb-web-2026-07-28.psalms-introduction"]}

Notes and limits: Corpus projection read in full on 2026-09-05; no biblical date was independently researched, substituted, or harmonized. Evidence carries exactly the source labels, subjects, relations, profiles, and answerability of the publication_claims intersection, never the normalized dates.

#### SCR-021 — scripture-context

Claim: Epistle chronology is the exact corpus answer below, retaining the distinct relations and recorded qualifications.

Evidence:

- src/gpt/liturgy/roman-rite/1962/propers/temporal/56-sixteenth-after-pentecost/research/chronology.toml; element epistle; requested profile catholic-comprehensive-v1; status composition-only; publication_status composition-only.
- {"subject": "composition.epistle-to-the-ephesians", "relation": "composition", "profile": "catholic-traditional-v1", "label": "a period between 58 and 63", "disposition": "disputed", "basis_class": "traditional-catholic", "answerability": "answerable", "sources": ["artifact.catholic-encyclopedia.volume-5.new-york-1909.newadvent-05485a-66d722ae"]}
- {"subject": "composition.epistle-to-the-ephesians", "relation": "composition", "profile": "catholic-traditional-v1", "label": "(Philemon; Colossians; Ephesians; Philippians), 61", "disposition": "disputed", "basis_class": "traditional-catholic", "answerability": "answerable", "sources": ["artifact.catholic-encyclopedia.volume-11.new-york-1911.newadvent-11567b-bff0dda8"]}

Notes and limits: Corpus projection read in full on 2026-09-05; no biblical date was independently researched, substituted, or harmonized. Evidence carries exactly the source labels, subjects, relations, profiles, and answerability of the publication_claims intersection, never the normalized dates.

#### SCR-022 — scripture-context

Claim: Gradual chronology is the exact corpus answer below, retaining the distinct relations and recorded qualifications.

Evidence:

- src/gpt/liturgy/roman-rite/1962/propers/temporal/56-sixteenth-after-pentecost/research/chronology.toml; element gradual; requested profile catholic-comprehensive-v1; status composition-only; publication_status composition-only.
- {"subject": "critical.psalms.latest-composition-boundary", "relation": "composition", "profile": "catholic-critical-v1", "label": "before the Maccabean period, around 165 B.C.; no individual psalm can be dated securely", "disposition": "preferred", "basis_class": "catholic-critical", "answerability": "answerable", "sources": ["passage.united-states-conference-of-catholic-bishops.new-american-bible-revised-edition.english-usccb-web-2026-07-28.psalms-introduction"]}

Notes and limits: Corpus projection read in full on 2026-09-05; no biblical date was independently researched, substituted, or harmonized. Evidence carries exactly the source labels, subjects, relations, profiles, and answerability of the publication_claims intersection, never the normalized dates.

#### SCR-023 — scripture-context

Claim: Alleluia chronology is the exact corpus answer below, retaining the distinct relations and recorded qualifications.

Evidence:

- src/gpt/liturgy/roman-rite/1962/propers/temporal/56-sixteenth-after-pentecost/research/chronology.toml; element alleluia; requested profile catholic-comprehensive-v1; status dated; publication_status dated.
- {"subject": "critical.psalms.latest-composition-boundary", "relation": "composition", "profile": "catholic-critical-v1", "label": "before the Maccabean period, around 165 B.C.; no individual psalm can be dated securely", "disposition": "preferred", "basis_class": "catholic-critical", "answerability": "answerable", "sources": ["passage.united-states-conference-of-catholic-bishops.new-american-bible-revised-edition.english-usccb-web-2026-07-28.psalms-introduction"]}
- {"subject": "life-of-christ.nativity", "relation": "prophetic-referent", "profile": "catholic-traditional-v1", "label": "the year of Rome 750 which he styles 3 B.C.", "disposition": "disputed", "basis_class": "reported-traditional", "answerability": "answerable", "sources": ["artifact.catholic-encyclopedia.volume-3.new-york-1908.newadvent-03738a-5eb03e5b"]}
- {"subject": "life-of-christ.nativity", "relation": "prophetic-referent", "profile": "catholic-traditional-v1", "label": "probably the year 7 B.C.", "disposition": "disputed", "basis_class": "traditional-catholic", "answerability": "answerable", "sources": ["artifact.catholic-encyclopedia.volume-3.new-york-1908.newadvent-03731a-f5f96f04"]}
- John Gerard, “General Chronology,” The Catholic Encyclopedia, vol. 3 (New York: Robert Appleton Company, 1908), section “Christian era,” first paragraph, sentence beginning “It is supposed by many”; https://www.newadvent.org/cathen/03738a.htm. Registered access date 2026-08-26; rechecked by direct retrieval 2026-09-05. New Advent transcription credited to Rick McCarty.
- Registered parent artifact.catholic-encyclopedia.volume-3.new-york-1908.newadvent-03738a-5eb03e5b: SHA-256 5eb03e5b5707514be6a0075d41f99970fd38a2dffe9c157191fa2fe3666c1dd0, 44502 bytes, retrieved 2026-08-26. Retained article derivative artifact.catholic-encyclopedia.volume-3.new-york-1908.newadvent-03738a-5eb03e5b-article-text: SHA-256 dea165f13c912bb66bb1bc30fae59d6a7aa732750427da1343e746582698d10d; local line 31 is the Christian era heading and line 33 its paragraph containing the assertion.

Notes and limits: Corpus projection read in full on 2026-09-05; no biblical date was independently researched, substituted, or harmonized. Evidence carries exactly the source labels, subjects, relations, profiles, and answerability of the publication_claims intersection, never the normalized dates. The two Nativity assertions are prophetic-referent, not composition, and remain disputed; the first is reported-traditional. CON-CIT-001a evidence repaired: the exact registered 03738a witness is Gerard’s General Chronology; its attribution and Christian era locus have been directly rechecked. The article reports a view held by others; its reported-traditional qualification remains intact. No chronology assertion was changed.  The newly fetched page has different exact bytes from the older registered parent; the checked article identity and relevant wording agree with the retained derivative. This receipt identifies the new response without changing or pretending to replace the registered artifact.

Exact acquisition receipts: see the public-identity receipt register below under SCR-023. Machine-local storage paths are omitted from this tracked brief.

#### SCR-024 — scripture-context

Claim: Gospel chronology is the exact corpus answer below, retaining the distinct relations and recorded qualifications.

Evidence:

- src/gpt/liturgy/roman-rite/1962/propers/temporal/56-sixteenth-after-pentecost/research/chronology.toml; element gospel; requested profile catholic-comprehensive-v1; status composition-only; publication_status composition-only.
- {"subject": "composition.gospel-of-luke", "relation": "composition", "profile": "catholic-traditional-v1", "label": "About the year 70", "disposition": "disputed", "basis_class": "traditional-catholic", "answerability": "answerable", "sources": ["artifact.catholic-encyclopedia.volume-14.new-york-1912.newadvent-14530a-0a19aa2c"]}
- {"subject": "composition.gospel-of-luke", "relation": "composition", "profile": "catholic-traditional-v1", "label": "before the end of the Roman imprisonment, when the Acts was finished", "disposition": "disputed", "basis_class": "traditional-catholic", "answerability": "answerable", "sources": ["passage.pontifical-biblical-commission.de-auctore-tempore-et-veritate-evangeliorum-marci-et-lucae.latin-aas-4-1912.responsa-i-ix"]}

Notes and limits: Corpus projection read in full on 2026-09-05; no biblical date was independently researched, substituted, or harmonized. Evidence carries exactly the source labels, subjects, relations, profiles, and answerability of the publication_claims intersection, never the normalized dates. The record supplies composition only; no event-date assertion for Luke 14:1–11 is available here.

#### SCR-025 — scripture-context

Claim: Offertory chronology is the exact corpus answer below, retaining the distinct relations and recorded qualifications.

Evidence:

- src/gpt/liturgy/roman-rite/1962/propers/temporal/56-sixteenth-after-pentecost/research/chronology.toml; element offertory; requested profile catholic-comprehensive-v1; status composition-only; publication_status composition-only.
- {"subject": "critical.psalms.latest-composition-boundary", "relation": "composition", "profile": "catholic-critical-v1", "label": "before the Maccabean period, around 165 B.C.; no individual psalm can be dated securely", "disposition": "preferred", "basis_class": "catholic-critical", "answerability": "answerable", "sources": ["passage.united-states-conference-of-catholic-bishops.new-american-bible-revised-edition.english-usccb-web-2026-07-28.psalms-introduction"]}

Notes and limits: Corpus projection read in full on 2026-09-05; no biblical date was independently researched, substituted, or harmonized. Evidence carries exactly the source labels, subjects, relations, profiles, and answerability of the publication_claims intersection, never the normalized dates.

#### SCR-026 — scripture-context

Claim: Communion chronology is the exact corpus answer below, retaining the distinct relations and recorded qualifications.

Evidence:

- src/gpt/liturgy/roman-rite/1962/propers/temporal/56-sixteenth-after-pentecost/research/chronology.toml; element communion; requested profile catholic-comprehensive-v1; status dated; publication_status dated.
- {"subject": "critical.psalms.latest-composition-boundary", "relation": "composition", "profile": "catholic-critical-v1", "label": "before the Maccabean period, around 165 B.C.; no individual psalm can be dated securely", "disposition": "preferred", "basis_class": "catholic-critical", "answerability": "answerable", "sources": ["passage.united-states-conference-of-catholic-bishops.new-american-bible-revised-edition.english-usccb-web-2026-07-28.psalms-introduction"]}
- {"subject": "israel.monarchy.david-flight-from-absalom", "relation": "historical-setting", "profile": "catholic-traditional-v1", "label": "when he fled from the face of his son Absalom", "disposition": "preferred", "basis_class": "scripture", "answerability": "answerable", "sources": ["bible:douay-rheims:Ps.3.1"]}
- {"subject": "israel.exile.first-captivity", "relation": "superscription-setting", "profile": "catholic-traditional-v1", "label": "A.M. 3398", "disposition": "alternate", "basis_class": "reported-excluded", "answerability": "answerable", "sources": ["passage.george-leo-haydock.douay-rheims-with-haydock-commentary.2014-loreto-feeney-memorial.psalm-70-captivities-usher-chronology"]}
- {"subject": "israel.exile.first-captivity", "relation": "superscription-setting", "profile": "catholic-traditional-v1", "label": "In the third year of the reign of Joakim, king of Juda", "disposition": "preferred", "basis_class": "scripture", "answerability": "answerable", "sources": ["bible:douay-rheims:Dan.1.1"]}

Notes and limits: Corpus projection read in full on 2026-09-05; no biblical date was independently researched, substituted, or harmonized. Evidence carries exactly the source labels, subjects, relations, profiles, and answerability of the publication_claims intersection, never the normalized dates. The recorded historical-setting and superscription-setting remain distinct; the A.M. label remains reported-excluded and alternate, never promoted into the preferred chronology.

### patristic-reception

#### PAT-001 — patristic-reception

Claim: In Psalm 85 (86):1, 3 and 5 Augustine hears Christ and his Church praying together, identifies the poverty heard by God with humble dependence, reads the all-day cry as the Church's prayer across successive generations, and understands divine graciousness as patience with distracted petitioners.

Evidence:

- Augustine, Enarrationes in Psalmos 85 §§1–3, 5 and 7 (NPNF1-08 prints this under Psalm LXXXVI), complete CCEL NPNF1-08 English text, physical lines 41953–42197: https://ccel.org/ccel/s/schaff/npnf108/cache/npnf108.txt. Appointed introit: Ps. 85:1,3,5.

Notes and limits: Direct reception rechecked on 2026-09-05 in registered CCEL NPNF1-08 source.txt, lines 41953–42197: §§1–7 and the opening of §8. NPNF uses modern-numbered Psalm LXXXVI for Augustine’s Latin Psalm 85 and visibly abridges the original. The complete digital edition is retained in src/sources, but no unabridged Latin collation is claimed. §3 permits rich persons to be God’s poor through humility; §7 does not promise every requested object. Retrievals are empty because the exact registered source was reused.

#### PAT-002 — patristic-reception

Claim: Chrysostom reads Ephesians 3:13–21 as encouragement that apostolic suffering serves the recipients' glory, that the Spirit strengthens faith and love, and that the four dimensions indicate Christ's immeasurable love rather than a measurable quantity.

Evidence:

- John Chrysostom, Homilies on Ephesians, Homily VII, exposition of Eph. 3:13–21, CCEL NPNF1-13 English text, physical lines 8030–8176: https://ccel.org/ccel/s/schaff/npnf113/cache/npnf113.txt.

Notes and limits: Direct Greek patristic reception rechecked on 2026-09-05 in retained NPNF1-13 English, lines 8020–8195: Eph. 3:13–21 and the immediately following interpretation and moral application. No Greek collation is claimed. Chrysostom’s alternative explanations of fullness (Trinitarian knowledge or virtue) and heavenly families (heavenly orders or derivative fatherhood) remain distinct; the dimensions indicate transcendent love, not a measurable quantity.

#### PAT-003 — patristic-reception

Claim: Chrysostom explains the doxology of Ephesians 3:20–21 as gratitude for gifts exceeding prior request or expectation and interprets the Church as enduring into eternity.

Evidence:

- John Chrysostom, Homilies on Ephesians VII, on Eph. 3:20–21 and following discussion, NPNF1-13, physical lines 8108–8176: https://ccel.org/ccel/s/schaff/npnf113/cache/npnf113.txt.

Notes and limits: Direct reception in the same freshly inspected homily and retained source as PAT-002. Chrysostom simultaneously requires the believers’ rooted faith and charity; no exemption from human response follows. No new source retrieval.

#### PAT-004 — patristic-reception

Claim: Augustine reads the Gradual's nations and kings as the gathering of peoples into one Church and Zion's building as a present work whose completion precedes Christ's glorious judgment.

Evidence:

- Augustine, Enarrationes in Psalmos 101, NPNF1-08 'Psalm CII' §§16–18, on Vulgate Ps. 101:16–18 (modern 102:15–17), physical lines 50510–50547 of the complete CCEL text retained with PAT-001: https://ccel.org/ccel/s/schaff/npnf108/cache/npnf108.txt.

Notes and limits: Re-entry inspection on 2026-09-05: read the exact registered CCEL NPNF1-08 source.txt at the line ranges named in evidence, including each relevant numbered section. Direct reception in an abridged English translation; not a fresh Latin facsimile check. Documented direct reception of the Gradual's Ps. 101:16–17, read with the prayer-of-the-poor continuation in §18. NPNF's English exposition has a continuous section sequence and abridgments; cite that edition's §§16–18 rather than silently transferring its numbering to a Latin sermon division. No inference about why the Roman compiler appointed these verses is made.

#### PAT-005 — patristic-reception

Claim: Augustine reads the Alleluia's new song as the life renewed in Christ and the Church's peace, then distinguishes merely recovering bodily health from being healed inwardly for God.

Evidence:

- Augustine, Enarrationes in Psalmos 97 §1, NPNF1-08 'Psalm XCVIII' §1, physical lines 48837–48875: https://ccel.org/ccel/s/schaff/npnf108/cache/npnf108.txt.

Notes and limits: Re-entry inspection on 2026-09-05: read the exact registered CCEL NPNF1-08 source.txt at the line ranges named in evidence, including each relevant numbered section. Direct reception in an abridged English translation; not a fresh Latin facsimile check. Documented direct reception. Augustine himself links the 'wonderful things' to a Gospel just heard, the raising of the widow's son at Nain (Luke 7), not the present Sunday’s Luke 14 healing; that difference matters if his liturgical allusion is retained. The inward-healing development comments on the remainder of Ps. 97:1, beyond the Alleluia's selected opening. No new retrieval: reused the registered exact CCEL artifact.

#### PAT-006 — patristic-reception

Claim: Augustine hears the Offertory psalm's plea for help as the suffering members' appeal to their physician, and reads its enemies in the setting of Christ's Passion while construing the following wish for their reversal as a wish for humble conversion.

Evidence:

- Augustine, Enarrationes in Psalmos 39 §§21–25, especially §§22–24, NPNF1-08 'Psalm XL', physical lines 13200–13266: https://ccel.org/ccel/s/schaff/npnf108/cache/npnf108.txt.

Notes and limits: Re-entry inspection on 2026-09-05: read the exact registered CCEL NPNF1-08 source.txt at the line ranges named in evidence, including each relevant numbered section. Direct reception in an abridged English translation; not a fresh Latin facsimile check. Direct reception of Ps. 39:14–15 within the complete verse context. The Offertory retains the request that those seeking the soul's destruction be ashamed but omits the 'turned backward' continuation on which §24 develops its positive interpretation. Do not present that omitted clause as appointed chant wording. No new retrieval: reused the registered exact CCEL artifact.

#### PAT-007 — patristic-reception

Claim: Augustine interprets the Communion's remembrance of God's justice alone as renouncing self-grounded righteousness, the teaching from youth as unearned conversion, and the prayer into old age as dependence on the grace that both begins and sustains life.

Evidence:

- Augustine, Enarrationes in Psalmos 70, NPNF1-08 'Psalm LXXI' §§18–21, physical lines 33083–33248: https://ccel.org/ccel/s/schaff/npnf108/cache/npnf108.txt.

Notes and limits: Re-entry inspection on 2026-09-05: read the exact registered CCEL NPNF1-08 source.txt at the line ranges named in evidence, including each relevant numbered section. Direct reception in an abridged English translation; not a fresh Latin facsimile check. Documented direct reception of Ps. 70:16–18. §20 expressly rejects treating God as a guide who shows the road and then becomes dispensable; §21 applies the ages both to each person's last breath and the Church's endurance to the world's end. NPNF uses continuous English section numbers: do not map them to a particular Latin sermon division without checking that edition. No new retrieval: reused the registered exact CCEL artifact.

#### PAT-008 — patristic-reception

Claim: Aquinas explains Paul's bent knees in Ephesians 3:14 as bodily acknowledgment of smallness and weakness, insists that the requested perseverance requires God's gift, and derives created fatherhood from divine fatherhood while distinguishing how humans first learn the name.

Evidence:

- Thomas Aquinas, Super Epistolam B. Pauli ad Ephesios lectura, cap. 3 lect. 4, Corpus Thomisticum unit [87804], Latin text based on the Turin 1953 edition, machine transcribed by Roberto Busa and revised by Enrique Alarcón: https://www.corpusthomisticum.org/cep.html#87804.

Notes and limits: Fresh re-entry inspection on 2026-09-05: complete Latin lecture 3.4 and edition masthead read. Direct medieval Doctoral reception, Latin lecture read in full, including the distinction between the name as a human concept learned from creatures and the reality of fatherhood as prior in God. Aquinas's scriptural wording follows paternitas. It should not efface Chrysostom's alternative explanation in terms of heavenly groups or families. Edition masthead inspected.

Exact acquisition receipts: see the public-identity receipt register below under PAT-008. Machine-local storage paths are omitted from this tracked brief.

#### PAT-009 — patristic-reception

Claim: Aquinas gives two readings of Ephesians 3:18–19—knowledge of God's immeasurable perfections and the extent, perseverance, heavenly aim and divine origin of charity—and expressly develops the latter through the four dimensions of the Cross.

Evidence:

- Thomas Aquinas, Super Ephesios, cap. 3 lect. 5, Corpus Thomisticum unit [87805], https://www.corpusthomisticum.org/cep.html#87805; the complete lecture includes the doxology through Eph. 3:21.

Notes and limits: Fresh re-entry inspection on 2026-09-05: complete Latin lecture 3.5 read, including both explanations and doxology. Direct medieval reception, Latin lecture read in full. 'Comprehension' means attaining and knowing God's presence, not containing all that God is; dimensions are metaphorical, since God is spirit. The hidden depth corresponds to the unseen divine source of charity and predestination, not a human ability to explain God's counsel. The Cross interpretation is explicitly Aquinas's retained reading, while Chrysostom's checked exposition uses the dimensions to signify immensity without this Cross elaboration. Aquinas offers more than one interpretation rather than a single exclusive sense.
 Complete current commentary receipt accompanies PAT-008.

#### PAT-010 — patristic-reception

Claim: Cyril treats Jesus' healing on the Sabbath as revelation of divine power and of the law's merciful purpose, and interprets spiritual Sabbath keeping as cessation from sin accompanied by holy works.

Evidence:

- Cyril of Alexandria, Commentary on Luke, Sermon CI, on Luke 14:1–6, R. Payne Smith, trans. from the Syriac (Oxford, 1859), pp. 471–475: https://www.tertullian.org/fathers/cyril_on_luke_10_sermons_99_109.htm.

Notes and limits: Fresh re-entry inspection on 2026-09-05: complete Sermon CI read from the registered Payne Smith/Pearse source HTML; Syriac and Greek originals not freshly collated. Direct Eastern patristic reception, inspected complete Sermon CI in the identified English translation of the Syriac witness. The selected text reads 'son or ox' at Luke 14:5, whereas the appointed Missal has 'ass or ox'; Cyril’s appeal to parental affection depends on his variant and must not be attributed to the Missal’s wording. Cyril’s polemical invective is source context, not a basis for general claims about Jews.

#### PAT-011 — patristic-reception

Claim: Cyril interprets the choice of the lowest place in Luke 14:7–11 as correction of vainglory grounded in truthful self-knowledge and the desire for honor bestowed by God.

Evidence:

- Cyril of Alexandria, Commentary on Luke, Sermon CII, on Luke 14:7–11, Payne Smith 1859, pp. 476–479: https://www.tertullian.org/fathers/cyril_on_luke_10_sermons_99_109.htm.

Notes and limits: Fresh re-entry inspection on 2026-09-05: complete Sermon CII read from the same registered source HTML. Direct reception; the full sermon was read. Cyril moves beyond embarrassment at misplaced rank to the transience of wealth, bodily weakness and mortality; humility can relinquish even honor one could claim without blame. Sermon CIII treats Luke 14:12–14 separately; its charity to poor guests is contextual continuation, not part of the appointed Gospel. No new retrieval: reused the registered complete sermon section.

#### PAT-012 — patristic-reception

Claim: Ambrose reads Luke 14's dropsy as fleshly excess obstructing the soul, then praises Christ's gentle correction of the ambition for a higher seat as a way that persuasion can reform desire.

Evidence:

- Ambrose, Expositio evangelii secundum Lucam VII.195, on Luke 14:2–14, PL 15, cols. 1752A–B, Latin text: https://la.wikisource.org/wiki/Expositio_evangelii_secundum_Lucam/VII.

Notes and limits: Direct Latin patristic reception rechecked on 2026-09-05 in registered Wikisource Book VII source.html: §195, its Luke 14:2–14 heading and PL 15 column markers 1752A–B. No fresh facsimile collation. The moralized dropsy is Ambrose’s spiritual interpretation; it is not a medical diagnosis or a literal accusation against Luke’s man. The extension to poor and disabled guests interprets subsequent vv. 12–14. No new retrieval.

#### PAT-013 — patristic-reception

Claim: Aquinas reads the Offertory's request for God's regard as help both to escape evil and perform good, and allows the enemies' shame in Psalm 39:15 to mean either penitence or punishment under divine justice.

Evidence:

- Thomas Aquinas, In psalmos Davidis expositio / Super Psalmo 39 n. 7, unit [87202], reportatio of Reginald of Piperno, Corpus Thomisticum Latin text based on Parma 1863, Busa transcription revised by Enrique Alarcón: https://www.corpusthomisticum.org/cps31.html#87202.

Notes and limits: Direct medieval reception: complete Latin Psalm 39 n. 7 rechecked on 2026-09-05 with the masthead naming Reginald of Piperno’s reportatio and Parma 1863 text, Busa transcription, Alarcón revision. Both penitential and punitive readings of shame are explicit. The commentary begins with the complete Complaceat clause omitted by the chant. The entire nine-file host presentation covering prologue and Psalms 1–54 was acquired; the receipts declare each section’s extent. Detailed inspection is confined to n. 7 and the masthead, not all acquired psalms. The psalms beyond 54 are outside this reportatio’s offered extent.

Exact acquisition receipts: see the public-identity receipt register below under PAT-013. Machine-local storage paths are omitted from this tracked brief.

#### PAT-014 — patristic-reception

Claim: Theodoret reads Psalm 85's poor petitioner as humble even when rich in righteousness, its daily cry as continual recourse to mercy, and God's mildness as patient accessibility to those in need.

Evidence:

- Theodoret of Cyrus, Interpretatio in Psalmos, Psalm 85, on vv. 1–5, PG 80 (Paris, 1860), cols. 1553C–1556B; complete facsimile PDF pp. 825–826: https://upload.wikimedia.org/wikipedia/commons/f/fd/Patrologia_Graeca_Vol._080.pdf.

Notes and limits: Re-entry on 2026-09-05: freshly inspected the identified facsimile pages at 180 dpi, using the paired Latin translation and Greek wording for Theodoret and O’Sullivan’s English for Bellarmine. Direct Greek tradition inspected on the paired Greek/Latin facsimile pages, with Latin translation carrying the detailed reading and Greek phrases cross-checked. His introductory application to David and Hezekiah is reception, not this lane's historical dating claim. He notes Symmachus's 'each day' for 'all day' and Aquila/Theodotion's 'placable' for 'mild', which shows his lexical attention rather than one English sense being exhaustive.

Exact acquisition receipts: see the public-identity receipt register below under PAT-014. Machine-local storage paths are omitted from this tracked brief.

#### PAT-015 — patristic-reception

Claim: Theodoret interprets Psalm 101's rebuilding of Zion first as restoration of the humbled city, but holds that the worldwide conversion of nations and kings in verse 16 points beyond that return to the Incarnation and its still unfolding fulfillment.

Evidence:

- Theodoret, Interpretatio in Psalmos 101, on vv. 14–19, especially vv. 16–17, PG 80, cols. 1679B–1682B; PDF pp. 890–891: https://upload.wikimedia.org/wikipedia/commons/f/fd/Patrologia_Graeca_Vol._080.pdf.

Notes and limits: Re-entry on 2026-09-05: freshly inspected the identified facsimile pages at 180 dpi, using the paired Latin translation and Greek wording for Theodoret and O’Sullivan’s English for Bellarmine. Direct Greek/Latin facsimile reading. He reasons that the Jews' neighbors marvelled at the return yet did not all believe and even attacked; hence the universal promise cannot be exhausted there. For v. 17 the city's restoration displays God's glory where captivity had been mistaken for divine weakness. This is a substantive development beside Augustine's ecclesial-building and final-judgment reading, not an assertion that the two expositions are identical.
 Complete facsimile retrieval receipt is attached to PAT-014.

#### PAT-016 — patristic-reception

Claim: Theodoret reads Psalm 97:1's new song as fitting a new way of worship and life inaugurated by the Savior's advent, and its wonders as divine acts beyond ordinary human expectation.

Evidence:

- Theodoret, Interpretatio in Psalmos 97, v. 1, PG 80, cols. 1657C–1658D; PDF p. 879: https://upload.wikimedia.org/wikipedia/commons/f/fd/Patrologia_Graeca_Vol._080.pdf.

Notes and limits: Re-entry on 2026-09-05: freshly inspected the identified facsimile pages at 180 dpi, using the paired Latin translation and Greek wording for Theodoret and O’Sullivan’s English for Bellarmine. Direct Greek/Latin facsimile reading. He continues beyond the appointed clause to interpret the right hand as power and salvation as a work God counts as his own gain through boundless love. That continuation is Psalm context, not extra Alleluia wording.
 Complete facsimile retrieval receipt is attached to PAT-014.

#### PAT-017 — patristic-reception

Claim: Theodoret hears Psalm 39:14–15 as the Church's appeal against persecutors seeking death, with their reversal meaning frustration of their intended harm.

Evidence:

- Theodoret, Interpretatio in Psalmos 39, vv. 13–17, PG 80, cols. 1159A–1160D; PDF p. 614: https://upload.wikimedia.org/wikipedia/commons/f/fd/Patrologia_Graeca_Vol._080.pdf.

Notes and limits: Re-entry on 2026-09-05: freshly inspected the identified facsimile pages at 180 dpi, using the paired Latin translation and Greek wording for Theodoret and O’Sullivan’s English for Bellarmine. Direct Greek/Latin facsimile reading. The preceding explanation explicitly gives the Church one voice that can include both perfected members and weak or sinful members. The appointed clauses are vv. 14–15; the further wish that enemies be turned backward belongs to the full biblical continuation, and Theodoret's immediate gloss emphasizes thwarting attacks rather than Augustine’s elaboration of following Christ.
 Complete facsimile retrieval receipt is attached to PAT-014.

#### PAT-018 — patristic-reception

Claim: Theodoret interprets Psalm 70:16–18's youth as the people’s schooling through Moses and old age as the law’s approaching end, while the remembered justice and divine protection carry their testimony toward the coming generation.

Evidence:

- Theodoret, Interpretatio in Psalmos 70, vv. 15–19, PG 80, cols. 1423B–1426C; PDF pp. 750–751: https://upload.wikimedia.org/wikipedia/commons/f/fd/Patrologia_Graeca_Vol._080.pdf.

Notes and limits: Re-entry on 2026-09-05: freshly inspected the identified facsimile pages at 180 dpi, using the paired Latin translation and Greek wording for Theodoret and O’Sullivan’s English for Bellarmine. Direct Greek/Latin facsimile reading. His corporate salvation-historical interpretation materially differs from Augustine's conversion-and-perseverance reading; he explicitly relates the oldness of the law to Hebrews 8:13 and the future generation to the Church from the nations. The brackets in the edition mark some textual additions, including a Christian grace parallel; do not attribute every bracketed clause to an undifferentiated textual witness. No dates are inferred from his exposition.
 Complete facsimile retrieval receipt is attached to PAT-014.

#### PAT-019 — patristic-reception

Claim: Bellarmine reads the Introit psalm's poverty as humble freedom from trust in wealth, its continual cry as fervent perseverance, and God's mildness as willingness to receive imperfect petitioners.

Evidence:

- Robert Bellarmine, A Commentary on the Book of Psalms, trans. John O'Sullivan (Dublin: James Duffy, 1866), Psalm LXXXV, on vv. 1, 3–5, printed pp. 259–260, PDF pp. 269–270: https://upload.wikimedia.org/wikipedia/commons/9/9d/Commentaryonbook0000bell.pdf.

Notes and limits: Re-entry on 2026-09-05: freshly inspected the identified facsimile pages at 180 dpi, using the paired Latin translation and Greek wording for Theodoret and O’Sullivan’s English for Bellarmine. Direct later canonized Doctoral exegesis checked on facsimile pages, rather than using the extracted OCR as control. Bellarmine explicitly invokes Augustine on humility versus material poverty; his account develops the source already checked in PAT-001 rather than supplying an independent ancient witness.

Exact acquisition receipts: see the public-identity receipt register below under PAT-019. Machine-local storage paths are omitted from this tracked brief.

#### PAT-020 — patristic-reception

Claim: Bellarmine interprets the Gradual's building of Zion as Christ's present establishment of the Church, and the appearance in glory as the future judgment following the humility of his first coming.

Evidence:

- Bellarmine, Commentary on the Book of Psalms, O'Sullivan/Duffy 1866, Psalm CI, on the clauses 'And the Gentiles shall fear thy name' and 'For the Lord hath built up Sion', printed p. 317, PDF p. 327: https://upload.wikimedia.org/wikipedia/commons/9/9d/Commentaryonbook0000bell.pdf.

Notes and limits: Re-entry on 2026-09-05: freshly inspected the identified facsimile pages at 180 dpi, using the paired Latin translation and Greek wording for Theodoret and O’Sullivan’s English for Bellarmine. Direct later Doctoral reception verified on the page image. The book numbers these two verse-comments 15–16; the controlling Missal appoints Ps. 101:16–17. Cite the quoted lemma and psalm to prevent mechanical transfer of this edition’s verse labels.
 Complete facsimile retrieval receipt is attached to PAT-019.

#### PAT-021 — patristic-reception

Claim: Bellarmine takes the Alleluia's wonders to encompass Christ's Incarnation, healings, Resurrection, Ascension and mission, emphasizing that Christ's victory acts through humility, obedience and sacrificial love.

Evidence:

- Bellarmine, Commentary on the Book of Psalms, O'Sullivan/Duffy 1866, Psalm XCVII, v. 1, printed p. 306, PDF p. 316: https://upload.wikimedia.org/wikipedia/commons/9/9d/Commentaryonbook0000bell.pdf.

Notes and limits: Re-entry on 2026-09-05: freshly inspected the identified facsimile pages at 180 dpi, using the paired Latin translation and Greek wording for Theodoret and O’Sullivan’s English for Bellarmine. Direct later Doctoral exegesis checked on facsimile. The second part of the exposition develops 'his right hand ... and his arm', which the Alleluia does not sing. Bellarmine’s claim that these are victories by the Cross rather than earthly arms is his actual interpretive move, not a new editorial analogy.
 Complete facsimile retrieval receipt is attached to PAT-019.

#### PAT-022 — patristic-reception

Claim: Bellarmine reads the Communion's justice alone as reliance on God's power rather than human counsel or strength, and its youth-to-old-age petition as David's continued testimony to God's help through the Psalms.

Evidence:

- Bellarmine, Commentary on the Book of Psalms, O'Sullivan/Duffy 1866, Psalm LXX, vv. 16–18, printed pp. 212–213, PDF pp. 222–223: https://upload.wikimedia.org/wikipedia/commons/9/9d/Commentaryonbook0000bell.pdf.

Notes and limits: Re-entry on 2026-09-05: freshly inspected the identified facsimile pages at 180 dpi, using the paired Latin translation and Greek wording for Theodoret and O’Sullivan’s English for Bellarmine. Direct later Doctoral exegesis verified on both facsimile pages. Bellarmine’s description of David and the production of the Psalms is reported as his interpretation, not accepted here as the passage’s historical date or compositional finding. It provides a personal reading alongside Augustine’s conversion/Church interpretation and Theodoret’s Moses/law interpretation.
 Complete facsimile retrieval receipt is attached to PAT-019.

#### PAT-023 — patristic-reception

Claim: Francis de Sales rejects taking the last place as a performance intended to obtain greater honor, requiring the heart's real desire for humility to correspond to its outward signs.

Evidence:

- Francis de Sales, Introduction à la vie dévote, Part III, chapter V, 'De l'humilité plus intérieure', especially the paragraph beginning 'Nous disons souvent que nous ne sommes rien'; Lyon/Paris: Perisse Frères, 1832, Gutenberg eBook 53540, lines 4409–4448: https://www.gutenberg.org/ebooks/53540.txt.utf-8.

Notes and limits: Later saintly and Doctoral spiritual reception rechecked in the registered French Perisse 1832/Gutenberg text, Part III chapter V, lines 4380–4480. It is a recognizable last-place/first-place echo of Luke 14:8–11, without an explicit Lukan citation here. Sales rejects performed humility and also a refusal of God’s gifts that obstructs charity. No author-made translation or new retrieval.

#### PAT-024 — patristic-reception

Claim: Augustine interprets Ephesians 3:13–19 through charity's good works, perseverance, heavenly hope and hidden origin in grace, explicitly finding these four dimensions in the shape of the Cross.

Evidence:

- Augustine, Epistula 140 ad Honoratum / De gratia Novi Testamenti, 25.62–26.64, with 24.60–61 and 26.65–27.67 as context, Latin text at https://www.augustinus.it/latino/lettere/lettera_141_testo.htm. The webpage itself identifies EPISTOLA 140; the filename's 141 is a delivery identifier, not the work number.

Notes and limits: Direct Latin exposition: freshly read heading identifying Epistola 140, §§60–67 (especially 62–64) on 2026-09-05. The delivery filename lettera_141 is not the letter number. §63 links the saints’ common life with one bread and one body and love of enemies; §64 names the hidden Cross root as gratuitous grace. Digital Latin text checked, no critical-edition or page-image collation. Jerome’s Eph. 3 commentary remains outside the directly inspected witnesses; no absence claim about it is made.

Exact acquisition receipts: see the public-identity receipt register below under PAT-024. Machine-local storage paths are omitted from this tracked brief.

#### PAT-025 — patristic-reception

Claim: Benedict XVI interprets Luke 14:8–11's lowest place through humanity's need for redemption and Christ's humility on the Cross, with exaltation understood as nearness to the Lord.

Evidence:

- Benedict XVI, Angelus, Castel Gandolfo, 29 August 2010, paragraphs beginning 'In this Sunday's Gospel' and 'At the end of the parable', official English text: https://www.vatican.va/content/benedict-xvi/en/angelus/2010/documents/hf_ben-xvi_ang_20100829.html.

Notes and limits: Later authoritative reception, freshly inspected the complete pre-Angelus reflection on 2026-09-05. The address treats the postconciliar reading Luke 14:1,7–14; use it for overlapping passage reception and not the 1962 formulary’s compilation. Deus caritas est 35 is cited inside its argument. Modern protected English is paraphrased; no redistribution permission for the exact HTML is inferred.

Exact acquisition receipts: see the public-identity receipt register below under PAT-025. Machine-local storage paths are omitted from this tracked brief.

#### PAT-026 — patristic-reception

Claim: Benedict XVI interprets Ephesians 3:18–19 as invitation to contemplation of Christ's inexhaustible mystery through a mind and heart informed by love.

Evidence:

- Benedict XVI, General Audience, 14 January 2009, 'Saint Paul (18): The theological vision of the Letters to the Colossians and Ephesians', paragraph beginning 'Then there is also a special concept', official English text: https://www.vatican.va/content/benedict-xvi/en/audiences/2009/documents/hf_ben-xvi_aud_20090114.html.

Notes and limits: Later authoritative reception: the mystery paragraph and its surrounding Christological and ecclesial argument were freshly read on 2026-09-05. This is a survey of Colossians and Ephesians, not a homily on this appointed Epistle. Its contemplative reading does not reject reason. Modern protected official text is paraphrased; no redistribution permission inferred.

Exact acquisition receipts: see the public-identity receipt register below under PAT-026. Machine-local storage paths are omitted from this tracked brief.

#### PAT-027 — patristic-reception

Claim: Anthony of Padua’s Dominica XVI post Pentecosten joins Ephesians 3:13–18 to the raising at Nain, interpreting indwelling faith as interior resurrection and the four dimensions through repentance and divine mercy.

Evidence:

- Saint Anthony of Padua (Antonius Patavinus), Sermones dominicales, “Dominica XVI post Pentecosten”; browser/page title “DOMENICA XVI DOPO PENTECOSTE | Saint Anthony of Padua”; §§2, 7, 12, especially §2 identifying Eph. 3 and Luke 7 and §12 expounding the dimensions. https://www.santantonio.org/en/node/869?latin=1
- Responsible host: Basilica of Saint Anthony of Padua (Basilica del Santo), santantonio.org; footer identifies PISAPFMC, Provincia Italiana di S. Antonio di Padova dei Frati Minori Conventuali. Latin digital sermon text selected by ?latin=1 despite the /en/ interface. No printed base edition, named modern editor, or translation credit is identified in the checked sermon page; the page timestamps describe web publication/modification, not Anthony’s composition or a critical-edition date. Accessed 2026-09-05.
- Exact HTML metadata: article:published_time = 2016-01-02T00:00:00+01:00; article:modified_time and og:updated_time = 2016-03-04T10:46:31+01:00. Canonical path is /en/node/869, but retain ?latin=1 in a Latin citation.

Notes and limits: Addresses the XVI citation-evidence part of CON-CIT-002a within saintly reception. Inspected sermon outline and §§2, 7, 12 in full; the complete served sermon has §§1–12. Do not transfer the Nain conjunction to this 1962 Sunday’s Luke 14 Gospel. Modern markup and editorial apparatus carry no redistribution permission inferred here. No claim about universal precedent or Roman compiler intention is made.

Exact acquisition receipts: see the public-identity receipt register below under PAT-027. Machine-local storage paths are omitted from this tracked brief.

#### PAT-028 — patristic-reception

Claim: Anthony of Padua’s Dominica XVII post Pentecosten interprets Luke 14’s dropsy as disordered desire healed by mercy, and its last place as ecclesial humility, while pairing the Gospel with Ephesians 4:1–6.

Evidence:

- Saint Anthony of Padua (Antonius Patavinus), Sermones dominicales, “Dominica XVII post Pentecosten”; browser/page title “DOMENICA XVII DOPO PENTECOSTE | Saint Anthony of Padua”; §§2, 6, 8–16: §2 divides Luke 14; §6 quotes Eph. 4:1–2; §§8–10 treat dropsy and cure; §§11–12 treat Eph. 4:3–4; §§13–15 expound humility; §16 pairs Luke 14:10 with Eph. 4:5–6. https://www.santantonio.org/en/sermons/sermoni-domenicali/domenica-xvii-dopo-pentecoste?latin=1
- Responsible host: Basilica of Saint Anthony of Padua (Basilica del Santo), santantonio.org; footer identifies PISAPFMC, Provincia Italiana di S. Antonio di Padova dei Frati Minori Conventuali. Latin digital sermon text selected by ?latin=1 despite the /en/ interface. No printed base edition, named modern editor, or translation credit is identified in the checked sermon page; the page timestamps describe web publication/modification, not Anthony’s composition or a critical-edition date. Accessed 2026-09-05.
- Exact HTML metadata: article:published_time = 2016-02-11T09:37:44+01:00; article:modified_time and og:updated_time = 2016-03-04T10:47:14+01:00. Canonical path omits the language selector; cite the full ?latin=1 URL to identify the Latin text.

Notes and limits: Addresses the XVII citation-evidence part of CON-CIT-002a within saintly reception. Inspected outline, §§2, 6, and §§8–16, retaining the difference between spiritual dropsy and the literal medical event. This sermon supplies reception of the appointed Luke passage with a distinct Pauline pairing; its references to fullness or unity do not make Ephesians 3 its appointed epistle. Authoring owns the printed References repair; this lane supplies metadata only.

Exact acquisition receipts: see the public-identity receipt register below under PAT-028. Machine-local storage paths are omitted from this tracked brief.

#### PAT-029 — patristic-reception

Claim: The reception sweep located direct ancient exegesis for every appointed biblical passage, while preserving differences in interpretation and limiting the inquiry to identified texts and loci.

Evidence:

- Introit Ps.85:1,3,5: Augustine and Theodoret, with Bellarmine, PAT-001,014,019; Gradual Ps.101:16–17: Augustine and Theodoret with Bellarmine, PAT-004,015,020; Alleluia Ps.97:1: Augustine and Theodoret with Bellarmine, PAT-005,016,021.
- Offertory Ps.39:14–15: Augustine and Theodoret with Aquinas, PAT-006,013,017; Communion Ps.70:16–18: Augustine and Theodoret with Bellarmine, PAT-007,018,022.
- Eph.3:13–21: Chrysostom, Augustine, Aquinas, Anthony, and Benedict XVI, PAT-002,003,008,009,024,026,027; Luke14:1–11: Cyril, Ambrose, Anthony, Sales’s spiritual application, and Benedict XVI, PAT-010,011,012,023,025,028.

Notes and limits: Search and inspection were passage-led in the registered source library and exact linked host texts: Augustine/NPNF English and Epistula 140 Latin; Chrysostom/NPNF English; Theodoret PG80 Greek/Latin facsimile; Cyril’s English translation from Syriac; Ambrose Latin; Aquinas Latin; Bellarmine English; Sales French; Anthony Latin; official Benedict XVI English. PDF indices and prior PAT loci served as location aids, followed by the source checks named in each finding. No author-wide or universal absence/originality result is claimed. Greek originals were sampled directly only in Theodoret’s paired pages. The inherited NPNF abridgments and uninspected Jerome commentary remain limits. Composed oration theology and the Nativity chronology citation in CON-CIT-001a are outside this lane.

### liturgical-history

#### LIT-001 — liturgical-history

Claim: The Secret Munda nos and Postcommunion Purifica already stand together in their respective ritual positions in the Old Gelasian sacramentary’s Sunday collection, with opening prayers different from the 1962 Sixteenth Sunday.

Evidence:

- H. A. Wilson, ed., The Gelasian Sacramentary: Liber Sacramentorum Romanae Ecclesiae (Oxford: Clarendon Press, 1894), book III, section XII, Item alia missa, p. 231 (PDF p. 324). Opening prayers: Fac nos ... prompta voluntate and Fac nos ... tuis obedire mandatis; Secreta Munda nos; Postcommun. Purifica. Complete scan https://archive.org/download/gelasiansacrame00wilsgoog/gelasiansacrame00wilsgoog.pdf.

Notes and limits: The edition’s p. 231 was freshly inspected on its page image on 2026-09-05. XII is the book’s section number, not the modern Sixteenth Sunday’s ordinal. The different collects prevent equating this antecedent with the whole target formulary. Wilson’s footnote reports divergent later Sunday allocations; those manuscript comparisons remain his collation, not a fresh inspection of each manuscript. The 1894 edition is public domain in the United States. The scan’s embedded text extraction yielded only 3,526 bytes of front matter, so a complete separate Internet Archive OCR was fetched for searching; claims are controlled by page images, never by that damaged embedded text. The exact OCR’s redistribution status remains unresolved in the registered artifact, so its bytes remain scratch evidence for registration review.

Exact acquisition receipts: see the public-identity receipt register below under LIT-001. Machine-local storage paths are omitted from this tracked brief.

#### LIT-002 — liturgical-history

Claim: The Collect Tua nos occurs among evening or morning prayers as well as in the Gregorian supplementary Sunday series.

Evidence:

- H. A. Wilson, ed., The Gregorian Sacramentary under Charles the Great, Henry Bradshaw Society 49 (London: Harrison and Sons, 1915), pp. 133–135, Incipiunt orationes uespertinales seu matutinales; Tua nos is the fifth Alia on p. 135 (PDF p. 193), with the O variant quaesumus domine for domine quaesumus. Sunday reuse: supplement XXXV, p. 174. Complete registered PDF https://archive.org/download/gregoriansacrame00cath/gregoriansacrame00cath.pdf; SHA-256 96fd93c73f8c9df47b6911981155b8b02cf2f2183ca6e87baad15128682d8681.
- Wilson 1915, introduction pp. xvii–xviii (PDF pp. 27–28), describes Reginae 337 and Ottobonianus 313 as ninth-century manuscripts and distinguishes the Gregorianum from the supplement; those two page images were also freshly inspected.

Notes and limits: The p. 135 page image and the pp. 133–135 surrounding text were freshly inspected on 2026-09-05. This establishes multiple ritual settings, not the original composer, the direction or date of transfer between settings, or Gregory the Great’s personal authorship. The source is already retained in src/sources; no fresh external retrieval.

#### LIT-003 — liturgical-history

Claim: The Gregorian sacramentary supplement groups Tua nos, Munda nos, and Purifica as the opening prayer, prayer over offerings, and closing prayer of Dominica XVII post Pentecosten, an antecedent triad under a different ordinal from the 1962 formulary.

Evidence:

- H. A. Wilson, ed., The Gregorian Sacramentary under Charles the Great, edited from three MSS. of the ninth century, Henry Bradshaw Society 49 (London: Harrison and Sons, 1915), supplement XXXV, Dominica XVII post Pentecosten, p. 174, R fols. 168v–169 (PDF p. 232). Complete edition: https://archive.org/download/gregoriansacrame00cath/gregoriansacrame00cath.pdf; registered exact artifact artifact.catholic-church.sacramentarium-gregorianum-hadrianum.wilson-1915-facsimile-web-2026-09-05.ia-gregorian-pdf-96fd93c7, SHA-256 96fd93c73f8c9df47b6911981155b8b02cf2f2183ca6e87baad15128682d8681.
- Wilson 1915, introduction p. xli: R labels these Sundays post Pentecosten, O post octavas Pentecosten; p. xviii distinguishes the supplement from the Gregorianum.

Notes and limits: The p. 174 page image and introduction pp. xvii–xviii and xli were freshly checked on page images on 2026-09-05. This proves the prayer grouping, not an unchanged complete formulary, an unchanged ordinal, a date of transfer to XVI, or Gregory the Great’s personal authorship. The p. 174 chant apparatus at XVII has different cues from the target. The 1915 edition is in the United States public domain; no new external retrieval was needed for this source already held in src/sources/.

#### LIT-004 — liturgical-history

Claim: Wilson’s Gregorian edition records four chants familiar from this formulary together at a historical Sunday position with different prayers and a later-added Alleluia.

Evidence:

- H. A. Wilson, The Gregorian Sacramentary under Charles the Great, HBS 49 (1915), p. 173 note c, attached to supplement XXXIII, Dominica XV post Pentecosten: Ant. Miserere mihi domine quoniam; Resp. Timebunt gentes; Off. Domine in auxilium me(um.); Com. Domine memorabor; [All. Laudate dominum.]. The corresponding opening prayer is Custodi domine. Complete retained scan https://archive.org/download/gregoriansacrame00cath/gregoriansacrame00cath.pdf; SHA-256 96fd93c73f8c9df47b6911981155b8b02cf2f2183ca6e87baad15128682d8681.
- Wilson 1915, introduction pp. xxx, xli, xliv–xlv: the chant cues are from the margins of Ottobonianus 313; round brackets mark letters lost through binding and square brackets a later addition or substitution. O’s Sunday labels reckon from Pentecost’s octave, while R’s are post Pentecosten.

Notes and limits: The p. 173 chant apparatus and pp. xli and xliv–xlv editorial explanation were freshly checked on page images; p. xxx was read in the full edition’s text layer. The Laudate dominum added by a later hand is not the target’s Cantate Domino. Incipits establish grouping, not identity of all words or melodies. The ninth-century dating and manuscript judgments are Wilson’s; no independent manuscript collation. Source already held in src/sources; no fresh retrieval.

#### LIT-005 — liturgical-history

Claim: Schuster interprets the Sixteenth Sunday as opening an autumn cycle around St Cyprian’s feast and a sequence of Sunday readings from Ephesians.

Evidence:

- Ildefonso Schuster, The Sacramentary (Liber Sacramentorum): Historical & Liturgical Notes on the Roman Missal, trans. Arthur Levelis-Marke, vol. III (London: Burns Oates & Washbourne, 1927), Sixteenth Sunday after Pentecost, p. 142 (PDF p. 158), heading Prima post natale Sancti Cypriani and opening paragraph. https://archive.org/download/LiberSacramentorum/The%20Sacramentary%20%28Liber%20Sacramentorum%29%3A%20Historical%20%26%20Liturgical%20Notes%20on%20the%20Roman%20Missal%20%28vol.%203%29.pdf
- Same volume, Twenty-second Sunday, p. 183 (PDF p. 199), explicitly begins Philippians and says it continues the following Sunday; Twenty-third Sunday, p. 186 (PDF p. 202), explicitly identifies Philippians 3:17–21; 4:1–3 and discusses the Würzburg capitulary’s post-Cyprian numbering.

Notes and limits: All three page images were freshly inspected on 2026-09-05. Schuster’s p. 142 says Ephesians continues until the Twenty-third Sunday with only XVIII excepted; his own pp. 183 and 186 contradict that endpoint. Do not repeat it. His Cyprian heading, autumn-cycle explanation, and original aliturgical status of XVIII are attributed historical judgments, not a fresh collation of the Würzburg capitulary and not a fixed occurrence rule for 1962. The 1927 edition is in the United States public domain. This complete retrieval also supports LIT-006.

Exact acquisition receipts: see the public-identity receipt register below under LIT-005. Machine-local storage paths are omitted from this tracked brief.

#### LIT-006 — liturgical-history

Claim: Schuster identifies the Sixteenth Sunday’s Gradual, Offertory, and Communion as chants also used in Epiphany and Lenten Masses.

Evidence:

- Ildefonso Schuster, The Sacramentary (Liber Sacramentorum): Historical & Liturgical Notes on the Roman Missal, trans. Arthur Levelis-Marke, vol. III (London: Burns Oates & Washbourne, 1927), Sixteenth Sunday after Pentecost, pp. 143–144 (PDF pp. 159–160). Timebunt gentes is also used on the Third Sunday after Epiphany; the Offertory is similar to that of Friday after the Second Sunday in Lent; the Communion is identical to that for Thursday after the Fourth Sunday in Lent. Complete scan https://archive.org/download/LiberSacramentorum/The%20Sacramentary%20%28Liber%20Sacramentorum%29%3A%20Historical%20%26%20Liturgical%20Notes%20on%20the%20Roman%20Missal%20%28vol.%203%29.pdf.

Notes and limits: All three comparisons were freshly checked on Schuster’s page images on 2026-09-05. His distinction between similar and identical is material. This is direct evidence of his historical liturgical interpretation, not independent word-for-word collation of the other formularies or evidence of borrowing direction. The full scan’s acquisition receipt will be attached once under LIT-005.

#### LIT-007 — liturgical-history

Claim: The Liturgical Year continuation reads this Mass as renewed ecclesial prayer for mercy leading to Eucharistic union, with the Secret preparing participation and the Postcommunion extending renewal to bodily life.

Evidence:

- The Liturgical Year, under Abbot Guéranger’s series name, trans. Dom Laurence Shepherd, Time after Pentecost, vol. II (complete-series XI), second edition (Stanbrook Abbey, Worcester; London: Burns & Oates, R. & T. Washbourne, and Art & Book Company, 1909), Sixteenth Sunday after Pentecost, p. 356 (PDF p. 377): the preceding Sunday’s raising of the widow of Naim’s son renews the Church’s confidence and introduces the Introit. Complete scan https://archive.org/download/V11TheLiturgicalYear/V11TheLiturgicalYear.pdf.
- Same edition, p. 365 (PDF p. 386): the Gospel wedding has its heavenly fulfillment and Eucharistic prelude; pp. 370–371 (PDF pp. 391–392): the Secret is related to imminent consecration and ensuing Communion, the Communion chant to thanksgiving bearing fruit, and the Postcommunion to renewal affecting the body now and hereafter.
- Same edition, title page (PDF p. 4), and preface pp. iii–iv (PDF pp. 6–7): the title gives 1909 and second edition; the preface calls this the second volume of the Continuation and speaks of the original author as deceased.

Notes and limits: The substantive loci and title page were freshly checked on images on 2026-09-05; the preface was inspected in the complete text layer. Cite the continuation rather than confidently assigning these paragraphs to Guéranger personally: the checked preface does not name the continuator. These exact bytes match the library artifact whose legacy path says english-duffy-1900-volume-11, but that path’s imprint is contradicted by the visible title page. The actual citation is the 1909 Stanbrook/London second edition. These are attributed historical liturgical interpretations, not evidence of an ancient compiler’s intention. The Naim event belongs explicitly to the preceding Sunday. The underlying 1909 printing is in the United States public domain; modern host presentation is a separate rights question.

Exact acquisition receipts: see the public-identity receipt register below under LIT-007. Machine-local storage paths are omitted from this tracked brief.

#### LIT-008 — liturgical-history

Claim: The checked historical witnesses do not establish a named compiler, an exact first-use date of the complete 1962 combination, or a documented original intention uniting all its elements.

Evidence:

- Bound of this sweep: H. A. Wilson’s Gelasian Sacramentary (1894), complete IA OCR searched for Tua nos, Munda nos, Purifica, praeveniat, gratia semper and Item alia missa; positive book III.XII, p. 231 checked on the edition page. Wilson’s Gregorian Sacramentary (1915), complete retained edition and its full text extraction searched for these prayer incipits and the corresponding Sunday section; pp. 135, 173–174 and introduction xvii–xviii, xli, xliv–xlv were checked on images.
- Ildefonso Schuster, The Sacramentary III (1927), full registered OCR searched for Sixteenth Sunday and prima post; Sixteenth Sunday pp. 142–145 and contrary neighboring-series loci pp. 183 and 186 inspected on facsimile pages. The Liturgical Year continuation, Time after Pentecost II (1909), Sixteenth Sunday pp. 356–372, with p. 356, p. 365, pp. 370–371 and title page image checks and preface text inspection.
- External discovery queries on 2026-09-05: "Tua nos" "Gelasian"; "sixteenth sunday" Schuster sacramentary; "sixteenth sunday after Pentecost" Gueranger. Modern devotional pages and search excerpts were leads only; historical claims were resolved in the named complete editions.

Notes and limits: This is a bounded and correctable negative about what this sweep established, not a universal absence claim. Damaged OCR, spelling variants, raw-line breaks, uncatalogued sources and unsearched manuscripts limit discovery. The Gregorian prayer triad and separately aligned chant group establish antecedents, while their differing ordinals and chants forbid an unchanged-whole-formulary inference. The additional claim on p. 372 of the Liturgical Year continuation that the Gospel was anticipated by eight days remains an attributed historical assertion without an independently dated transfer record in this sweep; it does not settle first use. All retrieved source receipts are attached to the positive findings; no new bytes were fetched solely for this negative. The forwarded CON-CIT-001a (Gerard article identity) and CON-CIT-002a (Anthony sermon digital citation metadata) concern other research scopes and have not been represented as repaired by this lane.

### theological-synthesis

#### THE-001 — theological-synthesis

Claim: Candidate source-grounded synthesis: the Collect's preceding and following grace, the Epistle's divine power at work within us, and the Secret's merciful purification present good works and fitness for participation as gifts sought from God.

Evidence:

- Missale Romanum (Vatican: Typis Polyglottis Vaticanis, 1962), Dominica decima sexta post Pentecosten, printed pp. 397–398, nos. 1593, 1594, 1599: Collect Tua nos; Ephesians 3:16–20; Secret Munda nos. All ten appointed texts read in the accepted source-audit record, src/gpt/liturgy/roman-rite/1962/propers/temporal/56-sixteenth-after-pentecost/propers/verified.md; the packet treats that collation as settled.
- The Roman Missal translated into the English language for the use of the laity (Philadelphia: Eugene Cummiskey, 1861), XVI. Sunday after Pentecost, Collect and Secret, printed pp. 429 and 431; registered temporal-orations-en.tsv, post-pentecosten-16 rows, freshly inspected.
- Douay–Rheims/Challoner, registered edition challoner-gutenberg-1581, Ephesians 2:4–10 and 3:13–21, in artifact verse-text-56-ephesians-10c79be0/56-ephesians.tsv; the complete six-chapter epistle was freshly inspected. Ephesians 2:8–10 is contextual illumination, not part of the appointed lesson.

Notes and limits: Class 4 candidate grounded in class 1 observations. The Collect specifies sustained good works as grace's intended effect, and Ephesians 2:10 reinforces that conjunction in the surrounding letter. The Secret asks mercy to make participation worthy. The candidate would be defeated by suppressing human action, making good works an unaided purchase of grace, or claiming that this textual conjunction establishes every technical distinction concerning operative/cooperative grace, merit, or justification. No historical reason for the selection or compiler's intention is asserted. Retrievals are empty because the accepted audit and exact registered source texts already exist locally.

#### THE-002 — theological-synthesis

Claim: Candidate source-grounded synthesis: the Gospel's correction of self-exaltation preserves honor received from another, while the Epistle and Communion redirect glory and remembrance toward God's action.

Evidence:

- Missale Romanum (1962), Dominica decima sexta post Pentecosten, printed pp. 397–398, nos. 1594, 1597, 1600: Ephesians 3:13, 20–21; Luke 14:7–11; Communion Domine, memorabor iustitiae tuae solius, Psalm 70 (71):16–18. Accepted complete collation in the target leaf's propers/verified.md, elements 3, 6, 9.
- Douay–Rheims/Challoner, challoner-gutenberg-1581, Ephesians 3 and Luke 14 in full, and Psalm 70 in full; registered verse artifacts verse-text-56-ephesians-10c79be0, verse-text-49-luke-d8269c33, and verse-text-21-psalms-578f023d, freshly inspected. Luke 14:10 explicitly retains public honor following the inviter's call; Ephesians 3:13 names apostolic tribulation before the concluding doxology.

Notes and limits: Class 4 candidate. Luke's social honor and Ephesians' doxological glory have distinct referents; shared wording does not identify them. The connection concerns receiving good without making oneself its independent source. It fails if humility becomes a guaranteed method of social promotion, if the literal meal setting disappears, or if God's favor is equated with immediate worldly success despite Paul's tribulations. Identifying Luke's inviter as Christ or the higher seat as a precise eschatological rank would need checked reception or explicit class 5 treatment. No historical dependence among selections is claimed.

#### THE-003 — theological-synthesis

Claim: Candidate source-grounded synthesis: the Gospel's bodily cure, the Epistle's strengthening of the inner person, and the Postcommunion's purification of minds with present and future bodily help join interior renewal to embodied need.

Evidence:

- Missale Romanum (1962), Dominica decima sexta post Pentecosten, printed pp. 397–398, nos. 1594, 1597, 1601: Ephesians 3:16–17, per Spiritum eius in interiorem hominem; Luke 14:2–6, cure and rescue analogy; Postcommunion Purifica ... mentes nostras ... et corporum praesens pariter et futurum ... auxilium. Accepted collated text in the target leaf's propers/verified.md, elements 3, 6, 10.
- Cummiskey, Roman Missal (1861), XVI. Sunday after Pentecost, Postcommunion, printed p. 431; registered temporal-orations-en.tsv, post-pentecosten-16/postcommunion row, freshly inspected. The historical English describes help during mortal embodied life and hereafter.
- Douay–Rheims/Challoner, challoner-gutenberg-1581, Luke 13–14 and Ephesians 3 in full, freshly inspected in the registered Luke and Ephesians verse artifacts. Luke 14:4 states that Jesus heals the man and sends him away.

Notes and limits: Class 4 candidate. Preserve the difference between the Latin prayer's explicit bodies and its historical English rendering. The Latin future bodily help permits an eschatological horizon but does not by itself specify a complete resurrection doctrine. The candidate would fail if bodily illness were diagnosed as the man's personal sin, inward strengthening and physical cure were identified as one effect, or reception of Communion were said to guarantee medical cure or longevity. The cured man is dismissed; no subsequent seating or sacramental reception is narrated.

#### THE-004 — theological-synthesis

Claim: Candidate source-grounded synthesis: prayer to the Father for strengthening through the Spirit and Christ's indwelling is communal in the Epistle, and the Gradual places divine glory before Sion, nations, and kings.

Evidence:

- Missale Romanum (Vatican typical edition, 1962), Dominica decima sexta post Pentecosten, printed pp. 397–398, nos. 1594–1595: Ephesians 3:14–21 and Gradual, Psalm 101 (102):16–17. Accepted collated texts in the target leaf's propers/verified.md, elements 3–4.
- Douay–Rheims/Challoner, challoner-gutenberg-1581, Ephesians 2:11–22 and 3:1–21, registered verse-text-56-ephesians-10c79be0/56-ephesians.tsv; complete epistle freshly read. The context names Gentile co-inheritance, access in one Spirit to the Father, and common building as God's habitation.
- Douay–Rheims/Challoner, same edition, Psalm 101 in full, registered verse-text-21-psalms-578f023d/21-psalms.tsv, physical lines 1646–1674, freshly read; especially vv. 14–23, Sion's restoration, the humble petition, subsequent generations, and peoples gathered for divine service.

Notes and limits: Class 4 candidate. Father, Spirit, Christ, all saints, and Church are in the appointed Epistle itself. The community's shared comprehension prevents inward growth from being reduced to a private feeling. Ephesians 2 and 3:1–12 and the unselected Psalm 101 verses remain context. The candidate would fail if Sion's historical referent, the faithful person's heart, and the Church were simply identified; the analogy coordinates distinct scenes of divine action. The texts do not establish a political programme, a wholesale rejection of Israel, or a doctrinal claim that created persons become identical with God's essence. No compositional intention or intertextual dependence among the liturgical selections is asserted.

#### THE-005 — theological-synthesis

Claim: Candidate source-grounded synthesis: the Collect's prayer for constant good works gains concrete moral content from the Gospel's prompt relief of distress and its correction of guests who choose precedence for themselves.

Evidence:

- Missale Romanum (1962), Dominica decima sexta post Pentecosten, printed pp. 397–398, nos. 1593 and 1597: Collect, bonis operibus iugiter ... intentos; Luke 14:1–11, especially Jesus' healing in v. 4, immediate rescue in v. 5, and instruction about the chosen seats in vv. 7–11. Accepted collation in the target leaf's propers/verified.md, elements 2 and 6.
- Cummiskey, Roman Missal (Philadelphia, 1861), XVI. Sunday after Pentecost, Collect, printed p. 429; registered temporal-orations-en.tsv, post-pentecosten-16/collect row, freshly inspected.
- Douay–Rheims/Challoner, challoner-gutenberg-1581, Luke 13–14 in full, registered verse-text-49-luke-d8269c33/49-luke.tsv, physical lines 627–696, freshly inspected; Luke 13:10–17 is a related Sabbath cure, while Luke 14:12–14 continues the meal discourse with hospitality without repayment.

Notes and limits: Class 4 candidate, specifying examples of the good sought in prayer without making them an exhaustive catalogue. Healing is Jesus' action; choosing the lower place is instruction addressed to invitees. The candidate would be defeated by generalizing this controversy to all Jews or Pharisees, presenting mercy as indifference to every law, or turning humility into withdrawal from a neighbor's need. Luke 14:12–14 is subsequent canonical context and is not appointed here. No historical reason for pairing this particular Collect and Gospel is established.

#### THE-006 — theological-synthesis

Claim: Candidate source-grounded synthesis: abundant divine power and continuing human need coexist in the Introit, Epistle, Offertory, and Communion, making confident prayer compatible with suffering and repeated pleas for help.

Evidence:

- Missale Romanum (1962), Dominica decima sexta post Pentecosten, printed pp. 397–398, nos. 1592, 1594, 1598, 1600: Introit, Psalm 85 (86):1, 3, 5; Ephesians 3:13, 20–21; Offertory's selected and repeated clauses from Psalm 39 (40):14–15; Communion's selected clauses from Psalm 70 (71):16–18. Accepted collation in the target leaf's propers/verified.md, elements 1, 3, 7, 9.
- Douay–Rheims/Challoner, challoner-gutenberg-1581, Psalms 39, 70, and 85 in full, registered verse-text-21-psalms-578f023d/21-psalms.tsv, physical lines 608–625, 1090–1113, 1406–1422, freshly read. These whole psalms retain enemies, failing strength, past deliverance, praise, and renewed requests.

Notes and limits: Class 4 candidate. The Offertory's plea that life-threatening enemies be confounded and ashamed is real and must remain part of the argument. The chant does not identify those enemies as the Gospel's observers, nor does a plea for divine rescue narrate an act of personal vengeance. The proposed relation would fail if Ephesians' superabundant power became a promise of present prosperity, the Communion's need meant earlier prayer had failed, or all the original biblical speakers were made one dramatic character. This lane establishes no particular patristic interpretation of the enemy clauses; that belongs to the reception sweep.

#### THE-007 — theological-synthesis

Claim: Candidate source-grounded synthesis: the Alleluia's new praise and the Postcommunion's sacramental renewal accompany the Communion's remembrance of divine teaching from youth into old age and its continuing plea against abandonment.

Evidence:

- Missale Romanum (1962), Dominica decima sexta post Pentecosten, printed p. 398, nos. 1596, 1600–1601: Alleluia, canticum novum ... mirabilia fecit Dominus; Communion, docuisti me a iuventute mea ... senectam et senium ... ne derelinquas me; Postcommunion, renova caelestibus sacramentis. Accepted collation in the target leaf's propers/verified.md, elements 5, 9, 10.
- Douay–Rheims/Challoner, challoner-gutenberg-1581, Psalms 70 and 97 in full, registered verse-text-21-psalms-578f023d/21-psalms.tsv, physical lines 1090–1113 and 1615–1623, freshly read. Psalm 97 connects God's wonders with manifested salvation, faithfulness to Israel, and just judgment; Psalm 70 keeps received teaching together with the aging speaker's dependence and witness.
- Cummiskey, Roman Missal (1861), XVI. Sunday after Pentecost, Postcommunion, printed p. 431; registered temporal-orations-en.tsv, post-pentecosten-16/postcommunion row, freshly inspected.

Notes and limits: Class 4 only for the restrained conjunction stated: praise and sacramental renewal coexist with memory, aging, and continuing dependence. The stronger thesis that renewal preserves a person's received history through time is a class 5 interpretive extension, not something any one appointed text explicitly teaches about the others. The Communion omits Psalm 70:17's wonderful-works clause and the later clause of v. 18 about the next generation; those belong to canonical context, not the chant. The candidate fails if newness is equated with youth, if sacramental renewal denies aging, or if novum and renova are taken as proof of deliberate textual design, a specific initiation rite, musical innovation, or liturgical reform.

#### THE-008 — theological-synthesis

Claim: Candidate source-grounded synthesis: the Secret and Postcommunion ask purification through the present sacrifice and heavenly mysteries, while the Epistle locates inward fullness in faith, charity, and divine power.

Evidence:

- Missale Romanum (1962), Dominica decima sexta post Pentecosten, printed pp. 397–398, nos. 1594, 1599, 1601: Ephesians 3:16–20; Secret, sacrificii praesentis effectu ... perfice miseratus in nobis ... participes; Postcommunion, Purifica ... renova caelestibus sacramentis. Accepted collation in the target leaf's propers/verified.md, elements 3, 8, 10.
- Cummiskey, Roman Missal (1861), XVI. Sunday after Pentecost, Secret and Postcommunion, printed p. 431; registered temporal-orations-en.tsv, post-pentecosten-16/secret and post-pentecosten-16/postcommunion rows, freshly inspected. The Secret names the efficacy of the sacrifice and mercy making the petitioner worthy of partaking; the Postcommunion again asks purification and renewal.

Notes and limits: Class 4 candidate. This differs from THE-001 by concentrating on the named sacramental means and the petition for purification both before and after participation. The liturgical placement supports that sequence of petitions; it does not give a complete causal timetable of grace. The candidate would fail if communicants were made the source of sacramental efficacy, if Christ's indwelling by faith were simply equated with Eucharistic reception, or if divine fullness meant identity with God's essence. The conjunction alone does not define validity, every requirement for reception, transubstantiation, or the full doctrine of Eucharistic sacrifice; those claims would require checked doctrinal evidence beyond this lane's textual synthesis.

#### THE-009 — theological-synthesis

Claim: Candidate exploratory proposal: the Collect, Gospel, and Communion can be read as a conversion of attention from watching and competing for precedence toward good works and remembrance of God's justice.

Evidence:

- Missale Romanum (Vatican typical edition, 1962), Dominica decima sexta post Pentecosten, printed pp. 397–398, nos. 1593, 1597, 1600: Collect, bonis operibus ... intentos; Luke 14:1, ipsi observabant eum, and 14:7, intendens quomodo primos accubitus eligerent; Communion, memorabor iustitiae tuae solius. Accepted collated text in the target leaf's propers/verified.md, elements 2, 6, 9.
- Douay–Rheims/Challoner, challoner-gutenberg-1581, Luke 14 and Psalm 70 in full, freshly read in the registered Luke and Psalms verse artifacts. Luke distinguishes the observers watching Jesus from Jesus attending to the invitees' choices.

Notes and limits: Class 5 only. Mechanism: place the Gospel's different acts of observing beside the Collect's sustained orientation toward good works and the Communion's remembered object. Fruit: a concrete examination of what worshippers notice and pursue, connecting prayer with merciful activity. Separate treatment can miss competing orientations of attention across these ritual moments. Strongest limit: shared intend- vocabulary does not establish compositional design; observing is not inherently sinful, and the Communion does not narrate the Gospel observers' conversion. Those assertions would defeat the proposal. The exact conjunction has not received a targeted precedent search in this lane, which owns no precedent finding; no novelty or absence-of-precedent claim is made. Inclusion remains contingent on the separate required precedent check.

#### THE-010 — theological-synthesis

Claim: Candidate exploratory proposal: the Gospel's guest and inviter roles, the Epistle's indwelling Christ, and the Secret's requested participation can explore how welcoming Christ accompanies receiving a place and capacity one cannot assign oneself.

Evidence:

- Missale Romanum (1962), Dominica decima sexta post Pentecosten, printed pp. 397–398, nos. 1594, 1597, 1599: Ephesians 3:17, Christum habitare per fidem in cordibus vestris; Luke 14:1, Jesus entering a house to eat, and 14:8–10, the inviter assigning places; Secret, perfice miseratus in nobis ... participes. Accepted collated text in the target leaf's propers/verified.md, elements 3, 6, 8.
- Douay–Rheims/Challoner, challoner-gutenberg-1581, Ephesians 3 and Luke 14 in full, freshly read in registered verse-text-56-ephesians-10c79be0/56-ephesians.tsv and verse-text-49-luke-d8269c33/49-luke.tsv; Luke 14:4 explicitly states that the healed man is sent away.

Notes and limits: Class 5 only. Mechanism: compare giving room to Jesus in a house and to Christ in the heart with receiving one's place from the inviter and fitness for participation through mercy. Fruit: hospitality understood without possession or control of God's gifts. An element-by-element reading can miss the change between welcoming another and being welcomed or made capable of participation. Strongest limit: Luke does not identify the Sabbath meal as a wedding or Eucharist, does not expressly identify the parable's inviter as Christ, and does not seat the healed man after dismissing him. Indwelling by faith and Eucharistic participation are not interchangeable textual statements. Any of those identities asserted as narrated fact would defeat the proposal. No targeted precedent judgment is made here; retention requires the owning precedent lane's check.

#### THE-011 — theological-synthesis

Claim: Candidate exploratory proposal: the Gospel's unanswered questions, the Epistle's knowledge of charity surpassing knowledge, and the Communion's memory of divine teaching can illuminate the difference between inability to answer and readiness to learn.

Evidence:

- Missale Romanum (1962), Dominica decima sexta post Pentecosten, printed pp. 397–398, nos. 1594, 1597, 1600: Luke 14:3–6, silence and inability to reply after the cure; Ephesians 3:17–20, charity, shared comprehension, knowledge of Christ's surpassing charity, and divine action beyond what is asked or understood; Communion, Deus, docuisti me a iuventute mea. Accepted collation in the target leaf's propers/verified.md, elements 3, 6, 9.
- Douay–Rheims/Challoner, challoner-gutenberg-1581, Ephesians 3 and Luke 14 in full, freshly read in the registered Ephesians and Luke verse artifacts. Ephesians 3:3–4 describes a disclosed mystery and a reader's understanding; those verses provide canonical context for the appointed epistemic language without becoming part of the lesson.

Notes and limits: Class 5 only. Mechanism: compare controversy ending in silence with prayer seeking knowledge exceeded by its object, then add the Communion speaker's lifetime of divine instruction. Fruit: intellectual humility that joins reasoning, charity, and teachability. Separate exposition can miss the difference between two limits of human speech: a failed reply and real understanding unable to exhaust divine charity. Strongest limit: Luke does not disclose every interlocutor's motive or final interior response, and Paul is not commenting on their silence. The proposal fails if legal inquiry itself becomes unbelief, every inability to answer becomes culpable, or faith and charity become reasons to reject thought. Precedent checking is not performed or claimed in this lane; the candidate remains available for the separate targeted check.

#### THE-012 — theological-synthesis

Claim: Candidate exploratory proposal: the Introit's inclined divine ear, the Epistle's bent knees, and the Gospel's rescue upward and invitation to rise can connect lowering and raising with prayer and aid instead of competition for height.

Evidence:

- Missale Romanum (1962), Dominica decima sexta post Pentecosten, printed pp. 397–398, nos. 1592, 1594, 1597: Introit verse, Inclina, Domine, aurem tuam; Ephesians 3:14, flecto genua mea, and 3:18, height and depth among the four dimensions; Luke 14:5, drawing an animal out of a pit, and 14:10–11, ascende superius and the humbling/exalting reversal. Accepted collation in the target leaf's propers/verified.md, elements 1, 3, 6.
- Douay–Rheims/Challoner, challoner-gutenberg-1581, Psalm 85, Ephesians 3, and Luke 14 in full, freshly read in the registered Psalms, Ephesians, and Luke verse artifacts. The accepted Missal and this English witness both carry the ass/ox rescue analogy.

Notes and limits: Class 5 only. Mechanism: compare God's figurative inclination to hear with bodily prayer, upward rescue, and a higher seat received by invitation. Fruit: a bodily imagination of humility as readiness for God and neighbor, with lowliness distinct from worthlessness. An element-by-element reading can miss that height signifies both a good rescue and a status competitively seized. Strongest limit: an anthropomorphic ear, a kneeling person, a rescue analogy, and a seating parable are different kinds of speech and action. Ephesians does not map its dimensions onto these gestures. A four-part geometry, numerological design, intentional liturgical choreography, or single literal action would defeat the candidate. No novelty judgment or targeted precedent result is asserted; the separate precedent check is still required before selection.

### source-citation-coverage

#### COV-001 — source-citation-coverage

Claim: The Cummiskey Collect record still carries the obsolete 1962 marginal locator, while the settled source audit supplies the correct locator and historical edition identity.

Evidence:

- The target propers/verified.md, Provenance and audit and Textual differences and boundaries, identifies the 1962 formulary at printed pp.397–398, nos.1592–1601, with Collect no.1593 and the 1861 Cummiskey formulary at pp.429–431.
- src/sources/works/eugene-cummiskey/roman-missal-english-laity/editions/philadelphia-1861/passages/post-pentecosten-16--collect.toml: physical line 158, notes still cite no.1575; the controlling artifact and edition manifests identify the unnamed historical translator and Philadelphia first revised edition of 1861.
- The current publication’s research/source-bindings.toml binds the three Cummiskey temporal-orations-en rows as translation controls, with explicit historical-translator qualification; sections/99-references.tex cites XVI Sunday by formulary.

Notes and limits: Moderate library metadata risk, confined to the cross-reference. The accepted source audit controls no.1593; this lane has not repeated its image collation or reopened the appointed wording. The old locator is no missing source or publication prerequisite, and the historical English must not be called an approved 1962 translation. No repository correction was made.

#### COV-002 — source-citation-coverage

Claim: All appointed English has registered source controls, with an explicit distinction between the Gutenberg Challoner electronic edition, the 1861 hand missal, and the Missal’s liturgical adaptations.

Evidence:

- The target propers/verified.md identifies all ten elements and their English controls, including Vulgate Psalm 39:14–15 versus modern 40:13–14 and Vulgate 101:16–17 versus modern 102:15–16; it preserves full biblical comparison verses where the chants select only clauses.
- src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/edition.toml: the e-text combines multiple Challoner editions, was released in 1998 and updated in 2023, and is not exactly identified with the 1899/1914 American printing. The registered Psalm, Luke, and Ephesians artifact records and current translation-control bindings were inspected.
- Cummiskey temporal-orations-en/artifact.toml: tracked public-domain TSV, SHA-256 c79e9500b1b3a50f4ed3f6096b9bf89012f16bf79a8d24c1ed365b295ec1bae0, 183 oration rows; the three Sixteenth Sunday rows preserve historical wording and abbreviated conclusions.

Notes and limits: High quotation/attribution risk if an English incipit, expanded conclusion, or newly translated chant is supplied without its controlling witness; the present audit identifies no missing English source. Gutenberg 1581 is an eBook number, not a printing year. The accepted source audit remains controlling; this is an identity and coverage check, not new wording collation.

#### COV-003 — source-citation-coverage

Claim: The present library and bindings now identify direct Epistle and Gospel witnesses at the appointed loci, so the initial absence of suitable registered passage checks must not be repeated as a current evidence gap.

Evidence:

- The current research/source-bindings.toml binds Chrysostom, Homilies on Ephesians VII, and Aquinas, Super Ephesios chapter 3 lectures 4–5, plus Cyril, Commentary on Luke Sermons CI–CII, and Ambrose, Expositio in Lucam VII.195, as inspected reception. The diagnostic read covered these bindings and their controlling work, edition, artifact, and segment records.
- segment.john-chrysostom.homilies-on-ephesians.english-npnf13-ccel-web-2026-09-05.complete-commentary identifies the complete argument and twenty-four homilies in CCEL NPNF I.13, physical lines 4997–16475 of the registered anthology; the used locus is Homily VII, not the older registered Homily XIII on Ephesians 4.
- The Cyril 2026-09-05 Payne Smith/Pearse edition records all sixteen offered parts; the registered cyril-on-luke-10-sermons-99-109-f545b082 response contains the used CI–CII, pp.471–479. The Ambrose 2026-09-05 Latin Wikisource edition records all ten books and used Book VII; its book-7-html-895ee72a artifact is retained.
- tools/source-reader list --find Ephesians --plain and --find Commentary on Luke --plain were run on 2026-09-05; the output now distinguishes these new edition states from the older narrower holdings.

Notes and limits: Positive coverage result, superseding COV-003’s initial baseline absence. Record inspection establishes source identity and declared bounds, not a new theological interpretation or independent re-verification of another lane’s substantive claims. Chrysostom is an English translation; Cyril is Payne Smith’s Syriac-based English in Pearse’s explicitly modernized web edition, not untouched 1859 wording or a Greek control. The catalog supplies no checked Greek counterpart for those new bindings; that limits original-language and work-wide claims, not a cited paraphrase at the identified loci.

#### COV-004 — source-citation-coverage

Claim: The five appointed Psalms now have identified Augustine and Theodoret reception coverage, supplemented by later sources, but the scope of the English editions remains narrower than an unabridged author-wide corpus.

Evidence:

- The target research/source-bindings.toml binds Augustine’s NPNF I.8 at Latin Psalms 39.21–25,70.18–21,85.1–3,5,7,97.1,101.16–18 and Theodoret’s PG80 at 1159A–1160D,1423B–1426C,1553C–1556B,1657C–1658D,1679B–1682B, covering all five appointed Psalm loci.
- Augustine’s 2026-09-05 english-npnf8-ccel edition and ccel-npnf108-text-d6841950 artifact manifests: tracked 5029159-byte complete offered digital volume, 81685 physical lines and all 150 headings, with explicit editorial abridgments; the header Print Basis 1886 and preface 1888 are kept distinct.
- Theodoret, Interpretatio in Psalmos, edition.migne-pg80-paris-1860, work/edition and wikimedia-pdf-72ee8714 artifact records: Schulze’s recension with paired Greek/Latin, Paris 1860; complete remote 1068-page,129500554-byte facsimile.
- Bellarmine, Commentary on the Book of Psalms, osullivan-duffy-1866 edition and commons-ia-facsimile-78b290d4 artifact: John O’Sullivan’s expressly abridged English, Dublin/London: Duffy, 1866; the publication binds Psalms 70,85,97,101 at exact pages. Aquinas Super Psalmo 39 nn.6–7 supplies its declared later witness for the remaining Psalm.

Notes and limits: Positive passage-coverage result, superseding COV-004’s initial baseline absence. The library records and current loci were inspected; this lane has not reopened the facsimile columns or interpreted the Psalms. Complete delivery does not mean unabridged translation, all surviving Latin/Greek witnesses, or all later saintly exegesis. Any negative reception claim must retain this edition/language boundary. No unregistered-source condition is imposed.

#### COV-005 — source-citation-coverage

Claim: The current historical bindings identify primary sacramentary loci, while the older ancient-sacramentary corpus still cannot support an executable negative text search or a claim of exhaustive early history.

Evidence:

- src/sources/corpora/ancient-sacramentaries-2026-08-01.toml declares eight OCR artifacts from six editions, snapshot sha256:af10423188c72d0515bfddb7a357a3e63206581be01f8bb197cd20b743a759dd; it excludes eighth-century Gelasian books, Ambrosian books, and many medieval witnesses.
- On 2026-09-05 tools/source-library search corpus.catholic-church.ancient-sacramentaries-2026-08-01 was run separately for Tua nos, sacrificii praesentis, and mentes nostras, each with --count. All three returned exit 1 because the search boundary contains a non-indexable artifact; none produced a zero-match result.
- The current target bindings identify Wilson, Gelasian Sacramentary (Oxford: Clarendon, 1894), III.12 p.231, and Wilson, Gregorian Sacramentary, HBS 49 (1915), pp. 133–135,173 note c,174, with named introduction loci. The corresponding registered full facsimile manifests and edition records were inspected; the Gregorian 432-page PDF is now tracked as ia-gregorian-pdf-96fd93c7.
- Schuster, The Sacramentary, Arthur Levelis-Marke English, vol.III (London: Burns Oates & Washbourne,1927), is bound at Sixteenth Sunday pp.143–144; its registered 462-page volume record was read. This is a named later reception witness, not a substitute for an earlier primary sacramentary.

Notes and limits: The initial general lack of direct historical loci is no longer the current state. The remaining material risk is overclaiming first composition, first assignment, compiler intent, or an absence from all sacramentaries. Failed corpus searches establish no literary absence. This lane inspected identities, artifact bounds, and binding loci without reopening their historical argument or the settled appointed-text rights. New library registration, if needed for other checked witnesses, belongs to source-registration, not to an authoring precondition.

#### COV-006 — source-citation-coverage

Claim: Direct doctrinal source records are available for precise grace, sacrifice, and Eucharistic-hope claims, but their narrowly checked loci should not be transferred to neighboring theological questions.

Evidence:

- Council of Trent, Canones et decreta, Latin Tauchnitz 1887: passages/sessio-6-decretum-16.toml identifies printed p.34 and the divine aid preceding, accompanying, and following good works; passages/sessio-22-decretum-2.toml identifies printed p.118 and the unity of Christ’s sacrifice. Both registered passage records were read; neither controls an English quotation.
- Thomas Aquinas, Summa theologiae I–II q.114 a.8, Corpus Thomisticum Latin web state 2026-08-21: passages/i-ii-114-8-corpus.toml identifies complete article units 38711–38718 and explicitly confines the claim to increase of grace already possessed; it does not settle first grace or final perseverance.
- Catechism of the Catholic Church, official English Vatican web state 2026-07-23: passage records 1362–1377 and 1402–1405 identify exact hashed source responses for Eucharistic sacrifice/presence and eschatological pledge. These records were inspected at their stated source-local bounds.

Notes and limits: Positive record-level coverage and a moderate scope risk; no new doctrinal claim or fresh source-text verification is made here. These are doctrinal illumination, not historical evidence about an oration’s compiler. A technically stronger formulation than the currently used prayer paraphrase would need its own directly checked locus; the existence of a nearby registered article is not that check. No new English translation or unrestricted reproduction grant follows from the Latin or restricted official-English record.

#### COV-007 — source-citation-coverage

Claim: The postconciliar translation inventory still contains a project-created English rendering of this Collect’s Latin incipit that cannot replace the registered historical English witness.

Evidence:

- src/sources/inventories/postconciliar-proper-translations-v1.toml, lines1708–1727, mass ot-28 Collect Tua nos: translation rights are explicitly project-created, while the ancient Latin match points to Wilson’s 1915 Gregorianum OCR with match_coverage0.9412.
- The target propers/verified.md and the Cummiskey Philadelphia1861 temporal-orations-en artifact identify the permitted Sixteenth Sunday Collect at TSV line158, with Secret and Postcommunion at159–160.
- guidance/liturgy/roman-1962-propers.md, Published Text and English, requires quoted registered public-domain English and forbids a new rendering authored by the guide.

Notes and limits: High concrete attribution risk if search-by-incipit promotes this project-created rendering into the historical witness. The current publication has the correct Cummiskey control, so this is a retained risk, not a missing source or a requested new translation. The old Gregorianum OCR match remains a locating lead distinct from the primary facsimile loci now bound for history.

#### COV-008 — source-citation-coverage

Claim: The library has a direct Jerome source behind Gadenz’s Lukan-provenance report, while the registered Gadenz excerpt cannot support uninspected Luke 14 commentary.

Evidence:

- Pablo T. Gadenz, The Gospel of Luke (Baker Academic, 2018), passages/introduction-pages-16-19.toml and ccss-publisher-excerpt-pdf-1c4a7e38/artifact.toml: a restricted 27-page publisher excerpt covering introduction and chapter 1, with the Achaia/Boeotia note at printed p. 19 n. 20 identified as secondary reporting.
- Jerome, Commentariorum in Evangelium Matthaei, prologue, Vallarsi/Maffei text in PL 26 (Paris, 1845), col.18, artifact p.14: passages/prologus-luke.toml and segment pl26-columns-15-218.toml directly record the passage and the adjacent apparatus’s contrary ancient testimony.
- The current target bindings separately identify official USCCB Ephesians 3 and Luke 14 chapter-note responses as contextual witnesses; the older Psalms introduction remains catalog-only for this publication. These binding states were read, not promoted to new inspections.

Notes and limits: Positive replacement lead and a moderate scope risk. A checked direct Jerome citation can replace reporting only Gadenz’s note; the edition’s recorded disagreement remains material. The publisher excerpt is not the full commentary, and no new biblical date or authorship conclusion is supplied by this diagnostic. Biblical chronology remains governed by the corpus. This lane read source records, not the restricted publisher excerpt or the remote PL26 image anew.

#### COV-009 — source-citation-coverage

Claim: Earlier OCR-only source records and normalized calendar projections must remain distinct from the accepted full facsimile collation for this proper.

Evidence:

- Pustet 1862 passages/pentecost-16-orations.toml still records only text-layer inspection, with explicit missing-image limits; the current proper’s propers/verified.md records later image collation on 2026-09-05 and no unresolved Latin reading.
- src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml, pentecost-16 Collect, Secret, and Postcommunion entries, lines8275–8352, identifies a Triptych editorial projection with removed accents, expanded ligatures, and normalized consonantal i/j. Its Postcommunion note records an older OCR omission of et before renova, with 1570/1604 corroborants.
- The current research/source-bindings.toml separately binds the 1962 CMAA facsimile as textual control and the 1862 Pustet facsimile as rights control, verified_on 2026-09-05, across all ten elements.

Notes and limits: Moderate provenance/state risk, not a reopened Latin or rights defect. The packet settles the source audit, so an older OCR limitation cannot undo its later image collation. Use the appointed-text transcription under that audit, not an editorial calendar projection presented as the book’s exact typography. This lane does not mutate either source record; source-registration owns any metadata reconciliation supported by receipts.

#### COV-010 — source-citation-coverage

Claim: The 03738a Nativity witness is John Gerard’s General Chronology, whose exact citation bundle is available without altering the inherited chronology assertion.

Evidence:

- John Gerard, “General Chronology,” The Catholic Encyclopedia, vol. 3 (New York: Robert Appleton Company, 1908), section “Christian era,” first paragraph; New Advent transcription by Rick McCarty, https://www.newadvent.org/cathen/03738a.htm#Christian. The fetched HTML identifies author, title, volume, imprint, and transcriber in its About this page apparatus; the complete article was acquired directly on 2026-09-05.
- Registered witness artifact.catholic-encyclopedia.volume-3.new-york-1908.newadvent-03738a-5eb03e5b: artifact.toml records retrieval/access on 2026-08-26, SHA-256 5eb03e5b5707514be6a0075d41f99970fd38a2dffe9c157191fa2fe3666c1dd0, and 44502 bytes. Its edition and artifact records were read directly.
- Registered retained derivative artifact.catholic-encyclopedia.volume-3.new-york-1908.newadvent-03738a-5eb03e5b-article-text: the exact retained text was inspected at physical lines 31–33, heading and paragraph “Christian era”; line 33 contains the inherited label “the year of Rome 750 which he styles 3 B.C.” in a report of an opinion held by many. Parent and derivative manifests identify the same article.

Notes and limits: Supplies the missing research input requested by CON-CIT-001a. Use the registered witness’s recorded access date, 2026-08-26, when citing that artifact; 2026-09-05 is the separate present recheck. The fresh HTML has different bytes, so it is receipted separately, not substituted under the existing artifact ID. Preserve the immutable label, disputed disposition, and reported-traditional qualification; the passage reports an opinion and is not a fresh independent Nativity date. The citation is to General Chronology, not Christmas. This lane changes neither the chronology corpus nor the brief nor the published reference; CON-CIT-001b remains the authoring owner. The registered article-only derivative provides the existing lawful offline witness; New Advent presentation rights remain separate.

Exact acquisition receipts: see the public-identity receipt register below under COV-010. Machine-local storage paths are omitted from this tracked brief.

#### COV-011 — source-citation-coverage

Claim: Anthony’s Sunday XVI citation can name the exact Latin page, institutional host, dated web metadata, and checked section loci.

Evidence:

- Anthony of Padua, Sermones dominicales, Dominica XVI post Pentecosten; page title DOMENICA XVI DOPO PENTECOSTE, in Sermoni Domenicali, Basilica of Saint Anthony of Padua, santantonio.org, Latin web text, §§2, 7, 12; https://www.santantonio.org/en/node/869?latin=1; accessed 2026-09-05. The page footer identifies PISAPFMC, Provincia Italiana di S. Antonio di Padova dei Frati Minori Conventuali, as the website’s institutional copyright holder.
- The directly fetched complete Latin page carries OpenGraph og:updated_time=2016-03-04T10:46:31+01:00. No printed base edition, modern textual editor, or Latin-edition publication date is identified on this page: cite the Latin web edition as undated, with this separate page-update metadata and access date. The HTML canonical link omits ?latin=1, so retain the language selector in the cited public route.
- Directly inspected §§2, 7, 12: §2 explicitly pairs Ephesians 3 with the raising at Nain in Luke 7; §7 develops Ephesians 3:13–17, and §12 relates Ephesians 3:17–18 to Luke 7:14–16.
- src/sources/works/anthony-of-padua/sermo-dominica-xvi-post-pentecosten/editions/2026-09-05-basilica-latin-web-2026-09-05/edition.toml and artifacts/dominica-xvi-latin-html-29835eb6/artifact.toml were read: existing registered retrieval 2026-09-05, SHA-256 29835eb699389d45a96953a58ae8cf7b5e808972159ddfe665adfda7e424fbfd. The work record attributes the sermon to Anthony; the target source-bindings.toml binds this exact sermon as an analogue.

Notes and limits: This bundle supplies the Sunday XVI portion of CON-CIT-002a; together COV-011 and COV-012 supply both requested citations. The page-update stamp is website metadata, not a composition date or a claim of a 2016 critical edition. Preserve the stated reading pairing: these two sermons do not constitute a witness to the present Ephesians 3–Luke 14 formulary pairing. The new response differs in hash from the registered response and is receipted as new bytes; no existing artifact identity was overwritten. Full-page redistribution rights remain unresolved in the existing artifact record; this is a citation and attributed-reception witness, not an English proper-text source. Citation use in References remains CON-CIT-002b’s authoring work.

Exact acquisition receipts: see the public-identity receipt register below under COV-011. Machine-local storage paths are omitted from this tracked brief.

#### COV-012 — source-citation-coverage

Claim: Anthony’s Sunday XVII citation can name the exact Latin page, institutional host, dated web metadata, and checked section loci.

Evidence:

- Anthony of Padua, Sermones dominicales, Dominica XVII post Pentecosten; page title DOMENICA XVII DOPO PENTECOSTE, in Sermoni Domenicali, Basilica of Saint Anthony of Padua, santantonio.org, Latin web text, §§2, 6, 8–16; https://www.santantonio.org/en/sermons/sermoni-domenicali/domenica-xvii-dopo-pentecoste?latin=1; accessed 2026-09-05. The page footer identifies PISAPFMC, Provincia Italiana di S. Antonio di Padova dei Frati Minori Conventuali, as the website’s institutional copyright holder.
- The directly fetched complete Latin page carries OpenGraph og:updated_time=2016-03-04T10:47:14+01:00. No printed base edition, modern textual editor, or Latin-edition publication date is identified on this page: cite the Latin web edition as undated, with this separate page-update metadata and access date. The HTML canonical link omits ?latin=1, so retain the language selector in the cited public route.
- Directly inspected §§2, 6, 8–16: §§2 and 6 identify the Luke 14/Ephesians 4 pairing; §§8–12 give the dropsical-man and ecclesial-unity treatment; §§13–16 interpret Luke 14:8–11 and connect it to Ephesians 4:5–6.
- src/sources/works/anthony-of-padua/sermo-dominica-xvii-post-pentecosten/editions/2026-09-05-basilica-latin-web-2026-09-05/edition.toml and artifacts/dominica-xvii-latin-html-8fe0b3b5/artifact.toml were read: existing registered retrieval 2026-09-05, SHA-256 8fe0b3b50ad751847cc25a830f19b1779fceed059498e12bc463b500294f01b6. The work record attributes the sermon to Anthony; the target source-bindings.toml binds this exact sermon as an analogue.

Notes and limits: This bundle supplies the Sunday XVII portion of CON-CIT-002a; together COV-011 and COV-012 supply both requested citations. The page-update stamp is website metadata, not a composition date or a claim of a 2016 critical edition. Preserve the stated reading pairing: these two sermons do not constitute a witness to the present Ephesians 3–Luke 14 formulary pairing. The new response differs in hash from the registered response and is receipted as new bytes; no existing artifact identity was overwritten. Full-page redistribution rights remain unresolved in the existing artifact record; this is a citation and attributed-reception witness, not an English proper-text source. Citation use in References remains CON-CIT-002b’s authoring work.

Exact acquisition receipts: see the public-identity receipt register below under COV-012. Machine-local storage paths are omitted from this tracked brief.

#### COV-013 — source-citation-coverage

Claim: The selected cultural examples have identified primary literary and public-record sources, with edition and rights limits that prevent treating each complete modern delivery as freely reusable text.

Evidence:

- The current target bindings and their corresponding work, edition, artifact, and segment records were inspected for Shakespeare, Sonnets 57 (Folger); Nietzsche, Human, All Too Human §87 (Alexander Harvey, 1908); Browning, Sonnets from the Portuguese XLIII (Caradoc Press, 1906); Fitzgerald, Fatal Zero, All the Year Round p.163 (1869); and Riegle, Congressional Record p.32287 (4 October 1977). No quote aggregator is the bound control for these five examples.
- The Nietzsche artifact identifies the complete offered Harvey volume through aphorism 144, not the complete multipart German work. The Folger edition distinguishes public-domain underlying English from modern editorial material. The Fitzgerald segment names its constituent in the complete journal container rather than assigning Dickens authorship of the novel.
- The Congressional Record government-page-32287 derivative is retained under its own public-domain basis; the complete 139-page parent is restricted because it also contains newspaper reprints. Doug Batchelor’s 2014 Amazing Facts publisher PDF remains a restricted modern corroborant, including separately licensed NKJV material.

Notes and limits: Positive identity/primary-source coverage at the registered loci; this lane does not re-evaluate the examples’ cultural payoff or assert a new dependence relation. Moderate quotation/extent risk remains if whole-volume rights or an original-language check is inferred from these bounded records. The cultural lane owns substantive verification; this diagnostic confirms that the guide’s cited witnesses have exact registered controls and gives no registration precondition.

#### COV-014 — source-citation-coverage

Claim: Two reused library editions have bibliographic metadata contradicted by their own witnesses: the Liturgical Year scan is 1909, and the Dickens volume’s publisher is Chapman and Hall.

Evidence:

- The Liturgical Year, Time after Pentecost II, second edition, title leaf (PDF p.4) and preface pp. iii–iv (PDF pp.6–7), freshly acquired as the complete 539-page PDF from https://archive.org/download/V11TheLiturgicalYear/V11TheLiturgicalYear.pdf and visually inspected. The title identifies Stanbrook Abbey, Worcester; London: Burns & Oates, R. & T. Washbourne, and Art & Book Company; United States: Benziger Brothers; 1909; translator Dom Laurence Shepherd. The preface identifies a continuation after Guéranger and does not name its writer.
- The existing edition.prosper-gueranger.the-liturgical-year.english-duffy-1900-volume-11 record still says Dublin: James Duffy and Co., 1900, and its ia-pdf-95ba98e2 artifact’s rights explanation also says 1900. The newly acquired PDF has the same SHA-256 as that existing artifact, so this is bibliographic metadata about the same bytes, not a new printing inferred from a changed route.
- The Letters of Charles Dickens, vol.III, edited by his sister-in-law and eldest daughter (London: Chapman and Hall, 1882), retained artifact gutenberg-25854-text-dbc34492, title at physical lines 59–77. The library edition.charles-dickens.letters.macmillan-volume-3-gutenberg record instead says Macmillan. The same retained text identifies the relevant letter as to Mrs. James T. Fields, Glasgow, 16 December 1868, at lines 7716–7718, and names Percy Fitzgerald as author of Fatal Zero at 7797–7798; the Fitzgerald edition record’s note incorrectly describes it as a letter to Fitzgerald.
- The current sections/99-references.tex already cites the Liturgical Year’s 1909 imprint, Dickens’s Chapman and Hall 1882 volume, and the letter to Mrs. Fields. Those intelligible citations agree with the witnesses inspected in this diagnostic.

Notes and limits: Moderate source-library provenance risk; no missing witness or new publication defect is established. Keep the current correct human citations and the continuation qualification; do not derive imprint, author, or recipient from a stale machine ID or catalog note. Source-registration owns any supported library-metadata reconciliation. This lane changes no source record, and these corrections do not reopen the historical or cultural arguments. The Liturgical Year’s complete response is receipted below; Dickens’s source is already retained, so no new Dickens retrieval was made.

Exact acquisition receipts: see the public-identity receipt register below under COV-014. Machine-local storage paths are omitted from this tracked brief.

### cultural-afterlife

#### CUL-002 — cultural-afterlife

Claim: The Princess in Love’s Labor’s Lost makes “world without end” the measure of a marriage commitment that the King’s last-minute proposal cannot secure.

Evidence:

- The Bible, Douay-Rheims, Complete, Challoner revision, Project Gutenberg eBook 1581, released 1998-12-01, updated 2023-09-23; Richard Challoner (revision), Dennis McCarthy and Tad Book (electronic production); https://www.gutenberg.org/ebooks/1581 ; consulted in registered repository verse artifacts on 2026-09-05. Ephesians 3:21, src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-56-ephesians-10c79be0/56-ephesians.tsv, physical line 67: “world without end”.
- William Shakespeare, Love’s Labor’s Lost, act 5, scene 2, Folger lines 865–866 (FTLN 2762–2763): “A time, methinks, too short / To make a world-without-end bargain in.” Folger Shakespeare Library edition, Barbara A. Mowat and Paul Werstine, with Michael Poston and Rebecca Niles; FDT 0.9.2, created 2015-07-31; https://www.folger.edu/explore/shakespeares-works/loves-labors-lost/read/5/2/#line-5.2.865 ; complete text https://folger-main-site-assets.s3.amazonaws.com/uploads/2022/11/loves-labors-lost_TXT_FolgerShakespeare.txt ; accessed 2026-09-05. Complete-text physical lines 4486–4534 checked for the proposal, rejection and year’s trial.
- Folger Shakespeare Library, Love’s Labor’s Lost – Entire Play, https://www.folger.edu/explore/shakespeares-works/loves-labors-lost/read/ ; accessed 2026-09-05. Full-play HTML directly confirms scene-line IDs line-5.2.865 and line-5.2.866 beside FTLN 2762–2763. Editor and creation information come from the complete text header identified above.

Notes and limits: Qualifying theatrical/comic candidate. The quoted English phrase is identical apart from adjectival hyphenation; the relationship is a biblical/liturgical idiom echoed, not proved direct dependence on this Pauline verse or the Mass. Its turn is from endless praise to a binding earthly bargain, set against the brevity and unreliability of fashionable wooing. The Princess does not accept at once; she requires a year’s test. Use the Folger locus actually checked (5.2.865–866); other editions number this speech around 5.2.783–784 and must not be blended with Folger’s numbers. Shakespeare’s original English is public domain in the United States; modern Folger editing/presentation has separate rights. The two-line extract is brief. This and CUL-001 reuse one phrase but make distinct cultural moves; gallery selection belongs to the later worker. Citation-metadata correction from direct header inspection: this play download says FDT 0.9.2, not 0.9.0.1 as the earlier brief stated; the sonnets download separately remains 0.9.0.1. Both source files were freshly retrieved, and the scene’s surrounding proposal and trial were re-inspected.

Exact acquisition receipts: see the public-identity receipt register below under CUL-002. Machine-local storage paths are omitted from this tracked brief.

#### CUL-007 — cultural-afterlife

Claim: Bob Corker turns the Gospel’s endangered ox into a metaphor for a company crisis requiring action instead of blame.

Evidence:

- The Bible, Douay-Rheims, Complete, Challoner revision, Project Gutenberg eBook 1581, released 1998-12-01, updated 2023-09-23; Richard Challoner (revision), Dennis McCarthy and Tad Book (electronic production); https://www.gutenberg.org/ebooks/1581 ; consulted in registered repository verse artifacts on 2026-09-05. Luke 14:5, registered Luke verse artifact physical line 666: “an ox fall into a pit”; the complete verse asks whether one would immediately draw it out even on the sabbath.
- Bob Corker, interview by Cal Fussman, “What I’ve Learned: Senator Bob Corker (R, Tenn.),” Esquire, published 18 October 2010, 7:24 AM EDT; https://www.esquire.com/news-politics/news/a8668/bob-corker-interview-1110/ ; accessed 2026-09-05. Exact locus: paragraph beginning “There’s plenty of blame to go around,” especially “an ox in the ditch, if you will”; complete interview read.
- Doug Batchelor, How to Keep the Sabbath Holy (Roseville, California: Amazing Facts, Inc., 2014), ISBN 978-1-58019-618-5, “The Ox in the Ditch,” printed p. 78 (PDF page 77), first paragraph explicitly links “an ox in the ditch” to Luke 14:5. Publisher’s complete PDF https://www.amazingfacts.org/wp-content/uploads/2025/06/BK-HKSH.pdf ; accessed 2026-09-05; title/copyright text and p. 78 image inspected on this iteration. Used only as a primary modern witness to the idiom’s consciously biblical association, not for the theology of Sabbath observance or for earliest origin.

Notes and limits: Qualifying business idiom in a politician’s interview. Rescue becomes practical company problem-solving. Relationship: idiomatic echo, not a verbatim biblical quotation or documented direct dependence by Corker; “ditch” differs from the appointed “pit.” Original English; Esquire interview protected, retain only the nine-word phrase for quotation. Batchelor is a separate protected corroborant of the idiom’s Luke 14:5 association, not evidence of Corker’s reading. No claim is made about Corker’s current office or policies. This iteration freshly retrieved and read the complete Esquire interview; its own headline, byline and published timestamp confirm the citation bundle. Batchelor’s identical publisher PDF is receipted once under CUL-006 and is the same checked corroborant here.

Exact acquisition receipts: see the public-identity receipt register below under CUL-007. Machine-local storage paths are omitted from this tracked brief.

#### CUL-008 — cultural-afterlife

Claim: No qualifying Introit afterlife was established in this iteration’s checked phrase searches.

Evidence:

- The Bible, Douay-Rheims, Complete, Challoner revision; Richard Challoner (revision), Dennis McCarthy and Tad Book (electronic production); Project Gutenberg eBook 1581, released 1998-12-01, updated 2023-09-23; https://www.gutenberg.org/ebooks/1581 ; accessed through registered verse artifact on 2026-09-05, src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-21-psalms-578f023d/21-psalms.tsv. Appointed selection and adaptation boundaries were read in the target leaf’s propers/verified.md. The English is a registered historical translation, not a new rendering. Exact loci: Psalm 85:1, Psalm 85:3, Psalm 85:5.

Notes and limits: Introit: Psalm 85 (86):1, 3, 5. Exact appointed phrases swept: I am needy and poor; sweet and mild; the plea for mercy. Web queries on 2026-09-05 included "needy and poor" Shakespeare and "sweet and mild" Psalm poem parody. Bible/exposition matches and generic adjectival poetry did not establish the gallery’s redirected verbal reuse. A new discovery lead, the medieval mock-Gospel called Gospel According to the Mark of Silver / Evangelium secundum marcas argenti, appeared in English secondary material; the Latin search lead has egenus et pauper rather than the Introit’s inops et pauper, and no underlying edition was inspected. That lead is not promoted as a verified Introit afterlife. This is a negative within these English/Latin title and phrase searches and the primary works checked under CUL-001–007, not an absence claim across medieval literature, translations or visual art.

#### CUL-009 — cultural-afterlife

Claim: No qualifying Gradual afterlife was established in this iteration’s checked phrase searches.

Evidence:

- The Bible, Douay-Rheims, Complete, Challoner revision; Richard Challoner (revision), Dennis McCarthy and Tad Book (electronic production); Project Gutenberg eBook 1581, released 1998-12-01, updated 2023-09-23; https://www.gutenberg.org/ebooks/1581 ; accessed through registered verse artifact on 2026-09-05, src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-21-psalms-578f023d/21-psalms.tsv. Appointed selection and adaptation boundaries were read in the target leaf’s propers/verified.md. The English is a registered historical translation, not a new rendering. Exact loci: Psalm 101:16, Psalm 101:17.

Notes and limits: Gradual: Psalm 101 (102):16–17, corresponding to modern English 102:15–16. Queries on 2026-09-05: "built up Sion" satire and "all the kings of the earth thy glory" literature. Returned leads were principally Scripture, exposition, religious application and a nonspecific phrase about kings in drama. None provided a checked redirection of the appointed wording. Broader Zion imagery or royal imagery cannot by itself establish this verbal link. Negative is limited to these web searches and inspected works, not all literature or musical/visual reception.

#### CUL-010 — cultural-afterlife

Claim: The Alleluia sweep found an ironic thesis-title lead but no additional fully verified gallery candidate.

Evidence:

- The Bible, Douay-Rheims, Complete, Challoner revision; Richard Challoner (revision), Dennis McCarthy and Tad Book (electronic production); Project Gutenberg eBook 1581, released 1998-12-01, updated 2023-09-23; https://www.gutenberg.org/ebooks/1581 ; accessed through registered verse artifact on 2026-09-05, src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-21-psalms-578f023d/21-psalms.tsv. Appointed selection and adaptation boundaries were read in the target leaf’s propers/verified.md. The English is a registered historical translation, not a new rendering. Exact loci: Psalm 97:1.
- Jon Edward Bullock, “'Sing unto the Lord a New Song--Just Not That One!' A Case Study of Music Censorship in Free Will Baptist Colleges,” MA thesis, Liberty University, Department of Worship and Music – Ethnomusicology, June 2015; Katherine Morehouse, chair. Liberty University Scholars Crossing, Masters Theses 370, https://digitalcommons.liberty.edu/masters/370/ ; accessed 2026-09-05. Exact checked loci: page headline, Date 6-2015, Department, Degree, Chair, Recommended Citation, and the complete author-supplied Abstract. Repository footer says downloads counted since June 22, 2015; no later edition stamp is supplied. The full thesis PDF was not obtained; this evidence is limited to the repository record and abstract, not a complete thesis inspection.

Notes and limits: Alleluia: Psalm 97 (98):1, opening sentence, Sing ye to the Lord a new canticle; Latin Cantate Domino canticum novum. Queries on 2026-09-05 included "Cantate Domino" parody advertisement, "Sing unto the Lord a new song" satire novel, and the exact Bullock thesis title. Ordinary settings and bare incipits remain excluded; an Adiemus/Cantate Domino advertising association did not verify that the appointed words occur in an advertisement. Bullock’s title deliberately restricts the imperative with Just Not That One, and the author’s abstract describes the tension between spiritual authority and students’ musical choices, making it a promising ironic institutional candidate. However, the primary thesis body at the repository’s full-download URL https://digitalcommons.liberty.edu/cgi/viewcontent.cgi?article=1365&context=masters returned HTTP 403 on this iteration. Only its author-supplied repository abstract and metadata were obtained. The original argument and exact biblical source identification were not inspected, so this candidate is not counted among the seven fully checked candidates. New-song wording occurs in several psalms; no specific dependence on Psalm 97/98 or this Mass is asserted. Modern 2015 thesis/abstract and host markup remain protected, with only the brief title phrase needed; no new translation or republication permission inferred. This result is bounded to the stated searches and available abstract, not a claim that the thesis would fail after a complete check.

Exact acquisition receipts: see the public-identity receipt register below under CUL-010. Machine-local storage paths are omitted from this tracked brief.

#### CUL-011 — cultural-afterlife

Claim: No qualifying Offertory afterlife was established in this iteration’s checked phrase searches.

Evidence:

- The Bible, Douay-Rheims, Complete, Challoner revision; Richard Challoner (revision), Dennis McCarthy and Tad Book (electronic production); Project Gutenberg eBook 1581, released 1998-12-01, updated 2023-09-23; https://www.gutenberg.org/ebooks/1581 ; accessed through registered verse artifact on 2026-09-05, src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-21-psalms-578f023d/21-psalms.tsv. Appointed selection and adaptation boundaries were read in the target leaf’s propers/verified.md. The English is a registered historical translation, not a new rendering. Exact loci: Psalm 39:14, Psalm 39:15.

Notes and limits: Offertory: the appointed selections from Psalm 39 (40):14–15, modern English 40:13–14. Queries on 2026-09-05 paired "look down, O Lord, to help me" with literature, and "seek after my soul to take it away" with poem satire. Results were biblical text, chant, prayer-book reproduction and exposition, with no verified later cultural redirection. The famous new-song image earlier in Psalm 40 is outside the appointed verses and does not supply an Offertory candidate. Negative is limited to these phrase searches and checked works.

#### CUL-012 — cultural-afterlife

Claim: No qualifying Communion afterlife was established in this iteration’s checked phrase searches.

Evidence:

- The Bible, Douay-Rheims, Complete, Challoner revision; Richard Challoner (revision), Dennis McCarthy and Tad Book (electronic production); Project Gutenberg eBook 1581, released 1998-12-01, updated 2023-09-23; https://www.gutenberg.org/ebooks/1581 ; accessed through registered verse artifact on 2026-09-05, src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-21-psalms-578f023d/21-psalms.tsv. Appointed selection and adaptation boundaries were read in the target leaf’s propers/verified.md. The English is a registered historical translation, not a new rendering. Exact loci: Psalm 70:16, Psalm 70:17, Psalm 70:18.

Notes and limits: Communion: appointed selections from Psalm 70 (71):16–18, including I will be mindful of thy justice alone and O God, forsake me not. Queries on 2026-09-05 paired those exact phrases with novel. Results included biblical text, devotional hymnody and dying-word attribution leads; they did not supply a verified change in the appointed wording’s force. A prayer repeated in devotional use is outside the gallery rule, and general older-age language is too broad to establish dependence. No claim is made about absence from unsearched print, visual, musical, or other-language sources.

#### CUL-013 — cultural-afterlife

Claim: The fourth-dimensional church lead remains unsuitable for the gallery because the original Gardner narrative has not been verified.

Evidence:

- The Bible, Douay-Rheims, Complete, Challoner revision; Project Gutenberg eBook 1581, released 1998-12-01, updated 2023-09-23; Richard Challoner (revision), Dennis McCarthy and Tad Book (electronic production); https://www.gutenberg.org/ebooks/1581 ; registered Ephesians 3:17–18 text inspected 2026-09-05, physical lines 63–64 of src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/verse-text-56-ephesians-10c79be0/56-ephesians.tsv.
- Rudy Rucker, The Fourth Dimension: Toward a Geometry of Higher Reality, second edition (Dover Publications, 2014), author-hosted web edition copyright 2016, https://www.rudyrucker.com/thefourthdimension/ ; original access recorded 2026-09-05. Prior audit locus: Part I, chapter 5, Ghosts from Hyperspace?, Martin Gardner sidebar The Church of the Fourth Dimension (1962), after figure 62. This iteration inspected the registered artifact metadata at src/sources/works/rudy-rucker/the-fourth-dimension/editions/2026-09-05-author-web-2026-09-05/artifacts/author-complete-html-beda0cab/artifact.toml; the complete work’s exact protected HTML is not retained in Git. The prior excerpt-only reading is not a fresh underlying-source verification.
- Martin Gardner, “Mathematical Games: An adventure in hyperspace at the Church of the Fourth Dimension,” Scientific American 206, no. 1 (January 1962), starting p. 136, DOI 10.1038/scientificamerican0162-136; publisher page dated 1 January 1962, https://www.scientificamerican.com/article/mathematical-games-1962-01/ ; original access recorded 2026-09-05. This iteration inspected registered artifact metadata at src/sources/works/martin-gardner/mathematical-games-1962-01/editions/2026-09-05-publisher-landing-web-2026-09-05/artifacts/publisher-metadata-html-7fd29742/artifact.toml. The record explicitly states that only title, byline, date and bibliographic credit were returned, without the original narrative; the source’s original article was marked isAccessibleForFree=false.

Notes and limits: Not counted as a qualifying candidate. The inherited audit reports a Gardner excerpt naming Ephesians 3:17–18 and turning the dimensions into hyperspatial theology, but an excerpt in a later book cannot establish the original satire’s complete context. This iteration checked the recorded access and extent boundaries, without new retrieval or promotion of the underlying work. The original narrative remains unverified. Both Gardner’s 1962 text and Rucker’s modern work remain protected. Seven other candidates are independently checked, so the gallery does not depend on resolving this lead.

### precedent-search

#### PRE-001 — precedent-search

Claim: The immediately preceding GPT Fifteenth-Sunday guide supplies a reusable substantive structure: direct thematic opening, five functional cross-proper units, an independently integrated commentary, and six separately audited exploratory conjunctions.

Evidence:

- Triptych, GPT, 55-fifteenth-after-pentecost, sections/synthesis/10-themes-and-movement.tex, opening and units 1–5: heard cry and communicated life; grace and responsible action; differentiated registers of life; public praise; sacramental transformation.
- Same guide, sections/synthesis/20-integrated-commentary.tex, five cross-proper subsections; sections/35-source-grounded-synthesis.tex, six thematic relations; research/scope.md, Interpretive-proposal audit, IP-1–IP-6, lines 633–753.

Notes and limits: Inspected repository precedent at the packet's seed checkout. Reuse concerns the arrangement of claims and evidence, not prior wording or the guide's own judgments as theological authority. The current profile still controls exact page count, component membership, and semantic fields; no PDF or layout acceptance was inferred from source inspection. Re-entry: cited source sections re-inspected and unchanged corpus fingerprint replayed on 2026-09-05.

#### PRE-002 — precedent-search

Claim: Several nearby guides preserve rhetorical scaffolds now expressly disallowed, so their substantive movements cannot be adopted by copying their wrappers.

Evidence:

- GPT 50-tenth-after-pentecost, sections/synthesis/10-themes-and-movement.tex:4; GPT 51-eleventh-after-pentecost, sections/synthesis/10-themes-and-movement.tex:7; GPT 52-twelfth-after-pentecost, sections/20-themes.tex:5; GPT 53-thirteenth-after-pentecost and 54-fourteenth-after-pentecost, sections/synthesis/10-themes-and-movement.tex:6: all use a Governing thesis box.
- guidance/editorial.md, Reader-first structure; guidance/liturgy/roman-1962-propers.md, Themes, commentary, and exploration: a single Governing thesis, Thesis, Key takeaway, Argument map, Reading order, or equivalent wrapper is a structural defect.

Notes and limits: Observed nonconforming precedent, not a reusable pattern. The GPT 55 direct prose opening is the nearer conforming alternative. This finding concerns reader-facing scaffolding only and does not assert that the earlier research is unusable. Re-entry: cited source sections re-inspected and unchanged corpus fingerprint replayed on 2026-09-05.

#### PRE-003 — precedent-search

Claim: The repeated precedent sweep reproduces the same 328-file two-provider proper-guide snapshot and eight conjunction searches, supplemented by two complete Anthony sermon pages and the Sixteenth-Sunday chapter of the 1909 Liturgical Year continuation.

Evidence:

- Local corpus: every *.tex and research/scope.md under src/gpt/liturgy/ and src/claude/liturgy/ whose path contains /propers/, excluding both providers’ current 56-sixteenth-after-pentecost leaf. All 328 path/hash entries reproduce the earlier manifest exactly; corpus-files.sha256 SHA-256 43ed2e1592bbd72360538c2374ce43b7bf69b0142674f43e6ed41e59c342179c.
- Repeated complete-file case-insensitive DOTALL regex co-occurrence searches, conjunction-searches.json: C1 swelling/fullness 0 files; C2 lifelong grace 41; C3 dwelling/common space 110; C4 lowering/raising 39; C5 shame/self-examination 16; C6 renewal/age 20; C7 grace/justice alone 56; C8 body/mind/healing 62. These are file co-occurrences, not counts of precedents.
- Fresh external exact downloads: Anthony XVI, https://www.santantonio.org/en/node/869?latin=1, sections 1–12; Anthony XVII, https://www.santantonio.org/en/sermons/sermoni-domenicali/domenica-xvii-dopo-pentecoste?latin=1, sections 1–16 (PRE-005 receipts); The Liturgical Year continuation XI (1909), complete PDF, Sixteenth-Sunday chapter printed pp. 356–372, PDF pp. 377–393, opening/closing adjacent material excluded from the chapter claim (PRE-006 receipt).

Notes and limits: English and Latin lexical families were searched using ripgrep and complete-file regular expressions, then the named nearest passages were read. A second ripgrep searched old.age, senect-, grey/gray hair, youth and iuvent- across all 328 files; its new-song/renewal candidate contexts were inspected. Exact passage/incipit search also reached other GPT/Claude publication genres, but these received no exhaustive semantic or author-wide search. This excludes other checkouts, unpublished branches, paywalled material, complete external author corpora, and a universal web survey. Whole-file hits may be accidental (for example aging within packaging); zero regex hits do not exclude synonyms, inflection, markup differences or paraphrase. The sweep covered eight distinctive conjunctions, PRE-007–014, before any re-entry synthesis selection.

#### PRE-004 — precedent-search

Claim: Nearby guides already treat overlapping psalms, humility, plenitude, and the later portion of Luke 14, but their appointed limits differ from the present formulary.

Evidence:

- GPT 55-fifteenth-after-pentecost, sections/synthesis/10-themes-and-movement.tex, unit 1, and research/scope.md, Psalm 85:1–4 reception row, lines 346–365: needy prayer and gifted praise; its Offertory is Psalm 39:2–4, whereas the current Offertory selects 39:14–15.
- GPT 48-eighth-after-pentecost, research/scope.md, Psalm 70:1 reception row and Augustine locus, lines 35 and 70: hope transferred from self to Christ; it does not appoint the current Communion’s youth/old-age selection.
- GPT 41-second-after-pentecost, main.tex, Gospel commentary and interpretive speech-to-song proposal at lines 273–280; research/scope.md, Luke 14:16–24 row and proposal audit: banquet refusal and charity in deed, from a different pericope.
- Claude 51-eleventh-after-pentecost, sections/30-commentary.tex:284–295: Ephesians 3:20 as an echo in its Collect, not its appointed Epistle; GPT 50-tenth-after-pentecost, main.tex:75–101: Luke 18’s humiliation/exaltation and relinquished self-verdict.

Notes and limits: These are inspected Triptych treatments, not fresh verification of every Father those guides cite. They offer locations to reuse or compare through the normal source checks. Do not import Nain into Luke 14, the great-supper invitation into the appointed vv. 1–11, earlier Psalm 39 verses into this Offertory, or Psalm 70:1 into the Communion as though appointed. Re-entry on 2026-09-05: the unchanged corpus and all eight search families were replayed, the named nearest passages re-inspected, and the two Anthony pages and complete Liturgical Year volume freshly retrieved. PRE-005 now supplies complete Anthony citation metadata; PRE-006 supplies the corrected 1909 continuation identity. No novel universal-priority claim is made.

#### PRE-005 — precedent-search

Claim: Anthony provides genuine cross-reading precedent with fully recovered Latin citation identities, while his XVI and XVII sermons retain distinct Ephesians 3–Luke 7 and Ephesians 4–Luke 14 reading pairs.

Evidence:

- Anthony of Padua (Antonius Patavinus), Sermones dominicales, Dominica XVI post Pentecosten; page heading DOMINICA XVI POST PENTECOSTEN, within Sermoni Domenicali, Basilica of Saint Anthony of Padua website, operated by PISAPFMC, Provincia Italiana di S. Antonio di Padova dei Frati Minori Conventuali (identified in the page footer). Latin digital text selected by ?latin=1; stable checked route https://www.santantonio.org/en/node/869?latin=1; accessed 2026-09-05. Page metadata: article:published_time 2016-01-02T00:00:00+01:00; article:modified_time and og:updated_time 2016-03-04T10:46:31+01:00. These are web-node datestamps; no base print edition, editor, or critical apparatus is identified by the checked page. Complete offered sermon: thematic outline and numbered sections 1–12, four text panels.
- Anthony, Dominica XVI, section 2 explicitly pairs the Nain resurrection (Luke 7) with the Epistle beginning Obsecro vos ne deficiatis (Ephesians 3:13); section 7 treats Ephesians 3:13–17 and kneeling/indwelling; section 12 develops rooted/founded charity and the four dimensions, Ephesians 3:17–18. The Gospel is Luke 7, not Luke 14.
- Anthony of Padua (Antonius Patavinus), Sermones dominicales, Dominica XVII post Pentecosten; Latin page heading DOMINICA XVII POST PENTECOSTEN (HTML title and og:title retain the Italian DOMENICA XVII DOPO PENTECOSTE), within Sermoni Domenicali, same Basilica website and responsible Conventual Franciscan province. Latin digital text selected by ?latin=1; stable checked route https://www.santantonio.org/en/sermons/sermoni-domenicali/domenica-xvii-dopo-pentecoste?latin=1; accessed 2026-09-05. Page metadata: article:published_time 2016-02-11T09:37:44+01:00; article:modified_time and og:updated_time 2016-03-04T10:47:14+01:00. These are web-node datestamps, not a supplied base-edition date; no print editor or critical-edition identity is given. Complete offered sermon: thematic outline and numbered sections 1–16, five text panels.
- Anthony, Dominica XVII, section 2 announces Luke 14 and Ephesians 4:1 and explains humility as preserving ecclesial unity; section 6 expounds Ephesians 4:1–2; sections 7–12 develop dropsy, distorted appetite, healing and unity, with section 11 the link to Ephesians 4:3–4; sections 13–16 expound the lower place, humility, invitation higher, and Ephesians 4:5–6. The Pauline reading is Ephesians 4, not Ephesians 3.

Notes and limits: Classification: near analogue located. This supplies the evidence bundle requested by CON-CIT-002a without changing published References (CON-CIT-002b belongs to authoring). The supplied section loci were checked in exact direct-download HTML and surrounding paragraphs; the entire two pages were retained and searched, not the entire sermon collection. The XVI node route is essential: the guessed /en/sermons/sermoni-domenicali/domenica-xvi-dopo-pentecoste?latin=1 returned a sermon index rather than this sermon. The /en/ path is not evidence of English text, and XVII without its selector serves Italian. Modern page markup and editorial apparatus have no located redistribution grant; the prior artifact records classify their redistribution rights as unresolved. Anthony’s quotations of earlier authors remain leads until their underlying works are checked independently. The current downloads are separately hashed exact responses; their HTML hashes are not substituted for the already registered earlier responses. The recovered bibliographic bundle applies to the stated Latin sermon witnesses.

Exact acquisition receipts: see the public-identity receipt register below under PRE-005. Machine-local storage paths are omitted from this tracked brief.

#### PRE-006 — precedent-search

Claim: The Sixteenth-Sunday chapter in the 1909 second-edition continuation of The Liturgical Year is the nearest located full-formulary commentary, joining indwelling, common praise and Sion, and distinguishing preparation for Communion from its continuing fruits.

Evidence:

- The Liturgical Year, continued under Abbot Guéranger’s series name, translated from the French by Dom Laurence Shepherd, O.S.B., Time after Pentecost, vol. II (= complete-series XI), second edition (Stanbrook Abbey, Worcester; London: Burns & Oates, Ltd.; R. & T. Washbourne, Ltd.; Art & Book Company, Ltd.; United States: Benziger Bros., New York, Cincinnati & Chicago, 1909), The Sixteenth Sunday after Pentecost, printed pp. 356–372; https://archive.org/download/V11TheLiturgicalYear/V11TheLiturgicalYear.pdf; accessed 2026-09-05.
- Title page (PDF p. 4) visibly prints 1909 and second edition; preface p. iii (PDF p. 6) calls this the second volume of the Continuation, and p. iv (PDF p. 7) speaks of the deceased author. The checked preface does not name the continuator. The earlier source-library directory’s english-duffy-1900 label is not the imprint of these exact bytes.
- Printed p. 359 develops inward strengthening and plenitude; p. 363 passes from ecclesial union and praise to Sion built by the divine Architect. Printed pp. 368–370 develop humility, contempt and shame before introducing the Offertory; pp. 370–371 distinguish sacrificial preparation for Communion from renewed life and bodily aid now and hereafter.

Notes and limits: Classification: precedent located for the stated cross-proper relations. The whole Sixteenth-Sunday chapter was read in its full-volume text layer, and title page, preface p. iii, and printed pp. 359, 363, 368–371 were checked on page images. The chapter begins partway through p. 356 and ends early on p. 372; adjacent Fifteenth/Seventeenth-Sunday matter is not attributed to it. The 1909 continuation identification preserves the correction already accepted in the immutable brief and replaces the prior PRE-006 Dublin/Duffy 1900 and personal Guéranger attribution. Seasonal programmes and compiler-intention statements remain this commentator’s attributed interpretation; its citations of earlier writers are not independent primary checks by this lane. The complete 539-page volume was acquired, while the search and inspection claim extends only to the specified chapter and front matter.

Exact acquisition receipts: see the public-identity receipt register below under PRE-006. Machine-local storage paths are omitted from this tracked brief.

#### PRE-013 — precedent-search

Claim: For C7, good works sustained by grace beside God’s justice alone and the refusal of self-exaltation has a near analogue in the Tenth-Sunday distinction between real action and self-justifying possession.

Evidence:

- src/gpt/liturgy/roman-rite/1962/propers/temporal/50-tenth-after-pentecost/sections/35-source-grounded-synthesis.tex, entire three-paragraph argument: activity, gift, divine acceptance and common service remain real without becoming a private certificate of superiority.
- src/gpt/liturgy/roman-rite/1962/propers/temporal/50-tenth-after-pentecost/main.tex:84–101, Gift received, boast relinquished, offering accepted and The altar receives what boasting cannot secure.
- src/gpt/liturgy/roman-rite/1962/propers/temporal/55-fifteenth-after-pentecost/sections/synthesis/20-integrated-commentary.tex, The gift that precedes also commands: prior grace and actual responsibility are coordinated.

Notes and limits: Classification: near analogue located. Conjunction searched: Collect grace/good works, Communion iustitiae tuae solius, and Gospel self-exaltation/humility; optionally the Secret’s making-worthy is within the reached field. PRE-003 corpus and the two external comparisons; searches combined justice/iustiti-/justification, alone/solius, grace/gratia and good works. No inspected earlier guide uses the present set. Possible fruit: thanksgiving for God’s justice can discipline the way good works are remembered, instead of turning remembrance into rank. Solius does not by itself decide a complete doctrine of justification or erase grace-enabled works; the underlying Psalm 70 exegesis must be supplied by its owning lane. Re-entry on 2026-09-05: the unchanged corpus and all eight search families were replayed, the named nearest passages re-inspected, and the two Anthony pages and complete Liturgical Year volume freshly retrieved. PRE-005 now supplies complete Anthony citation metadata; PRE-006 supplies the corrected 1909 continuation identity. No novel universal-priority claim is made.

#### PRE-014 — precedent-search

Claim: For C8, the healed body, inward strengthening, and post-Communion help for bodies now and hereafter have close prior models that distinguish bodily, moral, sacramental, and final goods.

Evidence:

- src/gpt/liturgy/roman-rite/1962/propers/temporal/51-eleventh-after-pentecost/sections/50-interpretive.tex:65–78, Material signs minister to the whole person: bodily healing, offering and help for mind/body are joined with explicit differences among their actions.
- src/gpt/liturgy/roman-rite/1962/propers/temporal/52-twelfth-after-pentecost/sections/50-interpretive.tex, The medicine is neither only natural nor only sacramental: practical wound care, created provision and sacramental participation.
- src/gpt/liturgy/roman-rite/1962/propers/temporal/55-fifteenth-after-pentecost/sections/50-interpretive.tex, Four registers of life; sections/synthesis/20-integrated-commentary.tex, One formulary coordinates four registers of life.

Notes and limits: Classification: near analogue located. Conjunction searched: Gospel apprehensum sanavit/dismissal, Epistle interior homo and strengthening, Secret cleansing/perfection, and Postcommunion mentes/corpora/praesens/futurum. PRE-003 corpus plus the two Antonian sermons and The Liturgical Year continuation’s chapter; terms heal/sanav-/san-/cure/medicin-, mind/interior/mentes, body/corp-. The target’s combination was not located as a developed prior proposal. Possible fruit: an inward act of grace can be considered alongside bodily care and bodily hope without competing with them. Separate commentary misses the change of time horizon and kind of assistance. It does not identify Eucharistic reception with an immediate medical cure, mortal healing with final resurrection, or bodily illness with sin. Re-entry on 2026-09-05: the unchanged corpus and all eight search families were replayed, the named nearest passages re-inspected, and the two Anthony pages and complete Liturgical Year volume freshly retrieved. PRE-005 now supplies complete Anthony citation metadata; PRE-006 supplies the corrected 1909 continuation identity. No novel universal-priority claim is made.

## Public-identity acquisition receipt register

These are the lanes' supplied retrieval receipts, not new synthesis
retrievals. Public URL, retrieved date, exact SHA-256, byte size, media type and
reported extent are preserved. Duplicate exact responses are joined by their
public identity and all contributing finding IDs are named. Local scratch
paths are intentionally absent from tracked content. Empty retrieval lists
mean that a lane reused the retained source named in its evidence, not that it
performed no check. Whole-source acquisition and the smaller actually
inspected extent remain distinct as each finding and receipt states.

### SCR-008 — 3b7cf9781633

- Public source: https://bible.usccb.org/bible/ephesians/3
- Retrieved: 2026-09-05
- SHA-256: `3b7cf97816332b06715660f5c0a5da0dbef832a131f3acb468e6c38b1ee60f7e`
- Byte size: 60628
- Media type as supplied: text/html
- Reported extent: Complete chapter page response: all 21 numbered verses, accompanying chapter notes and cross-reference apparatus. This is the entire public chapter view; it is not a retrieval of the complete NABRE Bible.

### SCR-009 — 77a39108cd0b

- Public source: https://bible.usccb.org/bible/luke/14
- Retrieved: 2026-09-05
- SHA-256: `77a39108cd0b4325ae69fa7803a38751358b2960a20d9ab8ec16e7cb45e7dbd8`
- Byte size: 64972
- Media type as supplied: text/html
- Reported extent: Complete chapter page response: all 35 numbered verses, accompanying chapter notes and cross-reference apparatus. This is the entire public chapter view; it is not a retrieval of the complete NABRE Bible.

### SCR-023, COV-010 — c9e065db65e7

- Public source: https://www.newadvent.org/cathen/03738a.htm
- Retrieved: 2026-09-05
- SHA-256: `c9e065db65e7fbf1d5ccd86f3f60dbb37816619b352417b3210c00b6749cbc48`
- Byte size: 44196
- Media type as supplied: text/html
- Reported extent: Complete single-page General Chronology article response: all ten named topical sections from Christian era through The century, plus bibliography and About this page attribution; no pagination or omitted article continuation indicated.
- Reported extent: Complete offered General Chronology article HTML, 182 physical lines, with article introduction, all ten indexed sections from Christian era through The century, tables, sources, and About this page citation/transcription apparatus; not the complete encyclopedia. The public page offers no free whole-encyclopedia download.

### PAT-008 — 9dad10c5c2dd

- Public source: https://www.corpusthomisticum.org/cep.html
- Retrieved: 2026-09-05
- SHA-256: `9dad10c5c2dde8cf5f74fbc4b8ecb62bb4808d6e98dd6510759ac7f6ef932e6e`
- Byte size: 351481
- Media type as supplied: text/html
- Reported extent: Complete served commentary on Ephesians, prologue and chapters 1–6; 257 physical lines.

### PAT-013 — 4cb627da2148

- Public source: https://www.corpusthomisticum.org/cps01.html
- Retrieved: 2026-09-05
- SHA-256: `4cb627da2148f050e1f250207761e6c5a12285152d7ef6bfdf716fa1a317d0f7`
- Byte size: 13423
- Media type as supplied: text/html
- Reported extent: Complete served cps01.html section; one of all nine linked files covering the prologue and Psalms 1–54, acquired together; no single whole-work download linked in the checked navigation; 91 physical lines.

### PAT-013 — e2d50b43f003

- Public source: https://www.corpusthomisticum.org/cps31.html
- Retrieved: 2026-09-05
- SHA-256: `e2d50b43f0036d33450b908632ba6d741277edb8ad9381c851eddeb005f90749`
- Byte size: 359759
- Media type as supplied: text/html
- Reported extent: Complete served cps31.html section; one of all nine linked files covering the prologue and Psalms 1–54, acquired together; no single whole-work download linked in the checked navigation; 375 physical lines.

### PAT-013 — da7e3e2a3d32

- Public source: https://www.corpusthomisticum.org/cps51.html
- Retrieved: 2026-09-05
- SHA-256: `da7e3e2a3d32344d3dd4e5f872df2be5f44cbf18de867b5a4bcf260ee2cbb2f6`
- Byte size: 19649
- Media type as supplied: text/html
- Reported extent: Complete served cps51.html section; one of all nine linked files covering the prologue and Psalms 1–54, acquired together; no single whole-work download linked in the checked navigation; 95 physical lines.

### PAT-013 — 5b8dc98e53ad

- Public source: https://www.corpusthomisticum.org/cps00.html
- Retrieved: 2026-09-05
- SHA-256: `5b8dc98e53ad81b451125e74e8d2d797df95a24c46ed36fc57deac1fb5085d75`
- Byte size: 19691
- Media type as supplied: text/html
- Reported extent: Complete served cps00.html section; one of all nine linked files covering the prologue and Psalms 1–54, acquired together; no single whole-work download linked in the checked navigation; 85 physical lines.

### PAT-013 — b281d5eb67a6

- Public source: https://www.corpusthomisticum.org/cps52.html
- Retrieved: 2026-09-05
- SHA-256: `b281d5eb67a619410ffc7547e8d29851f9a7d4f100e10289810c122902927dbd`
- Byte size: 54972
- Media type as supplied: text/html
- Reported extent: Complete served cps52.html section; one of all nine linked files covering the prologue and Psalms 1–54, acquired together; no single whole-work download linked in the checked navigation; 145 physical lines.

### PAT-013 — 73a0a0c27e74

- Public source: https://www.corpusthomisticum.org/cps02.html
- Retrieved: 2026-09-05
- SHA-256: `73a0a0c27e746ff867b725c53f9d26138a8c861e5178a3b674d0fdb311a1cfa4`
- Byte size: 217681
- Media type as supplied: text/html
- Reported extent: Complete served cps02.html section; one of all nine linked files covering the prologue and Psalms 1–54, acquired together; no single whole-work download linked in the checked navigation; 265 physical lines.

### PAT-013 — 27fad154f832

- Public source: https://www.corpusthomisticum.org/cps11.html
- Retrieved: 2026-09-05
- SHA-256: `27fad154f83226475da95ed754ab0adf8ee3ae19949ff8cfd38c31ca2f8f693e`
- Byte size: 254560
- Media type as supplied: text/html
- Reported extent: Complete served cps11.html section; one of all nine linked files covering the prologue and Psalms 1–54, acquired together; no single whole-work download linked in the checked navigation; 279 physical lines.

### PAT-013 — 5e8fdbbea9c1

- Public source: https://www.corpusthomisticum.org/cps21.html
- Retrieved: 2026-09-05
- SHA-256: `5e8fdbbea9c1baf3cec1163cb88cca8744bc1f9cbca6a65b605c9a0a7f1366ed`
- Byte size: 271127
- Media type as supplied: text/html
- Reported extent: Complete served cps21.html section; one of all nine linked files covering the prologue and Psalms 1–54, acquired together; no single whole-work download linked in the checked navigation; 339 physical lines.

### PAT-013 — 7879ef1346a1

- Public source: https://www.corpusthomisticum.org/cps41.html
- Retrieved: 2026-09-05
- SHA-256: `7879ef1346a1a21847de0adf00c1ec1b6237befb0b031980b8e4af66082ad9c7`
- Byte size: 286376
- Media type as supplied: text/html
- Reported extent: Complete served cps41.html section; one of all nine linked files covering the prologue and Psalms 1–54, acquired together; no single whole-work download linked in the checked navigation; 259 physical lines.

### PAT-014 — 72ee87148ebd

- Public source: https://upload.wikimedia.org/wikipedia/commons/f/fd/Patrologia_Graeca_Vol._080.pdf
- Retrieved: 2026-09-05
- SHA-256: `72ee87148ebda475ceea8b46b4325358dd20b07562ba0072b6fe06554eacbdd8`
- Byte size: 129500554
- Media type as supplied: application/pdf
- Reported extent: Complete PG 80 volume, 1068 PDF pages; target Psalms 39, 70, 85, 97, 101 occur within the complete hosted volume

### PAT-019 — 78b290d42073

- Public source: https://upload.wikimedia.org/wikipedia/commons/9/9d/Commentaryonbook0000bell.pdf
- Retrieved: 2026-09-05
- SHA-256: `78b290d420736cb04d1e744375caa0b97edf374dbdcc53076277a7bb20897f9a`
- Byte size: 56448883
- Media type as supplied: application/pdf
- Reported extent: Complete hosted O’Sullivan/Duffy 1866 volume, 482 PDF pages, including its preliminaries and terminal matter

### PAT-024 — 911b4374ff88

- Public source: https://www.augustinus.it/latino/lettere/lettera_141_testo.htm
- Retrieved: 2026-09-05
- SHA-256: `911b4374ff880fea5ccf5d87578fb795bc439f3b607096575df6cd9ebed76069`
- Byte size: 157069
- Media type as supplied: text/html
- Reported extent: Complete served Epistula 140 / De gratia Novi Testamenti, numbered §§1–85 and source notes; 201 physical lines.

### PAT-025 — 95070a43427c

- Public source: https://www.vatican.va/content/benedict-xvi/en/angelus/2010/documents/hf_ben-xvi_ang_20100829.html
- Retrieved: 2026-09-05
- SHA-256: `95070a43427c8dfb722dc15039be6c1684b424b7350b86eb1378032d4cce0f62`
- Byte size: 38226
- Media type as supplied: text/html
- Reported extent: Complete served official Angelus address of 29 August 2010, including greetings and terminal copyright notice; 890 physical lines.

### PAT-026 — f1f17ccf7d9a

- Public source: https://www.vatican.va/content/benedict-xvi/en/audiences/2009/documents/hf_ben-xvi_aud_20090114.html
- Retrieved: 2026-09-05
- SHA-256: `f1f17ccf7d9a564b8375d2c455f8c9834e84c74d6c6e13048c3acf89b846fcef`
- Byte size: 48985
- Media type as supplied: text/html
- Reported extent: Complete served official General Audience of 14 January 2009, including greetings and terminal copyright notice; 907 physical lines.

### PAT-027, COV-011, PRE-005 — 7596e867d949

- Public source: https://www.santantonio.org/en/node/869?latin=1
- Retrieved: 2026-09-05
- SHA-256: `7596e867d949f05848904037cd7266f549593cb95e8433b2824afe663d3c3135`
- Byte size: 90849
- Media type as supplied: text/html; text/html; charset=utf-8
- Reported extent: Complete served Dominica XVI sermon page: outline and numbered §§1–12 in four text panels, ending with the final Amen/Alleluia; not the whole sermon collection; no complete collection download linked in this page; 844 physical lines.
- Reported extent: Complete offered Dominica XVI Latin sermon page: thematic outline and all numbered sections 1–12 in 4 panels, 844 physical HTML lines, followed by site footer. All sermon panels are in the response; the page offers no PDF or whole-collection download link. This is one complete sermon, not the entire Sermones dominicales collection.
- Reported extent: Complete retrieved Latin sermon page, outline and sections 1–12 in four panels, not the complete sermon collection; 90849 bytes; 844 physical lines.

### PAT-028, COV-012, PRE-005 — deb89addec18

- Public source: https://www.santantonio.org/en/sermons/sermoni-domenicali/domenica-xvii-dopo-pentecoste?latin=1
- Retrieved: 2026-09-05
- SHA-256: `deb89addec1842e9ea85a4a09f00a6bf5aa0effbc84e168e4aacf7bd30623738`
- Byte size: 98178
- Media type as supplied: text/html; text/html; charset=utf-8
- Reported extent: Complete served Dominica XVII sermon page: outline and numbered §§1–16 in five text panels, ending with final Amen/Alleluia; not the whole sermon collection; no complete collection download linked in this page; 873 physical lines.
- Reported extent: Complete offered Dominica XVII Latin sermon page: thematic outline and all numbered sections 1–16 in 5 panels, 873 physical HTML lines, followed by site footer. All sermon panels are in the response; the page offers no PDF or whole-collection download link. This is one complete sermon, not the entire Sermones dominicales collection.
- Reported extent: Complete retrieved Latin sermon page, outline and sections 1–16 in five panels, not the complete sermon collection; 98178 bytes; 873 physical lines.

### LIT-001 — 404f7df5d060

- Public source: https://archive.org/download/gelasiansacrame00wilsgoog/gelasiansacrame00wilsgoog.pdf
- Retrieved: 2026-09-05
- SHA-256: `404f7df5d06059676cacccaca05f997ca59407d0bff74b6a867c509eeefac72b`
- Byte size: 14980268
- Media type as supplied: application/pdf
- Reported extent: Complete 497-page scanned volume, with title, introduction, edited text, appendices and indexes; p. 231 is PDF p. 324.

### LIT-001 — 039123ca029b

- Public source: https://archive.org/download/gelasiansacrame00wilsgoog/gelasiansacrame00wilsgoog_djvu.txt
- Retrieved: 2026-09-05
- SHA-256: `039123ca029bf1684b2e8b0dec014cc3fa9057ecb30da3494f7165cb89684d84`
- Byte size: 1098845
- Media type as supplied: text/plain
- Reported extent: Complete Internet Archive DjVuTXT derivative of the 497-page volume: 1098845 bytes and 37086 LF-delimited lines; includes front matter, edition, appendices and index. OCR is a locating aid only.

### LIT-005 — 410f6d115543

- Public source: https://archive.org/download/LiberSacramentorum/The%20Sacramentary%20%28Liber%20Sacramentorum%29%3A%20Historical%20%26%20Liturgical%20Notes%20on%20the%20Roman%20Missal%20%28vol.%203%29.pdf
- Retrieved: 2026-09-05
- SHA-256: `410f6d1155436714f76a4ca3645edcd33ca6ef65bed3d37b1d3e6f10b0c37239`
- Byte size: 158333284
- Media type as supplied: application/pdf
- Reported extent: Complete 462-page scanned volume III; the item offers five volumes separately and this file contains all of volume III. Printed pp. 142–145 are PDF pp. 158–161; pp. 183 and 186 are PDF pp. 199 and 202.

### LIT-007, COV-014, PRE-006 — 95ba98e2d71e

- Public source: https://archive.org/download/V11TheLiturgicalYear/V11TheLiturgicalYear.pdf
- Retrieved: 2026-09-05
- SHA-256: `95ba98e2d71e4374c4e5262935c71d5d2479b64b34dd3da290b60209ebd92690`
- Byte size: 11026232
- Media type as supplied: application/pdf
- Reported extent: Complete 539-page scanned volume, including title, preface, contents, all chapters and index; Sixteenth Sunday occupies printed pp. 356–372 (PDF pp. 377–393).
- Reported extent: Complete offered Time after Pentecost II (complete-series XI) facsimile, 539 PDF pages, matching pdfinfo page count and the already registered exact artifact; title, preface, contents, full volume, and terminal matter included. Bibliographic inspection in this lane was confined to title leaf PDF p.4 and preface printed pp. iii–iv/PDF pp.6–7; the book’s substantive commentary was not reinspected.
- Reported extent: Complete offered 539-page PDF volume, including title page, front matter, main text, contents and index; 11026232 bytes. Research inspected the Sixteenth-Sunday chapter at printed pp. 356–372 (PDF pp. 377–393) and the stated front matter, not the whole volume.

### CUL-001 — 4edceb55d15b

- Public source: https://folger-main-site-assets.s3.amazonaws.com/uploads/2022/11/shakespeares-sonnets_TXT_FolgerShakespeare.txt
- Retrieved: 2026-09-05
- SHA-256: `4edceb55d15b87236a5e46069a1edf813864def60497b9fbd6afb0a6a47cdb6e`
- Byte size: 99272
- Media type as supplied: text/plain
- Reported extent: Complete Folger text download: edition header and all 154 sonnets; Sonnet 57 at physical lines 964–979. Header gives FDT 0.9.0.1, created 2015-07-31.

### CUL-002 — 2b4a17384730

- Public source: https://folger-main-site-assets.s3.amazonaws.com/uploads/2022/11/loves-labors-lost_TXT_FolgerShakespeare.txt
- Retrieved: 2026-09-05
- SHA-256: `2b4a1738473009e9cd4b2b06bdad2171c222268441f420a8a8065ec91ba7fa6c`
- Byte size: 132828
- Media type as supplied: text/plain
- Reported extent: Complete Folger play download: edition header, cast, all five acts, and closing stage direction; relevant proposal and year-long trial at physical lines 4486–4534. Header gives FDT 0.9.2, created 2015-07-31.

### CUL-002 — 2773d2f61f3f

- Public source: https://www.folger.edu/explore/shakespeares-works/loves-labors-lost/read/
- Retrieved: 2026-09-05
- SHA-256: `2773d2f61f3f6b04daa6b5a764b99d9fc39c0e0b7b80bc485792911f8fb00c9f`
- Byte size: 995762
- Media type as supplied: text/html
- Reported extent: Complete Entire Play HTML response, all five acts with Folger scene line and FTLN anchors; checked 5.2.865–866 = FTLN 2762–2763, plus the surrounding proposal and year-long trial.

### CUL-006 — 8767548d28a5

- Public source: https://www.amazingfacts.org/wp-content/uploads/2025/06/BK-HKSH.pdf
- Retrieved: 2026-09-05
- SHA-256: `8767548d28a5d72078a966175f1dcb94f03b884cfb02baebfaba5a3b94489c8c`
- Byte size: 3564983
- Media type as supplied: application/pdf
- Reported extent: Complete publisher download, 95 PDF pages, cover spread and front matter through printed p. 96; The Ox in the Ditch starts at printed p. 78 = PDF page 77, visually inspected. ISBN 978-1-58019-618-5; copyright 2014 Amazing Facts.

### CUL-007 — a5793a447ef0

- Public source: https://www.esquire.com/news-politics/news/a8668/bob-corker-interview-1110/
- Retrieved: 2026-09-05
- SHA-256: `a5793a447ef0ad1967d4b47d7c15e1113eb3f89419189539f238a7df80437812`
- Byte size: 646988
- Media type as supplied: text/html
- Reported extent: Complete interview article HTML, with headline, Cal Fussman byline, 2010-10-18 07:24 EDT publication stamp, and all paragraphs from My dad just imprinted through the concluding telephone interruption; also host navigation, advertising and related-story material. Entire interview inspected.

### CUL-010 — c185dad17113

- Public source: https://digitalcommons.liberty.edu/masters/370/
- Retrieved: 2026-09-05
- SHA-256: `c185dad171133623a6ab213fb4dd1c7ee4b4846ddfbdfafde9e5f7fec13b63d5`
- Byte size: 40840
- Media type as supplied: text/html
- Reported extent: Complete repository landing-page HTML response for Masters Theses 370: title, author, June 2015 date, degree, chair, recommended citation and complete abstract. The linked full thesis download returned HTTP 403; no thesis pages are contained in this response.

### PRE-005 — c1d583bfd588

- Public source: https://www.santantonio.org/en/sermons/sermoni-domenicali/domenica-xvi-dopo-pentecoste?latin=1
- Retrieved: 2026-09-05
- SHA-256: `c1d583bfd5880209324285bef9fdeb54aba5e3a27e93527af3709a626fff8499`
- Byte size: 62860
- Media type as supplied: text/html
- Reported extent: Complete returned sermon-index page from a plausible but non-sermon route; no XVI sermon is supplied; 62860 bytes; 866 physical lines.

## Completion audit

The full 116-finding fresh join was read and integrated in canonical lane
order. All seven appointed Scriptures and all three composed prayers have
substantive evidence positions. Five cross-proper claims, six searched
proposals, and five qualifying cultural afterlives are settled. Every selected
gallery citation bundle was compared to its lane entry and is present in
full; each proposal retains its actual precedent classification and search
boundary. All fourteen chronology assertions retain their exact labels,
subjects, relations, profiles, dispositions, answerability, source IDs and
locus reaches; `research/chronology.toml` was not edited. All six standing
evaluation findings are carried forward, with the two research evidence
defects answered and the four authoring repairs still outstanding. No
registration prerequisite, new source, new date, original-research result,
or completed publication review is asserted by this PASS.
