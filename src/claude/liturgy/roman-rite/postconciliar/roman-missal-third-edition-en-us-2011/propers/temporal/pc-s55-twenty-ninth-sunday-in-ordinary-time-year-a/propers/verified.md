# `PC-S55-A` — Target Composition Audit (Claude edition)

**Formula:** `PC-S55-A`, Twenty-ninth Sunday in Ordinary Time, Year A
**Canonical Missal owner:** [Ordinary Time Week XXIX](../../shared/ordinary-time/weeks/29/propers/verified.md)
**Identity record:** [`instance/manifest.md`](../instance/manifest.md)
**Collated:** 2026-10-16; revised the same day for the `proper-study` v12 revision (run `821c824684b0c7a7`), whose changes are marked *Revision*
**Provider:** Anthropic Claude

This record verifies the composition of the target: which units make up this
Mass, in what order, with what boundaries, branches and rights dispositions.
The Missal formulary's witnesses, locators, incipits and variation check belong
to the owner and are not restated. The Lectionary witnesses, with their hashes
and page locators, were collated at context resolution and are recorded in
[`research/context.md`](../research/context.md); this record states what the
research stage itself re-checked.

## What this stage checked, and what it relied on

| Matter | Basis |
| --- | --- |
| Sunday, cycle, occurrence, Lectionary no. 145 and every reading boundary | Re-collated at the research stage from bytes fetched whole over verified TLS on 2026-10-16 and matched to their registered hashes before reading: the USCCB 2026 calendar at printed pp. 5 and 41 (artifact pp. 7 and 43), and the *Ordo lectionum Missae* 1981 no. 145 on a page image of printed p. 79 (artifact p. 133) rendered at 200 dpi. The dated readings page for 18 October 2026 was fetched again (58,047 bytes, SHA-256 `369f06fd…`); its bytes differ from both the context stage's copy and the state registered on 2026-10-13, so this state was registered and read: heading, Lectionary no. 145, every locator, the response locator (7b) and the five units agree with `research/context.md`. All are bound in `research/source-bindings.toml`. *Revision:* the official readings page refused every direct request of 16 October 2026 (HTTP 403 challenge page), so the revision read it whole in the Internet Archive capture of 15 March 2026 (60,138 bytes, `f20f2e3c…`), now registered and bound; heading, Lectionary 145, every locator, the response locator, the four strophes (v. 8 whole; v. 10 first and last clauses) and the copyright notice agree with the state above and with the *Ordo* |
| Missal elements, order, *Vel:* structure, absent units, conclusions | The Week XXIX owner. Re-read at the research stage in the 2002 Latin at physical PDF pp. 291–292 (text layer) and in the ICEL excerpt at printed p. 81 (artifact p. 89, text layer); nothing differs from the owner's table. The owner's additions of this date record the passage records, the oration antecedents and the antiphons' comparison with the *Nova Vulgata* |
| Precedence and the omitted feast | `research/context.md`, whose loci in the 2002 artifact (*Normae universales* nos. 58–60, pp. 70–71; the *Calendarium Romanum generale*, p. 79) are bound to it. Not re-read at this stage |
| Chant and branch rubrics | The governing United States English GIRM. *Revision:* chapter II was re-read directly by the revision's context stage on 16 October 2026 and is byte-identical to its registered state (nos. 48, 51, 53, 61, 62, 63, 66, 68, 74 and 87). Chapters VII and VIII refused direct requests that day; the revision's research read them whole in Internet Archive captures of the official pages of 13 and 18 June 2026 (chapter VII nos. 357–367, relied on at 363–365; chapter VIII nos. 368–378, relied on at 372–374), registered and bound in `research/source-bindings.toml`. The states the first context stage read on 16 October could not be re-read by any later stage and are kept only as catalogued records. The Latin typical rules read in the 2002 Missal (*Tempus per annum* rubrics 3–6; Masses for Various Needs, introduction no. 2 and no. 18, physical pp. 667 and 695, re-read by the revision's research) carry the same branch rows where they exist |
| Study-text boundaries | Re-read at this stage in the tracked Douay–Rheims (Challoner) and Clementine Vulgate at Isaiah 44:24–45:13; Psalm 95 whole; Psalm 16 whole; Psalm 32:12–22; 1 Thessalonians 1:1–10; Philippians 2:14–16; Matthew 21:23, 21:45–46 and 22:15–23; Mark 10:42–45; and Acts 17:1–10 |
| Lectionary Latin | The *Nova Vulgata* as published on the Holy See's site, read at Isaiah 44:24–45:13, Psalms 17 (16), 33 (32) and 96 (95), Matthew 22:14–23, Mark 10:42–46, Philippians 2:12–18 and 1 Thessalonians 1:1–10, in web states fetched whole on 2026-10-16, not registered and not retained (sizes and SHA-256 values in `research/scope.md` section 5) |
| Greek and Hebrew controls | The SBL Greek New Testament text and apparatus of Matthew and Mark, fetched whole and matched to their registered hashes, read at Matthew 22:15–21 and Mark 10:45; the same edition's 1 Thessalonians and Philippians files, fetched from the same commit and not registered, at 1 Thessalonians 1:1–5 and Philippians 2:15–16; Swete's Septuagint Psalms (tracked digitisation) at Psalm 95:1, 5, 7 and 10; Brenton's English Septuagint (tracked) at Isaiah 45:1–6; the King James Version (tracked) for the Hebrew-based reading at Isaiah 45:1, 4–5 and Psalms 17:6–8 and 96:5, 7, 10. No Hebrew or Greek text of Isaiah was read in the original language |
| Citation encoding | Every citation below was passed through `tools/tpt proper-chronology`, which parses it with `tools/citations` and returned its book, chapter and verse ranges with partial-verse letters intact |

## Ordered textual units

| Order | Key | Unit and boundary | Status | Rights disposition |
| --- | --- | --- | --- | --- |
| 1 | `entrance-antiphon` | *Ego clamavi, quoniam exaudisti me, Deus*. Psalm 16 (Hebrew 17):6 and 8, printed with `Cf.`: v. 6 without *mihi*, v. 7 passed over, v. 8 without its opening *A resistentibus dexterae tuae* and with the vocative *Domine* added after *Custodi me* (owner finding 1) | required | Latin incipit and original description only. Douay–Rheims Psalm 16:6, 8 may stand beside it as its identified scriptural source, labelled as such and with the Missal's departures stated; no English is composed for the antiphon or its vocative |
| 2 | `collect` | *Omnipotens sempiterne Deus, fac nos tibi semper*; long conclusion | required | Latin incipit and original description only; see `research/scope.md` section 9 on the early witness |
| 3 | `first-reading` | Isaiah 45:1, 4–6; vv. 2–3 omitted between the segments | required | Douay–Rheims (Challoner), public domain, labelled as study text; the omission marked, never closed up |
| 4 | `responsorial-psalm` | Psalm 96 (95):1 and 3, 4–5, 7–8, 9–10a and 10c; response from v. 7b | required | Douay–Rheims at Psalm 95. Verse 2 and v. 6 marked as not sung, v. 10 shown with its middle clause as context; the title standing within v. 1 is not part of the first strophe; finding 2 governs how the United States response stands to v. 7b |
| 5 | `second-reading` | 1 Thessalonians 1:1–5b; the rest of v. 5 marked as context | required | Douay–Rheims; in that version the greeting stands at the start of v. 2 |
| 6 | `acclamation` | Alleluia verse, Philippians 2:15d, 16a, without `Cf.` | required | Philippians 2:15–16 in Douay–Rheims with 15d and 16a marked; finding 3 governs the English mood; no English is composed for the verse |
| 7 | `gospel` | Matthew 22:15–21 | required | Douay–Rheims |
| 8 | `prayer-over-offerings` | *Tribue nos, Domine, quaesumus, donis tuis*; short conclusion | required | Latin incipit and original description only |
| 9a | `communion-antiphon-a` | `Cf.` Psalm 33 (32):18–19 | appointed alternative | Douay–Rheims at Psalm 32:18–19 beside a description of the Missal's departure (owner finding 2); no English is composed for the antiphon |
| 9b | `communion-antiphon-b` | Mark 10:45, its second half, without *Nam et* and the contrast of service; printed without `Cf.` | appointed alternative | Douay–Rheims at Mark 10:45 as its identified source, with the departures described (owner finding 3); no English is composed for the antiphon |
| 10 | `prayer-after-communion` | *Fac nos, quaesumus, Domine, caelestium rerum*; short conclusion | required | Latin incipit and original description only |

No Offertory antiphon, Sequence, proper Preface, proper Eucharistic Prayer
insert, prayer over the people or solemn blessing is appointed. The approved
United States English of the Missal and of the Lectionary is reproduced nowhere
in this leaf.

## Findings of this stage

1. **Isaiah 45:1 and 45:4: which Latin the Lectionary follows.** The
   *Ordo*'s incipit, read on the page image, is *Haec dicit Dominus de uncto
   meo Cyro*. The *Nova Vulgata* (web state of 2026-10-16) reads *de uncto suo
   Cyro*; the Clementine reads *christo meo Cyro*; Brenton's English of the
   Septuagint reads "to my anointed Cyrus"; the King James Version, from the
   Hebrew, "to his anointed, to Cyrus". The *Ordo*'s incipit therefore joins
   the *Nova Vulgata*'s noun (*unctus*, not the transliterated *christus*) with
   the possessive of the Clementine and the Septuagint (*meo*, not *suo*).
   Whether the *Nova Vulgata* state of 1979 that the 1981 *Ordo* used read
   *meo* was not established; no printed *Nova Vulgata* was read. The *Ordo*'s
   titulus, *Apprehendi dexteram Cyri ut subiciam ante faciem eius gentes*,
   condenses v. 1 in the wording of both Latin texts with the relative pronoun
   replaced by the name. In v. 4 the *Nova Vulgata* reads *designavi te*
   (Hebrew-based: King James "I have surnamed thee"), the Clementine
   *assimilavi te* (Douay–Rheims "I have made a likeness of thee"), and
   Brenton's Septuagint "and accept thee"; the dated USCCB page, described
   and not transcribed, follows the sense of the Hebrew. Two Fathers turn on
   the Clementine wording of v. 4 (`research/scope.md` section 3.2), so the
   studies must say which text a Father read whenever his argument rests on
   *assimilavi*. No Hebrew or Greek of Isaiah was read in the original.
2. **Psalm 96 (95): the response, v. 5 and v. 10.** The *Ordo* prints the
   response *Afferte Domino gloriam et potentiam* (7b), which is the *Nova
   Vulgata*'s wording of v. 7b (*gloriam et potentiam*), close to the
   Hebrew-based "glory and strength"; the Clementine, the Douay–Rheims and
   Swete's Septuagint (δόξαν καὶ τιμήν) have glory and honour. The dated
   USCCB page, described, gives a response naming glory and honour while its
   own third strophe renders v. 7b with a different second noun, and it
   attributes its psalm refrain to ICEL. The United States response is
   therefore a refrain that does not reproduce the *Ordo*'s Latin of v. 7b,
   and no claim may rest on the second noun of the response. In v. 5 the
   *Nova Vulgata* reads *inania* (the Hebrew-based "idols", the dated page's
   "things of nought"), the Clementine *daemonia*, the Septuagint δαιμόνια
   and the Douay–Rheims "devils"; Augustine and Bellarmine expound the
   Clementine form (`research/scope.md` section 3.3). In v. 10 neither Latin
   text, Swete's Greek nor the King James Version reads "from the wood"; the
   Old Latin form *Dominus regnavit a ligno* is the text Augustine expounds
   (NPNF, *En. in Ps.* 95.2 and 11), and the NPNF note reports it in Justin
   Martyr. No study may present "from the wood" as the appointed verse.
   The *Ordo*'s locator `9-10a et c` and the dated page's `9-10` describe the
   same sung text (finding of `research/context.md`). The Clementine and the
   Douay–Rheims print the psalm's title, *Canticum ipsi David, quando domus
   aedificabatur post captivitatem*, inside v. 1; the *Nova Vulgata* prints
   no title; the title is not sung.
3. **Philippians 2:15d, 16a: the mood of the verse.** The *Ordo*'s verse,
   read on the page image, is *Lucetis sicut luminaria in mundo, verbum vitae
   continentes*: the Clementine's cola without *inter quos*, indicative, with
   *continentes*. The *Nova Vulgata* reads *lucetis … verbum vitae firmiter
   tenentes*. The Greek (SBL) has φαίνεσθε, a form that is the same in the
   indicative and the imperative, inside a relative clause, and ἐπέχοντες,
   which can mean holding fast or holding out. The dated USCCB page,
   described, phrases the verse as an exhortation to shine and to hold on to
   the word of life. The United States verse is therefore a rendering of the
   Greek's possible sense in the form of an acclamation, not an adaptation of
   the Latin, and no `Cf.` is printed; but no claim may rest on the mood of
   the English verb, and the Douay–Rheims ("you shine … holding forth") is
   shown as the study text with that difference stated.
4. **1 Thessalonians 1:1–5b.** The SBL apparatus records the Byzantine
   addition "from God our Father and the Lord Jesus Christ" after the
   greeting of v. 1 (absent from the Clementine and the *Nova Vulgata*), the
   article before θεοῦ in v. 4, and ἐν before πληροφορίᾳ in v. 5; none
   changes the sense of the appointment. The *Ordo*'s titulus, *Memores fidei
   vestrae et caritatis et spei*, condenses v. 3; the Clementine and the
   *Nova Vulgata* both read *memores operis fidei vestrae*. The reading ends
   with "in much fullness" (Douay–Rheims; Clementine *in plenitudine multa*;
   Greek πληροφορίᾳ πολλῇ); the clause on what manner of men the
   missionaries were (5c) is context. No study may cite 5c, or 1:6–10, as part
   of this Sunday's reading.
5. **Matthew 22:15–21: the text.** The SBL apparatus records only λέγοντες
   against λέγοντας (v. 16) and the omission of αὐτῷ by Westcott–Hort (v. 21);
   the Clementine and the *Nova Vulgata* differ only in *videtur*/*videatur*,
   *numisma*/*nomisma* and the Clementine's *Jesus* in v. 20. The *Ordo* opens
   with *In illo tempore: Abeuntes pharisaei* and names Jesus in v. 15. The
   coin is a denarius in every text read (δηνάριον, *denarium*, "a penny"),
   called "the coin of the tribute" (νόμισμα τοῦ κήνσου); the question is
   whether it is lawful to give the census (κῆνσον, *censum*) to Caesar. No
   manuscript was examined.
6. **Entrance antiphon.** The owner's finding 1 and its addition 5 govern:
   the antiphon follows the Clementine wording of Psalm 16:6 without *mihi*
   and of v. 8 without its opening phrase, adding *Domine*; the *Nova
   Vulgata* reads *Ego ad te clamavi, quoniam exaudis me* and gives the clause
   on those who resist God's right hand to v. 7. The chronology input records
   the Missal's printed locator as an `adaptation` in Vulgate numbering.
7. **Communion antiphon A.** The owner's finding 2 and addition 5 govern:
   Vulgate Psalm 32:18–19 with `Cf.`, Hebrew 33:18–19, *timentes* where both
   the Clementine and the *Nova Vulgata* have *metuentes*. Verse 16, the king
   not saved by much strength, is context and not part of the antiphon.
8. **Communion antiphon B.** The owner's finding 3 and additions 5 and 6 govern: the
   second half of Mark 10:45, printed without `Cf.`; recorded as an
   `adaptation`. Verses 42–44, on the rulers of the gentiles who lord it over
   them, are context and not part of the antiphon. At no. 146 the *Ordo*
   gives Mark 10:45 as the Year B acclamation verse with the clause of service
   (*ut ministraret*) that the Missal antiphon omits.

**Which conclusions rest on the *Nova Vulgata* delivery alone.** The *Nova
Vulgata* books were read in the Holy See's web delivery, recorded by size and
SHA-256 in `research/scope.md` section 5, neither registered nor bound. The
following stand on bound evidence without it: the Lectionary's *de uncto meo
Cyro* in the *Ordo*'s incipit, the *Ordo*'s response *Afferte Domino gloriam
et potentiam* and its verse *Lucetis sicut luminaria in mundo, verbum vitae
continentes* (the bound *Ordo* passage record and page image); the absence of
"likeness" at Isaiah 45:4 in the Hebrew-based King James ("I have surnamed
thee"), Brenton's Septuagint ("accept thee") and the bound dated USCCB page,
which is what limits the use of Jerome's *assimilavi* typology; the
Clementine, Douay–Rheims, Swete and King James readings of Psalm 95/96:5, 7
and 10; and the antiphons' departures from the Clementine (owner findings
1–3). The following rest on the unregistered delivery alone and are reported
as its readings, not as sealed evidence: *de uncto suo Cyro* and *designavi
te* as the *Nova Vulgata*'s words; *inania* at Psalm 95:5; the absence of a
title in the *Nova Vulgata* psalm; *firmiter tenentes* at Philippians 2:16;
and every comparison of an antiphon with the *Nova Vulgata* (findings 6–7 and
the owner's addition 5).

## Relationship classes

| Relation | Class | Authority |
| --- | --- | --- |
| First reading ↔ Gospel | `officially correlated` | *Praenotanda* 1981, nos. 105–107; no. 106 says the relation between the readings of one Mass is shown by the careful choice of the tituli set over them. At no. 145 the *Ordo* heads the first reading with Isaiah 45:1, *Apprehendi dexteram Cyri ut subiciam ante faciem eius gentes*, and the Gospel with Matthew 22:21, *Reddite quae sunt Caesaris Caesari, et quae sunt Dei Deo*: each titulus names a gentile ruler |
| Second reading, the *Ordo*'s emphasis | `semi-continuous` | Headed *Memores fidei vestrae et caritatis et spei* (1 Thessalonians 1:3, condensed). The three tituli are edition-controlled evidence of what the Lectionary singles out in each reading and of the one official correlation; they are not evidence of a whole-formulary design |
| Psalm → first reading | `responsorial` | GIRM 61 |
| Alleluia verse → Gospel | `acclamatory` | GIRM 62 |
| Second reading; Gospel | each `semi-continuous`; this is the first Sunday of the five-Sunday 1 Thessalonians course of Year A (*Tabella II*), and the Gospel's course runs from Matthew 22:1–14 on 11 October to 22:34–40 on 25 October | *Praenotanda* 1981, no. 107 and *Tabella II*; national calendar |
| Missal antiphons and orations ↔ Year A readings | `source-grounded synthesis`, `documented reception` or `editorial or AI proposal`, labelled case by case in `research/interpretations.md` | The week's Missal texts serve all three cycles; Communion antiphon B is drawn from the Year B Gospel (`research/context.md`) |
| Recurrence of the vocabulary of serving, rendering and gifts, of image and likeness, of the nations and their rulers, of seeing and knowing, and of sincerity and hypocrisy across units | `textual observation` | The texts themselves (Douay–Rheims and Clementine); `research/scope.md` section 2 lists them. No source consulted states a design |

## Branches

The twelve branch IDs of `instance/manifest.md` apply unchanged. *Revision:*
`mass-for-evangelization-of-peoples` remains `conditional` and unselected. Its
rubric's condition can be met on 18 October 2026, the 100th World Mission Day
(Holy See message and video message; the Pontifical Mission Societies in the
United States for World Mission Sunday and its collection, all registered and
bound), but the rubric permits that Mass and no witness appoints it; the
observance adds no unit, branch or relationship to this target. Statuses,
authorities and resolutions are those tabulated in `research/context.md`; no
selection was supplied and none is inferred. For the Communion pair, every
claim resting on one antiphon only is marked with that antiphon. A claim
resting on an antiphon's wording does not hold where a sung substitute
replaces it (`entrance-or-communion-chant-substitution`).

## Outstanding

The printed United States Lectionary at the psalm response (finding 2) and at
the whole of no. 145, which was not inspected; the *Nova Vulgata* of 1979 at
Isaiah 45:1 (finding 1); the Hebrew and Greek of Isaiah 45 in the original
languages; manuscript evidence for Matthew 22:15–21 beyond the editions'
apparatus; a direct official delivery of GIRM chapters VII and VIII and of the
readings page on or after 16 October 2026, which the publisher's challenge
page prevented (the archived captures of June and March 2026 stand in for
them); independent review of this audit.
