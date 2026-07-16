# Postconciliar Proper Guides

This profile governs guides to the variable parts of postconciliar Roman-rite liturgies. It supplements the repository-wide editorial and source rules. It does **not** inherit the architecture of the 1962 weekly guides: their ten-item proper inventory, Lent-first numbering, fixed page sequence, historical dossier shape, Latin-incipit conventions, and section titles are not defaults here.

Under the present provider, each document lives at `src/gpt/liturgy/roman-rite/postconciliar/<edition-locale>/propers/<calendar-family>/<document>/`; another provider uses the same content taxonomy beneath its own provider directory. The edition-locale component is an identity guardrail, not a substitute for the fuller manifest below. The Sunday series fixes `<calendar-family>` as `temporal`; the General Calendar replacement series fixes it as `general-calendar`.

## Canonical Sunday-proper production order

The postconciliar Sunday collection uses the following **60 stable Proper-of-Time identities**. This is the firm repository order for planning, identifiers, paths, status tracking, and creation. It follows the section order of the postconciliar Roman Missal—Advent, Christmas Time, Lent and Holy Week, Easter Time, Ordinary Time, and the Sunday-capable Solemnities of the Lord in Ordinary Time—rather than the Lent-first 1962 rotation or the occurrence pattern of one civil year.

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
| A `PC-R` cycle, form, or occurrence guide | `<proper-root>/general-calendar/<full-publication-slug>/` | Publishable leaf with `main.tex` |
| Canonical `PC-R` Missal formulary owner | `<proper-root>/general-calendar/shared/formularies/<required-slug-stem>/` | Non-publishable shared source |

The shared owner keeps the edition-specific verified Missal record, provenance, rights status, and any reusable source fragment. The publishable leaf owns its resolved liturgical-instance manifest, cycle-specific Lectionary audit, analysis, generation metadata, and PDF; it references or imports the shared owner and must not become a second owner of the formulary. For `PC-S26`–`PC-S57`, the corresponding `weeks/02`–`weeks/33` directory is the shared owner. Every import outside a publishable leaf requires an explicit cross-document build dependency, and a shared-source change requires rebuilding every consumer.

### Cycles, forms, and completion

An identity is a stable parent, not by itself a complete liturgical instance. For each identity:

- link each identity to exactly one canonical Missal formulary owner at the applicable edition-locale path fixed above;
- create distinct `year-a`, `year-b`, and `year-c` Lectionary paths wherever the approved Lectionary differs, and use an `abc` path only when direct collation establishes that the appointed set is invariant;
- never use the Sunday letter to infer a weekday cycle, or the civil year's parity to infer a Sunday cycle;
- append a form suffix such as `vigil`, `night`, `dawn`, or `day` when the edition appoints materially different Mass forms; an ordinary anticipated Mass on Saturday evening remains the following Sunday's Mass and does not acquire a fictitious Vigil form;
- preserve every authorized reading substitution or option as a named branch, including the permitted Year A readings on the Third through Fifth Sundays of Lent in Years B and C; and
- count the parent complete only when all cycles, appointed forms, and materially different authorized paths in the selected editions have been sourced and evaluated, even if publication proceeds one cycle or form at a time.

A full publication slug consists of the table's stem plus suffixes in the fixed order **cycle, appointed Mass form, occurrence**. Use `-year-a`, `-year-b`, or `-year-c` for a cycle-specific guide and `-abc` only when direct collation establishes that the complete treated path is invariant across all three cycles. A publication treating all three materially different cycles together is exceptional, uses `-years-a-b-c`, and must keep the three complete paths visibly separate rather than produce a synthetic formulary. Normalize an edition-appointed form title as a literal suffix such as `-vigil`, `-extended-vigil`, `-night`, `-dawn`, or `-day`. Add an occurrence suffix only when the occurrence changes the treated path or scope, and name it exactly—for example `-december-30`, `-monday`, `-thursday`, or `-sunday`; never use a generic `-weekday`. Thus valid combinations include `-year-a-vigil` and `-year-b-monday`. Do not omit the cycle suffix from a Sunday-series publication, and do not use `-abc` without a recorded collation.

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

`PC-R` publications use the same full-slug cycle, appointed-form, and occurrence grammar fixed for `PC-S`; their source owner and publishable leaf use the `general-calendar` paths fixed above.

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

This order and policy were checked on 15 July 2026 against Paul VI's [*Mysterii Paschalis*](https://www.vatican.va/content/paul-vi/la/motu_proprio/documents/hf_p-vi_motu-proprio_19690214_mysterii-paschalis.html), the bishops' approved English [Universal Norms on the Liturgical Year and the Calendar](https://www.liturgyoffice.org.uk/Resources/GIRM/Documents/GNLY.pdf), the official [Roman Missal, Third Edition contents](https://www.liturgyoffice.org.uk/Missal/Information/RM3-contents.pdf) and [Ordinary Time directions](https://www.liturgyoffice.org.uk/Missal/Music/Antiphonary.pdf), the [General Introduction to the Lectionary](https://www.liturgyoffice.org/Resources/GIRM/Documents/Lectionary.pdf), the *Missale Romanum*, editio typica tertia, reimpressio emendata 2008, *Tempus per annum*, introductory rubrics 1–6 and formularies for Weeks I–XXXIV, especially pp. 450–484, the Dicastery's live [calendar-variations index](https://www.cultodivino.va/en/formazione/pubblicazioni/libri-liturgici/aliae/calendarium-romanum.html), and the Holy See's [General Instruction of the Roman Missal](https://www.vatican.va/roman_curia/congregations/ccdds/documents/rc_con_ccdds_doc_20030317_ordinamento-messale_en.html), especially nos. 353–363 and 376. The exact typical and vernacular editions, later decrees, and competent annual calendar still govern each publication.

## Establish the liturgical instance first

Before research or drafting, create a manifest that identifies the texts actually being studied. Record at least:

- the Latin typical edition of the Roman Missal and, when applicable, its printing or reprint;
- the vernacular Missal edition, language, episcopal conference or territory, publisher, and approval or implementation date;
- the Lectionary edition and volume, language, territory, and edition-specific reading references;
- the governing calendar: General Roman Calendar and every national, diocesan, religious, parish, or other proper calendar that affects the celebration;
- the celebration, rank, ritual or pastoral context, and civil date when a date is needed to resolve precedence;
- the Sunday cycle (`A`, `B`, or `C`), or `not applicable` when the instance has no Sunday-cycle path; the weekday cycle (`I` or `II`), or `not applicable` when the instance has no weekday readings; and any special cycle or vigil form;
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

Keep a guide-local source audit beside each guide and link it to any canonical shared formulary record fixed above; do not duplicate the shared Missal record in the publishable leaf, and do not assume that an accessible liturgical text may be republished. For every local or shared source record:

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

- when the guide belongs to `PC-S` or `PC-R`, its identity, slug, source ownership, and path conform to the defined series above, and an occurrence audit resolves whether that celebration governs the selected date; a ritual, local, or other proper outside those series follows its own defined inventory and may not use the reserved `PC-W` namespace;
- the liturgical-instance manifest resolves edition, language, territory, calendar, cycle, and options;
- every treated element has a source and liturgical-status classification;
- quotations and tracked records comply with the applicable copyright or license;
- variant paths and local choices are not presented as universal requirements;
- authoritative claims and editorial synthesis are visibly distinct; and
- the PDF and its mirrored source records pass the repository-wide build and editorial checks.
