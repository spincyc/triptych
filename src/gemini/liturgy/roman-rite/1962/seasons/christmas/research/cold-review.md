# Fresh-Reader Verification and Cold Review — 1962 Roman Rite Christmas Seasonal Handbook (Gemini Edition)

- **Document:** `gemini/liturgy/roman-rite/1962/seasons/christmas` (*Keeping Christmas: A Companion to the 1962 Roman Rite*)
- **Review Date:** 2026-11-27
- **Scope of Review:** Voice and register audit against `guidance/editorial.md`; quotation, Collect, and Breviary fidelity audit against `src/sources/`; liturgical, canonical, and calendar walkthroughs across all 7 weekday shapes of 25 December (2020/2021–2120/2121); Pandoc web-edition inspection; and `native-print-compile` (pinned `wasmtex-2026-47ff73bab1a2e548`) + `check-pdf-anchors` + visual PNG page inspection.

---

## 1. Voice, Gravity, and Wonder Check (`guidance/editorial.md`)

A complete review and automated scan across all 12 body chapters (`01`–`12`) and 4 appendices (`90`–`99`) checked for banned meta-prose, AI/audit jargon, inline glosses, orphaned attributions, and repetition:

| Check | Scope | Result | Notes |
| --- | --- | --- | --- |
| `(gloss: ...)` inline glosses | All 16 `.tex` files | **0 hits** | Every Latin liturgical phrase is rendered smoothly inside the English sentence. |
| House-voice preflight (`tools/check-content-preflight --check house-voice`) | All 17 reader-facing files (incl. `main.tex` & scope appendix) | **0 errors** | Removed early draft phrase `"The liturgical horizon of this handbook"` in Ch. 3; replaced two occurrences of `"formulary"` in Ch. 10 and App. A with `"Mass"`. |
| Orphaned `\hfill ---` blockquote attributions | All 16 `.tex` files | **0 hits** | Every quotation attribution is folded cleanly into lead-in prose. |
| Dropped Pandoc wrappers (`\noindent{\footnotesize ...}`, nested `\textit{}`) | All 16 `.tex` files | **0 hits** | Caught and fixed one nested `\textit{Mass (\textit{Vultum tuum}):}` in App. A Table 2 (`sections/90-daily-course.tex`), eliminating raw asterisk nesting in Markdown. |
| Raw Markdown syntax in `.tex` | All 16 `.tex` files | **0 hits** | Caught and fixed a draft Markdown italic note under the St. Sylvester Collect in Ch. 9 (`sections/09-days-within-the-octave-thomas-sylvester.tex`), replacing it with the verified Lasance Common of Supreme Pontiffs English Collect inside the `massbox`. |

---

## 2. Independent Cold-Review Remediation Record (`B1`–`B7` and Advisories)

Every blocking finding (`B1`–`B7`) and advisory from the independent read-only cold review was resolved and re-verified on committed HEAD:

- **B1 (Second Vespers of 25 December, `06-dawn-and-day-masses.tex`):** Removed the pre-1960 commemoration of St. Stephen at Second Vespers of Christmas. Under 1960 *Codex Rubricarum* RG 108–111, ordinary commemorations never occur at Vespers and II cl. feasts of saints have no First Vespers; Second Vespers of Christmas admits at most one privileged commemoration of the Sunday within the Octave when 26 December falls on a Sunday.
- **B2 (Pre-1960 Breviary anachronisms, `08`, `09`, `90-daily-course.tex`):**
  - On the Sunday within the Octave, specified under RGBR 162 a and 220 b that 1962 Sunday Matins has 3 lessons total where Lesson III is strictly the former Lesson VII (St. Ambrose on Simeon, Bute p. 304), whereas Anna (`Ambrose II.62`, Bute p. 305) was the former Lesson IX in pre-1960 Breviaries and `II.58` is outside the Breviary.
  - On 29 and 31 December, explicitly qualified St. Thomas of Canterbury's Lesson VI (not V–VI), St. John Chrysostom's Homily 59, and St. Sylvester's Lesson VI (*Feria*) as belonging to the traditional pre-1960 Roman Breviary Office (Pustet 1888 / Bute 1908), since the universal 1962 Breviary keeps the Octave Office with only a Lauds commemoration on those days.
