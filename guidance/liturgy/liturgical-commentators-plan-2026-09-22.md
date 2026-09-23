# Liturgical commentators: standing, keying and inclusion — plan of 2026-09-22

This is a maintainer record. It holds the decisions the maintainer made on
2026-09-22 and, below them, the design proposal those decisions were made on.
The rules it leads to will live in their owning guidance and workflow files
once they land; until then this record is the warrant for them, and
[`PROJECT-WORK.md`](../../PROJECT-WORK.md) (deliverable
`liturgical-commentators-2026-09-22`) tracks what has and has not been done.

## Maintainer decisions, 2026-09-22

The question: how Triptych should source, store and include appropriately
authoritative liturgical commentators in its proper studies, with Prosper
Guéranger's *The Liturgical Year* as the example. It arose in the Claude 1962
Eighteenth Sunday after Pentecost production, when the research record denied
that any witness read that Sunday's Gospel as the priests' power to forgive
sins, and a cold review found two registered commentators who do. The
decisions refer to §6 of the proposal below.

| Decision | Chosen | Consequence |
| --- | --- | --- |
| D1. Does "saints" include the Blessed? | **B.** Fathers, canonized saints and the Blessed may count toward a reading's two authors, provided at least one of the two is a Father or canonized saint. | Schuster may be one of a reading's two authors. Guéranger, his continuator, Rupert, Durandus, Honorius and Sicard may not. They remain witnesses to the Mass as a compilation, and may be a reading's principal witness for its claim about the Mass as a Mass. |
| D2. May a commentator with no cultus count as a reading's second author? | **Never.** | The two-author rule keeps its purpose. |
| D3. Censured and non-Catholic authors (Amalarius, Blunt) | **Structure and context only.** Record the censure; never cite Amalarius on the censured point. | — |
| D4. Where Mass-keyed commentary loci live | **One file, `src/sources/commentary/formulary-loci.yaml`**, with a `genre` field, matched on a formulary's elements and keeping each commentator's own Sunday label as data. | Sunday-label drift cannot misfile a commentator. |
| D5. Author-standing registry and check | **Registry plus an opt-in check**, made mandatory at the next `proper-study` version. | Closes the gap where the component checker counts any two author names. |
| D6. Timing relative to the live Eighteenth Sunday run | **Rule changes land after that run publishes.** Inventories, tools and acquisitions may land now. | That Sunday is produced under the rule as it stood when the run was seeded. `guidance/liturgy/propers-three-documents.md` is sealed into that run's research, so changing it between research acceptance and publication would return the run to research. |
| D7. The *Liturgical Year* continuation | **Credit it to Dom Lucien Fromage**, recorded as data in the Mass-keyed locus file. Put the published leaves that attribute it to Guéranger on the staleness list for their next revision. | Published leaves are not rewritten now. |
| D8. Acquisitions | **First-priority items now; second-priority items as studies need them.** | Free public downloads only, as `guidance/sources.md` requires. |
| D9. Google usage-guidelines pages in retained scans | **Settle once in a rights record under `src/sources/inventories/`**; prefer non-Google scans meanwhile. | — |
| D10. Two artifact records for one text layer | **Leave both, document the duplication, merge at the next deliberate schema change.** | No fingerprint moves now. |

