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
| Proper Collects for Days 1–9 | `devotions/novenas/10-our-lady-of-mount-carmel/prayers/day-01-collect.tex` through `day-09-collect.tex` | One appointed collect each day |
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
- All 32 canonical Latin and English prayer bodies were compared against extracted text from both rendered consumers, with only line-wrap hyphenation, whitespace, and equivalent TeX punctuation normalized; every body matched the source in the full guide and this companion.
- The refactored 27-page full guide retained page-for-page raster identity with the pre-factoring installed proof. The 8-page companion settled after every day heading and each long closing unit were kept with their appointed prayer cards; every final page was visually inspected at full size.
- Both PDFs passed clean-log scans, structured and inherited metadata validation, PDF title and subject checks, letter geometry, `qpdf` structure checks, text extraction, Unicode mapping, and complete font embedding. Extracted companion text contains neither the internal ordering keys nor a duplicate visible AI-generation block.
- The installed full guide and companion were byte-identical to their reviewed builds, and the installed companion's page rasters matched the frozen reviewed proof.
- Independent Carmelite, historical, liturgical, Mariological, sacramental-theological, biblical, pastoral, Latin, hymnological, translation, and ecclesiastical review remains outstanding exactly as recorded for the canonical full guide.
