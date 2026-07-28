# Object inventory

Status: **54 canonical records populated; 27 records in the current comprehensive alpha**
Audit date: 2026-07-28

The authoritative format is the structured contract under `shared/schema/`.
This Markdown file is the human audit index for the populated TOML records and
their validator. The names in the discovery queue below are **candidate search
terms**, not verified identities, prescribed forms, exhaustive lists, or
authorization to render an entry.

## Workflow counts

| State | Count |
| --- | ---: |
| Lead | 2 canonical records |
| Identified | 10 |
| Source-audited | 33 |
| Art-reviewed | 3 |
| Priestly-review-ready | 4 |
| Publication-ready | 2 |
| Held | 0 canonical records |

`shared/schema/object.example.toml` is a syntax fixture and is excluded from
all counts. These counts describe canonical workflow labels. The canonical
alpha path separately admits a source-audited or later record only when
identity and status are resolved, every rendered factual claim has a
claim-verified binding, artwork rights/provenance and exact asset identity are
recorded, and the visual has passed identity and basic usability review. There
is no external-review admission path.

The structured inventory validator accepts all 54 records as conforming to
the current TOML contract. That is a structural result only: it does not close
the source corpus, the completeness matrix, variants, artwork review, rights,
or any publication gate.

## Candidate discovery queue

| Category | Illustrative search terms to test | Principal unresolved boundary |
| --- | --- | --- |
| Church and sanctuary | altar, high altar, side altar, predella/footpace, steps, rail, gates, tabernacle, canopy/baldachin, credence, sedilia, throne, faldstool, pulpit, lectern, sacristy furnishings | Prescribed/presupposed object versus architectural or local practical furnishing |
| Altar and appointments | altar stone, sepulchre, cloths, frontal/antependium, gradine, cross, candlesticks, cards, tabernacle veil, sanctuary lamp, reliquary, protective cover | Universal requirement, permission, custom, and decoration |
| Sacred vessels | chalice, paten, ciborium, pyx, lunette, monstrance, oilstock | Vessel taxonomy, components, pontifical or related-ceremony scope |
| Linens and textiles | corporal, purificator, pall, lavabo towel, credence cloth, Communion cloth, amice, chalice veil, burse, humeral veil, gremial, vimpa | Similar white textiles; fold, marking, size, and handler claims |
| Books and printed objects | Missal, stand/cushion, Epistolary, Evangeliary, chant books, Ritual, Pontifical, Ceremonial, markers, covers | Exact official title versus generic physical object |
| Service objects | cruets, tray, basin, pitcher, bells, Communion plate, taper, lighter/extinguisher, torches, processional cross, stands/racks | Liturgical object versus practical equipment; branch dependence |
| Incense | thurible, boat, spoon, stand, container | Components, safe disposition, and substantive forms |
| Priestly vestments | amice, alb, cincture, maniple, stole, chasuble, cope, biretta | Construction forms, privileges, colors, and decorative variation |
| Deacon and subdeacon | dalmatic, tunicle, stole arrangement, maniple, folded chasuble, broad stole, humeral veil | Ceremony and reform horizon; worn arrangement |
| Pontifical and prelatial | stockings, sandals, gloves, ring, pectoral cross, under-vestments, pallium, mitres, crosier, gremial, rationale, choir dress; throne/faldstool compositions, books and supports, hand candle, hand-washing articles, vimpae, insignia supports, additional credences, conditional altar and processional articles | Rank, privilege, function, use-specific status, and the complete preparation-transfer-disposition chain; see `pontifical-ceremony-candidate-audit.md` |
| Servers, ministers, choir | cassock, surplice, cotta, rochet, apparelled forms, role-specific carried objects | Vesture by rank, region, institution, and religious community |
| Requiem | bier, catafalque, funeral pall, candles, absolution equipment | Mass versus absolution; universal versus local arrangement |
| Nuptial and ritual | nuptial cloth/veil, kneelers, stools, ceremony-specific books and vessels | Universal provision versus regional custom |
| Holy Week | palms, repository furnishings, crosses and veils, special candles, fire and incense equipment, ceremony-specific stands and vessels | Exact 1962 reform state; celebration-specific presence |
| Related ceremonies | aspergillum, holy-water vessel, monstrance-related equipment, canopy, humeral veil, processional objects | Separate related-ceremony scope and overlap with Mass |
| Historical | obsolete or discontinued objects found by period-specific source audit | Roman identity, chronology, cessation, survival, and revival |