- **B3 (St. Thérèse of Lisieux, `04-prayer-home-and-feasting.tex`):** Replaced the non-Taylor quotation `"fortunately this is the last year!"` with clean indirect narration honoring `chapter-v-christmas-1886.toml`, and removed the De la Fuente footnote quote from St. Teresa's paragraph.
- **B4 (Eliminated all unattributed English translations in quotation marks):** Replaced every unattributed English quotation with either verbatim tracked human translations—Bute 1908 (Gregory *Homily* 8 p. 276, *Kalenda* p. 269, *Cum ortus fuerit* p. 272, *Hodie per totum mundum* p. 273, Ambrose Lesson VII p. 304 & IX p. 305, 1 January Martyrology p. 309 `"Octave of the Lord's Birth"`, Jan 1 R6 & R8 pp. 313–314), Lasance 1945 (Midnight Secret, Day Alleluia p. 144 & Postcommunion, Jan 1 Postcommunion, *Vultum tuum* pp. 1404–1405), and Lefebvre 1925 (*Communicantes* `"in which"`, pp. 59–60)—or clean unquoted prose paraphrases (Gregory *Homily* 8 second half, Ambrose *Exp. in Luc.* II.41 & II.58, Peter Chrysologus *Sermons* 148 & 155, Dawn Secret, and Nativity Preface). Corrected `99-references.tex` so Bute p. 276 is cited only for the opening excerpt of Gregory *Homily* 8.
- **B5 (Complete 1 January Mass Collect, `10`, `92`, `95`, `99`):** Replaced truncated Bute p. 211 (Compline *Alma Redemptoris* form) in the 1 January Mass Collect with Bute 1908 p. 315 containing the full Trinitarian doxology, keeping p. 211 solely in the Compline *Alma Redemptoris Mater* block.
- **B6 (St. Cyril of Alexandria sermon numbering, `10`, `90`, `99`, `scope.md`, `source-bindings.toml`):** Audited `cyril-on-luke-01-sermons-01-11-36441dbd/source.html` directly (TOC and `<A NAME="C3">SERMON III. [From Aubert.] cc. 2:21-24</A>` confirm the Circumcision / Joshua flint-knives passage stands in **Sermon 3**, while the manger as altar stands in **Sermon 1**, Luke 2:1–7) and unified every mention on **Sermons 1 and 3**, eliminating the erroneous `"Sermon 5"` in Appendix A and `scope.md`.
- **B7 (Calendar arithmetic, `calendar-verification.md`):** Corrected Mon–Fri 5 January from `58/101` to **`73/101 seasons`** (`73 Mon–Fri + 14 Sat + 14 Sun = 101`).
- **Advisories (all 7 resolved):** Replaced `2--5 January` with `2–5 January` in `publication.toml` (`pdfsubject`) and refreshed `main.tex`; pruned uncited St. Jerome *Commentary on Matthew* and *De viris illustribus* from `99-references.tex`; supplied exact numbered loci across Appendix A (`Jerome Comm. in Gal. III.6`, `Irenaeus Adv. Haer. III.3.3`, `Durandus Rationale VI`, `Alphonsus Discourse on the Name of Jesus pp. 151–163`, `Ambrose Exp. in Luc. II.53` introduced in Ch. 12, and parish/Breviary *Te Deum* clarification); fixed binding loci for Chesterton (**Ch. VII**), St. Thérèse (**p. 100**), Gregory Nazianzen (**§16**), and Aquinas (**`III.35.7.reply-1` & `reply-3`**); smoothed meta/seminar phrases in Ch. 1, 5, 11, and App. C; tightened em-dash spacing in `92-received-prayers.tex:455` and verified Pustet 1888 p. 207 *Salvete flores Martyrum* doxology.

## 3. Earlier Pre-Commit Liturgical & Textual Verification Catches

