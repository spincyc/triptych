# GPT Twenty-first Sunday after Pentecost production

This production studies the 1962 Roman Missal formulary for 18 October 2026,
for an adult parish assembly. The source owner is
`src/gpt/liturgy/roman-rite/1962/propers/temporal/61-twenty-first-after-pentecost`.

## Bound run

| Field | Recorded value |
| --- | --- |
| Workflow | `proper-study`, version 10 |
| Run | `a72731c5491066a3` |
| Seed commit | `9c4d5e5eb1cb12bc10ceece135f344c284ff8e52` |
| Workflow digest | `692be31073c9d612d9b08b3eb086d865bc3ed25f32a26f0a50c98f0a1e65ca65` |
| Date argument | `2026-10-18` |
| Audience | `adult parish assembly` |

The preliminary source handoff supplies leads, not inherited verification or
approval. The foundation was independently reviewed and committed before the
run was seeded. Every single stage is dispatched to a fresh Codex GPT-6
worker without inherited authoring conversation: authors at `high`, cold
reviewers at `xhigh`. Workers receive the actual compiled packet and separate
scratch/result destinations; they do not delegate. The engine runs all
program gates and owns transitions, input seals, and acceptance.

## Progress

The scope gate and resolve-context iteration 0 passed. The context records the
dated mission orations and conditional St Luke commemoration, with Mass type
and local-calendar limits, rather than assuming only the ordinary Sunday
inventory. Research iteration 0 and research-preflight iteration 0 passed.
Cold research-review iteration 0 returned `CHANGES_REQUIRED`: `RES-001` requires
preserved and sealed owners for the adopted Gregory, Aquinas, and Rabanus loci;
`RES-002` requires the six actually used Catholic Encyclopedia chronology
derivatives and governing rights inventory in the seal. Research iteration 1
and its real preflight gate passed after repair. Before dispatching the fresh
`xhigh` reviewer at iteration 1, the driver verified the 48 requested repair
path/hash entries and 12 omitted-payload/manifest checks against the actual
compiled packet. All 60 checks matched, and all 1,738 sealed files matched
current bytes. This proves dispatch integrity, not research acceptance. Cold
review iteration 1 then returned actual `PASS`, with no blocking findings.
The engine accepted that result, cleared the standing research findings, and
compiled `author-study-0000`. Author dispatch is held for the coordinator's
accepted-research checkpoint commit.

After the engine-owned findings update, publication inventories and the
source-family ledger were refreshed. Source-inventory, source-family
migration, publication-inventory validation, and whitespace checks passed.
All 1,738 research-sealed files plus 13 chronology computation inputs still
match their accepted hashes. The review preserved its scoped limits: newly
retained sources are checked digital transcriptions and derivatives, not new
print-facsimile collations, and no rendered publication was under review.

The research worker completed source-specific validation, publication source
inventories, source-family ledger, containment and commentator inventories,
source-reader rights/projection checks, and both chronology currency checks.
The aggregate `make check-sources` stops at the new owner's missing downstream
`web-edition.toml`; the publication declaration belongs to later authoring, so
this is recorded as an incomplete aggregate check, not bypassed or called a
pass.

Research corrected the Mame St Luke Secret locator from printed page 726 /
PDF page 840 to printed page 739 / PDF page 853; no prior publication bound
that passage. It also corrected only the comparison note in row 6 of the
Cummiskey preface TSV: both checked Cummiskey and 1962 images read `Quam`.
The historical English is unchanged. The two existing consumers' source
fingerprints and context notes were updated after the coordinator's narrow
impact review in `workflows/reviews/propers-quality-2026-10-12/SOURCE-IMPACT.md`;
their historical evidence states, dates, and archived approvals are unchanged.

A reported Exodus orientation defect was retracted after inspection: the
visible `orientation-v1` arguments correctly identify Temple construction as
the interval endpoint. Raw source labels and legacy detailed prose are
distinct from those displayed rows. No chronology data, dates, or workflow
code were changed for that report.

The authoritative active run is under `build/tpt-runs/a72731c5491066a3/`.
The `run-a72731c5491066a3/` checkpoint archive retains its actual packets,
results, untouched gate logs, input seals, and current nonterminal state.
Its manifest identifies exact originals and one explicitly labeled auxiliary
public derivative that omits only a native process identifier; original local
evidence is untouched. The native verdict and packet remain byte-exact. The
archive will be extended through actual terminal disposition. No verdict or
state is manufactured or edited by the driver.
