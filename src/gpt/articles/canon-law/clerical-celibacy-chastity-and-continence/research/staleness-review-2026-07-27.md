# Staleness review — 2026-07-27

## Exact trigger

`scripts/research-staleness explain gpt
articles/canon-law/clerical-celibacy-chastity-and-continence` reported exactly
two new inputs:

- `src/sources/works/catholic-church/catechism/editions/english-vatican-web-2026-07-23/artifacts/eucharist-opening-html-ab7990d1/artifact.toml`
- `src/sources/works/catholic-church/catechism/editions/english-vatican-web-2026-07-23/passages/1322-1323.toml`

The article binds that Catechism edition only at paragraphs 2337--2350 and
1577--1580. The new artifact and passage concern paragraphs 1322--1323 on the
Eucharist. Their appearance in `explain` follows the edition-level input rule;
it does not make those paragraphs evidence for this article.

## Candidates

- Minimal modification:
  `build/staleness/gpt/articles/canon-law/clerical-celibacy-chastity-and-continence/modified/main.tex`
  with its complete copied `sections/` tree.
- Research-first rewrite:
  `build/staleness/gpt/articles/canon-law/clerical-celibacy-chastity-and-continence/rewritten/treatment.md`.

The minimal candidate is byte-identical to the current source because importing
an unrelated Eucharistic passage would create a false evidentiary connection.
The rewrite was organized from the governing research claims and treats the new
passage only to test its relevance.

## Consequential-claim comparison

| Claim | Old | Modified | Rewritten | Effect of changed research |
|---|---|---|---|---|
| Chastity, continence, and celibacy are distinct | States the distinctions and their juridical consequences. | Unchanged. | Reconstructs the same distinctions. | None; Catechism 1322--1323 addresses the Eucharist, not these terms. |
| Priesthood does not by sacramental nature require celibacy | Preserves both theological fittingness and disciplinary mutability. | Unchanged. | Reaches the same bounded conclusion. | None. |
| Early discipline was neither simply uniform nor a late arbitrary invention | Preserves married ministry, fourth-century Western continence law, divergent settlements, and the disputed apostolic-continence thesis. | Unchanged. | Reconstructs the same calibrated history. | None. |
| Current Latin law ordinarily selects celibate presbyters while admitting defined married clergy | Distinguishes admission, celibacy, continence, impediment, loss of state, and dispensation. | Unchanged. | Reaches the same legal result. | None. |
| Canon 277 and married permanent deacons remain an unresolved interpretive question | States the located norms and absence of a settling authentic interpretation. | Unchanged. | Preserves the unresolved status. | None. |
| Eastern common law honors both celibate and married clergy | Separates common-law capacity from particular-law implementation. | Unchanged. | Reaches the same jurisdictionally bounded result. | None. |
| Marriage before orders differs from attempted marriage after orders | Preserves both codes' impediment and the need for competent authority in concrete cases. | Unchanged. | Reaches the same conclusion. | None. |
| Spousal consent does not ordain the wife or erase marital rights | States the family and pastoral boundaries. | Unchanged. | Preserves them. | None. |
| Concrete cases are not decided by the article | Refers fact-dependent cases to competent authority or a qualified canonist. | Unchanged. | Preserves the referral. | None. |

## Candidate disagreement

The rewrite is shorter and reorganizes the material by controlling legal
question rather than reproducing the article's historical sequence, tables, and
apparatus. It disagrees with neither the old paper nor the minimal candidate in
substance. The changed research adds no evidence within the article's bound
loci and does not strengthen, weaken, remove, or contradict any consequential
claim.

## Verdict

**No material change.** The current publication should remain unchanged. The
minimal candidate is preferable because it preserves the full audited argument
and source qualifications; the rewrite confirms the same conclusions but
offers no evidentiary improvement. This review does not rebaseline the shared
ledger and does not alter the publication.
