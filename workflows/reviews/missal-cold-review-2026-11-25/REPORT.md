# Missal Timeline Cold Review, Multi-Rite Expansion & Diffable Original-Language Corpus Report (2026-11-25)

- **Branch & Base**: Reconciled and rebased onto `origin/main` (`462f311014`) on workspace branch `feature/missal-timeline`, prepared for fast-forward publication to `main`.
- **Scope**: Cold architectural, historical, textual, corpus, visual, and cross-referencing review of Triptych's Missal Timeline (`tools/act-history`, `tools/missal-coverage-reconciliation`, `scripts/_eucharistic_*.py`, `src/sources/inventories/`, `src/sources/works/`, `src/web/browser/history/`, and sibling routes), followed by deduplicated multi-lane research expansion, independent pixel-collated original-language constituent transcription across all six Catholic liturgical traditions, browser-product parity recording, release-binding refresh, and deployment-gate verification.
- **Governing policies**: `guidance/time-machine.md`, `guidance/act-histories.md`, `guidance/sources.md`, `guidance/liturgical-text-publication-policy.md`, and `THIRD_PARTY.md`.

---

## 1. Cold Review Findings & Reconciliation Scope

A cold review of Triptych's Missal Timeline (originally audited on October checkpoint `fe1cf06ac9` and reconciled cleanly onto `origin/main` `462f311014`, preserving 100% of Batch 4/5 dossiers, 20 existing checked native books, the unreviewed Greek Chrysostom drafts, and the browser-product/corpus-index architecture) identified and addressed six concrete gaps:

1. **Original-language native text skewed exclusively Latin/Arabic**: Even after Batch 5 expanded Western Latin constituents to 20 books (Roman 1570/1604/1635, Dominican 1550/1553/1603/1604, Cistercian 1606/1657, Mozarabic 1500/1755/1804, plus 1 Arabic Creed in Tuki 1736), **zero** independently reviewed native-book constituents existed in Greek (`grc`), Classical Armenian (`hy`), Bohairic Coptic (`cop`), Classical Ethiopic (`gez`), or Classical Syriac (`syr`), despite tracked US-public-domain facsimiles already sitting in `src/sources/works/`.
2. **Research & geographic coverage gaps**: Several *sui iuris* Eastern Churches and regional trajectories needed dedicated staged timelines or deeper coverage (Belarusian, Križevci/Croatia–Serbia, Georgian Byzantine control, deeper Melkite/Syro-Malankara/Hungarian/Bulgarian/Macedonian stages); global & missionary Catholic history (Mexico City 1561, Lima 1583, Quebec 1703/1851, China 1615/1670/1949, Japan 1605 ritual control, Goa/Diamper 1599, India 1969, Philippines, Brazil, Chiapas, Broome, Carthage control, Eritrea/Keren) and uncovered Western uses/orders (Lübeck, Merseburg, Benedictine monastic, plus deeper Dominican/Carmelite/Carthusian/Premonstratensian/Augustinian/Servite/Franciscan stages) lacked staged sequences; and 21 acquired canonical `edition.*` records in `src/sources/works/` were unlinked in the Eastern/Western timelines.
3. **Factual primary-source locus error in existing Chaldean 1767 metadata**: Direct pixel inspection of `artifact.chaldean-catholic-church.missale.1767-rome-propaganda.google-scan-pdf-4d048b31` (independently confirmed by both transcriber and collator) established that Addai & Mari Gehanta 3 (omitting the life-giving Gospel phrase) lies on **PDF p. 333 / printed p. 285 (`ܪܦܗ`)** rather than PDF p. 339 / printed p. 284 (PDF 339 is printed p. 279 `ܪܥܛ`, a pre-anaphoral litany), and that Mosul 1901 (`PDF 67`) and Puttenpalli 1906 (`PDF 234`) both print pure Syriac feminine **`ܒܣܒܪܬܗ ܡܚܝܢܝܬܐ`** (*b-sḇarṯēh mḥayyānīṯā*) rather than the Greek loanword `ܒܐܘܢܓܠܝܘܢܗ ܡܚܝܢܐ`.
4. **Single-witness stage rigidity**: `scripts/_eucharistic_stages.py` and `src/web/browser/history/history.js` previously required `binding["catalogue_witness_ids"] == stage["witness_ids"]` even for partial `constituent` bindings, preventing honest single-witness transcription on multi-witness stages (such as Chaldean 1901 Ordinary + Companion Propers or Maronite Dibs 1888 / 1908 second printing).
5. **Uncached library-reload fanout in `tools/missal-coverage-reconciliation`**: With `origin/main`'s growth to 128,302 entries in `src/sources/works/`, calling `history.catalogue()` without reusing the freshly loaded cold `library` triggered 38 separate cold tree walks (>70 min). Extending `replay_library(root, preloaded=...)` in `scripts/_eucharistic_texts.py` (preserving disk-uncached read-only isolation and exit-time byte verification of every pinned manifest) reduced `tools/missal-coverage-reconciliation` to **1m39s** on `462f311014`.
6. **Reader navigation, visual diffing, and cross-site discoverability**: The timeline lacked rite-family and geographic-region browsing controls, era orientation bands, an inline word-by-word Visual Diff Studio with reproducible `git diff --word-diff=color` commands, and reverse cross-links from the Source Library (`sources/`), Liturgical Day / Propers Reader (`liturgy/`), and narrative library catalogues (`library/*.md`, `docs/the-mass.md`).

