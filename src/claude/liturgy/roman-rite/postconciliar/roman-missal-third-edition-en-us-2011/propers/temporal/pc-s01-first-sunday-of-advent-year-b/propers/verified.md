# `PC-S01-B` — Target Composition Audit (Claude edition)

**Formula:** `PC-S01-B`, First Sunday of Advent, Year B
**Canonical Missal owner:** [First Sunday of Advent](../../shared/formularies/pc-s01-first-sunday-of-advent/propers/verified.md)
**Identity record:** [`instance/manifest.md`](../instance/manifest.md)
**Collated:** 2026-11-26, research stage of the `proper-study` v20 production, run `99f04ef5cf9b711b`; the relationship row *Psalm to first reading* corrected at the research stage's second iteration the same day, after a re-reading of the *Nova Vulgata* Isaiah 63:15–17 and Psalm 79 (80), the readings page, Jerome at PL 24 cols. 648–649 and Aquinas at [85023], and restated at its third iteration, after Jerome at PL 24 cols. 642–644 and 649 (page images) and Aquinas at [85023] were read again for what each does with the two petitions
**Provider:** Anthropic Claude

This record verifies the composition of the target: which units make up this
Mass, in what order, with what boundaries, branches and rights dispositions.
The Missal formulary's witnesses, locators, incipits and variation check belong
to the owner and are not restated. The Lectionary witnesses, with their hashes
and page locators, were collated at context resolution and are recorded in
[`research/context.md`](../research/context.md); this record states what the
research stage itself re-checked and settled.

## What this stage checked, and what it relied on

| Matter | Basis |
| --- | --- |
| Sunday, cycle, occurrence, Lectionary no. 2 and every reading boundary | `research/context.md`, whose downloads the research stage re-hashed before relying on them: the 2026 and 2027 national calendars (`4bd9add0…`, `d7997b57…`), the 2002 Missal (`0b458944…`), the 1981 *Ordo* (`ed4bc14e…`), the *Notitiae* issue (`74c8d174…`), the ICEL excerpt (`e6b82741…`) and the readings page in its state of 26 November 2026 (`7e0b44c0…`, 56,311 bytes; registered at source registration as `…2026-11-26-page-for-2026-11-29.lectionary-2-7e0b44c0`), all matching. The readings page's first reading and psalm were read again at this stage for the two citation questions below; its wording is described, not transcribed |
| Missal elements, order, rubrics, conclusions | The owner. The research stage re-read the Latin of the formulary in the text layer of the 2002 artifact (pp. 82–83), the Preface (p. 311) and nothing else of the Missal; nothing differs from the owner's table. The research stage's additions to the owner (findings 5–8) record the antiphons against the *Nova Vulgata* and the early witnesses of the Collect, the Prayer over the Offerings, the Prayer after Communion and the Preface |
| Chant and branch rubrics | `research/context.md` and the General Instruction states listed there; not re-read at this stage. The `advent-wreath-blessing` lead was read at this stage (Branches) |
| Study-text boundaries | Re-read at this stage in the tracked Douay–Rheims (Challoner) at Isaiah 63:15–64:12, 1 Corinthians 1:1–10 and Mark 13:28–37, and in the tracked King James Version at Psalm 80:14–17 (its 80:13–16 numbering one lower) |
| Lectionary Latin | The *Nova Vulgata* as published on the Holy See's site: the book of Isaiah (web state of 26 November 2026, 204,149 bytes, SHA-256 `9c9c78c4…`; registered at source registration as `…liber-isaiae-9c9c78c4`) at 63:15–65:5, and the Psalter (web state of the same date, 269,126 bytes, byte-identical to the registered state `…liber-psalmorum-e508ed1c`) at Psalms 25 (24), 80 (79) and 85 (84) whole |
| Approved English translation tradition | The *New American Bible, Revised Edition* on the USCCB site, Isaiah 64 with its notes (web state of 26 November 2026, 58,899 bytes, SHA-256 `35573e1b…`; registered at source registration as `…english-usccb-web-2026-11-26.isaiah-64-35573e1b`). Isaiah 63 refused the same day (HTTP 403, a 15,748-byte challenge page). The NABRE is the bishops' current Bible, not the Lectionary's 1970 Old Testament translation, which was not read; it is used only for what its translators' note says about the Hebrew of 64:2 |