**Amendment to D6, 2026-09-22.** Research-review iteration 3 of the
Eighteenth Sunday run found Bl. Ildefonso Schuster, commenting on the 1962
Mass itself, reading that Sunday's Gospel of power communicated to the
apostles and their successors in the priesthood. Research iteration 3 had
already found Aquinas reading Mt 9:6 of a ministry exercised by way of
administration. Under D1 the two may carry that reading as its own
interpretation. The reason for deferring the rule was that it would change the
Sunday only if research went round again, and research was going round again.
The maintainer therefore moved step 5 into the hold before research iteration
4. The rule now stands as the "Liturgical commentators" subsection of
[the three-document profile](propers-three-documents.md#liturgical-commentators).
Step 7, the workflow change, still waits for that run to publish.

**D11, 2026-09-22: commentators whose Mass had another Gospel.** The
maintainer decided that such a commentator is cited in a reader-facing
document only for what he says of an element this formulary shares, and never
in support of a connection to this formulary's Gospel. The Gospel difference
stays in the research records, where it guards against false claims about the
formulary's history, and in at most one clause of the scope appendix. The
readings, the concise study and the homily never mention it. Reason: a reader
of a 1962 guide is not served by other Masses. Citing a commentator on a
shared chant beside this Gospel implies a link he never made, and a disclosure
sentence repairs that only by adding the other Mass. It was first set to land after the Eighteenth Sunday run published, because
that run's accepted research sealed the three-document profile. Study-review
iteration 0 then returned the run to research (STU-001), so every downstream
document and review would rerun anyway. D11 therefore landed in the hold
before research iteration 5, and the Eighteenth Sunday study is re-authored
under it. The maintainer had said that other Masses do not belong in a 1962
guide. The rule applies to a differing chant as to a differing Gospel, for the
same reason.

**D12, 2026-09-23: lectionary history.** The maintainer extended D11's
principle to the history of a formulary's texts in early lectionary and
sacramentary lists. The history of this formulary's own texts may appear in
the expansive study, where it can replace an unsupported claim about a
pairing's age. It never appears in the concise study or the homily, and what
another Sunday's Mass contained stays in the research records. The rule lands
in the three-document profile after the Claude 1962 Eighteenth Sunday run
publishes, because that run's accepted reviews seal the current profile. That
Sunday's accepted study already keeps such history to one paragraph of its
element-by-element section and is not revised for D12.

**Standing settlements, 2026-09-23.** Decided on the evidence of the
Eighteenth Sunday run. Recorded so a later session does not re-derive them.

- **Theodoret of Cyrus and Cassiodorus stay ecclesiastical writers, not
  Fathers.** No source read calls them Fathers. The Catholic Encyclopedia calls
  Theodoret an "ecclesiastical writer", and Constantinople II (553) condemned
  his writings against Cyril. Neither may be one of an interpretation's two
  authors; both remain usable as supporting witnesses. Every published lane
  already has two Fathers or saints without them.
- **Rabanus Maurus is a saint.** The current Martyrologium Romanum (2004, p.
  133) gives his feast on 4 February and calls him *sanctus*. The maintainer
  supplied this on 2026-09-23 through the English Wikipedia's report of that
  entry, after the 1902 and 1914 recensions, which omit him, had been read.
  He may be one of an interpretation's two authors and may anchor a Blessed
  under D1.
- **Theophylact of Ohrid is an ecclesiastical writer, not a writer outside
  Catholic communion under D3.** His Western reception is long (the *Catena
  aurea* names him over a thousand times on Mark, Luke and John, though never
  in its Matthew volume), and his Pauline commentary is not
  schismatic polemic. His row records his post-1054 Byzantine see. He may
  support what his checked locus says and is never one of a reading's two
  authors. The Catholic Encyclopedia's "Exegesis, Biblical" article lists him among
  "adherents of the Greek Schism"; his registry row records that sentence as
  contrary evidence beside the settled standing. The maintainer reaffirmed the
  settlement on 2026-09-23 with that sentence and the corrected Catena count
  before him; they are not new evidence for reopening it.

**Erratum to the proposal.** §0, §1.3 and D7 count seven published leaves that
credit the continuation to Guéranger with a corrected imprint. A search of the
published leaves for that imprint finds more than seven, and the set it names
differs. Recount the affected leaves from the tracked files before marking any
of them stale; do not take the proposal's list as the set.

**Correction to §5.2(e) and step 7, 2026-09-23.** The mandatory authority
check does not go on `research-preflight`. `proper-components.toml` is first
written by `author-study`, after that gate, so `--require-authority` starts at
`study-preflight` and every later content, artifact and publication gate
repeats it. `workflows/OPERATOR.md`, under `proper-study` version 7, records
the reasoning.

---

## The proposal as reviewed

**Evidence tags.** **[F]** is a fact, with the repository path and line or the
URL it was read from. **[I]** is an inference. **[U]** means uncertain or not
verified in this lane. "Read" means read in the bytes this lane fetched or in a
tracked file. It does not mean collated against a page image unless the text
says so.

**One correction to the brief.** The sentence admitting "a named liturgical
commentator [who] expounds the Mass of the day as his books gave it" is in
`guidance/liturgy/propers-three-documents.md:115-118`, not in the workflow
contract. The contract carries only the two-author rule (§1.1).

---

### 0. Summary

| Section | Top recommendation |
| --- | --- |
| 1 Current state | Most of the question is already answered. The profile treats a liturgical commentator as a separate witness: evidence of how he received the compilation. Four gaps remain. "Saint" is defined nowhere. Nothing mechanical checks an author's standing. Nothing can find these works from a Mass. The *Liturgical Year* continuation is misattributed in seven published leaves. |
| 2 Authority classes | Classify authors on two axes: **standing** (who the author is) and **keying** (what his text is about). Only Fathers and canonized saints or Doctors count toward the two-author minimum. On balance, the Blessed may also fill the *second* place (decision D1). Every other orthodox commentator may be the principal witness for the Mass as a compilation and may support a reading, but never counts as one of its two authors. |
| 3 Sourcing | First priority: the French *L'Année liturgique* (a University of Toronto scan, no Google page); non-Google text layers of the 1883 English Time-after-Pentecost volumes; and Patrologia Latina 172, which holds the whole *Gemma animae*. Second priority: the rest of Schuster in English, Haymo's *Homiliae de tempore*, Smaragdus, and Alphonsus's *Sermons for all the Sundays*. All are free public downloads. `sources.md` forbids purchases. |
| 4 Storage and keying | A new file, `src/sources/commentary/formulary-loci.yaml`, for Mass-keyed loci. Each row records the Mass **as the commentator gives it**, element by element, with his own Sunday heading kept as data. A tool compares those elements with any calendar's mass and stores no match results. Also a new `author-standing-v1.toml`. Holdings come from the parallel lane's containment inventory. No existing record is edited. |
| 5 Inclusion | One new guidance subsection, "Liturgical commentators", in `propers-three-documents.md`. One reviewer sentence and an opt-in checker contract arrive with the next `proper-study` version. |
| 6 Decisions | Ten decisions for the maintainer, listed in §6. |
| 7 Plan | Nine steps. Inventories, the tool and acquisitions can land at any time. Guidance edits take effect immediately. Workflow edits reach only runs seeded afterwards. Do not edit `workflows/` while the Eighteenth-Sunday run is live. |

---

### 1. Current state

#### 1.1 The rules as written

| Rule | Exact text | Where |
| --- | --- | --- |
| Two authors per reading (workflow) | "Group compatible checked arguments from at least two distinct Fathers or saints within each reading. Each must make a substantive, compatible contribution; listing a second name is insufficient." | [F] `workflows/fragments/proper-study/contract.md:37-40` |
| Same rule, restated three more times | "substantive contributions from at least two distinct Fathers or saints" | [F] `research-review.md:20-21`; `study-review.md:10-11`; `author-study.md:8` ("multiple checked Fathers or saints") |
| Two authors per reading (guidance) | "Each interpretation draws substantively on at least two distinct patristic or saintly authors. A second name without a developed contribution does not meet this requirement." | [F] `guidance/liturgy/propers-three-documents.md:157-159` |
| The liturgical commentator | "Where a named liturgical commentator expounds the Mass of the day as his books gave it, that is a distinct witness: documented reception of the compilation as he received it, which may differ from the governing edition's assignment." | [F] same file, `:115-118` |
| A commentator with another Gospel | Record compilation history only where it changes a claim, for example "a commentator whose Mass had another Gospel or chant". | [F] same file, `:120-125` |
| Reception classes (1962 profile) | "3. **Documented reception:** explicitly taught by an identified and checked patristic, saintly, doctrinal, or liturgical witness." | [F] `guidance/liturgy/roman-1962-propers.md:248` |
| Reception sweep (1962 profile) | "…then medieval Doctors and later **canonized** exegetes or spiritual writers." | [F] same file, `:156` |
| What the checker enforces | Counts at least two distinct `authors` strings per lane, case-folded. It knows nothing of standing. | [F] `scripts/_proper_components.py:751-753` |
| Harvest role vocabulary | `church-father`, `saint`, `saintly`, `pope`, `doctor`, `ecclesiastical-writer`. `saintly` is admitted to be a coarse tag. | [F] `src/sources/commentary/README.md` ("`role` is one of…") |

**What this settles and what it leaves open.** [I]

- The rule already settles the main point. A liturgical commentator is a
  separate witness, to the Mass as a compilation, and does not stand in for
  exegesis. Nothing needs to be invented.
- "Saint" is left undefined. The 1962 profile says *canonized* for the
  reception sweep. The workflow says *saints* and the guidance says *saintly*.
  The harvest applies `saintly` to Cornelius a Lapide and to Rupert, and tags
  Rupert both `saintly` and `ecclesiastical-writer` on different rows (§1.4).
  The Blessed are not addressed anywhere. Under `00-core.md` this is a defect in
  the guidance set. The safer reading ("canonized") governs until the maintainer
  decides.
- Standing is not checked mechanically. A lane whose authors are "Rupert of
  Deutz" and "William Durandus" would pass the checker. Only a reviewer's
  reading of the rule stands in the way.
- The same rule is restated in five places: four workflow fragments and one
  guidance file. Any change must reach all five, or `the-shape.md` §2 will
  apply.

#### 1.2 The eleven held liturgical commentaries

These are the 11 works with `work_type = "liturgical-commentary"` [F]
(`rg 'work_type = "liturgical-commentary"' src/sources/works`). Sizes are the
recorded `byte_size`. "Tracked" means the bytes are in Git.

| # | Work (id suffix) | Author, dates, standing, confession | Editions and artifacts held | Year coverage; Sunday by Sunday? | Locus for 1962 #58 (Eighteenth Sunday) |
| --- | --- | --- | --- | --- | --- |
| 1 | `prosper-gueranger.the-liturgical-year` | **Guéranger**, 1805–1875 [F: BnF catalogue records, §8]. Abbot of Solesmes. **Servant of God**: the diocesan process was opened at Le Mans on 21 Dec 2005 and remains in its diocesan phase [F: domgueranger.net pages, §8]. **The Time-after-Pentecost volumes are a posthumous continuation**, identified as the work of **Dom Lucien Fromage OSB, 1845–1916** (§3.2). Catholic. | English *Time after Pentecost* II (series vol. XI), 2nd ed. 1909. The PDF facsimile is tracked (11,026,232 B). There are two remote records of the same Internet Archive OCR bytes (sha256 `f4c31a52…`) and one checked transcription with its passage (p. 271). English vols X, XIII, XIV and XV are registered as remote, only to support negative findings. **No French is held.** [F: `…/the-liturgical-year/editions/*`] | The whole year in 15 volumes; the library holds only the Time after Pentecost. Sunday by Sunday: **yes**. Vol. XI runs from the 4th to the 24th Sunday [F: `pdftotext` of the tracked PDF, contents at text lines 198–685]. | 1909 vol. XI, printed p. 393 [F: contents line 499]. In the 1883 first edition it is vol. II p. 407 [F: §3.2]. |
| 2 | `ildefonso-schuster.the-sacramentary` | **Schuster**, 1880–1954. Abbot of St Paul's Outside the Walls, then Cardinal Archbishop of Milan. **Blessed**, beatified 12 May 1996 [F: USCCB beatification list, §8]. Catholic. | English, Burns Oates & Washbourne, vol. III only. The PDF is remote (158,333,284 B). The OCR is tracked (1,149,699 B). Two verified passages. [F] | **Vol. III covers the 1st to the 24th Sundays after Pentecost** [F: tracked OCR, contents lines 123–216]. Sunday by Sunday: **yes**. He follows the modern Missal and adds the old Roman names ("post natale S. Cypriani"). | **Vol. III pp. 167–170**, "Eighteenth Sunday after Pentecost: Tertia post natale Sancti Cypriani" [F: tracked OCR lines 10478–10600]. The Introit *Da pacem*, the Collect, 1 Cor 1:4–8, Ps 121, Ps 101 and Mt 9:1–8 all match 1962. |
| 3 | `rupert-of-deutz.de-divinis-officiis` | **Rupert**, abbot of Deutz (Benedictine). Dates [U]. No canonization or beatification was located [U]. No censure was located [U]. | PL 170 (Garnier reissue). The whole-volume OCR is tracked (4,217,071 B), plus two remote page images. [F] | The whole year. Book XII takes the Sundays after Pentecost chapter by chapter [F: OCR headings at 22693–23838]. | **XII.18**, "Dominica decima octava post Pentecosten". The chants and Epistle are 1962's but **the Gospel is Mt 23 (the chair of Moses)**. Mt 9 appears at **XII.19**, alongside the chants of 1962's Nineteenth Sunday [F: tracked OCR lines 23443–23534]. |
| 4 | `william-durandus.rationale-divinorum-officiorum` | **Durandus**, c. 1237–1296, Bishop of Mende. He wrote the *Rationale* in 1286 [F: Catholic Encyclopedia 05207a]. No cultus. | The 1568 Lyon composite with Beleth appended: OCR tracked (3,571,981 B). The 1612 Lyon tomus II: OCR tracked (1,901,920 B) plus three remote page images. [F] | The whole year. Book VI takes the Sundays; Ember-day chapters come in between. | **VI.135**, "De dominica decimaoctava post Pentecosten". Introit *Da pacem*, 1 Cor 1. **The Gospel is "in quibusdam Ecclesiis" Mt 23, or elsewhere Mt 22 (*Accesserunt*)**. The Alleluia is *Laudate Dominum omnes gentes*. Mt 9 appears "in quibusdam Ecclesiis" at **VI.136** [F: 1612 OCR ≈ lines 17100–17140]. |
| 5 | `honorius-augustodunensis.gemma-animae` | **Honorius**, flourished 1106–1135, *scholasticus*, "most mysterious" [F: Catholic Encyclopedia 07461a]. No cultus. | PL 172 (1854). A checked transcription of IV.65–68 is tracked (2,363 B) with two passages. The facsimile PDF (10,347,580 B) is **restricted**, because the host reserves rights. [F] | Book IV takes the temporal Sundays in "sub lege / sub gratia" pairs. | **IV.84–85**, "Dominica decima octava. Da pacem". The Introit, Oration, Epistle, Gradual, Offertory and Communion are 1962's. **The Gospel is the two great commandments (Mt 22)**. The Alleluia differs; the OCR is damaged there. Mt 9 appears at **IV.86**, "Dominica decima nona" [F: IA `patrologiaecursu0172mign` OCR lines 56955–57060]. **This locus is not held**; see P1-c. |
| 6 | `sicard-of-cremona.mitrale` | **Sicard**, Bishop of Cremona, d. 1215 [F: Catholic Encyclopedia 13770b]. No cultus. | PL 213. OCR tracked (3,018,404 B), plus two remote page images. [F] | The Sundays after Pentecost, chapter by chapter. | "Dominica decima octava post Pentecosten": Introit *Da pacem*, 1 Cor 1, **Gospel Mt 22 (two precepts), "secundum alios" Mt 23**. Mt 9 appears at the **Nineteenth** [F: tracked OCR line 29686ff]. |
| 7 | `amalarius-of-metz.liber-de-ordine-antiphonarii` | **Amalarius**, d. about 850. Bishop of Trier about 811, later administrator of Lyon. **Censured at the synod of Kiersy (Quierzy), 838**, "for his opinion concerning the signification of the parts of the divided Host at Mass" [F: Catholic Encyclopedia 01376b]. | PL 105 (Claremont scan). The OCR is tracked (4,071,455 B), plus one remote page image. A second, different OCR of PL 105 (PIMS scan, 4,636,959 B) is tracked under the container work `jacques-paul-migne.patrologia-latina-volume-105`, which also carries his *Liber officialis* [F]. | The office and the antiphoner (the September *historiae*). Per the Catholic Encyclopedia, the *Liber officialis* covers the seasons from Septuagesima to Pentecost, the Mass and the office [F]. **It does not go Sunday by Sunday through the Time after Pentecost** [I]. | None. It is a **structural** witness. |
| 8 | `john-beleth.summa-de-ecclesiasticis-officiis` | **Beleth**, twelfth century. Dates and standing [U]. No cultus located. | PL 202. OCR tracked (4,583,014 B), plus one remote page image. [F] | The course of readings, e.g. "Quid legi debeat ab octava Pentecostes usque ad Natale" [F: OCR line 4470]. A literal search found no Sunday-by-Sunday headings for the Time after Pentecost. | None. Structural. |
| 9 | `bernold-of-constance.micrologus-…` | **Bernold**, about 1054–1100. Priest, monk and chronicler. The *Micrologus* attribution is Dom Morin's [F: Catholic Encyclopedia 02512c]. No cultus located [U]. | PL 151. OCR tracked (4,656,302 B), plus three remote page images. [F] | The Mass and observances. Chapters XXVIII–XXIX cover the Ember fasts and the vacant Sundays. | None. Structural. |
| 10 | `berno-of-reichenau.libellus-…` | **Berno**, Abbot of Reichenau from 1008, d. 7 June 1048 [F: Catholic Encyclopedia 02512a]. No cultus located. | PL 142. OCR tracked (4,060,701 B). No page images. [F] | Chapter VI discusses the number of Sundays after Pentecost. | None. Structural. |
| 11 | `john-henry-blunt.the-annotated-book-of-common-prayer` | **Blunt**. Composed in 1866 [F: `work.toml` `composed`]. **Anglican**: the work is an apparatus to the Church of England's Prayer Book [F: `work.toml` description]. His orders and life dates were not verified [U]. | London 1866. OCR tracked (1,540,687 B). [F] | Sunday by Sunday **after Trinity**, with tables comparing the epistles and gospels of Sarum, Rome and the East [F]. | The comparable Sunday is labelled "after Trinity". Its offset from Rome's numbering was not verified [U]. |

**Adjacent holdings.** These are keyed to the Sunday but typed differently.
Anthony of Padua, **canonized in 1232** [F: Catholic Encyclopedia 01556a], is
held as five records of his *Sermones dominicales*. They are typed
`medieval-sermon` or `sermon-collection`. One work description already notes
that "Anthony's Sunday ordinal XV is not the 1962 Missal's Fifteenth" [F:
`anthony-of-padua/sermo-dominica-xv-post-pentecosten/work.toml`]. Gregory the
Great's *Homiliae in Evangelia* are station-Mass homilies [F: held]. Gihr
treats the Ordinary and Fortescue is history [F: held].

**Defects found in existing records.** These are reported, not fixed; the
records are fingerprinted.

- **The same bytes have two artifact identities.** Vol. XI's OCR (sha256
  `f4c31a52…`) is registered as both `ia-djvu-ocr-f4c31a52` and
  `ia-djvu-ocr-v11theliturgicalyear`. Claude 55 binds one and Claude 56 binds
  the other [F].
