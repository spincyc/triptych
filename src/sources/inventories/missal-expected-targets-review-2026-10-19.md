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
through the web reader, then inspected its index. The index identifies Common
subdivisions, additional Eucharistic Prayers and a one-minister Order of Mass.
It also locates ritual, votive and funeral material outside the calendar.
These positive headings enter bounded slices. A body check of the Marian Common
confirmed numbering beneath a heading: index leaves cannot stand in for every
formulary. Whole-book and internal-form enumeration remain open. This was a
bounded reading of that registered source's delivery, not a fresh hash check or
acquisition receipt; its existing artifact and edition limitations still apply.

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
reconciliation for temporal weekdays, all Commons and conditional appointments,
votive/ritual/Requiem formularies, proper Prefaces outside the main section,
Ordinary subdivisions, exceptional rites, and their appointed semantic slots;
the exact pre-1955 target witness; and explicit 2008/U.S. edition dispositions.
Known unavailable wording can then be classified per target without blocking an
otherwise complete identity inventory. Missing enumeration cannot be repaired by
assigning every current held row a state, and the accompanying record does not
claim to have done so.