---

## 2. Reconciled Quantitative Summary (`origin/main` `462f311014` → Current)

| Metric | `origin/main` (`462f311014`) | Reconciled Current | Delta |
| --- | ---: | ---: | ---: |
| Stage dossiers (`src/sources/inventories/eucharistic-stages/`) | 39 | **42** | +3 |
| Canonical traditions mapped | 259 | **278** | +19 net-new |
| Rite-family / Geographic-region taxonomy | unindexed | **10 rite families · 11 regions (278/278)** | new |
| Documented + provisional book stages | 483 | **568** | +85 |
| Stage transitions | 116 | **175** | +59 |
| Declared research gaps | 283 | **318** | +35 |
| Stage text coverage (`partial` / `not-transcribed` / `complete`) | 18 / 465 / 0 | **35 / 533 / 0** | +17 partial |
| Catalogue entries (Eastern + Western + legacy) | 2,031 | **2,052** (458 E · 1,535 W · 59 legacy) | +21 |
| Typed cross-tradition relationships | 62 | **92** | +30 net-new |
| **Checked native-book constituents (`eucharistic-books/`)** | 20 | **37** | **+17** |
| **Native liturgical languages represented** | 2 (`la`, `ar`) | **7** (`la`, `syr`, `grc`, `hy`, `cop`, `gez`, `ar`) | **+5 scripts** |
| **Catholic liturgical traditions with checked native text** | 2 (Latin, Coptic-Arabic) | **All 6** (Latin, Byzantine, Armenian, Alexandrian, East Syriac, West Syriac) | **6 / 6** |
| **Total canonical native units / words** | 387 units | **540 units · 24,499 words** | +153 units |
| **Source-hashed witness comparisons** | 31 | **43** | +12 |
| **Source Library ↔ Timeline reverse cross-links** | 0 | **84 canonical editions** | +84 |
| Browser product families / files / bytes | 13 / 30,437 / 284,475,770 | **13 / 30,620 / 295,763,131** | +183 files |
| `act-history` projection files / `sources` projection files | 557 / 19,670 | **587 / 19,823** | +30 / +153 |
| Source Library totals (`validate` exit 0) | 11,803 artifacts / 12,041 passages | **11,820 artifacts / 12,216 passages** | +17 / +175 |

---

## 3. Deduplicated Multi-Rite Research Expansion (Phase 3A)

