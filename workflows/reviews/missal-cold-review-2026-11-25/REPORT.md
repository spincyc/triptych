# Missal Timeline Cold Review, Multi-Rite Expansion & Diffable Original-Language Corpus Report (2026-11-25)

- **Branch**: `feature/missal-timeline` (base checkpoint `fe1cf06ac9`; local commit only — not pushed, `main` untouched, no deployment).
- **Scope**: Cold architectural, historical, textual, corpus, visual, and cross-referencing review of Triptych's Missal Timeline (`tools/act-history`, `scripts/_eucharistic_*.py`, `src/sources/inventories/`, `src/sources/works/`, `src/web/browser/history/`, and sibling routes), followed by multi-lane research expansion, independent pixel-collated original-language constituent transcription across all six Catholic liturgical traditions, deterministic Git corpus verification, and live headless Chromium inspection.
- **Governing policies**: `guidance/time-machine.md`, `guidance/act-histories.md`, `guidance/sources.md`, `guidance/liturgical-text-publication-policy.md`, and `THIRD_PARTY.md`.

---

## 1. Cold Review Findings on Base Checkpoint `fe1cf06ac9`

A full code, source-inventory, corpus, and visual cold review of `fe1cf06ac9` established that Triptych's underlying epistemic model (distinguishing acts from printings, coexistence from reception, acquisition from verified transcription, and Git parentage from textual similarity) is exceptionally rigorous, while surfacing six concrete structural gaps:

1. **Severe projection & test performance bottleneck**: `tools/act-history structure --check` required >9 minutes (and `test_act_history_structure.py` >42 minutes) because every adapter load re-walked `tree_fingerprint()` and re-hashed >520 MB of tracked facsimiles (~120 repeated SHA-256 passes).
2. **Original-language native text skewed heavily Western**: Only `11` native-book constituents existed (10 Latin — Cistercian 1606/1657, Mozarabic 1500/1755/1804, Roman 1570 — plus 1 Arabic Creed in Tuki 1736), leaving **zero** native-book constituents in Greek (`grc`), Classical Armenian (`hy`), Bohairic Coptic (`cop`), Classical Ethiopic (`gez`), or Classical Syriac (`syr`), despite tracked public-domain facsimiles already sitting in `src/sources/works/`.
3. **Research & geographic coverage gaps**: Several *sui iuris* Eastern Churches lacked dedicated timelines (Macedonian, Belarusian, Križevci/Croatia–Serbia, Albanian archival control, plus shallow coverage on Melkite, Romanian/Blaj, Syro-Malankara, and Hungarian); global & missionary Roman/Eastern history (New Spain 1561, Lima 1583, Quebec, China 1615/1670/1949, Goa/Diamper 1599, India 1969, Philippines, Brazil, Chiapas, Broome, Eritrea/Keren) and 11 uncovered Western diocesan/monastic routes lacked staged sequences; and 21 acquired canonical `edition.*` records in `src/sources/works/` were unlinked in the Eastern/Western timelines.
4. **Factual primary-source locus error in existing Chaldean 1767 metadata**: Direct pixel inspection of `artifact.chaldean-catholic-church.missale.1767-rome-propaganda.google-scan-pdf-4d048b31` (independently confirmed by both Lane T2 and Lane V2) established that Addai & Mari Gehanta 3 (omitting the life-giving Gospel phrase) lies on **PDF p. 333 / printed p. 285 (`ܪܦܗ`)** rather than PDF p. 339 / printed p. 284 (PDF 339 is printed p. 279 `ܪܥܛ`, a pre-anaphoral litany), and that Mosul 1901 (`PDF 67`) and Puttenpalli 1906 (`PDF 234`) both print pure Syriac feminine **`ܒܣܒܪܬܗ ܡܚܝܢܝܬܐ`** (*b-sḇarṯēh mḥayyānīṯā*) rather than the Greek loanword `ܒܐܘܢܓܠܝܘܢܗ ܡܚܝܢܐ`.
5. **Single-witness stage rigidity**: `scripts/_eucharistic_stages.py` and `src/web/browser/history/history.js` previously required `binding["catalogue_witness_ids"] == stage["witness_ids"]` even for partial `constituent` bindings, preventing honest single-witness transcription on multi-witness stages (such as Chaldean 1901 Ordinary + Companion Propers or Maronite Dibs 1888 / 1908 second printing).
6. **Reader navigation, visual diffing, and cross-site discoverability**: The timeline lacked rite-family and geographic-region browsing controls, era orientation bands, an inline word-by-word Visual Diff Studio with reproducible `git diff --word-diff=color` commands, and reverse cross-links from the Source Library (`sources/`), Liturgical Day / Propers Reader (`liturgy/`), and narrative library catalogues (`library/*.md`, `docs/the-mass.md`).

