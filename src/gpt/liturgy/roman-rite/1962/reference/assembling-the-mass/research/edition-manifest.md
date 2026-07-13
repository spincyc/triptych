# Assembling the Mass — Edition Manifest

## Controlling edition set

| Layer | Bibliographic identity | Material used | Control status | Digital object actually consulted |
|---|---|---|---|---|
| Promulgation | Ioannes XXIII, *Rubricarum instructum*, 25 July 1960, *AAS* 52 (1960), 593–595 | authority, effective incorporation, relation of new code to liturgical books | Primary, official | `https://www.vatican.va/content/john-xxiii/la/motu_proprio/documents/hf_j-xxiii_motu-proprio_19600725_rubricarum-instructum.html` |
| Rubrical code | *Codex rubricarum Breviarii ac Missalis Romani*, *AAS* 52 (1960), especially 597–620 | definitions, day classes, calendar layers, precedence table, occurrence, transfer, reposition, concurrence, commemorations | Primary, official | `https://www.vatican.va/archive/aas/documents/AAS-52-1960-ocr.pdf` |
| Mass rubrics | *Rubricae generales Missalis Romani*, in the same 1960 corpus and incorporated into the 1962 Missal; especially nn. 269–530 | calendar at the altar, Mass kinds, votives, Requiems, parts and conclusions of Mass | Primary, official | AAS pp. 643–685 and the typical-Missal facsimile below |
| Occurrence tables | 1960 corpus, *Tabella dierum liturgicorum* and occurrence/concurrence tables | complete twenty-eight positions and table checks | Primary, official | AAS pp. 610–612 and 703–705 |
| Typical Missal | *Missale Romanum ex decreto Sacrosancti Concilii Tridentini restitutum, Summorum Pontificum cura recognitum*, editio typica, Typis Polyglottis Vaticanis, 1962 | incorporated general rubrics; *Ritus servandus*; *Ordo Missae* and Canon; temporal, sanctoral, Common, votive, Requiem, and ritual pages | Primary, edition-controlling | `https://media.churchmusicassociation.org/pdf/missale62.pdf` (1,088-page image/OCR facsimile) |

## Internal source architecture

The document treats the typical Missal as several coordinated layers, not one undifferentiated text:

| Missal layer | Function in the manual |
|---|---|
| *Rubricae generales* nn. 269–305 | determines calendar followed at the altar, conventual obligations, Mass of the Office, repeated ferial Masses, resumed Sundays, and festive Masses |
| nn. 306–389 | defines votive classes, same-Person limits, exceptional/public/ritual permissions, external solemnity, Nuptial Mass, monthly devotions, and IV-class votives |
| nn. 390–423 | distinguishes All Souls, funeral, death-day, anniversary, cemetery, eight-day, and daily Requiems |
| nn. 424–510 | supplies the slot-level assembly rules from preparation through the Last Gospel |
| nn. 511–516 | distinguishes audible execution and solemn / ferial tone |
| *Ritus servandus* | supplies movement, ministers, incense, reading, offertory, Communion, and conclusion details not reducible to a proper-text list |
| *Ordo Missae* and Canon | supplies stable texts and exact locations for conditional or ritual insertions |
| Temporal and Sanctoral | supplies the proper texts of the selected day and explicit seasonal variants |
| Commons | completes only the elements to which a partial proper directs the reader |
| Votive / Requiem / ritual formularies | supplies category-specific proper texts, variants, and insertion directions |

## Calendar assumptions

- The universal calendar printed in the 1962 typical edition is the only concrete calendar baseline.
- Rubrics 274–284 determine which calendar an actual celebrant follows. The answer can depend on whether the place is a public or semipublic oratory, diocesan or religious church, cathedral, seminary, cemetery chapel, or travel setting.
- No United States, diocesan, religious-order, parish, title, dedication, patronal, or indult supplement was used as though universal.
- Cases 4, 10, 13, 14, 17, and any analogous local example are explicitly hypothetical until an approved particular source is attached.
- No civil year is named. The manual therefore does not depend on an unverified Easter computation or weekday alignment.

## Language and transcription policy

The controlling sources are Latin. English descriptions are fresh editorial paraphrases. Latin technical nouns are retained when translation could collapse distinctions, especially *occurrentia*, *concurrentia*, *translatio*, *repositio*, *solemnitas externa*, *Missa in cantu*, *Missa cantata*, and *Missa conventualis*.

The AAS file and the public Missal facsimile contain OCR layers, but OCR was used only to locate rubric numbers. No claim rests on an OCR spelling where the image and surrounding rule were unavailable. The publication avoids long quotations, so minor accent or ligature recognition does not enter its conclusions.

## Companion records

| Repository source | Use | Status |
|---|---|---|
| `src/gpt/liturgy/roman-rite/1962/ordinary/00-ordinary-of-the-mass/research/` | stable Ordinary / proper boundary and source architecture | supporting, not a replacement for the Missal |
| `src/gpt/liturgy/roman-rite/1962/propers/ritual/m01-nuptial-mass/propers/verified.md` | exact 1962 Nuptial formulary boundary and three ritual insertion points | supporting record visually checked against the typical-edition facsimile |

## Sources deliberately not controlling

No later Missal, pre-1960 rank table, postconciliar calendar, automated Ordo, commercial hand missal, devotional calendar, private-revelation text, blog, or unsourced “rubric cheat sheet” controls this publication. Such works may be useful for comparison, but importing their terminology could reintroduce doubles, semidoubles, multiple suppressed octaves, anticipated evening Mass assumptions, or permissions absent from the 1962 edition.
