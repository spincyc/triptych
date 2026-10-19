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

## Retrieval bounds and remaining work

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