---

## 2. Quantitative Before / After Summary

| Metric | Base `fe1cf06ac9` | Current (`feature/missal-timeline`) | Delta |
| --- | ---: | ---: | ---: |
| Stage dossiers (`src/sources/inventories/eucharistic-stages/`) | 36 | **39** | +3 |
| Canonical traditions mapped | 156 | **188** | +32 |
| Rite-family / Geographic-region taxonomy | unindexed | **10 rite families · 11 regions (188/188)** | new |
| Documented + provisional book stages | 295 | **418** | +123 |
| Evidenced transitions | 77 | **154** | +77 (2.0×) |
| Declared research gaps | 203 | **249** | +46 |
| Stages with pixel-verified native text (`partial`) | 16 | **30** | +14 |
| Catalogue entries (Eastern / Western / Legacy) | 1,962 (446 / 1,457 / 59) | **1,987** (449 / 1,479 / 59) | +25 |
| Typed cross-tradition relationships | 62 | **112** | +50 |
| **Native-book constituents (`eucharistic-books/`)** | 11 | **28** | **+17** |
| **Native liturgical languages represented** | 2 (`la`, `ar`) | **7** (`la`, `syr`, `grc`, `hy`, `cop`, `gez`, `ar`) | **+5 scripts** |
| **Catholic liturgical traditions with native text** | 2 (Latin, Coptic-Arabic) | **All 6** (Latin, Byzantine, Armenian, Alexandrian, East Syriac, West Syriac) | **6 / 6** |
| **Total canonical native units / words** | 235 units | **388 units · 17,621 words** | +153 units |
| **Source-hashed witness comparisons** | 31 | **43** | +12 |
| **Generated Git corpus refs (`version/` + `reconstruction/`)** | 37 | **71** (28 `version/` + 43 `reconstruction/`) | +34 |
| **Auto-discovered Git visual `diff_pairs`** | — | **21** | new |
| **Source Library ↔ Timeline reverse cross-links** | 0 | **80 canonical editions** | +80 |
| Source Library totals (`validate` exit 0) | 3,579 artifacts / 5,693 passages | **3,603 artifacts / 5,868 passages** (3,497 readable) | +24 / +175 |
| `act-history structure --check` runtime | >540 s (>9 min) | **~39 s** | **~14× faster** |

---

## 3. Multi-Rite Research Expansion (Phase 3A)

Three independent research lanes expanded historical and geographic coverage while preserving Triptych's strict evidence boundaries (no fabricated decrees, no unverified ancestry, explicit archival controls):

1. **Eastern Catholic Expansion (`src/sources/inventories/eucharistic-stages/eastern-expansion-2026-11.json`)**:
   - Added five traditions (`albanian` [honest 0 stages + 2 archival gaps], `macedonian` [2009 *recognitio*], `belarusian-uniate`, `croatia-serbia-krizevci`, and `georgian-byzantine` non-*sui iuris* control) and deepened `melkite` (1→13 stages), `romanian-blaj` (2→8), `syro-malankara` (2→7), `hungarian` (2→6), and `bulgarian` (+1) — adding 38 stages, 31 transitions, and 11 gaps, plus 5 new 1:1 `source_library_edition_id` links in `eastern-eucharistic-books-timeline-v1.toml`.
