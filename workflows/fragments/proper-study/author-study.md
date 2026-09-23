# Author the expansive study

Write the canonical `main.tex` and research-mode components only from reviewed
research. Author the complete source-first study: substantive opening and map,
lawful study texts or locators, detailed explanation of each appointed element,
two to five coherent whole-formulary interpretations, each with its own four
senses, and a short concluding comparison. Develop the actual exegetical moves
of multiple checked Fathers or saints, as the three-document profile defines
them, within each interpretation. Reader-first
titles describe what the readings find, not their technical manifest keys.

Use `research/interpretations.md` as the evidence map. Preserve material
qualifications and disagreements where they change a claim. Do not invent a
Father's commentary on this whole Mass, generic patristic agreement, or a
historically intentional postconciliar theme. Roughly 6,000–10,000 substantive
words is a planning range; the finished PDF must occupy 20–50 physical pages.
Meaningful exposition decides the treatment within that range. Reject both
padding and an outline passed off as expansive.

Create or revise the full schema-2 `proper-components.toml`, declaring future
synthesis and homily components as well as the actual research files. The
study preflight requires only research-mode files to exist yet. Record two to
five `[[lanes]]` with all appointed element keys, four senses, substantive
authors, source-audit paths, and the relevant interpretive-lane component keys.
Declare the profile's `interpretive-pagination-v1` presentation contract and
the future concise opening roles. Declare
`authority_contract = "authority-standing-v1"` and give each lane
`carrying_authors`: the authors, drawn from its `authors` and named as
`src/sources/inventories/author-standing-v1.toml` names them, whose standing
lets them carry the reading. Follow the checker and owning profile for exact
fields. Each interpretive lane
is a separate component. Keep shared source ownership and references explicit.

Import `common/preamble` then `common/propers-format` literally and declare
`format_contract = "propers-format-v1"`. Use the shared title, table, dossier,
keyed lane-heading and four-senses forms described in the three-document
profile. Keep ordinary semantic subsections and precise citations; supply
content fields rather than local presentation implementations. Latin Modern,
11-point article, 0.75-inch margins and monochrome are required. The expansive study has no fixed
opening-page positions; the concise companion's first four pages are fixed
by the owning three-document profile. Give its required reviewed chronology
a home here, normally a shared terminal historical appendix.
Do not repeat the concise four-page opening for every interpretation.
Keep every component import literal and unconditional; a template macro may
format its arguments but never choose or import a component dynamically.
Put work-wide scope and used references at the end; display the one canonical
generation timestamp and compact rights colophon. Set exact provenance from
this packet and declare canonical web eligibility.

Build an author proof with `make doc DOC={proper} PROVIDER={provider}` before
submission. Run
`tools/check-proper-components --provider {provider} --document {proper} --phase artifacts --edition research`; inspect
the settled PDF, its page count and build diagnostics. Keep any proof copies,
logs and raster evidence beneath this run's stage/iteration artifact directory,
with rasters in their own replaceable child. Report the exact PDF path and hash
for the cold reviewer. This is author verification; the later shared-timestamp
three-document build and independent visual review remain required.

Update `research/production-review.md` with actual scope, substantive word
count and source limits. On reentry, repair study-owned findings; the workflow
will rederive and independently review both companions. Do not silently change
research evidence to make a weak claim pass. Report any research defect for
the cold reviewer to route upstream. Return PASS only with a complete study.
