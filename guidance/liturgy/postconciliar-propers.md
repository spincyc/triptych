# Postconciliar Proper Guides

This profile governs study guides to the textual variable parts of identified postconciliar Roman-rite celebrations. It supplements the repository-wide editorial and source rules. The identified Missal, Lectionary, ritual books, calendar, and approved chant sources supply the inventory, order, terminology, and section design. Each guide first documents the texts appointed or lawfully selected for the identified celebration or formula target, then develops a source-grounded study guide from those texts, their ritual placement, scriptural context, and documented relationships.

Under the present provider, each document lives at `src/gpt/liturgy/roman-rite/postconciliar/<edition-locale>/propers/<calendar-family>/<document>/`; another provider uses the same content taxonomy beneath its own provider directory. The edition-locale component is an identity guardrail, not a substitute for the fuller manifest below. The Sunday series fixes `<calendar-family>` as `temporal`; the General Calendar replacement series fixes it as `general-calendar`.

## Canonical Sunday-proper production order

The postconciliar Sunday collection uses the following **60 stable Proper-of-Time identities**. This is the firm repository order for planning, identifiers, paths, status tracking, and creation. It follows the section order of the postconciliar Roman Missal—Advent, Christmas Time, Lent and Holy Week, Easter Time, Ordinary Time, and the Sunday-capable Solemnities of the Lord in Ordinary Time—independently of the occurrence pattern of any one civil year.

`PC-S` means the postconciliar Sunday-production series. It does not assert that every identity always occurs on Sunday: the series deliberately retains fixed or transferable Proper-of-Time celebrations that can occupy a Sunday, including the explicitly conditional Second Sunday after the Nativity and Seventh Sunday of Easter. IDs are permanent, may not be reassigned or renumbered, and do not establish liturgical rank or precedence. A document slug begins with the lowercase form shown below; cycle and form suffixes follow the variant rules after the table.

| ID | Required slug stem | Proper-of-Time identity |
| --- | --- | --- |
| PC-S01 | `pc-s01-first-sunday-of-advent` | First Sunday of Advent |
| PC-S02 | `pc-s02-second-sunday-of-advent` | Second Sunday of Advent |
| PC-S03 | `pc-s03-third-sunday-of-advent` | Third Sunday of Advent |
| PC-S04 | `pc-s04-fourth-sunday-of-advent` | Fourth Sunday of Advent |
| PC-S05 | `pc-s05-nativity-of-the-lord` | Nativity of the Lord |
| PC-S06 | `pc-s06-holy-family-of-jesus-mary-and-joseph` | Holy Family of Jesus, Mary, and Joseph |
| PC-S07 | `pc-s07-mary-holy-mother-of-god` | Mary, the Holy Mother of God |
| PC-S08 | `pc-s08-second-sunday-after-the-nativity` | Second Sunday after the Nativity |
| PC-S09 | `pc-s09-epiphany-of-the-lord` | Epiphany of the Lord |
| PC-S10 | `pc-s10-baptism-of-the-lord` | Baptism of the Lord |
| PC-S11 | `pc-s11-first-sunday-of-lent` | First Sunday of Lent |
| PC-S12 | `pc-s12-second-sunday-of-lent` | Second Sunday of Lent |
| PC-S13 | `pc-s13-third-sunday-of-lent` | Third Sunday of Lent |
| PC-S14 | `pc-s14-fourth-sunday-of-lent` | Fourth Sunday of Lent |
| PC-S15 | `pc-s15-fifth-sunday-of-lent` | Fifth Sunday of Lent |
| PC-S16 | `pc-s16-palm-sunday-of-the-passion-of-the-lord` | Palm Sunday of the Passion of the Lord |
| PC-S17 | `pc-s17-easter-sunday-of-the-resurrection-of-the-lord` | Easter Sunday of the Resurrection of the Lord |
| PC-S18 | `pc-s18-second-sunday-of-easter` | Second Sunday of Easter |
| PC-S19 | `pc-s19-third-sunday-of-easter` | Third Sunday of Easter |
| PC-S20 | `pc-s20-fourth-sunday-of-easter` | Fourth Sunday of Easter |
| PC-S21 | `pc-s21-fifth-sunday-of-easter` | Fifth Sunday of Easter |
| PC-S22 | `pc-s22-sixth-sunday-of-easter` | Sixth Sunday of Easter |
| PC-S23 | `pc-s23-ascension-of-the-lord` | Ascension of the Lord |
| PC-S24 | `pc-s24-seventh-sunday-of-easter` | Seventh Sunday of Easter |
| PC-S25 | `pc-s25-pentecost-sunday` | Pentecost Sunday |
| PC-S26 | `pc-s26-second-sunday-in-ordinary-time` | Second Sunday in Ordinary Time |
| PC-S27 | `pc-s27-third-sunday-in-ordinary-time` | Third Sunday in Ordinary Time |
| PC-S28 | `pc-s28-fourth-sunday-in-ordinary-time` | Fourth Sunday in Ordinary Time |
| PC-S29 | `pc-s29-fifth-sunday-in-ordinary-time` | Fifth Sunday in Ordinary Time |
| PC-S30 | `pc-s30-sixth-sunday-in-ordinary-time` | Sixth Sunday in Ordinary Time |
| PC-S31 | `pc-s31-seventh-sunday-in-ordinary-time` | Seventh Sunday in Ordinary Time |
| PC-S32 | `pc-s32-eighth-sunday-in-ordinary-time` | Eighth Sunday in Ordinary Time |
| PC-S33 | `pc-s33-ninth-sunday-in-ordinary-time` | Ninth Sunday in Ordinary Time |
| PC-S34 | `pc-s34-tenth-sunday-in-ordinary-time` | Tenth Sunday in Ordinary Time |
| PC-S35 | `pc-s35-eleventh-sunday-in-ordinary-time` | Eleventh Sunday in Ordinary Time |
| PC-S36 | `pc-s36-twelfth-sunday-in-ordinary-time` | Twelfth Sunday in Ordinary Time |
| PC-S37 | `pc-s37-thirteenth-sunday-in-ordinary-time` | Thirteenth Sunday in Ordinary Time |
| PC-S38 | `pc-s38-fourteenth-sunday-in-ordinary-time` | Fourteenth Sunday in Ordinary Time |
| PC-S39 | `pc-s39-fifteenth-sunday-in-ordinary-time` | Fifteenth Sunday in Ordinary Time |
| PC-S40 | `pc-s40-sixteenth-sunday-in-ordinary-time` | Sixteenth Sunday in Ordinary Time |
| PC-S41 | `pc-s41-seventeenth-sunday-in-ordinary-time` | Seventeenth Sunday in Ordinary Time |
| PC-S42 | `pc-s42-eighteenth-sunday-in-ordinary-time` | Eighteenth Sunday in Ordinary Time |
| PC-S43 | `pc-s43-nineteenth-sunday-in-ordinary-time` | Nineteenth Sunday in Ordinary Time |
| PC-S44 | `pc-s44-twentieth-sunday-in-ordinary-time` | Twentieth Sunday in Ordinary Time |
| PC-S45 | `pc-s45-twenty-first-sunday-in-ordinary-time` | Twenty-first Sunday in Ordinary Time |
| PC-S46 | `pc-s46-twenty-second-sunday-in-ordinary-time` | Twenty-second Sunday in Ordinary Time |
| PC-S47 | `pc-s47-twenty-third-sunday-in-ordinary-time` | Twenty-third Sunday in Ordinary Time |
| PC-S48 | `pc-s48-twenty-fourth-sunday-in-ordinary-time` | Twenty-fourth Sunday in Ordinary Time |
| PC-S49 | `pc-s49-twenty-fifth-sunday-in-ordinary-time` | Twenty-fifth Sunday in Ordinary Time |
| PC-S50 | `pc-s50-twenty-sixth-sunday-in-ordinary-time` | Twenty-sixth Sunday in Ordinary Time |
| PC-S51 | `pc-s51-twenty-seventh-sunday-in-ordinary-time` | Twenty-seventh Sunday in Ordinary Time |
| PC-S52 | `pc-s52-twenty-eighth-sunday-in-ordinary-time` | Twenty-eighth Sunday in Ordinary Time |
| PC-S53 | `pc-s53-twenty-ninth-sunday-in-ordinary-time` | Twenty-ninth Sunday in Ordinary Time |
| PC-S54 | `pc-s54-thirtieth-sunday-in-ordinary-time` | Thirtieth Sunday in Ordinary Time |
| PC-S55 | `pc-s55-thirty-first-sunday-in-ordinary-time` | Thirty-first Sunday in Ordinary Time |
| PC-S56 | `pc-s56-thirty-second-sunday-in-ordinary-time` | Thirty-second Sunday in Ordinary Time |
| PC-S57 | `pc-s57-thirty-third-sunday-in-ordinary-time` | Thirty-third Sunday in Ordinary Time |
| PC-S58 | `pc-s58-most-holy-trinity` | Most Holy Trinity |
| PC-S59 | `pc-s59-most-holy-body-and-blood-of-christ` | Most Holy Body and Blood of Christ |
| PC-S60 | `pc-s60-our-lord-jesus-christ-king-of-the-universe` | Our Lord Jesus Christ, King of the Universe, the Last Sunday in Ordinary Time |

There is no `PC-S` identity for a numbered First Sunday in Ordinary Time. Normally the Baptism of the Lord occupies that Sunday and Week I begins on Monday. Where a Sunday-transferred Epiphany falls on January 7 or 8, Epiphany occupies the Sunday, Baptism is celebrated Monday, and Week I begins Tuesday. There is no separate Thirty-fourth Sunday identity: Christ the King occupies the Last Sunday, while the weekdays of Week XXXIV have their own formulary. The Most Sacred Heart of Jesus is assigned to Friday in the General Calendar and therefore is not part of this baseline Sunday spine; any lawful Sunday observance is resolved as an occurrence overlay without renumbering `PC-S`.

### Fixed layout and ownership

Let `<proper-root>` mean `src/gpt/liturgy/roman-rite/postconciliar/<edition-locale>/propers`. Use these paths exactly; the corresponding publishable PDF mirrors follow the repository-wide `doc/` and `build/` rules.

