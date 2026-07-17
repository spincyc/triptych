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
| Received Collects for Days 1–9 | `devotions/novenas/10-our-lady-of-mount-carmel/prayers/day-01-collect.tex` through `day-09-collect.tex` | One received Latin collect, selected devotionally, with a source pointer to approved 2012 English that is not reproduced |
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
- Complete-*Flos Carmeli* translation search: `devotions/novenas/10-our-lady-of-mount-carmel/research/flos-carmeli-translation-search.md`
- Research scope: `devotions/novenas/10-our-lady-of-mount-carmel/research/scope.md`
- Tradition and promise status: `devotions/novenas/10-our-lady-of-mount-carmel/research/tradition-status.md`
- Source audit: `devotions/novenas/10-our-lady-of-mount-carmel/research/source-audit.md`

## Review state

- Canonical-fragment factoring and companion assembly completed on 2026-07-13.
- On 2026-07-14 the canonical full guide replaced its nine project-composed collects with received liturgical collects from the 1987 *Collectio* and completed their abbreviated endings only with the governing formulas in GIRM 54. A second revision removed every project-authored or project-translated vocal prayer: the daily collects became Latin-only with approved-English source pointers, the short *Flos Carmeli* received Best's 1902 English, the complete sequence became Latin-only, and the Hail Mary and feast prayer received Lefebvre's 1925 Latin and English. Because the companion imports those fragments, it owns none of the revised prayer wording.
- On 2026-07-15 the canonical guide's expanded translation search identified three complete modern English *Flos Carmeli* witnesses. After the requester confirmed approval to use all three, the guide selected the version attributed to the 1993 joint O.Carm.–OCD *Proper of the Liturgy of the Hours* for its strongest institutional provenance and coherent paired `nos ad esse / tecum in saeculum` Latin. The canonical fragment now reproduces the exact Carmelite-source transcription in two bilingual cards without adding `Amen`; the companion inherits that same fragment and introduces no separate translation or approval claim.
- The 30-page full guide and 11-page companion were rebuilt from the revised shared sources, compared for rendered-source equivalence, visually inspected page by page, and installed byte-identically to their reviewed builds, SHA-256 `8404c469d1702f8aece16048fc5b897f467b8c51e56e88f4d61ea8022216b481` and `eae645c94f2c126ff96d85dec00799ea4f372464d2ecec8420aa132cab5d6904`.
- Independent Carmelite, historical, liturgical, Mariological, sacramental-theological, biblical, pastoral, Latin, hymnological, translation, and ecclesiastical review remains outstanding exactly as recorded for the canonical full guide.
