# Omnium Sanctorum — Verified Propers

Facsimile-collated appointed text in liturgical order. This record is the text
control for the canonical leaf
`liturgy/roman-rite/1962/propers/temporal/f02-all-saints` and for every output
derived from it. It carries the Latin of the controlling edition as printed,
each element's relation to the public-domain witnesses and to the Clementine
Vulgate, the publication basis of the Latin, and the lawful English route for
each text. It contains no study prose. Occurrence on 1 November 2026 —
precedence, the commemoration of the Twenty-third Sunday after Pentecost, and
the disputed Preface — is settled as far as this stage can settle it in
`research/context.md` and is not re-argued here.

## Provenance

- **Controlling edition.** *Missale Romanum ex decreto Sacrosancti Concilii
  Tridentini restitutum, Summorum Pontificum cura recognitum*, editio typica
  (Typis Polyglottis Vaticanis, 1962). Source-library identity
  `edition.catholic-church.missale-romanum.vatican-typica-1962`.
- **Controlling artifact.** The CMAA facsimile,
  `artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf`,
  SHA-256 `648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a`,
  82,815,941 bytes. The copy held by this run's resolve-context stage matched
  the registered record before any page was rendered. The artifact is
  `storage = "remote"`; no payload is installed in this repository and no page
  image of it is reproduced anywhere.
- **Printed formulary heading and rank.** Below the running head `FESTA
  NOVEMBRIS` and a full-width engraved headpiece (the enthroned Lord, the
  Lamb with its book, the four living creatures, angels, and elders with palms
  and crowns): `Die 1 novembris` / `IN FESTO OMNIUM SANCTORUM` / `I classis`,
  centred, printed p. 702. The headpiece is decoration, not a text of the
  Mass, and is not reproduced.
- **Printed location.** The Sanctorale. Printed p. 702 (artifact PDF p. 783)
  carries the heading, the Introit (no. 3974) and Collect (3975) in its
  left-hand column and the Lesson's opening (3976) in its right-hand column.
  Printed p. 703 (PDF p. 784; running head `Festa novembris (1)`) carries the
  Lesson's remainder, the Gradual (3977), Alleluia (3978) and Gospel opening
  (3979) in its left-hand column, and the Gospel's remainder with the cue
  `Credo.`, Offertory (3980), Secret (3981), Communion (3982) and
  Postcommunion (3983) in its right-hand column. Marginal numbers
  **3974–3983**, ten numbers for ten printed elements, none skipped and none
  shared. The boundaries on either side (Ss Simon and Jude, ending no. 3973
  on printed p. 701; the *Missa votiva de omnibus Sanctis*, opening no. 3984
  on printed p. 704) were read on page images by the resolve-context stage
  and are recorded in `research/context.md`.
- **Commemorated Sunday's orations.** Printed p. 416 (PDF p. 497; running
  head `…III post Pentecosten`) carries the Collect of the Twenty-third
  Sunday after Pentecost at no. 1720; printed p. 417 (PDF p. 498; running
  head `Dominica XXIII post Pentecosten`) carries its Secret at no. 1726 —
  followed by the Sunday's own rubric `Præfatio de Ss.ma Trinitate.`, which
  belongs to the Sunday's Mass — and its Postcommunion at no. 1728.
- **Digital leaves and resolution.** PDF pp. 783 and 784 were rendered whole
  at 200 dpi and read; each page was then rendered at 400 dpi and read in
  overlapping quarter crops, so that every column section carrying this
  formulary was read at 400 dpi. PDF pp. 497 and 498 were read at 200 dpi,
  whole and in right-column crops. The rasters were transient working
  renders; they are not kept with these records and are not installed
  anywhere.
- **Colour.** White, which the formulary does not print; RG 120 d, as
  `research/context.md` records. The scan is bitonal.
- **Verification status and date.** Collated 2026-10-26 in the research stage
  of run `427e2f58bb897a16`. No unresolved reading remains in the controlling
  witness. The text-layer pulls in `propers/retrieved.txt` were not used for
  any reading.

## The publication basis of the Latin

