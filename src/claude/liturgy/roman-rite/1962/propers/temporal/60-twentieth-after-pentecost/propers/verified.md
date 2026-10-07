# Twentieth Sunday after Pentecost — Verified Propers

Facsimile-collated appointed text in liturgical order. This record is the text
control for the canonical leaf
`liturgy/roman-rite/1962/propers/temporal/60-twentieth-after-pentecost` and for
every output derived from it. It carries the Latin of the controlling edition as
printed, the collation of every element against the public-domain 1862
antecedent, each element's relation to the Clementine Vulgate, the three
orations of the commemoration that the rubrics add in a low or conventual Mass
on 11 October 2026, and the lawful English route for each text. It contains no
study prose.

## Provenance

- **Controlling edition.** *Missale Romanum ex decreto Sacrosancti Concilii
  Tridentini restitutum, Summorum Pontificum cura recognitum*, editio typica
  (Typis Polyglottis Vaticanis, 1962). Source-library identity
  `edition.catholic-church.missale-romanum.vatican-typica-1962`.
- **Controlling artifact.** The CMAA facsimile,
  `artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf`,
  SHA-256 `648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a`,
  82,815,941 bytes, retrieved from
  `https://media.churchmusicassociation.org/pdf/missale62.pdf`. The copy fetched
  on 2026-10-07 for this production was re-hashed in the research stage before
  any page was opened; digest and byte length matched the registered record. The
  artifact is registered `storage = "remote"`; no payload is installed in this
  repository.
- **Printed formulary heading and rank.** `DOMINICA VIGESIMA` (capitals),
  `post Pentecosten`, `II classis`, each on its own line, in the right-hand
  column of printed p. 412.
- **Printed location.** The heading stands in the right-hand column of printed
  p. 412 (artifact PDF p. 493), immediately below the Postcommunion *Tua nos,
  Domine, medicinalis operatio* (no. 1688) of the Nineteenth Sunday. That column
  carries the Introit (no. 1689), the Collect (1690) and the first three lines
  of the Epistle (1691). Printed p. 413 (PDF p. 494) carries the rest of the
  Epistle, the Gradual (1692), Alleluia (1693) and the opening of the Gospel
  (1694) in its left-hand column, and the close of the Gospel, the Offertory
  (1695), Secret (1696), Communion (1697) and Postcommunion (1698) in its
  right-hand column, above the heading `DOMINICA VIGESIMA PRIMA post
  Pentecosten`, `II classis`, whose Introit is no. 1699. Marginal numbers
  **1689–1698**, ten numbers for ten elements, none skipped and none shared.
- **Running heads.** Printed p. 412 is headed `Dominica XX post Pentecosten`,
  although its left-hand column belongs to the Nineteenth Sunday; p. 413 is
  headed `Dominica XXI post Pentecosten`, although all but its last lines belong
  to this formulary. The running heads do not bound the formulary.
- **Digital leaves and resolution.** Artifact PDF pp. 493 and 494, each one
  bitonal CCITT image at 500 ppi native (2591 × 3819 and 2573 × 3788 px). Both
  pages were rendered at 200 dpi for the whole page and at 400 dpi for crops of
  every column section that carries text of this formulary: the right-hand
  column of p. 412 from the heading to the foot, and on p. 413 the upper and
  lower halves of the left-hand column and the right-hand column from its head
  to the Postcommunion.
- **Marginal numbers.** Every number 1689–1698 prints whole and legible on the
  page images. The text layer's `!690` for 1690 is a layer fault.
- **Colour.** Green, which the formulary does not print; RG 127 b (printed
  p. XX) is the rule, as `research/context.md` records. The scan is bitonal.
- **Verification status and date.** Collated 2026-10-07 in the research stage
  of run `9c1136f1f8d1241c`. No unresolved reading remains in the controlling
  edition. The facsimile's text layer was used only to locate the pages and is
  kept, with its misreadings, in `propers/retrieved.txt`.

### The antecedent witness read, and what it was used for

