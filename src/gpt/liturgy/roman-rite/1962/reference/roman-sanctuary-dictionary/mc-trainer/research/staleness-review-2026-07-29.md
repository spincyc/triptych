# Staleness review — 2026-07-29

## Exact trigger and candidates

`scripts/research-staleness explain gpt
liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/mc-trainer`
reported exactly one changed input:

- `src/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/mc-trainer/research/guide-map.md`

The added paragraph records a publication-apparatus decision: the title page
now carries only the terse `Alpha` status; bounded inventory, 1962 horizon,
non-authority, and reliance qualifications appear once in the terminal Scope
and Qualifications appendix; and the common rights notice shares the final
generation-metadata page.

Both required ignored candidates were produced:

- `build/staleness/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/mc-trainer/modified/main.tex`
  is an exact copy of the current source because minimal incorporation changes
  no rendered claim or already-settled apparatus behavior.
- `build/staleness/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/mc-trainer/rewritten/treatment.md`
  independently reconstructs the audience boundary, plate selection,
  object-status controls, withheld matter, and terminal apparatus from the
  edition and family research.

The installed PDF was checked directly. It is ten pages, 18,057,940 bytes,
and has SHA-256
`a142ea35c553312d57aef8718315cec42d33a36f48dd201ce0fe8c8743dde63a`,
matching the current row in the series production manifest.

## Consequential-claim comparison

| Consequential claim family | Old publication | Modified candidate | Research-first candidate | Effect of changed input |
| --- | --- | --- | --- | --- |
| Alpha and reliance boundary | Terse Alpha status; bounded 1962 study reference, not an official book or local direction | Identical | Same status and boundary, consolidated terminally | Clarifies where existing qualifications are printed; adds no authority or approval. |
| Audience and selection | Curates required or useful canonical records for MCs and trainers | Identical | Reconstructs the same audience-controlled selection | None; no admission or omission record changed. |
| Object identity and status | Distinguishes universal, conditional, institutional, practical/local, and unresolved states | Identical | Preserves each status class | None; no canonical record changed. |
| Assignments and relationships | Prints only checked giver, receiver, use, placement, and handler relationships | Identical | Retains the same claim-level restriction | None; the apparatus paragraph neither adds nor removes a handoff, cue, route, or assignment. |
| Morphology and artwork | Treats drawings as controlled recognition aids and exemplar forms, not ceremonial evidence or universal morphology | Identical | Preserves exemplar and TeX-label controls | None; no artwork or material-culture input changed. |
| Altar, linen, Lavabo, incense, cruet, vessel, book, torch, and cross plates | Presents the admitted objects with their stated distinctions and safety limits | Identical | Reconstructs the same plate families and limits | None; no identity, use, relationship, handler, or safety claim is strengthened, weakened, removed, or contradicted. |
| Holy-water and canopy branches | Limits sprinkler relations to the checked Asperges locus and keeps conopaeum and Eucharistic ombrellino institutionally and ceremonially distinct | Identical | Retains the same bounded branches | None. |
| Sacristy lavatory | Withholds a pictorial form pending a checked exemplar and forbids invented equivalences or assignments | Identical | Retains the same withholding decision | None. |
| Rights and generation disclosure | Terminal publication apparatus carries the common rights notice and compact revision information | Identical | Places the same material terminally | The changed input strengthens the audit trail for placement only; it does not alter rights status or content. |

The old publication and modified candidate agree in wording and substance.
The research-first candidate differs in organization and compression but
reaches the same object identities, statuses, audience relationships, safety
limits, omissions, and reliance boundary. The candidates have no substantive
disagreement with the old publication.

## Verdict

**No material change.** The changed guide-map paragraph documents the already
rendered location and economy of the Alpha, scope, rights, and generation
apparatus. It adds, removes, strengthens, weakens, or contradicts no
consequential dictionary claim. Replacing the publication would offer no
evidentiary, visual, or training improvement.

No installed PDF, web edition, catalog, release record, source binding,
canonical object record, artwork, or plate was changed. The shared staleness
ledger was not rebaselined.
