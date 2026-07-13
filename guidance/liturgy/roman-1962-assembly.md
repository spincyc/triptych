# Assembling a Mass from the 1962 Roman Missal

This profile governs edition-specific reference works that explain how the Ordinary and variable propers are combined for a celebration according to the 1962 *Missale Romanum*. It does not govern a weekly proper guide or an exposition of the Ordinary. Under the present provider, publishable works live beneath `src/gpt/liturgy/roman-rite/1962/reference/`; build and installed PDFs mirror that path.

The object is the textual and rubrical system promulgated for the 1962 Missal: the 1960 *Codex rubricarum* as incorporated into the Missal, the *Rubricae generales Missalis Romani*, the *Ritus servandus*, and the edition's formularies. A reference identifies the Latin typical edition and any hand Missal, calendar, particular supplement, ceremonial, or translation it actually uses. Present canonical authorization to celebrate with this book is a distinct, mutable question and is outside scope unless the work deliberately researches and dates it.

## Keep the governing questions separate

An assembly reference must distinguish at least five decisions:

1. **Which liturgical day occurs?** Determine the temporal cycle, sanctoral cycle, proper calendar, vigils, octaves, and permitted Saturday observance.
2. **Which day has precedence?** Apply the 1960 table of liturgical days and the rules of occurrence. A feast's class, a feria's class, and a Mass category's class are related rubrical facts, not interchangeable labels.
3. **What happens to an impeded item?** Transfer, reposition, commemoration, or omission requires its own rule. Do not infer one merely from the fact that another day wins.
4. **Which kind of Mass is celebrated?** The Mass of the Office, a festive Mass, votive Mass, Requiem, ritual Mass, or external solemnity has its own admission rules.
5. **How is the admitted formulary assembled?** Only after the first four decisions may the Ordinary, proper texts, commemorations, seasonal interventions, and ceremonial directions be placed in sequence.

Occurrence concerns two offices or days falling on the same civil date. Concurrence concerns adjacent offices meeting at Vespers. A Mass manual must not import concurrence rules into the morning's choice of Mass. Likewise, the rank of the liturgical day does not by itself answer whether a requested votive, funeral, or ritual Mass is permitted.

## Required research records

Every document leaf keeps and imports one structured `generation-metadata.tex` record and keeps:

- `research/scope.md`, identifying edition, language, calendar assumptions, jurisdiction, included Mass categories, excluded canonical questions, source hierarchy, material uncertainties, and review state;
- `research/edition-manifest.md`, identifying the controlling Missal, rubrical code, general rubrics, Order of Mass, particular calendars or supplements, and any non-controlling working aid;
- `research/rubric-index.md`, mapping every decision rule and worked case to exact numbered rubrics and distinguishing direct rule, necessary inference, and editorial workflow;
- `research/worked-cases.md`, recording each case's date conditions, governing calendar, competing items, precedence row, consequence for the impeded item, permitted Mass category, inserted texts, and answer check; and
- `research/source-audit.md`, recording the actual facsimiles, official acts, translations, OCR status, supporting scholarship, rejected leads, and unresolved discrepancies.

The *Acta Apostolicae Sedis* promulgation of the 1960 rubrical code and a checked 1962 Missal facsimile control. OCR and commercial or devotional calendar tools are finding aids only. If a worked case depends on a diocesan, national, religious, church-title, patronal, or indult calendar, identify and source that particular law instead of treating a hypothetical local rank as universal.

## Day classes, Mass classes, and precedence

Teach the rubrical taxonomy exactly. Sundays and ferias have their own class rules. Feasts are class I, II, or III; class IV is not a fourth class of feast. Our Lady on Saturday is a class IV office, while votive and Requiem Masses are also classified for their separate admission rules. The document should repeatedly name which kind of class it is using where confusion is possible.

Reproduce or closely map the precedence table without silently shortening away exceptions. The explanation must cover:

- Sundays of class I and II, including the particular exceptions for the Immaculate Conception and feasts of the Lord;
- ferias of Holy Week, Ash Wednesday, Advent, Lent and Passiontide, Ember days, and ordinary class IV ferias;
- universal and particular feasts, including patrons, titulars, dedications, and religious calendars where sourced;
- privileged and ordinary commemorations, their numerical limits, and the prohibitions against commemorating the same person or mystery twice;
- accidental and perpetual occurrence, transfer, and reposition; and
- the distinction between an external solemnity, a transferred feast, and an allowed festive or votive Mass.