- **The 1862 antecedent.** *Missale Romanum*, Pustet, Ratisbon, 1862,
  `edition.catholic-church.missale-romanum.pustet-ratisbon-1862`, printed
  pp. 352–354 under the heading `Dominica XX. post Pentecosten.` Read twice:
  - on the page images of the tracked three-page extraction
    `artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.pentecost-20-pages-352-354`
    (SHA-256 recomputed as
    `1f171dea09c09014742cdcffcac175baa2fe39a0dfcae94316e300439a4d8768` and matched;
    each page one 2500 × 4097 px JPX image at 300 ppi native), rendered at
    300 dpi and read whole at reduced size and in crops at native resolution:
    the Introit opening (p. 352, foot of the right-hand column); the Introit's
    close, the Collect and Epistle, and the Epistle's close, Gradual and the
    Alleluia's first line (p. 353, left-hand column, two crops); the Alleluia
    verse and Gospel, and the Gospel's close, Offertory and Secret (p. 353,
    right-hand column, two crops); the Communion and Postcommunion (p. 354,
    head of the left-hand column); and
  - in the tracked public-domain text layer
    `artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.missale-romanum-1862-text-f34bc7cf`
    (SHA-256 recomputed and matched), physical lines 51986–52142, kept in
    `propers/retrieved.txt`.

  The running head of p. 352 reads `Dominica XX. post Pentecosten.` over a left
  column that carries the Nineteenth Sunday's Gospel; that of p. 354 reads
  `Dominica XXI. post Pentecosten.` over the Communion and Postcommunion of this
  formulary — the same head-versus-formulary mismatch the 1962 reproduces.

- **The Clementine Vulgate.** Every scriptural element was compared word by word
  with the tracked Clementine verse texts
  (`artifact.catholic-church.vulgata-clementina.ebible-latvuc.verse-text-32-daniel-3ca259b5`,
  `…-21-psalms-d20e21f8`, `…-56-ephesians-d9b55031`, `…-50-john-1542486b`) as
  projected by `tools/tpt mass-propers show --calendar roman-1962 --mass
  pentecost-20 --bible clementine-vulgate`, after normalising i/j, æ/ae, accents
  and pointing; Daniel 3:24–51 was read directly in the verse-text file. Psalm
  loci are the Missal's Vulgate numbers, resolved through the registered
  concordance `…challoner-gutenberg-1581.psalm-numbering-ee3c7757` (SHA-256
  recomputed and matched): Pss 118, 136 and 144 are Hebrew 119, 137 and 145 with
  a zero verse offset; Ps 107 is Hebrew 108, and because the concordance counts
  the inscription as Hebrew v. 1 the Missal's 107:2 is Hebrew 108:2 and English
  108:1.

## The appointed texts

Latin as printed in the 1962 typical edition, with its accents, ligatures and
pointing. `℣.` renders the printed versicle sign and `✠` the printed cross. The
drop capital of each element is joined to its word; a drop capital prints no
accent.

### 1. Introit (`introit`) — no. 1689, printed p. 412

*Antiphona ad Introitum* — *Dan. 3, 31, 29 et 35*

> Omnia, quæ fecísti nobis, Dómine, in vero iudício fecísti, quia peccávimus
> tibi, et mandátis tuis non obœdívimus: sed da glóriam nómini tuo, et fac
> nobíscum secúndum multitúdinem misericórdiæ tuæ. *Ps. 118, 1* Beáti
> immaculáti in via: qui ámbulant in lege Dómini. ℣. Glória Patri.

The antiphon is not a continuous Vulgate text and its closing clause does not
stand at the verses the Missal cites; see *Relation to the Clementine Vulgate*
below and `research/scope.md` § 1.3.

### 2. Collect (`collect`) — no. 1690, printed p. 412

*Oratio*

> Largíre, quǽsumus, Dómine, fidélibus tuis indulgéntiam placátus et pacem: ut
> páriter ab ómnibus mundéntur offénsis, et secúra tibi mente desérviant. Per
> Dóminum.

### 3. Epistle (`epistle`) — no. 1691, printed pp. 412–413

*Léctio Epístolæ beáti Pauli Apóstoli ad Ephésios.* — *Ephes. 5, 15-21*

> Fratres: Vidéte quómodo caute ambulétis: non quasi insipiéntes, sed ut
> sapiéntes, rediméntes tempus, quóniam dies mali sunt. Proptérea nolíte fíeri
> imprudéntes, sed intellegéntes quæ sit volúntas Dei. Et nolíte inebriári vino,
> in quo est luxúria: sed implémini Spíritu Sancto, loquéntes vobismetípsis in
> psalmis, et hymnis, et cánticis spirituálibus, cantántes, et psalléntes in
> córdibus vestris Dómino: grátias agéntes semper pro ómnibus, in nómine Dómini
> nostri Iesu Christi, Deo et Patri. Subiécti ínvicem in timóre Christi.

