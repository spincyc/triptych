# Independent review of the merged Ordinary tests

**ACCEPT** the frozen test resolution and the reviewed Ordinary context below.
No blocker was found in this lane. The coordinator retains the broader merge,
publication and deployment gates.

The earlier `deployment-blocker-cold.md` remains a historical acceptance of its
identified alias-based snapshot. Incoming main
`f3f59d483358128e1b78d7a12aaeb4f3feab4a8a` supersedes that repair: both John
Damascene alternatives now use the canonical role `Offertory`, distinguished
in the source calendar by occurrences 1 and 2. The temporary alias and expanded
loci are absent from the current Ordinary tables. This verdict does not carry
the earlier alias claim forward.

## Exact resolution reviewed

The worktree and staged `tools/tests/test_mass_ordinary.py` have identical bytes
and SHA-256
`63f6a32ffa312abd17502803183d5e46305fa8ad79ffb7cfa914ff979fc212cf`.
The diff against incoming main adds only the `Namespace` import and the two
adapted John Damascene regressions.

Independent AST comparison removed exactly those three additions and reproduced
the entire incoming module AST. All 81 upstream class methods and helpers,
their assertions, the Matthias `Tempore paschali` corruption control and the
module's harness string content are preserved. The full diff was also inspected;
no upstream test block was deleted or rewritten.

Both Ordinary inventories, both generated Ordinary JSON files,
`tools/mass-ordinary` and the shared seating implementation are byte-for-byte
equal to incoming main. Both current John Damascene generated Mass objects are
also exactly equal to their incoming counterparts. The combined calendar and
Propers JSON hashes below identify the reviewed integration context; the
separate native F02 review belongs to its assigned lane.

## Behavior and evidence boundary

The current Roman 1962 candidates retain their two occurrence identities,
non-Paschal-base and Paschal-body-gap options, tract/Paschal predicates and
unavailable complete Paschal body. Both fit the original `Offertory` seat,
whose only declared label is `Offertory` and whose generic qualifier flag
remains false. The source placement checked in the earlier review—one
Offertory heading governing the base and optional continuation—supports this
common role without requiring a label alias.

The pre-1955 projection retains the two named options and the original foreign
source basis with unresolved applicability. It deliberately carries neither
the source calendar's appointment identities nor its executable `when`
predicates into the target edition. The adapted regression independently
confirms the original foreign diagnostics, an unchanged Mass after static
validation, known structural seats, and refusal by appointment preparation,
unframed events and framed unit construction. A seat does not authorize target
execution or fill the missing body.

The preserved upstream John Damascene and Matthias negative controls reject
the undeclared `Offertory (Tempore paschali)` label and mixed semantic seats
even when the Paschal option is unknown or known inactive. Keeping the earlier
alias would defeat that intended negative control; restoring the canonical
tables is therefore required by this merged source model.

## Independent checks

All commands used the pinned publication Python with its virtualenv first in
`PATH`; bytecode writes were disabled. No generator or global source aggregate
was run.

| Check | Exit | Actual result |
| --- | ---: | --- |
| AST, staged-byte and incoming-byte comparisons | 0 | Only the two added methods/import remain beyond upstream; all six Ordinary/code files and both John Damascene Mass objects match incoming main. |
| Five targeted `OrdinaryTool` tests: both adapted regressions, both incoming John Damascene tests and the Matthias inactive/unknown guard; plus `test_ordinary_foreign_seat_diagnostics` and `test_proper_ordinary_disposition` | 0 | 21 tests passed. |
| `node tools/tests/test_foreign_static_target_seats.cjs` | 0 | All 5 guard groups passed. |
| `.scratch/publication-prep/venv/bin/python tools/tpt mass-ordinary check --json` | 0 | No stale files; 1,529 full-frame and 100 non-full forms; zero seating failures. |
| Scoped staged `git diff --check` for the test file | 0 | No whitespace defects. |

The independent Ordinary-check receipt has SHA-256
`d41b3e8a727d05912c49987ebdbd80040e844608a7722ddbd20cb29dedf91a20`,
equal to the author's reported receipt. The broader 89-test pass in
`merge-test-resolution.md` is the author's result; this reviewer independently
ran the focused 21-test set above.

The exploratory comparison initially assumed the foreign projection carried
the source's appointment identity and predicate fields. Inspection corrected
that assumption; their intentional absence matches incoming main and preserves
the foreign-applicability boundary. The corrected comparison passed.

## Reviewed identities

| File | SHA-256 |
| --- | --- |
| `tools/tests/test_mass_ordinary.py` | `63f6a32ffa312abd17502803183d5e46305fa8ad79ffb7cfa914ff979fc212cf` |
| `src/sources/inventories/roman-1962-ordo-missae-v1.toml` | `52940d1ab72eb486aa0f4add24be9ba8e5b24a7985351ac5dd3eade38764916d` |
| `src/sources/inventories/roman-pre-1955-ordo-missae-v1.toml` | `ae7b84f346e53ae27e789251033b749b791cb47e6e3deb7b0f92d56573859c88` |
| `src/web/data/structure/ordinary/roman-1962.json` | `6a131ccc5603941bc76b20159d03197315f2f2575b9bc4313e91c642faf7cf43` |
| `src/web/data/structure/ordinary/roman-pre-1955.json` | `6b2b0e9457f2a02f5d0d8d11c24f03dbd0b5cb8aa0ef797283c119f81de62938` |
| `src/sources/calendars/roman-1962/propers.yaml` | `3536021b46c88b5fc883e53319edd8c5e4ac90e906c50d630ffe35c3b192b545` |
| `src/web/data/structure/propers/roman-1962.json` | `b6dd4e9351a7f744aa9e76e7993083adc2388fdcd7271218f49237c3c06baed2` |
| `src/web/data/structure/propers/roman-pre-1955.json` | `ce7e025504c40f308e1cf8d2355ea7460d6a7f84011491b64f063cd7232d91dc` |
| `tools/mass-ordinary` | `b550fed2c641ad99f4b665597b9b5badc812ff3ce1785ea92a8ca6b30e9ee682` |
| `src/web/browser/liturgy/ordinary-seating.js` | `093bbd565d62814d8e2634e4073cc688927f4ad4470d4fee3e08bce87fef5e0f` |

No tracked file other than this new report was written by this follow-up
review. The earlier review records were preserved; no index, commit or ref was
changed by this lane.
