# Propers completion: what is outstanding

State of the calendar mass indexes as of 2026-07-30, so this can be resumed
without re-deriving it. The propers themselves were deliberately left as they
are; this records what completing them would involve and what is wrong now.

## Coverage

Only the `seasonal` section of each calendar carries real propers.

| calendar | section | masses | with propers | placeholder only |
| --- | --- | ---: | ---: | ---: |
| roman-1962 | seasonal | 59 | 59 | 0 |
| roman-1962 | christological | 8 | 0 | 8 |
| roman-1962 | marian | 17 | 0 | 17 |
| roman-1962 | sanctoral | 247 | 0 | 247 |
| postconciliar | seasonal | 63 | 63 | 0 |
| postconciliar | christological | 7 | 0 | 7 |
| postconciliar | marian | 14 | 0 | 14 |
| postconciliar | sanctoral | 181 | 0 | 181 |

474 masses hold exactly one placeholder proper each. None is partial, so there
is no cheap half-finished tier. Every placeholder does carry usable `key`,
`name`, `date`, `rank` and `kind`; only `registry` is synthetic.

## Scope decided 2026-07-30

All 167 postconciliar memorials and optional memorials are in scope, so the
full 202-mass sanctoral is, with a later round for expansion.

Fill scripture-bearing slots first. Two thirds of propers carry scripture and
the commentary corpus consumes nothing else: orations are composed Latin and
contribute no passage mappings. That is roughly 3,100 propers rather than
4,700, and it sidesteps the Commons question, which is oration-side.

| carries scripture | contributes nothing to the corpus |
| --- | --- |
| Introit, Epistle, Gradual, Alleluia, Tract, Gospel, Offertory, Communion | Collect, Secret, Postcommunion |
| Entrance and Communion Antiphons, readings, Responsorial Psalm, Gospel Acclamation | Collect, Prayer over the Offerings, Prayer after Communion |

Observed slot counts: 1962 is 10 for an ordinary Sunday, 9 in Paschaltide;
postconciliar is 10 as a base and 11 typically, because the data always carries
a Gospel Acclamation and 34 of 54 masses carry a second Communion Antiphon.

## The Commons, and what changed on 2026-07-31

The scope note above says the plan "sidesteps the Commons question, which is
oration-side". It cannot be sidestepped: it is why the 1962 sanctoral is 307
placeholders. In that book a third-class saint ordinarily takes the **whole
Mass** from the *Commune Sanctorum* and prints only his own orations, so the
sanctoral is not 307 formularies to transcribe — it is thirteen Commons plus a
pointer per day, and the pointer is printed in the book, in lines of the form
`Missa In medio, de Communi Doctorum [22]`.

Three things landed that day, and the order matters because none of the rest
was possible without the first:

1. **`takes_from`**, on a mass or on a proper — the schema had no way to say
   "this mass takes that text", which is the same missing mechanism behind the
   feria that takes the preceding Sunday and the sequence appointed across a
   span. `src/sources/calendars/README.md` owns the rule; nothing is copied,
   and `_calendars.resolve_propers` is the single derivation.
2. **A `common` section**, holding masses placed by use rather than by the
   year, with the *Commune Doctorum* transcribed into it and S. Hilarii at
   01-14 taking it under the Missal's own pointer.
3. **The 1861 witness's own Common of Saints**, which nobody had opened. It
   prints the Commons and a Proper of Saints in English, and the 1843 printing
   of the same translation prints them too, so the sanctoral has the same
   two-scan detector the temporal has.

What is left, in the order it should be done:

- **Twelve Commons.** Named with their printed page ranges in the 1962 file's
  `open_collation_items`. Each is a transcription job of the shape the
  Commune Doctorum entry demonstrates.
- **The sanctoral pointers.** A first mechanical pass over an independent 1962
  scan recovered 109 of them keyed by date heading. Do not land that pass until
  it is corroborated against the CMAA facsimile and mapped onto this file's
  mass keys: a pointer resolving to the wrong Common gives a saint a whole Mass
  that is not his, and it resolves cleanly and looks right.
- **The days' own orations**, which the Missal prints under each date with the
  saint's name supplied. These are transcription, not derivation — the schema
  performs no name substitution, and inventing one would be worse than typing
  the text the book prints.

## Known defects

**1962 commemorations are not modelled.** They exist only as prose inside the
`name` string — 102 entries mention one, and 44 masses carry rank `Comm.` — so
a commemoration's own three orations have nowhere to live. The 1962 Missal
carries many more than are recorded. This needs a schema before the coverage
gap can be closed, and rank `Comm.` entries are commemorations contributing
orations to another day's Mass rather than masses in their own right.

**Three days are missing entirely.** `1962-12-29`, `1962-12-30` and
`1962-12-31`, the fifth through seventh within the Octave of the Nativity, are
in the spine and in no section. Dec 26, 27 and 28 exist but sit under `sanctoral`
while `calendar-spine` classifies them `seasonal`. Nothing compares the spine
against the propers, which is why both slipped.

**Eleven postconciliar antiphons are numbered Vulgate** inside a calendar
declaring `psalm_numbering: hebrew`, so they fail to resolve against an indexed
bible: Psalms 15:11, 17:19-20, 24:16 and 18, 28:10-11, 30:20, 32:18-19,
67:33 and 35, 72:28, 77:29-30, 118:49-50, 118:137 and 124. The recovered
`citation_convention` predicts this — antiphons reproduce the Missal's printed
number while responsorial psalms use the Lectionary's. The file-level
declaration may need to become per-slot.

**The psalter bounds check now catches them.** `validate_psalm` in
`scripts/_psalms.py` used to hold verse ceilings for the six psalms that divide
between the systems and no others, so `Psalm 118:137` passed although Hebrew 118
ends at 29. Every psalm is bounded now, from the verse-level concordance tracked
with the Challoner edition rather than from a typed table; the two ceilings that
were typed wrong — Hebrew 10 and 115 carried the last verse of the Vulgate psalm
hosting them — went with it. All eleven references above are reported by
`check-calendar-masses`, by `index-bible` as unresolved, and by
`commentary-work-index` as unconvertible.

**Two references cannot resolve for upstream reasons.** `4 Esdras 2:36-37` is
not among the Douay-Rheims' 73 books, and `Malachi 3:19-20a` is Hebrew
numbering where the Vulgate prints Malachi 4:1-6; only psalms are converted
between systems today.

## Cost

About 4,700 propers to fill everything, or about 3,100 scripture-bearing ones.
Either takes the repository's uncollated propers from 1,457 to several times
that, so the collation debt is the real price rather than the authoring.

There is no sanctoral source text in the repository, so filling means
generating leads and collating them later, exactly as the seasonal sections
were made. Those sections are marked as unverified model-generated leads
requiring collation, and anything added here must carry the same marking.