### 4. Gradual (`gradual`) — no. 1692, printed p. 413

*Graduale* — *Ps. 144, 15-16*

> Oculi ómnium in te sperant, Dómine: et tu das illis escam in témpore
> opportúno. ℣. Aperis tu manum tuam: et imples omne ánimal benedictióne.

### 5. Alleluia (`alleluia`) — no. 1693, printed p. 413

> Allelúia, allelúia. ℣. *Ps. 107, 2* Parátum cor meum, Deus, parátum cor meum:
> cantábo, et psallam tibi, glória mea. Allelúia.

The citation stands inside the verse line. No Tract and no Sequence is printed.

### 6. Gospel (`gospel`) — no. 1694, printed p. 413

✠ *Sequéntia sancti Evangélii secúndum Ioánnem.* — *Io. 4, 46-53*

> In illo témpore: Erat quidam régulus, cuius fílius infirmabátur Caphárnaum.
> Hic cum audísset, quia Iesus adveníret a Iudǽa in Galilǽam, ábiit ad eum, et
> rogábat eum ut descénderet, et sanáret fílium eius: incipiébat enim mori.
> Dixit ergo Iesus ad eum: Nisi signa et prodígia vidéritis, non créditis.
> Dicit ad eum régulus: Dómine, descénde priúsquam moriátur fílius meus. Dicit
> ei Iesus: Vade, fílius tuus vivit. Crédidit homo sermóni, quem dixit ei Iesus,
> et ibat. Iam autem eo descendénte, servi occurrérunt ei, et nuntiavérunt
> dicéntes, quia fílius eius víveret. Interrogábat ergo horam ab eis, in qua
> mélius habúerit. Et dixérunt ei: Quia heri hora séptima relíquit eum febris.
> Cognóvit ergo pater quia illa hora erat, in qua dixit ei Iesus: Fílius tuus
> vivit: et crédidit ipse, et domus eius tota.

Followed by the printed cue *Credo.*

### 7. Offertory (`offertory`) — no. 1695, printed p. 413

*Ant. ad Offertorium* — *Ps. 136, 1*

> Super flúmina Babylónis illic sédimus, et flévimus: dum recordarémur tui,
> Sion.

### 8. Secret (`secret`) — no. 1696, printed p. 413

*Secreta*

> Cæléstem nobis prǽbeant hæc mystéria, quǽsumus, Dómine, medicínam: et vítia
> nostri cordis expúrgent. Per Dóminum.

Followed by the printed direction *Præfatio de Ssma Trinitate.*

### 9. Communion (`communion`) — no. 1697, printed p. 413

*Ant. ad Communionem* — *Ps. 118, 49-50*

> Meménto verbi tui servo tuo, Dómine, in quo mihi spem dedísti: hæc me
> consoláta est in humilitáte mea.

### 10. Postcommunion (`postcommunion`) — no. 1698, printed p. 413

*Postcommunio*

> Ut sacris, Dómine, reddámur digni munéribus: fac nos, quǽsumus, tuis semper
> obœdíre mandátis. Per Dóminum nostrum.

## Commemorated orations on 11 October 2026

These belong to the formulary *Die 11 octobris, MATERNITATIS BEATÆ MARIÆ
VIRGINIS, II classis* (printed pp. 685–686, artifact PDF pp. 766–767), not to
the Sunday. They are said, each under its own conclusion after the Sunday's
oration, in a low Mass and in a conventual Mass on this date, and omitted in a
sung Mass that is not conventual (`research/context.md`). Read on 200-dpi page
images of both pages and 400-dpi crops of the three orations (the same bitonal
500-ppi CCITT images, 2569 × 3785 and 2588 × 3798 px).

### Collect of the commemoration — no. 3847, printed p. 685

> Deus, qui de beátæ Maríæ Vírginis útero Verbum tuum, Angelo nuntiánte, carnem
> suscípere voluísti: præsta supplícibus tuis; ut, qui vere eam Genetrícem Dei
> crédimus, eius apud te intercessiónibus adiuvémur. Per eúndem Dóminum nostrum
> Iesum Christum Fílium tuum: Qui tecum vivit et regnat in unitáte.

### Secret of the commemoration — no. 3855, printed p. 686

