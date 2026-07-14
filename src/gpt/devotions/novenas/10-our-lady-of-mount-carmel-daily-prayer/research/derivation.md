# The Novena of Our Lady of Mount Carmel: Daily Prayer Book — Derivation Record

## Identity and controlling source

- **Provider and collection:** GPT; devotions; novena condensed recitation companion.
- **Canonical full guide:** `devotions/novenas/10-our-lady-of-mount-carmel`, published as *The Novena of Our Lady of Mount Carmel*.
- **Profile:** `guidance/devotions/novenas.md`, condensed-recitation-companion subtype.
- **Reader and use:** a reader who has already studied the canonical guide or is using the two publications together and needs a compact vocal-prayer book.
- **Provenance:** mechanically inherited from the canonical full guide through `generation-metadata.tex`; no second visible AI metadata block is permitted.

## Derivation boundary

The companion introduces no prayer text, theological synthesis, historical claim, calendar rule, promise, indulgence claim, translation, or source judgment. It contains fixed navigation and status rubrics, then imports every recited text from the same canonical fragments consumed by the full guide. The full guide controls Scripture, silence, meditation, examination, concrete act, calendar, Carmelite and Scapular status, textual variants, liturgical relationship, and all review limitations.

## Rendered-source map

| Companion content | Canonical owner | Use |
| --- | --- | --- |
| Sign of the Cross | `devotions/novenas/shared/common-prayers.tex` | Opening every day |
| Short *Flos Carmeli* | `devotions/novenas/10-our-lady-of-mount-carmel/prayers/short-flos-carmeli.tex` | Days 1–8 |
| Received Collects for Days 1–9 | `devotions/novenas/10-our-lady-of-mount-carmel/prayers/day-01-collect.tex` through `day-09-collect.tex` | One received Latin collect, selected devotionally and paired with a project translation, each day |
| Hail Mary | `devotions/novenas/10-our-lady-of-mount-carmel/prayers/hail-mary.tex` | Every day |
| Lord's Prayer and Lesser Doxology | `devotions/novenas/shared/common-prayers.tex` | Every day |
| Collect of the Feast | `devotions/novenas/10-our-lady-of-mount-carmel/prayers/feast-collect.tex` | Every day |
| Complete *Flos Carmeli* | `devotions/novenas/10-our-lady-of-mount-carmel/prayers/complete-flos-carmeli.tex` | Replaces the short form on Day 9 |
| Title, use notice, and day-heading macros | `devotions/novenas/shared/recitation-companion-format.tex` | Fixed non-substantive publication furniture |
| Source-specific order and canonical imports | `devotions/novenas/10-our-lady-of-mount-carmel-daily-prayer/main.tex` | Mechanical assembly only |

## Excluded material

The companion deliberately excludes the canonical guide's calendar instructions, worked dates, biblical and Carmelite exposition, historical development, Mariological and sacramental analysis, Scapular and promise dossier, meditations, examinations, concrete acts, pastoral qualifications, references, and annual-use commentary. Those exclusions implement the requested recitation-only format and do not revise the full guide.

## Controlling audit records

- Prayer inventory: `devotions/novenas/10-our-lady-of-mount-carmel/research/prayer-inventory.md`
- Research scope: `devotions/novenas/10-our-lady-of-mount-carmel/research/scope.md`
- Tradition and promise status: `devotions/novenas/10-our-lady-of-mount-carmel/research/tradition-status.md`
- Source audit: `devotions/novenas/10-our-lady-of-mount-carmel/research/source-audit.md`

## Review state

- Canonical-fragment factoring and companion assembly completed on 2026-07-13.
- On 2026-07-14 the canonical full guide replaced its nine project-composed collects with received liturgical collects from the 1987 *Collectio*. Because the companion imports those fragments, no companion-owned prayer wording was edited. All 32 canonical Latin and English prayer bodies were compared against extracted text from both rendered consumers, normalizing only line-wrap hyphenation, whitespace, Unicode composition, and equivalent TeX punctuation; every body matched its source and the other consumer.
- The full guide and companion settled at 29 and 10 pages. Every page was visually inspected; all prayer cards are complete, contained, and legible, and the companion introduces no blank, orphaned, clipped, split, or overlapping unit.
- Both PDFs passed clean-log scans, structured and inherited metadata validation, title and subject checks, letter geometry, `qpdf` structure checks, text extraction, Unicode mapping, and complete font embedding. Extracted companion text contains neither an internal ordering key nor a duplicate visible AI-generation block.
- The installed full guide and companion are byte-identical to their reviewed builds: SHA-256 `c4f69f803ee4d561b242a7d3dd14d15e4a6170a0a23c40987e9a48c9433b142c` and `26526ecb1d47af133cfb991117bcb3d4b1cd773be478b169a94cac34597997a7`, respectively.
- Independent Carmelite, historical, liturgical, Mariological, sacramental-theological, biblical, pastoral, Latin, hymnological, translation, and ecclesiastical review remains outstanding exactly as recorded for the canonical full guide.
