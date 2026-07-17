# Roman Calendar References

## Scope, identity, and location

This profile governs edition-specific reference works whose principal objects are the construction, historical development, and complete normative inventory of a Roman-rite liturgical calendar. It applies across editions only at the level of method. The identified typical book, rubrics or general norms, territory, language witness, jurisdiction, and terminal date determine each publication's substance; terminology and rules from one calendar may not be projected into another.

Under the present provider, a 1962 reference lives beneath `src/gpt/liturgy/roman-rite/1962/reference/`. A postconciliar reference lives beneath `src/gpt/liturgy/roman-rite/postconciliar/<edition-locale>/reference/`. Their build and installed PDFs mirror those paths. Each work has one catalog home on the page for its edition.

These references are recurring calendars, not civil-year Ordos. Unless a request names and the work computes a year, “complete calendar” means the complete normative movable cycle, every fixed universal entry, and every entry in the identified territorial overlay as of the stated cutoff. It does not mean that all entries will be celebrated in a particular year: occurrence, precedence, transfer, omission, and local propers still have to be resolved.

The historical module follows the evidence and timeline rules in `guidance/history/historical-accounts.md`; the normative module follows the identified edition's liturgical profile and controlling books. The local scope states which profile governs each module. A historical practice does not establish current law, and a current calendar does not prove an account of its own origins.

## Calendar layers and terminology

Keep these layers distinct throughout:

1. the Proper of Time or temporal cycle, including movable Sundays, seasons, privileged ferias, vigils, octaves, Ember or Rogation days where applicable, and celebrations positioned relative to Easter, Christmas, or a weekday;
2. the universal fixed calendar or sanctoral cycle;
3. a territorial calendar approved for a named bishops' conference or nation;
4. diocesan, religious-family, church-title, dedication, patronal, and other local propers; and
5. later permissions or optional mechanisms that supplement use of an older book without silently rewriting its printed base calendar.

Use the taxonomy of the calendar being documented. The 1960/1962 system has Sundays and ferias of their proper classes, feasts of class I, II, or III, and commemorations; it has no postconciliar category called an optional memorial and no general class called an optional feast. The postconciliar system distinguishes solemnities, feasts, obligatory memorials, optional memorials, and commemorations governed by its norms. Explain any ordinary-language request for “optional feast days” using the edition's real categories.

English calendar labels must come from an identified human edition or official calendar, or be expressly described as editorial identifiers rather than translations of liturgical text. Do not reproduce prayers, readings, chants, or complete third-party liturgical formularies merely to prove an entry's existence.

## Controlling sources and amendment cutoff

Record the source hierarchy before drafting. It ordinarily runs from promulgating act and typical calendar or Missal, through the applicable general norms, to the approved territorial proper and later decrees. A contemporary official annual calendar can verify how those sources are implemented in its year; it cannot by itself establish that an entry absent because of occurrence has disappeared from the recurring calendar. OCR, indexes, commercial calendars, Wikipedia, and devotional lists are discovery or transcription aids only.

Every publication states an exact amendment cutoff. For mutable postconciliar calendars, check official decrees and the competent territorial authority through that date. For a historical edition, distinguish the calendar printed or legally incorporated in the edition from later permissions to add celebrations while using it. Present authorization to celebrate according to an older book is a separate canonical question unless deliberately researched and dated.

## Required research records

Every calendar-reference leaf contains `main.tex`, `generation-metadata.tex`, organized `sections/`, and:

- `research/scope.md`, identifying rite, edition, language or label witness, territory, jurisdiction, historical period, normative cutoff, intended reader, inclusion and exclusion rules, terminology, material uncertainties, rights review, and review state;
- `research/edition-manifest.md`, identifying the promulgating acts, typical calendar or Missal, rubrics or general norms, territorial proper, later amendments, and non-controlling aids;
- `research/source-audit.md`, recording exact bibliographic data, stable links and access dates, file identity where locally checked, loci actually used, source role, OCR status, rights basis, rejected leads, and unresolved discrepancies;
- `research/evidence-map.md`, aligning each major construction-history and amendment claim with its evidence class, exact witness, confidence, and qualification; and
- `research/calendar-inventory.md`, accounting for every normative temporal identity and fixed entry, its date rule, rank or status, universal or territorial owner, exact controlling locus, transcription check, and any unresolved issue.

The records are an audit, not a search diary. Do not retain complete scans or bulk OCR in the publication leaf. A catalog entry links all five reader-facing records separately.

## Publication architecture

The title or one compact identity line names the exact edition and territory. Because an inventory of mutable law can become unsafe when detached from its date, that line may also give the amendment cutoff and point to the terminal appendix; it does not reproduce the source hierarchy, omitted layers, review status, or other qualifications. After the title and table of contents, the rendered reference begins with its substantive construction history or its guide to the calendar's layers, not a scope or method chapter. It includes:

- a periodized construction history that distinguishes origins, codification, inherited layers, and deliberate reform;
- a guide to the calendar's layers, ranks, and interaction rules;
- the complete normative movable cycle;
- the complete fixed universal inventory, month by month;
- a separate complete territorial overlay, with its actual ranks and displacement or transfer effects;
- an account of any later optional mechanism where it materially changes how the inventory is used;
- a terminal dated timeline appendix of substantive modifications, with selection criteria stated so that routine reprints are not mislabeled as reforms;
- a terminal `Scope, Edition, and Qualifications` appendix containing the object and thesis boundary, full edition and language witness, territory and jurisdiction, historical period, amendment cutoff, terminology, method, source hierarchy, inclusion and exclusion rules, omitted local layers, global uncertainties, rights and review limits;
- references grouped by controlling books, official amendments, territorial sources, and historical scholarship; and
- terminal structured generation metadata.

The timeline and scope sections may be adjacent parts of one appendix block, but neither appears before the substantive history or calendar system. Dense tables must remain readable at ordinary print size and repeat their headings across pages. Narrative interprets rather than merely restates the timeline and tables. The reference may use concise editorial English labels, but it must identify their witness and must not imply that an inventory is a substitute for a competent Ordo. A disputed date, uncertain origin, rank exception, transfer condition, or territorial difference remains beside the row or claim it qualifies.

## Completeness and review gate

Before installation:

- reconcile the inventory count and every row against the calendar inventory record;
- confirm that every month, movable celebration, vigil, octave, Ember or Rogation provision, and territorial entry required by the selected edition is accounted for;
- test all substantive timeline claims against the evidence map and preserve disputed or unrecoverable origins;
- confirm that substantive history or calendar use begins immediately after the title and contents and that the full scope, method, date range, cutoff, omitted-layer account, global qualifications, and timeline occur only in the terminal appendix block;
- verify rank changes, transfers, territorial status, promulgation and effective dates, and every amendment through the cutoff;
- keep universal, national, diocesan, religious, titular, patronal, and optional layers distinct;
- confirm that the work does not present a recurring inventory as a computed Ordo or imply present authorization beyond scope;
- complete link, quotation, translation, and rights review;
- run universal metadata and publication checks, including terminal provenance, multi-pass build, clean-log inspection, every-page visual review, PDF structure checks, installed/build comparison, and catalog and release-manifest updates; and
- record independent historical and liturgical review as outstanding until named review events occur.
