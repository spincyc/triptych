# Author the expansive study

Match the manifest's appointed-text publication mode to the reviewed research.
In reference-only mode, use `Research PDF` and retain the complete appointed-text
component as element-specific source locators with unique anchors, not full
liturgical bodies. Explain the texts through original scholarship without
substitute translation or close paraphrase, and state the omitted full texts
once in the terminal scope appendix.

Write the research-mode components only from reviewed research. Start the
leaf from the `proper-study-v1` document type (`guidance/document-schemas.md`,
Document types): declare `[document]` and `[document.main]` in
`publication.toml` with the study's metadata fields and the ordered `body` and
`apparatus` region lists of its own section files, then run
`tools/tpt document-types refresh --leaf {provider}/{proper}`. That command
writes `main.tex` and the Scriptural Date and Location appendix; never write or
edit either by hand. Author the complete source-first study: substantive
opening and map, lawful study texts or locators, detailed explanation of each appointed element,
two to five coherent whole-formulary interpretations, each with its own four
senses, and a short concluding comparison. Develop the actual exegetical moves
of multiple checked Fathers or saints, as the three-document profile defines
them, within each interpretation. Reader-first
titles describe what the interpretations find, not their technical manifest keys.

Use `research/interpretations.md` as the evidence map. Preserve material
qualifications and disagreements where they change a claim. Do not invent a
Father's commentary on this whole Mass, generic patristic agreement, or a
historically intentional postconciliar theme. Roughly 6,000–10,000 substantive
words is a planning range; an exported print edition must occupy 20–50 physical pages.
Meaningful exposition decides the treatment within that range. Reject both
padding and an outline passed off as expansive.

Develop the particular exegetical questions and distinctive arguments or
inferences audited under the three-document profile. Different readings may
answer the same question. Let their textual difficulties drive the exposition;
do not return each reading to the same application through different headings.
Teach the question, the appointed words that raise it, and the witness's
inference before drawing its consequence, as the profile's pedagogy standard
requires. Concrete textual detail should carry the exposition; repeated
abstract conclusions do not deepen it. Show each element's contribution where
the argument uses it, and do not open or close an interpretation with a claim
or a roll call that every element takes its place in one movement; the
profile's expansive-study section says why. Write every reader sentence to
`guidance/editorial.md`, "Say what the texts say, plainly": no maxim closers,
asserted significance, antitheses against positions nobody holds, texts
credited with the study's inferences, or production vocabulary in reader prose.

Create or revise `publication.toml` under `guidance/document-schemas.md` and the
full schema-2 `proper-components.toml`, declaring future
synthesis and homily components as well as the actual research files. The
study preflight requires only research-mode files to exist yet. Record two to
five `[[lanes]]` with all appointed element keys, four senses, substantive
authors, source-audit paths, and the relevant interpretive-lane component keys.
Declare the profile's `interpretive-pagination-v1` presentation contract and
the future concise opening roles. Declare
`authority_contract = "authority-standing-v1"` and give each lane
`carrying_authors`: the authors, drawn from its `authors` and named as
`src/sources/inventories/author-standing-v1.toml` names them, whose standing
qualifies them to support the interpretation. Follow the checker and owning profile for exact
fields. Each interpretive lane
is a separate component. Keep shared source ownership and references explicit.
Declare `chronology_presentation = "orientation-v3"` for the shared table.
Declare the study's chronology component at the generated appendix,
`generated/scriptural-date-location.tex`, with
`research/chronology-annotations.tex` and `research/chronology-table.tex` as
its references. Write no date prose, setting notes or date footnotes; where the
study needs the chronology it names the appendix (`\ref{sec:date-location}`).

Follow `guidance/web-editions.md` for appointed-text anchors: author exactly
one explicit `\label{proper-<element-key>}` for every declared element key,
including optional alternatives, at its appointed text or rights-safe locator.
Put it immediately after a heading naming only that element, or immediately
before its paragraph when a heading groups texts. Do not repeat it in the map
or commentary, or add an undeclared proper key. The converter requires unique,
complete source and rendered targets; it does not infer them from headings.

The document type imports `common/preamble` then `common/propers-format`;
declare `format_contract = "propers-format-v1"`. Use the shared title, table,
dossier, keyed lane-heading and four-senses forms described in the three-document
profile. Keep ordinary semantic subsections and precise citations; supply
content fields rather than local presentation implementations. Latin Modern,
11-point article, 0.75-inch margins and monochrome are required. The expansive study has no fixed
opening-page positions; the concise companion's first four pages are fixed
by the owning three-document profile. Its chronology's home here is the
generated appendix the type places before the terminal apparatus.
Do not repeat the concise four-page opening for every interpretation.
Every component appears once in a region list; a template macro may format
its arguments but never choose or import a component dynamically. Put
work-wide scope and used references in the `apparatus` region; the type
prints the one canonical generation timestamp and compact rights colophon. Set
exact provenance from this packet and declare canonical web eligibility.

Before submission, run the research-mode source/component checks and validate
the publication manifest and its available source roles. The study's future
companion declarations do not authorize invented files or review results. If an
author print proof is explicitly requested, use `tools/print-document` for this
output and inspect its settled PDF, page count, physical evidence, and build
diagnostics. Keep proof and review evidence in the run's stage/iteration area.
Report its exact identity without claiming cold print review. Normal source
submission does not require that proof.

Also run `tools/tpt web-edition --provider {provider} --output <probe-root> {proper}`,
using this run's `build/tpt-runs/<run>/artifacts/author-study-<iteration>/web-probe`
as the probe root. Use pandoc and the exact Python Markdown dependency pinned
in `requirements-public-alpha.txt`. Repair source defects before submission;
report converter defects without changing accepted research to evade them.
Study preflight repeats this conversion before the study is sealed for review.
It reads only the canonical study, so future companion files may still be
absent. This proof neither accepts a web edition nor creates a web receipt;
the later generate-web and independent web-review stages remain required.

Update `research/production-review.md` with actual scope, substantive word
count and source limits. On reentry, repair study-owned findings; the workflow
will rederive and independently review both companions. Do not silently change
research evidence to make a weak claim pass. Report any research defect for
the cold reviewer to route upstream. Return PASS only with a complete study.