> Tua, Dómine, propitiatióne, et beátæ Maríæ semper Vírginis, Unigéniti tui
> Matris, intercessióne, ad perpétuam atque præséntem hæc oblátio nobis
> profíciat prosperitátem et pacem. Per eúndem Dóminum.

The direction that follows it, *Præfatio de B. Maria Virg. Et te in
festivitáte*, does not travel with the commemoration (RGMR 483).

### Postcommunion of the commemoration — no. 3857, printed p. 686

> Hæc nos commúnio, Dómine, purget a crímine: et, intercedénte beáta Vírgine Dei
> Genetríce María, cæléstis remédii fáciat esse consórtes. Per eúndem Dóminum.

## Collation against the 1862 antecedent

Every element of the formulary stands in the 1862 in the same words. The
differences are transformations in the sense of `guidance/propers-for-agents.md`
("A transformation changes how a word is spelled; a variant changes which word
is said"); none is a variant.

| Element | 1862 (printed page) | Differences from the 1962, all transformations |
| --- | --- | --- |
| Introit | p. 352 right col. to p. 353 left col. | rubric *Introitus*; citation *Dan. 3.* and *Ps. 118.* without verses; *judício*, *obedívimus*; colon after *fecísti* where the 1962 has a comma |
| Collect | p. 353 left col. | no comma after *quǽsumus*; same conclusion *Per Dóminum.* |
| Epistle | p. 353 left col. | citation *c. 5.*; *Fratres.* with a full stop; *intelligéntes*; *Spíritu sancto*; *Jesu*; *Subjécti*; minor pointing |
| Gradual | p. 353 left col. | citation *Ps. 144.* with an asterisk; comma for colon after *manum tuam* |
| Alleluia | p. 353 left col. to right col. | *Allelúja*; citation *Ps. 107.* |
| Gospel | p. 353 right col. | citation *c. 4.*; *Joánnem*, *cujus*, *Jesus*, *Judǽa*, *ejus*, *Jam*; lower-case *quia* after *dixérunt ei:*; a comma after *pater* |
| Offertory | p. 353 right col. | rubric *Offertorium.*; citation *Ps. 136.*; comma for colon; no comma before *Sion* |
| Secret | p. 353 right col. | *Cœléstem*; no comma after *quǽsumus* |
| Communion | p. 354 left col. | rubric *Communio.*; citation *Ps. 118.* |
| Postcommunion | p. 354 left col. | *obedíre*; conclusion *Per Dóminum.* where the 1962 prints *Per Dóminum nostrum.* |

The 1862 also prints, on the same pages, its own *Secunda Oratio. A cunctis
nos. fol. 315.*, *Alia Secreta. Exaúdi nos Deus. fol. 316.*, *Alia
Postcommunio. Mundet et múniat. fol. 316.* and three cues *Tertia ad libitum.*
These belong to the pre-1960 rubrics and are not part of the 1962 formulary.

**The commemorated orations.** The 1862 prints all three under *Festa
Octobris. Dominica II. Festum Maternitatis B. Mariæ Virginis*, among its Masses
for certain places, appendix pp. [171]–[172]. They were read on the page images
of the tracked two-page extraction
`artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.maternity-pages-171-172`
(SHA-256 recomputed as
`f8276afb435a9c4924329692663a9ca354ccfbe82fce4e0107cb3a17140005c7` and matched;
300 ppi native), whole and in native-resolution crops of the Collect (p. [171],
right-hand column) and the Secret (p. [172], left-hand column); the
Postcommunion was read on the whole-page image. The words agree with the 1962.
The differences are *genitrícem* and *genitríce* (two received spellings of one
word), *ejus*, *adjuvémur*, *matris* lower-case, *Cœléstis*, pointing, and the
conclusions *Per eúmdem Dóminum.* where the 1962 prints *Per eúndem* (and, on the
Collect, the conclusion written out). That formulary has its own Introit
*Salve, sancta parens* and Gospel Lk 2:43–51, is said with a commemoration of
the occurring Sunday and the Sunday's Gospel at the end, and supplies nothing to
the 1962 Sunday but the antecedent wording of these three orations. The
registered passage
`passage.catholic-church.missale-romanum.pustet-ratisbon-1862.maternitatis-beatae-mariae-virginis-orations`
(verified 2026-10-05) records the same loci.

## Relation to the Clementine Vulgate

These are textual observations about wording and boundary. They assert no
origin for any form; `research/scope.md` § 1.3 records what was sought and not
found.

- **Introit.** A cento. Its first clause shares *quæ fecísti nobis … in vero
  iudício fecísti* with Clementine Dan 3:31 (*Omnia ergo, quæ induxisti super
  nos, et universa quæ fecisti nobis, in vero judicio fecisti*); *peccávimus*
  stands at v. 29; *mandátis tuis non obœdívimus* has no word-for-word
  Clementine counterpart (v. 30 reads *præcepta tua non audivimus, nec
  observavimus*); the closing *da glóriam nómini tuo, et fac nobíscum secúndum
  multitúdinem misericórdiæ tuæ* corresponds to words of vv. 43 (*da gloriam
  nomini tuo*) and 42 (*fac nobiscum juxta mansuetudinem tuam, et secundum
  multitudinem misericordiæ tuæ*). Clementine v. 35, which the Missal cites,
  reads *neque auferas misericordiam tuam a nobis, propter Abraham …*. The
  verse omits the Clementine's title *Alleluja* and letter heading *Aleph*,
  which the Clementine counts inside Ps 118:1. The same antiphon is the Introit
  of the 1962 Missal's *Feria V post dominicam I Passionis* (printed p. 124,
  no. 795, PDF p. 205), cited there *Dan. 3, 31* alone.
