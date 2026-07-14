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
| Received Collects for Days 1–9 | `devotions/novenas/00-ascension-to-pentecost/prayers/day-01-collect.tex` through `day-09-collect.tex` | One received 1962 Missal collect appointed devotionally each day; source contexts and project translations are controlled by the full guide |
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
- On 2026-07-14 the nine canonical daily fragments were replaced with received 1962 Missal collects and project translations without changing their one-to-one import paths. All 30 canonical Latin and English prayer bodies were compared against extracted text from both rendered consumers, normalizing only line-wrap hyphenation, whitespace, Unicode composition, and equivalent TeX punctuation; every body matched its source and the other consumer.
- The full guide and companion settled at 27 and 10 pages. Every page was visually inspected after the final reflow; all prayer cards are complete, contained, and legible, and the companion introduces no blank, orphaned, clipped, split, or overlapping unit.
- Both PDFs passed clean-log scans, structured and inherited metadata validation, title and subject checks, letter geometry, `qpdf` structure checks, text extraction, Unicode mapping, and complete font embedding. Extracted companion text contains neither an internal ordering key nor a duplicate visible AI-generation block.
- The installed full guide and companion are byte-identical to their reviewed builds: SHA-256 `01a41341f80c410b83fa1035a1ddffb48b74de954653ada0b303174214de7515` and `83d1480fa3c285720d22a9dead23e00a6f17ee0b20e593f51c477abf236dae19`, respectively.
- Independent liturgical, theological, patristic, Latin, translation, hymnological, pastoral, and ecclesiastical review remains outstanding exactly as recorded for the canonical full guide.