The feast in its present form (Gregory IV's extension of the Pantheon
dedication to the universal Church, ninth century) is ancient, so every
element of this formulary stands in the public-domain typical line this
repository tracks. The holding of
`src/sources/inventories/missale-romanum-1962-facsimile-rights-v1.toml` is the
route: the Latin travels on 17 U.S.C. 103(b) plus public-domain witnesses to
the preexisting words, never on a property of the 1962 book. No page image,
layout, accent scheme, rubric wording or marginal number of the 1962 book is
reproduced in any publication; the Latin below is this record's
facsimile-checked transcription of the words, with the page's own accent
marks kept here for control.

- **Witness for the feast's ten elements: the Tours Mame 1922 printing.**
  *Missale Romanum*, editio IV iuxta typicam (Mame, Tours, 1922),
  `edition.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam`,
  printed pp. 748–750 (artifact pp. 862–864), held as the scan extract
  `…all-saints-1922-pages-0682b2da` and read into two checked artifacts: the
  four own bodies `…all-saints-four-propers-la-checked-82edd79a` (SHA-256
  `2a0cd4cb…`) and the six scriptural bodies
  `…all-saints-scriptural-propers-la-checked-415a1d46` (SHA-256 `f8d0bf5c…`),
  each carried by its passages. A work published abroad in 1922 is in the
  United States public domain (the Cornell chart line recorded in
  `guidance/missals.md` §5, applied as of 2026-10-26).
- **Collation result, read this stage.** Each of the ten elements as the 1962
  page prints it stands in the Mame text word for word. The differences are
  orthography (the Mame's consonantal *j*, as printed: `Joannes`, `Jesus`,
  `Juda`, `justitiam`, `Justorum`, `justorum`, `Sancti ejus`,
  `discipuli ejus`),
  accents (the checked artifacts carry none), and one conclusion cue (the
  Postcommunion: Mame `Per Dominum.` against the 1962 `Per Dominum
  nostrum.`), on which the working rule recorded in
  `guidance/propers-for-agents.md` holds — conclusion length changes no
  verdict; reproduce the conclusion the target prints. No difference changes
  which word is said.
- **Witness for the commemoration's three orations: the Pustet 1862
  printing, read on its page images.** The Twenty-third Sunday's orations
  are preexisting words printed in the public-domain Ratisbon Pustet Missal
  of 1862. This stage's iteration-1 repair read the tracked page extract
  `artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.pentecost-23-prayer-pages-7e6ef53b`
  (438,339 bytes, SHA-256 `7e6ef53b…` matched; two pages = parent PDF
  pp. 443–444 of the registered facsimile `…ia-facsimile-pdf-363d6fc3` =
  printed pp. 357–358), rendered at 150 dpi whole and in 300-dpi crops:
  - Collect *Absólve, quæsumus Dómine, tuórum delícta populórum…tua
    benignitáte liberémur.*, cue `Per Dóminum.` — printed p. 357 (extract
    p. 1), foot of the left column;
  - Secret *Pro nostræ servitútis augménto…propítius exequáris.*, cue
    `Per Dóminum nostrum.` — printed p. 358 (extract p. 2), from the foot of
    the left column to the head of the right;
  - Postcommunion *Quǽsumus, omnípotens Deus: ut quos…subjacére perículis.*,
    cue `Per Dóminum.` — printed p. 358 (extract p. 2), right column.
  Each agrees with the 1962 page word for word. The differences are
  orthography (`exequáris` for `exsequáris`, `subjacére` for
  `subiacére`), light pointing (a comma fewer in places, e.g. after
  `quæsumus`), and the shorter conclusion cues; the 1962 page prints the
  conclusions in full, and they are given below as the target prints them.
  The provenance ledger
  `src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml` marks
  the `pentecost-23` Collect, Secret and Postcommunion rows `permitted` on
  the same printed pp. 357–358, with the Pustet text layer
  `…pustet-ratisbon-1862.missale-romanum-1862-text-f34bc7cf` (lines
  52526–52533, 52640–52649, 52660–52666), which this stage also read and
  which agrees with the page images.
