# Saint Robert Bellarmine — staleness review

Date: 2026-07-29
Edition: `claude:biographies/saint-robert-bellarmine`

The sibling GPT edition was fresh and was not re-evaluated. This record
preserves, and does not replace, the Claude edition's 2026-07-26 review in
`scope.md`.

## Explain inputs

`scripts/research-staleness explain claude
biographies/saint-robert-bellarmine` reported these new inputs:

- `src/sources/works/holy-see/acta-apostolicae-sedis/editions/volume-49-1957/edition.toml`;
- `src/sources/works/holy-see/acta-apostolicae-sedis/editions/volume-49-1957/artifacts/vatican-ocr-pdf-6cfd31d7/artifact.toml`; and
- `src/sources/works/holy-see/acta-apostolicae-sedis/editions/volume-49-1957/passages/p-91-95.toml`.

These records identify the official 1957 volume of *Acta Apostolicae Sedis*,
the restricted Vatican OCR PDF artifact, and verified printed pp. 91–95. The
passage contains the Sacred Congregation of Rites' *Ordinationes et
declarationes circa Ordinem hebdomadae sanctae instauratum*, dated 1 February
1957. It governs amendments concerning restored Holy Week, does not name
Bellarmine, and is explicitly distinguished from the 1957 *Ritus
Pontificalis*.

## Candidate comparison

A complete rewrite was drafted from the Claude research records and changed
inputs before the current publication prose was consulted. The modified
candidate then tested minimal incorporation against the current publication.
Because the changed passage supplies no Bellarmine evidence, the honest
minimal candidate was text-identical to the current publication; adding the
Holy Week act would introduce irrelevant liturgical history.

The old, modified, and rewritten treatments agree in substance on every
consequential claim:

- identity, family, Jesuit entry, formation, Louvain teaching, and the 1570
  ordination sequence;
- the Roman College chair, staged publication of the *Disputationes*, the
  unpromulgated 1590 Index episode, and the Clementine Vulgate controversy;
- catechisms, cardinalate, the bounded Bruno record, the non-resolution of
  *De auxiliis*, Capua, and the 1605 conclaves;
- the Venetian and English controversies and the historical limits of the
  indirect-power doctrine;
- the 1611–1616 Galileo documents, including the distinction among the
  qualifiers' censure, papal direction, unsigned minute, Bellarmine's report,
  Index decree, and certificate, together with the bounded 1633 reception;
- the chronology and genres of Bellarmine's writings, his death, process-based
  funeral memory, and the cause's contested delay;
- beatification, canonization, Doctor title, feast history, current
  17 September optional memorial, Capua patronage, relic limits, and unverified
  broader patronage or incorruption claims; and
- evidence-class, rights, currentness, and review ceilings.

The rewritten candidate differs in compression, order, and quotation, not in
the truth conditions or evidentiary ceilings of these claims. The 1957 Holy
Week act adds, removes, strengthens, weakens, and contradicts none of them. In
particular, it is not a Bellarmine feast or General Roman Calendar act and does
not affect the current-memorial claim.

## Verdict

No material publication correction was found. The changed records are an
adjacent *AAS* edition surfaced through the source dependency model, not a
source for this biography. No publication source or installed PDF should be
replaced on this evidence.

The ignored candidates and detailed comparison were retained under
`build/staleness/claude/biographies/saint-robert-bellarmine/` for this working
review. No ledger change or rebaseline was performed.
