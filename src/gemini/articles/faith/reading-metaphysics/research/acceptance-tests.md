# Acceptance Verification Record — *Reading Metaphysics*

**Document:** `src/gemini/articles/faith/reading-metaphysics/` (`article-v1`, kind `article-faith`)
**Governing Architecture:** `.scratch/lanes/lane-6/DOCUMENT-SPEC.md` (Version 2, §§1–18, Appendices A & B)
**Overall Verdict:** **PASS** — All 10 acceptance tests (A–J, §17.2), both cold pencil tests (§15.6 / §17.1), both pseudo-formalism checks (§17.3), the 12-item reviewer checklist (§17.6), scale enforcement (§17.5), independent cold-review remediation (all 5 Blocking + 7 Advisory findings), and all repository CLI gates pass cleanly.

---

## 1. The Two Cold Pencil Tests (§15.6 and §17.1) & Independent Cold Review

### 1.1 Phase 1 Vertical-Slice Gate (*ST* I, q. 8, a. 1) — **PASS (Round 2)**
- **Standalone artifact:** `.scratch/lanes/lane-6/vertical-slice/vertical-slice.tex` compiled via `/usr/bin/xelatex` to **12 rendered pages** (strictly within the §15.2 / §17.5 budget of 8–12 pages), covering St. Thomas Aquinas, *ST* I, q. 46, a. 2, ad 7 across all 15 required elements of §15.4 in exact order.
- **Unmarked test passage:** St. Thomas Aquinas, *ST* I, q. 8, a. 1 ("Whether God is in all things?"), never mentioned anywhere in the slice.
- **Independent reviewer:** Fresh `triptych-cold-reviewer` subagent (`5e73f861-169d-4c09-84ee-c8115db26f6e`), full Round 1 + Round 2 transcripts recorded in `research/vertical-slice-review.md`.
- **Disposition:** Round 1 returned HARD FAIL (catching a dual-error near-neighbour under Hard-Fail 5 prong 2, a contradiction between Section 6 and Sections 8/9/12 on narrow vs. cosmic burden, a logical wording slip in Section 8, and two citation corrections: *SCG* I, c. 13 n. 14 vs. n. 15 and divine intelligence in *ST* I, q. 14 rather than qq. 3–11). All defects were repaired and re-submitted; **Round 2 PASSED with zero hard fails and zero remaining defects.**

### 1.2 Final Full-Book Pencil Test (*ST* I, q. 9, a. 1) — **PASS**
- **Unmarked test passage:** St. Thomas Aquinas, *ST* I, q. 9, a. 1 ("Whether God is altogether immutable?"), full article (Obj. 1–3, *Sed contra*, *Corpus*, Replies 1–3), never analysed anywhere in the finished book.
- **Independent reviewer:** Fresh `triptych-cold-reviewer` subagent (`87c77b75-0efc-4bc0-8cc5-efa76343cb1a`), full report archived in `.scratch/lanes/lane-6/final-review/final-pencil-report.md`.
- **Result:** The reviewer produced a crisp one-page continuous-prose reading under all six headings (`Claim` + plain-language reading, `Meaning`, `Warrant`, `Burden`, `Consequence` + *Not yet established*, `Denial`) using **zero** house glossary and experiencing **zero** confusion over any heading, warrant kind, or denial kind. Deleting all six headings left smooth continuous prose.