- **Epistle.** The Missal prefixes the liturgical address *Fratres:* and omits
  the Clementine's *itaque* and its vocative *fratres* (*Videte itaque, fratres,
  quomodo caute ambuletis*); it spells *intellegéntes* for *intelligentes*.
  Every other word of vv. 15–21 agrees.
- **Gradual.** The Missal reads *et tu das illis escam* where the Clementine at
  Ps 144:15 reads *et tu das escam illorum*. The verse agrees.
- **Alleluia.** The Missal reads *cantábo, et psallam tibi, glória mea* where
  the Clementine at Ps 107:2 reads *cantabo, et psallam in gloria mea*.
- **Gospel.** The liturgical opening *In illo témpore: Erat quidam régulus*
  stands for the first half of v. 46, *Venit ergo iterum in Cana Galilææ, ubi
  fecit aquam vinum. Et erat quidam regulus*, so the pericope begins inside the
  verse it cites and leaves the Cana setting unread. Every other word of
  vv. 46–53 agrees.
- **Offertory.** The Missal omits the title *Psalmus David, Jeremiæ*, reads
  *dum* for *cum*, and adds *tui* (*dum recordarémur tui, Sion*; Clementine *cum
  recordaremur Sion*).
- **Communion.** The Missal reads *Meménto* for the Clementine's *Memor esto*,
  adds *Dómine* after *servo tuo*, and ends at *in humilitáte mea*, before the
  Clementine's close of v. 50, *quia eloquium tuum vivificavit me*. It omits the
  letter heading *Zain*.

## Lawful study-text routes

### Latin

- **The ten proper elements.** Publishable on 17 U.S.C. 103(b) with a
  public-domain antecedent, as settled once for the repository in
  `src/sources/inventories/missale-romanum-1962-facsimile-rights-v1.toml`: every
  element's wording stands in the 1862 Pustet printing (above), read on its page
  images. The provenance ledger
  `src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml` carries
  `permitted` rows for the Collect, Secret and Postcommunion; the Introit and the
  six scriptural elements have no ledger row, and the basis for them is the 1862
  collation recorded here (`research/scope.md` § 9).
- **The three commemorated orations.** Publishable on the same basis; the 1862
  appendix pp. [171]–[172] carries all three. The ledger's three rows for
  `maternitatis-beatae-mariae-virginis` are `permitted` but give as antecedent
  locators pages of the 1922 Tours Mame and of the 1862 text layer that the
  corrected 1862 passage record calls a misattribution (`research/scope.md` § 9).
- **The Trinity Preface.** Appointed by the printed direction after no. 1696
  and by RGMR 494 b; its text stands at printed p. 293, no. 1082 (PDF p. 374),
  within the registered `…vatican-typica-1962.praefationes` passage. It is cited,
  not reproduced, by this leaf's records.

### English

English is never composed, translated, adapted or paraphrased for this leaf.

