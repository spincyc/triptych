# Research-staleness review — 2026-07-27

Provider: Anthropic Claude
Publication: `history/traditional-priestly-institutes/02-fssp`

## Trigger

`scripts/research-staleness explain claude
history/traditional-priestly-institutes/02-fssp` reported one changed
input:

`src/sources/works/catholic-church/codex-iuris-canonici-1983/editions/latin-vatican-web-codex-2026-07-25/passages/canon-1172.toml`

The new passage is the authentic Latin of 1983 CIC canon 1172. It
governs the local ordinary's particular and express permission for a
priest to pronounce exorcisms over the possessed. It belongs to Book IV
and has no subject-matter relation to this account's bounded canon-law
module, which uses Book II norms on societies of apostolic life,
pontifical right, houses, incardination, governance, apostolate, and
relations with diocesan bishops. The FSSP publication does not mention
exorcism or canon 1172.

## Candidates built

- `build/staleness/claude/history/traditional-priestly-institutes/02-fssp/modified/`
  is an in-place candidate retaining the current source without change,
  because the new passage supplies no relevant fact or qualification.
- `build/staleness/claude/history/traditional-priestly-institutes/02-fssp/rewritten/`
  is a complete independent rewrite drafted from the scope, source
  audit, evidence map, and bindings. It expressly tests canon 1172
  against the work's subject boundary.

Both candidates were compiled through two `pdflatex` passes on
2026-07-27. The modified candidate is 47 pages; the rewritten candidate
is 5 pages. Both logs are free of fatal errors, undefined references,
and overfull or underfull boxes. The modified log retains the three
known `longtable` “Infinite glue shrinkage” notices recorded in the
publication's production audit; the rewritten log has none.

## Consequential-claim comparison

Impact terms refer only to the changed canon-1172 passage. “None” means
it neither adds, removes, strengthens, weakens, nor contradicts the
claim. Claim numbers correspond to `evidence-map.md`.

| Claim | Subject | Changed input | Modified against old | Rewritten against old |
|---|---|---|---|---|
| 1 | Protocol of 5 May 1988 | None | Same substance | Same substance |
| 2 | Declaration of 2 July 1988 | None | Same substance | Same substance |
| 3 | Foundation act of 18 July 1988 | None | Same substance | Same substance |
| 4 | Foundation signatures | None | Same substance | Omitted as non-load-bearing detail |
| 5 | Commission letter of 22 July 1988 | None | Same substance | Same substance |
| 6 | Six special faculties of 18 October 1988 | None | Same substance | Same substance |
| 7 | Relation of faculty 2 to the protocol | None | Same substance | Omitted as non-load-bearing synthesis |
| 8 | Liturgical decree of 10 September 1988 | None | Same substance | Same substance |
| 9 | Decree of erection of 18 October 1988 | None | Same substance | Same substance |
| 10 | Canonical anatomy of a society | None | Same substance | Same substance in shorter form |
| 11 | Wigratzbad beginnings | None | Same substance | Same substance |
| 12 | North American seminary | None | Same substance | Same substance |
| 13 | 1996 ordination rescript | None | Same substance | Omitted as non-load-bearing detail |
| 14 | Membership statistics | None | Same substance | Same substance |
| 15 | John Paul II's 1998 address | None | Same substance | Omitted as non-load-bearing context |
| 16 | Cardinal Ratzinger's 1998 conference | None | Same substance | Omitted as non-load-bearing context |
| 17 | Recourse of 29 June 1999 | None | Same substance | Same substance in summary |
| 18 | Responses of 3 July 1999 | None | Same substance | Same substance |
| 19 | Measures of 13 July 1999 | None | Same substance | Same substance in summary |
| 20 | Father Bisig's recourse | None | Same substance | Omitted as non-load-bearing detail |
| 21 | Assembly of February 2000 | None | Same substance | Same substance |
| 22 | Request for special law | None | Same substance | Same substance in summary |
| 23 | Letter of 29 June 2000 | None | Same substance | Same substance |
| 24 | Government imposed in 2000 | None | Same substance | Same substance in summary |
| 25 | Chapter response and recourse | None | Same substance | Same substance in summary |
| 26 | Chapter's constitutional argument | None | Same substance | Omitted as non-load-bearing detail |
| 27 | Decree of 12 October 2000 | None | Same substance | Same substance with evidence ceiling |
| 28 | Definitive constitutions of 2003 | None | Same substance | Same substance |
| 29 | Constitution article 8 and “exclusive” | None | Same substance | Same substance |
| 30 | *Summorum Pontificum* arts. 1 and 3 | None | Same substance | Same substance |
| 31 | Suppression of the Commission in 2019 | None | Same substance | Same substance |
| 32 | *Traditionis custodes* arts. 6 and 8 | None | Same substance | Same substance |
| 33 | FSSP communiqué of 20 July 2021 | None | Same substance | Omitted as non-load-bearing detail |
| 34 | 2021 *Responsa* | None | Same substance | Same substance in summary |
| 35 | Papal decree of 11 February 2022 | None | Same substance | Same substance |
| 36 | Report of audience of 4 February 2022 | None | Same substance | Omitted as non-load-bearing detail |
| 37 | Rescript of 20 February 2023 | None | Same substance | Same substance |
| 38 | Apostolic visitation opened in 2024 | None | Same substance | Same substance |
| 39 | Audience of 19 January 2026 | None | Same substance | Same substance |
| 40 | No published visitation outcome at cutoff | None | Same substance | Same substance |
| 41 | Erection and supervision are distinct | None | Same substance | Same substance |
| 42 | Limit imposed in 2000 | None | Same substance | Same substance |
| 43 | Practical position under the 2022 faculty | None | Same substance | Same substance |

The rewritten candidate differs from the old publication chiefly in
compression and omission of non-load-bearing narrative detail. None of
those differences follows from canon 1172. On every retained
consequential claim it reaches the same material result and preserves the
same evidential ceilings.

## Verdict

**No material change.** Canon 1172 adds no evidence, qualification, or
counterevidence relevant to any claim in this publication. The current
edition should remain installed unchanged. The staleness flag may be
cleared by a separately authorized rebaseline; this review does not
change the baseline or ledger.