Three net-new stage dossiers were deduplicated against `origin/main`'s Batch 4/5 work (avoiding any duplicate traditions, witnesses, or stages in `eastern-local-round2.json`, `romanian-blaj.json`, `iberian-historic-batch4.json`, `french-dioceses-{a,b}-batch4.json`, and `northern-central-regional.json`):

1. **Eastern Catholic Expansion (`src/sources/inventories/eucharistic-stages/eastern-expansion-2026-11.json`)**:
   - Added 3 net-new traditions (`belarusian-uniate`, `croatia-serbia-krizevci`, and `georgian-byzantine` non-*sui iuris* control), remapped Albanian and Macedonian additions onto `origin/main`'s `eastern-local-round2:{albanian,macedonian}`, and deepened `melkite`, `syro-malankara`, `hungarian`, `bulgarian`, and `macedonian` — adding **31 net-new stages, 26 transitions, and 11 gaps**, plus 5 new 1:1 `source_library_edition_id` links in `eastern-eucharistic-books-timeline-v1.toml`.
2. **Global, Missionary & Regional Adaptations (`src/sources/inventories/eucharistic-stages/global-mission-regional-2026-11.json`)**:
   - Added **13 traditions, 21 stages, 8 transitions, and 14 gaps** covering Mexico City 1561 (Espinosa), Peru/Lima 1583, Quebec 1703/1851, China 1615/1670/1949, Japan 1605 (ritual control), Goa/Diamper 1599, India 1969, Philippines, Brazil EP V 1974, Chiapas 2024, Broome Australia 2024, Ancient North Africa (Carthage control), and Eritrea Keren Blin–Ge'ez, plus concrete transitions for Zaire 1988 and Ordinariate BDW 2003→DWM 2015, and updated `regional-mission-permissions-2026-10-20.json` (+8 permissions, +3 non-admissions).
3. **Western Uses, Religious Orders & Cross-Tradition Relationships (`src/sources/inventories/eucharistic-stages/western-uses-orders-2026-11.json`)**:
   - Added **3 net-new traditions** (`lubeck-use`, `merseburg-use`, `benedictine-monastic`, omitting the 11 diocesan traditions already covered in Batch 4 / `northern-central-regional.json`), **33 net-new stages, 25 transitions, and 10 gaps** deepening Dominican, Carmelite, Carthusian, Premonstratensian, Augustinian, Servite, and Franciscan/Curial trajectories, 16 new 1:1 `source_library_edition_id` links in `western-eucharistic-books-timeline-v1.toml` (plus `paris-1481-dupre-huym` Canon passage bindings), and **+30 valid net-new East/West cross-tradition links** in `eucharistic-book-relationships-v1.toml` (62→92).
4. **Canonical Tradition Taxonomy (`src/sources/inventories/eucharistic-tradition-taxonomy-v1.toml`)**:
   - Classifies all **278 canonical traditions** into 10 rite families and 11 geographic regions with subregions for reader navigation (navigation metadata only, not canonical jurisdiction or lineage).

---

## 4. Seventeen Independently Collated Original-Language Native Constituents (Phase 3B)

Every newly installed literal liturgical constituent is US public domain by publication date, derived directly from a tracked facsimile in `src/sources/works/`, independently pixel-collated against rendered page images by a distinct reviewer (`reviewer != transcribed_by`, `independent: true`, `complete_extent_verified: true`), attributed in `THIRD_PARTY.md`, and aligned by shared canonical `native_path` slugs so `git diff --word-diff=color` produces minimal visual diffs across centuries. `origin/main`'s unreviewed `byzantine-greek-1738/1754/1873-chrysostom-anaphora` drafts remain untouched alongside our separately identified, reviewed `byzantine-1754-chrysostom-anaphora` and `byzantine-1873-chrysostom-anaphora` constituents (`*-strict-facsimile.toml`).

