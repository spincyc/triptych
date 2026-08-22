# Staleness review — 2026-07-29

## Edition and provider coverage

- Leaf: `liturgy/roman-rite/1962/propers/temporal/41-fourth-after-pentecost`.
- Edition reviewed: GPT.
- Other-provider edition: none. The staleness tool reports no Claude edition
  for this leaf, so no other-provider research or publication claims enter the
  comparison.
- Reusable inputs: the GPT bindings include the 1962 Missal witnesses and a
  bounded *City of God* 19.13 analogue, together with its edition/corpus
  records.

## Exact changed inputs

`scripts/research-staleness explain` reported sixteen new inputs:

- Augustine, *City of God* 9.2 in the Dods 1871 edition;
- thirteen 1962 Missal records concerning the Asperges, sacristy and altar
  preparation, candlesticks, pontifical vesture, chalice and paten,
  Communion plate, incense implements and service, the Offertory Lavabo,
  tabernacle and images, and related general rubrics; and
- two 2002 Missal records, for the Eighteenth and Twenty-sixth Sundays in
  Ordinary Time.

The Augustine passage rejects the proposal that supposedly good demons should
be cultivated as mediators to blessedness. It does not concern the
peace-as-order definition in *City of God* 19.13, the Collect, any appointed
passage, or any cultural or interpretive claim in this guide. The Missal
records belong to other rites, objects, rubrics, editions, and formularies.

## Candidate treatments

- Modified:
  `build/staleness/gpt/liturgy/roman-rite/1962/propers/temporal/41-fourth-after-pentecost/modified/`.
  It is an in-place copy because the applicable incorporation is null.
- Rewritten:
  `build/staleness/gpt/liturgy/roman-rite/1962/propers/temporal/41-fourth-after-pentecost/rewritten/`.
  Its compact independent `main.tex` was drafted from the research records
  and changed-input set without reusing the current exposition.

Both trees are ignored comparison artifacts and neither is proposed for
installation.

## Consequential-claim three-way comparison

| Consequential claim or control | Changed-research effect | Old edition | Modified candidate | Rewritten candidate | Substantive disagreement |
| --- | --- | --- | --- | --- | --- |
| 1962 formulary identity, rank, ten elements, pp. 382–383 | None | Retained and collated | Same | Retains identity compactly | None |
| Latin textual control and secondary witness boundary | None | Vatican typical edition controls; Benziger is analogue | Same | Proposes no textual variant | None; rewrite is less complete |
| Seven directly appointed biblical dossiers | None | Five psalm, Luke, and Romans dossiers | Same | Names the same seven | None |
| Davidic psalms: inherited attribution versus unrecoverable modern dates/sites | None | Distinction explicit | Same | Distinction explicit | None |
| Psalm 78: personal Asaphic attribution versus later communal/Babylonian horizon | None | Alternatives preserved | Same | Alternatives preserved | None |
| Luke composition versus narrated-event date and geography | None | Achaian/early tradition, modern AD 80–90 judgment, and Galilean event distinguished | Same | Preserves the distinction | None |
| Pauline Romans, Roman recipients, Corinth, c. AD 57 | None | Retained | Same | Retained | None |
| Augustine's direct appointed-psalm exegesis | None | Five exact psalm loci retained | Same | Preserves witness role | None |
| Chrysostom on Romans 8 and Cyril/Ambrose on Luke 5 | None | Direct reception retained | Same | Preserves witness roles | None |
| *City of God* 19.13 illuminates the Collect's ordered peace but is not direct commentary | 9.2 is topically distinct and neither strengthens nor weakens 19.13 | Exact boundary explicit | Same | Exact boundary explicit | None |
| Related illumination by Irenaeus, Augustine, Chrysostom, and other retained witnesses | None | Roles bounded | Same | Summarized without role inflation | None |
| Source-grounded movement from light/order and travail to mercy, command, purification, and protection | None | Developed across the guide | Same | Independently reaches the same restrained movement | None |
| Three notable cultural afterlives | None | Verified gallery retained | Same | Omitted | No contradiction; omission makes rewrite inferior |
| Five exploratory cross-element proposals | None | Labeled and controlled | Same | Omitted | No contradiction; omission makes rewrite inferior |
| Rights, research limits, and terminal apparatus | None | Full apparatus retained | Same | Candidate-purpose disclosure only | No contradiction; rewrite is not publishable |

No consequential claim is added, removed, strengthened, weakened, or
contradicted by the changed research. The modified candidate is substantively
identical to the old edition. The independent rewrite concurs on the central
textual, historical, reception, and synthesis judgments; its shorter scope
loses completeness but reveals no corrective evidence.

## Verdict

**No material change.** The new *City of God* chapter is a neighboring passage
under a broadly bound edition/corpus but is irrelevant to the leaf's sole
*City of God* use at 19.13. The other additions are unrelated Missal records.
The current GPT edition should remain installed.

Per assignment, this review does **not** rebaseline the edition, alter the
tracked ledger, install a candidate, rebuild the publication, or change its
catalog or web edition.
