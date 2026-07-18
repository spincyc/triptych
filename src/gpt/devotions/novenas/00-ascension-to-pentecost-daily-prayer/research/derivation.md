# The First Novena: Daily Prayer Book — Derivation Record

## Identity and controlling source

- **Provider and collection:** GPT; devotions; novena condensed recitation companion.
- **Canonical full guide:** `devotions/novenas/00-ascension-to-pentecost`, published as *The First Novena: From Ascension to Pentecost*.
- **Profile:** `guidance/devotions/novenas.md`, condensed-recitation-companion subtype.
- **Reader and use:** a reader who has already studied the canonical guide or is using the two publications together and needs a compact vocal-prayer book.
- **Provenance:** mechanically inherited from the canonical full guide through `generation-metadata.tex`; no second visible AI metadata block is permitted.

## Derivation boundary

The companion introduces no prayer text, theological synthesis, historical claim, calendar rule, indulgence claim, translation, or source judgment. It contains fixed navigation and a compact terminal status summary, then imports every recited text from the same canonical fragments consumed by the full guide. The full guide controls Scripture, silence, meditation, examination, concrete act, calendar, liturgical relationship, textual status, and all review limitations.

## Rendered-source map

| Companion content | Canonical owner | Use |
| --- | --- | --- |
| Sign of the Cross | `devotions/novenas/shared/common-prayers.tex` | Opening every day |
| Daily Invocation and Collect | `devotions/novenas/00-ascension-to-pentecost/prayers/daily-invocation.tex` | Opening every day |
| Received Collects for Days 1–9 | `devotions/novenas/00-ascension-to-pentecost/prayers/day-01-collect.tex` through `day-09-collect.tex` | One received 1962 Latin collect appointed devotionally each day with received historical English from Lefebvre's 1925 *Daily Missal*; source contexts and exact conclusion joins are controlled by the full guide |
| *Veni Creator Spiritus* | `devotions/novenas/00-ascension-to-pentecost/prayers/veni-creator.tex` | Every day; complete form preferred by the full guide |
| *Veni Sancte Spiritus* | `devotions/novenas/00-ascension-to-pentecost/prayers/veni-sancte.tex` | Added on Day 9 |
| Lord's Prayer and Lesser Doxology | `devotions/novenas/shared/common-prayers.tex` | Closing every day |
| Title, use notice, and day-heading macros | `devotions/novenas/shared/recitation-companion-format.tex` | Fixed non-substantive publication furniture |
| `Scope and Status` relationship, non-liturgical status, and calendar boundary | Canonical `research/scope.md` | Compact terminal summary only; the full guide retains the calculation, examples, qualifications, and review state |
| `Scope and Status` source and translation boundary | Canonical `research/prayer-inventory.md` and `research/source-audit.md` | Identifies the controlling witness families without adding prayer text, source loci, or an approval claim |
| Source-specific order and canonical imports | `devotions/novenas/00-ascension-to-pentecost-daily-prayer/main.tex` | Mechanical assembly only |

## Excluded material

The companion deliberately excludes the canonical guide's calendar instructions, worked dates, biblical and patristic exposition, historical development, theological analysis, meditations, examinations, concrete acts, pastoral qualifications, references, and annual-use commentary. Those exclusions implement the requested recitation-only format and do not revise the full guide.

## Controlling audit records

- Prayer inventory: `devotions/novenas/00-ascension-to-pentecost/research/prayer-inventory.md`
- Research scope: `devotions/novenas/00-ascension-to-pentecost/research/scope.md`
- Source audit: `devotions/novenas/00-ascension-to-pentecost/research/source-audit.md`

## Review state

- Canonical-fragment factoring and companion assembly completed on 2026-07-13.
- On 2026-07-14 every prose English vocal prayer in the imported canonical fragments was replaced with exact received wording from Lefebvre's 1925 *Daily Missal*. The full guide records each source locus, the same witness's exact formula used to complete each explicit conclusion abbreviation, its 1924/1925 permissions, and the applicable rights boundary. The companion continues to own no prayer wording or translation.
- The 28-page full guide and 10-page companion were rebuilt from the revised canonical fragments, compared for rendered prayer equivalence, visually inspected page by page, and installed byte-identically to their reviewed builds, SHA-256 `0ffcb950e654d647fd739b53069d2f7ea86a5a7cd7287cb612bd3e4c668de413` and `382099908037ddd4a9daa9da20265f23a5e37e30eec66a3a5f6610c510d0fc08`. Those production snapshots are superseded.
- Phase-three production verification completed on 2026-07-17 after the companion gained the profile-required terminal `Scope and Status` appendix, its title-page warning was reduced to a pointer, and the inherited metadata import moved behind the appendix. Coordinated settled two-pass builds produced a 29-page full-guide snapshot, SHA-256 `332de35a7ea6915d757bcc074c227d7edcd7e91cf450191ab485023f91ac55e8`, and an 11-page companion snapshot, SHA-256 `2ae9a17e607634e8ca0cb8606e7376d22c3b83c47bc1827de6bbfe2f6de6e648`. The final logs were warning-free; generation metadata, PDF structure and metadata, embedded/subsetted/Unicode-mapped fonts, extracted text, rendered prayer-body equivalence, all 40 physical-page visual checks, and installed/build identity comparisons passed. Those snapshots are superseded; the companion still imports the canonical prayer fragments without introducing independent prayer wording, translation, or source judgment.
- Final clean-build review completed on 2026-07-18: coordinated settled two-pass builds produced the current 28-page full guide, SHA-256 `cfc4a443ab087cd5ad84a8c89facd045cd28fa94f4dcd970cd0a004a034be5cf`, and 11-page companion, SHA-256 `2ae9a17e607634e8ca0cb8606e7376d22c3b83c47bc1827de6bbfe2f6de6e648`. The warning-free logs, generation metadata, PDF structure and metadata, embedded/subsetted/Unicode-mapped fonts, extracted text, rendered prayer-body equivalence, every-page visual review, and installed/build byte comparisons passed.
- Independent liturgical, theological, patristic, Latin, historical-English transcription, hymnological, pastoral, and ecclesiastical review remains outstanding exactly as recorded for the canonical full guide.