- **The records contradict themselves on date.** The OCR `rights_basis` texts
  say vol. XI "was published in 1900". The edition record corrects this to 1909
  [F].
- **Google's prose is handled inconsistently.** The tracked vol. XI PDF carries
  Google's "usage guidelines" front matter; `pdftotext` shows it at the head of
  the file [F]. The OCR of the same scan was ruled not retainable for exactly
  that front matter [F: artifact `rights_basis`]. The two dispositions
  contradict each other (decision D9).
- **PL 105 is tracked twice.** Two whole-volume OCRs from different scans sit
  under two owners [F]. The containment lane owns this problem.

#### 1.3 How published leaves use these works

**Bindings.** Extracted from every `src/*/liturgy/**/research/source-bindings.toml`
[F]. C is a Claude leaf, G a GPT leaf, and the number is the proper ID.

| Work | Leaves and binding role |
| --- | --- |
| *Liturgical Year* vol. XI | C53 reception (verified); **C55 direct-witness**; C56 context (×2); C57 reception; G50 reception (verified passage p. 271); G53, G55, G56 reception |
| Schuster vol. III | C53 reception; **C55 direct-witness**; C56 context; C57 reception; Claude pc-s51 context; G50, G52, G53, G54, G55, G56 reception |
| Rupert | C54, C57 reception |
| Durandus | C54, C57 reception |
| Honorius | **C55 direct-witness**; G51 reception (two verified passages) |
| Sicard, Berno, Bernold, Amalarius | C54 reception |
| Blunt | C56 context |
| Beleth | no bindings |

**Findings.** [F, except where marked]

1. **Three different roles are used for one kind of evidence.** `reception`,
   `direct-witness` and `context` are all applied to the same class of witness.
   `direct-witness` (C55) is the wrong role for a witness to the compilation
   [I].
2. **Claude 57 lists Rupert and Durandus as lane authors.**
   `proper-components.toml` includes them in the lanes `son-and-lord-of-david`
   and `just-judge-merciful-hearer`, beside Fathers. Its
   `research/interpretations.md` already models the practice this proposal would
   codify:

   > "Rupert of Deutz and Durandus did read a whole office of this Sunday, but
   > with a different Gospel (Luke 14); their readings are used only for the
   > elements they share with the 1962 book." (`:35-37`)

   > "The reading may use them for the chants and must not present them as
   > readers of Mt 22 on this Sunday." (`:628-629`)

   It also concedes: "The reading's anagogical sense rests on the liturgical
   commentators for the Introit and must say so" (`:634-636`). A commentator is
   therefore already doing more than supporting in one lane's anagogical sense.
3. **The continuation is misattributed, with the wrong imprint.** At least
   seven published leaves cite vol. XI as *Guéranger's*, with "(Dublin: Duffy,
   1900)". They are C53, C54, C56 and C57, and G49, G50 and G53 [F: `rg "Duffy,
   1900|James Duffy, 1900"`]. C57 opens "Prosper Guéranger records that…"
   [F: `57-…/sections/00-opening.tex:44`]. The library's own edition record
   says the volume is an unsigned continuation printed in 1909. GPT 56 already
   uses the corrected form: "continuation under Guéranger's series name… 1909"
   [F].
4. **Prose mentions.** A case-insensitive search puts Guéranger in about 20
   leaves, Schuster 15, Rupert 7, Durandus 10 and Honorius 4. This is
   approximate: the search matches names only and may include false positives
   [I].

#### 1.4 How discoverable these works are today

- **From a passage: not at all.** The discovery index is keyed by chapter and
  harvested by a model. It contains **no** liturgical-commentary work.
  - Rupert and Haymo appear only for their *exegetical* works. Their standing is
    tagged inconsistently: Rupert is `saintly` on some rows and
    `ecclesiastical-writer` on others [F: `passage-commentary-index.yaml`,
    counted by script].
  - `commentary-work-index discover --passage 'Matthew 9:1-8'` returns 19
    works, **none of them liturgical** [F: run this session].
  - The harvest's `death_year ≤ 1900` cutoff excludes Schuster (d. 1954) and
    Fromage (d. 1916) by construction [F: reading-plan guidance; I for its
    effect].
