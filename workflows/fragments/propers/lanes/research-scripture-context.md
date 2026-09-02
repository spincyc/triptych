# Lane: Scriptural Context

## Your lane

You own the Scriptural context of the appointed passages, and nothing else.
Another lane owns reception, liturgical history, theological synthesis, and
source coverage; do not report on theirs. You are read-only, as the shared
fragment above states: your only product is your returned result.

Read each directly appointed biblical passage in its complete literary
context, and collate:

- the immediate context of each passage — its literary unit, its argument
  or narrative, and what the appointed excerpt carries in from it
- cross-references that materially bear on the appointed wording
- typological and canonical relationships relevant to this proper
- textual relationships among the appointed proper elements themselves,
  where those relationships are grounded in the Scriptural text rather than
  in later interpretation

Keep textual observation distinct from synthesis: when a relationship is
your inference rather than something the text states, say so in `notes`.
Do not assert an association the appointed texts do not support, and do not
settle what the author should finally draw from one.

## When a passage was written, and when what it tells of happened

You do not research this. `guidance/scripture-chronology.md` §14: a proper
that needs biblical chronology MUST read the corpus at
`src/sources/chronology/` and MUST NOT independently infer, research,
harmonize, or assign a replacement biblical date. `resolve-context` has
already read it for this formulary and written the answer to
`src/{provider}/{proper}/research/chronology.toml`; read that file, and run

```
tools/tpt proper-chronology loci --document {proper}
```

if you want the same answer straight from the corpus. Report a date only as
the corpus states it, in the source's own `label` and never the normalized
`date`, and carry the `subject`, `relation` and `profile` beside it in your
finding so that the author can print it without asking again.

Where the corpus's status is `undated-in-tradition` or `research-pending`, or
where it answers with no assertion, **the finding is that absence**, and it is
reported at the extent the corpus records, not as plain silence. Do not close
it from a commentary, a chronological table, a superscription you have read
as a date, or your own recollection. A date is a well-formed integer, so a
wrong one reads exactly like a right one; a lane that supplies one has put a
second source of truth into a brief the author cannot check it against, and
`content-preflight` will refuse the leaf that prints it.

A source that dates a passage is still worth a finding — as reception, about
what that source says, attributed to it, and never restated as the date of the
passage.

## Result

Return a research result for this lane, per the shared contract above.
`PASS` when your sweep completed, `BLOCKED` when something stopped it.

Finding IDs must use the `SCR-` prefix and be stable across iterations.
