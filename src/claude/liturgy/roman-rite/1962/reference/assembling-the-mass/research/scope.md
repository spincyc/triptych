# Assembling the Mass (Claude edition) — Research Scope

## Identity

- **Provider:** Anthropic Claude, recorded in the leaf's `generation-metadata.tex`.
- **Collection / genre:** *Triptych*; edition-specific 1962 Roman-rite assembly reference.
  Governed by `guidance/liturgy/roman-1962-assembly.md`.
- **Rite and edition:** Roman Rite as printed in the 1962 Vatican typical edition of the
  *Missale Romanum*, applying the 1960 code of rubrics as that edition reprints it.
- **Language:** English exposition; Latin quoted from the controlling witness at its own locus.
- **Calendar layer:** the universal calendar. Every national, diocesan, religious, titular,
  patronal, dedication or indult result is stated as a conditional and names the approved
  proper that must be produced.
- **As-of date:** 2026-07-26. This date bounds the research; it makes no statement about
  present authorization to celebrate with the 1962 Missal.

## Research question

How does a reader determine, for a particular civil date, (1) which liturgical days occur,
(2) which of them takes the day, (3) what becomes of each impeded item, (4) which category of
Mass is admitted, and (5) what fills each variable slot of the Mass from the prayers at the
foot of the altar through the Last Gospel?

The five decisions are deliberately kept separate. The work's governing claim is that the
fourth decision does not reduce to the day's class; that claim is argued, with its strongest
counterargument, in the terminal `Project synthesis` block of Section 5 of the publication.

## Included subjects

- the liturgical day and its five kinds, the four day classes, and the Office of Our Lady on
  Saturday;
- which calendar binds a Mass in a given church, oratory, ship, seminary or house;
- Sundays, ferias, vigils, octaves, feasts, and the enumerated proper feasts a particular
  calendar must carry;
- the complete twenty-eight-row table of precedence, transcribed;
- occurrence (accidental and perpetual), concurrence, transfer, reposition, omission;
- the commemoration system: privileged and ordinary, the numeric ceilings, the identity
  exclusions, order, and what the 1960 reform removed;
- Mass categories: Mass of the Office, festive Masses in the strict and broad sense, votive
  Masses of four classes, Masses of the dead of four classes, ritual prayers, the nuptial
  Mass, and external solemnity;
- the complete slot map of the variable surface of a Mass, with the source of each slot;
- the number, order and conclusions of the orations, the imposed prayer and the votive prayer;
- the Preface decision procedure and the sixteen prefaces with both their assignments;
- the Last Gospel, its one express substitution and its six omissions;
- six worked cases; a twelve-line worksheet; a rubrical concordance with claim classes.

## Excluded questions

- present universal or particular authorization to celebrate with the 1962 Missal, and all
  questions of faculties;
- the arrangement of the Divine Office. Part two of the code (nn. 138–268) is used only for
  nn. 237–238 (cited as RGBR n), because RGMR 431 a depends on them;
- ceremonial: how ministers move at Solemn, pontifical, ordination, funeral, marriage,
  procession or exposition rites;
- an exposition of the restored Order of Holy Week, which is presupposed;
- canon law: the obligation of hearing Mass, the *pro populo* application, marriage law and
  funeral law are named only where a rubric points at them;
- reproduction of any formulary. The work explains where text comes from and prints no Mass;
- the construction of any actual national, diocesan, religious or local calendar.

## Source hierarchy

1. The code of rubrics as printed at the front of the 1962 Vatican typical *Missale Romanum*
   — the controlling witness for every rule cited as RG n or RGMR n.
2. The same code, and its promulgating acts, in *Acta Apostolicae Sedis* 52 (1960) — textual
   control, promulgation record, and the source of RGBR 237–238 which the Missal omits.
3. The Missal's own *Ordo Missae*, *Ritus servandus* and per-Mass rubrics — controlling for
   the Ordinary's text and conditional directions and for a formulary's own directions.
4. The *Variationes* of 1960 — used only for what the reform abolished.
5. Identified historical English witnesses (Cummiskey 1861; Douay-Rheims Challoner), quoted
   as witnesses and never as liturgical translations.
6. Optical transcriptions of the Benziger 1962 *editio iuxta typicam* — a locating aid only.

No manual, commentary, handbook or Ordo was consulted or cited. That limitation is stated in
the publication's References and is a real gap: see below.

## Translation and inference policy

The publication renders rules in English as explanation, never as an official translation.
Latin is quoted from the controlling witness with ligatured æ and œ rendered `ae` and `oe`
and the Missal's pronunciation accents dropped; nothing else is altered.

Three claim classes are used and are visible in the rendered text and in
`rubric-index.md`: **D** direct rule, **I** necessary inference, **C** contested.

## Material uncertainties

- **RGMR 406 b and second-class Sundays.** The grammar of `comprehensis` and the corroborating
  clause of RGMR 407 favour the reading on which the funeral Mass is not barred on an ordinary
  Sunday; the contemporaneous *festa de praecepto* list of the Sacred Congregation of the
  Council (3 December 1960) gives the contrary reading its footing. No answer is asserted.
- **RGMR 494 b and a Mass that is not of the Sunday.** Both readings are given. Unresolved.
- **RG 18 when Christ the King occupies a resumed Sunday's slot.** Both readings are given.
  Unresolved; a competent Ordo decides.
- **RGMR 271 and the sung/read boundary** when a choir sings and the celebrant reads. The
  literal test is preferred and the residual doubt is recorded.
- **RGMR 422's octave when All Souls has been transferred.** Marked as a necessary inference
  in the publication, not as a direct rule.
- **No result has been collated against a published Ordo** for any year the work names. Every
  civil date was computed and cross-checked against the code's own date rules only.
- **The synthesis claim in Section 5 rests on partial collation.** An exhaustive collation of
  RGMR 289–423 against the precedence table was not attempted, and the publication says so.

## Rights

Latin from the 1960 code and the 1962 Missal is official text of the Holy See, quoted at its
loci for study. The 1861 Cummiskey English and the Douay-Rheims Challoner English are
identified historical translations quoted as witnesses; neither was composed, adapted or
modernised by this project. The digitisations through which these texts were read are
third-party artifacts whose rights status is recorded in `src/sources/`; no page image or bulk
transcription is reproduced in the publication.

## Review state

- Scope, edition manifest, rubric index, worked-case ledger and source audit created
  2026-07-26.
- Every numbered rubric cited in the publication was read at its own locus. Every rubric
  quoted in Latin was additionally read as a page image (260 dpi for the Missal facsimile,
  200 dpi for the *Acta*).
- Build, log review, every-page visual review and web-edition conversion are recorded in
  `source-audit.md`.
- This is an internal source audit. It is not independent specialist, theological, canonical
  or liturgical review, not an Ordo, and not an ecclesiastical approval.

## Research-staleness verdict — 2026-07-26

The complete unbaselined input set and both candidates were compared. No rule,
case, slot, contested reading, or source boundary requires correction. This
exact edition is ready for its first baseline.
