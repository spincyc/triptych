# Jeremias: first scroll, later letter, and received book

This bounded correction repairs the false inheritance of 604 B.C. as the
composition date of every verse of Jeremias. It does not reopen the chronology
corpus's global acceptance or assign writing dates to unexamined constituents.

## Inspected evidence

Michael Faulhaber, “Jeremias,” *The Catholic Encyclopedia* 8 (New York, 1910),
“The book of the prophecies of Jeremias,” especially “Analysis of contents” and
“Literary criticism of the book,” was reopened in the retained article-text
derivative of the exact registered New Advent delivery:

- parent: `artifact.catholic-encyclopedia.volume-8.new-york-1910.newadvent-08334a-dd4ae528`;
- retained derivative: that id plus `-article-text`;
- retained-text SHA-256: `d90971c5159e5d8000aeced4cc2ff634fa8ed80574d609f84fe29ab6a360784e`;
- decisive physical lines in the retained derivative: 41 and 45;
- public delivery: <https://www.newadvent.org/cathen/08334a.htm>.

Line 45 dates the first authentic recension to the fourth year of Joakim,
604 B.C.; it then describes enlargement and identifies chapter 52 as a
post-Jeremianic addition. It does not establish an exact surviving extent for
the first scroll or a completion date for the received book. Its partly
qualified arrangement by reign cannot supply that missing extent. The earlier
whole-book composition assertion was consequently a demonstrated scope error,
not merely a date for which another source had yet to be found. The current
public page was also reopened; the correction remains grounded in the exact
registered retained witness, without claiming printed-page collation.

The tracked Douay-Rheims text was read independently at Jeremias 29:1–32 and
36:1–32. The chapter fragments identify their expression as the
Challoner/Gutenberg edition; the separately retained American 1899 verse-text
was checked at the decisive verses as well. Their minor punctuation and
singular/plural differences in 29:1–2 do not alter the chronological statements;
the claim quotes only wording shared by the inspected texts.

Jeremias 29:1–3 expressly identifies a letter from Jerusalem to the Babylonian
captives after Jechonias and the other deportees left Jerusalem. Verse 24
starts the address to Semeias, verses 25–29 concern his correspondence, and
verse 30 introduces a further word of the Lord. The first letter's positive
composition bound is therefore scoped to 29:1–23. It supplies no exact year or
completion horizon for the later correspondence.

Jeremias 36:1–4 dates the command and Baruch's first recording to Joakim's
fourth year. Verse 9 dates the subsequent public reading to the fifth year;
verses 27–32 narrate the replacement after the first scroll was burned. Those
events are not conflated.

## Canonical correction

| Subject | Corrected assertion |
| --- | --- |
| `composition.book-of-jeremias` | Stable id retained; relation changed to `final-formation`, with an open bound after the first recension. It assigns no constituent composition year. |
| `israel.exile.jeremias-first-scroll` | The first recording, bound as `narrated-event` only at 36:1–4. Scripture's fourth-year statement is preferred; Faulhaber's 604 B.C. remains an answerable alternate under the traditional profile. |
| `composition.jeremias-letter-to-the-exiles` | Composition of 29:1–23 follows the existing `israel.exile.second-captivity` event. It has no absolute endpoint and does not extend to 29:24–32. |

The anchors' existing dates and alternatives are unchanged. No conversion,
arithmetic, inferred first-scroll partition, new profile, or publication-local
replacement date is introduced. The comprehensive cascade selects these
traditional assertions under their separate relations.

## Query and consumer impact

Both `catholic-traditional-v1` and the default
`catholic-comprehensive-v1` were queried before and after the correction through
the public `scripture-chronology query` path.

| Loci | Before | After |
| --- | --- | --- |
| 29:11–14 | Whole-book composition at 604 B.C. | Letter composition after Jechonias's deportation, plus the distinct received-book formation bound. |
| 29:24 and 29:32 | Whole-book composition at 604 B.C. | Received-book formation bound only; no first-letter composition claim. |
| 36:1–4 | Whole-book composition at 604 B.C. | First-recording event: preferred fourth-year statement and alternate 604 B.C.; separate received-book formation bound. |
| 1:1 and 52:34 | Whole-book composition at 604 B.C. | Received-book formation bound only. |

All 1,363 canonical Jeremias loci lose the false whole-book composition year.
The generated primary coverage table changes only Jeremias rows, from 59 to
61 runs; its total changes from 1,896 to 1,898 runs. The four verses at 36:1–4
gain `dated` status. Chronology statuses elsewhere are unchanged;
`composition-only` continues to include final formation.

An exhaustive scan of both providers' generated `research/chronology.toml`
records found exactly one publication querying Jeremias loci: GPT
`liturgy/roman-rite/1962/propers/temporal/66-resumed-fifth-after-epiphany`, whose
Introit queries 29:11, 29:12, and 29:14. Its `research/chronology.toml` and
`research/chronology-annotations.tex` require regeneration by the publication
owner after independent source review. Other chronology records containing
`Jer.` use it within existing source ids, not appointed query loci. No existing
publication or web artifact was changed by this correction.

## Verification boundary

- `make check-scripture-chronology` passes; authored data validates and the
  regenerated `coverage.tsv` is current.
- Comprehensive `coverage --require-date` passes for both distinct content
  (37,171 loci) and supported addresses (42,589), with zero missing dates.
- All 26 `TrackedHardCaseTests` pass, including three new public-query
  regressions for the letter boundary, first-scroll testimony, and received
  book's relation.
- The full 269-test chronology suite has one failure:
  `TraditionalAttributionTests.test_the_tracked_attribution_is_exactly_the_inspected_psalm_scope`.
  The identical five extra Psalm scopes reproduce using the saved pre-change
  authored chronology; that inherited expectation defect is outside this
  correction. The other 268 tests pass, including source-quotation checks.
- The gated `profile-contract-rereview-manifest.tsv` was regenerated against
  its unchanged pinned base. Its 532 rows describe the current review surface;
  regeneration records no new acceptance or review verdict.
  The existing semantic differ does not export textual-unit relation, scope,
  title, or structured boundary fields. This correction still enters that
  manifest through its changed claim prose, precision and endpoints, but
  review of those omitted facets requires the canonical YAML and public-query
  comparison recorded above. No semantic-differ code is changed here.

Independent source review and publication-owner regeneration are separate from
these implementation checks. The source inventory/family refresh and
`make check-sources` belong to the coordinating source/publication change.
