# Expected Missal targets: source and scope review, 19 October 2026

The accompanying [inventory](missal-expected-targets-v1.toml) enumerates
source-backed identities independently of the texts currently served. It does
**not establish a complete target-book inventory for any of the three families**.
An unresolved book extent is different from a known target whose text is
unavailable. The inventory retains both; an unenumerated boundary contributes
neither zero nor the held-row count to a denominator.

The units are heterogeneous and must be counted by kind and slice. A celebration,
a form/cycle composition, a Common section heading, a Preface, and a ritual unit
are not interchangeable text slots. A complete bounded enumeration does not
establish exact target wording, all internal alternatives, publication rights,
or whole-book completeness. `complete-within-slice` describes the explicitly
named source extent, including a historical witness extent where stated.
`target-correspondence-unresolved` prevents that witness from being silently
promoted into the target edition.

Latin is the target-book language. English in each slice's requested language
scope means separately attributed English coverage, not an assertion that an
approved translation exists or is held. The selected English witness must retain
its own relation, identity, availability and publication basis. This inventory
contains metadata and source locators, not liturgical text bodies or a grant of
publication permission.

## Fixed-calendar identity slices

The identity source is the source-backed calendar-reference publication, reached
through `tools/calendar-spine derive --json`, not `propers.yaml`. The latter is
consulted only to test whether an independently enumerated identity is currently
represented. References to existing registry or Mass keys are joins, not new
evidence of an appointment or target text.

For 1962, the controlling publication's
[calendar inventory](../../gpt/liturgy/roman-rite/1962/reference/liturgical-calendar/research/calendar-inventory.md)
records its full fixed-calendar extent as 275 civil-date rows, collated against
the target facsimile's artifact pp. 47–55, printed XLV–LIII. The two source
sections explicitly distinguish a principal celebration from attached
commemorations after semicolons. Splitting those clauses gives 336 distinct
identities: 231 celebrations and 105 commemorations (44 standalone and 61
attached). Companions within one celebration remain one identity. Christmas's
Saint Anastasia is specifically a commemoration at the second Mass.

That last identity demonstrates why held rows cannot define expectation:
`roman-1962/propers.yaml` retains Saint Anastasia only in its explanatory header
and Nativity note, while the source calendar expressly appoints it. The inventory
keeps `1962-12-25-comm` as an expected identity even though that join has no held
Mass row. This is an identity finding, not permission to invent its orations.

The postconciliar publication's
[calendar inventory](../../gpt/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/reference/liturgical-calendar/research/calendar-inventory.md)
names its canonical row owners and audits 222 singular General Calendar rows
on 202 distinct dates. Coequal memorials are separate source-authored rows;
companions within one celebration are not. This slice inherits the publication's
**17 July 2026 normative cutoff**, not a fresh October amendment check. Its
separate 40 temporal range rows and U.S. overlay are not silently folded into
this fixed-calendar identity denominator. Neither fixed-calendar slice asserts
the number of formularies, appointed text slots or options needed for its days.

## Forms, cycles and the Ordinary

The [postconciliar proper registry](../../../guidance/liturgy/postconciliar-propers-registry.md)
explicitly writes 184 baseline PC-S composition keys. The inventory preserves
that bounded queue and its Sunday-cycle/form distinctions. It does not derive
unlisted Cartesian combinations. The
[U.S. edition disposition](../../gpt/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/registry/formula-dispositions.md)
expressly withholds assignment of the registry total to that edition and leaves
unlisted keys not evaluated. Consequently every imported composition retains
unresolved target correspondence. The uncollated U.S. All Souls reading pool,
conditional Scrutinies, weekday fallbacks and replacement combinations remain
explicit boundaries. PC-T03 is an Easter Vigil alias, not another composition.

A separate body reading of the registered 2002 witness, artifact pp. 82–303,
enumerates 185 named temporal Mass forms: Advent 29, Christmas season 19,
Lent 39, Holy Week 6, Easter season 54, and Ordinary Time with its concluding
solemnities 38. These are source forms, not a derivation from PC-S keys or a
civil-year calendar. The 34 Ordinary Time forms are reusable on weekdays;
weeks I and XXXIV explicitly redirect their Sunday appointments. No Saturday
of Advent III or Cartesian weekday/cycle combinations were invented.
Six Christmas weekday forms have paired Collect choices before/after Epiphany,
which are kept as prayer sets rather than extra complete Mass forms.

The same body pass records nineteen positive referrals, five exceptional rites,
twenty-two ritual units and thirty-one prayer sets at explicitly partial scope.
The Easter Vigil and its Mass have separate granularity; Good Friday and the
Holy Saturday observance are not Mass forms. The source expressly excludes Mass
before the Holy Saturday Vigil. Readings, internal options, ritual actions and
all proper/Ordinary slots require finer inventories beyond these named forms.

The Proper of Saints body, artifact pp. 415–535, independently supplies 212
entries under 207 celebration headings: 85 with all five printed core proper
roles, six three-prayer sets and 121 own-Collect categories. Three vigil/day
pairs and All Souls forms 1–3 account for the expansion. Every entry has one
own Collect heading; those 212 headings independently cross-check membership.
Christmas and January 1 belong to the temporal body. This does not equate the
212 source entries with the 222 identities of the later calendar publication.
Thirty printed Preface referrals and six Presentation rite options are separate
targets; they do not become additional owned Prefaces or complete Masses.

The already extracted sanctoral markers also supply 564 explicit core-role
appointments: 212 Collects, 91 prayers over the offerings, 91 postcommunions,
85 entrance antiphons and 85 Communion antiphons. Each target retains its exact
source heading line; its locator separately identifies where the owning form
begins, without pretending that opening page is the slot's page. Alternatives
under one heading and imported Common/seasonal choices remain distinct work.

The source-backed
[postconciliar sequence inventory](../../claude/liturgy/roman-rite/postconciliar/2008-latin-2011-us-english/ordinary/00-order-of-mass/research/sequence-inventory.md)
provides positive identities for greetings, Penitential Acts, sprinkling, Creeds,
the four principal Eucharistic Prayers, priestly preparation alternatives,
dismissals and blessing classes. These include choices beyond the current
selectors. Blessing classes do not enumerate every numbered blessing; the later
2002 body slices now supply the main section's twenty blessings and twenty-eight
prayers over the people. Roman Canon inserts, other internal alternatives and
supplementary Eucharistic Prayers still need their own source-defined detail.

The 1962 Mass-form slice names the hierarchical taxonomy of general rubric 271:
Low and sung, the Solemn/sung-without-sacred-ministers subdivision, and pontifical
qualification. It is not five mutually exclusive Mass configurations. The source
locator is preserved in the existing
[assembly rubric index](../../gpt/liturgy/roman-rite/1962/reference/assembling-the-mass/research/rubric-index.md).
Conventual status is a separate axis. A/B/C and I/II are inapplicable to the
older books, not missing targets that may be reconstructed from the modern one.

## Prefaces, Commons and exceptional rites

The registered 1962
[Preface passage](../works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/praefationes.toml)
enumerates sixteen identities in printed pp. 223–298 / artifact pp. 304–379.
The passage records an OCR structural reading on 25 July 2026, with provisional
orthography; this review does not claim a fresh image collation. Different chant
tones and unnotated repetitions do not multiply textual identity.

The registered 2002
[main Preface passage](../works/catholic-church/missale-romanum/editions/vatican-typica-tertia-2002/passages/ordo-missae-praefationes.toml)
independently enumerates fifty headings at artifact pp. 311–346. It explicitly
excludes Prefaces printed with proper formularies elsewhere. Those fifty are a
defensible main-section denominator, not a collation of the 2008 reprint or
English expression. A subsequent complete reading of the Preface index at
artifact pp. 818–821 identifies 98 contextual entries. Fifty refer to the
already enumerated main section. Two further entries repeat exactly the same
indexed body locus: joint ordination refers to diaconal ordination at printed
p. 1012, and the dedication anniversary repeats the second dedication Preface
at p. 1064. Excluding those two repeats leaves 46 additional appointments,
entered separately, and 96 indexed appointments across the two slices. This is
not a count of 96 unique formula wordings: distinct printed loci can carry the
same formula, and the source's index itself has textual and pagination defects.
Twelve temporal body Prefaces were independently located and attached to these
index identities, without creating duplicate target rows. Fifteen sanctoral
body occurrences likewise remain evidence of appointments, rather than an
additional fifteen entries on top of the index inventory.