- **From a Mass: no mechanism exists.** The only routes are work descriptions,
  which name one Sunday (Rupert "XII.14", Durandus "VI.128/129"), earlier
  leaves' `scope.md`, and their bindings [F].

#### 1.5 Evidence that Sunday labels drift (this Sunday, read this session)

The 1962 Eighteenth Sunday (`pentecost-18`, registry `58`) has: Introit *Da
pacem*; Collect *Dirigat corda*; Epistle 1 Cor 1:4–8; Gradual *Laetatus sum*;
Alleluia *Timebunt gentes*; **Gospel Mt 9:1–8**; Offertory *Sanctificavit
Moyses*; Communion *Tollite hostias* [F:
`src/sources/calendars/roman-1962/propers.yaml:14802ff`].

| Witness and locus | Its own heading | What matches 1962 #58 | What differs |
| --- | --- | --- | --- |
| Rupert XII.18 | *Dominica decima octava* | Introit, Epistle, Gradual verse, Offertory, Communion | **Gospel Mt 23** |
| Rupert XII.19 | *Dominica decima nona* | **Gospel Mt 9** only | Everything else belongs to 1962 #59 |
| Honorius IV.84–85 | *Dominica decima octava* | Introit, Oration, Epistle, Gradual, Offertory, Communion | **Gospel Mt 22 (two commandments)**; Alleluia |
| Honorius IV.86 | *Dominica decima nona* | **Gospel Mt 9** only | — |
| Durandus VI.135 | *dominica decimaoctava* | Introit, Epistle, Gradual, Offertory, Communion | Gospel Mt 23 or Mt 22 "in quibusdam ecclesiis"; Alleluia *Laudate Dominum omnes gentes* |
| Durandus VI.136 | *decimanona* | **Mt 9** "in quibusdam ecclesiis" | — |
| Sicard | *Dominica decima octava* | Introit, Epistle, Gradual | Gospel Mt 22, "secundum alios" Mt 23 |
| Haymo, homily CXXIX (PL 118) | *Dominica decima octava* | Nothing | Gospel Lk 14:1ff, which is **1962 #56**'s Gospel |
| Smaragdus, *Hebdomada XVIII* (PL 102) | *Hebdomada XVIII* | Nothing checked | Epistle Eph 4:1–6, which is **1962 #57**'s Epistle |
| Schuster III pp. 167–170 | "Eighteenth Sunday… Tertia post natale S. Cypriani" | Every element read | — |
| *Liturgical Year* continuation (1883 vol. II p. 407; 1909 vol. XI p. 393) | "Eighteenth Sunday after Pentecost" | Gospel (the paralytic); the other elements were not read | — |
| Hadrianum (from the live run's `scope.md` §2.2, not re-verified) | *DOMINICA .XIX.* carries 1962 #58's orations | — | "Four different Sunday numbers for one set of prayers" |

**Conclusion.** [I]

1. A key by Sunday label mis-files **at least six of the twelve rows above**.
2. A key by "the Gospel" alone would file Rupert XII.19 under #58 and lose
   XII.18. Yet XII.18 shares six elements with #58.
3. Only matching **element by element** reports both loci truthfully.

---

### 2. Authority classes

#### 2.1 Two axes, not one

Standing and keying are independent questions. A saint can write a structural
treatise. An abbot with no cultus can expound the whole Mass. The present rule
speaks only to standing ("Fathers or saints"). The profile's
"documented reception of the compilation" speaks only to keying. [I]

**Axis A: standing (who the author is).**

| Class | Members, with examples from §1 | Basis to record |
| --- | --- | --- |
| **F** Father | Augustine, Gregory, Chrysostom. By patrological convention: Cassiodorus and Theodoret, who are already lane authors in C57 [F]. | Convention. **Nowhere recorded** [F]. The registry should record it. |
| **S** Canonized saint or Doctor | Anthony of Padua [F: canonized 1232]; Alphonsus Liguori; Bellarmine; Aquinas [the last three U here] | The act of canonization |
| **B** Blessed | **Schuster** [F: beatified 1996] | Beatification |
| **V** Venerable or Servant of God | **Guéranger**, Servant of God [F] | An open cause |
| **E** Orthodox ecclesiastical writer. Includes bishops, abbots, and popes writing privately. | Rupert, Honorius, Durandus, Sicard, Beleth, Berno, Bernold, Smaragdus, Haymo, **Fromage**; Innocent III writing as Lothar [U]; Gihr; Parsch | — |
| **C** Censured on a specific point | **Amalarius** (Quierzy 838) [F] | The censure and its scope |
| **H** Modern historian of the liturgy | Fortescue; Wilson as editor of the Hadrianum | — |
| **X** Outside Catholic communion | **Blunt** | Confession |

**Why standing matters, and its limit.** [F, then I]

- Under *Divinus perfectionis Magister* (1983) I.2–3, a Servant of God's
  published writings are "examined by theological censors", and the cause
  proceeds only if they contain "nothing contrary to faith and good morals"
  [F: vatican.va]. This happens before any decree of heroic virtue, so it
  precedes both beatification and canonization.
- Standing therefore certifies that an author is orthodox and holy. It does
  **not** certify any particular exegesis. Canonization differs from
  beatification in universality and finality, not in whether the writings were
  vetted [I].
- The two-author rule exists to anchor each reading in the Church's recognized
  teachers rather than in the editor. Standing is the right test for that
  anchor [I]. It is still no substitute for checking the argument, and the rule
  already demands a "substantive, compatible contribution".

**Axis B: keying (what the text is about).**

| Key | Examples | Used as |
| --- | --- | --- |
| **K1 Exegesis** of a text | patristic commentary on a pericope or psalm | reception of that text |
| **K2 The Mass as the author received it** | Rupert, Honorius, Sicard, Durandus, Schuster, the *Liturgical Year* | reception of **the compilation** (the existing rule, `:115-118`) |
| **K3 Sunday sermons or catena**: the day's readings preached or excerpted as a cycle | Anthony, Alphonsus, Haymo, Smaragdus, Gregory's Gospel homilies | reception of the readings **as this Sunday's**; also exegesis (K1) of them |
| **K4 Structural or ordo witness** | Amalarius's *de ordine*, Micrologus, Berno, Beleth's course, Blunt's tables, the Hadrianum | documented historical orientation (1962 profile class 2) |

#### 2.2 What each class may support

| Role in a study | F | S | B | V, E | C | H | X |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Reception of the compilation (K2 or K3 loci) | yes | yes | yes | **yes** | yes, outside the censured point | no | no |
| Supporting witness within a reading, for what his checked locus says | yes | yes | yes | yes | yes; the censure is disclosed in the research records | historical claims only | historical or comparative data only |
| **Counts toward the two-author minimum** | **yes** | **yes** | **D1** (recommended: yes, as the *second* author only) | no | no | no | no |
| Principal witness for a reading's claim about the Mass *as a Mass* | yes | yes | yes | **yes**, provided two F/S (or D1-B) authors carry the reading | no | no | no |

#### 2.3 Options for the contested cell

| Option | Rule | For | Against |
| --- | --- | --- | --- |
| **A. Strict** | Only F and S count | Plain Catholic usage ("saint" means canonized); matches the 1962 profile's "canonized"; nothing moves | Schuster, the one Blessed who expounds this Missal Mass by Mass, can never carry a reading |
| **B. Include the Blessed, with an anchor** (recommended) | F, S or B count, but at least one must be F or S | Beatification follows the same censors' examination and a formal judgment of heroic virtue; the anchor keeps every reading tied to a Father or canonized saint | "Saints" in the workflow text then needs a stated definition |
| **C. Commentators on the compilation count** | Any K2 commentator can be the second author for a whole-formulary reading | Honours the compilation evidence | Discards the purpose of the rule. Rupert has no cultus and Amalarius was censured. Liturgical allegory would fill readings with authors the rule was meant to exclude. |

**Recommendation: B.** Its consequence for the live run: Schuster could be
one of the two authors. Guéranger, Fromage, Rupert, Durandus, Honorius and
Sicard could not, which is the status quo. Candidly, the status quo (option
A) is also sound. The substantive gain in B is small, and the real gains in
this proposal are elsewhere: definitions, keying and attribution.

---

### 3. Sourcing

#### 3.1 Constraints

- **No purchases.** Research uses only public sources. "Do not purchase an
  edition, use a paid subscription, request or store access credentials" [F:
  `guidance/sources.md` "Repository-first acquisition"]. The monetary cost of
  everything below is **$0**. The real cost is registration effort and bytes.
- **Rights under United States law**, which is the repository's jurisdiction
  [F: publication policy, head]. Works first published abroad before 1931 are
  in the public domain [F: `guidance/missals.md` §5, citing Cornell's chart as
  of 1 Jan 2026]. That line moves every January.