## Ordered textual units

| Order | Key | Unit and boundary | Status | Rights disposition |
| --- | --- | --- | --- | --- |
| 1 | `entrance-antiphon` | *Ad te levavi animam meam*. Psalm 24 (Hebrew 25):1–3, printed with `Cf.` (owner findings 1 and 5) | required | Latin incipit and original description only. Douay–Rheims Psalm 24:1–3 may stand beside it as its identified scriptural source, labelled as such, the title excluded and the departures stated; no English is composed for the antiphon |
| 2 | `collect` | *Da, quaesumus, omnipotens Deus, hanc tuis fidelibus voluntatem*; long conclusion | required | Latin incipit and original description only (owner finding 6 for the early witness) |
| 3 | `first-reading` | Isaiah 63:16b–17, 19b; 64:2b–7 (*Ordo*); 63:16b–17, 19b; 64:2–7 (United States witnesses); one form, three segments. Douay–Rheims and Clementine numbering: 63:16b–17; 64:1, 3–8 (finding 1) | required | Douay–Rheims (Challoner), public domain, labelled as study text. Shown as Douay 63:16b–17; 64:1; 64:3–8, with 63:16a and the second half of each partial verse marked as context, 63:18–19 and 64:2 marked as omitted segments, and 64:3 (Hebrew 64:2) shown whole with the note of finding 1. Every citation gives both numberings |
| 4 | `responsorial-psalm` | Psalm 80 (79):2a, 2c, 3b, 15–16, 18–19; response v. 4 (finding 2) | required | Douay–Rheims at Psalm 79. The title (v. 1), v. 2b, v. 3a, vv. 4–14 (v. 4 except as the response) and v. 17 marked as not sung; no English is composed for the response |
| 5 | `second-reading` | 1 Corinthians 1:3–9 | required | Douay–Rheims |
| 6 | `acclamation` | Alleluia verse, Psalm 85 (84):8, without `Cf.` | required | Douay–Rheims Psalm 84:8; no English is composed for the verse |
| 7 | `gospel` | Mark 13:33–37 | required | Douay–Rheims |
| 8 | `prayer-over-offerings` | *Suscipe, quaesumus, Domine, munera*; short conclusion | required | Latin incipit and original description only (owner finding 7) |
| 9 | `preface` | Preface I of Advent, *De duobus adventibus Christi* | required | Latin incipit and original description only (owner finding 8) |
| 10 | `communion-antiphon` | *Dominus dabit benignitatem*. Psalm 84 (Hebrew 85):13 without its opening *Etenim*, printed without `Cf.` (owner findings 2 and 5) | required | Douay–Rheims Psalm 84:13 as its identified source, with the departure stated; no English is composed for the antiphon |
| 11 | `prayer-after-communion` | *Prosint nobis, quaesumus, Domine, frequentata mysteria*; short conclusion | required | Latin incipit and original description only (owner finding 7) |
| 12 | `solemn-blessing` | Solemn blessing *In Adventu*: three invocations and the Trinitarian blessing | optional | Latin incipit and original description only |

No Offertory antiphon, Sequence, proper Eucharistic Prayer insert, prayer over
the people, second Communion antiphon or reading alternative is appointed. The
approved United States English of the Missal and of the Lectionary is
reproduced nowhere in this leaf.

## Findings of this stage