| Material | Required source path | Publication status |
| --- | --- | --- |
| A `PC-S` cycle, form, or occurrence guide | `<proper-root>/temporal/<full-publication-slug>/` | Publishable leaf with `main.tex` |
| Canonical `PC-S` Missal formulary owner, except Ordinary Time II–XXXIII | `<proper-root>/temporal/shared/formularies/<required-slug-stem>/` | Non-publishable shared source |
| Canonical Ordinary Time formulary owner | `<proper-root>/temporal/shared/ordinary-time/weeks/01/` through `weeks/34/` | Non-publishable shared source |
| Canonical conditional Scrutiny Ritual Mass owner | `<proper-root>/ritual/shared/formularies/celebration-of-the-scrutinies/` | Non-publishable shared source owning the three Ritual Mass formularies |
| A `PC-R` cycle, form, or occurrence guide | `<proper-root>/general-calendar/<full-publication-slug>/` | Publishable leaf with `main.tex` |
| Canonical `PC-R` Missal formulary owner | `<proper-root>/general-calendar/shared/formularies/<required-slug-stem>/` | Non-publishable shared source |

The shared owner keeps the edition-specific verified Missal record, provenance, rights status, and any reusable source fragment. The publishable leaf owns its resolved liturgical-instance manifest, cycle-specific Lectionary audit, analysis, generation metadata, and PDF; it references or imports the shared owner and must not become a second owner of the formulary. For `PC-S26`–`PC-S57`, the corresponding `weeks/02`–`weeks/33` directory is the shared owner. A conditional Scrutiny leaf remains in the temporal Sunday queue but imports the Ritual Mass owner fixed above. Every import outside a publishable leaf requires an explicit cross-document build dependency, and a shared-source change requires rebuilding every consumer.

### Formula targets, keys, and fixed order

The 60 identities are stable celebration parents, not 60 finished guides. A **Sunday production formula target** joins one separately appointed Mass form to one cycle coverage and its complete Lectionary-path inventory for one edition-locale. This includes separately indexed simple and extended Vigil forms. It is a composition and reference record, not another owner or copy of the Missal formulary. Shorter readings, permitted substitutions, ritual entrance modes within one Mass, optional sequences, and similar choices remain named branches inside that target unless an approved book actually substitutes a different Missal or Ritual Mass formulary. A civil-year occurrence is not another target unless it changes the reading structure or treated scope.

Every target has a permanent formula key:

`PC-Snn-<coverage>[-<APPOINTED-FORM>][-O-<OCCURRENCE>]`

General Calendar replacement targets substitute `PC-Rnn` for `PC-Snn` and otherwise use the same grammar.

Order and interpret the components as follows:

1. keep the parent order `PC-S01` through `PC-S60`;
2. within a parent, order cycle coverage `A`, `B`, `C`, using `ABC` only where direct collation proves that one complete target covers all three cycle slots without a material difference; when distinct forms under one parent require both coverage shapes, place the `ABC` forms before the A/B/C forms;
3. within a cycle, keep the appointed forms in the order printed by the Missal;
4. keep every approved reading, ritual, and other option as a semantic branch inside the listed target; a branch may not become another formula key or publication target unless a later profile revision adds that exact key to a registry and adjusts the canonical count; and
5. add an occurrence component only where this profile expressly lists an occurrence whose structure changes, as with Holy Family on December 30 or Baptism on Monday.

The explicit registry order controls if these rules could otherwise admit more than one reading, especially for `PC-S25`, whose common Vigil forms precede the A/B/C Day forms.

`ABC` is a verified coverage marker, not a fourth Lectionary cycle. The manifest for a dated use still records the actual cycle `A`, `B`, or `C`, or `not applicable` when that celebration's readings are not cycle-governed. Formula keys are permanent, may not be reassigned, and are ordered by their semantic components rather than lexical sorting.

Resolve the actual Sunday cycle from the liturgical year, which turns at the First Sunday of Advent, not from January 1 alone; one civil year normally contains the end of one Sunday cycle and the beginning of the next. Never infer the independent weekday cycle `I` or `II` from the Sunday letter, and never infer the Sunday letter from civil-year parity.

The full publication slug is the parent's required stem followed by lowercase suffixes in the same order: `-year-a`, `-year-b`, or `-year-c` for `A`, `B`, or `C`; `-abc` for verified common coverage; then a literal form such as `-vigil`, `-extended-vigil`, `-night`, `-dawn`, or `-day`; then an exact listed occurrence such as `-december-30`, `-monday`, or `-sunday`. Never add a branch suffix, use anonymous `option-1`, use a generic `weekday`, or invent a Vigil suffix for an ordinary anticipated Sunday Mass. A multi-cycle compilation is a derivative publication, not a canonical formula target; it may not replace the separate keys below or use the former `-years-a-b-c` exception.

### Complete Proper-of-Time formula registry

The following is the canonical creation queue. The formula keys are written out in their required order; braces or unlisted implied combinations are not part of the registry. The Lectionary numbers are structural locators in the current *Ordo Lectionum Missae* sequence and its approved English Volume I contents, not permission to mix editions or translations.

| Parent | Required formula keys, in order | Lectionary number(s) | Count |
| --- | --- | --- | ---: |
| PC-S01 | `PC-S01-A`, `PC-S01-B`, `PC-S01-C` | 1, 2, 3 | 3 |
| PC-S02 | `PC-S02-A`, `PC-S02-B`, `PC-S02-C` | 4, 5, 6 | 3 |
| PC-S03 | `PC-S03-A`, `PC-S03-B`, `PC-S03-C` | 7, 8, 9 | 3 |
| PC-S04 | `PC-S04-A`, `PC-S04-B`, `PC-S04-C` | 10, 11, 12 | 3 |
| PC-S05 | `PC-S05-ABC-VIGIL`, `PC-S05-ABC-NIGHT`, `PC-S05-ABC-DAWN`, `PC-S05-ABC-DAY` | 13, 14, 15, 16 | 4 |
| PC-S06 | `PC-S06-A`, `PC-S06-B`, `PC-S06-C` | 17 | 3 |
| PC-S07 | `PC-S07-ABC` | 18 | 1 |
| PC-S08 | `PC-S08-ABC` | 19 | 1 |
| PC-S09 | `PC-S09-ABC-VIGIL`, `PC-S09-ABC-DAY` | 20 | 2 |
| PC-S10 | `PC-S10-A`, `PC-S10-B`, `PC-S10-C` | 21 | 3 |
| PC-S11 | `PC-S11-A`, `PC-S11-B`, `PC-S11-C` | 22, 23, 24 | 3 |
| PC-S12 | `PC-S12-A`, `PC-S12-B`, `PC-S12-C` | 25, 26, 27 | 3 |
| PC-S13 | `PC-S13-A`, `PC-S13-B`, `PC-S13-C` | 28, 29, 30 | 3 |
| PC-S14 | `PC-S14-A`, `PC-S14-B`, `PC-S14-C` | 31, 32, 33 | 3 |
| PC-S15 | `PC-S15-A`, `PC-S15-B`, `PC-S15-C` | 34, 35, 36 | 3 |
| PC-S16 | `PC-S16-A`, `PC-S16-B`, `PC-S16-C` | 37-A/38-A, 37-B/38-B, 37-C/38-C | 3 |
| PC-S17 | `PC-S17-A-VIGIL`, `PC-S17-A-DAY`, `PC-S17-B-VIGIL`, `PC-S17-B-DAY`, `PC-S17-C-VIGIL`, `PC-S17-C-DAY` | 41, 42 | 6 |
| PC-S18 | `PC-S18-A`, `PC-S18-B`, `PC-S18-C` | 43, 44, 45 | 3 |
| PC-S19 | `PC-S19-A`, `PC-S19-B`, `PC-S19-C` | 46, 47, 48 | 3 |
| PC-S20 | `PC-S20-A`, `PC-S20-B`, `PC-S20-C` | 49, 50, 51 | 3 |
| PC-S21 | `PC-S21-A`, `PC-S21-B`, `PC-S21-C` | 52, 53, 54 | 3 |
| PC-S22 | `PC-S22-A`, `PC-S22-B`, `PC-S22-C` | 55, 56, 57 | 3 |
| PC-S23 | `PC-S23-A-VIGIL`, `PC-S23-A-DAY`, `PC-S23-B-VIGIL`, `PC-S23-B-DAY`, `PC-S23-C-VIGIL`, `PC-S23-C-DAY` | 58 | 6 |
| PC-S24 | `PC-S24-A`, `PC-S24-B`, `PC-S24-C` | 59, 60, 61 | 3 |
| PC-S25 | `PC-S25-ABC-VIGIL`, `PC-S25-ABC-EXTENDED-VIGIL`, `PC-S25-A-DAY`, `PC-S25-B-DAY`, `PC-S25-C-DAY` | 62, 62a, 63 | 5 |
| PC-S26 | `PC-S26-A`, `PC-S26-B`, `PC-S26-C` | 64, 65, 66 | 3 |
| PC-S27 | `PC-S27-A`, `PC-S27-B`, `PC-S27-C` | 67, 68, 69 | 3 |
| PC-S28 | `PC-S28-A`, `PC-S28-B`, `PC-S28-C` | 70, 71, 72 | 3 |
| PC-S29 | `PC-S29-A`, `PC-S29-B`, `PC-S29-C` | 73, 74, 75 | 3 |
| PC-S30 | `PC-S30-A`, `PC-S30-B`, `PC-S30-C` | 76, 77, 78 | 3 |
| PC-S31 | `PC-S31-A`, `PC-S31-B`, `PC-S31-C` | 79, 80, 81 | 3 |
| PC-S32 | `PC-S32-A`, `PC-S32-B`, `PC-S32-C` | 82, 83, 84 | 3 |
| PC-S33 | `PC-S33-A`, `PC-S33-B`, `PC-S33-C` | 85, 86, 87 | 3 |
| PC-S34 | `PC-S34-A`, `PC-S34-B`, `PC-S34-C` | 88, 89, 90 | 3 |
| PC-S35 | `PC-S35-A`, `PC-S35-B`, `PC-S35-C` | 91, 92, 93 | 3 |
| PC-S36 | `PC-S36-A`, `PC-S36-B`, `PC-S36-C` | 94, 95, 96 | 3 |
| PC-S37 | `PC-S37-A`, `PC-S37-B`, `PC-S37-C` | 97, 98, 99 | 3 |
| PC-S38 | `PC-S38-A`, `PC-S38-B`, `PC-S38-C` | 100, 101, 102 | 3 |
| PC-S39 | `PC-S39-A`, `PC-S39-B`, `PC-S39-C` | 103, 104, 105 | 3 |
| PC-S40 | `PC-S40-A`, `PC-S40-B`, `PC-S40-C` | 106, 107, 108 | 3 |
| PC-S41 | `PC-S41-A`, `PC-S41-B`, `PC-S41-C` | 109, 110, 111 | 3 |
| PC-S42 | `PC-S42-A`, `PC-S42-B`, `PC-S42-C` | 112, 113, 114 | 3 |
| PC-S43 | `PC-S43-A`, `PC-S43-B`, `PC-S43-C` | 115, 116, 117 | 3 |
| PC-S44 | `PC-S44-A`, `PC-S44-B`, `PC-S44-C` | 118, 119, 120 | 3 |
| PC-S45 | `PC-S45-A`, `PC-S45-B`, `PC-S45-C` | 121, 122, 123 | 3 |
| PC-S46 | `PC-S46-A`, `PC-S46-B`, `PC-S46-C` | 124, 125, 126 | 3 |
| PC-S47 | `PC-S47-A`, `PC-S47-B`, `PC-S47-C` | 127, 128, 129 | 3 |
| PC-S48 | `PC-S48-A`, `PC-S48-B`, `PC-S48-C` | 130, 131, 132 | 3 |
| PC-S49 | `PC-S49-A`, `PC-S49-B`, `PC-S49-C` | 133, 134, 135 | 3 |
| PC-S50 | `PC-S50-A`, `PC-S50-B`, `PC-S50-C` | 136, 137, 138 | 3 |
| PC-S51 | `PC-S51-A`, `PC-S51-B`, `PC-S51-C` | 139, 140, 141 | 3 |
| PC-S52 | `PC-S52-A`, `PC-S52-B`, `PC-S52-C` | 142, 143, 144 | 3 |
| PC-S53 | `PC-S53-A`, `PC-S53-B`, `PC-S53-C` | 145, 146, 147 | 3 |
| PC-S54 | `PC-S54-A`, `PC-S54-B`, `PC-S54-C` | 148, 149, 150 | 3 |
| PC-S55 | `PC-S55-A`, `PC-S55-B`, `PC-S55-C` | 151, 152, 153 | 3 |
| PC-S56 | `PC-S56-A`, `PC-S56-B`, `PC-S56-C` | 154, 155, 156 | 3 |
| PC-S57 | `PC-S57-A`, `PC-S57-B`, `PC-S57-C` | 157, 158, 159 | 3 |
| PC-S58 | `PC-S58-A`, `PC-S58-B`, `PC-S58-C` | 164, 165, 166 | 3 |
| PC-S59 | `PC-S59-A`, `PC-S59-B`, `PC-S59-C` | 167, 168, 169 | 3 |
| PC-S60 | `PC-S60-A`, `PC-S60-B`, `PC-S60-C` | 160, 161, 162 | 3 |