- **Prefer non-Google scans.** Google's front-matter prose makes an OCR
  "remote, unresolved" [F: the vol. XI OCR record]. Every scan recommended
  below was checked this session and contains **no** "google" or "usage
  guidelines" string [F].
- **Size.** Keep text layers of about 1–4 MB tracked, which is existing
  practice for Migne OCR. Keep PDFs of 20–160 MB remote, with page images per
  cited locus, which is the existing Migne pattern.

#### 3.2 The French original, and who wrote the continuation

- **Internet Archive `lanneliturgiqu11gu`** (PIMS, University of Toronto) [F:
  metadata API and text layer, §8].
  - Title page: "L'ANNÉE LITURGIQUE par le R. P. Dom Prosper Guéranger… DEUXIÈME
    VOLUME DE LA CONTINUATION — LE TEMPS APRÈS LA PENTECÔTE, TOME II — LES
    DIMANCHES APRÈS LA PENTECÔTE, Douzième édition, Paris/Poitiers: H. Oudin,
    1911". Imprimatur by Henricus, bishop of Poitiers, April 1911.
  - The eighteenth Sunday ("LE DIX-HUITIÈME DIMANCHE") is at text-layer line
    28324.
  - Text layer: 1,178,533 B, sha1 `832f8006…`, sha256 `c24539c7…`. PDF:
    21,695,860 B.
- **The rest of the set.** Items `lanneliturgiqu01gu` to `…15gu` exist [F:
  advanced search]. Vol. 10 has a 1,087,838 B text layer and vol. 12 has
  1,225,796 B [F]. Their title pages and years were **not** read [U].
- **The continuator is Dom Lucien Fromage (1845–1916).** Three pieces of
  evidence:
  1. The French preface is **signed "Fr. L. F., O. S. B., Solesmes", October
     188[2?]**. The OCR is damaged at the year [F: text lines at the preface's
     end; year U]. The English preface omits the signature [F: 1883 and 1909
     English text layers].
  2. The BnF catalogue names **"Fromage, Lucien (1845-1916)"** as
     *Continuateur* (`cb318196703`), *Collaborateur* (`cb32133488h`), *Auteur
     du texte* (`cb32203039r`), and *Préfacier* of "Deuxième volume de la
     continuation. Le temps après la Pentecôte. Tome II" (`cb321334875`) [F:
     BnF SRU].
  3. Oxford catalogue metadata on four Internet Archive items reads
     "Continuation [by L. Fromage]" (`liturgicalyeart00fromgoog` to
     `…03fromgoog`) [F]. These are Google scans; use them for the attribution
     only.
- Whether Fromage alone wrote every continuation volume is [U]. The title
  pages of *Time after Pentecost* I and II call them the first and second
  volumes of the continuation [F: vol. X edition record; the French vol. 11].
- **Rights.** Paris 1911 is a foreign publication before 1931, so it is public
  domain in the US [I from the rule in §3.1]. The authors died in 1875 and
  1916. Life plus 70 has also expired in France, whatever the wartime
  extensions [I].
- The English 1883 first edition gives the Mass a reading of priesthood.
  Following the September Ember-day ordinations, "the powers conferred, by the
  imposition of the Bishop's hands… are the most marvellous gift", and "the
  other portions of the Mass… are… most appropriate to the prerogatives of the
  new Priesthood" [F: `liturgicalyear11gu` text layer ≈ lines 24545–24560].

#### 3.3 Prioritized acquisitions

Every item is a public download and no purchase is involved. "Verified" means
the item's metadata and the named locus were read this session.

| P | Work and item | Internet Archive id (verified) | Size (text layer / PDF) | Rights evidence | Value for 1962 studies |
| --- | --- | --- | --- | --- | --- |
| **P1-a** | *L'Année liturgique*, French, the *Temps après la Pentecôte* volumes (10–15). Start with 11 and 10. | `lanneliturgiqu11gu` (read); `lanneliturgiqu10gu`, `…12gu` (metadata only) | 1.18 MB / 21.7 MB; 1.09 / 22.4; 1.23 / 28.4 | Paris 1911 [F for vol. 11]; authors d. 1875 and 1916 → US public domain [I] | The original of the most-cited commentator. Provides the "own language" layer that catena Rule 11 depends on, and fixes the attribution. **High.** |
| **P1-b** | *Liturgical Year*, English 1883 Duffy, *Time after Pentecost* I–III, **without Google prose** | `liturgicalyear11gu` (title page "1883" read; eighteenth Sunday at p. 407); `liturgicalyear10gu`, `…12gu` (metadata only); UNC alternatives `liturgicalyear11gura` etc. | 1.19 MB / 35.1 MB (vol. 11) | 1883 → US public domain by date [I]. The scan stamp is Internet Archive's four-line credit, the same class as tracked Migne OCR [F] | A **trackable, searchable** English text. Today's vol. XI OCR is remote because of Google prose. **High.** |
| **P1-c** | Honorius, the whole *Gemma animae* (PL 172) | `patrologiaecursu0172mign` (Claremont; IV.84–86 read); alternative `patrologiaecur172mign` (PIMS) | 4.17 MB / 88.3 MB | Migne 1854; Claremont PL OCRs are already tracked as public domain [F] | Replaces a *restricted* holding with a lawful one and reaches every Sunday. **High.** |
| **P2-a** | Schuster, English vols I, II, IV and V | `LiberSacramentorum` (five PDFs and five text layers; files listed) | 0.84–1.12 MB each / 124–154 MB each | Published in London, dated 1924–1930 in Internet Archive metadata [F]; the date of each volume is [U]; foreign publication before 1931 → US public domain [I] | The rest of the year. The Time after Pentecost is **already covered by vol. III** [F]. Medium for this series. |
| **P2-b** | Haymo, *Homiliae de tempore* (PL 118) | `patrologiaecursu0118mign` (homily CXXIX read) | 3.10 MB / 64.5 MB | Migne, public domain | A Sunday-Gospel homiliary (K3). Migne's "Haymo of Halberstadt" versus "of Auxerre" is [U]. Medium. |
| **P2-c** | Smaragdus, *Collectiones in epistolas et evangelia* (PL 102) | `patrologiaecursu0102mign` (*Hebdomada XVIII* read) | 3.45 MB / 69.5 MB | Migne, public domain | A Carolingian patristic catena on the week's Epistle and Gospel. **Beware the appended sixteenth-century *Summarium*** at col. 553 [F: the volume's contents]. Medium; a source of leads. |
| **P2-d** | Alphonsus Liguori, *Sermons for all the Sundays in the year* | `sermonsforallsun00liguuoft` (Dublin: Duffy, 1882; metadata only); alternative `sermonsforallsun00ligu` (Boston Public Library) | 1.08 MB / 29.2 MB | 1882 → US public domain [I]; the translator was not checked [U] | A Doctor (standing S) whose Sundays are the Tridentine ones [I]. Can carry a reading. Medium–high. |
| P2-e | Anthony of Padua, the whole *Sermones dominicales* | Partly held already. A search of Internet Archive for the Locatelli edition (Padua 1895–1913) **found no item** [F, bounded negative] | — | [U] | A canonized author whose sermons are keyed to the Sunday. Find a whole public-domain witness later. |
| P3 | Innocent III, *De sacro altaris mysterio* (PL 217) | `patrologiaecursu0217mign` (heading read) | 3.49 MB | public domain | The Ordinary, not the propers (belongs to ordinary-expositions). Low here. |
| P3 | Pseudo-Alcuin, *De divinis officiis* (PL 101) | `patrologiaecursu0101mign` | 4.74 MB | public domain | A literal search found **no** "post Pentecosten" Sunday chapters [F, bounded; OCR may miss them]. Low. |
| — | Amalarius, *Liber officialis* | Already tracked, inside the PL 105 container [F] | — | — | For the containment lane to expose. |

**Not acquirable under current policy.**

- **Parsch**, *The Church's Year of Grace* (1953–59) and *Das Jahr des Heiles*
  (1933, 1938). Internet Archive offers only controlled lending
  (`inlibrary`/`printdisabled`), and borrowing needs credentials [F:
  advanced-search collections]. The 1953–59 US editions would also need a
  renewal search [U].
- **Schuster's Italian original.** Not found on Internet Archive [F, bounded
  search]. Gallica and HathiTrust were not searched [U].
- **Modern critical editions and translations.** Hanssens's Amalarius
  (1948–50), the CCCM editions of Rupert, Beleth and Durandus, and the Knibbs
  and Thibodeau translations: copyright is presumed and was **not checked** [U].

**Approximate total cost.** $0.

- Bytes: about 20 MB of new tracked text layers if every P1 and P2 item lands.
  PDFs stay remote, as measured size arguments.
- Effort: one registration lane per P1 item. Each needs a title-page reading,
  hashing, a Google-prose probe, a rights basis, and a check of Migne
  constituent extents in coordination with the containment inventory.

---

### 4. Storage and keying