1. **Holy Innocents (28 December) in 1962:** Verified directly against 1960 *Codex Rubricarum* (RG 124 e, RG 137, RGMR 431 a, 507) and 1962 *Missale Romanum* pp. 27–28 (unit 186): red vestments unconditionally, folded chasubles abolished, and *Gloria*, *Te Deum*, *Alleluia* (*Laudate, pueri*), and *Ite, missa est* used whenever the feast is celebrated (discarding Lasance 1945 p. 153's obsolete pre-1960 violet heading).
2. **Non-Holy-Name Saturdays in 2–5 January (`missa-de-s-maria-in-sabbato-2`):** Verified directly in `tools/calendar-rubrics` (`rubrics.yaml` lines 734–789) and 1962 Missal pp. 284 and [44]–[45]: obligatory IV cl. Office and Mass of Our Lady on Saturday (*Vultum tuum*, row 27) outranks the IV cl. feria (row 28) in 57 of 101 seasons and keeps its own proper BVM Preface (*Et te in veneratione*) because 2–5 January lacks the Octave override of 26–31 December.
3. **15-Collect Grammatical & Translation Collation:** All 15 Christmas-season Collects are addressed to God the Father (0 *Qui vivis*). Rejected Lasance 1945 where defective: used Dom Gaspar Lefebvre (1925, p. 399) for St. Stephen (restoring *"Thy Son"* omitted in Lasance p. 147), Marquess of Bute (1908, p. 211) for 1 January (avoiding Lasance's misplaced semicolon on pp. 167 & 1403), Bute (1908, p. 365) for Most Holy Name, and Lasance Common of Supreme Pontiffs (ordinary p. 1302) for St. Sylvester and St. Telesphorus (avoiding p. 164's inserted *"Thy"*). Also avoided Lasance's defective Nativity Preface (*"dominions and powers"*, dropping Thrones), Dawn Postcommunion, and St. John Postcommunion.
4. **Latin *Benedictus* (Luke 1:70):** Restored received liturgical reading *sicut locutus est* against upstream `latVUC` error *locutum*, verified via Migne PL 142 (Bruno of Würzburg) and J. H. Blunt (1866).
5. **Canonical Precision and Honest Absence Boundaries:** Distinguished three dated strata (Trent 1563 / Baltimore 1889; 1917 CIC cc. 1108 §§1–3, 1252 §§1, 2, 4 + 1959 decree; 1983 CIC cc. 1246–1247, 1249–1253 + *Paenitemini* + USCCB 1966/1983–84/2026 notes). Explicitly highlighted that Fridays on 26–31 December and 2–5 January remain penitential days under both 1917 CIC c. 1252 §1 and 1983 CIC c. 1251 (not solemnities), and disclosed absent canons (1917 CIC cc. 806 §1 & 1247; 1983 CIC c. 1248; 1991/92 USCCB c. 1246 §2 decree text) in Appendix C and `research/source-audit.md`.

---

## 3. Fresh-Reader Calendar Walkthroughs Across All Seven Shapes

| Scenario | Walkthrough Result |
| --- | --- |
| **Latecomer opening the book on 29 December** | Ch. 1 directs the reader straight to Appendix A without guilt. Table 1 opens to `29 December` (Day 5 within Octave, Titus 3:4–7 & Luke 2:15–20, St. Thomas Becket Low Mass comm.), with an explicit switch pointer to Table 2 if 29 December is a Sunday (omitting St. Thomas). |
| **25 December on Sunday (e.g., 2022/23, 2033/34)** | Ch. 8, App. A, App. C, and `calendar-verification.md` agree: no Sunday within the Octave occurs anywhere in the season (*Dum medium silentium* omitted); Most Holy Name falls on fallback Monday 2 January; 3–5 January are Mon–Fri ferias (Jan 1 Mass, St. Telesphorus Low Mass comm. on 5 Jan). |
| **25 December on Wednesday (e.g., 2024/25, 2030/31)** | Ch. 9, Ch. 11, Ch. 12, App. A, and App. C agree: Sun 29 Dec Sunday within Octave omits St. Thomas; Sat 4 Jan takes Our Lady on Saturday (*Vultum tuum*, BVM Preface); Sun 5 Jan Most Holy Name omits St. Telesphorus even at Low Mass. |
| **25 December on Tuesday (e.g., 2029/30, 2035/36)** | Ch. 11, Ch. 12, App. A, and App. C agree: Wed 2 Jan fallback Most Holy Name; Sat 5 Jan takes Our Lady on Saturday (*Vultum tuum*, BVM Preface) WITH Low Mass commemoration of St. Telesphorus. |
| **25 December on Thursday / Friday / Saturday (e.g., 2025/26, 2026/27, 2027/28)** | Ch. 7, Ch. 8, App. A, and App. C agree: Sunday within the Octave wins over Holy Innocents (28 Dec), St. John (27 Dec), or St. Stephen (26 Dec) with ordinary commemoration in Low Mass only (reversing pre-1960 precedence). |

---

## 4. Verification Gates, Web Edition, and Print Visual Inspection

- **Document Schema (`tools/document-schema check --phase content`):** `1 documents, 1 outputs: 0 content schema errors.` (exit 0)
- **Generated Entrypoint (`tools/document-types refresh --check`):** `gemini/liturgy/roman-rite/1962/seasons/christmas: current` (exit 0)
- **Generation Metadata (`tools/check-generation-metadata`):** `Generation metadata valid: 1 canonical record(s), 0 inherited record(s).` (exit 0)
- **Content Preflight (`tools/check-content-preflight` — ALL checks):**
  - `bindings-valid`: **176 bindings**, every ID registered and canonically fingerprinted.
  - `house-voice`: **17 reader-facing files**, 0 errors.
  - `identifiers-resolve`: 0 raw source IDs in reader prose.
  - `references-used`: **56 entries**, every one used in the body.
  - `restricted-not-reproduced`: **176 bound sources** (28 restricted), none reproduced.
  - `unquoted-not-quoted`: 0 errors.
  - Overall exit code: **0**.
- **Web Edition (`tools/check-web-edition` + `tools/web-edition`):** `eligible`, exit 0, **29,552 words** rendered cleanly in Markdown with zero raw LaTeX leaks, zero dropped tables, and zero orphaned attributions.
- **Native Print Compile (`tools/native-print-compile prepare` + `compile` with `wasmtex-2026-47ff73bab1a2e548`) & Anchor Check (`tools/check-pdf-anchors`):**
  - **48 pages**, 2 passes of `pdftex`, `"problems": []`, **0 overfull hboxes**, **0 undefined references**, exit 0.
  - `check-pdf-anchors`: **72 contents lines, 16 bookmarks, every one on its own anchor** (exit 0).
  - Visual PNG inspection (title page, single-page Contents, Ch. 5 opening, App. A tables, App. B unbroken `massbox`es & split hymn boxes, App. C 7-shape table, and balanced 28-line closing p. 48 with colophon) confirmed publication-grade print layout.