1. **Isaiah 64:2: the United States text and the *Ordo* read different
   members of one verse.** The *Nova Vulgata* (web state above) prints Isaiah
   63:19 in two members, the second being the cry *Utinam dirumperes caelos et
   descenderes! A facie tua montes defluerent*, and 64:2 in two members: *cum
   feceris mirabilia, quae non sperabamus* and *Descendisti, et a facie tua
   montes defluxerunt*. The *Ordo* begins the last segment at 64:2b, so its
   Latin reading has the mountains flowing at 63:19b and again, as done, at
   64:2b. The readings page for 29 November 2026 (state `7e0b44c0…`) cites
   64:2–7; in its text, after the cry to rend the heavens, the quaking of the
   mountains stands once, followed by the clause of the awesome deeds not hoped
   for, which answers to 64:2a; nothing answers to *Descendisti*. The NABRE's
   note on 64:2 states that its translation omits words that the Hebrew repeats
   from 63:19. The two editions therefore differ in extent, not only in
   numbering: the *Ordo* reads 64:2b and not 64:2a; the United States text reads
   64:2a and leaves out 64:2b, whose words repeat 63:19b. Whether the
   Lectionary's own 1970 translation carries the same note was not
   established; the printed Lectionary was not read. *Praenotanda* no. 119
   (cited in `research/context.md`) lets vernacular editions follow the
   numbering of their approved version; it is consistent with the United
   States citation and does not by itself explain the different extent. The
   Clementine and the Douay–Rheims carry both members in their 64:3 (*Cum
   feceris mirabilia, non sustinebimus: descendisti, et a facie tua montes
   defluxerunt*; "When thou shalt do wonderful things, we shall not bear
   them: thou didst come down, and at thy presence the mountains melted
   away"). The study text shows Douay 64:3 whole and says which member each
   edition reads. Jerome and Aquinas both comment on *descendisti*
   (`research/scope.md` section 3.3); in the United States proclamation the
   answering *you came down* is not heard.
2. **Psalm 80: the locator and v. 16b.** The *Ordo* prints *Ps 79, 2ac et 3b.
   15-16. 18-19*; the readings page prints 80:2–3, 15–16, 18–19, and its first
   strophe gives only 2a, 2c and 3b, so the page's locator states more than it
   sings. The inventory follows the *Ordo*'s members. The *Ordo*'s response
   *Deus, converte nos, illustra faciem tuam, et salvi erimus* is the *Nova
   Vulgata*'s v. 4 word for word; the Clementine reads *ostende* for
   *illustra*. At v. 16 the *Nova Vulgata*, the Clementine and the Douay–Rheims
   end the verse with *et super filium hominis, quem confirmasti tibi* ("and
   upon the son of man whom thou hast confirmed for thyself"), the words that
   also end v. 18; the King James Version, translating the Hebrew, has "the
   branch that thou madest strong for thyself" in the corresponding verse (its
   80:15) and "the son of man" only in its 80:17. The readings page's second
   strophe ends with a line naming the son of man, so the United States psalm
   agrees here with the Latin tradition, not with the King James rendering.
   No Hebrew text was read; what the Hebrew word at v. 16b is was not verified
   in an original-language witness. Augustine and Bellarmine read the son of
   man of vv. 16 and 18 as Christ (`research/scope.md` section 3.4).
3. **The tituli.** The research stage confirms the context's reading of the
   *Ordo*'s three tituli against the *Nova Vulgata* where it was read: the first
   reading's titulus is the first half of *Nova Vulgata* 63:19b without the
   mountains clause. The second and Gospel tituli were compared with the
   Clementine only (`research/context.md`).
4. **The Book of Blessings lead** is resolved under Branches.

## Relationship classes

| Join | Class | Basis |
| --- | --- | --- |
| First reading, second reading and Gospel to the season and to this Sunday | seasonal or ritual | *Praenotanda* nos. 67 and 93 (`research/context.md`): in Advent the readings are composed for the season's character; the First Sunday's Gospel concerns the Lord's coming at the end of time; the Old Testament readings are prophecies of the Messiah and the messianic time; the apostolic readings give exhortations according to the season. None is semi-continuous |
| First reading to Gospel | no official correlation stated | The *Ordo* prints no titulus or rubric that pairs them; its tituli single out the plea for the Lord's descent, the waiting for Christ's revelation and the watch. A link between them is source-grounded synthesis at most |
| Psalm to first reading | responsorial | GIRM 61 (United States English, in the state cited by `research/context.md`). **The texts:** the two petitions are worded differently. The refrain (Psalm 80 (79):4, *Deus, converte nos*) asks God to turn *us*; the United States refrain asks the same. In the Hebrew-based Latin of the *Nova Vulgata*, Isaiah 63:17b (*Convertere propter servos tuos*) asks God himself to turn, that is, to return; the United States reading keeps a verb of returning. The psalm has Isaiah's own imperative at Psalm 80 (79):15, *Deus virtutum, convertere*, sung in the second strophe; the United States psalm renders that imperative adverbially (God is asked to look down again), so the shared verb is not heard in the English. These are textual observations. **The witnesses** read here do not keep the two petitions apart; both join them, on Latin texts. Jerome, on Isaiah 63:17 itself, reads the petition two ways: *Convertere, ait, Domine, sive converte nos propter servos tuos*, "Turn, he says, Lord, or turn us" (*In Isaiam* XVII, PL 24 col. 643, page image). He develops the second reading with the Septuagint's added clause: *Sive converte nos, ut, juxta Septuaginta, paululum possideamus montis sancti tui*, so that, having a part, we may come to its fullness and *contemplemur gloriam Unigeniti* (cols. 643–644). His lemma (col. 642) gives the verse from the Hebrew and from the Septuagint, and both of his Latin renderings read *convertere propter servos tuos*; *converte nos* is therefore Jerome's reading of the petition, not the wording of either text. Jerome also ties the refrain to this reading by quoting it, on Isaiah 64:7 (Vulgate; *Nova Vulgata* and Lectionary 64:6), where God has hidden his face: he answers with Psalm 79:4, *Ostende faciem tuam, et salvi erimus* (col. 649, page image). Aquinas, on the Vulgate's *convertere*, which he glosses *de ira ad misericordiam* as the people's petition for mercy, adduces together Psalm 89:13 (Hebrew 90:13), *convertere, domine*, and Lamentations 5:21, *converte nos, domine et convertemur* (*Super Isaiam* c. 63, [85023]): God's turning and his turning of us stand under the one petition. Neither witness quotes the refrain at 63:17; the words *converte nos* there are Jerome's alternative and Aquinas's Lamentations |
| Acclamation to Gospel | acclamatory | GIRM 62 |
| Preface to the Gospel and the second reading | textual observation | The Preface's closing clause speaks of those who wait watchfully now (*vigilantes nunc*) for the second coming; Mark 13:33–37 commands watching and 1 Corinthians 1:7 speaks of waiting for Christ's revelation. Shared vocabulary only; no witness joins them |
| Collect to Isaiah 64:4 (Hebrew; Douay 64:5) | textual observation | The Collect asks that the faithful go out to meet (*occurrentes*) Christ with righteous deeds; the *Nova Vulgata* says God meets (*Occurris*) the one who rejoices and does justice. The same verb and the same works, in opposite directions. No witness read joins them |
| Universal Norms 39 to the Preface | textual observation | Advent's double character (preparation for the remembrance of the first coming; minds turned to the second) and the Preface's two comings, in the Missal's own words |
| Every join among the Missal texts (shared by Years A, B and C) and the Year B readings | source-grounded synthesis or editorial or AI proposal | The three-document profile's rule for every formulary. `research/interpretations.md` labels each such join |

## Branches

The branch IDs and resolutions of `research/context.md` stand unchanged, with
one addition from this stage's reading:

| Branch ID | Authority and trigger | Status | Places affected | Resolution |
| --- | --- | --- | --- | --- |
| `advent-wreath-blessing` | *Book of Blessings* (ICEL; Collegeville: The Liturgical Press, 1989, as the transcription states), chapter on the blessing of an Advent wreath, nos. 1509–1520, read in the Catholic Culture transcription of 26 November 2026 (58,627 bytes, SHA-256 `25cf5943…`, registered at source registration as `…advent-wreath-html-25cf5943`; the registered state of 23 November, `…advent-wreath-html-6be75b4e`, differs and was not re-read). No. 1509 places the blessing on the First Sunday of Advent or the evening before; nos. 1517–1520 give an order within Mass in which, after the Gospel and homily, the general intercessions follow and the celebrant concludes them with the prayer of blessing; no. 1513 says that on the later Sundays the candles are lit before Mass or immediately before the opening prayer, without added rites | permitted | Universal Prayer (its conclusion) | Unselected. The rite adds a blessing; it replaces no proper text of this formulary and changes no reading. The printed ritual book was not read, so the documents cite it through the transcription and describe it only. No. 1527 lists Isaiah 63:16–17, 19; 64:2–7 among the readings of the order outside Mass: a documented reuse of this Sunday's first reading in the ritual book, not evidence about the Lectionary's choice |

## Outstanding

The printed United States Lectionary volume and a named altar-book printing
were not collated. The Lectionary's 1970 translation of Isaiah 64:2 and the
Hebrew of Psalm 80:16b were not read. The printed *Book of Blessings* was not
read. The readings page state of 26 November 2026, the *Nova Vulgata* Isaiah
state and the NABRE Isaiah 64 state are recorded for source registration
(`research/scope.md` section 5).