## Canonical record checklist

Before a candidate receives an `obj-...` ID, record at minimum:

1. preferred English and Latin headwords and material aliases;
2. category, period, status, ceremonies, branches, and presence;
3. appearance and only substantive variants;
4. placement, function, handler, disposition, and server relation;
5. confusable and related objects;
6. claim-level source IDs, exact loci, evidence states, rights, and limits;
7. artwork requirements and audience relevance;
8. unresolved contradictions and publication hold state.

## Focused Pontificale discovery evidence

The comparative contents printed on pp. IX--XII of Sodi and Toniolo's
publicly hosted introduction to the 2008 Vatican facsimile was inspected on
2026-07-27. It supports only the bounded statement that the 1961--1962
Pontifical includes rites or blessings bearing the following object-relevant
titles. It does **not** verify an object's form, component parts, dimensions,
ordinary presence at Mass, handler, or the full contents of the rite.

| Part and facsimile-introduction locus | Named rite/blessing that opens an inventory lead | Candidate inventory implications | State |
| --- | --- | --- | --- |
| Pars prima; introduction p. IX | *De pallio* | pallium; its relationship to patriarchal/archiepiscopal use | Identified source lead; full rite uninspected |
| Pars secunda; introduction pp. IX--X | rites for the first stone, church dedication, altar consecration, portable altar, bell, cemetery, chalice and paten, antimension | foundation stone; altar and altar sepulchre/relic context; portable altar; bell; chalice; paten; antimension | Identified source leads; full rites uninspected |
| Pars secunda; introduction p. X | general blessing of sacred vessels and church/altar ornaments; blessing of tabernacle, pyx, ostensorium, and *theca* | tabernacle; pyx; monstrance/ostensorium; *theca*; unresolved class of sacred vessels and ornaments | Identified source leads; terminology and scope unresolved |
| Pars secunda; introduction p. X | blessings of altar cloths, corporal, pall, purificator, and priestly vestments | altar cloths; corporal; chalice pall; purificator; priestly-vestment class | Identified source leads; material, fold, marking, and handling unverified |
| Pars secunda; introduction p. X | blessings of a new cross, pectoral cross, images, reliquary cases, holy water, incense, and altar/church furnishings | altar/processional/other cross types unresolved; pectoral cross; images; reliquary cases; holy-water and incense equipment | Identified source leads; object boundaries unverified |
| Pars tertia; introduction pp. X--XI | Holy Thursday office in which oils are blessed and chrism is confected | vessels for oils, balsam, and chrism; related episcopal composition | Identified source leads; actual vessel names and forms require the full rite |
| Appendix; introduction p. XII | pontifical rites for Baptism and Matrimony and pontifical blessing within Solemn Mass | ceremony-specific vessels, books, furnishings, and insignia to test against full rubrics | Category lead only; no object inferred |

Pierre Jounel's contemporary survey in *La Maison-Dieu* 75 (1963), pp.
155--158, independently corroborates these three book-level inventories and
adds one materially useful distinction: in his account of Book II, the
portable altar is distinguished from the simple altar stone or *tabula*, with
different rites. This creates two confusable-object leads; it does not yet
support canonical dimensions, construction, placement, or handling claims.
The same survey reports that the Book II formularies include cult objects,
liturgical vestments, sacred images, holy water, Gregorian water, incense,
altar cloths, and sacred vessels, while Book III includes the holy oils and
chrism on Holy Thursday.

Paul VI's official 1978 *Inter eximia* calls the pallium an insignia of
episcopal office and cites the 1962 Pontifical, Pars prima, p. 92. This
supports a focused identity-class lead and exact locus target; it does not
make the later 1978 discipline the inventory's 1962 status rule.

This evidence adds search targets but does not itself advance any record.
The workflow counts above supersede earlier tranche snapshots. Canonical alpha
admission is evaluated separately from the workflow label and presently
admits twenty-seven records to the comprehensive bounded edition.

## Alpha boundary

Do not convert the discovery queue into prose or captions. A record enters the
bounded public alpha only through the canonical source, rights, identity,
safety, and visual-usability gate described above. A familiar name or
plausible image never establishes eligibility, and alpha admission does not
claim that a category or the comprehensive corpus is complete.
