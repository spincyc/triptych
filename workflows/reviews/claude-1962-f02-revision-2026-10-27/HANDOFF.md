# Research handoff: revision of the Claude All Saints (1962)

Identity `liturgy/roman-rite/1962/propers/temporal/f02-all-saints`, provider
`claude`, Sunday 1 November 2026, audience "adult parish assembly".

On 27 October 2026 the maintainer asked for the Claude work of 26–27 October
to be checked, because partway through that work the host had run some stages
on a different model without notice. For All Saints the maintainer decided:

- the expansive study starts again from the last text the Claude model wrote,
  the study as it stood after author-study iteration 1 of run
  `427e2f58bb897a16`, and every later revision is made in this run;
- the research is rebuilt from the sources, with nothing taken over from the
  earlier research records;
- the concise study and the homily are derived again from the revised study.

The earlier research records (`research/`, except the study's production
record, and `propers/`), the concise study, the homily, the standing-findings
record `evaluations/blocking-findings-v1.toml` and the earlier contribution
lines were removed from the leaf before this run was seeded, together with
the two Patrologia Latina volume 35 artifacts registered for them. The first run's archive under
`evaluations/proper-study-results/427e2f58bb897a16/` stays as the record of
that run. It is not evidence, and no verdict in it carries over. Do not open
it, and do not recover the removed files from Git history: this handoff is the
only thing carried over, and everything in it is a **lead** to verify against
the sources.

This remains an independent Claude production. Do not open the GPT leaf for
the same identity, its PDFs or web edition, or its workflow records.

## The study's own review (study-review iteration 0)

The restored study is the text that review read. Its findings stand against
it, and the revision should answer each. Line numbers refer to the restored
files.

- **STU-001 (research).** Victorinus of Pettau was recorded as not reaching
  Apoc 7, so Bede alone carried the first reading. The registered ANF VII text
  (`ccel-text-b69327af`) comments on chapter 7 from line 33565: the ascending
  angel of 7:2 is Elias, and "the number of those that shall believe, of the
  Jews and of the nations, is a great multitude which no man was able to
  number" (lines 33575–33577); on 7:9, the multitude is "the number of the
  elect out of all believers" (lines 33620–33625). He also reads the 144,000
  at 12:6. The artifact's elucidations carry a recension caution. The review
  also asked for a proportionate second search for an eligible witness on
  Apoc 7 beside Bede, naming Caesarius of Arles' Apocalypse homilies.
- **STU-002.** Each interpretation must read the whole Mass. The first never
  used the Gospel, Alleluia, Communion or either Secret; the second never used
  the Lesson, the Secret, the Postcommunion or the commemoration's Secret and
  Postcommunion; the third never used the Lesson, Introit or Communion.
- **STU-003.** The study gave four Fathers an agreement they do not hold, that
  the first and eighth beatitudes are present and the six between future. The
  two-and-six observation is the study's own. Augustine (*De serm. Dom.*
  I.4.12) says the promises can be fulfilled in this life, as in the apostles;
  Chrysostom (*Hom. in Matt.* 15) says the mourners are comforted "both here
  and there"; Aquinas (*Super Matt.* 5) has the rewards begun on the way;
  Hilary reads them of those changed by immortality.
- **STU-004.** "Bellarmine alone keeps a temporal sense" is false. Aquinas,
  *Super Psalmos* 33 n. 10 (Parma vol. 14), expounds *non est inopia* first of
  bodily want and adds "Item Deus quaerentibus se subvenit in necessitate".
- **STU-005.** Several sentences credit named Fathers with the study's own
  synthesis of the feast (00 L69–76; 20 L6–10, L135–136; 30 L9–10; 40 L54–55).
- **STU-006.** The body narrates the study's procedure ("the study notes",
  "that join is the study's", disclaimers about what it does not supply).
- **STU-007.** Paragraphs close on maxims or restatements, and antitheses are
  drawn against positions nobody holds.
- **STU-008.** Apoc 7:11 misread at 10 L80–81: it is the angels, standing
  round the throne, the ancients and the living creatures, who fall on their
  faces.
- **STU-009.** The second interpretation asks why the Communion sings three
  beatitudes again and does not answer.
- **STU-010.** The Offertory's history of wording is told in full twice.
- **STU-011.** St Bernard's sermons for All Saints, the first of which
  expounds this Gospel's beatitudes, were not read because nothing was
  registered. A registry gap is not a search result: look for a lawful text
  (PL 183, or an English translation before 1931).
- **STU-012.** "(Super Matt. 5, with Chrysostom)" needs a finer locus and a
  plain account of what Aquinas quotes from Chrysostom.

## Points where later revisions went wrong

