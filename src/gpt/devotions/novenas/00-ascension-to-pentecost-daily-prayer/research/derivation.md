# The First Novena: Daily Prayer Book — Derivation Record

## Identity and controlling source

- **Provider and collection:** GPT; devotions; novena condensed recitation companion.
- **Canonical full guide:** `devotions/novenas/00-ascension-to-pentecost`, published as *The First Novena: From Ascension to Pentecost*.
- **Profile:** `guidance/devotions/novenas.md`, condensed-recitation-companion subtype.
- **Reader and use:** a reader who has already studied the canonical guide or is using the two publications together and needs a compact vocal-prayer book.
- **Provenance:** mechanically inherited from the canonical full guide through `generation-metadata.tex`; no second visible AI metadata block is permitted.

## Derivation boundary

The companion introduces no prayer text, theological synthesis, historical claim, calendar rule, indulgence claim, translation, or source judgment. It contains fixed navigation and status rubrics, then imports every recited text from the same canonical fragments consumed by the full guide. The full guide controls Scripture, silence, meditation, examination, concrete act, calendar, liturgical relationship, textual status, and all review limitations.

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
- The 28-page full guide and 10-page companion were rebuilt from the revised canonical fragments, compared for rendered prayer equivalence, visually inspected page by page, and installed byte-identically to their reviewed builds, SHA-256 `bd509b65321012e60a1f6e09aa411cb67e72d6a3c37f3d8e04c53f8e4115f255` and `aa8c424b6d802555a069d42cf75b1481e02d997733b58c52c636953d05c5c98d`.
- Independent liturgical, theological, patristic, Latin, historical-English transcription, hymnological, pastoral, and ecclesiastical review remains outstanding exactly as recorded for the canonical full guide.