### 1.3 Independent Cold Review Remediation (5 Blocking + 7 Advisory — ALL RESOLVED)
Audited against `guidance/editorial.md`, `guidance/the-shape.md`, `guidance/articles.md`, print PDF, and converted web-edition Markdown (`.scratch/cold-reviews/lane-6/review.md`). Every blocking and advisory finding was fixed and re-verified:
- **B1 (`09-lesson-8.tex:71`):** Repaired reversed inline predicate arguments `\logicop{Prec}(y, x)` -> `\logicop{Prec}(x, y)` to match the fixed definition at lines 45–47.
- **B2 (Aristotle Bekker/chapter citations):** Corrected *Post. An.* I.30 `88a5--17` -> `87b19--27` (`01-lesson-0.tex`, `07-lesson-6.tex`, `80-appendix-historical-sources.tex`); corrected *Prior Analytics* `I.2, 24b18--20` -> `I.1, 24b18--20` (`02-lesson-1.tex`, `99-references.tex`); capped *Metaphysics* Gamma 4 at `1009a5` (`06-lesson-5.tex`, `80-appendix-historical-sources.tex`, `99-references.tex`).
- **B3 (`04-lesson-3.tex:22, 173`):** Updated `"or by a previous citation?"` -> `"or deferred to a prior result?"` to align Lesson 3 with Opening and Appendix B.
- **B4 (Bindings, references, Exercise 7.4):** Removed unused `work.thomas-aquinas.de-potentia` binding from `research/source-bindings.toml`; removed unused *In Metaph.* entry from `99-references.tex` and `80-appendix-historical-sources.tex`; reconciled every `"cited at..."` sub-locus in `99-references.tex` (`Post. An.`, `SCG I`, `In PA`, `Super Boet. De Trin.`) 1:1 against body and Appendix A citations; revised `08-lesson-7.tex` Exercise 7.4 accurately to note that two sentences of the second argument appeared in Lesson 1.
- **B5 (Voice, meta-labels, self-narration, workflow jargon):** Removed all four `\emph{What the book supplies and what it withholds:}` wrappers in Lesson 7; eliminated `"This lesson installs..."`, `"This book neither belittles..."`, `"rest of this book"`, `"scaffolding of this book"`, and `"Nothing in these nine lessons..."`; stripped internal workflow jargon from `90-scope-method-qualifications.tex` and recast sentences so `check-content-preflight --check house-voice` exits `0`.
- **A1–A7 (All 7 advisories resolved):** Added trailing spaces to binary operators (`→ `, `∧ `, `≠ `, `∈ `) in `format.tex` web branch (verified clean in rendered Markdown); replaced `\item[(a)]`/`\item[(b)]` in Exercise 0.1 with bold `(a)`/`(b)` in `itemize` (preserved in web Markdown); added `\setcounter{section}{-1}` in `format.tex` print branch so Lesson 0–8 align 1:1 with Section 0–8 while Appendices remain A–D; added `\keeppair` (`\Needspace{7\baselineskip}` in print, empty in web) to keep Lesson 4's paired modal-scope formulas together on Arabic p. 32 and prevent an orphan `A Defective Near-Neighbour` heading on p. 55; removed all 12 `"Notice"`/`"Pause and notice"` imperatives; replaced Exercise 6.2's duplicate moon-phases pair with Aristotle's distinct *Post. An.* II.16 (`98b4–10`, deciduous/broad-leaved vine) example; aligned `research/source-audit.md` inspected vs. cataloged states with `source-bindings.toml`; corrected `09-lesson-8.tex` foot-in-the-dust attribution to *"the Platonists' image reported by St. Augustine"* (*De Civ. Dei* X, 31) and removed the redundant `\emph{Claim and plain-language reading.}` label in Solution 8.1; harmonized all Exercise and Solution headings across Lessons 0–8 to `\subsubsection*`.

---

## 2. Ten Acceptance Tests (§17.2)

