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

The inventory adds 35 slices, 7,621 targets and 30 boundaries for `roman-1962`.
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
| `sanctoral-preface-appointments` | partial | slot 42 |
| `purification-rite` | partial | slot 13, rite-unit 3, referral 1 |
| `body-commons-forms` | complete | form 24, prayer-set 17, common 4 |
| `body-marian-saturday-forms` | complete | form 5 |
| `body-votives-forms` | complete | form 33, prayer-set 18, ord-opt 6, referral 1 |
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
| `local-additional-commons` | complete | slot 90, prayer-set 12, common 6 |
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
- **Prefaces.** Preface headings and the *Vere dignum* incipit occur only in the
  Preface section, artifact pp. 305–379, and in the solemn-tone appendix,
  pp. 1044–1070. The appendix has fourteen tones of existing Prefaces. Every
  section lane records Preface appointments only as referrals. This supports
  treating the sixteen existing Preface identities as the whole book's Preface
  identity inventory, but the search ran over extracted text.

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

The whole-book slice therefore remains `unresolved`. Retiring its form and
Preface boundaries was proposed and, on 19 October 2026, deferred: the
formulary cross-check supports whole-book form enumeration, but the sanctoral
and Commons sections rest on their first lanes' image checks and have not been
independently re-verified, and the Preface search ran over extracted text. Both
boundaries stay `unenumerated` with that evidence restated, until an
independent review confirms them on page images. Text slots, Ordinary options, commemorations,
Commons as a kind, and exceptional rites keep explicit `unenumerated`
boundaries. No whole-book text-slot denominator is asserted.

Known presentation inconsistencies are retained rather than silently
normalized. The kind `common` holds four additional-reading pools as well as
the local Common headings, while the main Common Masses are `form`. Holy Week
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

## Retrieval bounds and remaining work

**Retry, 19 October 2026.** After the execution restrictions were removed, the
retry superseded three of the access findings below. The registered CMAA 1962
facsimile was acquired whole with its registered hash and is inventoried in the
section above. Isidore item 3453 was retrieved and is byte-identical to the
registered 2004 Bonn *reimpressio*, so it is not a 1920 Vatican impression. The
selected U.S. edition's General Index was acquired from the publisher's preview
and is inventoried above. An authenticated 1920 Vatican typical impression and
authenticated complete 2008 contents or body evidence remain outstanding. The
bullets that follow record the earlier pass as it happened.

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