- **Project editorial projections, internal only.** Two project artifacts
  join the checked witnesses into working text:
  `artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.all-saints-four-propers-adfda498`
  (the four own bodies, in the calendar's *j* orthography) and
  `…editorial-projection-2026-10-25-f02.f02-remaining-nine-latin-f645e8ee`
  (the six scriptural bodies in the target's *i* orthography, plus the three
  commemoration orations). Each declares its sources and transformation in
  its artifact record. They are collation conveniences, not a publication
  source; the 1962 page remains the control.
- **Rubrics and preface directions.** The feast's formulary prints no rubric
  beyond its headings and cues. The Sunday's rubric `Præfatio de Ss.ma
  Trinitate.` (no. 1726, p. 417) is 1960 rubrical matter of the Sunday's
  Mass; the studies describe it and do not reproduce it as this feast's text.

The shared ledger has no `omnium-sanctorum` rows for the six scriptural
bodies; this record carries the collation, and the missing rows are reported
for that ledger's owner in `research/scope.md` §10.

## Appointed text, as printed in 1962

Accents, ligatures and pointing are those of the page images. `℣.` renders
the versicle sign. Elements 1–14 are said on 1 November 2026; the Preface
slot (element 11) is disputed and is recorded, not filled.

### 1. Introit (`introit`) — no. 3974, printed p. 702, left column

Heading: `Antiphona ad Introitum` · verse citation `Ps. 32, 1`

> Gaudeámus omnes in Dómino, diem festum celebrántes sub honóre Sanctórum
> ómnium: de quorum solemnitáte gaudent Angeli, et colláudant Fílium Dei.
> *Ps. 32, 1* Exsultáte, iusti, in Dómino: rectos decet collaudátio.
> ℣. Glória Patri.

The repetition of the antiphon after the *Gloria Patri* is the rubrical rule
(RGMR 427), not printed. The antiphon is an ecclesiastical composition and
carries no citation; the psalm verse is its citation. Mame (p. 748): same
words; `justi`. Clementine: Ps 32:1 agrees, without the inscription `Psalmus
David`, which the Clementine prints inside v. 1.

### 2. Collect (`collect`) — no. 3975, printed p. 702, left column

Heading: `Oratio`

> Omnípotens sempitérne Deus, qui nos ómnium Sanctórum tuórum mérita sub una
> tribuísti celebritáte venerári: quǽsumus; ut desiderátam nobis tuæ
> propitiatiónis abundántiam, multiplicátis intercessóribus, largiáris. Per
> Dóminum.

Mame (p. 748): same words and the same cue.

### 3. Commemoration Collect (`commemoration-collect`) — no. 1720, printed p. 416, right column

Heading: `Oratio` (of the Dominica XXIII post Pentecosten)

> Absólve, quǽsumus, Dómine, tuórum delícta populórum: ut a peccatórum
> néxibus, quæ pro nostra fragilitáte contráximus, tua benignitáte liberémur.
> Per Dóminum nostrum Iesum Christum, Fílium tuum: Qui tecum vivit et regnat
> in unitáte.

Said after the feast's Collect under this second conclusion (RG 108–109 a,
111 a; RGMR 434 a, 437 a), as `research/context.md` settles. Pustet 1862
(printed p. 357, read on the page image): same words, with the cue
`Per Dóminum.`.

### 4. Lesson (`lesson`) — no. 3976, printed pp. 702–703

Heading: `Léctio libri Apocalýpsis beáti Ioánnis Apóstoli.` · `Apoc. 7, 2-12`

> In diébus illis: Ecce ego Ioánnes vidi álterum Angelum ascendéntem ab ortu
> solis, habéntem signum Dei vivi: et clamávit voce magna quátuor Angelis,
> quibus datum est nocére terræ et mari, dicens: Nolíte nocére terræ et mari,
> neque arbóribus, quoadúsque signémus servos Dei nostri in fróntibus eórum.
> Et audívi númerum signatórum, centum quadragínta quátuor mília signáti, ex
> omni tribu filiórum Israel. Ex tribu Iuda duódecim mília signáti. Ex tribu
> Ruben duódecim mília signáti. Ex tribu Gad duódecim mília signáti. Ex tribu
> Aser duódecim mília signáti. Ex tribu Néphtali duódecim mília signáti. Ex
> tribu Manásse duódecim mília signáti. Ex tribu Símeon duódecim mília
> signáti. Ex tribu Levi duódecim mília signáti. Ex tribu Issachar duódecim
> mília signáti. Ex tribu Zábulon duódecim mília signáti. Ex tribu Ioseph
> duódecim mília signáti. Ex tribu Béniamin duódecim mília signáti. Post hæc
> vidi turbam magnam, quam dinumeráre nemo póterat, ex ómnibus géntibus, et
> tríbubus, et pópulis, et linguis: stantes ante thronum, et in conspéctu
> Agni, amícti stolis albis, et palmæ in mánibus eórum: et clamábant voce
> magna, dicéntes: Salus Deo nostro, qui sedet super thronum, et Agno. Et
> omnes Angeli stabant in circúitu throni, et seniórum, et quátuor
> animálium: et cecidérunt in conspéctu throni in fácies suas, et
> adoravérunt Deum, dicéntes: Amen. Benedíctio, et cláritas, et sapiéntia, et
> gratiárum áctio, honor, et virtus, et fortitúdo Deo nostro in sǽcula
> sæculórum. Amen.

The Lesson crosses the page at `Néphtali duódecim / mília signáti`. Mame
(pp. 748–749): same words; `Joannes`, `Juda`. Clementine: the liturgical
incipit `In diébus illis: Ecce ego Ioánnes vidi álterum Angelum` stands for
`Et vidi alterum angelum ascendentem` (7:2); every other word of vv. 2–12
agrees.

### 5. Gradual (`gradual`) — no. 3977, printed p. 703, left column

Heading: `Graduale` · `Ps. 33, 10 et 11`

> Timéte Dóminum, omnes Sancti eius: quóniam nihil deest timéntibus eum.
> ℣. Inquiréntes autem Dóminum, non defícient omni bono.

Mame (p. 749): same words; `Sancti ejus`. Clementine: the Missal keeps the
older Roman psalter wording — v. 10 as `quóniam nihil deest timéntibus eum`
for the Clementine's `quoniam non est inopia timentibus eum`, and the second
clause of v. 11 as `non defícient omni bono` for `non minuentur omni bono`;
v. 11a `Dívites eguérunt, et esuriérunt` is not said.

### 6. Alleluia (`alleluia`) — no. 3978, printed p. 703, left column

> Allelúia, allelúia. ℣. *Matth. 11, 28* Veníte ad me, omnes qui laborátis
> et oneráti estis: et ego refíciam vos. Allelúia.

Mame (p. 749): same words. Clementine: agrees apart from orthography. No
Sequence and no Tract; the feast never falls in Septuagesima or paschal
time.

### 7. Gospel (`gospel`) — no. 3979, printed p. 703, both columns

Heading: `✠ Sequéntia sancti Evangélii secúndum Matthǽum.` · `Mt. 5, 1-12`

> In illo témpore: Videns Iesus turbas, ascéndit in montem, et cum sedísset,
> accessérunt ad eum discípuli eius, et apériens os suum, docébat eos,
> dicens: Beáti páuperes spíritu: quóniam ipsórum est regnum cælórum. Beáti
> mites: quóniam ipsi possidébunt terram. Beáti qui lugent: quóniam ipsi
> consolabúntur. Beáti qui esúriunt et sítiunt iustítiam: quóniam ipsi
> saturabúntur. Beáti misericórdes: quóniam ipsi misericórdiam consequéntur.
> Beáti mundo corde: quóniam ipsi Deum vidébunt. Beáti pacífici: quóniam
> fílii Dei vocabúntur. Beáti qui persecutiónem patiúntur propter iustítiam:
> quóniam ipsórum est regnum cælórum. Beáti estis cum maledíxerint vobis, et
> persecúti vos fúerint, et díxerint omne malum advérsum vos, mentiéntes,
> propter me: gaudéte et exsultáte, quóniam merces vestra copiósa est in
> cælis.

Cue: `Credo.` Mame (pp. 749–750): same words; `Jesus`, `discipuli ejus`.
Clementine: the liturgical opening `In illo tempore: Videns Iesus turbas`
stands for `Videns autem Jesus turbas` (5:1); the reading ends at 5:12a
(`in cælis`), before `Sic enim persecuti sunt prophetas…`; every other word
of vv. 1–12a agrees.

### 8. Offertory (`offertory`) — no. 3980, printed p. 703, right column

Heading: `Ant. ad Offertorium` · `Sap. 3, 1, 2 et 3`

> Iustórum ánimæ in manu Dei sunt, et non tanget illos torméntum malítiæ:
> visi sunt óculis insipiéntium mori: illi autem sunt in pace, allelúia.

Mame (p. 750): same words; `Justorum`. Clementine
(`src/sources/bibles/clementine-vulgate/chapters/Wis/3.json`): Wis 3:1
`Justorum autem animæ in manu Dei sunt, et non tangent illos tormentum
mortis.` 3:2 `Visi sunt oculis insipientium mori, et æstimata est afflictio
exitus illorum,` 3:3 `et quod a nobis est iter exterminium; illi autem sunt
in pace:`. Against it the antiphon (1) omits `autem` after `Iustórum`
(3:1); (2) reads `tanget` for `tangent` (3:1); (3) reads `malítiæ` for
`mortis` (3:1); (4) omits `et æstimata est afflictio exitus illorum, et quod
a nobis est iter exterminium` (3:2b–3a); and (5) adds `allelúia`. The
antiphon is the received liturgical form, not the verse. Its history is
recorded in `research/scope.md` §3.7: the 1570 Missal's own All Saints
Offertory reads `tormentum mortis` without alleluia.

### 9. Secret (`secret`) — no. 3981, printed p. 703, right column

Heading: `Secreta`

> Múnera tibi, Dómine, nostræ devotiónis offérimus: quæ et pro cunctórum
> tibi grata sint honóre iustórum, et nobis salutária, te miseránte,
> reddántur. Per Dóminum.

Mame (p. 750): same words and cue; `justorum`.

### 10. Commemoration Secret (`commemoration-secret`) — no. 1726, printed p. 417, right column

Heading: `Secreta` (of the Sunday)

> Pro nostræ servitútis augménto sacrifícium tibi, Dómine, laudis offérimus:
> ut, quod imméritis contulísti, propítius exsequáris. Per Dóminum nostrum
> Iesum Christum, Fílium tuum: Qui tecum vivit et regnat in unitáte.

Said secretly after the feast's Secret; its last words are said aloud before
the Preface (RGMR 481). The rubric `Præfatio de Ss.ma Trinitate.` printed
after it belongs to the Sunday's Mass and is not inherited (RGMR 483).

### 11. Preface (`preface`) — disputed, recorded not filled

The feast prints no proper Preface and no Preface direction. The slot is one
Preface, either *Præfatio de Ss.ma Trinitate* (n. 1082, printed p. 293) or
*Præfatio commúnis* (n. 1086, printed p. 297). The evidence both ways rests
only on registered loci of this edition: RGMR 482, 483, 494 b and 498
(printed p. XXXIV) and the Vigil of the Nativity rubric (printed p. 16),
stated in `research/scope.md` §6 item 7 and `research/context.md`
(*Occurrence*, Preface). The repository test that asserts the common Preface
without an authority is reported for its owner in `research/scope.md` §10.
No registered source settles the slot, and the studies follow the fixed rule
in `research/scope.md` §11: both candidates named with their basis, neither
asserted, and no Ordo or web calendar cited. Neither text is reproduced here, because
neither is settled as this feast's appointment and both are registered
elsewhere (`…vatican-typica-1962.praefationes`,
`…praefationes-sine-cantu`, with the 1861 Cummiskey antecedent collations in
`src/sources/inventories/roman-1962-ordo-missae-v1.toml`).

### 12. Communion (`communion`) — no. 3982, printed p. 703, right column

Heading: `Ant. ad Communionem` · `Mt. 5, 8-10`

> Beáti mundo corde, quóniam ipsi Deum vidébunt: beáti pacífici, quóniam
> fílii Dei vocabúntur: beáti qui persecutiónem patiúntur propter
> iustítiam, quóniam ipsórum est regnum cælórum.

Mame (p. 750): same words. Clementine: vv. 8–10, agreeing word for word.

### 13. Postcommunion (`postcommunion`) — no. 3983, printed p. 703, right column

Heading: `Postcommunio`

> Da, quǽsumus, Dómine, fidélibus pópulis ómnium Sanctórum semper
> veneratióne lætári: et eórum perpétua supplicatióne muníri. Per Dóminum
> nostrum.

Mame (p. 750): same words; the cue is `Per Dominum.` — the one conclusion
difference between the witnesses, handled by the conclusion rule above.

### 14. Commemoration Postcommunion (`commemoration-postcommunion`) — no. 1728, printed p. 417, right column

Heading: `Postcommunio` (of the Sunday)

> Quǽsumus, omnípotens Deus: ut, quos divína tríbuis participatióne
> gaudére, humánis non sinas subiacére perículis. Per Dóminum nostrum Iesum
> Christum, Fílium tuum: Qui tecum vivit et regnat in unitáte.

Said after the feast's Postcommunion under this second conclusion, as no. 3.

### Nothing else is proper

The formulary prints no Sequence, Tract, prophecy, proper *Communicantes* or
*Hanc igitur*, *Oratio super populum*, second oration beyond the Sunday's
commemoration, blessing or alternative reading (RGMR 501). The votive
formulary on printed p. 704 is a separate Mass and contributes nothing. The
Ordinary is not reproduced.

## English routes

English is never composed, translated, adapted or paraphrased by the studies.
Every English text below is quoted from a registered public-domain witness
and attributed at first use and in the references. None is an approved
liturgical translation.

- **Scriptural elements: the Douay-Rheims (Challoner),**
  `edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581`,
  read through `tools/tpt mass-propers show --bible douay-rheims` and the
  verse-text artifacts directly. Where the Missal selects part of a verse,
  the Douay words for that part are quoted, with an ellipsis for what the
  Missal omits; nothing is reworded to fit. The Douay cannot carry these
  Missal forms, which the studies give in Latin with a plain statement of
  what they are:
  - the Lesson's liturgical incipit `In diebus illis: Ecce ego Ioannes vidi
    alterum Angelum ascendentem ab ortu solis` (the Douay's 7:2 begins `And
    I saw another angel ascending from the rising of the sun`);
  - the Gradual's received wording (`Fear the Lord, all ye his saints: for
    there is no want to them that fear him` is close, but the Douay's v. 11
    begins `The rich have wanted, and have suffered hunger`, which the Mass
    does not read, and `shall not be deprived of any good` for the Missal's
    `non deficient omni bono` differs in the verb);
  - the Gospel's liturgical opening `In illo témpore: Videns Iesus turbas`
    (the Douay's 5:1 reads `And seeing the multitudes`) and its end at 12a;
  - the Offertory, an adaptation. Douay Wis 3:1–3 reads `But the souls of
    the just are in the hand of God, and the torment of death shall not
    touch them. In the sight of the unwise they seemed to die: and their
    departure was taken for misery: And their going away from us, for utter
    destruction: but they are in peace.` The antiphon has no `But` at the
    start (the omitted `autem`), `the torment of malice` where the Douay
    has `the torment of death`, none of `and their departure was taken for
    misery: And their going away from us, for utter destruction` (3:2b–3a),
    and a closing `alleluia`. (The `tanget`/`tangent` difference does not
    show in English.);
  - the Introit antiphon (no biblical source) and the Introit verse's omitted
    inscription `A psalm for David`, which the Douay prints inside Ps 32:1
    (its own numbering; the Missal's `Ps. 32, 1` is the Douay's 32:1 with
    the inscription separate, per the repository concordance
    `…challoner-gutenberg-1581.psalm-numbering-ee3c7757`: Vulgate 32 =
    Hebrew/English 33. For the Gradual, the Vulgate and the Douay both count
    Ps 33's inscription as v. 1, as the Hebrew does, so Vulgate 33:10–11 =
    Douay 33:10–11 = Hebrew 34:10–11; English Bibles that follow the Hebrew
    but leave the inscription unnumbered call these verses 34:9–10).
  The Lasance hand missal (next item) prints its own English of every one of
  these received forms in the registered checked artifact
  `artifact.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.all-saints-scriptural-propers-en-checked-ff92e98e`
  (SHA-256 `99597fe1…`), e.g. `In those days, behold, I, John, saw another
  angel ascending from the rising of the sun` and `the torment of malice
  shall not touch them … but they are in peace. Alleluia.` No
  translations-inventory row registers that artifact, so it is a lead: an
  author who quotes it does so under the Lasance's attribution and says so.
- **Orations: the Lasance *New Roman Missal*, Benziger revised edition of
  1945,**
  `edition.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945`,
  English layer public domain in the United States by nonrenewal
  (`src/sources/inventories/lasance-new-roman-missal-rights-v1.toml`). The
  Introit and Collect (printed p. 1265) and the Secret and Postcommunion
  (printed p. 1268) stand in
  `src/sources/inventories/roman-1962-proper-translations-v1.toml` with
  `collation_result = "confirmed"`; the commemoration's three orations stand
  in the same inventory under `pentecost-23` (printed pp. 733, 735-736, 736).
  Those rows rest on these Lasance records, every one of them declared in
  `research/review-dependencies.toml` and so inside the research seal: the
  publication artifacts
  `artifact.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.resume-orations-core193-2026-10-23-0736f65f`
  (`english.tsv` rows 83-86, the omnium-sanctorum Collect, Introit,
  Postcommunion and Secret) and `…resume-orations-phase2-2026-10-23-5a4e83f7`
  (rows 88-90, the pentecost-23 Collect, Postcommunion and Secret); the
  verify passages (page-image inspection of the facsimile
  `…internet-archive-facsimile-pdf-6cf3c3d0`) and publish passages (the
  bounded derivative rows)
  `…resume-orations-core193-2026-10-23-{verify,publish}-omnium-sanctorum--main--{introit,collect,secret,postcommunion}--all--1`
  and
  `…resume-orations-phase2-2026-10-23-{verify,publish}-pentecost-23--main--{collect,secret,postcommunion}--all--1`;
  and the same-witness conclusion table
  `…resume-orations-conclusion-table-2026-10-23-7dbb4a25` with its verify and
  transcription passages, on which the omnium-sanctorum Postcommunion and the
  three pentecost-23 rows rest. The English quoted must be the publish
  passage's row, byte for byte. The Lasance English was not re-read on its
  page images in this stage.
  **Rubrical difference, disclosed.** The Lasance prints the pre-1960 order
  (`Double of the First Class`, additional commemorations and conclusions,
  and a different commemorated-Sunday apparatus). None of that is the 1962
  order, and the studies never present it as such. Its Latin column is not a
  publication source here.
- **Restricted English, never used.** No ICEL, Knox, Jerusalem, RSV, NRSV,
  NABRE or Grail text is reproduced.

## Unresolved discrepancies

None in the controlling witness: no element has an unread word. Two bounded
matters are recorded, not errors: (1) the Mame Postcommunion cue `Per
Dominum.` against the 1962 `Per Dominum nostrum.`, settled by the
conclusion rule; (2) the Preface appointment is disputed between the Trinity
and common Prefaces — a rubrical question about which text is said, not a
textual defect, carried open in `research/context.md` and reported for the
test's owner. The shared records' over-wide Gradual, Gospel and Offertory
ranges, which make `mass-propers show` serve Douay words the Mass does not
read, are reported in `research/scope.md` §10.