| Test | Criterion | Verdict | Concrete Evidence |
|---|---|---|---|
| **A. Personal usefulness** | Applicable with a pencil to an unmarked page of Aquinas with zero house glossary | **PASS** | Passed both cold pencil tests (*ST* I, q. 8, a. 1 on vertical slice; *ST* I, q. 9, a. 1 on full book). Mechanical scan confirms **0** occurrences of `S1`–`S8`, `W1`–`W8`, `D1`–`D5`, `E1`–`E9`, or unlisted house jargon across all 14 `.tex` files. |
| **B. Burden visibility** | Every worked passage names one clear burden-bearing proposition (or separates upstream vs. on-page burden explicitly) after definitional unpacking | **PASS** | Verified across all worked passages in Lessons 3–8 and Appendix B specimen. Opening, Lesson 3, and Appendix B define Burden identically (`"not supplied merely by vocabulary or deferred to a prior result"`). |
| **C. Authority discipline** | Removing proper names/citations removes zero warrant (except explicitly labelled *provenance only* or *revelation*) | **PASS** | Verified in Lesson 2 (Aristotle, Damascene, *ST* I, q. 1, a. 8, ad 2), Lesson 7, Lesson 8, and cold audit. Citations to earlier articles enter as *prior result* standing on *provenance only* on the page until audited. |
| **D. Formalism discipline** | Every displayed formula has an explicit licensing sentence naming a specific §9 feature | **PASS** | All **16** displayed formulas (`\ldisplay{...}`) across 5 files carry explicit licensing prose right beside them: `01-lesson-0.tex` (2), `04-lesson-3.tex` (2), `05-lesson-4.tex` (8), `08-lesson-7.tex` (2), and `09-lesson-8.tex` (2). Zero displays in Lessons 1, 2, 5, 6; zero-symbol refusal modelled explicitly in Lesson 4 Worked Passage 2, Lesson 7 Worked Passage 2, and Appendix B. |
| **E. Tautology discipline** | Hostile-reader check (§17.3) passes on every worked passage and solution; no definition masquerades as discovery | **PASS** | Explicit hostile-reader check applied across Lessons 3–8, including explicit refused definitional cheats in Lesson 8 Worked Passage 2 and Exercise 8.3. |
| **F. Bounded conclusions** | Every worked passage states a concrete *Not yet established* list naming specific propositions commonly claimed at that point | **PASS** | Verified across Lessons 4–8 and Appendix B. Every *Not yet established* list names specific doctrinal or philosophical destinations. |
| **G. Honest disagreement** | Denial accurately classified among the five kinds; every rival stated at its ablest defender's strength | **PASS** | Verified across Lessons 5, 7, 8, and Appendix B (microstructuralism, Humean regularity, conceptual essence/existence distinction, emergentism, Scotus *Ord.* I d. 3 n. 26, Hume *Dialogues* IX, Kenny vs. Wippel/Feser, eternal created cosmos). |
| **H. Historical fidelity** | Zero retrojection; all citations verified against Appendix A and primary witnesses; zero unverified loci cited | **PASS** | Verified across all 9 lessons, Appendix A, and References; zero citations to UNVERIFIED loci; all Aristotle Bekker/chapter citations verified (*Post. An.* I.30 = `87b19–27`; *Prior An.* I.1 = `24b18–20`; *Metaph.* Gamma 4 capped at `1009a5`; *Post. An.* II.16 = `98b4–10`). |
| **I. Scale** | Total PDF strictly **50–80 pages** via content discipline; every lesson inside §12.9 budget; Appendix B fits on **1 exact page** | **PASS** | Official `./tools/print-document build` output: **80 physical PDF pages** (Title + TOC p. i + Arabic pp. 1–78), strictly inside 50–80 pages; Appendix B visually verified on Arabic p. 75 (PDF p. 77) alone. |
| **J. Transfer** | Every lesson includes kind (c) unannotated new prose; no lesson ends on kind (a); >50% of all exercises are kind (c) | **PASS** | **39 exercises** matched 1:1 by **39 continuous-prose solutions** (uniform `\subsubsection*` headings throughout). **22 of 39 exercises (56.4%)** are strictly kind (c) unannotated new prose with nothing supplied; **every single lesson (0 through 8)** includes kind (c) and **ends on kind (c)** (Ex. 0.3, 1.5, 2.5, 3.5, 4.5, 5.5, 6.4, 7.4, 8.3). Exercise 6.2 uses a distinct *Post. An.* II.16 example (zero exercise duplication across the book). |

---

## 3. Scale Enforcement Breakdown (§17.5)

Measured directly from the final official `./tools/print-document build` PDF (`reading-metaphysics--45300ac8e8be3155.pdf`, **80 physical pages**, letter size, 784,218 bytes, 0 TeX errors, 0 undefined references, 0 overfull hboxes, 0 PDF anchor problems):

| Section | Arabic Pages | Rendered Span | §12.9 Budget | Status |
|---|---|---|---|---|
| Front Matter (Title + Contents) | — / i | 2 pp. | — | Clean (`0 Lesson 0`..`8 Lesson 8`, `A`..`D`) |
| Opening: Reading a Difficult Page with a Pencil | 1–2 | ~1.5 pp. | ~2 pp. | PASS |
| 0 Lesson 0: What Demonstration Meant | 2–7 | ~5 pp. | 4–6 pp. | PASS |
| 1 Lesson 1: What Is Being Said? | 7–14 | ~6.5 pp. | 5–7 pp. | PASS |
| 2 Lesson 2: Why Am I Supposed to Believe It? | 14–21 | ~7.5 pp. | 6–8 pp. | PASS |
| 3 Lesson 3: Where Is the Real Claim? | 21–29 | ~8.5 pp. | 7–9 pp. | PASS |
| 4 Lesson 4: What Actually Follows? | 30–37 | ~8 pp. | 6–8 pp. | PASS (modal pair together on p. 32) |
| 5 Lesson 5: What If I Say No? | 38–46 | ~8 pp. | 7–9 pp. | PASS |
| 6 Lesson 6: Demonstration and Its Limits | 46–52 | ~6 pp. | 5–7 pp. | PASS |
| 7 Lesson 7: Reading Real Metaphysics | 52–63 | ~11 pp. | 8–11 pp. | PASS (no orphan heading on p. 55) |
| 8 Lesson 8: Can We Demonstrate It? | 63–71 | ~8.5 pp. | 8–11 pp. | PASS |
| A Historical Sources and Concordance | 72–74 | ~2.5 pp. | Concise | PASS |
| B The One-Page Analysis Sheet | **75** | **1 exact page** | **1 page strictly** | **PASS (visually verified PDF p. 77)** |
| C Scope, Method, and Qualifications | 76–77 (top) | ~1.3 pp. | Concise | PASS (visually verified PDF pp. 78–79) |
| D References & Colophon | 77–78 | ~1.5 pp. | Concise | PASS (visually verified PDF pp. 79–80) |
| **Total** | **pp. 1–78 (+ 2 front)** | **80 PDF pages** | **50–80 pages** | **PASS** |