2. **Global, Missionary & Regional Adaptations (`src/sources/inventories/eucharistic-stages/global-mission-regional-2026-11.json`)**:
   - Added 13 traditions covering Mexico City 1561 (Espinosa), Peru/Lima 1583, Quebec 1703/1851, China 1615/1670/1949, Japan 1605 (ritual control), Goa/Diamper 1599, India 1969, Philippines, Brazil EP V 1974, Chiapas 2024, Broome Australia 2024, Ancient North Africa (Carthage control), and Eritrea Keren Blin–Ge'ez, plus concrete transitions for Zaire 1988 and Ordinariate BDW 2003→DWM 2015 — adding 21 stages, 8 transitions, 14 gaps, and updating `regional-mission-permissions-2026-10-20.json` (+8 permissions, +3 non-admissions).
3. **Western Uses, Religious Orders & Cross-Tradition Relationships (`src/sources/inventories/eucharistic-stages/western-uses-orders-2026-11.json`)**:
   - Added 14 traditions mapping 11 previously uncovered Iberian/French/German diocesan routes (Zaragoza, Valencia, Tarragona, Urgell, Toulouse, Tours, Verdun, Meaux, Bordeaux, Grenoble, Halberstadt, Lübeck, Merseburg) plus `benedictine-monastic`, and deepened Dominican, Carmelite, Carthusian, Premonstratensian, Augustinian, Servite, and Franciscan/Curial trajectories — adding 64 stages, 38 transitions, 21 gaps, 16 new 1:1 `source_library_edition_id` links in `western-eucharistic-books-timeline-v1.toml`, and +50 East/West cross-tradition links in `eucharistic-book-relationships-v1.toml` (62→112).
4. **Canonical Tradition Taxonomy (`src/sources/inventories/eucharistic-tradition-taxonomy-v1.toml`)**:
   - Classifies all **188 traditions** into 10 rite families and 11 geographic regions with subregions for reader navigation (explicitly navigation metadata, not canonical jurisdiction or textual lineage).

---

## 4. Seventeen Independently Collated Original-Language Native Constituents (Phase 3B)

Every new literal liturgical text is US public domain by publication date, derived directly from a tracked facsimile in `src/sources/works/`, independently pixel-collated against rendered page images by a distinct reviewer (`reviewer != transcribed_by`, `independent: true`, `complete_extent_verified: true`), attributed in `THIRD_PARTY.md`, and aligned by shared canonical `native_path` slugs so `git diff --word-diff=color` produces clean minimal diffs across centuries.

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

## 5. Deterministic Diffable Git Corpus, Visual Verification & Cross-Referencing

- **Deterministic Git Corpus Proof**: Two independent fresh exports (`tools/act-history corpus --out ... --json`) produced **100% byte-identical `git show-ref` OIDs across all 71 branches** (`28 version/*` + `43 reconstruction/*`), passed **`git fsck --strict` across all 6,951 Git objects**, exposed **21 auto-discovered `diff_pairs`** in `.triptych-act-history-corpus.json` and `README.md`, and produced clean minimal `git diff --word-diff=plain` output across every aligned pair in all six liturgical traditions.
- **Engine & Browser Architecture**:
  - Scoped `session_cache(root)` + streaming 1 MB `(path, mtime_ns, size)` digest cache in `scripts/_eucharistic_texts.py` and `scripts/_eucharistic_history.py` reduced `tools/act-history structure --check` from >9 minutes to ~39 seconds with zero side effects and bit-identical projections.
  - Multi-witness constituent support in `scripts/_eucharistic_stages.py` and `src/web/browser/history/history.js` allows a bounded constituent (`whole_book_complete == false`) to bind cleanly to one acquired witness of a multi-witness stage while continuing to enforce strict witness equality on whole-book bindings and rejecting out-of-stage witnesses.
  - Interactive UI upgraded (`src/web/browser/history/{index.html, history.css, history.js}`): unified `.section-green` palette, 10 color-coded Rite-Family filter pills, Region/Search/Has-Text discovery bar, SVG Era Bands, crisp inline-SVG legend, non-overlapping `TEXT` badges, sticky `44%` desktop detail drawer, multi-script `font-family` stacks, and an exact **Myers O((N+M)D) word-by-word Visual Diff Studio** with copyable `git diff --word-diff=color` commands.
  - Reverse cross-referencing wired across `src/web/data/structure/act-history/edition-cross-references.json` (80 editions), `src/web/browser/sources/{sources.js, sources.css}` ("In the Missal Timeline"), `src/web/browser/liturgy/{day.js, propers-reader.js}`, `library/{liturgy,history,traditional-latin-mass,novus-ordo-liturgy,law-and-church-discipline}.md`, and `docs/the-mass.md`.
