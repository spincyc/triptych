# Ecclesiastical Latin — Answer-Key Audit

## Object and rendering identity

The authoritative exercise inputs are the four worksheet-bank sources,
`assessments/all.tex`, and each module's local enrichment source. A learning
packet selects two of its unit's four worksheet variants and renders only those
sources twice: once with `solutionsfalse` in the student sequence and once with
`solutionstrue` in the terminal answer part. An assessment companion applies
the same two-pass rule to its selected stable forms. There is no separately
maintained answer manuscript. The solution pass preserves explicit worksheet,
passage, worked-example, assessment, and item identifiers while using a
separate PDF-anchor namespace. This removes drift without implying that every
open model is uniquely correct.

Inventory at integration:

| Family | Worksheet forms | Exercise / assessment calls | Answer type |
|---|---:|---:|---|
| Volume I | 48 | 288 | closed morphology and parsing; translation alternatives; controlled models |
| Volume II | 56 | 340 | closed syntax discrimination; reconstruction; translations; controlled and open models |
| Volume III | 48 | 288 | received-passage analysis; source checks; reconstruction; direct-reading rubrics |
| Volume IV | 32 | 162 | comparison, rhetoric, source dossiers, imitation, open composition rubrics |
| Assessments | 9 forms after integration | 133 items after M-C addition | closed checks, designated-form diagnostics, unfamiliar-formulary rubric, advanced portfolios |

Counts are structural coverage, not evidence that an answer is correct.

## Ambiguity and scoring policy

- A form or parse is closed only to the extent that the supplied context rules
  out real alternatives. The key must state unresolved morphological or
  syntactic ambiguity rather than silently choose one.
- A structural translation preserves relations; a natural translation may
  vary. The key names material alternatives and rejects only a rendering that
  loses the tested grammar or proposition.
- Reconstruction may reorder or bracket supplied material but may not rewrite
  received text. An interpretive supply is labeled.
- Open composition answers are models. They are scored for morphology,
  agreement, government, syntax, intended proposition, and defensible idiom.
- Source, register, allusion, and collation tasks use evidence rubrics and allow
  a documented negative result. They do not require invention of a source.
- Percentages use the denominator defined in the assessment protocol and
  `curriculum-map.md`; no many-part response receives one opaque point.

## Completed internal checks and corrections

Two independent read-only audit passes divided Volumes I–II and Volumes
III–IV/reference/assessments. The integration pass then searched every reported
term through teaching, worksheet, assessment, and solution renderings before
editing the authoritative source. High-confidence corrections include:

- replacing false gender, tense, voice, case-use, compound-pronoun, and
  participle labels where the printed form contradicted them;
- distinguishing the alternative third-person plural perfect ending
  `-ere` from syncope in *conflixere*;
- identifying *praeveniendo* as an inflected ablative gerund rather than an
  indeclinable form;
- correcting a Common-of-a-Martyr source and its propagated placeholder
  exercise;
- distinguishing interrogative `-ne` from negative `ne`, personal subjects
  from impersonal verbs, and antecedent relatives from free relatives;
- correcting exact assessment wording (*advenientis*, hortatory subjunctives,
  gerundive status, and purpose/result ambiguity); and
- adding M-C because the original M-A/M-B reused extensively taught First
  Advent and Pentecost formularies and therefore could not prove unfamiliar
  transfer.

The detailed textual decisions and remaining source limits are in
`source-audit.md`. The post-correction macro inventory found 48/56/48/32
worksheet forms, 288/340/288/162 exercise calls, and 9 assessment forms with
133 assessment items in the four authoritative banks and assessment source.
Across all 46 learning packets, the selectors account for 92 of the 184
worksheet variants and 539 of the 1,078 exercise calls. Every selected prompt
and its answer come from the same captured source environment; the other 92
variants remain optional owner sources rather than omitted required answers.
Each module also keeps its enrichment prompt and checkable model or rubric in
one `SubmoduleExtension` call. The four assessment companions account for all
nine forms and 133 items in both student and solution passes.

## Open review boundary

The audit is internal, not an independent examination by a Latinist or
pedagogue. No human learner has completed the curriculum, timed the two-session
envelopes or gates, or validated writable space and workload in use. The
envelope is an editorial design target, not evidence that every learner should
advance after two days. Received-text attribution and collation are controlled
separately by `passage-inventory.md`; an answer can be grammatically coherent
while still quoting or identifying a source incorrectly. The rebuilt packets
therefore remain uninstalled review candidates even after internal build and
production checks; installation and any changed-byte release authorization are
separate decisions.
