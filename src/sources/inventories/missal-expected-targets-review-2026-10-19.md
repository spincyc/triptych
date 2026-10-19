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

The source-backed
[postconciliar sequence inventory](../../claude/liturgy/roman-rite/postconciliar/2008-latin-2011-us-english/ordinary/00-order-of-mass/research/sequence-inventory.md)
provides positive identities for greetings, Penitential Acts, sprinkling, Creeds,
the four principal Eucharistic Prayers, priestly preparation alternatives,
dismissals and blessing classes. These include choices beyond the current
selectors. Blessing classes do not enumerate every numbered blessing. Roman
Canon inserts, internal alternatives, supplementary Eucharistic Prayers and
individual prayers over the people still need their own source-defined detail.

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
defensible main-section denominator, not the book's complete Preface count and
not a collation of the 2008 reprint or English expression.

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
| Commons | 536–592 | 60 numbered formularies beneath 33 section headings |
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

Internal alternate Collects and antiphons, proper Prefaces and Eucharistic
Prayer inserts, blessings, conditional appointments, and semantic slots remain
separate work. These are per-entry structural unknowns; the named body entries
themselves are now enumerated within the five stated source sections. This was a
bounded reading of that registered source's delivery, not a fresh hash check or
acquisition receipt; its existing artifact and edition limitations still apply.

The registered official
[2008 variation list and Supplementum](../works/holy-see/variationes-et-additiones-missalis-romani-2008/editions/latin-notitiae-503-504/segments/notitiae-pages-368-387.toml)
also opened through the web reader. A separate bounded slice records fourteen
positive 2008 target identities: the extended Pentecost Vigil, six post-reading
prayer alternatives, two Vigil dismissals, the September 8 Prayer over the
Offerings, an alternative Prayer over the Offerings for Marian Common I.1, and
the Collects of Pio, Juan Diego and Guadalupe. These have established identity
from the official 2008 publication itself. Their language availability and
publication status are separate questions. The three general dismissal additions
already occur in the Ordinary-option inventory and are not counted again here.

The official notice and the existing Ordinary source audit explicitly limit the
variation list: it is directed to changes affecting translation, while further
presentation and textual corrections are unlisted. Its silence cannot establish
exact 2008 correspondence for every 2002 row. The selected Supplementum slice
also leaves the extended Vigil's remaining readings, responses, Vespers options,
references and ritual actions unenumerated; it does not hide those under a
claim of a complete rite.

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

These are access findings for the named routes in this session, not claims that
the books cannot be obtained. Existing registered records remain the evidence
for prior acquisitions and collations.

Closing C1 for the full intended scope still requires an item-level body/index
reconciliation for temporal weekdays, conditional appointments, proper Prefaces
outside the main section, Ordinary subdivisions, appendix and exceptional rites,
and appointed semantic slots and internal alternatives of the enumerated forms;
the exact pre-1955 target witness; and explicit 2008/U.S. edition dispositions.
Known unavailable wording can then be classified per target without blocking an
otherwise complete identity inventory. Missing enumeration cannot be repaired by
assigning every current held row a state, and the accompanying record does not
claim to have done so.
