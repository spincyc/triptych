# Research Scope

## Identity

- **Provider:** Claude (Anthropic).
- **Collection and genre:** Roman-rite liturgy; edition-specific calendar reference under
  `guidance/liturgy/roman-calendar-references.md`. This leaf is scoped as a **norms, temporal-cycle,
  and precedence reference with a partial fixed inventory**, not as a complete normative inventory
  of the sanctoral.
- **Rite:** Roman Rite in its 1962 state.
- **Controlling norms:** *Rubricae Breviarii et Missalis Romani*, approved by John XXIII's apostolic
  letter *motu proprio* *Rubricarum instructum* of 25 July 1960 and promulgated by general decree of
  the Sacred Congregation of Rites on 26 July 1960, printed in *Acta Apostolicae Sedis* 52 (1960)
  593-740 with the annexed *Variationes*. Part one (*Rubricae generales*, nn. 1-137) and part three
  (*Rubricae generales Missalis Romani*, nn. 269-530) govern; part two (Breviary rubrics,
  nn. 138-268) is out of scope by the same code's own division of labour.
- **Controlling book:** *Missale Romanum*, editio typica, declared typical by decree of the Sacred
  Congregation of Rites of 23 June 1962, with its front matter, its universal *Calendarium* at
  printed pages XLV-LIII, and its paschal tables.
- **Effective law:** the code binds from 1 January 1961. The 1962 Missal is the book made to fit a
  law already in force, not the instrument that enacted it.
- **Territory:** the universal Roman calendar only. No territorial, diocesan, religious, titular,
  dedication, or patronal layer is inventoried; the rules by which such layers are built are given.
- **Normative cutoff:** 23 June 1962. No later act is stated as modifying the calendar or rubrics
  described. Later permissions concerning the use of the older books are deliberately not stated.
- **Language:** normative Latin throughout. Every English rendering in the publication is a labelled
  project working gloss; no approved English translation of a rubric is quoted or implied.
- **Governing profiles:** `guidance/liturgy/roman-calendar-references.md` governs this leaf;
  `guidance/liturgy/calendar-computation.md` owns the recurring arithmetic the publication states and
  applies; `guidance/editorial.md` and `guidance/web-editions.md` govern evidence and the web
  edition.

## Question and intended reader

The question is not "what was celebrated" but "what does the law say, and where does it say it".
The reader is someone who must ground a rule at its own locus: a compiler of a calendar reference, a
writer of 1962 proper guides, a student of the 1962 books, or an editor checking a received summary
against the promulgated text. The publication is therefore organised by locus, and quotes the rule
rather than paraphrasing a received summary of it.

## Inclusion rules

Included:

- the complete normative temporal cycle: the six seasons and their sub-periods with exact
  boundaries (nn. 71-77); the classes and closed enumerations of Sundays (nn. 9-20), ferias
  (nn. 21-27), vigils (nn. 28-34), and octaves (nn. 63-70); the Ember and Rogation provisions
  (nn. 80-90 and the Missal's *De anno et eius partibus*);
- the movable computation from Easter, both counts and their ranges, and the resumption mechanism at
  n. 18 with its two Missal loci;
- the complete rank and precedence machinery: the four classes and the grade conversion from the
  older system; the table of precedence at n. 91 in full; occurrence, translation, reposition, and
  concurrence (nn. 92-105); commemorations and the counting rules (nn. 106-114) with their Missal
  implementation in the orations (nn. 433-465);
- the structure of the printed sanctoral, the complete I class and II class entries of the universal
  calendar, the rules for particular calendars (nn. 41-58) and for assigning days (nn. 59-62), and
  the itemised calendar changes recorded in *Variationes in Calendario*, nn. 1-12.

Excluded, and said to be excluded in the publication's terminal appendix:

- an entry-by-entry inventory of the III class feasts and commemorations;
- any territorial, diocesan, religious, or church calendar and its contents;
- an Ordo for any civil year; the worked years apply universal rules and are not occurrence records;
- Mass and Office texts beyond short rubrical sentences quoted as law;
- the Breviary rubrics (nn. 138-268) and the Acta's tables of occurrence and concurrence;
- present discipline concerning the use of the 1962 books.

Because the sanctoral inventory is partial by design, nothing in this leaf may be presented as a
"complete calendar" within the meaning of the governing profile.

## Terminology

The publication uses the edition's own taxonomy and no other. Liturgical days are of the I, II, III,
or IV class; there are no solemnities, feasts, memorials, or optional memorials in this system, and
no Ordinary Time. *Tempus "per annum"* is the code's own term of art, written in inverted commas,
and is not the postconciliar *tempus per annum*. A commemoration is not a rank of feast but the mode
of non-full celebration defined at n. 5. English labels for entries are project working glosses;
Latin entry titles are given as the calendar prints them.

## Uncertainties carried into publication

1. The year of twenty-three Sundays after Pentecost is unlegislated. Two readings are set out at
   full strength, an editorial assessment is labelled as such, and the case is left unresolved.
2. Which II class feasts are *festa Domini* is operative at lines 14 and 16 of the table and at
   n. 16 a, and no controlling list was established. The concrete instance of 9 November 2008 is
   left open.
3. The act that changed the September Ember dating from the Exaltation of the Holy Cross to the
   third Sunday of September is not identified.
4. Whether the pre-1960 Breviary rubrics carried an equivalent exclusivity clause is untested; the
   Missal side of that test was run and is reported.

## Rights

The Latin quoted is official normative and liturgical text of the Holy See; the project claims no
rights in it. Quotation is focused on rules the publication states and does not reproduce Mass or
Office prayers. Working glosses are project-created English, marked as such, and are not
translations of record. The two controlling digitisations and the two comparative witnesses are
registered in `src/sources/works/` with their retrieval routes, hashes, and rights status; all four
are recorded with rights unresolved and no payload is retained in the repository.

## Review state

No independent liturgical, rubrical, historical, or canonical review has been performed. The
publication is a study aid, not an official liturgical book, a critical edition, an Ordo, a
canonical opinion, or a substitute for the competent authority, and it says so in its terminal
appendix.
