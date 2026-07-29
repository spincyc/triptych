# Staleness Review — 2026-07-29

Edition: `gpt/liturgy/roman-rite/1962/propers/temporal/19-fifth-after-pentecost`

Command reviewed:

```text
scripts/research-staleness explain gpt liturgy/roman-rite/1962/propers/temporal/19-fifth-after-pentecost
```

## Changed inputs

The command reports sixteen new passage records:

- Augustine, *City of God* 9.2, in the retained Dods 1871 edition.
- Thirteen 1962 Missal records concerning the Sunday holy-water order,
  pontifical tunicle and dalmatic, acolyte candlesticks, altar/tabernacle/
  images, chalice and paten preparation, the Communion plate, incense boat
  and spoon, Offertory lavabo, sacristy preparation, thurible service, altar
  preparation, and lavabo articles.
- Two 2002 Missal records: the Eighteenth and Twenty-sixth Sundays in
  Ordinary Time.

The records entered the dependency set through broadly bound reusable edition
records. None is at a locus named in this leaf's
`research/source-bindings.toml`: the Augustinian binding is *City of God*
10.5–6, and the 1962 Missal binding is the Fifth Sunday formulary at printed
pages 383–384.

## Three-way per-claim comparison

| Consequential claim family | Old edition | Modified candidate | Research-only rewritten candidate | Effect of changed research |
| --- | --- | --- | --- | --- |
| Formulary identity and appointed elements | Treats the ten appointed propers from the 1962 Fifth Sunday after Pentecost formulary. | Retains it unchanged. | Makes no replacement claim because the changed records contain no evidence for this formulary. | No addition, removal, strengthening, weakening, or contradiction. |
| Direct and adapted biblical text | Distinguishes direct excerpts from Psalms 15, 20, and 26, Matthew 5, and 1 Peter 3 from the Gradual's adaptation of Psalm 83. | Retains it unchanged. | Makes no replacement claim. | No changed record addresses these passages or the Gradual adaptation. |
| Historical coordinates | Qualifies Psalm attribution and dating, Matthew's composition and narrated event, and 1 Peter's authorship, audience, place, and date. | Retains it unchanged. | Makes no replacement claim. | No historical-orientation source changed. |
| Reconciliation and peace | Reads the Epistle and Gospel through blessing, truthful peace, remembered grievance, initiative, safety, and unequal culpability. | Retains it unchanged. | Makes no replacement claim. | Augustine 9.2 concerns demonic mediation, not the appointed texts or interpersonal reconciliation. |
| Ordered love and sacrifice | Uses Augustine's ordered-love teaching and *City of God* 10.5–6 as bounded illumination of Collect and Secret. | Retains it unchanged. | Makes no replacement claim. | The new 9.2 record neither revises nor contradicts 10.5–6; it addresses a distinct argument. |
| Psalmic desire and liturgical synthesis | Relates the sought face, one house, servant petitions, received royal joy, offering, and post-Communion need. | Retains it unchanged. | Refuses to synthesize unrelated evidence. | General sanctuary records do not establish the Sunday's particular textual synthesis. |
| Patristic, medieval, and later reception | Uses checked Augustine, Chrysostom, Bede, Jerome, and Anthony at identified loci. | Retains it unchanged. | Makes no replacement claim. | No retained reception locus changed. |
| Notable afterlives and exploratory proposals | Documents three cultural afterlives and five bounded multi-proper proposals. | Retains them unchanged. | Makes no replacement claim. | None of the new records adds or disconfirms an afterlife or proposal precedent. |

## Candidate comparison

The modified candidate is a deliberate no-op: minimal incorporation requires
no source or prose change.

The rewritten candidate was produced through a two-stage boundary. First, an
evidence packet was made solely from the sixteen paths emitted by `explain`.
Second, the candidate was drafted solely from that packet, without using the
old guide as a prose model. Because the changed evidence contains no material
about this Sunday, the rewrite declines to fabricate a replacement. Its
silence is evidentiary restraint, not substantive contradiction.

Ignored candidates:

- `build/staleness/gpt/liturgy/roman-rite/1962/propers/temporal/19-fifth-after-pentecost/modified/candidate.md`
- `build/staleness/gpt/liturgy/roman-rite/1962/propers/temporal/19-fifth-after-pentecost/rewritten/research-evidence.md`
- `build/staleness/gpt/liturgy/roman-rite/1962/propers/temporal/19-fifth-after-pentecost/rewritten/candidate.md`

## Verdict

**No material change.** The stale flag reflects new records elsewhere in
broadly bound editions, not changed evidence for the Fifth Sunday after
Pentecost. Retain the installed edition. Per the assigned scope, no rebaseline
was run and the tracked staleness ledger was not touched.
