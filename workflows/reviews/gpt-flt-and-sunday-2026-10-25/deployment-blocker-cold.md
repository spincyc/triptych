# Independent review of the inherited deployment repair

**ACCEPT** the frozen three-file source repair below. No source, seating, or
guard blocker was found. Generated-output currentness, publication checks and
deployment remain the coordinator's separate gates.

## Exact reviewed inputs

The review inspected the uncommitted diff against
`9ff79af29d54644d91792f4eda4d71f6fcfc2506` on
`feature/propers/codex`, after the author's explicit freeze. These hashes were
independently recomputed:

| File | SHA-256 |
| --- | --- |
| `src/sources/inventories/roman-1962-ordo-missae-v1.toml` | `07d257473c98dd67ac198f1f32351b3a189984b594a7927bd4536737a8404446` |
| `src/sources/inventories/roman-pre-1955-ordo-missae-v1.toml` | `7ef0b961804e3e69074c35739fca36606ab56bea41fcdbb818d91e9645462d07` |
| `tools/tests/test_mass_ordinary.py` | `3c22165c8d72b5d8a37d56f3fe43e1a7d825633d649d693ac1c19bddd6ae8541` |

Parsed TOML comparison proves that each inventory changes only the
`offertorium` slot's exact label list and evidence locus. Both retain the
existing anchor and a derived `qualified = false`. The validator and shared
JavaScript seating model are unchanged, as are both calendars. No translation
sidecar, seasonal fact, source record, source graph, release record or native
production input is part of this repair.

## Primary evidence checked independently

Both whole held PDFs were hashed against their canonical artifact records, then
the pages below were independently rendered and opened on 25 October 2026.

| Witness and exact PDF SHA-256 | Checked pages | Finding |
| --- | --- | --- |
| CMAA 1962 typical-edition facsimile, `648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a` | artifact 577 / printed 496; artifact 579 / printed 498 | The first page identifies the 27 March John Damascene Mass. Unit 2342 on the latter page places the base and parenthetical Paschal continuation under one `Ant. ad Offertorium` heading. Mapping the two project labels to one Offertory seat follows that source placement. |
| Tours Mame 1922 conformed printing, `9873693a2937c6a573ed050351b30c545b7464b87b06390785e504fb0aac7005` | artifact 77 / printed lxvii; artifact 673 / printed 559 | Ritus servandus VII.1 states the fixed Offertory position. The local proper page prints the base without a Paschal continuation. This check establishes neither a pre-1955 appointment of the foreign 1962 candidate nor an independently available complete Paschal body. |

Canonical manifests are the CMAA `cmaa-facsimile-pdf/artifact.toml` under
`src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/`
and the Mame `ia-scan-pdf-9873693a/artifact.toml` under the same work's
`1922-tours-mame-editio-quarta-iuxta-typicam/` edition. The Mame witness remains
a conformed 1922 printing, rather than an authenticated 1920 Vatican impression.

## Guard and regression assessment

The new tests exercise real John Damascene candidates against freshly built
Ordinary inventories. They verify the exact alias and disabled generic
qualifiers, all twelve retained candidates, the distinct tract/Paschal
conditions, and the unavailable Paschal body. The foreign test checks both
Offertory source diagnostics and unresolved markers, checks that static
validation leaves the Mass unchanged, then proves that appointment preparation,
unframed events and framed units all refuse foreign execution despite the known
structural seat.

Changing the Matthias adversary to an actually undeclared qualifier is correct:
the newly declared exact label can no longer serve as a negative control.
Its unknown and known-false conditions, cross-seat corruption and refusal
assertions remain intact.

An independent in-memory probe restored the old label list and reproduced the
original alternative-group refusal. The repaired list accepted all twelve
candidates. With the repaired inventory freshly built, both unknown conditions
and a synthetic tract regime making the Paschal option false still rejected
an undeclared Offertory qualifier and a Communion substitution. The static
validator continues to validate source candidates before any inactive-option
filter could hide an invalid seat.

## Checks actually run by this reviewer

Python used `.scratch/publication-prep/venv/bin/python`, with that virtualenv's
`bin` first in `PATH` and bytecode writes disabled.

| Check | Exit | Result |
| --- | ---: | --- |
| Five `OrdinaryTool` tests: both new John Damascene tests, Matthias inactive/unknown guards, cross-layer unknown/backward/stale guards, singleton/mixed-seat choices | 0 | 5 tests passed. |
| `PYTHONPATH=tools/tests .scratch/publication-prep/venv/bin/python -m unittest tools.tests.test_common_ordinary_gate tools.tests.test_ordinary_foreign_seat_diagnostics tools.tests.test_proper_appointment_foreign_applicability` | 0 | 23 tests passed. |
| `node tools/tests/test_foreign_static_target_seats.cjs` | 0 | All 5 guard groups passed. |
| Independent parsed-diff, baseline reproduction and rebuilt-table negative probe | 0 | Only the two intended TOML fields differ per inventory; baseline refuses, repaired candidates pass, invalid unknown/false candidates refuse. |
| Scoped `git diff --check` for the frozen three files | 0 | No whitespace defects. |

The first broad Python invocation omitted `PYTHONPATH=tools/tests` and exited 1
at an existing sibling-module import; the corrected invocation above passed.
An initial synthetic John Damascene control used `regular`, which appoints
neither of this Mass's two Offertory options and correctly refused before the
seat check. The final negative probe used `tract`, preserving an active base
while making the Paschal option false.

The author's full Ordinary check reported zero seating failures but exit 1
for two stale generated Ordinary JSON files. This review does not report that
global gate as passed or authorize bypassing it. The shared owner must refresh
those projections and the coordinator must establish currentness before
publication. No generated files, index, commits or refs were changed by this
review lane.
