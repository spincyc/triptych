# Inherited Ordinary-seat deployment blocker, 25 October 2026

## Reproduction and cause

Main commit `6a1fe6e3361fec6d1f011a0ae03a0e47d12fa6cf` failed
[Pages run 40033634816](https://github.com/spincyc/triptych/actions/runs/40033634816)
at `mass-ordinary check`. The focused command, run with the pinned publication
Python, reproduced exit 2:

```text
roman-1962/s-ioannis-damasceni-confessoris-ecclesiae-doctoris/main:
alternative Proper group must share one usable semantic Ordinary seat
```

The offending source unit is `john-damascene-offertory`. Its alternatives are
`Offertory` and `Offertory (Tempore paschali)`. The Ordinary declares only the
first exact name, with generic qualifier admission disabled. The shared seating
validator correctly refuses the second candidate, including when its season is
unknown or inactive. No validator relaxation is appropriate.

After the Roman 1962 table was repaired, the complete focused check exposed the
same undeclared role in the pre-1955 projection. Its candidates retain typed
foreign-source applicability and must not execute as target appointments.

## Direct evidence and bounded correction

The following whole source PDFs were matched to their canonical artifact hashes
before the stated page images were rendered at 150 dpi and individually opened.
No scan or raster is added to Git.

| Exact witness | SHA-256 | Pages actually inspected | Finding |
| --- | --- | --- | --- |
| CMAA 1962 typical-edition facsimile | `648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a` | artifact 579 / printed 498 | The heading `Ant. ad Offertorium` governs unit 2342, including its separately marked optional Paschal continuation. The two candidate bodies occupy one Offertory position. |
| Mame 1922 conformed printing | `9873693a2937c6a573ed050351b30c545b7464b87b06390785e504fb0aac7005` | artifact 77 / printed lxvii; artifact 673 / printed 559 | Ritus servandus VII.1 establishes the fixed Offertory position. The local John Damascene page has the base Offertory without the later candidate's Paschal continuation; it does not establish that candidate's target applicability or complete body. |

Canonical source records:

- `src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/artifacts/cmaa-facsimile-pdf/artifact.toml`
- `src/sources/works/catholic-church/missale-romanum/editions/1922-tours-mame-editio-quarta-iuxta-typicam/artifacts/ia-scan-pdf-9873693a/artifact.toml`

Both Ordinary inventories now list the exact project role label
`Offertory (Tempore paschali)` beside `Offertory` and state their checked loci.
Generic qualifier admission remains false. The pre-1955 locus explicitly limits
the alias to a structural role for the retained foreign candidate. It confers
neither target appointment nor body availability. The calendars, translation
sidecars, seasonal facts, raw witnesses and validator implementation are unchanged.

The native driver checked that neither edited Ordinary inventory belongs to
the accepted All Saints review-input sets or render receipt before these changes
were authorized. Its sealed calendar, rubrics and projection implementation
were preserved.

## Regression and validation

`tools/tests/test_mass_ordinary.py` adds two regressions using the real published
John Damascene candidates and freshly derived Ordinary tables:

1. Both Roman 1962 Offertory options have the same explicitly declared seat,
   retain their tract/Paschal conditions, and keep the Paschal body unavailable.
2. The pre-1955 candidates retain their foreign-source diagnostics and unresolved
   markers. Appointment preparation, unframed execution and framed unit
   construction all continue to refuse them despite their known structural seat.

The existing Matthias negative controls now use an actually undeclared qualifier
instead of the newly declared exact alias. Unknown and known-false conditions,
mixed semantic seats and arbitrary qualifier refusals retain their former force.

The following invocation passed all 20 tests:

```sh
.scratch/publication-prep/venv/bin/python -m unittest \
  tools.tests.test_mass_ordinary.OrdinaryTool.test_john_damascene_paschal_offertory_has_an_exact_declared_seat \
  tools.tests.test_mass_ordinary.OrdinaryTool.test_john_damascene_foreign_offertory_seat_does_not_authorize_execution \
  tools.tests.test_mass_ordinary.OrdinaryTool.test_matthias_normal_paschal_candidates_have_exact_ordinary_seats \
  tools.tests.test_mass_ordinary.OrdinaryTool.test_matthias_inactive_or_unknown_options_cannot_evade_exact_seat_guards \
  tools.tests.test_ordinary_foreign_seat_diagnostics \
  tools.tests.test_proper_ordinary_disposition
node tools/tests/test_foreign_static_target_seats.cjs
```

The Node invocation independently passed five guard groups. Scoped
`git diff --check` passed.

The complete `mass-ordinary check --json` then validated all 1,529 full-frame
and 100 non-full forms with zero seating failures. Its actual exit remained 1,
solely because these two generated files need the shared owner's refresh:

- `src/web/data/structure/ordinary/roman-1962.json`
- `src/web/data/structure/ordinary/roman-pre-1955.json`

No generated-data, release, index, commit or push mutation was made by this lane.
Independent cold review and a current generated-output check remain coordinator
gates; this report does not infer their future verdicts.

## Frozen source identities

| File | SHA-256 |
| --- | --- |
| `src/sources/inventories/roman-1962-ordo-missae-v1.toml` | `07d257473c98dd67ac198f1f32351b3a189984b594a7927bd4536737a8404446` |
| `src/sources/inventories/roman-pre-1955-ordo-missae-v1.toml` | `7ef0b961804e3e69074c35739fca36606ab56bea41fcdbb818d91e9645462d07` |
| `tools/tests/test_mass_ordinary.py` | `3c22165c8d72b5d8a37d56f3fe43e1a7d825633d649d693ac1c19bddd6ae8541` |