The registry contains **184 baseline Proper-of-Time targets**: 79 for `PC-S01`–`PC-S25` and 105 for `PC-S26`–`PC-S60`. Each appointed form must cover the three A/B/C occurrence slots exactly once: three cycle-specific keys or one directly collated `ABC` key, never both. For `PC-S26`–`PC-S57`, the Lectionary number is independently checkable as `64 + 3 × (parent number − 26) + cycle offset`, where the offsets for A, B, and C are 0, 1, and 2. The count excludes the separate weekday occurrence targets, General Calendar replacements, and conditional Ritual Masses below.

The registry fixes the production kernel established by the Latin typical books. Before creating a leaf, collate the selected approved Lectionary and Missal edition. An edition-specific additional option remains a named branch. If an approved adaptation makes a listed `PC-Snn-ABC[-FORM]` target materially cycle-dependent, fail closed: do not publish that `ABC` leaf and do not invent A/B/C overlay keys under the general grammar. Record the conflict, then revise this profile or an edition-locale registry expressly established by it to list the exact replacement keys, canonical position, and adjusted count before creating any leaf. No optional branch or unregistered edition difference may promote itself into another target.

### Required branches and conditional Ritual Masses

Branches do not multiply the 184 baseline targets, but omitting them leaves a target incomplete. Every target audit must name every approved longer, shorter, alternative, or selectable path in the selected edition. The structurally important branches include:

- the common and cycle-specific reading sets for Holy Family and Baptism in Years B and C;
- the Rite of Election when celebrated within the Mass of the First Sunday of Lent, using that Sunday's Mass while recording the rite as an internal branch; the separate Election Ritual Mass is for an admitted celebration apart from that Sunday and is not another `PC-S11` target;
- the Year A initiation readings permitted in Years B and C on the Third, Fourth, and Fifth Sundays of Lent and required when the corresponding Scrutiny is celebrated, together with the prayers and prefaces bound to that reading path;
- Palm Sunday's procession, solemn-entrance, and simple-entrance modes; its cycle-specific entrance Gospel choices; the long and short Passion; and every authorized reduction of the pre-Gospel readings;
- the Easter Vigil's full and pastorally reduced Old Testament reading paths, their shorter readings and psalm alternatives, the required Exodus reading, the cycle-specific Gospel, and every applicable initiation or reception path;
- Easter Day's two second-reading choices, John 20, the current cycle's Vigil Gospel, the evening Emmaus option, and any approved baptismal-renewal path;
- the Ascension's alternative and shorter second readings in Years B and C;
- Pentecost's simple-Vigil reading selection, complete extended Vigil, Day alternatives in Years B and C, and the Sequence; and
- every edition-appointed pericope length, alternative refrain, acclamation, sequence form, preface, and prayer option in Ordinary Time and the solemnities.

The Ritual Masses for the three Scrutinies substitute distinct formularies and therefore are conditional formula targets rather than branches of the temporal Missal owner:

| Sunday parent | Conditional formula key | Required slug suffix | Canonical owner |
| --- | --- | --- | --- |
| PC-S13 | `PC-S13-ABC-FIRST-SCRUTINY` | `-abc-first-scrutiny` | First-Scrutiny Ritual Mass in the selected approved edition |
| PC-S14 | `PC-S14-ABC-SECOND-SCRUTINY` | `-abc-second-scrutiny` | Second-Scrutiny Ritual Mass in the selected approved edition |
| PC-S15 | `PC-S15-ABC-THIRD-SCRUTINY` | `-abc-third-scrutiny` | Third-Scrutiny Ritual Mass in the selected approved edition |

These three keys use the Year A initiation readings in every actual cycle, apply only when the corresponding Scrutiny is celebrated and the governing books admit the Ritual Mass, and do not become duplicate temporal-formulary owners. They raise the fixed Proper-of-Time-linked Sunday queue from 184 to **187** when conditional Sunday Ritual Masses are included. General Ritual Masses, Masses for Various Needs and Occasions, and Votive Masses admitted on particular Sundays remain resolver overlays with their own owners; they do not enter or renumber this Proper-of-Time registry.

### Occurrence resolver and Sunday replacements

The fixed order is not an annual Ordo. Before assigning any `PC-S` identity to a civil date, resolve the exact General, territorial, diocesan, religious, parish, and church calendar under the current table of precedence. Begin with the temporal identity, overlay higher-ranking celebrations, approved transfers, and any pastoral Sunday observance lawfully admitted under Universal Norms 58, and record whether the temporal Sunday is celebrated, replaced, or absent. A replaced Sunday is not transferred merely to preserve this production list, and its texts do not become part of the replacing celebration.

As of 15 July 2026, the following registry is exhaustive for universal fixed-date General Calendar celebrations, not already owned by `PC-S`, that can replace a Sunday in Christmas Time or Ordinary Time. It is not a substitute for the territorial and proper-calendar overlays required below. These celebrations have their own source ownership and permanent `PC-R` replacement IDs; they do not enter or renumber the `PC-S` sequence. Append a later qualifying General Calendar addition and retire a removed identity without reusing or renumbering any existing ID.

| ID | Required slug stem | Date | General Calendar celebration | Why it enters the resolver |
| --- | --- | --- | --- | --- |
| PC-R01 | `pc-r01-presentation-of-the-lord` | February 2 | Presentation of the Lord | Feast of the Lord |
| PC-R02 | `pc-r02-nativity-of-saint-john-the-baptist` | June 24 | Nativity of Saint John the Baptist | Solemnity in the General Calendar |
| PC-R03 | `pc-r03-saints-peter-and-paul-apostles` | June 29 | Saints Peter and Paul, Apostles | Solemnity in the General Calendar |
| PC-R04 | `pc-r04-transfiguration-of-the-lord` | August 6 | Transfiguration of the Lord | Feast of the Lord |
| PC-R05 | `pc-r05-assumption-of-the-blessed-virgin-mary` | August 15 | Assumption of the Blessed Virgin Mary | Solemnity in the General Calendar |
| PC-R06 | `pc-r06-exaltation-of-the-holy-cross` | September 14 | Exaltation of the Holy Cross | Feast of the Lord |
| PC-R07 | `pc-r07-all-saints` | November 1 | All Saints | Solemnity in the General Calendar |
| PC-R08 | `pc-r08-commemoration-of-all-the-faithful-departed` | November 2 | Commemoration of All the Faithful Departed | Assigned the precedence of General Calendar solemnities |
| PC-R09 | `pc-r09-dedication-of-the-lateran-basilica` | November 9 | Dedication of the Lateran Basilica | Feast of the Lord in the General Calendar |

`PC-R` publications use the same formula-key and full-slug grammar fixed for `PC-S`; their source owner and publishable leaf use the `general-calendar` paths fixed above. The complete replacement-parent matrix, with its one edition-dependent expansion, is:

| Parent | Required Sunday-replacement formula keys, in order | Count | Required distinctions |
| --- | --- | ---: | --- |
| PC-R01 | `PC-R01-ABC-O-SUNDAY` | 1 | Presentation on Sunday has both pre-Gospel readings; keep procession and solemn entrance as named ritual branches of the one Mass formulary. |
| PC-R02 | `PC-R02-ABC-VIGIL`, `PC-R02-ABC-DAY` | 2 | The Nativity of Saint John the Baptist has distinct Vigil and Day formularies. |
| PC-R03 | `PC-R03-ABC-VIGIL`, `PC-R03-ABC-DAY` | 2 | Saints Peter and Paul has distinct Vigil and Day formularies. |
| PC-R04 | `PC-R04-A-O-SUNDAY`, `PC-R04-B-O-SUNDAY`, `PC-R04-C-O-SUNDAY` | 3 | Transfiguration has cycle-specific Sunday Gospels and both pre-Gospel readings. |
| PC-R05 | `PC-R05-ABC-VIGIL`, `PC-R05-ABC-DAY` | 2 | Assumption has distinct Vigil and Day formularies. |
| PC-R06 | `PC-R06-ABC-O-SUNDAY` | 1 | Exaltation of the Holy Cross on Sunday has both pre-Gospel readings. |
| PC-R07 | `PC-R07-ABC` | 1 | All Saints has no appointed Vigil formulary; an anticipated Mass uses the same formulary. |
| PC-R08 | edition-resolved expansion below | 3 or 9 | All Souls has three distinct Missal formularies; the Lectionary cycle shape differs among approved editions. |
| PC-R09 | `PC-R09-ABC-O-SUNDAY` | 1 | Lateran Dedication on Sunday has both pre-Gospel readings. |

For `PC-R08`, select exactly one of these expansions after collating the approved Lectionary:

- if the complete reading inventory is invariant across the Sunday cycles: `PC-R08-ABC-FORMULARY-1`, `PC-R08-ABC-FORMULARY-2`, `PC-R08-ABC-FORMULARY-3`;
- if the edition appoints A/B/C sets: `PC-R08-A-FORMULARY-1`, `PC-R08-A-FORMULARY-2`, `PC-R08-A-FORMULARY-3`, `PC-R08-B-FORMULARY-1`, `PC-R08-B-FORMULARY-2`, `PC-R08-B-FORMULARY-3`, `PC-R08-C-FORMULARY-1`, `PC-R08-C-FORMULARY-2`, `PC-R08-C-FORMULARY-3`.

Do not collapse the three All Souls Missal formularies into anonymous prayer options, and do not explode the edition's selectable Masses-for-the-Dead readings into a Cartesian set of publication leaves. `FORMULARY-1`, `FORMULARY-2`, and `FORMULARY-3` identify the three printed formularies only; they do not prescribe the chronological order of Masses celebrated, an intention, or a pairing with a reading branch. Preserve each approved reading tuple as a semantic internal branch. The replacement queue therefore contains **16 targets** in an edition with invariant All Souls readings and **22 targets** in an edition whose All Souls readings are cycle-distinguished. For example, the current approved [Lectionary Volume I contents for England and Wales](https://www.liturgyoffice.org.uk/Resources/Lectionary/Lectionary-1-contents.pdf) uses the 22-target shape, while the current [United States All Souls directions](https://bible.usccb.org/bible/readings/110225.cfm) require a separately collated broad reading pool rather than importing that national A/B/C arrangement.

The Sunday suffix on `PC-R01`, `PC-R04`, `PC-R06`, and `PC-R09` is mandatory because these Feasts use both pre-Gospel readings when they replace a Sunday but only one, chosen as the Lectionary directs, when celebrated on a weekday. Keep that weekday rule in the shared owner; do not create `PC-R` weekday publication keys before a weekday collection is defined.

The complete **fixed registry queue** for a selected edition-locale is therefore **203 targets** in an edition with the 16-target replacement shape, or **209 targets** in an edition with the 22-target replacement shape: 184 Proper-of-Time targets, three conditional Scrutiny Ritual Masses, and the applicable replacement matrix. The six weekday fallbacks are tracked separately, bringing the total working inventory to 209 or 215 respectively; they do not change the Sunday count. Other admitted Ritual Masses and territorial, diocesan, religious, parish, and church-proper overlays are resolver-generated additions, so no finite universal total can include them in advance.

A celebration admitted to an Ordinary Time Sunday under Universal Norms 58 retains its underlying celebration identity and source owner; Sunday occurrence alone does not create a new `PC-S` or `PC-R` identity. This rule governs, for example, a lawful Sunday observance of the Most Sacred Heart of Jesus.

The resolver must also test proper solemnities, celebrations lawfully assigned or transferred to Sunday for the territory, and changes to the General Calendar after that as-of date. Audit the Dicastery's live [*Calendarium Romanum* variations index](https://www.cultodivino.va/en/formazione/pubblicazioni/libri-liturgici/aliae/calendarium-romanum.html) and subsequent Dicastery decrees before resolving a new annual calendar. The additions of [Saint Teresa of Calcutta](https://press.vatican.va/content/salastampa/en/bollettino/pubblico/2025/02/11/250211b.html) in 2025 and [Saint John Henry Newman](https://www.cultodivino.va/en/attivita/2026/inscription-of-s-john-henry-newman-in-the-general-roman-calendar.html) in 2026 are optional memorials and therefore do not alter this replacement registry. Saint Joseph, the Annunciation, and the Immaculate Conception are not standing Sunday variants: when their fixed dates meet a Sunday of Lent, Easter Time, or Advent, the seasonal Sunday prevails and the competent calendar resolves the impeded celebration. A devotional designation or special observance attached to a Sunday does not create another proper-guide identity unless the governing liturgical books actually appoint different texts or rites.

### Weekday spillover and ownership

Do not enlarge the 60-item Sunday spine into a seven-day series. "Weekday spillover" has three distinct meanings, and every guide must identify which one applies:

1. **The same celebration occurs on a weekday.** Keep one celebration owner with occurrence branches rather than duplicate Sunday and weekday guides.
2. **A Sunday or week formulary is permitted at a feria.** Reuse the canonical Missal record, but create a separate weekday liturgical instance and record the actual choice.
3. **A Sunday is absent or replaced in a particular year.** Preserve its stable identity and source work, but do not present it as celebrated on that date.

The weekday-capable parents and conditional omissions in this spine are fixed as follows:

| Parent | Sunday and weekday relationship |
| --- | --- |
| PC-S05 Nativity | Fixed on December 25; retain the Vigil form used on the evening of December 24 and the appointed Night, Dawn, and Day forms whether December 25 is Sunday or a weekday. |
| PC-S06 Holy Family | Sunday occurring from December 26 through December 31; if none occurs, December 30. The same feast formulary remains authoritative, but the December 30 occurrence uses the edition-appointed one-reading-before-the-Gospel arrangement, preserving its cycle and option distinctions; it is not a distinct Missal formulary. |
| PC-S07 Mary, Mother of God | Fixed on January 1, whether Sunday or weekday. |
| PC-S08 Second Sunday after the Nativity | Exists only on a Sunday falling January 2–5; it has no weekday fallback. |
| PC-S09 Epiphany | January 6 where retained there, or the Sunday falling January 2–8 where assigned by the competent authority. |
| PC-S10 Baptism | Ordinarily the Sunday after January 6; the following Monday when a Sunday-transferred Epiphany falls January 7 or 8. The same feast formulary remains authoritative, but the Monday occurrence uses the appointed one-reading-before-the-Gospel arrangement. Week I then begins Tuesday; record any permission actually used to join the displaced Monday readings to Tuesday's readings. |
| PC-S23 Ascension | The fortieth day of Easter or the Seventh Sunday of Easter, according to the competent calendar. |
| PC-S24 Seventh Sunday of Easter | Preserved in the inventory but replaced, without weekday fallback, where Ascension is assigned to that Sunday. |
| PC-S25 Pentecost | Sunday celebration; where Monday or Tuesday after Pentecost is a day on which the faithful are obliged or accustomed to attend Mass, the Missal permits the Pentecost Mass to be repeated or a Mass of the Holy Spirit to be used. This is conditional reuse, not transfer or a new identity. |
| PC-S59 Body and Blood of Christ | Thursday after Trinity Sunday or the following Sunday, according to the competent calendar. |

Only two Proper-of-Time parents require separate, prebuilt weekday fallback targets because the fallback changes the Liturgy of the Word. Their six keys follow the Sunday registry but do not count as Sunday formulas:

| Order | Formula key | Required slug suffix | Weekday structure |
| ---: | --- | --- | --- |
| 1 | `PC-S06-A-O-DECEMBER-30` | `-year-a-december-30` | One reading before the Gospel; preserve the Year A path. |
| 2 | `PC-S06-B-O-DECEMBER-30` | `-year-b-december-30` | One reading before the Gospel; preserve the common-versus-Year-B option. |
| 3 | `PC-S06-C-O-DECEMBER-30` | `-year-c-december-30` | One reading before the Gospel; preserve the common-versus-Year-C option. |
| 4 | `PC-S10-A-O-MONDAY` | `-year-a-monday` | One reading before the Gospel, chosen as the approved Lectionary directs. |
| 5 | `PC-S10-B-O-MONDAY` | `-year-b-monday` | One reading before the Gospel; preserve the common-versus-Year-B option. |
| 6 | `PC-S10-C-O-MONDAY` | `-year-c-monday` | One reading before the Gospel; preserve the common-versus-Year-C option. |

The temporal production queue is therefore **190 targets** when the 184 Sunday formulas and these six deterministic weekday fallbacks are counted together, or **193** when the three conditional Scrutiny formularies are also included. Nativity on a weekday, Mary on January 1, Epiphany on January 6, Ascension on Thursday, and Corpus Christi on Thursday reuse their existing formula targets because the day of occurrence does not itself change the treated texts. Pentecost on Monday or Tuesday is a conditional reuse edge, not a prebuilt fallback target.

The fixed `temporal/shared/ordinary-time/weeks/01` through `weeks/34` layer owns the Ordinary Time Missal formularies and, when warranted, supplies separately manifested weekday companions:

- Week I has no numbered Sunday consumer; its separate formulary is available for ferial use and cross-references `PC-S10`. Never invent a First Sunday in Ordinary Time.
- Weeks II–XXXIII are owned by the week layer and consumed by `PC-S26`–`PC-S57`. On an Ordinary Time weekday, use of that formulary or of orations from another Sunday is a permitted selection, not an assertion that the Sunday celebration continues unchanged.
- The ordinary Week XXXIV formulary has no numbered Sunday consumer and is available for ferial use; the Sunday of Week XXXIV is `PC-S60` Christ the King, whose formulary is distinct.
- The Roman Missal's *Tempus per annum* rubric 3(b) permits selection of any of the 34 Ordinary Time formularies—their antiphons and orations—on an eligible Ordinary Time feria; GIRM 363 separately permits orations from the preceding or another Ordinary Time Sunday. Chronological proximity does not make one of them automatically appointed.
- The annual calendar determines the week resumed after Pentecost. When only thirty-three weeks occur, the first week that would otherwise resume is omitted so that the final eschatological weeks remain in place. A Sunday displaced by Pentecost, Trinity, Corpus Christi, or another celebration does not erase its numbered weekday week.
- Weekday readings remain the independent Lectionary cycle `I` or `II`, including their semi-continuous sequence. They are not imported from Sunday `A`, `B`, or `C`; an interruption and any permitted joining of omitted passages must be recorded in the resolved weekday instance.
- Ferial use of an Ordinary Time formulary does not import Sunday readings, the Gloria, Creed, or Sunday Preface. Apply the Missal's Ordinary Time rubrics 4–6: retain the weekday Lectionary, omit the Gloria and Creed, use the applicable weekday Preface rule, and evaluate the Communion-antiphon option against the actual Gospel.
- Seasonal weekdays retain their own appointed formularies and reading structures. Do not reuse a Sunday merely by analogy where the Missal provides proper seasonal weekday orations.

Rogation and Ember days are weekday overlays under Universal Norms 45–47: the conference sets their time and manner, and on each such day the Mass for Various Needs and Occasions best suited to the intentions is used. They neither extend a Sunday proper nor enter the `PC-S` spine.

The Ordinary Time week layer owns each Missal formulary once and lets Sunday and weekday consumers import or reference it; do not duplicate its protected wording in three Sunday-cycle records or again in weekday consumers. Reserve `PC-W` for a future full weekday collection that keeps seasonal, fixed-date, and Ordinary Time material outside the immutable `PC-S` numbering; do not assign a `PC-W` ID or create a `PC-W` slug until this profile adds its complete inventory, slug grammar, and layout. Where Monday or Tuesday after Pentecost is a day on which the faithful are obliged or accustomed to attend Mass, the exceptional permission to repeat the Pentecost Mass or use a Mass of the Holy Spirit remains valid under the Holy See's [2018 notification concerning the Memorial of the Blessed Virgin Mary, Mother of the Church](https://press.vatican.va/content/salastampa/en/bollettino/pubblico/2018/03/27/180327b.html); record it as a conditional reuse edge on `PC-S25`, not as a new Sunday or weekday identity. The Monday memorial remains obligatory and is preferred all else being equal; when it is celebrated, its proper readings replace the Ordinary Time weekday readings. Any exceptional selection must follow the circumstances stated in the Missal, GIRM 376, and the competent calendar.

