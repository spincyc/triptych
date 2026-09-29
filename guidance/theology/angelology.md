# Angelology Reference Work

This profile governs the comprehensive reference on the angels at
`src/<provider>/theology/angelology/`. It is not a devotional manual, a guide
to discerning or combating spiritual assault in a particular case, a catalogue
of angel names, or a history of exorcism; the exorcism study under
`history/catholic-exorcism/` owns rites, discipline, and pastoral practice.

## Governing priorities

1. Follow the order of Aquinas's treatise, *Summa theologiae* I qq. 50–64 and
   106–114, as the systematic spine, and name the governing question and
   article of every doctrinal claim drawn from it.
2. Keep grades of authority distinct: defined faith, other Church teaching,
   the common teaching of Fathers and theologians, the Thomist position among
   Catholic schools, disputed opinion, and pious or apocryphal tradition.
3. Give the *Celestial Hierarchy* of the Dionysian corpus its own
   chapter-by-chapter exposition as the text Aquinas received, stating its
   attribution and date where they bear on a claim.
4. Carry disagreement among Fathers, Doctors, and schools rather than
   harmonizing it.
5. Put corpus, completeness, grading rule, terminology, and global
   qualifications in terminal apparatus.

## Corpus and controlling inventory

The controlling corpus is:

- Sacred Scripture, cited by Vulgate book, chapter, and verse with the Hebrew
  numbering added where it differs, quoted in English from a registered
  public-domain witness;
- the *Celestial Hierarchy*, addressed by chapter and section as printed in
  Migne, *Patrologia Graeca* 3, quoted in English from an identified
  public-domain translation;
- Aquinas, *Summa theologiae* I qq. 50–64 and 106–114, with III q. 8 a. 4 and
  other loci where the treatise points to them, and the parallel treatments
  in his other authentic works where they clarify or depart from the *Summa*;
- the Fathers and Doctors who supply the treatise's authorities or its
  contrary opinions, read at their own loci rather than through the *Summa*'s
  quotation of them;
- conciliar, papal, and curial acts that teach or regulate belief and
  devotion concerning the angels; and
- the liturgical books and calendars in which the angels are celebrated,
  identified by rite, edition, and calendar.

Later school authors (Bonaventure, Scotus, Suárez, and others) and the
Byzantine tradition enter as witnesses to named disputed questions, each at
an identified locus. Handbooks, encyclopedias, and modern charts are finding
aids; they cannot supply a position to a named author.

`research/question-inventory.md` lists every article of I qq. 50–64 and
106–114 exactly once: key, question and article, the article's question as
posed, Aquinas's determination, the principal authority of the *sed contra*,
grade, body location, and any recorded contrary opinion. The article census
appendix is that inventory's reader-facing projection and must agree with it.

`research/order-inventory.md` records the angelic orders across witnesses:
order key, source term in each language, scriptural locus, rank in each
witness's list, the witness's characterization, and verification state.
Every comparative ordering printed in the publication appears there with its
locus.

## Grades of authority

Grades describe the standing of a proposition, not the weight of the author
who states it. Use these reader-facing values:

- **Defined** — taught by a conciliar definition or profession of faith;
- **Church teaching** — taught by the ordinary magisterium, the Catechism, or
  a papal act, without a definition;
- **Common teaching** — held commonly by the Fathers and theologians, without
  a magisterial act that teaches it;
- **Thomist position** — Aquinas's systematic determination as such; name a
  contrary Catholic school when its position has been read at its own locus,
  without implying that this label alone establishes dissent;
- **Disputed** — an open question on which the witnesses divide without a
  prevailing common teaching; and
- **Pious tradition** or **Apocryphal** — devotional or extra-canonical
  material, stated as such.

The grade attached to a proposition is project synthesis. Its basis is the
act or witness cited beside it; where the witnesses do not settle the grade,
the lower grade is used and the reason stays with the claim. Terminal
apparatus states the grading rule once.

