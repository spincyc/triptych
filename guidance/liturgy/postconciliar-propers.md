# Postconciliar Proper Guides

This profile governs guides to the variable parts of postconciliar Roman-rite liturgies. It supplements the repository-wide editorial and source rules. It does **not** inherit the architecture of the 1962 weekly guides: their ten-item proper inventory, Lent-first numbering, fixed page sequence, historical dossier shape, Latin-incipit conventions, and section titles are not defaults here.

Under the present provider, each document lives at `src/gpt/liturgy/roman-rite/postconciliar/<edition-locale>/propers/<calendar-family>/<document>/`; another provider uses the same content taxonomy beneath its own provider directory. The edition-locale component is an identity guardrail, not a substitute for the fuller manifest below.

## Establish the liturgical instance first

Before research or drafting, create a manifest that identifies the texts actually being studied. Record at least:

- the Latin typical edition of the Roman Missal and, when applicable, its printing or reprint;
- the vernacular Missal edition, language, episcopal conference or territory, publisher, and approval or implementation date;
- the Lectionary edition and volume, language, territory, and edition-specific reading references;
- the governing calendar: General Roman Calendar and every national, diocesan, religious, parish, or other proper calendar that affects the celebration;
- the celebration, rank, ritual or pastoral context, and civil date when a date is needed to resolve precedence;
- the Sunday cycle (`A`, `B`, or `C`), weekday cycle (`I` or `II`), and any special cycle or vigil form;
- every permitted option selected, including alternative readings, prayers, prefaces, ritual forms, or formulary sources; and
- unresolved choices that would produce materially different documents.

Do not combine texts from different editions, territories, cycles, calendars, or option paths into a synthetic formulary. If several legitimate paths deserve treatment, identify each as a variant and show which claims belong to which path. A date alone never identifies a liturgical instance adequately.

## Inventory the variable texts

Build the document around the appointed elements of the identified celebration, not around a legacy item count. Distinguish:

- Missal prayers and antiphons;
- Lectionary readings, responsorial psalm, Gospel acclamation, and authorized alternatives;
- proper chants from an identified chant book;
- ritual texts supplied by another approved book;
- options chosen locally under the rubrics; and
- hymns, songs, or pastoral additions that are not themselves appointed propers.

Do not silently substitute a Gradual, another chant source, or a locally selected song for a Missal or Lectionary text. State the source and liturgical status of each item. Preserve mandatory, optional, seasonal, and omitted elements as distinct categories.

The guide's order and teaching forms should follow the actual formulary and the reader's needs. A concise map, historical context, source-grounded exposition, bounded editorial synthesis, and references may remain useful; structured generation metadata remains required under the universal standard, but the 1962 guide's exact placement, headings, page counts, tables, and macro-order apply only when this profile explicitly adopts them.

## Copyright-aware source records

Keep a source record beside each guide, but do not assume that an accessible liturgical text may be republished. For every source record:

- give the exact title, edition, language, territory, publisher or rights holder, year, volume, page or stable locator, and access date;
- record the celebration, element, incipit, biblical citation, and verification result with enough precision to reproduce the research;
- state the source's copyright or licensing status when known and flag uncertainty rather than guessing;
- quote only the minimum needed for verification and commentary unless permission or a compatible license authorizes more;
- prefer citations, incipits, references, and original analytical notes over repository copies of complete protected vernacular texts; and
- do not commit scans, bulk transcriptions, paywalled material, or circumvention-derived text.

A private copy used lawfully for collation is not automatically a distributable repository source. When the full wording cannot be tracked, record the edition and locator plus a verification note; never reconstruct a protected translation from memory or mix it with another edition. Biblical copyright and liturgical-text copyright must be evaluated separately.

## Research and claims

Read each selected passage in its complete literary context and study each prayer or chant as an edition-specific liturgical text. Distinguish what the approved text says, what its biblical or historical sources establish, what official liturgical documents teach, and what the project proposes as synthesis. Rubrical permission is not evidence of pastoral preference, and a permitted option is not necessarily appointed in every celebration.

When describing development from an earlier Missal, compare identified editions directly. Do not treat the postconciliar form as a paraphrase of 1962, project later categories backward, or present historical influence as identity without evidence.

## Completion gate

A postconciliar proper guide is ready to publish only when:

- the liturgical-instance manifest resolves edition, language, territory, calendar, cycle, and options;
- every treated element has a source and liturgical-status classification;
- quotations and tracked records comply with the applicable copyright or license;
- variant paths and local choices are not presented as universal requirements;
- authoritative claims and editorial synthesis are visibly distinct; and
- the PDF and its mirrored source records pass the repository-wide build and editorial checks.
