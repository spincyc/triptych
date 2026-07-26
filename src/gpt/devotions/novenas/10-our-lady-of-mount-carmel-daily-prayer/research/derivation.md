# The Novena of Our Lady of Mount Carmel: Daily Prayer Book — Derivation Record

## Identity and controlling source

- **Provider and collection:** GPT; devotions; novena condensed recitation companion.
- **Canonical full guide:** `devotions/novenas/10-our-lady-of-mount-carmel`, published as *The Novena of Our Lady of Mount Carmel*.
- **Profile:** `guidance/devotions/novenas.md`, condensed-recitation-companion subtype.
- **Reader and use:** a reader who has already studied the canonical guide or is using the two publications together and needs a compact vocal-prayer book.
- **Provenance:** mechanically inherited from the canonical full guide through `generation-metadata.tex`; no second visible AI metadata block is permitted.

## Derivation boundary

The companion introduces no prayer text, theological synthesis, historical claim, calendar rule, promise, indulgence claim, translation, or source judgment. It contains fixed navigation and a compact terminal status summary, then imports every recited text from the same canonical fragments consumed by the full guide. The full guide controls Scripture, silence, meditation, examination, concrete act, calendar, Carmelite and Scapular status, textual variants, liturgical relationship, and all review limitations.

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
| `Scope and Status` relationship, non-liturgical status, and calendar boundary | Canonical `research/scope.md` and `research/tradition-status.md` | Compact terminal summary only; the full guide retains the calendar detail, Carmelite and Scapular qualifications, and review state |
| `Scope and Status` source and translation boundary | Canonical `research/prayer-inventory.md`, `research/flos-carmeli-translation-search.md`, and `research/source-audit.md` | Identifies the controlling witness families without adding prayer text, source loci, or an approval claim |
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
- Phase-three production verification completed on 2026-07-17 after the companion gained the profile-required terminal `Scope and Status` appendix, its title-page warning was reduced to a pointer, and the inherited metadata import moved behind the appendix. Coordinated settled two-pass builds produced a 30-page full guide, SHA-256 `f83b8303c6c1699b67a49b65e8416ff5609f61929b6c34ae1ae036d2af08c8b8`, and 12-page companion, SHA-256 `632c71f5a21205a4acf310ee6ebdc11f779e7dcb2e4ec053dcbf922b4186bbcd`. The final logs were warning-free; generation metadata, PDF structure and metadata, embedded/subsetted/Unicode-mapped fonts, extracted text, and rendered shared-prayer equivalence passed; all 42 physical pages were visually reviewed; and each installed PDF was byte-identical to its reviewed build. Those snapshots are superseded. The companion still imported the canonical prayer fragments without introducing independent prayer wording, translation, approval claim, or source judgment.
- Final-typography production review completed on 2026-07-19: coordinated settled two-pass builds produced the current 30-page full guide, SHA-256 `ae2a16c3586a231c8a2df5c3cd9fb0f2659fea5bad73d3151f5f47e481c072a6`, and 13-page companion, SHA-256 `4a1fcf4e17458cea4f9593efb5aa5782c4a6301fd9d156d0153ece5cc25558af`. Both warning-free final logs, `qpdf`, PDF title and page metadata, embedded/subsetted/Unicode-mapped fonts, nonempty text extraction, and rendered shared-prayer equivalence passed. All 43 physical pages were visually reviewed, and both installed PDFs are byte-identical to their reviewed builds. The companion still imports the canonical prayer fragments without introducing independent prayer wording, translation, approval claim, or source judgment.
- Independent Carmelite, historical, liturgical, Mariological, sacramental-theological, biblical, pastoral, Latin, hymnological, translation, and ecclesiastical review remains outstanding exactly as recorded for the canonical full guide.

## Compact-rights-colophon production review — 2026-07-19

The settled 12-page PDF, SHA-256 `d6eaf8220ff47fe26618c9dc4d3b0ae3e18e9770585514b9a55874f3c2d91c2c`, is the exact repository-reviewed build snapshot. The final log was warning-free; generation metadata, `qpdf` structure, PDF title/page metadata, embedded and subsetted fonts with Unicode maps, and nonempty text extraction passed their gates. Repository production review inspected every physical page; the compact final-page reuse-and-rights colophon is readable, unclipped, non-overlapping, remains with terminal content, and creates no rights-only spill page. The installed PDF is byte-identical to this reviewed build. This reviewed build supersedes every earlier production snapshot. This exact current snapshot has release-specific distribution clearance under the 20 July 2026 dated rights supplement. That operational decision supplies no independent review or ecclesiastical approval.

## Research-staleness verdict — 2026-07-26

Both candidates were compared with owner and companion. No fragment, rubric,
dependency, or independent-claim correction was found; this exact companion
is ready for rebaselining.