---

## 4. Exercise Transfer-Ladder Audit (§14.3 & Test J)

- **Kind (a) — Already-analysed passage:** 0 (every exercise introduces a fresh passage, a fresh critical paragraph, or a full unexamined article; Exercise 7.4 openly notes two sentences of its second argument appeared earlier under Claim/Meaning in Lesson 1 before requiring full unaided analysis of all three arguments).
- **Kind (b) — New prose with markings, numbered tags, italicized cues, or partial analysis supplied (17 of 39 = 43.6%):**
  Ex. 0.1, 0.2; 1.1, 1.2; 2.1, 2.2, 2.3, 2.4; 3.1, 3.2, 3.3; 4.1, 4.2; 5.1, 5.2; 6.1, 6.2 (*Post. An.* II.16 deciduousness/broad leaves).
- **Kind (c) — New prose with nothing supplied / unaided synthesis (22 of 39 = 56.4%, strictly > 50%):**
  Ex. 0.3; 1.3, 1.4, 1.5; 2.5; 3.4, 3.5; 4.3, 4.4, 4.5; 5.3, 5.4, 5.5; 6.3, 6.4; 7.1, 7.2, 7.3, 7.4; 8.1, 8.2, 8.3.

---

## 5. Repository CLI Verification Gates (Final Post-Review Run, 2026-11-26)

| Gate Command | Result |
|---|---|
| `./tools/tpt document-types refresh --leaf gemini/articles/faith/reading-metaphysics` | **PASS** — `gemini/articles/faith/reading-metaphysics: current` |
| `./tools/document-schema check --phase content --document gemini/articles/faith/reading-metaphysics` | **PASS** — `1 documents, 1 outputs: 0 content schema errors.` |
| `./tools/check-generation-metadata --provider gemini` | **PASS** — `Generation metadata valid: 11 canonical record(s), 0 inherited record(s).` |
| `./tools/check-content-preflight --provider gemini --document articles/faith/reading-metaphysics --check house-voice` | **PASS (exit 0)** — `house-voice: 15 reader-facing files, no sentence taking the guide, its apparatus or the repository as its subject` |
| `./tools/check-content-preflight --provider gemini --document articles/faith/reading-metaphysics --check references-used` | **PASS (exit 0)** — `references-used: 17 entries, every one used in the body` |
| `./tools/check-web-edition --provider gemini --document articles/faith/reading-metaphysics` | **PASS** — `Web-edition declarations valid: 1 eligible, 0 conditional, 0 ineligible.` |
| `PATH=.../.scratch/venv/bin:$PATH ./tools/web-edition check --leaf gemini/articles/faith/reading-metaphysics` | **PASS (exit 0)** — `Web editions convert: 1 reader output(s), 0 figure(s).`; verified clean binary-operator spacing (`→ `, `∧ `, `≠ `, `∈ `) and Exercise 0.1 `**(a)**`/`**(b)**` labels in rendered Markdown |
| `./tools/source-library validate` | **PASS — 0 errors** on `src/gemini/articles/faith/reading-metaphysics/research/source-bindings.toml` (5 active bindings, unused `de-potentia` removed, exact hashed artifacts + canonical `source_fingerprint`s) |
| `./tools/print-document build --document publication:gemini/articles/faith/reading-metaphysics --out .scratch/lanes/lane-6/final-recheck` | **PASS (exit 0)** — **80 pages**, 0 TeX errors, 0 undefined refs, 0 overfull hboxes, 0 PDF anchor defects; TOC (`0`–`8`, `A`–`D`), Lesson 4 modal pair (p. 32), Lesson 7 near-neighbour (p. 55), Appendix B (p. 75 alone), Appendix C (pp. 76–77 top), and References/Colophon (pp. 77–78) visually verified via `pdftoppm` + `read_file` |
| Stray build-file scan under `src/gemini/articles/faith/reading-metaphysics/` | **PASS** — zero `.pdf`, `.aux`, `.log`, `.toc`, `.out`, `.revision.tex`, `.fls`, or `.fdb_latexmk` files present |