- **Headless Chromium Visual Inspection**: 12 live screenshots captured inside standard sandbox mode (desktop `1440×960` and mobile `390×844`) verified `horiz_overflow=0px`, zero application JS errors, non-overlapping SVG `TEXT` badges, crisp Latin/Greek/Armenian/Arabic rendering, exact Myers word-by-word diffs, live `sources/` back-links, and Syriac RTL (`dir="rtl"`, `lang="syr"`) layout and multi-witness stage rendering on `maronite-dibs1888`. **Observed environment limit**: the headless Linux container ships DejaVu/Adwaita fonts without Syriac/Coptic/Ethiopic system fonts, so glyph shaping for `syr`/`cop`/`gez` could not be visually inspected in container screenshots; explicit language-scoped `font-family` fallbacks were added in `history.css` for desktop/mobile browsers carrying Noto/Estrangelo/Abyssinica/Antinoou fonts.

---

## 6. Verification Gates & Candid Remaining Boundaries

All repository gates pass cleanly on the final tree:
- `./tools/source-library validate`: **PASS** (`artifact=3603 corpus=5 edition=1236 passage=5868 segment=113 work=1054 bindings=3955`, 0 errors).
- `./tools/missal-coverage-reconciliation`: **PASS** (`0` findings; 449 Eastern, 1,479 Western, 39 dossiers, 188 traditions, 418 stages, 154 transitions, 249 gaps).
- `./tools/source-reader structure && ./tools/source-reader check --json`: **PASS** (`4,734` files, `3,497` readable, `2,371` withheld, `0` library errors).
- `./tools/act-history structure && ./tools/act-history structure --check`: **PASS** (`578` files, `0` drift).
- Full automated test suite (**13/13 suites, 403 tests: 402 passed, 1 optional skip, 0 failures, 0 errors**): `test_eucharistic_stages` (39), `test_eucharistic_history` (55), `test_eucharistic_texts` (47), `test_act_history_inheritance` (6), `test_act_history_preview` (27), `test_missal_coverage_reconciliation` (15), `test_history_catalogue` (67 passed / 1 optional skip), `test_browser_url_contract` (64), `test_browser_collisions` (15), `test_source_reader` (31), `test_day_missal_integration` (13), `test_chronology_binding_sources` (10), `test_act_history_structure` (13).
- `./tools/tpt --check`: **PASS** (`registry ok: 45 tools`).
- `git diff --check`: **PASS** (0 whitespace or conflict issues).

### Candid Remaining Boundaries (Why `all-rite-missal-timeline-2026-10-16` Remains `in_progress`)
1. **Whole-book transcription**: Every newly installed constituent is an explicitly declared **bounded constituent** (core Anaphora or *Canon Missae*; `text_coverage: "partial"`). Whole-book transcription and independent pixel collation of 300–1,000-page historical missals (Ordinary + Propers + Lectionary + Calendar + Rubrics) remains open (`0` whole-book complete stages).
2. **Post-1930 copyrighted liturgical books**: Contemporary approved missals (post-Vatican II Roman Missal typical editions, ICEL 2010, Ambrosian 2024, Chaldean 2014/2020/2025, Maronite 1992/2005, Syro-Malabar Qurbana 1962/1989/2021, Ruthenian/Ukrainian/Melkite/Romanian modern editions, Zaire 1988, Ordinariate DWM 2015) remain protected by copyright and are represented strictly by sourced metadata, structural stage dossiers, and non-text research summaries under `guidance/liturgical-text-publication-policy.md`.
3. **Unacquired primary archival books & copy-to-copy textual parentage**: 249 explicitly documented archival gaps remain (including Albanian Byzantine celebrant books, unacquired 16th–18th-century regional missals, and copy-to-copy typesetting parentage between parentless `version/*` roots in Git).
4. **Print PDF & spoken screen-reader verification**: Print companion PDFs and live assistive-technology screen-reader runs were not re-executed in this pass.
