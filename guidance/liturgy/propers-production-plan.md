# Propers Production Plan

This is the maintainer's record of one decision — that the two Roman Rite
propers collections are **closed** — and of how to find out what they actually
contain. It is not a catalog, not a queue, and not a publication commitment.

Reader-facing catalogs under `library/` list published works only. This file is
the maintainer view and is deliberately not mirrored there.

## Authority

Nothing here originates an identity, key, slug, order, count, owner path, or
occurrence rule. Those live where they are derived:

| What you want | Where it is owned |
| --- | --- |
| Postconciliar identities, formula keys, slug grammar, canonical order, Lectionary locators, target counts, the `PC-R08` fork | [the postconciliar proper registry](postconciliar-propers-registry.md) |
| The reusable postconciliar guide architecture | [the postconciliar proper profile](postconciliar-propers.md) |
| The 1962 `01`–`68` temporal spine, `64`–`67` (resumed Sundays), and the `F`/`M` prefixes | [the 1962 proper-guide profile](roman-1962-propers.md) |
| Edition-locale adoption, dispositions, and dated occurrence results | the selected edition's `propers/registry/` records |
| Leaf paths, the canonical-plus-`-synthesis` publication pair, catalog rules | [the repository contract](../repository.md) |

Where any of those revises, it controls and this file follows. An earlier
revision of this file reproduced all of it — 60 parent rows, 184 queue rows, 52
temporal rows, the replacement matrix — and the copies had already begun to
disagree with the tree they described. The tables are gone for the reason §2 of
[the shape](../the-shape.md) gives: a hand-written table beside a derived one is
not documentation, it is a second source of truth, and the wrong one is the one
being read.

## Scope boundary

The propers collections are **bounded at the set already published**. The
maintainer closed them on 2026-07-25. Each provider brings its published propers
to the current profile — English, two editions apiece — and authors no further
calendar targets. The reference works, ordinaries, and the comparative study are
outside this boundary and continue.

On 2026-08-19 the maintainer reopened this boundary for exactly three Claude
targets: the 1962 temporal guides `51`–`53`, the Eleventh through Thirteenth
Sundays after Pentecost, authored to the current componentized profile. On
2026-08-20 the maintainer independently reopened the same three identities for
GPT. Each provider target is a full target — canonical leaf, synthesis
companion, web edition, and release records. No other identity becomes a target
by either decision, and the collections otherwise remain closed as recorded
above.

On 2026-08-26 the maintainer reopened this boundary once more, for the single
1962 temporal identity `54`, the Fourteenth Sunday after Pentecost, for both
Claude and GPT, authored to the current componentized profile. Each provider
target is a full target on the same terms as `51`–`53`. No other identity
becomes a target by this decision, and the collections otherwise remain closed.

The permanent identities in the registry and the profile remain complete and
fixed, because an identity may never be reassigned and a future maintainer must
be able to place any guide that does get written. They are **not** a queue, and
an identity with no guide is the normal state of this collection, not debt.

The reasoning is kept because the pressure to resume will recur. The fixed
inventory runs to roughly five hundred targets, which the canonical-plus-synthesis
pair doubles; at the depth these guides are authored to, that is not a backlog
but an asymptote, and the marginal value of the four-hundredth Sunday guide is a
small fraction of the first. A library that can be finished is worth more than
one that cannot.

### Authorized targets

Each line below records one maintainer decision to open the boundary for
one provider and one permanent identity. A line is the whole
authorization: it opens that provider's target and nothing else — not the
other provider, not a neighbouring identity, not the series it belongs
to. A permanent identity in the registry is not itself an authorization,
and an identity with no line here is closed.

- Authorized 2026-08-27: provider `claude`, identity `liturgy/roman-rite/1962/propers/temporal/54-fourteenth-after-pentecost`.
- Authorized 2026-09-03: provider `gpt`, identity `liturgy/roman-rite/1962/propers/temporal/55-fifteenth-after-pentecost`.
- Authorized 2026-09-05: provider `gpt`, identity `liturgy/roman-rite/1962/propers/temporal/56-sixteenth-after-pentecost`.

## How to find out what exists

**Derive it; do not read it from a table here.** What each provider has
published moves whenever a leaf lands, and a status table in a guidance file is
stale the hour after it is written.

```sh
tools/document-library list --section liturgy            # every leaf, both providers
tools/document-library list --section liturgy --provider claude
```

A leaf's release state is its own record at
`release/publications/<provider>/<leaf-id>.json`; the path below the provider
mirrors the leaf ID. A leaf directory under `src/<provider>/` with no such
record is authored but not released.

**`release/public-alpha.json` is not where publication ids live, and reading it
for one is the mistake this section replaced.** At schema version 2 that file
holds the site authorization, the rights record, and the hashes of the
reader-facing sources; per-publication state was moved out to the independently
writable records above. A previous revision of this plan derived every provider
cell in every table from the old shape, so those cells reported `not started`
against leaves that were released, and reported one provider's synthesis
published where that provider had no leaf at all. Nothing failed; the tables
simply answered, and answered wrongly.

## What was checked, and when

On the revision that carried the tables, every count in them was recomputed from
the registry's own per-parent key lists and agreed with the registry's stated
totals, including all 96 `PC-S28`–`PC-S59` Lectionary cells recomputed
independently with the registry's formula. **No disagreement was found in the
counts** — the defect was never arithmetic, it was that the same numbers were
being held in two files. The registry states them; read them there.

Two claims that revision made about its own sources were false and are recorded
so they are not made again:

- It said the 1962 profile "does not print" the 68-item temporal enumeration and
  that this plan therefore reconstructed it. The profile prints the complete
  banded registry; there was nothing to reconstruct.
- It said the two profiles define a study edition at the bare id and a full-text
  edition at `<id>-full-text`. No `-full-text` leaf, PDF, or release record has
  ever existed. The pair that was actually built is the canonical leaf and its
  mechanical `-synthesis` companion, compiled through `proper-components.toml`
  and owned by [the repository contract](../repository.md).

## Counting rule

Registry counts are counts of **targets**. A target is one canonical leaf and,
where its manifest authorizes one, one derived `-synthesis` companion — one
identity, one owner, one research trail, one set of source bindings. A target is
not finished when only the canonical PDF exists, and the companion is never a
second target.

The English requirement is retrospective. Every proper published before it was
authored under the previous rule, which printed the appointed Latin in full and
supplied no English. Those leaves are superseded in form, not in research: their
collation findings, reception matrices, and commentary stand, and a rebuild
carries them forward rather than repeating the work. Each provider reissues its
own leaves.

## Maintenance

Correct this file when the scope boundary itself changes. Do not restore a
status table, a target enumeration, or a count that the registry or a profile
already states — the derivation above is the whole mechanism, and adding a
second one recreates the defect this revision removed.