This order and policy were checked on 15 July 2026 against Paul VI's [*Mysterii Paschalis*](https://www.vatican.va/content/paul-vi/la/motu_proprio/documents/hf_p-vi_motu-proprio_19690214_mysterii-paschalis.html), the bishops' approved English [Universal Norms on the Liturgical Year and the Calendar](https://www.liturgyoffice.org.uk/Resources/GIRM/Documents/GNLY.pdf), the official [Roman Missal, Third Edition contents](https://www.liturgyoffice.org.uk/Missal/Information/RM3-contents.pdf) and [Ordinary Time directions](https://www.liturgyoffice.org.uk/Missal/Music/Antiphonary.pdf), the approved [Lectionary Volume I contents](https://www.liturgyoffice.org.uk/Resources/Lectionary/Lectionary-1-contents.pdf), the [General Introduction to the Lectionary](https://www.liturgyoffice.org/Resources/GIRM/Documents/Lectionary.pdf), and the bishops' official structural matrices for [Christmas](https://www.liturgyoffice.org.uk/Calendar/Sunday/ChristmasSunday.shtml), [Lent and Palm Sunday](https://www.liturgyoffice.org.uk/Calendar/Sunday/LentSunday.shtml), the [Paschal Triduum](https://www.liturgyoffice.org.uk/Calendar/Sunday/Triduum.shtml), [Easter Time](https://www.liturgyoffice.org.uk/Calendar/Sunday/EasterSunday.shtml), and [General Calendar Feasts of the Lord](https://www.liturgyoffice.org.uk/Calendar/Sunday/Feasts.shtml). It was also checked against the *Missale Romanum*, editio typica tertia, reimpressio emendata 2008, *Tempus per annum*, introductory rubrics 1–6 and formularies for Weeks I–XXXIV, especially pp. 450–484, the Dicastery's live [calendar-variations index](https://www.cultodivino.va/en/formazione/pubblicazioni/libri-liturgici/aliae/calendarium-romanum.html), and the Holy See's [General Instruction of the Roman Missal](https://www.vatican.va/roman_curia/congregations/ccdds/documents/rc_con_ccdds_doc_20030317_ordinamento-messale_en.html), especially nos. 353–363 and 376. The exact typical and vernacular editions, later decrees, and competent annual calendar still govern each publication.

## Establish the liturgical instance first

Before research or drafting, create a manifest that identifies the texts actually being studied. Record at least:

- the permanent parent ID and formula key when assigned, or the identity fixed by the governing ritual or local inventory; its `A`, `B`, `C`, or verified `ABC` production coverage when applicable; its canonical Missal or Ritual Mass owner; and every selected named branch;
- the Latin typical edition of the Roman Missal and, when applicable, its printing or reprint;
- the vernacular Missal edition, language, episcopal conference or territory, publisher, and approval or implementation date;
- the Lectionary edition and volume, language, territory, and edition-specific reading references;
- the governing calendar: General Roman Calendar and every national, diocesan, religious, parish, or other proper calendar that affects the celebration;
- the as-of date for rubrics, calendar law, approved adaptations, and later decrees, together with any known pending change material to the instance;
- the celebration, rank, ritual or pastoral context, and civil date when a date is needed to resolve precedence;
- the actual Sunday cycle (`A`, `B`, or `C`) for a dated occurrence, or `not applicable` when the instance has no Sunday-cycle path; the weekday cycle (`I` or `II`), or `not applicable` when the instance has no weekday readings; and any special cycle, appointed form, branch, or occurrence discriminator;
- every permitted option selected, including alternative readings, prayers, prefaces, ritual forms, formulary sources, and the Eucharistic Prayer when its selection activates a proper insert or otherwise changes a treated text; and
- unresolved choices that would produce materially different documents.

Do not combine texts from different editions, territories, cycles, calendars, or option paths into a synthetic formulary. If several legitimate paths deserve treatment, identify each as a variant and show which claims belong to which path. A date alone never identifies a liturgical instance adequately.

## Required guide and source-record schema

A proper exposition is an advanced lay reader's preparation companion for use beside the approved Missal and Lectionary. It is not a substitute liturgical book, a worship aid, an annual Ordo, or a record of what happened at an unspecified parish Mass. Research studies the complete appointed texts and every branch registered or named by the governing inventory; the PDF quotes only the citations, incipits, and clauses needed for analysis unless the rights record permits more.

Every publishable leaf has this minimum tracked layout:

```text
<document-slug>/
  main.tex
  generation-metadata.tex
  instance/
    manifest.md
  propers/
    verified.md
  research/
    scope.md
```

The canonical Missal or Ritual Mass owner---a shared owner for `PC-S` and `PC-R`, or the owner fixed by another governing inventory---keeps its own `propers/verified.md`. The owner and leaf records have different jobs:

- the **formulary-owner record** verifies the reusable Missal or Ritual Mass formulary, its rubrics, source edition, provenance, rights status, variants, and unresolved discrepancies once; and
- the **leaf record** verifies the target's composition: assigned formula key or governing identity, owner link, Lectionary path, ordered element inventory, branches, chant layer, source locators, and the status of every treated element without duplicating protected owner wording.

`instance/manifest.md` is the authoritative formula-identity and resolution record. `research/scope.md` preserves the operational scholarship audit displaced from the PDF: biblical and liturgical context, historical judgments, direct and illuminating reception, governing jurisdiction and as-of date, languages and corpora searched, material disagreement, negative results, rejected or unresolved leads, branch-specific limitations, source roles, rights boundaries, review performed, and review outstanding. It is not a diary or chain-of-thought record.

Source work uses the manifest and verified records defined above. A focused source extract may be retained only when its redistribution is lawful, its audit purpose cannot be met by edition and locator data, and the rights basis is recorded. Never make a complete modern vernacular Missal, Lectionary, ritual book, chant book, or bulk transcription a repository dependency.

### Required fields in the verified records

The formulary owner's `propers/verified.md` records at least:

- the exact book title, Latin typical edition and printing or reprint, approved vernacular edition when used, language, territory, promulgating or approving authority, publisher or rights holder, year, and implementation date;
- the printed formulary heading, rank or ritual use, page or stable locator, access or collation date, and the controlling rubrics;
- every Missal or Ritual Mass element actually appointed by that formulary, including authorized alternatives, proper prefaces, proper Eucharistic Prayer inserts, prayers over the people, solemn blessings, and special dismissals where present;
- an incipit, biblical citation, or other minimal identifier for each element; its source, liturgical function, and verification result; and
- witnesses consulted, rights or licensing status, material edition differences, unresolved discrepancies, and the final verification date.

The leaf `propers/verified.md` records at least:

- the permanent formula key, full slug, and parent when assigned, or the identity fixed by the governing ritual or local inventory; the canonical owner, edition-locale, Lectionary number or other locator, and every book supplying part of the target;
- the complete ordered element inventory and branch matrix defined below;
- the exact citations and pericope boundaries for every reading, psalm, acclamation, and scriptural ritual text, including longer and shorter forms, alternatives, and omitted verses;
- the source and status of each chant or other musical text path, identified by its liturgical placement and distinguishing a Missal antiphon from the *Graduale Romanum*, *Graduale Simplex*, another approved collection, and a local selection;
- the resolved choice, if the leaf represents a dated or otherwise resolved occurrence, without erasing the target's unselected authorized branches; and
- verification status, source locators, rights disposition, unresolved choices, discrepancies, and the final collation date.

## Required reader-facing exposition order

Every postconciliar proper exposition uses this native macro-order:

1. title and a compact identity, use, rights, and review-status note;
2. `Textual Variable Parts`, a documentary two-column inventory in actual liturgical order;
3. `Study Guide: Scripture and Liturgical Context`;
4. `Study Guide: Liturgical Movement and Textual Relationships`;
5. `Study Guide: Theological and Spiritual Synthesis`;
6. `Study Guide: Commentary on the Texts`;
7. optional `Study Guide: Further Interpretive Possibilities`, with the required editorial or AI disclosure;
8. optional `Reception and Cultural Echoes`;
9. any required `Sacramental Appendix`;
10. a fresh-page `Appendix: Liturgical Resolution`, containing `Liturgical Instance`, `Branch Resolution` for reader-relevant textual or ritual branches, and only the occurrence or transfer material needed to identify the instance or interpret those branches;
11. `References`, ending with `Search Scope and Limitations`; and
12. terminal `Generation Metadata`, imported from `generation-metadata.tex`.

The title, compact note, and `Textual Variable Parts` begin on page 1 and use as much space as complete, readable documentation requires. Taken together, the title and note identify the exact edition-locale, formula or governing identity, occurrence when resolved, use boundary, rights boundary, and material review limits. The Study Guide and `Appendix: Liturgical Resolution` each begin on a fresh page; additional internal page breaks follow readability and the actual scale of the celebration. Palm Sunday, the Easter Vigil, the extended Pentecost Vigil, Ritual Masses, and other textually extensive targets expand rather than compress or omit material. Study Guide prose uses the shared `deepstudy` size or an exact readable equivalent. Visual distinctions remain intelligible in pure black and white, with no color-dependent distinction or gray fill.

`Reception and Cultural Echoes` is included only for verified reception of an appointed text or distinctive wording and never to meet a quota. When Mass incorporates or directly targets a non-Eucharistic sacrament, import the repository's canonical one-page sacramental summary before the liturgical-resolution appendix; research must use the full sacramental reference and its sources rather than treating that appendix as sufficient evidence.

`References` is the final scholarly section and contains only sources actually used. Its terminal `Search Scope and Limitations` subsection gives a compact reader-facing account of text verification, principal direct and illuminating sources, and branch or rights limits that affect the argument. It points to the leaf's `instance/manifest.md`, the leaf's composition audit at `propers/verified.md`, the canonical formulary owner's `propers/verified.md`, and the leaf's `research/scope.md`. `Generation Metadata` follows it and no expository prose follows the metadata.

### Structural rationale

The reader-facing order has three deliberate layers: a documentary record of the textual variable parts, a study guide grounded in those texts, and a technical resolution appendix. The opening inventory answers which texts the celebration appoints or concretely selects. The Study Guide explains scriptural context, liturgical relationships, theology, spirituality, and the individual texts. The appendix identifies the celebration and records the authority and resolution of branches that a reader needs to understand the text inventory or study. Complete source, status, and unresolved-choice data remain in the tracked audits.

Within `Textual Variable Parts`, one row represents one text-bearing liturgical unit. Closed alternatives belonging to that unit remain together in its `Text / citation` cell, while exact semantic branch IDs, authority, controlled status, and resolution remain in `Branch Resolution` and the tracked audits. Visible phase dividers follow the actual rite and omit empty phases. An ordinary Sunday may use `Introductory Rites`, `Liturgy of the Word`, `Liturgy of the Eucharist`, and `Concluding Rites` when a distinctive textual variable is inventoried there; Palm Sunday, Vigils, Ritual Masses, and other special forms use their own modules. This structure was re-evaluated across every existing postconciliar proper guide on 16 July 2026.

## Document the textual variable parts

Build the textual record from the ordered text-bearing units appointed or lawfully selected for the identified celebration. Collate every governing book and preserve each source layer in the audit.

### Liturgical Instance appendix panel

The first subsection of `Appendix: Liturgical Resolution` gives:

- the celebration, rank, season, liturgical color, parent ID and permanent formula key when assigned, or the governing ritual or local identity, and the full form or occurrence name;
- the selected edition-locale, governing calendar and territory, Missal or Ritual Mass owner, Lectionary edition and number, and any additional ritual or chant book actually used;
- the production coverage (`A`, `B`, `C`, or verified `ABC`), the actual Sunday cycle for a resolved occurrence, and the independent weekday cycle when applicable;
- the canonical formulary owner and the relationship between its reusable text record and the leaf's dated or cycle-specific composition; and
- the textual branches treated by the guide and, for a resolved occurrence, the selections that can be established from the evidence.

The tracked manifest and verified audit record ordinary-unit status, ritual substitutions, open selections, and every applicable branch. The reader-facing `Liturgical Instance` includes such information only when it is needed to identify the form or interpret a textual variable treated in the guide.

The manifest and verified audit always record the applicable Preface rule and any Eucharistic Prayer choice that activates a proper insert. `Textual Variable Parts` includes a Preface or Eucharistic Prayer insert only when the text is proper, narrowly appointed, or concretely selected in a resolved instance. The reader appendix states a Preface or Eucharistic Prayer dependency only when it changes an inventoried text or materially limits the Study Guide.

Model prayer-specific dependencies as coupled branches in the audits. On an Ordinary Time Sunday, the Missal directs a Sunday-in-Ordinary-Time Preface unless the selected Eucharistic Prayer carries its own Preface (*Tempus per annum*, rubric 5). Eucharistic Prayer IV is selected together with its own inseparable Preface under GIRM 365(d); a celebration whose formulary appoints a proper Preface follows the corresponding restriction. Apply the governing rubric to every Eucharistic Prayer whose Preface or insert constrains the selection.

### Textual Variable Parts

The inventory has a variable number of rows and exactly two conceptual columns:

| Column | Required content |
| --- | --- |
| `Textual unit` | One text-bearing variable unit in its actual liturgical position. |
| `Text / citation` | Incipit or minimum necessary clause for a prayer or antiphon; exact biblical citation and pericope boundary for a Lectionary element; all closed alternatives for the same unit, labeled in ordinary language within the one cell. |

Use one row per actual unit, not one row per branch. Put long and short forms of one Gospel in the same Gospel row and the same `Text / citation` column. Apply the same rule to alternative psalm responses, sequence forms, Prefaces, Communion antiphons, and alternative forms of one appointed concluding text. Use ordinary-language labels such as `Long`, `Short`, `A`, and `B`; keep the exact semantic branch IDs in the appendix and tracked audits. Genuinely repeated units in a special form---for example, the Easter Vigil's several reading--psalm--collect modules---remain separate modules, and a complex cell may continue for legibility rather than become an unreadable list.

Include every text appointed by the governing books and every concretely documented local selection. Consolidate closed alternatives in their textual-unit row. Record every unresolved selection class, omission, and applicability result in the tracked audits; include one in the resolution appendix only when it is needed to identify the instance or interpret the textual record or Study Guide. A documented local selection becomes a row when its actual source and selected content are known.

Group the rows with visible, untabulated phase labels following the actual liturgical form. Omit an empty phase. These dividers aid scanning but do not replace the unit labels, change the rite's hierarchy, or imply that every form has the ordinary Sunday's phases.

Assign every inventoried textual unit an unambiguous short cue for later navigation. Text-focused subsection headings and substantial proposal leads end with quiet italic parenthetical cues in actual liturgical order, adding an ordinary-language alternative label where needed. Cues distinguish a Missal antiphon from a concretely selected chant and a chant at the Preparation of the Gifts from the Prayer over the Offerings. Do not use raw branch IDs, numeric badges, decorative icons, or a cue whose meaning changes between guides.

Use the shared postconciliar textual-variable-parts environment, with the two columns above, actual-form phase dividers, one textual unit per row, consolidated closed alternatives, and readable multipage behavior for complex formulas.

Use these controlled statuses throughout the tracked source audit and for every branch included in `Branch Resolution`, translating them into ordinary prose where the appendix requires explanation: `required`, `appointed alternative`, `conditional`, `permitted`, `ritual substitution`, `locally selected`, `omitted`, and `not applicable`. The textual inventory carries only the two fields above. Do not collapse omission into inapplicability, call an option required, call a permitted substitution appointed, or describe an unselected alternative as proclaimed, sung, or prayed.

For a normal Sunday or solemnity, inspect these possible text-bearing units in actual liturgical order. The selected books and the identified form determine which ones appear:

1. texts appointed for a distinct entrance form, blessing, or procession;
2. the applicable Missal Entrance Antiphon and any concretely appointed or selected approved entrance chant;
3. Collect;
4. First Reading;
5. Responsorial Psalm, including its response and appointed verses or authorized alternative;
6. Second Reading;
7. Sequence;
8. Gospel acclamation or Lenten verse;
9. Gospel;
10. any concretely appointed or selected approved chant at the Preparation of the Gifts;
11. Prayer over the Offerings;
12. proper, narrowly appointed, or concretely selected Preface;
13. proper Eucharistic Prayer insert;
14. the applicable Missal Communion Antiphon and any concretely appointed or selected approved Communion chant;
15. Prayer after Communion; and
16. appointed Prayer over the People, solemn blessing, special dismissal, or other concluding text.

Alternatives belonging to one unit normally share one row. On Sundays and solemnities, the usual Liturgy of the Word orders the readings, Responsorial Psalm, Sequence where appointed, Gospel acclamation, and Gospel according to the selected Lectionary; special vigils and rituals follow their own repeated or substituted textual units.

At the Preparation of the Gifts, record the Prayer over the Offerings. When an identified approved chant source appoints a chant, or a resolved instance identifies the chant actually selected, record that text in its liturgical position and identify its source. At the Entrance and Communion, record the applicable Missal antiphon or closed alternatives and any concretely appointed or selected approved chant. Keep unresolved selection classes in the tracked audits and include them in the reader appendix only when they materially identify or limit the guide's treatment.

Identify every chant path by book, edition, liturgical placement, and status. Classify hymns, songs, commentary, and pastoral additions as local material unless a governing liturgical source appoints them.

### Branch Resolution and resolved instances

Every target with a closed textual alternative, or a ritual branch needed to understand an inventoried text, has a reader-facing `Branch Resolution` subsection after `Liturgical Instance`. It uses:

| Branch ID | Authority and trigger | Status | Units affected | Resolution |
| --- | --- | --- | --- | --- |

Branch IDs are stable semantic names such as `short-passion`, `procession`, `year-a-scrutiny-readings`, or `evening-emmaus-gospel`, never anonymous `option-1`. A branch names the choice authorized by the book; it does not create another formula key unless the registry expressly says so.

Use each branch ID unchanged in `Branch Resolution`, `instance/manifest.md`, and leaf `propers/verified.md`. The textual inventory uses ordinary-language labels within its one-unit row rather than exposing raw branch IDs. Do not introduce aliases or abbreviated IDs in the records; carry the readable element name and explanation in the neighboring fields instead.

A territorial norm that permits selection from an open or extensive approved musical repertory is one source-class branch in the tracked audits, not one branch per possible song. Name and analyze a particular hymn, antiphon, or chant only when an approved book appoints it or a resolved instance actually selects it.

The tracked manifest and verified audit document one registered formula target and every legitimate named branch. The reader appendix presents the subset needed to interpret its textual record and Study Guide. A dated or otherwise resolved instance records which branches were actually selected. Unselected closed alternatives remain documented in the one-unit row, appendix, and audits and may receive branch-specific commentary. Mutually exclusive alternatives may not be narrated as concurrent parts of one celebration; unresolved choices are treated separately or limit claims that depend on them.

## Study Guide: Scripture and Liturgical Context

This section inventories every distinct directly appointed biblical passage and book-identified scriptural adaptation used by the target: Lectionary readings and Responsorial Psalms; biblical or book-identified scriptural Gospel acclamations and verses; and scriptural Missal antiphons or ritual texts. Include an explicitly cited adaptation marked `Cf.` or an equivalent source marker, but label it as adaptation or allusion rather than verbatim quotation. A nonbiblical acclamation or composed liturgical text still belongs in the textual record and commentary but not in this historical Scripture inventory. Do not promote loose echoes in composed orations to direct biblical appointments.

Order dossiers by the Catholic canonical order of the biblical books and then by chapter and verse, not by Mass order. Consolidate a repeated passage into one dossier while listing every element and branch in which it appears. Use these exact conceptual columns:

| `Textual unit / alternative` | `Citation` | `Location` | `Date` |
| --- | --- | --- | --- |

Each dossier begins with a composition row, followed by a full-width explanatory row that distinguishes inherited attribution from historical judgment and states, as the evidence permits, authorship, composition date and place, first audience, compositional horizon, and place in salvation history. For a Gospel or any other narrative whose narrated event is materially distinct from the text's composition, insert a separate `Narrated event` row with its locating citations, event location, and date before the explanation. Keep writer, audience, and event locations distinct; give present-day equivalents for secure ancient places; preserve disputes and unknowns.

The table gives citations and historical orientation, not copyrighted biblical text. It begins on a fresh page but has no fixed one-page limit. The Easter Vigil and other scripturally extensive targets expand as needed rather than omit readings, compress alternatives, or make the table unreadable. Full historical disputes and source-role details remain in `research/scope.md`.

## Relationship discipline and exposition

Do not presume that every postconciliar element was composed or selected as one thematic whole. Before drafting, classify every cross-element relation under one of these evidence labels:

- `officially correlated`: the Lectionary or another governing liturgical book states or structurally establishes the relationship;
- `responsorial`: the Responsorial Psalm is appointed after and normally corresponds to the First Reading;
- `acclamatory`: the Alleluia or other Gospel acclamation welcomes the Lord about to speak in the Gospel and uses the verse appointed or selected under the governing book;
- `semi-continuous`: a reading belongs to an ordered course whose primary relation is to its biblical sequence rather than to every other text of the day;
- `seasonal or ritual`: the relationship arises from the season, celebration, sacrament, or ritual action;
- `textual observation`: exact shared wording, image, citation, or rhetorical structure visible in the appointed texts;
- `documented reception`: an identified patristic, saintly, magisterial, liturgical, or scholarly witness makes the relationship;
- `source-grounded synthesis`: the project joins checked elements without claiming historical design or inherited authority; or
- `editorial or AI proposal`: a plausible original extension reserved for `Study Guide: Further Interpretive Possibilities`.

The General Introduction to the Lectionary controls the baseline. In Ordinary Time the Old Testament reading is normally selected in relation to the Gospel, while the apostolic and Gospel readings proceed in semi-continuous series; it expressly rejects imposing an organic thematic harmony on Sunday readings merely to aid homiletic instruction. The Second Reading must still be studied fully, but it may remain an independent apostolic strand. Orations and antiphons shared across A/B/C likewise may not be described as historically designed for one cycle's readings without direct evidence. In Advent, Lent, Easter, ritual celebrations, and other specially arranged forms, report only the degree and kind of harmony the governing books actually establish.

### Study Guide: Liturgical Movement and Textual Relationships

This section is the source-grounded architectural synthesis. Begin with a one- or two-sentence governing account and one scan-first orienting form of no more than four primary stages. For an ordinary formula, use three to five relationship-titled units keyed to that account; a complex vigil or ritual may use the minimum additional units required by its actual repeated structure. Follow the celebration's real movement---for example, gathering or a special entrance rite, proclamation and response, preparation and thanksgiving, Communion, and sending---and its actual text-bearing structure.

Every inventoried text contributes to a functional grouping or is explicitly identified as an independent, semi-continuous, or optional strand. A thesis may be plural rather than force false unity. Decisive witnesses and guardrails are visibly labeled, no prose paragraph exceeds 120 words, and no unstructured prose run exceeds two paragraphs. Original AI proposals do not appear here. Completeness and readable proportion control the section's length.

### Study Guide: Theological and Spiritual Synthesis

Draw only dimensions supported by the appointed texts and verified reception. Select categories responsive to the celebration---such as Christological, ecclesial, sacramental, moral, pastoral, or eschatological dimensions---without requiring a fixed number or type. Preserve branch-specific limits and material alternatives. If the evidence supports a connection only within one text or branch, state that narrower anchor rather than converting it into a whole-formulary thesis.

### Study Guide: Commentary on the Texts

This section supplies the evidence and qualifications behind the synthesis. Study every inventoried prayer, antiphon, reading, psalm, acclamation, sequence, proper Preface, insert, blessing, dismissal, or other variable text in full. Give biblical exegesis, literary and liturgical context, direct patristic or saintly reception where verified, lexical work when it clarifies rather than ornaments, doctrinal illumination, genuine disagreement, branch-specific consequences, and explicit limits. Distinguish direct commentary from later doctrinal illumination, an official relationship from editorial synthesis, and a selected path from an unselected alternative.

Organize by the formula's strongest evidenced relationships and ritual movement rather than mechanically repeating inventory rows. Each substantial claim has one fullest home. Do not duplicate the historical dossier or the overview paragraph for paragraph, and do not force an independent semi-continuous reading into another unit merely to create a whole-formulary thesis.

### Study Guide: Further Interpretive Possibilities

Open with one global notice that the section contains original editorial or AI-generated possibilities attributed to none of the cited authorities and claims no historical compositional intent. Place every original analogy, typological extension, compositional inference, or unsourced cross-element connection here. Each substantial proposal identifies its appointed anchors, explains its theological or pastoral fruit, and states material limits or serious alternatives. Select proposals for anchoring, novelty, coherence, plausibility, and usefulness rather than a prescribed number or length.

## Required structural modules

The macro-order above is stable; the textual inventory, visible phase groups, Study Guide, and liturgical-resolution appendix expand to match the actual form. At minimum, apply these modules to the registered targets already fixed in this profile:

| Target or form | Required interior structure |
| --- | --- |
| Ordinary Sunday or solemnity | Textual groups for the Introductory Rites, Liturgy of the Word with readings, psalm, Sequence where appointed, acclamation, and Gospel, Liturgy of the Eucharist with orations, proper or selected Preface or insert where inventoried, and the Communion texts, plus Concluding Rites when a distinctive text is appointed; reader-relevant appendix branch blocks. |
| Palm Sunday | Separate `Commemoration of the Lord's Entrance` and `Mass` blocks; procession, solemn-entrance, and simple-entrance branches; cycle-specific entrance Gospel; the status of the ordinary Introductory Rites; and long or short Passion and any admitted pre-Gospel reduction without ever treating the Passion as optional. |
| Easter Vigil | Four blocks for the Service of Light, Liturgy of the Word, Baptismal Liturgy, and Liturgy of the Eucharist; each Old Testament reading--psalm--collect module; the lawful reduction rule and required Exodus module; Romans, cycle Gospel, initiation or reception paths, and proper Eucharistic or dismissal material. |
| Easter Day | Alternative second readings, required Sequence, Day Gospel and admitted Vigil-Gospel or evening-Emmaus paths, plus the Missal-authorized baptismal-renewal branch and any territorial adaptation. |
| Pentecost Vigil | Separate simple and extended forms as the registry requires; the simple form's Old Testament-reading selection and the extended form's repeated reading--psalm--collect modules must not be collapsed. |
| Pentecost Day | The required Sequence and every edition-appointed cycle-dependent second-reading or Gospel alternative. |
| Scrutiny target | The selected Ritual Mass owner, required Year A initiation readings, proper prayers and preface, and the post-homily intercessions, exorcism, and dismissal or retention rules supplied by the initiation rite. It is not merely a Sunday-reading branch. |
| Feast replacing Sunday or weekday fallback | Preserve the same Missal owner while resolving the Sunday or weekday Lectionary structure independently, including the number of pre-Gospel readings and every cycle-specific alternative. |
| Other Ritual Mass | Follow the actual sacramental or sacramental-unit order and include every ritual text that changes the Mass without forcing the normal Sunday row order. Add the sacramental appendix when the rite confers or directly targets a non-Eucharistic sacrament. |

This table describes exposition modules, not new formula keys. The registry and selected approved books still decide whether a form is a separate target, an internal branch, a conditional Ritual Mass, or a resolved occurrence.

## Research and generation workflow

Use this sequence for every new or substantially revised proper exposition:

1. **Resolve identity and authority.** Complete `instance/manifest.md`; resolve the formula key and parent when assigned, or the identity fixed by the governing ritual or local inventory, together with the owner, editions, territory, calendar, cycle, form, occurrence, ritual context, and branch universe before collecting texts.
2. **Collate the complete formula.** Verify every appointed or permitted element against the identified books; complete the formulary-owner and leaf `propers/verified.md` records; preserve exact pericope boundaries, rubrics, options, omissions, source roles, rights, and discrepancies.
3. **Study Scripture historically.** Read every selected passage in its complete literary context; prepare the canonical-order dossiers; distinguish composition, audience, and narrated event; preserve traditional and modern judgments without silent harmonization.
4. **Study reception and liturgical function.** Seek direct patristic or saintly exegesis first, then accurately labeled doctrinal or liturgical illumination. Study each oration, antiphon, chant, preface, insert, and ritual action in full. Record material negative results rather than inventing a witness.
5. **Classify relationships.** Apply the evidence labels above, the Lectionary's harmony and semi-continuity principles, and the branch matrix. Do not infer historical compositional unity from same-day co-occurrence.
6. **Classify claims.** Keep verified text, documented history, documented reception, source-grounded synthesis, and editorial or AI proposal visibly distinct. Resolve contradictions and branch scope before drafting reader-facing prose.
7. **Draft from depth to compression.** Write `Study Guide: Commentary on the Texts` first; then derive the liturgical-relational and theological syntheses and the compact scope panel. Populate `Textual Variable Parts` only from the verified text audit; it contains no synthesized claim. Consolidate each unit's closed alternatives without erasing their distinctions, and place source, status, and resolution mechanics in the appendix and tracked records. Do not pad to a page target or use the synthesis to introduce evidence absent from the commentary.
8. **Assemble and verify.** Apply the required macro-order, textual phase groups, appendix placement, and fresh-page boundaries; refresh structured metadata; build for enough passes to settle references and contents; inspect the log; and visually inspect every page, textual inventory, and branch table before installing a PDF.

Study each text's documented origin and reception only where verified. The governing postconciliar books determine the guide's inventory and organization; historical-development claims do not supply its architecture. Rubrical permission is not evidence of pastoral preference, and a permitted option is not necessarily appointed in every celebration.

## Structural verification basis

This schema was checked on 15 July 2026 against the Holy See's [General Instruction of the Roman Missal](https://www.vatican.va/roman_curia/congregations/ccdds/documents/rc_con_ccdds_doc_20030317_ordinamento-messale_en.html), especially nos. 46--90 and 352--367; the approved [General Introduction to the Lectionary](https://www.liturgyoffice.org.uk/Resources/GIRM/Documents/Lectionary.pdf), especially nos. 65--69, 78--91, and 93--110; the official [Roman Missal, Third Edition contents](https://www.liturgyoffice.org.uk/Missal/Information/RM3-contents.pdf); and the bishops' official [Missal Antiphonary](https://www.liturgyoffice.org.uk/Missal/Music/Antiphonary.pdf). Those sources establish the Liturgy of the Word and Liturgy of the Eucharist as the two principal parts forming one act of worship, together with the Introductory and Concluding Rites; the positions and functions of the variable texts; the source and selection rules for music at Entrance, the Preparation of the Gifts, and Communion; Sunday and weekday reading structures; longer, shorter, and alternative readings; the independent A/B/C and I/II courses; and the Lectionary's distinct principles of harmony and semi-continuous reading.

The special-form modules were also checked against the bishops' official matrices for [Christmas](https://www.liturgyoffice.org.uk/Calendar/Sunday/ChristmasSunday.shtml), [Lent and Palm Sunday](https://www.liturgyoffice.org.uk/Calendar/Sunday/LentSunday.shtml), the [Paschal Triduum](https://www.liturgyoffice.org.uk/Calendar/Sunday/Triduum.shtml), [Easter Time and Pentecost](https://www.liturgyoffice.org.uk/Calendar/Sunday/EasterSunday.shtml), and [Feasts of the Lord](https://www.liturgyoffice.org.uk/Calendar/Sunday/Feasts.shtml), and against the approved [Rite of Christian Initiation of Adults](https://www.liturgyoffice.org.uk/Resources/Rites/RCIA.pdf) for the Scrutinies. These universal norms and official territorial witnesses verify the schema's structural distinctions; the exact Latin typical edition, selected approved vernacular books, territorial adaptations, ritual edition, later decrees, and competent calendar still control every leaf.

## Copyright-aware source records

Keep a guide-local source audit beside each guide and link it to any canonical shared formulary record fixed above; do not duplicate the shared Missal record in the publishable leaf, and do not assume that an accessible liturgical text may be republished. For every local or shared source record:

- give the exact title, edition, language, territory, publisher or rights holder, year, volume, page or stable locator, and access date;
- record the celebration, element, incipit, biblical citation, and verification result with enough precision to reproduce the research;
- state the source's copyright or licensing status when known and flag uncertainty rather than guessing;
- quote only the minimum needed for verification and commentary unless permission or a compatible license authorizes more;
- prefer citations, incipits, references, and original analytical notes over repository copies of complete protected vernacular texts; and
- do not commit scans, bulk transcriptions, paywalled material, or circumvention-derived text.

A private copy used lawfully for collation is not automatically a distributable repository source. When the full wording cannot be tracked, record the edition and locator plus a verification note; never reconstruct a protected translation from memory or mix it with another edition. Biblical copyright and liturgical-text copyright must be evaluated separately.

## Exact-snapshot release and profile-final status

The release manifest and this profile's completion gate answer different
questions.  `release` authorizes distribution of one exact installed PDF hash;
it does not certify that the guide is profile-final or that every source-audit
layer is complete.  An express exact-snapshot approval may clear the project's
rights and liturgical-distribution gates while accepting the named
U.S.-altar-book collation and independent specialist review as disclosed
limitations.  In that case the guide remains a working exposition,
source-audited only at the layers its records identify, and not
publication-final under this profile.  Keep the missing collation and review
visible in the guide, catalog, and research records, and do not claim an
imprimatur, ecclesiastical approval, specialist review, or collation that did
not occur.  Any changed or rebuilt PDF requires a renewed exact-snapshot
approval even when its editorial maturity is otherwise unchanged.

## Completion gate

Do not describe an edition-locale's Proper-of-Time Sunday collection as complete until all 184 baseline keys are either published or carry a sourced `not-present-in-edition` disposition authorized by this profile, no cycle-split conflict remains unresolved, all three conditional Scrutiny keys have been evaluated, the six weekday fallback keys have been evaluated, and the applicable replacement and local-overlay matrix has been resolved. A celebration's absence in one civil year is an occurrence result, not a reason to omit its permanent production target.

A postconciliar proper guide reaches profile-final status only when:

- when the guide belongs to `PC-S` or `PC-R`, its permanent formula key, derived slug, source ownership, and path conform to the registries above, and an occurrence audit resolves whether that celebration governs the selected date; a ritual, local, or other proper outside those series follows its own defined inventory and may not use the reserved `PC-W` namespace;
- the registry has no duplicate key or slug, every target references exactly one canonical Missal or Ritual Mass owner, and the selected edition covers A/B/C exactly once for every appointed form without an `ABC` overlap;
- the target's branch audit accounts for every authorized longer, shorter, substitute, ritual, sequence, preface, and prayer path in the selected edition, even though those internal branches do not multiply the baseline target count;
- the leaf contains tracked `main.tex`, `generation-metadata.tex`, `instance/manifest.md`, `propers/verified.md`, and `research/scope.md`, while its canonical formulary owner contains the verified reusable Missal or Ritual Mass record;
- the liturgical-instance manifest resolves edition, language, territory, calendar, cycle, form, occurrence, ritual context, source owners, and options;
- the opening survey uses the complete two-column, one-textual-unit-row `Textual Variable Parts` inventory with actual-form phase groups and no interpretive or source-status column;
- every treated element has a source-layer and liturgical-status classification in the tracked audit; every reader-relevant textual or ritual branch has its authority, status, effect, and resolution in the liturgical-resolution appendix; and every concrete chant selection states its source and liturgical placement;
- `Study Guide: Scripture and Liturgical Context` covers every distinct directly appointed scriptural passage and marked adaptation in canonical order, distinguishes composition from narrated event, and expands rather than omits material when the target is complex;
- every cross-element relationship is classified, Ordinary Time's correlated and semi-continuous strands remain distinct, and no whole-formulary historical design is claimed without evidence;
- `Study Guide: Liturgical Movement and Textual Relationships`, `Study Guide: Theological and Spiritual Synthesis`, `Study Guide: Commentary on the Texts`, and any `Study Guide: Further Interpretive Possibilities` perform their distinct source-grounded, synthetic, evidentiary, and exploratory functions in the required order;
- the textual record contains every appointed or concretely selected text; the tracked audits account for all alternatives, unresolved selections, omissions, and applicability results; and the reader appendix presents the subset needed to identify the instance or interpret the textual record or Study Guide;
- the Study Guide and `Appendix: Liturgical Resolution` begin at their required fresh-page boundaries without compressed type or omitted material;
- optional `Reception and Cultural Echoes` and any required `Sacramental Appendix` occur in their prescribed position before `Appendix: Liturgical Resolution`, which in turn precedes `References`;
- quotations and tracked records comply with the applicable copyright or license;
- variant paths and local choices are not presented as universal requirements;
- authoritative claims, source-grounded synthesis, and editorial proposals are visibly distinct;
- `Appendix: Liturgical Resolution` preserves the reader-facing instance and the authority, status, and resolution of branches needed to interpret the text record or Study Guide; `References` then ends the scholarship with a compact `Search Scope and Limitations` panel pointing to the leaf manifest, leaf composition audit, canonical formulary-owner audit, and research scope, and imported structured `Generation Metadata` is terminal;
- every imported owner or shared fragment has an explicit cross-document build dependency, and every consumer has been rebuilt and inspected after a shared-source change;
- the PDF builds for enough passes to settle references without fatal errors, undefined references, overflow, or material layout warnings; and
- every page and every branch table is visually checked before the reviewed PDF is installed, and the mirrored source records pass the repository-wide editorial and build checks.