Cold audits on 27 October found these in study text written after
iteration 1. That text has been removed, but the same loci will come up
again.

- **Fromage on the Communion.** *L'Année liturgique* vol. 15
  (`ia-djvu-text-6301674b`, lines 8479–8484) gives a reason for the three
  beatitudes: the antiphon cannot list the whole series again, so it recalls
  the last three, and in doing so brings all of them to the Sacrament in which
  they are nourished. Do not say the sources are silent, and do not put an
  English phrase in quotation marks that is not in a source; the text is
  French.
- **Victorinus on 7:2.** He does speak of the number at 7:2 and joins it to
  the multitude (above). He calls Elias the precursor "of the times of
  Antichrist, for the restoration and establishment of the churches from the
  great and intolerable persecution" (lines 33568–33570). His remark that one
  must not look for order in the Apocalypse (lines 33604–33613) concerns the
  trumpets and the phials; applying it to the sealing is an inference and must
  be marked as one.
- **Bellarmine on Ps 33:10–11** (`historical-text-357551e1`, lines
  1201–1203) says that to feel no want is the essence of perfection, and that
  those who cling to the Supreme Good possess all good. He says nothing of the
  vision of God or of the Communion, and he keeps a humbler temporal sense.
- **Aquinas, *Super Matt.* 5, in the Venice printing of 1745.** No lecture
  heading appears near the locus (OCR line 10412). Cite the page and column of
  the printing read, or verify a lecture number in a printing that has one.
- **Hilary on the beatitudes** (PL 9). The contrast with Augustine is the
  change by immortality ("nisi spiritu perfecti, et immortalitate
  immutati"). The phrase at col. 934 reads "in paternae scilicet majestatis";
  do not drop *scilicet* without an ellipsis (STU-014).
- **Six orations, not seven** (05 L22 and 90 L37; SYN-002).
- **Cyprian** (ANF V, `a02b61c3`): "the Christian martyrs cannot be
  numbered" introduces his quotation of the Apocalypse rather than concluding
  from it. Keep him out of the middle of a paragraph about Bede.
- **Augustine on Ps 118:109.** NPNF reads "My soul is alway in Thy hand"; the
  Douay reads "continually in my hands". Do not mix them.
- **Register.** Production words such as "witness", "carry", "the
  continuation" and "among the witnesses read"; a sentence repeated verbatim
  in two sections; a fixed formula ("Read together") used three times; long
  gathering paragraphs that string one-line glosses on many texts.

## Research leads

Rebuild the research from the sources. These are the places the earlier
research went wrong or left gaps.

1. **Victorinus.** `src/sources/inventories/source-containment-v1.toml`
   (the Victorinus constituent, around line 3621) bounds his extent at Rev 1,
   5 and 19. That bound produced the false negative behind STU-001. Read the
   commentary at chapters 7 and 12 yourself; do not let the inventory stand in
   for the text.
2. **The 1570 Offertory.** In `missale-romanum-1570-text-563f4dd2` the All
   Saints Offertory (from line 71705) reads *tormentum mortis* with no
   *alleluia*. Lines 62448 and 68676–68680 belong to other Masses. Find
   witnessed evidence for when *malitiae* and the *alleluia* entered this
   Offertory (the earlier research found the *alleluia* first in Mame 1922 of
   the printings it read), or record the history as unresolved.
3. **The Offertory against Wis 3:1–3** (Clementine). The antiphon omits
   *autem*, reads *tanget* for *tangent* and *malitiae* for *mortis*, omits
   3:2b–3a and adds *alleluia*. Check this collation yourself.
4. **Psalm 33 numbering.** NPNF's Augustine numbers from the Hebrew (its
   9–11 are Vulgate 10–12); Bellarmine's English is not Vulgate either (his
   9–10 are Vulgate 10–11). Vulgate 33:12, "Venite, filii", is not said in
   the Gradual. State the basis of every psalm citation.
5. **Pustet 1862.** The tracked extract
   `pentecost-23-prayer-pages-7e6ef53b` holds the commemoration's orations.
   Read it and bind it with a fingerprint, or report no Pustet reading.
6. **Mame 1922 forms** are *Juda*, *justitiam*, *Justorum*.
7. **Bede on 7:9** first reads the multitude as those who overcome the last
   persecution, and gives the Gentiles joined to the Church as an alternative.
   Report his order.