| Tradition & Family | Native Book ID | Lang | Units | Words | Independent Reviewer | Pixel Corrections Caught |
| --- | --- | :---: | ---: | ---: | --- | :---: |
| **Byzantine** (St. John Chrysostom) | `byzantine-1754-chrysostom-anaphora` | `grc` | 10 | 1,206 | `independent-collator-v1-byz-arm` | 26 across V1 |
| **Byzantine** (St. John Chrysostom) | `byzantine-1873-chrysostom-anaphora` | `grc` | 10 | 1,379 | `independent-collator-v1-byz-arm` | (included above) |
| **Armenian** (Badarak Anaphora) | `armenian-1642-badarak-anaphora` | `hy` | 6 | 759 | `independent-collator-v1-byz-arm` | (included above) |
| **Armenian** (Badarak Anaphora) | `armenian-1823-badarak-anaphora` | `hy` | 6 | 721 | `independent-collator-v1-byz-arm` | (included above) |
| **Alexandrian** (Coptic St. Basil) | `coptic-1736-basil-anaphora` | `cop` | 8 | 1,311 | `independent-collator-v3-alex-west` | 113 across V3 |
| **Alexandrian** (Ge'ez Apostles) | `geez-1914-apostles-anaphora` | `gez` | 6 | 652 | `independent-collator-v3-alex-west` | (included above) |
| **Western Latin** (Gregorian Hadrianum) | `gregorian-wilson-1915-canon-missae` | `la` | 14 | 574 | `independent-collator-v3-alex-west` | (included above) |
| **Western Latin** (Insular Stowe Missal) | `stowe-warner-1915-canon-missae` | `la` | 16 | 1,172 | `independent-collator-v3-alex-west` | (included above) |
| **Western Latin** (Paris 1481) | `paris-1481-canon-missae` | `la` | 16 | 838 | `independent-collator-v3-alex-west` | (included above) |
| **Western Latin** (Tarazona 1500) | `tarazona-1500-canon-missae` | `la` | 15 | 716 | `independent-collator-v3-alex-west` | (included above) |
| **East Syriac** (Chaldean Rome 1767) | `chaldean-1767-addai-mari` | `syr` | 8 | 457 | `independent-collator-v2-syriac` | 5 (6 sites) |
| **East Syriac** (Chaldean Mosul 1901) | `chaldean-1901-addai-mari` | `syr` | 8 | 545 | `independent-collator-v2-syriac` | 3 (4 words) |
| **East Syriac** (Syro-Malabar 1906) | `syro-malabar-1906-addai-mari` | `syr` | 8 | 440 | `independent-collator-v2-syriac` | 7 |
| **West Syriac** (Maronite Rome 1594) | `maronite-1594-anaphora` | `syr` | 5 | 106 | `independent-collator-v2-syriac` | 0 (clean) |
| **West Syriac** (Maronite Beirut 1908) | `maronite-1908-anaphora` | `syr` | 5 | 154 | `independent-collator-v2-syriac` | 0 (clean) |
| **West Syriac** (Syriac Cath. Rome 1843) | `syriac-1843-anaphora` | `syr` | 6 | 608 | `independent-collator-v2-syriac` | 2 |
| **West Syriac** (Syriac Cath. Sharfeh 1922) | `syriac-1922-anaphora` | `syr` | 6 | 582 | `independent-collator-v2-syriac` | 7 |

### Notable Primary-Source Discoveries Exposed by Independent Pixel Collation
- **Armenian Epiclesis shift (`1642` ↔ `1823`)**: Directly exposes the shift from Rome 1642 optative `արասցես` to Venice 1823 triple past-tense `արարեր` (following Rome 1677).
- **East Syriac 3-way Addai & Mari (`1767` ↔ `1901` ↔ `1906`)**: Directly verifies Fraction-placed Romanized *mysterium fidei* Institution in 1767 & 1906 vs Post-Sanctus relocation in Mosul 1901; Marian clause insertion in 1767 & 1906 vs removal in 1901; omission of `ܒܣܒܪܬܗ ܡܚܝܢܝܬܐ` in 1767 (PDF 333 / p. 285) vs presence in 1901 & 1906; and uncontracted analytic 1pl `ܘܡܫܒܚܝܢ ܚܢܢ` in Puttenpalli 1906 (`PDF 234`).
- **Maronite 314-year textual invariance (`1594` ↔ `1908`)**: `text/native/anaphoras/twelve-apostles/05-epiclesis-consecration.txt` is **0 bytes diff (100% SHA-256 identical)** across 314 years (`7c11417135875f9a032f9276b8b4541289a2e8f66ed02928a1bda59212bbed05`), directly confirming from primary scans the 1594 Romanized Epiclesis petition alongside 1908's expansion of Dialogue/Epiclesis incipits and insertion of `ܘܩܕܫ`.
- **Syriac Catholic Rahmani 1922 (`1843` ↔ `1922`)**: Direct pixel collation reveals extensive wording adjustments across Post-Sanctus, Institution Narrative, Anamnesis, and Epiclesis (`505 shared, −103 left, +77 right`), showing substantially deeper editorial intervention than Rahmani's conservative Latin preface implies.
- **Western Latin Canon divergences (`Gregorian` / `Stowe` / `Paris 1481` / `Tarazona 1500` ↔ `Rome 1570`)**: Directly exhibits archaic `nos tui serui ... domini dei nostri`, `et rege nostro`, Stowe's *Canón dominicus papę gilasi* & St. Patrick in *Nobis quoque*, Parisian cruciform-arms rubric before *Unde et memores*, and Tarazona's *Hic non dicitur: Amen:* rubric.

---

## 5. Diffable Git Corpus, Interactive Visual Diff Studio & Cross-Referencing

- **Engine & Diffable Git Corpus**:
  - `scripts/_eucharistic_history.py` emits `tradition_taxonomy` and `cross_references` in `catalogue.json`, writes `structure/act-history/edition-cross-references.json` (**84 canonical Source Library editions**), documents `## Visual Git Diffing` in every emitted Git corpus `README.md`, and exposes auto-discovered `diff_pairs` in `.triptych-act-history-corpus.json`.
  - `scripts/_eucharistic_stages.py` supports bounded constituents (`whole_book_complete == false`) covering one acquired witness of a multi-witness stage while keeping strict witness equality on whole-book bindings and rejecting out-of-stage witnesses.
  - `scripts/_eucharistic_texts.py` accepts `scan-pdf-page-range` and `facsimile-pdf` as direct facsimiles and preserves `origin/main`'s `_LazyLibraryRecords`, `_artifact_store`, and `_source_delivery_policy` alongside `replay_library(root, preloaded=...)`.
- **Interactive UI & Project-Wide Cross-Referencing**:
  - `src/web/browser/history/{index.html, history.css, history.js}`: retains `origin/main`'s 2026-11-16 `.section-green` / `--focus` / `--radius` / `--control-min` tokens and `❦` fleuron mark while adding 10 color-coded Rite-Family filter pills, Region/Search/Has-Text discovery bar, SVG Era Bands, inline-SVG legend, non-overlapping `TEXT` badges, sticky desktop detail drawer, multi-script `font-family` stacks (`syr`, `cop`, `gez`, `hy`, `grc`, `ar`), and an exact **Myers O((N+M)D) word-by-word Visual Diff Studio** with copyable `git diff --word-diff=color` commands.
  - Reverse cross-referencing wired across `structure/act-history/edition-cross-references.json` (84 editions), `src/web/browser/sources/{sources.js, sources.css}` ("In the Missal Timeline"), `src/web/browser/liturgy/{day.js, propers-reader.js}`, `library/{liturgy,history,traditional-latin-mass,novus-ordo-liturgy,law-and-church-discipline}.md`, and `docs/the-mass.md`, with two-sided URL contract tests in `tools/tests/test_browser_url_contract.py`.
- **Headless Chromium Visual Inspection (pre-rebase verification)**: 12 live screenshots (desktop `1440×960` and mobile `390×844`) confirmed `horiz_overflow=0px`, zero JS errors, non-overlapping SVG badges, Myers word-by-word diffs, live `sources/` back-links, and Syriac RTL (`dir="rtl"`, `lang="syr"`) layout. Container Linux lacks installed Syriac/Coptic/Ethiopic system fonts, so glyph shaping for `syr`/`cop`/`gez` relies on the explicit client `font-family` stacks in `history.css`.

---

## 6. Verification Gates & Candid Remaining Boundaries

- `./tools/source-library validate`: **PASS** (`artifact=11820 corpus=5 edition=14565 passage=12216 segment=10858 work=11109 bindings=5346`, 0 errors).
- `./tools/missal-coverage-reconciliation`: **PASS** (`0` findings; 458 Eastern, 1,535 Western, 42 dossiers, 278 traditions, 568 stages, 175 transitions, 318 gaps).
- `./tools/tpt browser-products audit --family act-history --family sources`: **PASS** (0 outside/excluded/unaudited reads).
- `./tools/tpt browser-products record && ./tools/tpt browser-products check --json`: **PASS** (two independent cold builds agreed byte-for-byte across all 13 families, `30,620` files, `295,763,131` bytes).
- `./tools/corpus-index refresh --readers && ./tools/corpus-index refresh`: **PASS** (`85,769` files, `60,573` records).
- Scoped `make refresh-release-bindings ONLY="..."` + `./tools/release-bindings status`: **PASS** (`0 stale binding(s)` across our exact 19 modified site sources).
- Automated test suites: `test_act_history_replay` (11/11), `test_eucharistic_stages` (39/39), `test_eucharistic_texts` (47/47), `test_browser_url_contract` (67/67), `test_act_history_structure` (13/13), `test_eucharistic_history` (55/55), `test_history_catalogue` (67 passed / 1 optional skip), `test_act_history_inheritance` (6/6), `test_act_history_preview` (27/27), `test_source_reader` (31/31), `test_missal_coverage_reconciliation` (15/15) — **0 failures on any touched component**. Pre-existing unrelated baseline failures on `origin/main` in `test_browser_collisions` (`catena/catena.css`, `shared/publication-reader.css`) and `test_day_missal_integration` (Roman Ordinary counts `(6, 204, 11)` vs `(6, 196, 9)` and `resultStateForBranch`) are unchanged from `origin/main`.
- `scripts/check_tracked_ignored_paths.py`, `./tools/tpt --check` (`registry ok: 64 tools`), and `git diff --check`: **PASS**.
- Local Pages deploy gates (`make check-corpus-index`, `make check-deployment-sources`, `make public-site`, `./tools/tpt public-alpha verify --deployment-target github-pages`): executed prior to push and recorded in commit/publication summary.

### Candid Remaining Boundaries (Why `all-rite-missal-timeline-2026-10-16` Remains `in_progress`)
1. **Whole-book transcription**: Every newly installed constituent is an explicitly declared **bounded constituent** (core Anaphora or *Canon Missae*; `text_coverage: "partial"`). Whole-book transcription and independent pixel collation of 300–1,000-page historical missals remains open (`0` whole-book complete stages).
2. **Post-1930 copyrighted liturgical books**: Contemporary approved missals remain protected by copyright and are represented strictly by sourced metadata, structural stage dossiers, and non-text research summaries under `guidance/liturgical-text-publication-policy.md`.
3. **Unacquired primary archival books & copy-to-copy textual parentage**: 318 explicitly documented archival gaps remain, along with copy-to-copy typesetting parentage between parentless `version/*` roots in Git and the separate unreviewed Greek Chrysostom drafts on `main`.
4. **Print PDF & live screen-reader verification**: Print companion PDFs and live assistive-technology runs were not re-executed in this pass.