- **Scriptural elements** take the Douay–Rheims (Challoner) as registered
  (`edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581`;
  verse texts `…verse-text-21-psalms-578f023d`, `…-32-daniel-8954f60d`,
  `…-56-ephesians-10c79be0`, `…-50-john-27b8f3ed`, each SHA-256 recomputed and
  matched), at the Missal's Vulgate loci. Its canonical verses do **not** carry
  the Missal's form at:
  - the Introit antiphon (a cento the Douay verses at Dan 3:31, 29 and 35 do not
    carry; the closing clause stands in the Douay at Dan 3:42–43);
  - the Epistle's liturgical address (the Douay reads *See therefore, brethren,
    how you walk circumspectly*);
  - the Gradual's *illis* (the Douay's *thou givest them meat in due season*
    renders either form and is usable as it stands);
  - the Alleluia's *psallam tibi, glória mea* (the Douay gives *I will sing,
    and will give praise, with my glory*);
  - the Gospel's liturgical opening (the Douay's v. 46 begins *He came again
    therefore into Cana of Galilee*);
  - the Offertory's *tui* (the Douay gives *when we remembered Sion*); and
  - the Communion's *Meménto … Dómine* and shortened close (the Douay gives *Be
    thou mindful of thy word to thy servant, in which thou hast given me hope.
    This hath comforted me in my humiliation: because thy word hath enlivened
    me*).

  Where the Douay cannot carry the Missal's form, the Latin is given with a
  description of the difference, or the Douay verse is given as the verse and
  identified as such; nothing is composed to fill the gap.
- **The Sunday's three orations** take the 1861 Cummiskey hand missal,
  `edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861`, under
  *XX. SUNDAY after PENTECOST*, printed pp. 448–450. Two tracked payloads carry
  the same wording, word for word: `…philadelphia-1861.temporal-orations-en`
  (physical lines 170–172; passages `…post-pentecosten-20.collect` and
  `…post-pentecosten-20.secret` verified 2026-10-05, and
  `…post-pentecosten-20` inspected for all three) and
  `…philadelphia-1861.pentecost-20-checked-english`. The chosen route is
  `temporal-orations-en` with its passages, because it alone carries passage
  records. The registered scan `…philadelphia-1861.ia-scan-pdf` (SHA-256
  `85034c90d5cbfe891f4359fb2faff907d217dbd11a30458b55e4c48eae028898`, re-hashed
  and matched) was read in this stage on PDF pp. 457–459 rendered at 200 dpi
  (native 600-ppi JBIG2), and all three prayers stand there in the payloads'
  wording:
  - Collect, p. 448: *Favourably grant, we beseech thee, O Lord, thy servants
    both pardon and peace; that, being cleansed from the guilt of all their
    offences, they may serve thee with secure minds. Thro’.*
  - Secret, p. 449: *May these mysteries, O Lord, we beseech thee, procure us a
    heavenly remedy, and cleanse away the vices of our hearts. Thro’.*
  - Postcommunion, pp. 449–450: *That we may be worthy of thy sacred gifts, O
    Lord: grant, we beseech thee, we may always obey thy commandments. Thro’.*

  The same pages print the 1861 book's own English for the whole Mass. It is not
  the route for the scriptural elements; two of its forms are recorded so that
  no one takes them for the Missal's sense: the Offertory *when we remembered
  thee, O Sion* and the Communion *Remember, O Lord, what thou saidst to thy
  servant, and by which thou gavest me hopes: this hath comforted me in my
  distress.* Its Introit English (*Whatever thou hast done to us, O Lord, thou
  hast done by a just judgment …*) renders the Missal's cento and is the only
  historical English of it located; using it would quote the 1861 book under its
  own attribution, not the Douay (`research/scope.md` § 9).
- **The three commemorated orations** take the Lasance *New Roman Missal*,
  Benziger revision of 1945,
  `edition.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945`,
  through the tracked `…maternity-checked-english` payload (SHA-256
  `661c88187ac134bbfb0f542c42e9f65dfed9fc77f29da06f18df9d547d620fa9` recomputed
  and matched) and its passage. The registered scan
  `…benziger-revised-1945.internet-archive-facsimile-pdf-6cf3c3d0` (SHA-256
  `6cf3c3d01b853bc4a35c1cc9b0a4e54a0489a5ccf5d9a742bb681ac10608ce70`, re-hashed and
  matched) was read on PDF pp. 1234, 1236 and 1237 at 150 dpi; the three prayers
  stand there in the payload's wording (printed pp. 1233, 1235, 1236). Its
  Postcommunion renders *cæléstis remédii* as *of Him, Who is our heavenly
  healing*; that is the translators' interpretation, and a study that quotes it
  says so.