Never reduce the system to “celebrate the higher number and commemorate the lower.” The governing table establishes precedence; separate rubrics determine the losing item's disposition and the admissibility of another Mass.

## Assembly map

The published work should give a complete slot-by-slot map from ministers' entrance through the last Gospel, showing which material comes from:

- the stable Order of Mass and Canon;
- the proper of the season, saint, common, votive, ritual, or Requiem formulary;
- the day's psalter or resumed Sunday instructions;
- an allowed commemoration or additional collect;
- conditional seasonal rules, including Gloria, Alleluia or Tract, Credo, preface, *Benedicamus Domino*, and last Gospel; and
- Low, sung, or Solemn execution and any genuinely governing companion book.

The map must explain how to use a Common when a sanctoral formulary supplies only some texts, how several references compose one complete formulary, and how the celebration's liturgical color and named preface are determined. It must identify rather than silently fill any item that the controlling source leaves to a Common, proper calendar, choice, or local rule.

## Devotional weekdays and requested Masses

First Friday and First Saturday are not automatic replacements for the Mass of the day. State the 1962 conditions for the class III votive Masses of the Sacred Heart and Immaculate Heart, including the qualified church or oratory, exercises actually held that day, allowed number of Masses, and prohibition on liturgical days of class I or II. Distinguish:

- the First Friday votive of the Sacred Heart from the Office or external solemnity of the Sacred Heart;
- the First Saturday votive of the Immaculate Heart from the class IV Office and Mass of Our Lady on Saturday; and
- private devotional practice or an apparition-associated request from permission to replace the day's liturgical Mass.

Apply the same discipline to Masses of Christ the Eternal High Priest, other class III or IV votives, external solemnities, funeral and other Requiem Masses, and ritual Masses. A good reason, pastoral custom, or number of attendees does not erase the edition's enumerated prohibitions.

## Worked-case standard

Include enough fully solved cases to test every major branch, not merely obvious examples. At minimum cover:

- a class I feast meeting a class I or II Sunday, including the Immaculate Conception exception;
- a class II feast of the Lord and a class II saint meeting a class II Sunday;
- a class III saint meeting an Advent feria before 17 December and a Lenten feria;
- an Ember day, Ash Wednesday, Holy Week, the Annunciation impeded near Easter, and All Souls on Sunday;
- universal and particular feasts whose relative order cannot be solved from class alone;
- multiple eligible commemorations at each day class and an excluded duplicate commemoration;
- qualified and unqualified First Friday and First Saturday requests on class I, II, III, and IV days;
- an external solemnity that does not transfer the Office;
- a funeral or ritual Mass on both an admitted and a prohibited day;
- a resumed Sunday after Epiphany used after Pentecost; and
- at least one hypothetical local patron, titular, or dedication case whose answer expressly depends on a sourced proper calendar.

Every answer shows its work in this order: calendar facts; competing ranks; exact precedence row and exception; treatment of the impeded item; Mass-category permission; complete formulary assembly; and remaining uncertainty. Examples must use a named civil year only if the calendar has been computed and checked for that year; otherwise state conditions abstractly and avoid a fictitious date.

## Completion gate

A 1962 assembly reference is ready to publish only when:

- all controlling rubrical claims are traced to exact numbered rubrics in the 1960 code or 1962 Missal;
- day class, feast class, Mass class, occurrence, concurrence, transfer, reposition, commemoration, and omission remain distinct;
- the Ordinary/proper assembly map accounts for every variable slot and conditional intervention;
- universal, national, diocesan, religious, and church-specific calendars are not conflated;
- First Friday, First Saturday, external solemnity, votive, Requiem, and ritual permissions are stated with their actual conditions;
- each worked case has been independently recalculated from the rules and agrees with its research record;
- the work does not imply present canonical authorization beyond its stated textual scope; and
- universal metadata validation, multi-pass build, clean-log inspection, every-page visual review, PDF structure checks, installed/build comparison, source records, and catalog update are complete.
