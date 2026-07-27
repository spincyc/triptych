# Staleness Review — 2026-07-27

## Exact explanation

`scripts/research-staleness explain claude
articles/canon-law/clerical-celibacy-chastity-and-continence` reported nine new
inputs:

- CCC English edition: artifact `eucharist-opening-html-ab7990d1` and passage
  `1322-1323`;
- CIC 1917 Vatican Polyglot edition: artifact `leaf-384-image` and passages
  `canon-1151`, `canon-1152`, and `canon-1153`;
- CIC 1983 Latin Vatican web edition: passage `canon-1172`; and
- Council of Trent, Tauchnitz 1887 Latin edition: passages
  `sessio-13-canon-1-11` and `sessio-13-decretum-1-5`.

These became inputs because the Claude leaf already binds other loci within
the same reusable editions. The new CCC and Trent records concern the
Eucharist. The new CIC records concern exorcism. None changes the identity,
text, or verification state of a locus used by this article.

## Candidates

- `build/staleness/claude/articles/canon-law/clerical-celibacy-chastity-and-continence/modified/`
  is an exact copy of the current source. Minimal incorporation produces no
  rendered change because none of the changed inputs bears on a claim.
- `build/staleness/claude/articles/canon-law/clerical-celibacy-chastity-and-continence/rewritten/rewrite.md`
  is a complete fresh treatment drafted from the research records. It covers
  the three-term distinction; CIC 277 and attachment, impediment, penalty,
  loss-of-state, and dispensation rules; Eastern common law and the Churches
  *sui iuris*; the permanent-diaconate dispute; historical development;
  convert clergy; modern teaching; arguments; and legal qualifications.

The rewritten candidate was composed as an audit candidate, not as a
publication-ready replacement. It has not passed the ordinary source,
typesetting, web, or page-review gates.

## Consequential-claim comparison

| Claim family | Old | Modified | Rewritten | Effect of changed research |
|---|---|---|---|---|
| Chastity, continence, and celibacy are distinct | Retained | Same | Retained | None; CCC 1322–1323 concerns the Eucharist, not CCC 2337–2350. |
| CIC 277 binds Latin clerics to continence and therefore celibacy | Retained | Same | Retained | None; CIC 1172 concerns major exorcism. |
| Obligation, impediment, penalty, loss of state, and dispensation are distinct | Retained | Same | Retained | None; CIC 1917 cc. 1151–1153 concern exorcism, not the bound historical clerical rule at c. 132. |
| Eastern common law honors married and celibate clergy but forbids marriage after ordination | Retained | Same | Retained | None. |
| The count of Churches *sui iuris* is a bounded reconstruction | Retained | Same | Retained | None. |
| Married permanent-deacon continence is not resolved by an identified authentic interpretation | Retained | Same | Retained | None. |
| Western discipline developed through distinct historical stages | Retained | Same | Retained | None; Trent session XIII is Eucharistic, while this article uses session XXIV on marriage. |
| Convert-clergy provisions are controlled exceptions | Retained | Same | Retained | None. |
| Modern teaching praises celibacy without making it intrinsic to priesthood | Retained | Same | Retained | None. |
| Personal cases require competent authority and current applicable law | Retained | Same | Retained | None. |

The rewritten candidate differs substantially in compression, organization,
and rhetoric. It does not differ from the old or modified treatment on any
consequential conclusion. No changed input adds, removes, strengthens, weakens,
or contradicts a claim in this leaf.

## Verdict

**No material change.** The staleness is edition-directory propagation from
new sibling source records outside the article's bound loci. No publication
replacement is warranted. Rebaseline and ledger changes are intentionally left
to the coordinating agent; this audit makes neither.
