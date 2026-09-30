# The Angels — Research Scope and Qualification Record

## Work identity and governing question

- **Provider and collection:** Anthropic Claude (the Opus 5.5 model, run
  first through the Factory Droid agent and from 2026-09-30 through Claude
  Code); theology reference works.
- **Leaf:** `theology/angelology`. The GPT edition at
  `src/gpt/theology/angelology/` is an independent composition under the
  same profile; neither edition borrows the other's prose.
- **Genre and profile:** comprehensive theological reference;
  `guidance/theology/angelology.md` governs, under the universal standard in
  `guidance/editorial.md`. The profile was written for this work on
  2026-09-29 because no existing profile fit.
- **Language, rite, and currentness:** English, with Latin and transliterated
  Greek for key technical terms. Liturgical claims name the Roman Rite book
  and calendar (pre-1955, 1962, postconciliar) and, for the Byzantine line,
  the tradition cited. Mutable facts (current calendar ranks, current
  curial documents) are checked as of the date recorded in the source audit.
- **Intended reader:** a serious Catholic reader, student, or teacher who
  wants the Church's teaching on the angels in Aquinas's systematic order,
  with the sources he received and the disputes he did not close.
- **Governing question:** What does the Catholic tradition, systematized by
  Aquinas, hold about the angels — what they are, how they know and will,
  how they were made and how some fell, how they are ordered, and what they
  do for the world and for man — and on what authority does each part rest?
- **Thesis:** the angels are the summit of creation's intellectual order.
  Aquinas's treatise reads them as pure created intelligences whose being,
  knowledge, and love are measured by their nearness to God, and whose
  hierarchy is the channel through which God's light descends to the lower
  creation. The *Celestial Hierarchy* supplies the ordering Aquinas
  receives; Gregory, Augustine, and Damascene supply much of the rest. The
  Church confesses the angels' creation from nothing, the goodness of
  their created nature, and the fall of some by their own will; the Fathers
  and Doctors unfold the rest, and the document declares each part at its
  own degree of determination.

## Recorded user deliverable (2026-09-29)

The user requested, in this order of emphasis:

1. a document on angelology following the systematic teaching of Thomas
   Aquinas, prepared under the Triptych repository's guidance;
2. the *Celestial Hierarchy* (c. 5th–6th century) sourced and included — the
   user chose a chapter-by-chapter exposition with focused quotations, not the
   complete text;
3. the corpus expanded with patristic and saintly sources as research
   warrants;
4. a robust, thorough final document with ample appendices containing
   tables, hierarchies, and similar apparatus;
5. no target length: as long as the material requires;
6. quotations in English, with the Latin or Greek of key technical
   definitions in the text or notes;
7. extensions beyond the core treatise, all four chosen: the fallen angels as
   Aquinas treats them (cross-referenced to the exorcism study); liturgy and
   devotion (1962 and postconciliar feasts, prefaces, the Leo XIII prayer to
   Saint Michael, the *Angele Dei*); the magisterium (Lateran IV, Vatican I,
   *Humani generis*, the Catechism, John Paul II's 1986 catecheses, the
   Directory on Popular Piety on angel names); and disputed questions after
   Aquinas (Bonaventure, Scotus, and Suárez on angelic matter, individuation,
   and the motive of the fall, with the Byzantine line through Damascene and
   Palamas);
8. the full publication pipeline: LaTeX leaf, research records, reviewed PDF,
   web edition, catalog row, release record, and ledger entry;
9. subagents permitted, all work done on Opus 5.5 with no model switch; and
10. incremental commits pushed to `feature/droid/theology/angelology` so that
    another agent can take over.

## Voice directive (2026-09-30)

On resuming the work the user directed that the voice simply declare what it
can, at different levels of determination; that it not spend sentences on
what is or is not dogma; that the work be an expansive, in-depth account of
what the best patristic sources wrote about the angels; and that it be an
authentic Catholic treatise, not a secular skeptical review. The profile's
"Voice and determination" section carries the resulting rules. The drafted
units were revised to them, and the patristic corpus was widened to give
the Greek and Latin Fathers before Dionysius separate sections, and to add
a section on the saints and spiritual writers.

The ledger entry `claude-angelology-2026-09-29` in
`promised-deliverables.toml` carries these as requirements.

## Planned structure

Body, in the profile's reader order:

1. The angels in Sacred Scripture
2. The faith of the Church concerning the angels
3. The Greek Fathers before Dionysius
4. The Latin Fathers before Dionysius, with Augustine and Cassian
5. The *Celestial Hierarchy* — the corpus, its reception, and all fifteen
   chapters
6. The Fathers and Doctors after Dionysius, to Peter Lombard
7. The angelic substance (I q. 50)
8. Bodies, place, and motion (qq. 51–53)
9. The angelic intellect and its knowledge (qq. 54–58)
10. The angelic will and love (qq. 59–60)
11. Creation, grace, and glory (qq. 61–62)
12. The fall of the angels and its punishment (qq. 63–64; *De malo* q. 16)
13. Illumination and speech (qq. 106–107)
14. Hierarchies and orders, good and fallen (qq. 108–109)
15. The angels in the government of the world; their mission (qq. 110–112)
16. The guardian angels (q. 113)
17. The assaults of the demons (q. 114)
18. Christ, Mary, and the angels; men and the angelic ranks
19. Disputed questions after Aquinas
20. The Byzantine line
21. The angels in the liturgy
22. Devotion and its regulation
23. The saints and the holy angels
24. The angels and the order of the universe

Appendices: the nine orders; comparative orderings; the article census;
parallels in Aquinas's other works; the *Celestial Hierarchy* in the
*Summa*; magisterial chronology; the angels in the calendar; Scripture
index; the names of angels; the demons' powers and limits; positions on the
first sin; terminology; witness register; Scope, Corpus, and
Qualifications; References.

## Evidence and authority structure

1. **Scripture:** Douay–Rheims (Challoner), public domain; Vulgate numbering
   with Hebrew numbering added where it differs.
2. **The Dionysian corpus:** *Celestial Hierarchy*, PG 3 chapter and section
   numbering; English from John Parker's public-domain translation (edition
   and date to be fixed in the source audit from the witness actually read).
3. **Aquinas:** *Summa theologiae*, Latin of the Leonine text as presented at
   Corpus Thomisticum; English of the Fathers of the English Dominican
   Province (public domain) as presented at New Advent. Parallels in the
   *Scriptum super Sententiis*, *Summa contra gentiles*, *De veritate*,
   *De spiritualibus creaturis*, *De substantiis separatis*, and *De malo*.
4. **Fathers and Doctors:** read at their own loci in identified
   public-domain editions and translations (Migne; ANF and NPNF series).
5. **Magisterium:** acts at their official or Denzinger loci; the Catechism
   and papal catecheses at the Holy See's official presentation.
6. **Liturgy:** the repository's calendar indexes and identified missals and
   breviaries; received prayers only from identified witnesses.
7. **Project synthesis:** gradings, tables, comparative orderings, and
   section architecture; attributed to no source.

## Grading rule

Each proposition carries one grade from the profile: Defined, Church
teaching, Common teaching, Thomist position, Disputed, Pious tradition, or
Apocryphal. The grade cites its basis; where the witnesses do not settle it,
the lower grade is used and the reason stays beside the claim.

## Included and excluded scope

Included: every article of I qq. 50–64 and 106–114; Aquinas's parallel
treatments where they clarify or depart; the fifteen chapters of the
*Celestial Hierarchy*; the principal patristic witnesses Aquinas uses or
that shaped the questions he answers; the magisterial acts on the angels'
existence, creation, nature, fall, and cult; the Roman liturgical cult of the
angels in the three calendars the repository carries; the regulation of
devotion; the named disputed questions after Aquinas; and the Byzantine line
as far as Damascene and Palamas.

Excluded: rites, discipline, and pastoral practice of exorcism (owned by the
exorcism study); discernment of particular cases; claims about any named
person's spiritual state; angelology of non-Christian religions except where a
Father's argument requires it; the complete text of the *Celestial
Hierarchy* or of any other work; art history beyond what the liturgy's own
texts carry; and any adjudication among Catholic schools beyond reporting
their positions and the Church's acts.

## Rights

Project prose, tables, and gradings are CC BY 4.0 under `LICENSE`.
Quotations are from public-domain translations and editions identified in
the source audit. Postconciliar English liturgical text is cited, not
reproduced, unless `guidance/liturgical-text-publication-policy.md` permits
the specific use.

## Review

No independent theological, clerical, or ecclesiastical review has been
performed or is claimed.
