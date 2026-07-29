# Staleness Review — 2026-07-29

Edition: `gpt/liturgy/roman-rite/1962/propers/ritual/m01-nuptial-mass`

Command reviewed:

```text
scripts/research-staleness explain gpt liturgy/roman-rite/1962/propers/ritual/m01-nuptial-mass
```

## Changed inputs

The command reports 26 new passage records:

- Catechism (USCCB second edition, 2019): 270; 277; 391–395; 550;
  1667–1673; 1700–1706; 1734–1735; 1857–1859; 2111; 2116–2117; and
  2846–2854.
- 1962 Missal: the Sunday holy-water order; pontifical tunicle and dalmatic
  prayers and rubrics; acolyte candlesticks; altar, tabernacle, and images;
  chalice and paten preparation; Communion plate; incense boat and spoon;
  Offertory lavabo; sacristy preparation; thurible service; altar
  preparation; and lavabo articles.
- 2002 Missal: the Eighteenth and Twenty-sixth Sundays in Ordinary Time.

The records entered the dependency set because this edition binds reusable
edition records broadly. None is at a locus named in this leaf's
`research/source-bindings.toml`.

## Three-way per-claim comparison

| Consequential claim family | Old edition | Modified candidate | Research-only rewritten candidate | Effect of changed research |
| --- | --- | --- | --- | --- |
| Formulary identity and rank | Identifies the 1962 `Pro sponsis` Mass as a white votive Mass of II class. | Retains it unchanged. | Makes no replacement claim because the changed records contain no `Pro sponsis` evidence. | No addition, removal, strengthening, weakening, or contradiction. |
| Admission and exclusion | Explains General Rubrics 378–381, including closed time, Sundays, impeded formularies, transfer, and the inseparability of the blessing from Mass absent indult. | Retains it unchanged. | Makes no replacement claim. | No changed record addresses nn. 378–381. |
| Gloria, Creed, Preface, and conclusion | Explains the appointed Gloria, normally omitted Creed, seasonal/Common Preface, and complete end sequence. | Retains it unchanged. | Makes no replacement claim. | General ceremonial records do not change the leaf's bound rubrics 341–343, 482, 484–490, 493–494, 498, or 507–509. |
| Appointed proper texts and biblical movement | Treats Tobit, Psalms 19/30/127/133, Matthew 19, Ephesians 5, the orations, blessing, Communion rubric, and admonition. | Retains it unchanged. | Makes no replacement claim. | No changed record supplies or revises an appointed text or its biblical context. |
| Matrimony doctrine and canonical qualifications | Distinguishes the historical formulary from current doctrine and law and uses bound Catechism loci on Matrimony. | Retains it unchanged. | Makes no replacement claim. | The new Catechism loci concern other topics and do not alter the bound Matrimony loci. |
| Patristic, medieval, scholastic, and later reception | Uses checked reception of the appointed passages and marriage doctrine. | Retains it unchanged. | Makes no replacement claim. | No reception source changed. |
| Source-grounded synthesis and exploratory proposals | Synthesizes Creator, self-gift, household/Sion, peace, and bounded cross-proper proposals. | Retains it unchanged. | Refuses to synthesize unrelated evidence into a Nuptial claim. | No substantive disagreement; the rewrite's silence is evidentiary restraint, not contradiction. |
| Sacramental appendix | Imports the canonical Matrimony summary with its own evidence dependency. | Retains it unchanged. | Makes no replacement claim. | None of the new records changes the summary's named Matrimony controls. |

## Candidate comparison

The modified candidate is a deliberate no-op: it records why minimal
incorporation requires no prose change.

The rewritten candidate was produced through a two-stage boundary. First, an
evidence packet was made solely from the 26 paths emitted by `explain`.
Second, the candidate was drafted solely from that packet, without using the
old guide as a prose model. Because the changed evidence contains no Nuptial
Mass material, the rewrite responsibly declines to fabricate a replacement.
Its difference from the old edition is absence of claims, not a substantive
contradiction.

Ignored candidates:

- `build/staleness/gpt/liturgy/roman-rite/1962/propers/ritual/m01-nuptial-mass/modified/candidate.md`
- `build/staleness/gpt/liturgy/roman-rite/1962/propers/ritual/m01-nuptial-mass/rewritten/research-evidence.md`
- `build/staleness/gpt/liturgy/roman-rite/1962/propers/ritual/m01-nuptial-mass/rewritten/candidate.md`

## Verdict

**No material change.** The staleness is dependency-graph churn from new
passage records elsewhere in broadly bound editions, not changed evidence for
this guide. Retain the installed edition. Per the assigned scope, no
rebaseline was run and the tracked staleness ledger was not touched.