#### 4.1 Principles

1. **Edit no existing record.** A field added to `work.toml` moves its
   `source_fingerprint` and cascades review obligations. Measured: 53 bindings
   hang from one Augustine record [F: `src/sources/commentary/work-extents.yaml`
   header]. Sidecars are the precedent (`fragment-loci.yaml`,
   `work-extents.yaml`).
2. **Record the Mass the commentator had, not the one we have.** Store his
   elements as he names them, and his heading as data.
3. **Derive every match to a calendar; store none.** This is `the-shape.md` §2:
   a stored match to 1962 would be a second source of truth.
4. **The inventory is a finding aid, not evidence** [F: `sources.md`, "An index
   is a planning and cross-reference spine…"]. A study still inspects and binds
   the locus.
5. **Holdings belong to the containment inventory.** This file only names
   `work_id`s.
6. **Standing belongs to one registry**, never to locus rows or harvest tags.

#### 4.2 New file: `src/sources/commentary/formulary-loci.yaml` (recommended)

It is the Mass-keyed twin of `fragment-loci.yaml`: a typed edge from a
commentary locus to what it comments on. It belongs beside that file and is read
by the same tool. The alternative location is decision D4.

```yaml
schema: triptych-commentary-formulary-loci/v1
updated: '2026-09-22'
numbering: vulgate            # every `ref` below is in Clementine Vulgate numbering
works:
  - work_id: 'work.rupert-of-deutz.de-divinis-officiis'
    genre: 'office-exposition'        # office-exposition | mass-exposition | missal-commentary
                                      # | sunday-sermons | sunday-catena | structural
    locus_grammar: 'XII.<chapter>'    # the author's own division
    label_system: "Rupert's own 'Dominica N post Pentecosten', Book XII"
    loci:
      - locus: 'XII.18'
        read_in: 'artifact.rupert-of-deutz.de-divinis-officiis.latin-migne-pl-170.ia-djvu-ocr-2e2ca850'
        lines: [23443, 23486]                 # tracked text: replayable
        printed: 'PL 170 cols. 325-326'       # optional; [U] until read on an image
        own_label: 'Dominica decima octava post Pentecosten'
        season: 'after-pentecost'
        ordinal: 18                           # the author's ordinal, never the 1962 one
        treatment: 'whole-office'             # whole-office | per-element | single-element | structural
        elements:
          - {role: 'introit',   incipit: 'Da pacem',               ref: 'Sirach 36:18'}
          - {role: 'epistle',   incipit: 'Gratias ago Deo meo',    ref: '1 Corinthians 1'}
          - {role: 'gradual',   incipit: 'Fiat pax in virtute tua', ref: 'Psalm 121:7', as: 'verse'}
          - {role: 'gospel',    incipit: 'Super cathedram Moysi',  ref: 'Matthew 23'}
          - {role: 'offertory', incipit: 'Sanctificavit Moyses',   ref: 'Exodus 24'}
          - {role: 'communion', incipit: 'Tollite hostias',        ref: 'Psalm 95'}
        state: 'located'                      # located (text layer) | inspected (page image)
        checked_on: '2026-09-22'
      - locus: 'XII.19'
        # … own_label 'Dominica decima nona post Pentecosten'; gospel ref 'Matthew 9' …
  - work_id: 'work.william-durandus.rationale-divinorum-officiorum'
    loci:
      - locus: 'VI.135'
        edition_note: 'chapter numbers vary by printing; Lyon 1612 t. II prints CXXXV'
        elements:
          - {role: 'gospel', ref: 'Matthew 23', alternative: 'in quibusdam ecclesiis'}
          - {role: 'gospel', ref: 'Matthew 22', alternative: 'in quibusdam ecclesiis'}
          # …
  - work_id: 'work.prosper-gueranger.the-liturgical-year'
    writer: 'Dom Lucien Fromage OSB (1845-1916)'   # for the Time after Pentecost volumes; see D7
    writer_basis: 'French 1911 vol. 11 preface signed Fr. L. F.; BnF cb321334875 (Préfacier), cb318196703 (Continuateur)'
    locus_grammar: 'tap-<sunday>'      # the book's own chapter, stable across editions
    loci:
      - locus: 'tap-18'
        at: [{edition: '…english-duffy-1900-volume-11', pages: '393-'},   # 1909 printing
             {edition: '(1883 Duffy, when registered)', pages: '407-'}]
        own_label: 'Eighteenth Sunday after Pentecost'
```

**Closed vocabularies.**

- `role`: introit, collect, lesson, epistle, gradual, alleluia, tract,
  sequence, gospel, offertory, secret, preface, communion, postcommunion,
  historia (office), other.
- `genre`, `treatment` and `state` as in the sample.

**Structural loci** (Berno VI, Micrologus XXVIII–XXIX, Amalarius's *de ordine*
LXXIII) get `treatment: structural` and no elements. They are listed by topic
and never matched to a Mass.

#### 4.3 The derived projection

This is computed by a tool and never stored.

**Command.**
`commentary-work-index formulary --calendar roman-1962 --mass pentecost-18
[--json]`. It is a new verb, so it does not collide with the containment lane's
changes to `discover`.

**Algorithm.**

1. **Normalize incipits.** Casefold; strip diacritics; j→i, v→u, æ/ae→e,
   œ/oe→e; collapse whitespace. Two incipits match when the shorter is a prefix
   of the longer and at least two words long.
2. **Compare references.** Parse them through `tools/citations`, with psalms in
   declared numbering through `scripts/_psalms.py` (this reuses the existing
   rules and adds none). They match on overlap **at the precision recorded**.
   "Matthew 23" is chapter-level and is never narrowed.
3. **Build one match vector per locus.** Each role is `same`, `different`,
   `not-named-by-commentator` or `not-in-calendar`. Alternatives ("in quibusdam
   ecclesiis") are reported as alternatives.
4. **List a locus under a mass** when it matches at least one of Introit,
   Collect, Epistle or Gospel, or at least two other roles.
   - A match only on a chant that recurs at more than one mass of the calendar
     is flagged `weak`. The recurrence count is derived.
   - A row whose `ordinal` differs from the matched mass's is flagged
     `label-drift`. This is **information, not an error**.
5. **Report beside each row.** Author standing (from the registry), holding
   state (from the containment inventory) and the row's `state`.
6. **Refuse** a row with neither elements nor `structural`, a role outside the
   vocabulary, or an unknown key. The last closes the unrecognised-key gap that
   `sources.md` names.

**Expected output for #58.** This is the fixture the tests should pin.

- Rupert XII.18 and Honorius IV.84: listed; "Gospel differs"; `label-drift`
  none.
- Rupert XII.19 and Honorius IV.86: listed as "Gospel only"; `label-drift`
  19≠18.
- Durandus VI.135: listed; Gospel alternatives both differ. VI.136: Gospel
  only.
- Schuster III: full match.
- Haymo CXXIX: **not listed** under #58, and listed under #56 with drift 18≠16.

**Portable across calendars.** The same rows project onto `roman-pre-1955` or
`postconciliar` without change [I]. That is what storing the commentator's Mass
buys.

#### 4.4 Locus patterns

| Work | Locus (the author's own division) | Stable across editions? |
| --- | --- | --- |
| Rupert, *De div. off.* | `XII.<chapter>` | yes |
| Durandus, *Rationale* | `VI.<chapter>` | **no**. Printings number differently: Lyon 1612 has 135 for the eighteenth Sunday, and the 1568 layer is damaged [F: C57 binding]. Record `edition_note`. |
| Honorius, *Gemma animae* | `IV.<chapter>` (the existing `locus_pattern`) | yes. A Sunday spans a "sub lege / sub gratia" pair (IV.84–85). |
| Sicard, *Mitrale* | `VIII.<chapter>` [I from the work description's "VIII.14"] | [U] |
| Beleth, Micrologus, Berno, Amalarius (*de ordine*) | `<chapter>` | structural |
| *Liturgical Year* | `tap-<n>`, the book's chapter. Pages vary by printing (1883 p. 407; 1909 p. 393), so pages live in `at`. | chapter: yes; pages: no |
| Schuster | `vol-<n>/<Sunday chapter>` with pages | [U] across the Italian and English |
| Anthony of Padua | `dominica-<ordinal>-post-pentecosten/sections-<a>-<b>` (existing pattern) | yes |
| Haymo | `hom-<n>` (CXXIX) | Migne numbering |
| Smaragdus | `hebdomada-<n>-post-pentecosten` | Migne |
| Blunt | `trinity-<n>` | yes |

#### 4.5 New file: `src/sources/inventories/author-standing-v1.toml`

Schema `triptych-author-standing/v1`. One row per **person**, keyed by the
work-id namespace (`rupert-of-deutz`).

**Fields.**

- `name`, `died`
- `standing`: father | doctor | saint | blessed | venerable | servant-of-god |
  ecclesiastical-writer | historian | non-catholic
- `standing_basis`: the act and its date, with a source URL or record id
- `censures`: a list of {body, year, point}
- `confession`, `notes`

**Seed rows from this lane.**

- Schuster: `blessed`, 1996-05-12, USCCB.
- Guéranger: `servant-of-god`, cause opened 2005-12-21.
- Fromage: `ecclesiastical-writer`.
- Amalarius: `ecclesiastical-writer`, with censures `{Kiersy, 838, the
  signification of the divided Host}`.
- Anthony: `saint`, canonized 1232.
- Blunt: `non-catholic`, Anglican.
- The rest as in §1.2.
- **Also record the conventional Fathers** already used as lane authors
  (Cassiodorus, Theodoret), so that "Father" stops being unrecorded.

The harvest's `role` field remains **model lead data**, not standing.

#### 4.6 How this composes with the containment inventory

The containment lane (`src/sources/inventories/`, new file) maps each container
artifact to its constituent `work_id`s with extents [F: brief; the worktree
showed no committed changes when inspected].

- `formulary-loci` never states holdings. The tool asks the containment layer
  what holds `work_id` W. It then prints tracked-text, remote, in-container
  (with the extent) or catalog-only.
- **Cross-check.** When a row's `read_in` is a container artifact, or a
  constituent's copy of container bytes (Rupert inside the PL 170 OCR), the
  row's `lines` must fall inside that constituent's declared extent. The check
  is cheap and catches a locus filed under the wrong work [I; it depends on the
  lane's final field names].
- Bindings are unchanged. A study that uses a locus binds its
  passage/artifact/segment in `research/source-bindings.toml` as it does today.
- `build-corpus` may later add a `liturgical_commentary` section per mass to
  `mass-commentary-corpus.yaml`. It must stay unranked and kept apart from the
  harvest's confidence scores, following catena Rule 1 in spirit [I].

---

### 5. Inclusion

#### 5.1 How a study should use these witnesses

**Attribution.**

- Name the writer the locus inventory names. The *Time after Pentecost* volumes
  are "the continuation of Guéranger's *Liturgical Year* (Dom Lucien Fromage)".
  They are **not** "Guéranger records".
- Cite the printing actually used, e.g. "(Stanbrook Abbey; London: Burns &
  Oates, 1909)". Do not use "Duffy, 1900".

**Separation from the Fathers.**

- In `research/interpretations.md`, give liturgical witnesses their own mark,
  e.g. `[L]`, beside the existing `[A]/[T]/[H]/[E]` scheme of C57. This
  separates "what Rupert said of his office" from both a Father's exegesis and
  editorial synthesis.
- In `proper-components.toml`, list them in `authors` but not in
  `carrying_authors` (§5.3).

**A Mass with another Gospel.**

- Use the commentator only for the elements his Mass shares with this one.
- Record the element that differs.
- Reader-facing prose says so once, where he is first used, in the tradition's
  voice.
- His reading of his own Gospel counts as reception of *that* Gospel only.
- The C57 practice is the model.

**Binding role.** Use `reception` for K2 and K3 loci and `context` for K4 and
class X. Never use `direct-witness` for a commentator on the compilation [I;
one vocabulary for the ambiguity in §1.3].

**What the reviewer checks.**

1. The element comparison was made.
2. Each commentator is used only for the shared elements.
3. The differing element is recorded.
4. Each commentator's standing matches the role he plays.
5. No reading's two-author minimum depends on class V, E, C, H or X.
6. Attribution follows the registry.

#### 5.2 Proposed rule text

**(a) Guidance.** Owned by `guidance/liturgy/propers-three-documents.md`, as a
new subsection after "The formulary is a compilation". Guidance is not
digested, so this **takes effect immediately for every stage dispatched after
it lands, including stages of runs already in flight**. The final sentence
limits its reach backwards (decision D6).

> ### Liturgical commentators
>
> A liturgical commentator expounds a Mass or office as a whole — Rupert of
> Deutz, Honorius, Sicard, Durandus, Schuster, *The Liturgical Year* — or
> preaches the Sunday's readings as a cycle, as Anthony of Padua and Alphonsus
> Liguori did. His witness is reception of the compilation as his books gave
> it, and it is used in that role.
>
> Identify his Mass by its elements, never by its Sunday number. Compare the
> Introit, Collect, Epistle, Gospel and other elements he names with the
> governing edition's; `commentary-work-index formulary` reports that
> comparison from `src/sources/commentary/formulary-loci.yaml`. Record in
> `research/scope.md` his own heading beside the elements that match and those
> that differ. A commentator's "eighteenth Sunday" is evidence only for the
> elements it shares with this formulary.
>
> Where his Mass had another Gospel or chant, attribute to him only what he
> says of the elements this formulary keeps, record which element differed,
> and say so once where he is first used. Do not present him as a reader of a
> Gospel his Mass did not have; his reading of the Gospel it did have is
> reception of that Gospel.
>
> Standing decides what a commentator may carry.
> `src/sources/inventories/author-standing-v1.toml` records each author's
> standing and its basis. An interpretation's two authors are Fathers,
> canonized saints or Doctors, [or the Blessed, provided at least one is a
> Father or canonized saint — per D1]. Any other commentator may be a reading's
> principal witness to the Mass as a Mass and may support any claim his checked
> locus makes, but is never one of its two authors. A commentator censured on a
> point is not cited for that point. A writer outside Catholic communion
> supplies historical or comparative data only.
>
> Attribute words to the writer the locus inventory names; a posthumous
> continuation published under a founder's series name is the continuator's
> and is cited as the continuation. Research first submitted for review before
> [date of adoption] is not reopened for this subsection alone.

**(b) Guidance.** Owned by `guidance/liturgy/roman-1962-propers.md:156`. Add to
the reception-sweep sentence: "…and search the formulary's liturgical
commentators through `commentary-work-index formulary` as well as each
passage's exegetes." Effective immediately.

**(c) Schema documentation.** Owned by `src/sources/commentary/README.md`. Add a
section describing `formulary-loci.yaml`, its closed field set, and the rule
that matches are derived. It is not a workflow file, so it has no runtime
consequence.

**(d) Workflow data.** Owned by `workflows/fragments/proper-study/research-review.md`.
Add after line 22: "For every liturgical commentator used, confirm the element
comparison, that his locus supports only elements his Mass shares with this
formulary, and that his recorded standing permits the role he plays." Also, in
`contract.md:38`, `research-review.md:21`, `study-review.md:11` and
`author-study.md:8`, change "Fathers or saints" to "Fathers or saints, as the
profile defines them". **Consequence:** this moves the `proper-study` workflow
digest. Any run seeded earlier fails closed at its next `advance` [F:
`workflows/ARCHITECTURE.md:268-271`]. It therefore applies only to runs seeded
after the version bump. **Do not land it while the Eighteenth-Sunday run is
live.**

**(e) Code, opt-in.** Owned by `scripts/_proper_components.py` and the
"Mechanical and judgment gates" section of the three-documents profile.

- A manifest that declares `authority_contract = "authority-standing-v1"` gives
  each lane `carrying_authors` (a subset of `authors`). The checker requires at
  least two distinct persons whose registry standing is permitted, with at
  least one Father or canonized saint.
- The pipeline makes this mandatory by adding `--require-authority` to the
  `research-preflight` command in `proper-study.json`. That is workflow data,
  so it reaches future runs only.
- **Consequence:** gate code is not digested, so it runs in live runs too
  [F: the digest covers "the canonicalized pipeline JSON plus… every fragment
  and schema", `ARCHITECTURE.md:250-252`]. It stays safe only because it is
  opt-in.

#### 5.3 Who owns what: summary

| Rule | Owning file | Kind | Takes effect |
| --- | --- | --- | --- |
| Element-based identification; the different-Gospel rule; attribution | `guidance/liturgy/propers-three-documents.md` (new subsection) | guidance | immediately, for all later dispatches |
| What counts as a "saint"; standing | the same subsection, plus the data in `author-standing-v1.toml` | guidance + data | immediately (transitional clause) |
| The sweep includes Mass-keyed commentators | `guidance/liturgy/roman-1962-propers.md:156` | guidance | immediately |
| Reviewer checklist; the "as the profile defines" pointer | four `workflows/fragments/proper-study/*.md` files | workflow data | runs seeded after the version bump only |
| Mechanical standing check | `scripts/_proper_components.py` (opt-in) plus a gate flag in `proper-study.json` | code + workflow | code: none until a manifest opts in; flag: future runs |

---

### 6. Decisions for the maintainer

| # | Decision | Options | Recommendation | Consequence |
| --- | --- | --- | --- | --- |
| **D1** | Does "saints" in the two-author rule include the Blessed? | A: canonized only. B: plus the Blessed, provided one of the two is a Father or canonized saint. C: plus Venerables and Servants of God. | **B** | Schuster can carry a reading; Guéranger and Fromage cannot. One sentence in guidance, plus registry data. |
| **D2** | May a liturgical commentator with no cultus ever count as a reading's second author? | Never. Only for whole-formulary readings. Freely. | **Never.** He may be the principal witness to the Mass as a Mass. | Keeps the rule's purpose. C57-style lanes stay valid because Fathers carry them. |
| **D3** | Censured authors (Amalarius) and non-Catholic ones (Blunt) | Exclude. Allow as structural or context only. Treat like others. | **Structural or context only.** A censure is recorded and never cited for its point. | Blunt remains available for historical comparison of readings. |
| **D4** | Where the Mass-keyed locus inventory lives, and whether Sunday sermon cycles belong in it | `src/sources/commentary/formulary-loci.yaml` or `src/sources/inventories/liturgical-commentary-loci-v1.toml`; one file or two | **`commentary/formulary-loci.yaml`, one file, with `genre`** | It sits beside `fragment-loci.yaml` and is read by the same tool. |
| **D5** | Create the author-standing registry and the opt-in mechanical check? | Registry and check. Registry only. Neither (reviewers alone). | **Registry and opt-in check**, made mandatory at the next `proper-study` version | Closes the checker's blind spot (`_proper_components.py:751`). |
| **D6** | Timing relative to the live Eighteenth-Sunday run | Land everything now. Land guidance now with a transitional clause, and workflows after the run. Land everything after the run. | **Inventories, tool and acquisitions now.** Guidance with the transitional clause. `workflows/` edits only after the run publishes. | Nothing seals the live run out. The live run may use the §5.1 practice voluntarily. |
| **D7** | Attribute the *Time after Pentecost* continuation to Fromage, and correct published leaves? | Adopt and correct. Adopt for new work only. Keep "Guéranger and continuators". | **Adopt**, recorded in `formulary-loci` (`writer`, `writer_basis`). Put the seven leaves on the staleness list for their next revision. | Corrections are per-leaf content revisions, each rebuilt and reviewed. Existing records are not touched. |
| **D8** | Approve the acquisitions | P1 only. P1 and P2. Defer. | **P1 now; P2 as studies need it** | About 20 MB of tracked text if all land; $0. |
| **D9** | Google front matter: the tracked vol. XI PDF contains Google's usage-guidelines page, while the OCR of the same scan was refused for that page | Refuse such PDFs too. Allow such OCR too. Settle once in a rights record. | **One rights record under `inventories/`** settling Google front matter. Meanwhile prefer non-Google scans (P1-b). | Removes an internal contradiction. May change future dispositions. |
| **D10** | Two artifact identities for one vol. XI OCR (sha256 `f4c31a52…`) | Leave it. Supersede one at the next schema revision. | **Leave it**, and note it in `formulary-loci`. Fold the two together at the next deliberate schema change. | No fingerprint movement now. |

---

### 7. Implementation plan

| Step | What | Touches | Tests and checks | Disturbs the live run? |
| --- | --- | --- | --- | --- |
| 0 | Maintainer decides D1–D6 | — | — | no |
| 1 | `author-standing-v1.toml`: schema, seed rows, validator (closed fields; every basis cited; persons unique) | new file; a validator verb in `commentary-work-index` or `source-library` | a unit test; a line in `make check-sources` | no. Nothing reads it yet. |
| 2 | `formulary-loci.yaml`: schema, the seed rows of §1.5, validator (closed fields; quoted scalars; `work_id` and `read_in` exist; **the own_label occurs within `lines`** of the tracked artifact; refs parse; role vocabulary) | new file; `src/sources/commentary/README.md` | a fixture test for #58 with the §4.3 expectations; register the replayed example | no |
| 3 | The `commentary-work-index formulary` verb (derived projection; standing and holding joins) | the tool; `tmt.json` registration | `make check-examples`; test the drift flags and the `weak` flag | no. **Wait for the containment lane** before the holdings join. |
| 4 | Acquisitions P1-a, P1-b and P1-c, as **new** editions and artifacts only. Coordinate PL 172 with the containment inventory (a container record plus a segment, or a constituent edition). | new records under existing works. Adding a child does not move an ancestor's fingerprint [I: the fingerprint hashes a record and its ancestors]. | `make check-sources`; source-inventory and family-migration refresh per `sources.md` | no |
| 5 | Guidance: subsection 5.2(a) and sentence 5.2(b) | two guidance files | none mechanical | **yes, immediately.** Keep the transitional clause (D6). |
| 6 | Opt-in `authority_contract` in `_proper_components.py` | code | `tools/tests/test_proper_components_v2.py` gains cases for pass, fail, and missing registry | no, while opt-in |
| 7 | Workflow: the reviewer sentence, the four "as defined" pointers, `--require-authority` in `research-preflight`, and a `proper-study` version bump | `workflows/fragments/proper-study/*.md`, `workflows/pipelines/proper-study.json` | workflow digest and version tests | **yes, the live run fails closed.** Land after the Eighteenth-Sunday run publishes. |
| 8 | Correct the seven leaves' *Liturgical Year* attribution and imprint | per-leaf content revisions; research-staleness inventory | per-leaf build, review and installation | no. These are separate publications. |
| 9 | Optional: a `liturgical_commentary` section in `build-corpus` | the tool; `mass-commentary-corpus.yaml` | a byte-identical rerun test | no |

**What the live run can do today, with no rule change.** The existing text
(`propers-three-documents.md:115-125`) already permits the following as
documented reception of the compilation:

- Rupert XII.18 and XII.19, Durandus VI.135 and VI.136, and Sicard, all held
  as tracked OCR.
- Schuster III pp. 167–170, held.
- The continuation, vol. XI p. 393, held.
- Honorius IV.84–86. **This is not held.** Cite it in the ordinary
  bibliography until P1-c lands; `research.md:8-9` forbids inventing a binding.

Each must follow the C57 practice for a differing Gospel. None may be counted
as a Father or saint (option A), except Schuster if D1 is decided as B before
the review.

---

### 8. Receipts and what could not be verified

**Fetched this session.** Hashes were computed locally. The bytes were deleted
after reading, and each can be re-fetched by URL.

| What | URL | Bytes | Hash |
| --- | --- | --- | --- |
| French *Année liturgique*, vol. 11, text layer | archive.org/download/lanneliturgiqu11gu/lanneliturgiqu11gu_djvu.txt | 1,178,533 | sha256 `c24539c74426ab89d37b6dd1fb4909297c1361b15b555a760165920fd7fd6c07` |
| English 1883 vol. II (11), text layer | archive.org/download/liturgicalyear11gu/liturgicalyear11gu_djvu.txt | 1,186,268 | sha256 `95cdb0fcbc8a5457884b9484a1034869be7669ce7a0fbef431cbd99a6f5d503d` |
| PL 172 OCR | archive.org/download/patrologiaecursu0172mign/…_djvu.txt | 4,174,594 | sha256 `2ebfcb5f…444b1` |
| PL 118 OCR | …/patrologiaecursu0118mign/… | 3,104,199 | sha256 `901072d1…db58` |
| PL 102 OCR | …/patrologiaecursu0102mign/… | 3,447,804 | sha256 `feed5e4c…1df34` |
| PL 101 OCR | …/patrologiaecursu0101mign/… | 4,737,235 | sha256 `e7e2370e…b71f0` |
| PL 217 OCR | …/patrologiaecursu0217mign/… | 3,490,162 | sha256 `4eb35d5e…a48` |
| Internet Archive metadata | archive.org/metadata/{id}, for the ids in §3.3 | — | — |
| BnF catalogue | catalogue.bnf.fr/api/SRU, query `bib.author all "Fromage" and bib.title all "année liturgique"` | — | records cited in §3.2 |
| Catholic Encyclopedia | newadvent.org/cathen/{07058a, 01376b, 05207a, 13770b, 02512a, 02512c, 07461a, 01556a}.htm | — | — |
| Guéranger's cause | domgueranger.net: "le-proces-de-beatification-et-de-canonisation/" and "ouverture-de-la-cause-…-2/" | — | — |
| Schuster's beatification | usccb.org/offices/general-secretariat/beatifications-during-pope-john-paul-iis-pontificate | — | — |
| *Divinus perfectionis Magister* | vatican.va, English and Latin, hf_jp-ii_apc_25011983 | — | — |

No source text passed through a model. Fetches used `curl`, and reading used
`rg`, `sed` and `pdftotext` locally. One web search was used, only to locate
the two status pages, which were then fetched with `curl`.

**Not verified [U].**

- Life dates and standing of Rupert, Beleth and Blunt beyond what the records
  state.
- Blunt's orders.
- The Doctor status of Anthony (1946) and Alphonsus.
- The year of the French preface (OCR damaged).
- Whether Fromage alone wrote every continuation volume.
- Title pages of the French vols 10 and 12–15 and the English vols 10 and 12.
- The per-volume dates and contents of Schuster's English vols I, II, IV and V.
- Whether Schuster's Italian original exists on Gallica or HathiTrust.
- Rights of the modern critical editions.
- Haymo's attribution.
- Sicard's book number.
- Blunt's Trinity/Pentecost offset.
- The Hadrianum claim, taken from the live run's `scope.md` and not
  re-verified.
- The containment inventory's final field names.
- Every [I] above.