8. **Chronology sources.** The corpus is `src/sources/chronology/`. Name the
   sources the generated rows actually cite (the Catholic Encyclopedia
   articles, Haydock's report of Ussher, the NABRE Psalms introduction) and
   inspect each passage used.
9. **Lasance orations.** The English of the four own orations and the
   commemoration's three rests on the Lasance passages and the derivative
   artifacts `…resume-orations-core193-2026-10-23-0736f65f` and
   `…resume-orations-phase2-2026-10-23-5a4e83f7`. Bind them or declare them
   in `research/review-dependencies.toml`, so the seal covers them.
10. **Dated web witnesses.** The ICRSP, FSSP and FSSPX ordos, the Missale
    Meum page and Murphy 1960 are registered as context-only restricted
    witnesses. Re-read whatever you rely on and reconcile it; the Divinum
    Officium response was an access-block page.
11. **The Preface.** The registered rubrical sources did not settle Trinity
    (no. 1082) against the common Preface (no. 1086). Unless a registered
    authority settles it, name both candidates with their rubrical basis and
    assert neither.
12. **Augustine in the first reading.** His "one nation of the heavenly city"
    comes from Ps 32:12, which the Mass does not say, and the Gradual gloss
    on the Living Bread comes from his comment on a half-verse the Gradual
    omits.
13. **Who carries each reading.** `proper-components.toml`'s
    `carrying_authors` must agree with `research/interpretations.md`.
    Supporting reception is not carrying (RES-019, SYN-001).
14. **The anonymous *Expositio in Apocalypsim* in PL 35** (Homily VI begins
    at col. 2425 on Apoc 7:2; cols. 2426–2428 treat the 144,000 and the
    multitude). The excerpt registered for it earlier was removed. If you use
    the text, register what you read from the tracked parent
    `internet-archive-google-pdf-b3ff8a95`, with col. 2425 among its loci.
15. **Bernard** (STU-011 above).
16. **Records.** Keep machine paths and scratch locations out of tracked
    records; point every cross-reference at the section that carries the
    material.

## The concise study and the homily

Cold audits of the removed versions found these. They are guides to the
sources, not to the removed text.

- **Concise study.** Production vocabulary and repeated inference formulas
  through the commentary; the apparatus listing supporting authors among
  those who carry a reading, against the study's comparison; a page
  cross-reference to the wrong page; the Postcommunion said to join the
  Introit's joy to the Collect's "defence", where the Collect asks for
  intercession; Themes pages that string authorities with one-line verdicts
  and have no thesis.
- **The number of the saved.** Apoc 7:9 says no *man* could number the
  multitude. The Missal's oration says "Deus, cui soli cognitus est numerus
  electorum", and Aquinas (*ST* I q.23 a.7) that the number of the
  predestined is certain to God. Augustine, Sermon LXI (NPNF I.6), says the
  few are few "in comparison of the lost" and many "in the society of the
  Angels". Do not say they cannot be counted in God's sight.
- **Augustine's "mass".** In Sermon LXI the "great mass" is the heap of grain
  on the threshing floor that fills the barn of heaven. Spoken at Mass
  without the image, the word is heard as the liturgy.
- **Durandus** (*Rationale* VII.34) gives the supplying of omitted feasts as
  the second of four causes of the feast, not the only one.
- **Augustine on the eighth beatitude** says it returns to the starting
  point because it shows and commends what is complete and perfect.
- **Chrysostom** (*Hom. in Matt.* 15): mark any omission within a quotation.
- **The homily's note** must describe what the speech uses, including any use
  of Augustine's comment on the half-verse of Ps 33:11 that the Gradual omits,
  and its Douay references must list only loci quoted from the Douay.
- **Speech.** Credentials and dates belong in the note; one idea a sentence
  and one step a paragraph; no closing maxims, refrains or restatement; put
  the governing question to the hearer once, near the opening, and leave out
  stops that do not advance the answer.

## Layout

- The study's last page held only the rights colophon.
- The study's element map split 13 rows to 1 across pages 3 and 4.
- The generated chronology notes repeated their row labels as their first
  words, and the passage column printed "Revelation" where the documents say
  "Apoc". These come from the chronology record and its generator.
- Running heads take the first mark on a page. That is the shared style, not
  this leaf's to change.

## Left for other owners

These stood after the first run. No stage of this run owns them; do not
change them mid-run.

- `propers.yaml` `omnium-sanctorum` ranges run wider than the said text, and
  there is no Preface case.
- `tools/tests/test_ordinary_appointments.py` (`allSaintsSunday1962`)
  asserts the common Preface.
- The Latin-provenance, translations and formulary-loci ledgers lack rows for
  this formulary.
- `author-standing-v1.toml` lacks Bernard, Victorinus, Cyprian, Gregory of
  Nyssa, Alphonsus, Athanasius, Peter of Celle and Murphy.
- `work.fsspx.ordo` declares English; its responses are French.
- Bede's *Explanatio Apocalypsis* has no passage records for Apoc 7:2–3.