Do not use **Disputed** merely because a survey establishing common teaching
has not been performed. It records an actual open disagreement in the
identified witnesses. Attribute a scholastic determination to Aquinas instead
of manufacturing uncertainty about what he teaches. This clarification follows
the maintainer's 29 September 2026 direction to give an affirmative Catholic
treatise at the appropriate levels of determination, with compact authority
distinctions and expansive patristic exposition.

## Dossier contract

Each treated question of the *Summa* receives exposition in prose and one
dossier frame with these fields: `Summa`, `Grade`, `Authorities`, and
`Contrary opinion` where one is recorded. `Authorities` names the witnesses
the article itself invokes and any added patristic, conciliar, or liturgical
witness read for the claim. Definitions and determinations are source-grounded
synthesis; a quotation is marked as one and carries its locus.

## Celestial Hierarchy exposition

Treat all fifteen chapters in order. For each, give the chapter's title as
printed in the translation used, its PG 3 locus, an exposition of its
argument, focused quotations with section numbers, and the loci at which
Aquinas receives or qualifies it. Do not reproduce the treatise entire.

State the attribution to Dionysius the Areopagite of Acts 17:34 and the modern
dating of the corpus where the exposition's claims depend on either; report
the corpus's authority in the Church's reception as the reception records
it. The Dionysian order of the orders and Gregory the Great's differ; present
both, and Aquinas's account of the difference, rather than silently choosing
one.

## Liturgy, prayer, and devotion

Every liturgical claim names the rite, the typical edition or calendar, and
the date or rank as that book gives it; use the repository's calendar indexes
under `src/sources/calendars/` where they carry the day. Every text offered
for prayer reproduces an identified witness under the editorial standard:
Latin from an identified edition, English only from an identified human
translation whose rights are recorded. Postconciliar English liturgical text
follows `guidance/liturgical-text-publication-policy.md`.

Report the Church's regulation of devotion to the angels — including the
limitation of proper names to those Scripture gives — at the act that makes
it, with its date and authority.

## Fallen angels

Treat the demons as the treatise does (I qq. 63–64, 109, 114, with *De malo*
q. 16 as its parallel): their sin, punishment, order, and assault. Do not give
instructions for deliverance, a method for judging a particular case, or any
claim about a named person's possession, and point to the exorcism study for
rite and discipline. Sensational or speculative material that the corpus does
not require is omitted rather than rebutted.

## Required records

The leaf keeps:

- `research/scope.md`: question, reader, thesis, corpus and completeness rule,
  grading rule, rights, limits, review, and the recorded user deliverable;
- `research/source-audit.md`: every witness, edition, translation, rights
  basis, exact loci read, and verification ceiling;
- `research/question-inventory.md`: the article census and its gradings;
- `research/order-inventory.md`: the comparative orders;
- `research/terminology-audit.md`: preferred English terms, Latin and Greek
  source terms, translation choices, and collisions; and
- `research/source-bindings.toml`: bindings under `guidance/sources.md`.

## Reader order and terminal apparatus

After title and contents, begin with the angels in Scripture and the faith of
the Church; then the Fathers' witness before and after Dionysius, with the
*Celestial Hierarchy* exposition in its place; then the treatise in the
*Summa*'s order; then Christ, Mary, and the angels; the disputed questions
after Aquinas and the Byzantine line; the liturgy; and devotion with its
regulation.

Appendices follow in this order: reference tables and concordances (orders,
comparative orderings, article census, parallels in Aquinas's works,
*Celestial Hierarchy* citations in the *Summa*, magisterial chronology,
calendar, Scripture index, names, the demons' powers and limits, positions on
the first sin, terminology, and witness register); then `Scope, Corpus, and
Qualifications`; references; and generation metadata. The scope appendix owns
the question, reader, corpus and completeness rule, grading rule, terminology
policy, translation and rights policy, global limits, and review facts.

## Profile gate

Publication, question inventory, order inventory, terminology audit, and
appendices must agree. Every article of the two question ranges appears once
in the census with its determination and grade; every comparative order row
carries a locus read at its source; every grade has a stated basis; every
quotation has an identified witness and locus; every received prayer
reproduces an identified witness; and independent theological review is
claimed only when recorded.
