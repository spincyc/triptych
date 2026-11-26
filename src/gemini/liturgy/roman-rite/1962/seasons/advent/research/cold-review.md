# Fresh-Reader Verification and Cold Review — 1962 Roman Rite Advent Seasonal Handbook (Gemini Edition)

- **Document:** `gemini/liturgy/roman-rite/1962/seasons/advent` (*Keeping Advent: A Companion to the 1962 Roman Rite*)
- **Initial Review Date:** 2026-11-26
- **Post-Cold-Review Revision Date:** 2026-11-26
- **Scope of Review:** Voice and register audit against `guidance/editorial.md`; quotation fidelity audit against `src/sources/`; liturgical, canonical, and calendar walkthroughs across all 7 Advent opening shapes; independent cold-review remediation (`B1`–`B4` and `A1`–`A7`); web-edition conversion check; and print-PDF visual inspection.

---

## 1. Voice, Gravity, and Wonder Check (`guidance/editorial.md`)

A full read and automated scan across all 12 body chapters (`01`–`12`) and 4 appendices (`90`–`99`) checked for banned meta-prose, defensive hedging, AI jargon, repetition, and mechanical phrasing:

| Check | Scope | Result | Notes |
| --- | --- | --- | --- |
| `(gloss: ...)` inline glosses | All 16 `.tex` files | **0 hits** | Every Latin phrase is translated smoothly inside the English sentence. |
| AI/audit jargon (`formulary`, `element` as jargon, `lane`, `locus`, `binding` as jargon, `witness` in body prose) | Ch. 1–12 | **0 hits** | House-voice preflight reports 0 hits; manual pass also cut process self-narration (`05:45`) and moved apparatus/editor notes from Ch. 3, 5, 10, 11 to Appendix C/D. |
| Defensive secular hedging & guidance-echo negations | All 16 `.tex` files | **0 hits** | Rewrote Ch. 12 Luke 2:7 / 23:53 discussion affirmatively; removed closing restating maxim in Ch. 10. |
| Verbatim cross-chapter duplication | Ch. 1–12 | **Resolved** | Assigned each signature quote one primary home (Gregory *Hom.* 1.3 in Ch. 6; Vigil Collect `massbox` in Ch. 11; Leo *Sermon 13* in Ch. 8; Durandus *Rationale* VI.2 in Ch. 3; Is 1:16–18 in Ch. 5; Luke 3:4–6 in Ch. 10; *Rorate* v. 4 in Ch. 11; *Admirabile signum* in Ch. 12; Nazianzen *Or.* 38.17 in Ch. 6) with concise recalls elsewhere. |
| Blockquote & orthography consistency | All 16 `.tex` files | **Pass** | Removed all 14 trailing `\hfill ---` attributions in Ch. 9–12 (folding short citations into lead-in prose matching Ch. 1–8); harmonized `Isaiah`, `Ecclus`/`Agg`, Day-Month dates (`24 December`), `Rorate caeli`, `St.~`, and running-case prayer openings. |

---

## 2. Independent Cold-Review Remediation Record (`B1`–`B4`, `A1`–`A7`)

Every author-side blocking and advisory finding from the independent cold review was resolved and re-verified:

- **B1 (Latin *Benedictus* upstream `latVUC` typo):** Corrected `sicut locutum est` to **`sicut locutus est`** (`sections/92-received-prayers.tex`), collated against tracked liturgical witnesses (Bruno of Würzburg in Migne PL 142 and Blunt 1866), cited in Appendix C and Appendix D, and recorded as `catch-007` in `research/source-audit.md` and `research/source-bindings.toml`.
- **B2 (`source-audit.md` contradiction, unused bindings/references, omitted Chrysostom homily):**
  - Corrected `catch-001` in `research/source-audit.md` to exact 1962 Latin **`Qui tecum vivit et regnat in unitate`** and Lefebvre 1925 p. 339 **`Who liveth and reigneth with Thee`**.
  - Pruned all unused research-dossier passages and artifacts from `research/source-bindings.toml`, `research/source-audit.md`, and `sections/99-references.tex` (reducing bindings cleanly to strictly relied-upon sources), corrected St. Alphonsus and Aquinas `III, q. 1, a. 1` section tags to `App. A`, and added **St. John Chrysostom, Homily XXXVI on Matthew** to `sections/99-references.tex`, `research/source-audit.md`, and `research/source-bindings.toml`.
