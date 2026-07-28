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

## Second exact-trigger review — 2026-07-27

After the earlier review, the exact explanation changed. Immediately before
this second comparison,

```text
scripts/research-staleness explain claude \
  articles/canon-law/clerical-celibacy-chastity-and-continence
```

reported exactly ten new inputs:

- Catechism, English USCCB second edition (2019): passages 391–395, 550,
  1667–1673, 1700–1706, 1734–1735, 1857–1859, 2111, 2116–2117, and
  2846–2854; and
- CIC 1983, Latin Vatican web codex state dated 2026-07-25: canon 1166.

The ignored modified candidate is an exact copy of the current publication
source at
`build/staleness/claude/articles/canon-law/clerical-celibacy-chastity-and-continence/modified/`.
Minimal incorporation therefore makes no source or rendered change. The
ignored research-first candidate at the corresponding
`rewritten/treatment.md` was drafted from the research scope, audits, and
identified authorities without consulting the current article prose. It
independently treats the three-term distinction; Latin clerics and permanent
deacons; Eastern discipline; historical development; convert clergy and
dispensation; theological rationale; current controversies; authority and
case limits; and the effect of this exact ten-record trigger.

| Consequential claim family | Old publication | Modified candidate | Research-first candidate | Effect of the ten changed inputs |
|---|---|---|---|---|
| Chastity, continence, and celibacy are distinct | Retained | Identical | Retained | None. The nine Catechism passages concern demonology, sacramentals, freedom and imputability, mortal sin, occult practices, and temptation, not the bound chastity loci at CCC 2337 and 2348–2350. |
| CIC 277 governs Latin clerical continence and celibacy | Retained | Identical | Retained | None. Canon 1166 defines sacramentals and does not modify canon 277. |
| Admission, impediment, penalty, loss of state, and dispensation are separate juridic questions | Retained | Identical | Retained | None. No changed input alters a canon used for these questions. |
| Married permanent-deacon discipline and its unresolved continence dispute require exact legal controls | Retained | Identical | Retained | None. Neither canon 1166 nor the new Catechism loci supplies an authentic interpretation or changes the governing canons. |
| Eastern common law preserves married and celibate clergy while forbidding marriage after ordination | Retained | Identical | Retained | None. No CCEO or proper-law input changed. |
| Western discipline has a staged historical development | Retained | Identical | Retained | None. No historical witness changed. |
| Convert-clergy provisions and dispensations are controlled juridic exceptions | Retained | Identical | Retained | None. No governing provision changed. |
| Modern teaching praises celibacy without making it intrinsic to priesthood | Retained | Identical | Retained | None. No cited magisterial locus changed. |
| Consultative proposals, papal teaching, and enacted law have distinct juridic force | Retained | Identical | Retained | None. No synodal, papal, or legislative input relevant to that comparison changed. |
| Concrete cases require competent authority and current applicable law | Retained | Identical | Retained | None. The new records neither expand nor narrow this limit. |

The changed research adds, removes, strengthens, weakens, or contradicts no
consequential claim in the old publication. The modified treatment is
identical. The research-first treatment differs in organization and
compression, but reaches the same legal, historical, theological, and
prudential conclusions. Its disagreement with the old paper is rhetorical,
not substantive.

**Second-review verdict: no material change.** The ten additions enter the
fingerprint through whole-work hashing: this leaf binds other Catechism
editions and loci and other loci in the same CIC edition. None is an exact
bound locus used by the publication. No prose, source binding, PDF, web
edition, catalog, release, jurisdiction, currentness, or review-state change
is warranted.

## Third exact-trigger review — 2026-07-27

Immediately before this comparison, the exact explanation reported one new
input:

- the GPT sibling edition's
  `research/staleness-review-2026-07-27-second.md`.

That file is an editorial audit record. It reports the GPT edition's
independent no-material assessment of its own sibling-review and Catechism
triggers; it is not a new canon, authentic interpretation, magisterial text,
historical witness, or factual source for this Claude edition.

The ignored modified candidate is an exact pre-note snapshot of the current
Claude source. The ignored research-first treatment was checked independently
against the Claude scope, audit, bindings, and controlling authorities. The
three-term distinction, Latin and Eastern legal regimes, permanent-diaconate
question, historical development, convert-clergy exceptions, theological
arguments, and case limits remain unchanged. The GPT editorial record adds,
removes, strengthens, weakens, or contradicts none of those consequential
claims.

**Third-review verdict: no material change.** The sole trigger is
provider-sibling editorial collateral. No publication, source binding, PDF,
web edition, catalog, currentness, or review-state revision is warranted.
Rebaseline and ledger mutation remain for the coordinating agent.