A second source pass opened the complete, 828-page
[registered 2002 digital reproduction](https://media.musicasacra.com/books/latin_missal2002.pdf)
through the web reader, then inspected its index and the complete body sections
for Commons, ritual Masses, various needs, votive Masses and the dead. The index identifies Common
subdivisions, additional Eucharistic Prayers and a one-minister Order of Mass.
It also locates ritual, votive and funeral material outside the calendar.
These positive headings enter bounded slices. The subsequent body reading
establishes the following separate entry inventories; index leaves cannot stand
in for every formulary:

| Source body slice | Artifact pages | Source-defined entries |
| --- | --- | --- |
| Commons | 536–593 | 60 numbered formularies beneath 33 section headings |
| Ritual | 593–667 | 28 formularies, one alternative prayer set, two referrals |
| Various needs | 667–724 | 49 formularies, ten prayer sets, ten Collect categories |
| Votive | 724–749 | 23 formularies and one Marian Common referral |
| Dead | 750–777 | 16 formularies, twenty prayer sets, six Collect categories |

These five body slices contribute 226 metadata identities. Their whole bounded
sections were read in overlapping extraction windows; numbered/lettered
subdivisions were checked in surrounding body context. The source locators use
one-based artifact pages and web-extraction lines because the source's printed
pagination differs. The existing 33 Common headings remain section identities,
not another 33 Masses. All new body identities retain unresolved correspondence
to 2008; a complete 2002 witness section does not settle the target edition.

The Common sequence comprises dedication (2), Mary (11), martyrs (14), pastors
(12), doctors (2), virgins (4), and saints (15). Ritual Confirmation C is an
alternative three-prayer set. Anointing refers to the Mass for the sick;
institution of lectors/acolytes refers to ministers of the Church. Renewal of
vows appoints antiphons by reference but supplies its Mass prayers. Various-needs
categories 11 A–C and 39 are prayer sets; categories 21–24, 34–37 and 44 are
Collect-only, while 30 B contains two Collect choices. Votive Mary A refers to
the appropriate seasonal Common. These referrals remain explicit identities
rather than guessed combinations of their possible targets.

The dead section has funeral entries A–F, with E subdivided 1–2; anniversary
A–E; daily Masses for one deceased 1–5 and several/all deceased 1–9; and diverse
prayers 1 A–C, 2 A–B, 3 A–B, then 4–12. Some lettered entries are prayer sets,
and diverse-prayer categories 5–10 supply only Collects. The section explicitly
permits interchange and grammatical adaptations, so forty-two named entries
cannot be promoted to forty-two full Masses or a finite Cartesian total.

A further Common body pass identifies 403 explicit contextual slot options:
94 entrance antiphons, 78 Collects, 63 prayers over the offerings, 93 Communion
antiphons, 62 postcommunions and thirteen explicit Preface appointments. Each of
the sixty forms has all five core proper roles. Alternatives introduced by
`Vel` and the separately labelled papal/episcopal Collects retain distinct
option identities and precise source loci. The Preface appointments comprise
two printed dedication Prefaces and eleven Marian references; referenced
alternatives are not silently expanded. These are contextual appointments, not
403 unique texts. General-rubric choices, cross-references outside these roles,
grammatical substitutions and exact 2008 correspondence remain explicit limits.
The Common introduction at artifact pp. 535–536 expressly permits interchange
within a Common, seasonal prayers for memorials, and grammatical adaptation;
its temporal/circumstantial restrictions remain controlling. Those permissions
do not create a finite list of all assembled combinations.

The main Ordinary's blessing section separately supplies twenty numbered solemn
blessings and twenty-eight prayers over the people, at artifact pp. 370–383.
The source's prayer 14 is concatenated after the previous conclusion in the text
extraction; its printed number was retained. These complete bounded sequences
do not enumerate blessings or prayers appointed elsewhere in the book.

The appendices add fifty-five positive source structures: eleven index-only
chant categories, three rites, four water/salt prayer options, eight sprinkling
chants, eleven sample universal-prayer sets, four preparation units, seven
thanksgiving units, six supplementary Eucharistic-Prayer forms and the
single-minister Mass form. The last seven refine previously recorded rite-level
identities; they are not seven additional liturgical celebrations. Source bounds
are artifact pp. 383–414 and 777–812, with the chant index at pp. 827–828.
Appendix I's music is absent from the accessible text body, so its eleven index
headings do not establish its musical variants. Numbered intentions and seasonal
inserts inside these forms remain a finer inventory boundary.

Three children's Eucharistic Prayers printed in the 2002 appendix are retained
only as named `inapplicable` boundaries. The official 2008 variation list,
printed p. 379 / artifact p. 61, explicitly removes that appendix from the 2008
book. They contribute no expected target rows. This bibliographic exclusion
makes no claim about their liturgical use beyond the target book.

Internal alternate Collects and antiphons beyond the enumerated Common roles,
proper Prefaces and Eucharistic Prayer inserts, other blessings, conditional
appointments, and further semantic slots remain separate work. These are
per-entry structural unknowns; the named body entries
themselves are now enumerated within the five stated source sections. This was a
bounded reading of that registered source's delivery, not a fresh hash check or
acquisition receipt; its existing artifact and edition limitations still apply.

The registered official
[2008 variation list and Supplementum](../works/holy-see/variationes-et-additiones-missalis-romani-2008/editions/latin-notitiae-503-504/segments/notitiae-pages-368-387.toml)
also opened through the web reader. A separate bounded slice records sixty
positive 2008 target identities. It covers the extended Pentecost Vigil's two
opening modes; its reading, psalm, response, prayer and dismissal appointments;
conditional Vespers actions; explicit referrals; the September 8 Prayer over the
Offerings; an alternative Prayer over the Offerings for Marian Common I.1; and
the Collects and Common referrals of Pio, Juan Diego and Guadalupe. These have established identity
from the official 2008 publication itself. Their language availability and
publication status are separate questions. The three general dismissal additions
already occur in the Ordinary-option inventory and are not counted again here.

The official notice and the existing Ordinary source audit explicitly limit the
variation list: it is directed to changes affecting translation, while further
presentation and textual corrections are unlisted. Its silence cannot establish
exact 2008 correspondence for every 2002 row. The Supplementum slice closes
that publication's appointment/referral extent, including all four Old Testament
readings and their explicit response options, six post-reading prayer alternatives,
the apostolic reading, two opening modes, and the Vespers actions specified in
nn. 1–13. Biblical numbering follows the source. A response group may instead
be replaced by silence; the shared prayer invitation and ritual pause remain
separate identities, as does the shared response to the six post-reading prayer
options. Repeated use of a shared prayer does not multiply its target,
and permitted similar admonition wording does not imply a finite list of paraphrases.

References to the ordinary Vigil Mass, Lectionary and Hours remain explicit
referrals. Their owning editions still need downstream slot inventories; no
familiar Gospel, psalmody or ordinary text was supplied from memory. This
distinguishes a complete bounded supplement inventory from a complete assembled
Vigil or entire 2008 book.

The 1962 exceptional-rite subset combines five precedents to Mass explicitly
named in the registered reading of rubric 424 with the separately collated
holy-water preparation/sprinkling record. Other consecrations mentioned by the
rubric were not guessed into individual targets. The subset is not an exhaustive
inventory of exceptional rites or their internal texts.

## Pre-1955 evidence and the unavailable denominator

**Superseded in part, 19 October 2026.** The pre-1955 recension now has an
accepted witness and a section inventory; see "The pre-1955 witness: section body
inventory" below. Its Holy Week slices replace the two witness slices described
here. The paragraphs that follow record the earlier state.

The target remains `roman-1920`, the 1920 Vatican typical edition. The positive
Holy Week entries come from the explicit witness-level structure of
[roman-holy-week-acts-v1.toml](roman-holy-week-acts-v1.toml): four celebration
identities and thirty-eight units at their own OCR loci. The tracer itself
limits its extent; it does not claim every unit of those rites. Its witnesses
are the 1862 Pustet and a later composite whose body is dated 1951–1954. Some
tracer rows attest two witnesses but give a locus in only one; this inventory
retains that bounded locator rather than inventing a second one.

The eleven Prefaces independently enumerated from the 1861 Cummiskey witness's
heading rows establish that hand missal's section only. They are not the 1920
altar book's denominator. Every pre-1955 positive target therefore retains
unresolved target correspondence. No 1962 effective-calendar inheritance was
used to manufacture a pre-1955 expected list.

The [acquisition audit](missal-acquisition-audit-v1.toml) and
[recension coverage](../calendars/roman-pre-1955/propers.yaml) identify the
missing exact 1920 impression and the known misidentification of the composite.
The registered Mame book is a genuine 1922 conformed printing; its identity
cannot be changed into a 1920 typical impression to close this gap.

## The complete 1962 facsimile: section body inventory

The registered
[CMAA facsimile](../works/catholic-church/missale-romanum/editions/vatican-typica-1962/artifacts/cmaa-facsimile-pdf/artifact.toml)
was acquired whole on 19 October 2026. Its SHA-256 matches the registered value,
`648fdb8f…3518a`, and it has 82,815,941 bytes and 1,088 artifact pages. Artifact
p. 2 carries the promulgating decree. The typical edition ends at p. 1073 with
*FINIS EDITIONIS TYPICAE*. Pages 1074–1081 are a separately headed *Appendix ad
Missale Romanum*, and pp. 1082–1088 are the alphabetic index of feasts. Section
lanes read the embedded text of their extents and checked page images wherever a
heading, a marginal number or a seam was doubtful. They derived identities from
the book alone. Held propers, Mass keys and implementation selectors were not
consulted. The payload stays outside the repository; this record holds metadata
only.

The inventory adds 35 slices, 7,623 targets and 28 boundaries for `roman-1962`,
after the independent review corrections recorded below.
Every artifact page now belongs either to a positive section slice or to an
explicit extent boundary:

| Section | Artifact pp. | Printed pp. (marginal units) | Owner | Status |
| --- | --- | --- | --- | --- |
| Title page, decree, bulls | 1–9 | –; I–IX | extent boundary | inapplicable |
| General rubrics | 10–34 | X–XXXVI | extent boundary; nn. 271, 424 in existing slices | unenumerated |
| Incensation diagrams | 35–38 | unnumbered | extent boundary | inapplicable |
| *De anno*, computus tables | 39–46 | XXXVII–XLIV | extent boundary | inapplicable |
| Calendarium | 47–55 | XLV–LIII | existing fixed-calendar slice | complete |
| *Ritus servandus* | 56–67 | LIV–LXV | `ritus-additional-text-appointments` | complete after Ordo deduplication |
| *De defectibus* | 68–70 | LXVI–LXVIII | extent boundary | unenumerated |
| Preparation and thanksgiving | 71–81 | LXIX–LXXIX | `preparation-thanksgiving-*` | complete |
| Temporal: Advent to Saturday after Ash Wednesday | 82–144 | 1–63 (1–427) | `temporal-pre-holy-week-*` | forms and slots complete; appointments partial |
| Temporal: Lent I to Saturday after Passion Sunday | 144–210 | 63–129 (428–825) | `temporal-lent-source-forms-slots` | complete |
| Holy Week to the Easter Vigil Mass | 211–296 | 130–215 (826–1012) | `temporal-holy-week-source-enumeration` | complete |
| Ordo Missae, Prefaces, Canon | 297–409 | 216–328 | `ordinary-*`; existing Preface slice | complete |
| Easter Sunday to the last Sunday; *Tabula orationum* | 410–508 | 329–427 (1140–1808) | `temporal-easter-through-last-sunday`, `tabula-orationum` | complete |
| Proper of Saints | 509–808 | 428–727 | `sanctoral-*`, `purification-rite` | forms complete; slots and referrals partial |
| Commons, votives, the dead, absolutions | 809–944 | [1]–[136] (4175–5200) | `body-*` | forms complete; slots partial |
| Propers for certain places | 945–1026 | [137]–[218] | `local-proper-forms` | complete |
| Additional local Commons | 1027–1038 | [219]–[230] | `local-additional-commons` | complete |
| Holy-water blessing and sprinkling | 1039–1041 | [231]–[233] | `holy-water-units` under the existing rite | complete |
| Chant appendix | 1042–1073 | [234]–[265] | `appendix-chant-options` | complete |
| Bound *Appendix ad Missale Romanum* | 1074–1081 | [266]–[273] | `bound-ritual-appendix` | complete |
| Index | 1082–1088 | [274]–[282] | extent boundary | inapplicable |

The only shared page is p. 144. It ends the Saturday after Ash Wednesday at
marginal 427 and then opens Lent I at 428. The marginal numbering is continuous
across the temporal sections: 1–427, 428–825, 826–1012, the Ordinary's own
numbers, and then 1140–1808. Page 296 ends the Vigil Mass, p. 297 opens the
Ordo, and p. 410 resumes with Easter Sunday. Page 508 ends the *Tabula* and
p. 509 opens the Proper of Saints. Page 944 ends the absent-body absolution and
p. 945 opens the local propers. The table refers to slices by their names
without the `roman-1962-` prefix. A check confirms that every target locus falls
within its section's extent.

`complete` means `complete-within-slice` at the granularity each slice declares.
The kinds are not interchangeable and must never be summed into a text total:

| Slice | State | Targets by kind |
| --- | --- | --- |
| `temporal-pre-holy-week-forms` | complete | form 39 |
| `temporal-pre-holy-week-slots` | complete | slot 427 |
| `temporal-pre-holy-week-appointments` | partial | slot 58, ord-opt 18, referral 11 |
| `temporal-lent-source-forms-slots` | complete | slot 436, form 36, ord-opt 16, referral 7 |
| `temporal-holy-week-source-enumeration` | complete | slot 219, rite-unit 31, celebration 7, form 7, rite 5, ord-opt 3 |
| `temporal-easter-through-last-sunday` | complete | slot 739, form 60, referral 4 |
| `tabula-orationum` | complete | slot 30, prayer-set 10 |
| `ordinary-text-blocks` | complete | slot 111, referral 13 |
| `ordinary-canon-and-preface-options` | complete | ord-opt 27 |
| `ordinary-musical-presentation-options` | complete | ord-opt 53 |
| `preparation-thanksgiving-entries` | complete | form 24 |
| `preparation-thanksgiving-slots` | complete | slot 92 |
| `ritus-additional-text-appointments` | complete | slot 9, ord-opt 4 |
| `sanctoral-body-forms` | complete | form 323 |
| `sanctoral-printed-slots` | partial | slot 2336 |
| `sanctoral-form-referrals` | partial | referral 164 |
| `sanctoral-preface-appointments` | partial | slot 44 |
| `purification-rite` | partial | slot 13, rite-unit 3, referral 1 |
| `body-commons-forms` | complete | form 24, prayer-set 17, common 4 |
| `body-marian-saturday-forms` | complete | form 5 |
| `body-votives-forms` | complete | form 32, prayer-set 18, ord-opt 6, referral 2 |
| `body-diverse-prayers-forms` | complete | prayer-set 37 |
| `body-dead-forms` | complete | prayer-set 25, form 3, referral 1 |
| `body-absolutions-forms` | complete | rite 2 |
| `body-commons-slots` | partial | slot 314, referral 32 |
| `body-marian-saturday-slots` | partial | slot 51, referral 4 |
| `body-votives-slots` | partial | slot 437, referral 26 |
| `body-diverse-prayers-slots` | partial | slot 111 |
| `body-dead-slots` | partial | slot 103, referral 9 |
| `body-absolutions-slots` | partial | rite-unit 21, referral 4 |
| `local-proper-forms` | complete | slot 650, form 66, referral 18, comm. 1 |
| `local-additional-commons` | complete | slot 90, prayer-set 12, form 6 |
| `holy-water-units` | complete | rite-unit 13 |
| `appendix-chant-options` | complete | ord-opt 34 |
| `bound-ritual-appendix` | complete | rite-unit 35, rite 16, slot 14 |

### Method and granularity by section

The **temporal** lanes assign every printed marginal unit to one semantic role.
Introit with its psalm, Gradual, Tract and paired Alleluia each remain one
compound appointment. Their verses and repetitions are not multiplied. Separately
printed long and short forms of the Ember Saturdays are distinct formularies.
Unnumbered Preface appointments, Credo directions, Passiontide omissions,
*Flectamus genua* directions, commemoration-use rubrics and conditional
ordination-oration referrals are kept as separate positive targets. Holy Week is
counted in named semantic blocks. The consecratory prayer for the baptismal
water is one block, and the candle-inscription and incense clauses remain parts
of their formulas. Rites referred to the Pontificale or Rituale are retained as
named referrals; their internal texts are not counted.

The Lent sub-lane's first enumeration was generated from formulary templates and
had no evidence record. It was therefore verified independently. The role
headings in the raw extraction were segmented at the 36 formulary headings.
Every formulary's OCR role sequence is a subsequence of the enumerated one: 20
match exactly, and 16 lack one or two OCR headings, 20 headings in all. The one
extra token is an "ad Introitum" phrase inside the Passiontide rubric. Of the
398 marginal numbers, 350 are visible in a monotone OCR run, and their page
locators agree. The 48 invisible numbers and the 20 missing headings were all
confirmed on page images. One locator was wrong: marginal 577 is on p. 166, not
p. 167.

The **Ordinary** slices enumerate prayer blocks and dialogue turns, textual
wording alternatives in the Preface section and the Communicantes, and musical
presentations. The **preparation** slices enumerate 24 entry forms and 92 slots.
The *Ritus servandus* adds thirteen appointments not already owned by the Ordo.
The **sanctoral** lane swept all date headings and checked damaged headings on
images. Its role extraction is positive but partial, because the OCR damages
some role headings; their loci are listed in the lane evidence. The
**Commons/votive/dead** lane reconciles the own numbered units 4175–5190
contiguously and adds 21 semantic units for the two absolution rites. The
**local and appendix** lane separates the conditional local book, the local
Commons, the holy-water units, the chant options and the bound appendix.

### Cross-checks

- **Formularies.** Every civil date bearing a celebration in the existing
  fixed-calendar slice has a printed formulary heading, in the sanctoral slice or
  in the temporal Christmas–Epiphany cycle. Every sanctoral date heading falls on
  a calendar celebration or commemoration date. Per-date counts reconcile
  except in two expected cases. First, the Apostle commemorations of 25 January,
  22 February and 30 June are printed inside the feast. Second, All Souls has
  three Masses.
- **Prefaces.** General rubrics nn. 484–499 (artifact p. 32) name sixteen
  Prefaces. The Preface section, artifact pp. 304–379, prints fifteen in the
  solemn tone (including the Chrism Mass), fifteen in the ferial tone and
  fifteen without chant: together exactly the sixteen existing identities. The
  solemn-tone appendix, pp. 1044–1071, has fourteen tones of existing Prefaces
  and adds none. Every Preface appointment found in the text names one of the
  sixteen. *Vere dignum* also occurs in the Exsultet (p. 268) and the
  baptismal-water blessing (p. 281), rite texts sung in the manner of a Preface
  and owned by Holy Week rows, not Mass Prefaces.

### Overlap with existing rows

No new slice, target or boundary ID collides with an existing one. Five
fragment rows repeated an identity already present and were not added:

| Not added | Existing owner | Reason |
| --- | --- | --- |
| Ash Wednesday blessing and imposition of ashes (pp. 136–138) | `roman-1962.rite.ash-blessing` | same rite named by rubric 424; the emptied ash-rite slice was dropped |
| Solemn palm procession (pp. 211–216) | `roman-1962.rite.palm-blessing` | same rite |
| Paschal Vigil before Mass (pp. 263–292) | `roman-1962.rite.easter-vigil` | same rite |
| 29 December commemoration of Thomas | `roman-1962:commemoration:1962-12-29-comm` | same calendar identity |
| 31 December commemoration of Sylvester | `roman-1962:commemoration:1962-12-31-comm` | same calendar identity |

The February 2 body sections are units of the existing candle rite. They cover
the blessing, the distribution and the procession, plus a referral permitting
the simple form. They are not four further rites. The holy-water units likewise
sit under the existing sprinkling rite. Preface appointments in formularies,
the solemn-tone Prefaces and the Preface wording options are separate kinds from
the sixteen Preface identities. The formularies of the temporal Christmas cycle
and of the Proper of Saints are form-level targets, distinct from the
fixed-calendar celebration identities. This follows the postconciliar
precedent, where calendar rows and 2002 body forms coexist.

`form_id` here names the parent target, as in the 2002 sanctoral core-slot
slice. On rows without a calendar join it is inert in the coverage validator.
No row carries both `form_id` and `calendar_mass_key`. Bare local keys were
mapped to their parent row, and self-references were dropped. So was the value
`main` on sanctoral form rows: it is meaningful only as a join to a held Mass.
No calendar joins were added. The only kinds with a joining precedent are
celebration, commemoration and exceptional rite. Five Holy Week day headings
correspond by name to held Masses, but the correspondence is not mechanically
checkable. Holy Thursday and Holy Saturday do not correspond one to one.

### Limits

These are structural identities, not wording collations. Latin wording, English
witnesses and publication rights remain separate questions. Incipits in labels
identify units; they are not verified text. Several kinds of appointment are not
expanded: imported Common bodies, referred Masses, occurrence-dependent
commemorations and general-rubric appointments. Each such gap is an explicit
`unenumerated` boundary. The general rubrics (pp. 10–34) and *De defectibus*
(pp. 68–70) are unenumerated extents. The bound appendix excerpts the Rituale
and Pontificale; it is not those books. The local propers are conditional
local-book use, not universal calendar membership.

The whole-book slice remains `unresolved`, but its form and Preface boundaries
are retired. Retirement was first deferred, because the sanctoral and Commons
enumerations rested on their first lanes' image checks and the Preface search
ran over extracted text. An independent review on 19 October 2026 then
compared the targets with three self-derived text checks (date headings, rank
lines and Introit markers), the book's alphabetic index, and 238 page images,
115 of them in the sanctoral and Commons sections. It found no missing and no
phantom formulary heading, and exactly sixteen Prefaces. It also found kind
inconsistencies, now corrected:

- The paschal sub-variants of the Peter and Paul and the Apostles votive Masses
  (pp. 862, 864) were split out as forms; elsewhere the same device stays inside
  one form, and the book's index lists each Mass once. They are now
  `form-referral`.
- The numbered marriage-anniversary heading (p. 885) is now `form`, as
  referral-only headings are in the sanctoral and local propers.
- The six full local Common Masses (pp. 1027–1038) are now `form`, not
  `common`.
- Two Preface appointments missed by the OCR (pp. 598 and 607) were added to
  the partial sanctoral Preface-appointment slice.

The whole-book Mass-formulary denominator is the `form` rows of the temporal,
sanctoral, body Commons/Marian/votive/dead, local-proper and local-Commons
slices: 601. The rubric n. 271 taxonomy (5) and the devotional preparation and
thanksgiving entries (24) share the kind but are not formularies; oration-only
and rite headings are `prayer-set` and `exceptional-rite` rows. The review's
limit is stated plainly: a heading the OCR lost on its date line, rank line,
Introit and index entry at once, on a page not imaged, cannot be ruled out; for
fixed-date feasts the calendar check confines that risk to non-calendar
headings. Text slots, Ordinary options, commemorations, Commons as a kind, and
exceptional rites keep explicit `unenumerated` boundaries. No whole-book
text-slot denominator is asserted.

Known presentation inconsistencies are retained rather than silently
normalized. The kind `common` holds four additional-reading pools, while the
Common Masses are `form`. Holy Week
days carry both a `celebration` and a `form` target, while other temporal days
carry only `form`. Three identifier styles coexist. None of these is summed
across kinds. The parent-row use of `form_id` remains a latent schema hazard:
the coverage validator reads that field as a join to a held Mass's forms, so a
future row carrying both `form_id` and `calendar_mass_key` would be misread.

## Twenty 2002 appointments positively named by the 2008 variation list

The official list of *Variationes et additiones in reimpressione emendata
"Missalis Romani", editionis typicae tertiae* is the already registered
[segment](../works/holy-see/variationes-et-additiones-missalis-romani-2008/editions/latin-notitiae-503-504/segments/notitiae-pages-368-387.toml)
of Notitiae 44 (2008), nos. 503-504, artifact SHA-256
`74c8d1740284984d0f4d64b2223edf805dadfa55aec8a92f8cfba9ab901eca0f`. Its
entries cite pages of the 2002 typical edition, and its abbreviations note
(printed p. 368, artifact p. 50) defines a.i., a.c., c., s.o. and p.c. The
notice and list were re-read on 19 October 2026 from page images of printed
pp. 367-368, 372-375 and 380 (artifact pp. 49-50, 54-57 and 62), not from
extracted text.

Twenty existing targets now carry established 2008 identity because a list
entry names the appointment itself:

| Slice | Rows | List pages (printed / artifact) |
| --- | --- | --- |
| `postconciliar-2002-common-appointed-slots` | 8 | 375 / 57 |
| `postconciliar-2002-sanctoral-core-slots` | 10 | 373-374 / 55-56 |
| `postconciliar-main-preface-section` | 1 (Easter Preface I) | 372 / 54 |
| `postconciliar-2002-prefaces-outside-main-section` | 1 (index D.4.II) | 380 / 62 |

Each join was made from content, not from page arithmetic. The 2002 witness
used for context is the registered digital reproduction, SHA-256
`0b458944824d2ee92854b9664f83e553af0342e0b15a9dc14b00e846405523d7`, which
does not print its source pagination. For every entry, the 2002 wording the
list replaces was searched across the whole reproduction. Its occurrence was
then read in context to confirm the form, the role heading and the option
number. Three joins depended on that reading:

- The phrase corrected at 2002 p. 797 occurs only in the Peter Julian Eymard
  Collect (reproduction artifact p. 473), not in the Eusebius Collect beside
  it.
- The one wording corrected at 2002 pp. 930 and 943 occurs twice: in the
  second Collect of Bishop 1 (artifact p. 565) and in the first Collect of
  Doctors 1 (artifact pp. 574-575). The list's page order matches the order
  of the two forms.
- The Lateran entry at 2002 p. 864 replaces the second Collect. The sanctoral
  target is the Collect heading, so the heading is established; the first
  alternative under it is not separately attested.

The D.4.II entry corrects the Preface index title at 2002 pp. 1309 and 1310.
Each page number is printed beside a bracketed second number, [1299] and
[1300]. The notice at printed p. 367 (artifact p. 49, read as an image) says
the 2008 book keeps the 2002 page numbers except in the concluding part and
the indexes, which move because the children's Eucharistic Prayers were
omitted. The bracketed numbers are consistent with that shifted 2008 index
pagination. The list itself does not label them. The correction covers D.4.II
and its repeated anniversary referral E.4, which together stay one target.
The same notice's statement that body pagination is unchanged also supports
reading the other nineteen entries' 2002 page references as 2008 loci.

**What this establishes.** The named appointment exists in the 2008 book. It
does not establish unchanged wording; each of these entries records changed
wording, citation, rubric or conclusion. It establishes nothing about an
unlisted neighbouring appointment, English correspondence or publication
rights. The notice at printed p. 367 presents the list as the variations
bearing most directly on translation work, after describing wider corrections
of accents, punctuation, red-black colouring and typography. The list's silence
about any other 2002 row is therefore still not attestation. Where this review elsewhere says all new body identities retain unresolved
correspondence to 2008, that statement is superseded for these twenty rows
only.

**What remains unresolved.** Two Common corrections are deliberately not
joined. At 2002 p. 915 the entry falls on a form boundary. At p. 961 it
supplies only a generic conclusion change, and no exact contextual join was
established. Other positively named list entries (ritual, needs, votive and
other entries) remain candidates for further narrow joins. No such join alters
`enumeration_state` or a 2002 source-extent count. The joined rows have no
`calendar_mass_key`, so their computed coverage state stays `unresolved`. The
change is to identity evidence, not to the held-row join.

## The selected U.S. 2011 edition's General Index

The new slice `postconciliar-us2011-general-index-headings` (recension
`roman-missal-en-us-2011`, territory US, language `en`) enumerates 210 leaf
headings of the General Index, printed pp. 5*-8*. The index belongs to the
Catholic Book Publishing 2011 U.S. altar edition and was read from the
publisher's preview, artifact pp. 2-5, SHA-256
`ab44fd0a3677874c78821934ddb460f12f75aea6172d2f1dd3ead6e98f2b2944`. All
four pages were read as images, and every heading's index page and indexed
body page were checked against them. A parent heading counts only through its
children when it has no page of its own or shares its first child's page
(the dedication anniversary, the Scrutinies). Various-needs categories 7 and
13 have their own pages and count beside their anniversary children.

| Index section | Headings | Kind recorded |
| --- | --- | --- |
| Proper of Time | 41 | celebration |
| Commons | 33 | common |
| Ritual Masses | 25 | form |
| Various Needs and Occasions | 54 | form |
| Votive Masses | 21 | form |
| Masses for the Dead | 21 | 8 form, 13 prayer-set |
| Appendices, Preparation, Thanksgiving | 8 | 2 ordinary-option, 3 exceptional-rite, 3 prayer-set |
| Single-minister Order and Appendix to the Order of Mass | 7 | 1 form, 6 ordinary-option |

By kind: 109 form, 41 celebration, 33 common, 16 prayer-set,
8 ordinary-option and 3 exceptional-rite. **The kind is the nearest permitted kind for an
index heading, not a granularity claim.** Twenty of the 41 temporal headings
group a Sunday with its week, a run of weekdays, or a whole season, and their
labels say so. Ritual, needs, votive and dead Mass headings are recorded as
`form`, the kind the 2002 body slices give those sections, although one may
hold several forms, a prayer set, or a Collect only, and the index does not
say which. These are
heading identities, never 210 Masses or formularies.

Two liturgical headings carry the index's own [USA] marker: various-needs
category 48/1, thanksgiving for the gift of human life (body p. 1165), and
Appendix VI, sample Penitential Act invocations (body p. 1316). Both are at
printed p. 8*.

**No double counting.** The slice sits in the same recension as
`postconciliar-temporal-composition-registry` but does not duplicate,
replace or reconcile its 184 PC-S composition keys. That slice counts
form/cycle compositions as `cycle`; this one counts index headings. The 33
U.S. Common headings correspond in name to the 33 Latin
`postconciliar-common-index-headings`. That is structural resemblance in
another recension, not 2008 correspondence and not a shared target. No target
asserts a held-row join.

**Explicit boundaries (all `unenumerated`).**

- The Proper of Saints appears in the index as twelve month headings only
  (body pp. 651-867). U.S. sanctoral celebrations are not enumerated by this
  preview.
- The Alphabetical Index of Celebrations (body p. 1335) is referred to but is
  not in the preview.
- The Index of Prefaces (body p. 1339) and the Prefaces section (p. 386) are
  absent, so no U.S. Preface identities or count follow.
- The main Order of Mass section headings (printed pp. 5*-6*) are structural
  divisions. Their option-level U.S. contents are not in the preview and are
  not counted.
- Full formularies, internal numbered or lettered forms, reading cycles,
  Christmas and Pentecost alternatives, and Scrutiny conditions are absent.
- No U.S. text slot is enumerated.

Front-matter documents are not Mass targets and are left out. The slice
records `complete-within-slice` for its stated extent only. It closes no
whole-book U.S. denominator.

## The Catholic Book Publishing preview as a registered source

The preview is now registered under
[`2011-english-us-catholic-book-publishing`](../works/catholic-church/missale-romanum/editions/2011-english-us-catholic-book-publishing/edition.toml):
one edition, one restricted artifact
(`publisher-sample-pdf-ab44fd0a`, 1,076,966 bytes, 15 pages) and one
version 2 passage (`general-index`, artifact pp. 2-5, verified 19 October
2026). The artifact was fetched whole from the Look Inside link on the
publisher's product page (ISBN 9780899420738, 1456 pages). The product page
response has SHA-256
`6ce566a896280e073464d6a1e755edba833dffff00bd8e3bc0f077a05e11aa3c`.

**What is established.** The title page (artifact p. 1) identifies the
English translation according to the third typical edition, for use in the
dioceses of the United States, approved by the USCCB and confirmed by the
Apostolic See. It names Catholic Book Publishing Corp., New Jersey, 2011. The
measured extent of the preview is: title page, the complete General Index,
two front-matter decrees, a plate, and body leaves at printed pp. 365, 378,
379, 507, 526, 729 and 1003.

**What remains unresolved.** The PDF was produced in 2018-2019 (QuarkXPress
metadata, created 2018-11-04, modified 2019-05-07). Its title page date does
not show that it reproduces an unchanged first impression, and the preview
carries no impression statement. The bytes are `restricted`: the publisher's
preview establishes the authority of the copy, not redistribution, and
nothing of it is retained. The record states that access limitation in plain
words. ICEL's conditional web permission is not claimed to reach this PDF or
any USCCB material in it. The 1456-page body, including the two further
indexes, is not acquired.

## The pre-1955 witness: section body inventory

On 19 October 2026 the maintainer decided that the files circulating as the
"1920 typical edition" are public domain for their 1920 content and may be
used. Every such file found is the registered
[Bonn 2004 *reimpressio*](../works/catholic-church/missale-romanum/editions/2004-bonn-palmarum-reimpressio-editio-28-iuxta-typicam-1920/artifacts/ia-reimpressio-pdf-b676ce5c/artifact.toml)
of a 28th edition conformed to the Vatican typical edition: 1,220 artifact
pages, SHA-256 `b676ce5c…a1d`. It is a 2003 typesetting with a clean text layer
of a printing of about 1954. It carries St Pius X (1954) and lacks St Joseph the
Worker (1955), so it witnesses the recension as it stood before the 1955 Holy
Week reform. The registered
[1922 Mame conformed printing](../works/catholic-church/missale-romanum/editions/1922-tours-mame-editio-quarta-iuxta-typicam/artifacts/ia-scan-pdf-9873693a/artifact.toml)
is the control.

Four section lanes read the book. Each derived identities from the witness
alone and image-checked seams and doubtful cases against both books:

| Lane | Artifact pp. | Slices | Targets | Boundaries |
| --- | --- | --- | --- | --- |
| Front matter, Kalendarium, rubrics, preparation, Ordo, Prefaces, Canon | 1–104, 375–454 | 11 | 739 | 6 |
| Proprium de Tempore and the pre-1955 Holy Week | 105–374, 455–582 | 4 | 2,613 | 4 |
| Proprium de Sanctis | 583–966 | 7 | 2,899 | 0 |
| Commons, votives, the dead, rites, blessings, local propers | 967–1220 | 23 | 2,023 | 6 |

Every artifact page belongs to a section slice or an explicit extent boundary.
The 45 new slices hold 8,274 targets. All of them are `established` on the
witness, and none carries a calendar join yet.

**Post-1922 additions.** 323 targets in twelve `…-post-1922-additions` slices
have no counterpart in the 1922 control; each absence was confirmed on Mame
page images or its printed index. An addition has no counterpart in the
corresponding universal part of the 1922 control; for local propers the
comparison is with Mame's local supplement. A move within the 1922 universal
book is a relocation, not an addition. A form whose formulary differs, such as
the Sacred Heart, is classed by its formulary. An addition is not necessarily
new text. St Gabriel, St John Leonardi and St Margaret
Mary had Masses with the same Introit in Mame's local appendix before entering
the universal Proper. The 1922 local Maternity Mass differs from Bonn's.

No witness or registered source prints an institution date, except St Pius X,
whose 1954 date is in the registered artifact record. Every other row therefore
says "date not established". The rubrics show that the book does not reflect a
single moment. *Additiones* tit. VI n. 4 adds the Sacred Heart and Christ the
King to the days that exclude ordered Collects, while the general rubrics' Credo
list names Canisius and John of the Cross but omits Bellarmine and Albert.
Rights follow the same split: the 2026-10-19 public-domain decision does not
reach text first published in 1931 or later (`guidance/missals.md` §5).

**Identities only in the 1922 control** are reported, not inventoried:

- the Octave of the Assumption on 22 August;
- Mame's separate *Pro S. Christophoro* heading on 25 July (p. 783). Bonn's
  Kalendarium still prints *Com. S. Christophori*, and its body carries the
  orations within St James (pp. 812–813);
- Mame's Sacred Heart formularies *Miserebitur* and *Egredimini*;
- Kalendarium commemorations of Agapitus, Melchiades, Anastasia and the Vigil
  of the Immaculate Conception. Bonn's body still prints all four:
  Anastasia, Melchiades, Agapitus (p. 852) and the vigil.

Some dates or ranks moved: Peter Nolasco, Hedwig and Gertrude; Agnes
*secundo*; the Vigil of St Lawrence; and the Commemoration of the Supreme
Pontiffs, 3 July in Mame and 4 July in Bonn. Holy Family, Hyginus and the
Sacred Heart sit in Bonn's temporal but in Mame's sanctoral.

**Integration dispositions.**

- The two Holy Week slices from the 1862 Pustet and the 1951–1954 composite are
  superseded and removed; their mapping is in the temporal subsection.
  [roman-holy-week-acts-v1.toml](roman-holy-week-acts-v1.toml) stays as the
  other-witness tracer.
- The 1861 Cummiskey Preface slice is kept as other-witness evidence. Its
  eleven Prefaces are a strict subset of the fifteen enumerated here and are
  never summed with them.
- The whole-book slice stays `unresolved`. The independent review below
  retired its form and Preface boundaries; the others stay `unenumerated`.

The four lane records follow as the next subsections. Counts in them are as
each lane reported, except where integration changed them.

### Pre-1955 front matter, Kalendarium, Ordinary, Prefaces and Canon

On 19 October 2026 the maintainer accepted the registered
[Bonn reimpressio](../works/catholic-church/missale-romanum/editions/2004-bonn-palmarum-reimpressio-editio-28-iuxta-typicam-1920/artifacts/ia-reimpressio-pdf-b676ce5c/artifact.toml)
of the 28th edition *iuxta typicam Vaticanam* (SHA-256 `b676ce5c…`, 1,220
pages) as the witness for `roman-1920`. It is a later conformed printing.
This section covers artifact pp. 1–104 and 375–454. It reads the clean
InDesign text layer, page by page, and checks headings, seams and doubtful
cases on page images. The registered
[Mame 1922 scan](../works/catholic-church/missale-romanum/editions/1922-tours-mame-editio-quarta-iuxta-typicam/artifacts/ia-scan-pdf-9873693a/artifact.toml)
is the control for what already stood in 1922. Its OCR is used only to locate
text; every absence claimed below was confirmed on a Mame page image. No held
propers, Mass keys or selectors were consulted. The rows hold metadata only.

The lane adds 11 slices, 739 targets and 6 extent boundaries. No identifier
collides with an existing row. No row carries `calendar_mass_key`, so the
validator classifies all 739 targets as `unresolved`, as intended.

| Slice | State | Targets by kind |
| --- | --- | --- |
| `kalendarium-fixed` | complete | celebration 284, commemoration 91 |
| `kalendarium-movable` | complete | celebration 5, commemoration 3 |
| `kalendarium-post-1922-additions` | complete | celebration 12 |
| `ordinary-text-blocks` | complete | slot 111, referral 13 |
| `ordinary-canon-and-preface-options` | complete | ord-opt 26 |
| `ordinary-musical-presentation-options` | complete | ord-opt 43 |
| `prefaces` | complete | preface 13 |
| `ordinary-post-1922-additions` | complete | preface 2, ord-opt 5 |
| `ritus-additional-text-appointments` | complete | slot 11, ord-opt 5 |
| `preparation-thanksgiving-entries` | complete | form 23 |
| `preparation-thanksgiving-slots` | complete | slot 91 |

Slice names omit the `roman-pre-1955-` prefix.

#### Extent and seams

| Artifact pp. | Content | Owner | Status |
| --- | --- | --- | --- |
| 1–13 | Title (Bonn 2004), blank p. 2, 1920 decree, bulls | `extent-front-documents` | inapplicable |
| 14–25 | *De anno*, tables; Tabella temporaria 2003–2046 (reprinter) | `extent-computus-tables` | inapplicable |
| 26–36 | Kalendarium | `kalendarium-*` | complete |
| 37–47 | Rubricae generales I–XX | `extent-general-rubrics` | unenumerated |
| 48–59 | Additiones et Variationes | `extent-additiones` | unenumerated |
| 60–76 | Ritus servandus | `ritus-additional-text-appointments` | complete after Ordo deduplication |
| 77–82 | De defectibus | `extent-de-defectibus` | unenumerated |
| 83–101 | Praeparatio, Gratiarum actio | `preparation-thanksgiving-*` | complete |
| 102–104 | Ordo incensandi diagrams; plate p. 104 | `extent-incensation-diagrams` | inapplicable |
| 375–381 | Ordo Missae to the Secret | `ordinary-*` | complete |
| 382–403 | Prefaces, solemn tone (14) | `prefaces`, `ordinary-*` | complete |
| 404–425 | Prefaces, ferial tone (15) | `prefaces`, `ordinary-*` | complete |
| 426–437 | Prefaces without chant (15) | `prefaces`, options, dialogue | complete |
| 438 | Canon plate | none (image only) | — |
| 439–453 | Canon through Last Gospel | `ordinary-*` | complete |
| 454 | Plate before Easter | none (image only) | — |

Two seams in the brief's section map were corrected. Page 48 is the title page
and tit. I of the Additiones, so the general rubrics end at p. 47. Page 374 is
a full-page plate in the temporal lane's extent, not a blank. Page 426 is
shared: it ends the ferial Preface of the Dead and opens the Prefaces without
chant. In the Ordinary pages, printed page equals artifact page minus 104. In
the front matter, printed `n*` equals artifact page n.

#### Method and granularity

**Kalendarium.** All 365 date lines were parsed and checked for continuity
(31/28/31/30/… per month, none lost). That gives 296 dated entries. The model
is the 1962 fixed-calendar slice, with the same clause splitting:

- Each principal clause is one celebration. Vigils printed as the day's entry
  count as celebrations.
- Each `Com.` clause is one commemoration. A clause is split at *ac*/*et* only
  between distinct identities, never inside a companion group. For example,
  *Ss. Ursulæ ac Sociarum* stays one.
- Octave, vigil, feria and Sunday commemorations are kept as identities,
  with their owner in square brackets.
- The rankless 12-05 *Commemoratio S. Sabbæ* is a commemoration.

The six movable feasts printed inside the months form a separate slice, so
that the fixed slice stays comparable with 1962. Labels normalize glyph losses
in the typesetting (*Puriicatio*, *Transiguratio*, *iliorum*) and two
misprints (*Daminani*, *Alexandrini*).

**Ordinary.** The granularity of the corrected 1962 Ordinary slices is
followed:

- Text blocks are prayer blocks and dialogue turns. The Preface dialogue and
  Sanctus come from the first Preface without chant.
- Wording options cover the Preface rubrics and the Canon's seasonal
  Communicantes and Hanc igitur.
- Musical presentations are Gloria ×4, Credo ×1, Pater ×2, Pax ×1, dismissal
  ×11, plus each solemn and ferial Preface.

As in 1962, the Prefaces without chant are the spoken presentation. They own
the Preface identities and wording options and add no musical row.

Differences from 1962 at the same granularity:

- *Benedicamus Domino* is the alternative dismissal by quality of Mass; there
  is no procession form.
- The Joseph Preface has two occasions (feast, votive).
- The Gloria has four intonations.
- There is no Chrism Preface.

**Ritus servandus.** The 13 appointments of the 1962 model recur, including
the episcopal *Pax vobis* at V.1. Three more belong to the pre-1960
communion of the faithful (X.6): the minister's Confiteor, the *Misereatur
vestri*, and *Indulgentiam … peccatorum vestrorum*, the last as a wording
alternative.

**Preparation and thanksgiving.** The Bonn witness has 23 entries and 91
slots: the 1962 set without the *Oratio universalis* attributed to Clement XI.

#### Mame 1922 comparison

The Mame Kalendarium (artifact pp. 40–49) was read on page images, month by
month. **The scan lacks the leaf printed xxx–xxxi (7 May–10 July).** For that
range the Mame Proprium Sanctorum headings and index were used. The only Bonn
identity absent there is Robert Bellarmine: the Mass sequence passes from
12 May to 14 May (p. 709, image-checked).

| Post-1922 addition (Bonn) | Bonn locus | Mame 1922 evidence | Date |
| --- | --- | --- | --- |
| S. Joannes Bosco, 01-31 | Kal. p. 27 | p. 41: 01-31 is Peter Nolasco | not established |
| S. Gabriel a Virgine Perdolente, 02-27 | Kal. p. 27 (also leap-year note) | p. 41: 02-27 empty | not established |
| S. Petrus Canisius, 04-27 | Kal. p. 29 | p. 43: 04-27 empty | not established |
| S. Robertus Bellarmino, 05-13 | Kal. p. 30 | leaf missing; Proprium p. 709 has no 05-13; index has none | not established |
| S. Joannes Maria Vianney, 08-09 | Kal. p. 32 | p. 45: 08-09 is the Vigil of St Lawrence | not established |
| S. Joannes Eudes, 08-19 | Kal. p. 32 | p. 45: 08-19 is a day within the Assumption octave | not established |
| Immaculate Heart, 08-22 | Kal. p. 32 | p. 45: 08-22 is the Assumption octave day | not established |
| S. Teresia a Jesu Infante, 10-03 | Kal. p. 34 | p. 46: 10-03 empty | not established |
| Maternity of the BVM, 10-11 | Kal. p. 34 | p. 47: 10-11 empty | not established |
| S. Albertus Magnus, 11-15 | Kal. p. 35 | p. 47: 11-15 is Gertrude | not established |
| Christ the King, last Sunday of October | Kal. p. 34 | p. 47: none; Additiones p. 70 lacks it | not established |
| Preface of the Sacred Heart (solemn, ferial, without chant) | pp. 390, 412, 430 | absent; the Holy Cross Preface rubric (p. 399) appoints that Preface for the Sacred Heart | not established |
| Preface of Christ the King (solemn, ferial, without chant) | pp. 392, 414, 431 | absent from all three series | not established |
| Ferial tone of the Epiphany Preface | p. 405 | ferial series goes Nativity → Lent (pp. 418–420) | not established |

Neither witness prints any date later than 1920. Bonn's latest printed dates
are the 1920 decree (p. 3) and an indulgence of 1917 (p. 101). Mame's license
(p. 15) cites S.R.C. decrees of 24 October 1920 and 26 October 1921.

**1922-only identities**, present in Mame but absent from the Bonn
Kalendarium:

- the Assumption octave day (08-22);
- the commemorations of S. Agapitus (08-18), of the Vigil of the Immaculate
  Conception (12-07), of S. Melchiades (12-10) and of S. Anastasia in the
  second Christmas Mass (12-25).

Four of these persist in the Bonn *body*: the Vigil rubric on p. 594,
*Pro S. Melchiade* on p. 601, Agapitus on p. 852, and Anastasia on p. 127. They are therefore
omissions from the Kalendarium print, not lost identities. Their owning lanes
should keep them.

**Identities that changed date or kind** stay in the fixed slice with a note:

- Peter Nolasco moved from 01-31 to 01-28.
- Agnes *secundo* changed from a simplex celebration to a commemoration.
- The Vigil of St Lawrence changed from the principal entry to a commemoration.
- Gertrude moved from 11-15 to 11-16.

**Rank and title differences:**

- 09-29: Bonn *duplex II classis*, Mame *duplex I classis*. This may be a
  reprint error.
- Precious Blood, 07-01: Bonn prints *I classis*. Mame's Kalendarium leaf for
  this date is missing.
- John of the Cross is styled *Eccl. Doct.* in Bonn only.

Musical structure differs in one place. Mame has twelve dismissal tones, with
separate *Benedicamus* tones for ferias *per annum* and for Advent/Lent ferias
(pp. 467–468). Bonn merges these into its tone VIII, giving eleven tones.
Mame prints the seasonal Communicantes after each Preface without chant
(p. 447), not in the Canon. That is a placement difference, not a different
identity.

The Ordinary, Ritus and preparation sections otherwise match. The
preparation has the same 23 entries; only Oblatio sui and En ego change
places.

#### Rubrical evidence for dating (Additiones and general rubrics)

The rubrics give no dates, but they show that the rubric text was conformed
after 1922:

- Additiones tit. VI n. 4 (p. 58) adds the Sacred Heart and Christ the King to
  the first-class days that exclude ordered Collects. Mame's list (p. 70) ends
  at Corpus Christi.
- The Credo list, Rubricae generales XI (p. 42), adds Peter Canisius and John
  of the Cross. It gives the Sacred Heart an octave.
- That list does not name Robert Bellarmine or Albert the Great, although the
  Kalendarium styles both as Doctors. The rubric text was therefore not
  conformed as far as the Kalendarium. This supports dating each addition
  separately rather than treating the book as a single c. 1954 state.

#### Overlap with existing rows

`roman-pre-1955-cummiskey-prefaces` (1861, 11 Prefaces,
`target-correspondence-unresolved`) is a strict subset of the new Preface
identities. It lacks only St Joseph and the Dead, both added in 1919, and the
two post-1922 Prefaces. No Bonn Preface was added a second time under a
Cummiskey ID, and the two slices must not be summed.

Recommendation: keep the Cummiskey slice as other-witness evidence. Its basis
should cross-reference `roman-pre-1955-prefaces`. Retiring the whole-book
`roman-pre-1955-whole-preface` boundary should wait for an independent review
of these 15 identities. The whole-book slice basis, which says no 1920 witness
is held, needs updating by the coordinator.

The Holy Week rows belong to the temporal extent and do not overlap this
lane's extent.

#### Image checks

Bonn pages checked on images:

- Front matter and Kalendarium: 24, 27, 32, 34, 36.
- Rubrics, Additiones, preparation and diagrams: 48, 83, 104.
- Plates: 374, 438, 454.
- Ordinary, Prefaces and Canon: 377, 379, 392, 405, 446, 450, 451.

Mame pages checked on images:

- Kalendarium: 40–49.
- Ordinary and Canon: 386, 387, 455, 458, 465, 467, 468.
- Prefaces: 399, 416, 418–420, 440, 442, 447, 450, 453.
- Proprium Sanctorum: 709.

#### Limits

- These are structural identities, not wording collations.
- For the Mame leaf gap, presence of an identity in that range rests on Mame
  body headings found by OCR, not on Kalendarium images.
- Mame identity of the Ordinary blocks was established by OCR phrase search,
  plus images where the OCR failed.
- Dismissal-tone melodies were not compared note by note.
- The general rubrics, Additiones and *De defectibus* remain unenumerated.
- Kalendarium rows assert no formulary or calendar join.

### The pre-1955 witness: Proprium de Tempore and the pre-1955 Holy Week

The maintainer accepted the registered
[Bonn reimpressio](../works/catholic-church/missale-romanum/editions/2004-bonn-palmarum-reimpressio-editio-28-iuxta-typicam-1920/artifacts/ia-reimpressio-pdf-b676ce5c/artifact.toml)
on 19 October 2026 as the witness of the `roman-1920` recension. Its SHA-256 is
`b676ce5c…a1d` and it has 1,220 artifact pages. It is a 2003 typesetting of the
28th edition iuxta typicam and a conformed printing of about 1954. The
temporal lane read artifact pp. 105–374 and 455–582. The text layer is typeset,
not OCR, but it has scattered keying errors such as *Praetatio* and
*Postcornmuniones*. Every page of the extent belongs to a positive slice or is a
full-page plate or blank. The registered
[1922 Mame scan](../works/catholic-church/missale-romanum/editions/1922-tours-mame-editio-quarta-iuxta-typicam/artifacts/ia-scan-pdf-9873693a/artifact.toml)
is the control. The payloads stay outside the repository, and this record holds
metadata only.

The lane adds 4 slices, 2,613 targets and 4 boundaries. It used no held
propers, Mass keys or 1962 rows, and it adds no calendar joins.

| Section | Artifact pp. | Printed pp. | Slice | Status |
| --- | --- | --- | --- | --- |
| Plate facing the Temporal | 104 | – | extent boundary (lane-ordinary) | inapplicable |
| Advent to Saturday after Passion Sunday | 105–273 | 1–169 | `temporal-advent-to-passiontide` | complete |
| Holy Week, Palm Sunday to the Holy Saturday Vespers | 275–373 | 171–269 | `temporal-holy-week` | complete |
| Plate before the Ordo | 374 | 270 | none (no text) | inapplicable |
| Easter Sunday to the last Sunday after Pentecost | 455–581 | 351–477 | `temporal-easter-to-last-sunday` | complete |
| Sacred Heart formulary and octave appointments | 527–531 | 423–427 | `temporal-post-1922-additions` | complete |
| Plate before the Proprium de Sanctis | 582 | 478 | none (no text) | inapplicable |

Printed page numbers equal the artifact page minus 104 throughout this extent,
because the plates are paginated. Twenty-four pages have no text layer:

- 19 are full-page plates: pp. 104, 124, 146, 154, 158, 192, 258, 274, 306,
  314, 334, 374, 454, 482, 496, 512, 518, 526 and 582.
- 5 are blank: pp. 123, 153, 333, 495 and 525.

The seams are exact. Page 104 is a plate, and p. 105 opens *PROPRIUM DE
TEMPORE* with Advent I. Page 373 ends the Holy Saturday Vespers and dismissal,
p. 374 is a plate, and p. 375 opens the *ORDO MISSÆ*. Page 454 is a plate, and
p. 455 opens *DOMINICA RESURRECTIONIS*. Page 581 ends the last Sunday after
Pentecost, p. 582 is a plate, and p. 583 opens the *PROPRIUM DE SANCTIS*.

| Slice | State | Targets by kind |
| --- | --- | --- |
| `temporal-advent-to-passiontide` | complete | slot 966, referral 167, form 77, ord-opt 60, prayer-set 14, rite 1 |
| `temporal-holy-week` | complete | slot 210, rite-unit 26, referral 20, ord-opt 13, celebration 7, form 6, rite 4 |
| `temporal-easter-to-last-sunday` | complete | slot 742, referral 141, ord-opt 68, form 57, prayer-set 11 |
| `temporal-post-1922-additions` | complete | slot 19, referral 2, form 1, ord-opt 1 |

The lane first typed 152 Credo, Gloria, *Flectamus genua* and dismissal
directions as text slots. At integration the 142 Ordinary directions were
retyped `ordinary-option`, following the 1962 temporal convention. The eight
*Flectamus genua* units of the Good Friday solemn orations remain text slots of
the rite. Before that retyping, the 2,079 text slots divided as follows. They
must not be summed with other kinds:

| Text-slot role | Count |
| --- | --- |
| Printed proper units | 1,608 |
| Preface, Communicantes and Hanc igitur appointments | 190 |
| Credo, Gloria, Flectamus genua and dismissal directions | 152 |
| Seasonal prayer-set slots | 75 |
| Printed commemorations | 54 |

#### Method and granularity

The book prints no marginal unit numbers. The text layer was therefore parsed
with its typography, taking font, size, colour and position from
`pdftohtml -xml`. Each printed formulary heading is one `form`; these headings
are the bold black or large red titles. Within a formulary:

- Each red role heading is one compound unit. This covers the Introit with its
  psalm, each Oratio, the Gradual, the Tract, the Sequence, the Offertory, the
  Secret, the Communion, the Postcommunion and the *Oratio super populum*.
- Each reading title is a unit, as are the paragraph-initial *Alleluja* with its
  verse, the *Hymnus* of the Ember Saturdays and each Pentecost-vigil
  *Prophetia*.
- Repeated role headings take ordinals, as in the Ember-day collects and
  lessons.
- Seasonal and votive alternatives printed inside a formulary stay distinct
  slots under the same form. Examples are the post-Septuagesima votive Tract,
  the paschal Alleluja and the votive Offertory and Communion of the Sacred
  Heart.

The first pass missed role headings that were printed at 12 or 14 point, in
italic or with a truncated title, for example on pp. 120, 128, 209 and 521. The
role rule was widened to catch them, and the result was confirmed on page
images.

Pre-1955 printing has features that 1962 lacks, and they are recorded as
follows:

- **Seasonal orations.** The *Orationes pro diversitate Temporum* (de S. Maria,
  contra persecutores, pro Papa, ad poscenda suffragia, pro vivis et defunctis)
  are printed in full at eleven places. Each printed collect, secret and
  postcommunion triple is one `prayer-set` with three slots, which gives 25
  sets. Every other formulary refers to these sets in its collect, secret and
  postcommunion positions. Each printed referral (*Aliae Orationes / Secretae /
  Postcommuniones, ut supra*, *Altera Oratio*, or *Orationes … assignatae, ut*)
  is one `form-referral` per position.
- **Commemorations.** Printed commemorations are slots of their form. Examples
  are the octaves of the Nativity, Epiphany, Ascension, Corpus Christi and
  Sacred Heart, and Saints Anastasia and Telesphorus.
- **Referral headings.** The headings of 2–4 January (octave days) and of the
  Telesphorus commemoration are referral-only `form`s, each with a referral
  child. This follows the sanctoral precedent in the 1962 review. The Hyginus
  heading has three proper orations.
- **Directions and appointments.** Credo, Gloria and Flectamus genua directions,
  both positive and explicit negative, and printed dismissal directions are
  positive text-slots. So are the Preface, Communicantes and Hanc igitur
  appointments, including conditional alternatives. The Credo directions were
  read from the running text, not from the red drop capital, because many of
  them are printed without one.

Rites are recorded in this way:

- **Ashes.** The blessing of ashes is an `exceptional-rite` with 10 slots. No
  pre-1955 ash rite existed before this lane.
- **Holy Week.** Holy Week is counted in named semantic blocks at the
  granularity of the 1962 Holy Week lane:
  - 7 day celebrations.
  - Mass forms for Palm Sunday, Monday, Tuesday, Wednesday, Maundy Thursday
    and Holy Saturday.
  - The palms rite, with blessing, distribution and procession, 27 slots in
    all, including the Preface and Sanctus of the blessing.
  - The Thursday reposition, stripping of the altars and Mandatum, with nine
    antiphons.
  - Good Friday:
    - the lessons and Passion;
    - the nine solemn orations, including *pro Imperatore*, each a unit with
      an invitation, a Flectamus direction or, for the Jews, the printed
      rubric, and an oration;
    - the adoration of the Cross, with the Improperia, Crucem tuam, Crux
      fidelis, Pange lingua and doxology;
    - the Mass of the Presanctified, with Vexilla Regis, three incensation
      formulas, In spiritu humilitatis, Orate fratres, Pater noster, Libera nos
      and the communion formulas.
  - Holy Saturday:
    - the three new-fire orations, the blessing of the incense grains and
      Lumen Christi;
    - the deacon's blessing and the Exsultet as one block;
    - the twelve prophecies with twelve orations and three tracts;
    - the blessing of the font: the Sicut cervus procession, two orations, the
      Preface-tone consecratory prayer as one block, and the three oil and
      chrism formulas;
    - the litany;
    - the Mass with its Vespers.

  Named texts that are not printed are `form-referral`s: Pange lingua on
  Thursday, Psalm 21, Asperges and the Rituale baptism. No Chrism Mass is
  printed.

#### Cross-checks

- **Heading counts.** A line-start count of role headings in `pdftotext -raw`
  matched the slots for Introit, Offertory, Communion, Secret and Postcommunion
  page by page. The only differences were explained by rubric lines that begin
  with a role word and by tracts that sit inside rite and vigil blocks.
- **Formulary sequence.** Every Bonn temporal formulary was matched to Mame's
  running heads (Mame artifact pp. 115–593). The two temporal sequences are
  identical except for the cases below.
- **Holy Family and Hyginus.** Mame prints Holy Family in its Proprium de Sanctis
  (artifact pp. 614–616, printed 500–502) and Pro S. Hygino at artifact p. 617.
  Bonn prints both in the Temporal. These are relocations, not additions.

#### Post-1922 additions

These rows are printed in Bonn with no counterpart in Mame 1922. The absences
were confirmed on Mame page images at artifact pp. 540 and 720.

| Rows | Bonn locus | Mame 1922 | Date |
| --- | --- | --- | --- |
| Form *In Festo Sacratissimi Cordis Jesu* (Cogitationes; *cum Octava privilegiata III ordinis*), 15 slots, credo direction, Preface appointment, within-octave referral | pp. 527–529 | different formulary *Miserebitur*, Proprium de Sanctis p. 720 (printed 606), no octave | not established |
| Sacred Heart octave commemoration collect, secret and postcommunion, Sacred Heart Preface appointment, octave-day referral, in the *Dominica infra Octavam Sacratissimi Cordis* | pp. 529–531 | the same Mass headed *Dominica III post Pentecosten*, with no octave (p. 541) | not established |

The Sunday's own formulary has a 1922 counterpart and stays in the main slice.
Only its octave appointments move.

Mame's *Miserebitur* Sacred Heart formulary is the one 1922-only identity
connected with this extent. It is printed nowhere in Bonn: a text search of the
whole book found it absent. It belongs to Mame's sanctoral, so it is reported
here and was not entered as a row. Christ the King is printed in Bonn's
sanctoral (p. 927), outside this extent.

#### Holy Week: the earlier slices

The tracked slices `roman-pre-1955-holy-week-witness-celebrations` (4) and
`roman-pre-1955-holy-week-witness-units` (38) come from the 1862 Pustet and
from the 1951–1954 composite, and they are marked
`target-correspondence-unresolved`. Each of their 42 rows maps one-to-one to a
new established row:

- the four celebrations map to `roman-pre-1955:temporal:celebration:` plus
  `dominica-in-palmis`, `feria-5-in-cena-domini`, `feria-6-in-parasceve` and
  `sabbato-sancto`;
- the 14 palm-blessing units map to `…:slot:palm-blessing:palms-blessing:*`,
  and the three distribution units to `…:palms-distribution:*`;
- the Palm Sunday and Maundy Thursday Introits map to those Masses'
  `…:introit` slots;
- the three *pro Iudaeis* units map to
  `…:slot:parasceve:solemn-oration-8:{invitation,rubric-no-flectamus,oration}`;
- Prophecies 1–12 map to `…:slot:sabbato-sancto:prophecies:prophecy-NN`;
- the Holy Saturday *nec postcommunio* rubric and three Vespers units map to the
  corresponding `…:slot:sabbato-sancto-missa:` rows.

Keeping both sets would double-count those identities in the `roman-pre-1955`
report. The two old slices are therefore superseded and removed from the
inventory.
[roman-holy-week-acts-v1.toml](roman-holy-week-acts-v1.toml) stays as the
other-witness tracer and is not changed.

#### Image checks

Artifact pages checked as images:

| Witness | Artifact pages |
| --- | --- |
| Bonn | 104, 105, 120, 123, 124, 128, 146, 150, 152, 153, 154, 158, 162, 163, 192, 209, 223, 258, 274, 275, 280, 281, 306, 310, 311, 314, 325, 333, 334, 336, 359, 371, 374, 375, 454, 455, 456, 482, 493, 495, 496, 512, 518, 521, 525, 526, 527, 529, 582, 583 |
| Mame | 157, 165, 540, 720 |

The checks found two corrections, both made before the counts above:

- The Exsultet begins on p. 336, not p. 337.
- The Innocents Alleluja and Tract are conditional alternatives, not the
  votive post-Septuagesima pattern.

#### Limits

These are structural identities, not wording collations. Incipits in labels
identify units; they are not verified text.

Three things are not enumerated, and each is an explicit `unenumerated`
boundary:

- imported bodies of referred Masses;
- conditional omissions when a Sunday Mass is resumed on a feria;
- occurrence and commemoration rules, verse- and stanza-level segmentation and
  the unchanging Ordinary.

No dates were asserted for the post-1922 additions. The whole-book `roman-1920`
universe remains `unresolved`.

Three choices are open for review:

- **Kind of the directions.** Credo, Gloria and Flectamus directions are
  `text-slot`, as the brief specified. The 1962 Lent lane typed them as
  `ordinary-option`. Their IDs contain `:direction-`, so they can be retyped
  mechanically.
- **The Sacred Heart form.** It is held in the post-1922 slice. Its celebration
  existed in 1922, but the 1922 formulary text differs.
- **Unpaired qualifiers.** Some Ember and Lent orations without a printed
  qualifier were given ordinals by position.

### Pre-1955 Proprium de Sanctis (Bonn artifact pp. 583–966)

**Witness.** The registered
[Bonn 2004 reimpressio](../works/catholic-church/missale-romanum/editions/2004-bonn-palmarum-reimpressio-editio-28-iuxta-typicam-1920/artifacts/ia-reimpressio-pdf-b676ce5c/artifact.toml)
of the 28th edition iuxta typicam is a conformed printing of about 1954. Its SHA-256 is
`b676ce5c…a1d`, and it has 1,220 pages. The control witness is the registered
[1922 Mame editio quarta iuxta typicam](../works/catholic-church/missale-romanum/editions/1922-tours-mame-editio-quarta-iuxta-typicam/artifacts/ia-scan-pdf-9873693a/artifact.toml).
In this extent the printed page number is the artifact page minus 104 throughout,
and the running heads were checked against it. The Proprium opens at artifact
p. 583 and ends at p. 965. Pp. 598, 634, 668, 674, 768, 778, 830, 846, 874, 934
and 966 are full-page plates without text, so no targets fall on them.

**Method.** The lane worked on the `pdftotext -raw` layer, which is a clean
typeset text and not OCR. It then fixed the reading order. The raw stream follows
content order, so on pages where a heading spans both columns, that heading and
the lower band come out before the upper band (pp. 599, 635, 700, 831, 847, 896
and 938). The lane therefore rebuilt each page's reading order from word
coordinates, band by band and column by column. Every locus keeps its raw
page-local line number.

Date headings were swept with these patterns: *Die N*, *Eadem die*,
*Item eadem die*, *Die N vel N*, *Feria …* and *Dominica ultima Octobris*. Nested
*Missa votiva* headings and *Ad primam/secundam/tertiam Missam* were swept too.
Title lines, rank lines and Introit markers were then checked against those
headings. Role headings were classified from the line-start markers. A pattern
search also caught the text layer's typographic variants (*Postcummunio*,
*Postcommumo*, *Postcommimio*, *Offertórium*, *Seqientia*, *Prætatio*). Every
form's role sequence was then checked: full Masses for the
I–C–L–E–O–S–M–P core, and orations-only Masses for C–S–P.

Commemoration orations are identified in three ways:

- by a *Pro N.* heading, including one split across two lines;
- by an introducing *fit Commemoratio N.:* rubric, excluding the feria;
- by position, after the main oration of the same type.

Overrides, each checked by locus:

- the within-octave third orations *de Spiritu Sancto* (p. 601);
- the Vigil of Ss. Peter and Paul commemoration under St Irenaeus (pp. 763, 765);
- St Hadrian (p. 875);
- three role headings that do not begin a line (pp. 811, 946, 947).

**Granularity.** The granularity follows the corrected 1962 slices:

- The three All Souls Masses are separate forms.
- The 2 February Mass under *Ad Missam* belongs to the Purification form, and the candle rite is its own exceptional rite.
- Referral-only *Pro N.* and *Missa … de Communi* headings are forms.
- The second printed Masses of 1 May and 12 May are seasonal or votive sub-variants inside one form. Their role headings are counted as slots.
- Five rubric-only date headings are not forms: 28 Nov., 1 Dec., 14 Dec., 19 Dec. and 27 Jun.
- The 1 September *Pro Ss. duodecim Fratribus* appointment is printed as an italic rubric sentence, not a display heading. It is kept as a form because it carries its own orations (p. 870).

| Slice | State | Targets by kind |
| --- | --- | --- |
| `roman-pre-1955-sanctoral-body-forms` | complete | form 327 |
| `roman-pre-1955-sanctoral-printed-slots` | complete | slot 2130 |
| `roman-pre-1955-sanctoral-form-referrals` | partial | referral 224 |
| `roman-pre-1955-sanctoral-preface-appointments` | complete | slot 57 |
| `roman-pre-1955-purification-rite` | complete | rite 1, rite-unit 3, slot 15 |
| `roman-pre-1955-sanctoral-post-1922-additions` | complete | form 13, slot 126 (121 role, 5 Preface) |
| `roman-pre-1955-sanctoral-referrals-post-1922-additions` | partial | referral 4 |

The 2,130 role slots break down as follows:

| Role | Slots |
| --- | --- |
| collect | 266 |
| secret | 263 |
| postcommunion | 263 |
| alleluia | 194 |
| introit | 168 |
| epistle-or-lesson | 167 |
| offertory | 167 |
| communion | 166 |
| gospel | 163 |
| gradual | 154 |
| tract | 48 |
| commemoration collect | 33 |
| commemoration secret | 33 |
| commemoration postcommunion | 33 |
| sequence | 4 |
| third-oration collect | 2 |
| third-oration secret | 2 |
| third-oration postcommunion | 2 |
| alternative collect | 1 |
| commemoration Gospel | 1 |

The 228 referrals break down as follows:

| Referral type | Count |
| --- | --- |
| formulary | 191 |
| votive-use rubric | 20 |
| infra-octave | 5 |
| role-level | 11 |
| Greater Litanies Rogation Mass | 1 |

The 340 forms are the Mass-formulary denominator of this extent.

**Seams.** P. 582 is a plate without text, at the end of the temporal lane's
extent. P. 583 opens *Proprium de Sanctis* with its general rubric and then gives
28 Nov. (a rubric) and the Vigil of St Andrew. P. 965 ends with *Pro S. Petro
Alexandrino*, and p. 966 is the Commune frontispiece plate, without text.
P. 967 opens *Commune Sanctorum*. All four seam pages and the plate were checked
on images. Every target locus falls within pp. 583–965. The sanctoral has no
headings for 22 Dec.–13 Jan. These days are in the Bonn temporal, including
Hyginus at p. 163 and Holy Family at pp. 159–160. The Sacred Heart is also in the
temporal, at pp. 527–531.

**Kalendarium cross-check (pp. 26–36, read only).** Every Kalendarium celebration
dated in this extent has a printed formulary heading. The two movable ones (Seven
Sorrows in Lent, the Solemnity of St Joseph) and Christ the King are printed too.
Each listed commemoration is either a *Pro N.* form or a set of printed
commemoration orations. The exception is the Cathedra Antiochiae commemoration of
St Paul, which is referred to 18 Jan. Octave days are covered by the infra-octave
referrals (*Missa ut in Festo*): Immaculate Conception, St Joseph, St John
Baptist, Assumption and All Saints. The body prints four identities that the
Kalendarium omits:

- the Vigil of the Immaculate Conception on 7 Dec. (p. 596);
- St Pudentiana on 19 May (pp. 723–725);
- St Agapitus on 18 Aug. (p. 852);
- St John Leonardi on 9 Oct. (p. 908). The Kalendarium still gives Ss. Dionysius and companions as the day's semidouble, while the body makes John Leonardi the duplex and prints Dionysius as a *Pro* Mass.

There are also minor spelling variants: Christiana/Christina, Nicodemis/Nicomede,
Theresiae/Teresiae.

**Mame 1922 comparison.** Mame's Proprium de Sanctis occupies artifact
pp. 594–878. Its noisy OCR headings and running heads were aligned by date with
the Bonn forms. Each unmatched name was searched in the Mame text, and every
absence and doubtful match was checked on a Mame page image.

Thirteen Bonn formularies have no counterpart in Mame's Proprium:

- John Bosco, 31 Jan.
- Gabriel a Virgine Perdolente, 27 Feb.
- Peter Canisius, 27 Apr.
- Robert Bellarmine, 13 May
- John Vianney, 9 Aug.
- John Eudes, 19 Aug.
- Immaculate Heart, 22 Aug.
- Teresa of the Child Jesus, 3 Oct.
- John Leonardi, 9 Oct.
- Maternity of the BVM, 11 Oct.
- Margaret Mary Alacoque, 17 Oct.
- Christ the King, last Sunday of October
- Albert the Great, 15 Nov.

Four of these have a counterpart among Mame's *Missae propriae pro aliquibus
locis*:

- Gabriel, p. 1096, same Introit.
- B. Joannis Leonardi, p. 1086, same Introit.
- Margaret Mary, p. 1103, same Introit.
- Maternity, p. 1049, a different Mass (Introit *Salve sancta parens*, not *Ecce Virgo*).

Mame's local *Purissimi Cordis* Mass (p. 1048) is not the 1944 Immaculate Heart
formulary. Neither witness, nor any registered source, establishes institution or
decree dates. Three identities are present in Mame on another day: Peter Nolasco
(Mame 31 Jan.), Hedwig (Mame 17 Oct.) and Gertrude (Mame 15 Nov.).

Two Mame sanctoral formularies have no Bonn counterpart:

- *Eadem die 25 Julii Pro S. Christophoro* (Mame p. 783). Bonn keeps Christopher only as a private-Mass commemoration within St James (p. 813).
- *Die 22 Augusti In Octava Assumptionis* (Mame p. 811). Bonn suppresses it: *De die Octava … nihil fit*.

Mame's sanctoral also holds Holy Family, Hyginus and the Sacred Heart, which Bonn
places in the temporal. Several papal formularies now refer to a *Commune
Summorum Pontificum* that Mame does not have; for example, Mame refers Cletus and
Marcellinus to *Sancti tui* and prints Callistus in full. These are post-1922
changes to the referral targets of pre-1922 identities. They remain in the main
referral slice, and their loci show the target.

**Image checks.**

- Bonn artifact pp. 582, 583, 605, 607, 634, 635, 652, 681, 692, 700, 703, 719, 765, 770, 813, 856, 870, 893, 907, 925, 937, 938, 941, 965, 966 and 967.
- Mame artifact pp. 633, 634, 654, 655, 689, 690, 709, 783, 799, 810, 811, 833, 834, 842, 843, 848, 850, 851, 857, 860, 872, 1049, 1086, 1096 and 1103.

**Limits.** These are structural identities, not wording collations, and Preface
markers name an appointment, not a Preface identity. The *Præfatio propria* of
Christ the King (p. 927) implies a post-1922 Preface for the Ordinary lane to
reconcile. The candle-rite identity needs reconciling with any pre-1955
exceptional-rite inventory.

Referrals embedded mid-rubric, conventual-Mass directions, occasional-oration
referrals and last-Gospel directions are not exhausted; the referral slices are
therefore partial. Absence in Mame is certified for the Proprium de Sanctis as
image-checked at each date. It is not certified for the whole Mame volume beyond
the OCR searches stated. No calendar joins were added, so every target classifies
as `unresolved` in `expectations()`.

### The pre-1955 witness: Commons, votives, the dead, rites and propers for certain places

The registered
[Bonn reimpressio](../works/catholic-church/missale-romanum/editions/2004-bonn-palmarum-reimpressio-editio-28-iuxta-typicam-1920/artifacts/ia-reimpressio-pdf-b676ce5c/artifact.toml)
is accepted, by the maintainer's decision of 19 October 2026, as the witness of
the pre-1955 recension. Its SHA-256 matches the registered value, `b676ce5c…a1d`,
and it has 1,220 artifact pages. This section covers artifact pp. 967–1220: the
Commons, the votive Masses, the Orationes diversae, the Masses and prayers for
the dead, the absolution, the holy-water rite, the blessings, the Pontifical
excerpts, and the Masses and Commons for certain places. The text layer is a
2003 digital typesetting, not OCR. Identities were taken from that layer and
from page images. Held propers, Mass keys and selectors were not consulted. The
payload stays outside the repository, and this record holds metadata only.

The book is a conformed printing of about 1954, so it carries additions made
after 1920. Each identity was therefore compared with the registered
[1922 Mame editio quarta](../works/catholic-church/missale-romanum/editions/1922-tours-mame-editio-quarta-iuxta-typicam/artifacts/ia-scan-pdf-9873693a/artifact.toml).
An identity printed in Bonn with no Mame counterpart is placed in a separate
`…-post-1922-additions` slice. The public-domain decision does not reach text
first published in 1931 or later, so those slices must remain separable.

The inventory adds 23 slices, 2,023 targets and 6 boundaries for
`roman-pre-1955`:

| Section | Artifact pp. | Printed pp. | Slices | Status |
| --- | --- | --- | --- | --- |
| Commune Sanctorum | 967–1015 | [1]–[49] | `body-commons-*` | forms complete; slots partial |
| Missae de sancta Maria in Sabbato | 1015–1022 | [49]–[56] | `body-marian-saturday-*` | forms complete; slots partial |
| Commune Summorum Pontificum | 1022–1024 | [56]–[58] | `body-commons-*-post-1922-additions` | post-1922 |
| Missae votivae, votivae ad diversa | 1025–1076 | [59]–[110] | `body-votives-*`, `body-votives-*-post-1922-additions` | forms complete; slots partial |
| Orationes diversae | 1076–1089 | [110]–[123] | `body-diverse-prayers-*` | forms complete; slots partial |
| Missae Defunctorum, Orationes pro Defunctis | 1090–1106 | [124]–[140] | `body-dead-*` | forms complete; slots partial |
| Absolutio super tumulum | 1106–1110 | [140]–[144] | `body-absolution-*` | complete; units partial |
| Ordo ad faciendam aquam benedictam | 1111–1113 | [145]–[147] | `holy-water-rite` | complete |
| Benedictiones diversae; episcopal blessings | 1113–1117 | [147]–[151] | `blessings`, `blessings-post-1922-additions` | complete |
| Confirmation, paten and chalice; Pontifical orations | 1118–1124 | [152]–[158] | `pontificale-excerpts-post-1922-additions` | post-1922 |
| Missae pro aliquibus locis | 1125–1209 | [159]–[243] | `local-proper-forms`, `local-proper-forms-post-1922-additions` | complete |
| Commune Sanctorum pro aliquibus locis | 1209–1220 | [243]–[254] | `local-additional-commons` | complete |

Slices are named here without the `roman-pre-1955-` prefix. Kinds are counted
separately and must never be summed into a text total:

| Slice | State | Targets by kind |
| --- | --- | --- |
| `body-commons-forms` | complete | form 24, prayer-set 14, common 8 |
| `body-commons-slots` | partial | slot 309, referral 34 |
| `body-marian-saturday-forms` | complete | form 5 |
| `body-marian-saturday-slots` | partial | slot 51, referral 6 |
| `body-commons-forms-post-1922-additions` | complete | form 1, prayer-set 2 |
| `body-commons-slots-post-1922-additions` | partial | slot 15, referral 1 |
| `body-votives-forms` | complete | form 26, prayer-set 9 |
| `body-votives-slots` | partial | slot 323, referral 24 |
| `body-votives-forms-post-1922-additions` | complete | form 1 |
| `body-votives-slots-post-1922-additions` | partial | slot 12, referral 1 |
| `body-diverse-prayers-forms` | complete | prayer-set 36 |
| `body-diverse-prayers-slots` | partial | slot 108 |
| `body-dead-forms` | complete | prayer-set 27, form 3, referral 1 |
| `body-dead-slots` | partial | slot 109, referral 7 |
| `body-absolution-forms` | complete | rite 1 |
| `body-absolution-slots` | partial | rite-unit 13, referral 3 |
| `holy-water-rite` | complete | rite 1, rite-unit 11, referral 3 |
| `blessings` | complete | rite 2, rite-unit 2, slot 2 |
| `blessings-post-1922-additions` | complete | rite 8, rite-unit 8, slot 13 |
| `pontificale-excerpts-post-1922-additions` | complete | slot 18, rite-unit 17, referral 7, prayer-set 5, rite 2 |
| `local-proper-forms` | complete | slot 539, form 55, referral 20, comm. 1 |
| `local-proper-forms-post-1922-additions` | complete | slot 25, form 2 |
| `local-additional-commons` | complete | slot 83, prayer-set 12, referral 7, form 6 |

By kind: text-slot 1,607, form 121, form-referral 114, prayer-set 107,
exceptional-rite-unit 51, exceptional-rite 14, common 8 and commemoration 1.
The post-1922 slices hold 138 of these rows.

#### Method and granularity

The method and granularity follow the corrected 1962 body rows. The two-column
pages were put into reading order from the PDF's word boxes. Lines that the
extractor had merged across the gutter were split, and every line was mapped
back to its line in the `pdftotext -raw` page. A hand-built segmentation then
opens each formulary at its printed heading. Each marker must resolve to
exactly one line, and markers must run in page order. Role headings within a
segment become text slots. They are the Introit, Collect, Lesson, Gradual,
Alleluia, Tract, Sequence, Gospel, Offertory, Secret, Communion and
Postcommunion, numbered by option within the form. Readings and Masses printed
only by incipit with a cross-reference become `form-referral`, as do Preface
referrals.

- **Forms.** One `form` per printed Mass heading. Referral-only local headings,
  such as *Missa Salve, de Communi* with own prayers, are forms with a
  `:referral` child. Paschal variants printed inline under "Tempore autem
  Paschali dicitur sequens" stay options within the form. These are the Introit,
  Offertory and Communion of the Peter and Paul and Apostles votives. Bonn
  prints no paschal sub-heading, so the 1962 `form-referral` device does not
  arise.
- **Prayer sets.** Oration-only categories are `prayer-set`. These are the
  Orationes diversae, the diverse prayers for the dead and their printed plural
  sets, and numbered alternatives within a form. Other prayer sets are the
  consecration, ordination and thanksgiving prayers, which the Mass of the day
  takes, and the Pontifical orations.
- **Additional readings.** The pools of further Epistles and Gospels after a
  Common are `common`: 8 in all, against 4 in 1962. Bonn prints such pools
  after the paschal Martyrs, Doctors, Virgins and non-Virgins Commons as well.
- **Rites.** The absolution, holy-water rite, blessings, Confirmation, and
  paten and chalice consecration are `exceptional-rite`, counted in named
  semantic units as in 1962. Chant notation, responsory repeats and actions are
  not multiplied.
- **Corrections to the automatic pass.** Bonn prints the Saturday collect
  *Concede nos* twice in Saturday forms III and IV (pp. 1018, 1020). Mame 55*
  prints it once, so the repeat is a typesetting duplication and was dropped.
  The two prayers after the Pater noster and the final blessing in the
  marriage Mass are typed as nuptial units, as in 1962. The Consecrator and
  Consecratus Secret and Hanc igitur of the bishop's consecration were added
  as options.

#### Seams and printed numbers

The printed page number in brackets reconciles contiguously: artifact page = 966 + printed number,
[1]–[254], with no gap and no mismatch on all 254 pages. Four section-opening
pages under a plate carry no printed number: pp. 967 [1], 1025 [59], 1090 [124]
and 1125 [159]. The briefed ranges "[60]–[109]" and "[160]–[243]" begin one
page late for that reason, and the book ends at [254], not [252]. Bonn has no
marginal unit numbers, so there is no analogue of the 1962 4175–5190 audit.

| Seam | Evidence |
| --- | --- |
| 965 / 966 / 967 | p. 965 ends the Proper of Saints (26 November); p. 966 is a full-page plate with an empty text layer; p. 967 opens *Commune Sanctorum*. No target on p. 966. |
| 1015 | Marian Common ends; Saturday Masses begin on the same page |
| 1022 | Saturday V ends; Popes Common begins on the same page |
| 1024 / 1025 | Popes Common ends; *Missae votivae* opener |
| 1044 | heading *II Missae votivae ad diversa* inside the papal-election page |
| 1076 | thanksgiving Postcommunion, then *Orationes diversae* |
| 1089 / 1090 | prayer 35 ends; *Missae Defunctorum* opener |
| 1106 | prayer for the dead 17 ends; *Absolutio super tumulum* |
| 1110 / 1111 | absolution ends; holy-water *Ordo* |
| 1113, 1115 | holy water, then *Benedictiones diversae*; candles, then the episcopal blessings |
| 1117 / 1118, 1122 | tabernacle blessing, then *Forma Confirmationis*; *Appendix* of Pontifical orations |
| 1124 / 1125 | reconciliation prayers end; *Missae pro aliquibus locis* opener |
| 1208/1209 | Miraculous Medal ends on p. 1208; *Commune Sanctorum pro aliquibus locis* opens on p. 1209 |
| 1220 | last page of the artifact, ending with an ornament; no index follows |

#### Comparison with Mame 1922

The Mame Commons, votive and dead sections (pp. 879–1030, printed 1*–152*), the
local supplement (pp. 1031–1126, [1]–[96]) and its index (pp. 1136–1138) were
compared by heading and by index. Every absence was then confirmed on Mame page
images.

| Post-1922 identity | Bonn locus | Mame evidence | Date evidence |
| --- | --- | --- | --- |
| Commune unius aut plurium Summorum Pontificum | pp. 1022–1024 [56]–[58] | 59*–60* (pp. 937–938) pass from Saturday V straight to *Missae votivae*; index j omits it | not established |
| Missa de D. N. Jesu Christo summo et aeterno Sacerdote | pp. 1038–1040 [72]–[74] | 71*–74* (pp. 949–952): Eucharist votive, then *Feria VI* Cross; index omits it | not established |
| Blessings of eggs, bread, new fruits and any food | pp. 1113–1114 [147]–[148] | 152* (p. 1030) prints only the Easter lamb and candles; index j lists no others | not established |
| Episcopal blessings: vestments, altar linens, corporals, tabernacle | pp. 1115–1117 [149]–[151] | absent at 152*; no OCR hit anywhere in Mame | not established |
| Confirmation; paten and chalice consecration | pp. 1118–1121 [152]–[155] | absent at 152*; local Masses follow at once | not established |
| Pontifical orations: abbot, abbess, virgins, cemetery, reconciliation | pp. 1122–1124 [156]–[158] | absent; no OCR hit for *Abbatissae* | not established |
| Eucharistici Cordis Jesu (local) | pp. 1165–1167 [199]–[201] | absent from the *In honorem D. N. J. C.* section and from index i | not established |
| S. Pii X (local) | pp. 1189–1191 [223]–[225] | absent from index k–l | 1954, as stated by the registered Bonn artifact record |

Four identities in this extent are printed in Mame 1922 but not in Bonn's
pp. 967–1220. They are reported here, not added as rows:

- *Missa propria Sacratissimi Cordis Jesu* (*Egredimini*), Mame [3]–[4].
  Bonn has the feast in its temporal section, pp. 528–530, and uses the
  Introit *Egredimini* in the Crown of Thorns Mass (p. 1136).
- *Maternitatis B. M. V.* (11 October), Mame [19]–[20]. Bonn has it in its
  universal calendar (p. 34).
- *S. Gabrielis a Virgine Perdolente*, Mame [66]–[67]. Bonn has it in the
  Proper of Saints (p. 655).
- *S. Margaritae Mariae Alacoque*, Mame [73]–[74]. Bonn has it in the Proper of
  Saints (p. 916).
- *Commemoratio omnium Ss. Summorum Pontificum* is the same identity in both
  books, but the date differs: Mame's index gives 3 July and Bonn 4 July.

Everything else matches at identity level:

- Commons: Mame has the same thirteen sections, including *In Vigiliis
  Apostolorum*, *Doctorum* and *Abbatum*.
- Saturday Masses and votives: the five Saturday Masses, and every votive
  heading in Mame's index except the High Priest. Those are the 24 Bonn votive
  forms and the consecration, ordination, Holy Spirit and thanksgiving prayer
  sets.
Everything else in the extent matches at identity level:

- prayers: Orationes diversae 1–35 and Orationes pro Defunctis 1–17;
- rites: the absolution, the holy-water *Ordo*, and the Easter-lamb and candle
  blessings;
- local propers: 55 of Mame's 59 local Masses (its index lists 10 + 21 + 28,
  less the four above), and all six local Commons. Mame prints the same *juxta
  decretum S. R. C. diei 22 Maji 1914* heading.

Mame prints the Mediatrix Mass as an appendix at [94]–[96]; Bonn puts it at
31 May.

#### Image checks

Every two-page spread from 967 to 1124 was viewed at 100 dpi, most of them
twice. The spreads viewed on the local supplement were:

- 1125–1130 and 1133–1136;
- 1141–1142, 1155–1158, 1161–1162 and 1165–1168;
- 1175–1184, 1189–1194 and 1207–1220.

The seam and opener pages 965–967, 1025, 1089–1090 and 1125 were also viewed.
On the Mame side, the pages viewed were:

- 931–934, 937–938, 949–952 and 959–962;
- 1030, 1033–1034 and 1113–1124;
- the index, pp. 1136–1138.

The checks resolved these cases:

- the typo *Prætatio* on p. 1024, which is a Preface referral;
- the typo *Offebrium* on p. 1060, which is the Offertory;
- *Postcomrnunio* on p. 1128;
- the duplicated Saturday collect;
- the marriage-Mass units;
- the alternative episcopal-consecration texts;
- the referral-only local headings;
- the Commons with two forms, *I* and *II*.

#### Limits

These are structural identities, not wording collations. Labels identify units
and are not verified text. The slot slices are `partial`. The reasons are as
follows:

- Inherited appointments are not expanded: Commons and Masses of the day used
  with printed prayers, and the seasonal second and third prayers.
- Inline Credo, Gloria and Alleluia directions are not separate slots.
- The All Souls Masses are referred to the Proper of Saints.

The local propers are conditional local use, not membership of the universal
calendar.

Rights and provenance are affected in three places:

- On p. 1189 the printed rank note for St Pius X names the *Fraternitas
  sacerdotalis S. Pii X*. It is therefore a publisher's insertion later than
  1954, and was not made a target.
- The local supplement carries marginal *P* and *C (1)* markers, apparently
  publisher apparatus.
- Cross-references print as `[000]`.

The artifact record's rights note places the Immaculate Heart (1944) in the
local supplement. Bonn prints that Mass at p. 856, in the Proper of Saints, and
this extent contains no Immaculate Heart Mass. The record needs correcting. A
negative found only in the Mame OCR was always rechecked on Mame page images
or in its printed index.

### Independent review of the pre-1955 whole-book boundaries

On 19 October 2026 an independent reviewer compared the pre-1955 targets with
the witness. It used three self-derived checks over the typeset layer:

- 946 bold and large heading clusters;
- 418 Introit markers;
- 395 date headings and 274 rank lines.

It also checked the Kalendarium against the sanctoral, and viewed 151 Bonn page
images (a seeded stratified sample of 62, every disagreement, the Kalendarium
and the whole Preface section) and 31 Mame page images.

It found no missing and no phantom formulary heading, and exactly fifteen
Preface identities: 14 solemn, 15 ferial and 15 spoken headings, with every
Preface appointment naming one of them. *Vere dignum* outside the Preface
section occurs only in Holy Week rite texts: the palm blessing (p. 277), the
Exsultet (p. 338) and the font blessing (p. 359).

Corrections applied:

- two votive referral headings (pp. 1065, 1075) are now `form`;
- the two 3 May companion commemorations are merged into one;
- Margaret Mary's Kalendarium row (10-17) moves to the post-1922 additions,
  because Mame has Hedwig on 10-17 and Margaret Mary only in its local
  supplement;
- Hedwig's date move is recorded;
- an Apostles' Preface appointment printed mid-line on p. 613 is added;
- two locators move from p. 572 to p. 573.

The whole-book **form** and **Preface** boundaries are therefore retired. The
pre-1955 Mass-formulary denominator is 604 `form` rows across the temporal,
sanctoral, Commons, Marian Saturday, votive, dead, local-proper and local-Common
slices. The 23 preparation and thanksgiving entries share the kind but are not
formularies. Celebration, commemoration, Common, Ordinary-option,
exceptional-rite and text-slot boundaries stay `unenumerated`, each with a
specific basis:

- the body prints identities the Kalendarium omits;
- occurrence-dependent commemorations are not enumerated;
- inline directions outside the temporal are not enumerated;
- rites referred to the Rituale or Pontificale are not enumerated;
- the body slot slices are partial. The p. 613 miss shows that mid-line markers
  can escape the line-start method.

The review left these limits:

- no wording collation;
- no correspondence of this conformed printing to the 1920 typical edition;
- a residual risk of a heading that escaped every check on an unviewed page,
  since Bonn prints no index;
- for 7 May to 10 July, Mame-side absence rests on its Proprium and index,
  because its Kalendarium leaf is missing from the scan.

## Retrieval bounds and remaining work

**Retry, 19 October 2026.** After the execution restrictions were removed, the
retry superseded three of the access findings below. The registered CMAA 1962
facsimile was acquired whole with its registered hash and is inventoried in the
section above. Isidore item 3453 was retrieved and is byte-identical to the
registered 2004 Bonn *reimpressio*, so it is not a 1920 Vatican impression. The
selected U.S. edition's General Index was acquired from the publisher's preview
and is inventoried above. An authenticated 1920 Vatican typical impression and
authenticated complete 2008 contents or body evidence remain outstanding. A
bounded search of the major digital libraries and catalogues found neither. Every
file circulating as the "1920 typical edition" is the registered Bonn
*reimpressio*. The 2008 body exists online only as a paid electronic re-typeset.
Gallica, BNE, Internet Culturale, DigiVatLib and the Polish FBC federation were
behind bot challenges and were not searched. The
[acquisition audit](missal-acquisition-audit-v1.toml) records the hosts reached.
The bullets that follow record the earlier pass as it happened.

The second pass pursued registered alternatives rather than treating a local
absence as a worldwide absence:

- The registered CMAA 1962 PDF was rejected by the web reader at 82,815,941
  bytes; the registered Internet Archive SP07 alternate and Benziger OCR did
  not open. A shell retrieval could not resolve the remote host.
- The registered Mame 1922 PDF and OCR did not open through the web reader.
- An Isidore OCR-only 1962 delivery was rejected at 30,423,728 bytes; a bounded
  indexed search corroborated rubric 271. It was not acquired whole or hashed,
  is not a registered new witness, and is not substituted for the target
  artifact. The tracked assembly rubric index remains the inventory's owner.
- The registered 2002 digital reproduction opened in full through the web
  reader. A shell download failed DNS resolution, so this review records no
  fresh local byte acquisition or hash verification. Protected payloads were
  not retained or added to the repository.
- An exact-target follow-up opened the official 2008 Notitiae source, but found
  no authenticated complete 2008 body or structural index. The nominal 2008
  link at [Liturgia.it](https://www.liturgia.it/index.html) resolves to an
  [expanded partial transcription](https://iglesiaactualidad.wordpress.com/liturgia/missale-romanum/)
  containing later decrees through 2024 and incomplete ritual/needs/votive
  contents. It was not accepted as an exact-edition denominator. Searches for
  the 2008 title, index and ISBN 9788820981204 returned catalogue or sales
  metadata and the registered correction list.
- The exact 1920 impression is corroborated by
  [WorldCat 224202518](https://search.worldcat.org/title/Missale-Romanum/oclc/224202518)
  and [Google Books Z4zIzgEACAAJ](https://books.google.com/books/about/Missale_romanum.html?id=Z4zIzgEACAAJ),
  but their accessible pages expose no body or contents scan. A new candidate
  [Isidore item 3453](https://isidore.co/calibre/browse/book/3453) has a directory
  label claiming 1920; its PDF redirects to an inaccessible host and no title
  page was inspected. It remains unauthenticated and is not identified with
  either the exact target or the known composite. Bounded searches covered
  Archive.org, Google Books, Gallica, Vatican-title metadata and Isidore leads.

These are access findings for the named routes in this session, not claims that
the books cannot be obtained. Existing registered records remain the evidence
for prior acquisitions and collations.

The named 2002 source queues are now enumerated at their declared granularity:
temporal and sanctoral forms, Commons, ritual/needs/votive/dead entries, main
Ordinary options, appendix structures and the full Preface index. The already
extracted sanctoral core-role markers and the Common's explicit proper options
also have individual targets. The official 2008 Supplementum's printed
appointment/referral extent is separately complete. None of these facts
establishes an entire exact target book's denominator.

Further work runnable from the accessible 2002 witness comprises nested
alternatives within the remaining formularies, ritual and Eucharistic-Prayer
units, and reconciliation of Common/seasonal/Ordinary references.
Its absent Appendix I music cannot be reconstructed from index headings. More
2002 body detail would refine a source inventory; it cannot by itself establish
2008 membership or wording. The official variation list can independently
establish the specific changed appointments it positively names, but its silence
cannot turn the rest into target attestations. The missing downstream Lectionary
and Hours source inventories similarly cannot be supplied by familiar practice.

The next acquisitions needed for whole-target C1 are concrete: an authenticated
1920 Vatican typical impression with title, contents and body; authenticated
2008 contents/body evidence or documented correspondence for each bounded source
slice; the selected U.S. English edition's structural dispositions; and readable
access to the already registered complete 1962 target facsimile. For 1920, the
catalogued Vatican impression and unverified Isidore 3453 delivery are leads,
not attested replacements for the known composite. For 2008, the LEV ISBN
9788820981204 identifies the desired volume; the incomplete later web
transcription is unsuitable. For 1962, access to either registered CMAA or SP07
artifact through a delivery capable of handling its size would allow the
remaining whole-book inventory. These are source or retrieval blockers, distinct
from known unavailable wording at an already enumerated target.

Closing C1 still requires those target-book extents and their semantic slots to
be reconciled. Missing enumeration cannot be repaired by assigning every held
row a state, and this record does not claim to have done so.
