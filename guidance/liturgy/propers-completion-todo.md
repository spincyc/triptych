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
| roman-1962 | saintly | 247 | 0 | 247 |
| postconciliar | seasonal | 63 | 63 | 0 |
| postconciliar | christological | 7 | 0 | 7 |
| postconciliar | marian | 14 | 0 | 14 |
| postconciliar | saintly | 181 | 0 | 181 |

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

## Known defects

**1962 commemorations are not modelled.** They exist only as prose inside the
`name` string — 102 entries mention one, and 44 masses carry rank `Comm.` — so
a commemoration's own three orations have nowhere to live. The 1962 Missal
carries many more than are recorded. This needs a schema before the coverage
gap can be closed, and rank `Comm.` entries are commemorations contributing
orations to another day's Mass rather than masses in their own right.

**Three days are missing entirely.** `1962-12-29`, `1962-12-30` and
`1962-12-31`, the fifth through seventh within the Octave of the Nativity, are
in the spine and in no section. Dec 26, 27 and 28 exist but sit under `saintly`
while `calendar-spine` classifies them `seasonal`. Nothing compares the spine
against the propers, which is why both slipped.

**Eleven postconciliar antiphons are numbered Vulgate** inside a calendar
declaring `psalm_numbering: hebrew`, so they fail to resolve against an indexed
bible: Psalms 15:11, 17:19-20, 24:16 and 18, 28:10-11, 30:20, 32:18-19,
67:33 and 35, 72:28, 77:29-30, 118:49-50, 118:137 and 124. The recovered
`citation_convention` predicts this — antiphons reproduce the Missal's printed
number while responsorial psalms use the Lectionary's. The file-level
declaration may need to become per-slot.

**The psalter bounds check is too narrow to catch them.** `validate_psalm` in
`scripts/_psalms.py` holds verse ceilings only for the six psalms that divide
between the systems, so `Psalm 118:137` passes although Hebrew 118 ends at 29.
Full Vulgate verse counts can be derived from the tracked Challoner edition
rather than typed by hand, and Hebrew references validated by converting first.

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