- **B3 (Three factual/liturgical slips):**
  - `03-how-the-church-learned-to-wait.tex`: Corrected Third Plenary Council of Baltimore to **1884** (published in its 1889 *Manual of Prayers*).
  - `06-first-week.tex`: Ended the Advent I Mass Epistle quote (`Rom 13:11–14`) accurately at *"put ye on the Lord Jesus Christ"*, leaving the full v. 14 text in Augustine's *Confessions* VIII.12.29.
  - `10-fourth-week-and-great-antiphons.tex`: Qualified Week IV Thu/Fri Isaiah 64 and 66 to longer Advents (2 of 7 and 1 of 7 shapes under RGBR n. 213) alongside the everyday home course in Appendix A.
- **B4 (Orphaned `\hfill ---` attribution lines in Ch. 9–12):** Removed all 14 standalone `\hfill ---` lines after `\end{quote}` across Chapters 9–12 and folded attributions into introducing prose, eliminating both the orphaned attribution on printed p. 24 and bare left-aligned `— Author` lines in web Markdown.
- **A1–A7 (All advisories):** Tightened Ch. 5 self-narration (A1); moved manuscript shelfmarks, sigla, and editor/translator notes from Ch. 3, 5, 10, 11 into Appendix C/D (A2); deduplicated cross-chapter verbatim quotes (A3); cut restating maxim and defensive negations and broke up authority-stacked paragraphs (A4); refined 6 liturgical clarifications in Ch. 3, 9, 10, 12 (A5); added Table 1 Ember pointer rows, consistent Table 2 Ember overlays, `(from Week IV Matins)`, and `\Needspace{10\baselineskip}` before Section A.3 in Appendix A (A6); harmonized orthography, dates, prayer box headers, and decorative drop-caps (A7).

---

## 3. Practical Calendar & Reader Walkthroughs

| Scenario | Walkthrough Result |
| --- | --- |
| **Latecomer arriving on 19 December** | Ch. 1 sends the latecomer straight to Appendix A without guilt (Matt 20:6–14). Appendix A opens directly to Table 2 (`19 December: O Radix Jesse`) with consistent Sun IV and Ember overlay triggers. |
| **8 December on Sunday II (e.g., 2024, 2030)** | Ch. 7, Appendix A, and `research/calendar-verification.md` agree: Immaculate Conception (I cl., RG n. 91 row 4) wins over Sunday II (I cl., row 6); Sunday II receives the single privileged commemoration (RG nn. 15, 109 a, 111 a). |
| **17 December on Gaudete Sunday & 24 December on Sunday IV (e.g., 2023, 2028, 2034)** | Ch. 10, Ch. 11, and Appendix A agree: *O Sapientia* is sung at Vespers of Sunday III (17 Dec); on 24 December the Vigil of the Nativity (I cl., row 5) replaces Sunday IV outright with **no commemoration** (RG n. 30 a). |
| **21 December St. Thomas colliding with Ember Friday/Saturday vs. Sunday IV** | Ch. 9, Ch. 10, and Appendix A agree: St. Thomas (II cl., row 16) wins over Ember Friday/Saturday (II cl. feria, row 18) with privileged commemoration (RG n. 109 e), but yields to Sunday IV (I cl., row 6) when Advent I falls on 30 November. |

---

## 4. Build, Schema, Web-Edition, and Print Visual Inspection

- **Document Schema (`./tools/document-schema check --phase content`):** 0 content schema errors.
- **Generation Metadata (`./tools/check-generation-metadata --provider gemini`):** Valid.
- **House-Voice Preflight (`./tools/check-content-preflight --check house-voice`):** 0 errors.
- **Web-Edition Declaration & Conversion (`./tools/check-web-edition` + `./tools/web-edition check`):** Valid (`eligible`), 0 conversion or quotation-audit errors.
- **Source Library Validation (`./tools/source-library validate`):** 0 errors across all pruned, canonically fingerprinted bindings.
- **PDF Visual Inspection (`pdflatex` via `./tools/print-document build`, rendered at 150 DPI via `pdftoppm`):**
  - Unbroken `massbox` styling via `\renewtcolorbox{massbox}[1]{...}` in `format.tex` paired with split Latin/English boxes for long hymns (*Creator alme siderum*, *Rorate caeli*) keeps every prayer box intact on one page.
  - Post-fix visual inspection confirmed zero orphaned blockquote attributions in Ch. 9–12, clean Section A.3 page break (`\Needspace{10\baselineskip}`), corrected Latin *Benedictus* (`sicut locutus est`), crisp tables, zero undefined references, and a balanced closing page with no colophon-only spill.
