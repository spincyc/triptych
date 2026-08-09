# Corpus browser surface inventory

## Status and method

This is the A0 foundation inventory at exact base
`c27d6915319785686d1df6a1401a489aa9921f6f`. It records the current public
artifact and its owning sources; it does not authorize route, data, PDF, or
production-shell changes. The freshly generated artifact passed
`tools/public-alpha verify` and contains exactly 20,441 files. `SHA256SUMS`
contains 20,440 entries and intentionally omits itself.

The inventory combines the generator's expected set, the built artifact, the
catalogue and source projections, rendered-route inspection, and focused
surface audits. A representative screenshot matrix is evidence of visual debt;
it is not the route inventory itself.

## Artifact census

| Family | Count | Current owner |
| --- | ---: | --- |
| HTML | 144 | `tools/public-alpha`, fixed sources, web editions, browser entrances, gallery manifest |
| PDF | 192 | 186 publication issues plus 6 reading-plan PDFs |
| JSON | 19,957 | generated `/browse/` structures plus the publication manifest |
| JavaScript | 25 | top-level browser assets |
| CSS | 16 | site stylesheet plus browser assets |
| PNG | 102 | site art and sanctuary-gallery images |
| Text | 3 | `robots.txt` and two raw licences |
| Control files | 2 | `.nojekyll` and `SHA256SUMS` |

HTML breaks down as 25 fixed pages, 105 provider-qualified web editions, 13
browser pages, and one generated sanctuary gallery. The browser set contains
nine canonical pages and four publicly served, fully noindex liturgy
candidates/oracles. The four noindex pages are accessible review or
compatibility surfaces, not additional accepted products.

The generated corpus presently records 133 publication works, 178 provider
documents, 186 issues, 5,675 pages, 491 source works, 655 source editions,
1,467 artifacts, and 2,751 passages. Of 178 provider documents, 105 are
browser-readable and 73 are PDF-only. Of 2,751 source passages, 1,630 are
readable and 1,121 have explicit refusal or absence states.

## Public surface families

| Family | Public routes | Archetype or role | Owning source/build seam |
| --- | --- | --- | --- |
| Home | `/` | Catalogue/corpus map | `README.md`, `tools/public-alpha` |
| Utility | `/about.html`, `/contributing.html`, `/license.html`, `/third-party.html`, `/404.html` | Consumer, contribution, legal, recovery | fixed Markdown and layout |
| Method studies | `/docs/bibles.html`, `/docs/the-mass.html`, `/docs/reading-and-commentary.html` | Reader | fixed Markdown |
| Library | sixteen `/library/*.html` routes, including seven portals and nine child catalogues | Catalogue | `library/*.md`, catalogue rewrite |
| Picture dictionary | `/library/sanctuary-picture-dictionary.html` | special Catalogue/Reader | sanctuary inventory, artwork manifest, gallery renderer |
| Publication readers | 105 `/web/{provider}/{leaf}.html` routes | Reader | reviewed `web/**/*.md`, shared renderer |
| Liturgy | `/liturgy/`, `/liturgy/day.html` | protected Liturgical Instrument | liturgy source, generated calendars/Propers/Bibles |
| Scripture | `/scripture/`, `/scripture/track.html` | Reader/Instrument | reading-plan and Bible projections |
| Commentary | `/catena/` | Instrument | Catena spine and fragment projection |
| Sources | `/sources/` | Catalogue-to-Instrument hybrid | source-library projection |
| History | `/history/` | Instrument | act-history spine/fragments |
| Law | `/law/` | Instrument | canon-law act history and code model |
| Every Document | `/texts/` | Catalogue | generated document corpus |
| Retained liturgy evidence | four `/liturgy/*.html` routes | noindex candidate/oracle | top-level entrance glob |

There is no generated sitemap, canonical-link contract, route manifest, global
typed search index, service worker, server API, or rewrite layer. Directory and
explicit `index.html` forms coexist. Public application state is largely in
route-owned queries and hashes and must remain so until a governed URL
migration supplies compatibility.

## Current normalized state coverage

| Surface | Loading | Empty | Invalid/error | Partial/choice | Withheld/unread | URL quality |
| --- | --- | --- | --- | --- | --- | --- |
| Static pages/readers | not applicable | catalogue empty shelf only | build/404 | mixed edition availability | held publications excluded | headings usually text-derived |
| Day | explicit | not applicable | fail closed | explicit branch/coverage | explicit Ordinary absences | strongest governed state contract |
| Propers | explicit | intentional Browse | fail closed | cycles/witness/coverage | unavailable text explicit | strong, edition-qualified |
| Scripture | explicit | orientation/empty track | some silent normalization | citation/numbering gaps | edition absence | reading identity is an ordinal |
| Catena | global and fragment-local | held-none and lead-only | invalid values may fall back | voice/cross-chapter | blocked/lead support | no fragment address |
| Sources | global/edition/passage | no matches/no passage | mismatched passage can select passage zero | mixed availability | first-class reasons | work/artifact unaddressable |
| History | global and lazy | no-change/no-pair | invalid station may default | branch/gap/partial fragment | unread/withheld distinct | station/unit supported |
| Law | global and lazy | initial/no match | exact and fuzzy paths conflict | paragraph/act gaps | present/withheld/unread distinct | code-qualified state exists |
| Every Document | explicit | filter zero | invalid filters coerce | paired/single/PDF-only | not rendered state | hash clear/history defects |

## Cross-cutting baseline findings

- Every one of the 13 built browser pages currently contains a nested `<main>`
  landmark because route markup is inserted into the layout's main.
- The shared public header exposes only Home, About, and Feedback. Route
  instruments duplicate inconsistent cross-corpus link lists in their footers
  or Details panels.
- At 320 CSS pixels, Every Document overflows the page by 56 pixels and Sources
  by 24 pixels. Library tables use internal horizontal scrolling rather than a
  mobile catalogue composition.
- On narrow screens, the first useful result falls below the first viewport on
  Every Document, Sources, History, and Law. Current forms and filters dominate
  the initial view.
- Only Liturgy has comprehensive real-browser responsive, focus, forced-color,
  reduced-motion, and print coverage. Its accepted cutover evidence predates
  the current in-progress Ritual Flow delta and current generated-data freeze.
- Static publication Readers have a sound source/reflow pipeline but no local
  contents, direct canonical-PDF action, citation-return enhancement, or
  browser accessibility matrix.
- The current sanctuary gallery publishes 100 original PNGs totalling about
  49.3 MB and loses material source, audience, and depicted-state
  qualifications in its public projection.
- No general site stylesheet owns forced colors or browser-Instrument print.
  Focus, target size, typography, and state vocabularies vary across routes.
- The whole served JSON corpus is additive and selective at runtime, but
  Roman-1962 Propers uses one roughly 4 MB raw structure, and the two catalogue
  spines are roughly 443–446 KB raw each.
- Current hash history has shared clear/back-forward defects. Invalid cited
  objects sometimes fail closed and sometimes silently select an arbitrary or
  previous object.

## Protected baseline and compatibility boundary

The accepted Liturgical Instrument remains the visual reference for calm
reading, the 39.75rem/636px Read axis, opaque square edge controls, one-open
surface behavior, focus and semantic-position restoration, forced colors, and
print. Canonical Day and Propers keep exactly four actions: Date/Browse,
Contents, Mode, and Details. They may not receive a fifth global action, a
second visible masthead, another modal owner, or new sticky edge chrome under
A0-A4.

The exact base also contains an unaccepted Ritual Flow work-in-progress and a
Day-reader symptom fix recorded as not fully verified. Current/live captures
must be labelled current WIP; accepted-reference captures must name the earlier
accepted cutover evidence. The foundation prototype does not import, modify,
or claim acceptance of either production state.

## Deferred implementation owners

A0 identifies rather than fixes the following: B0/B1 own production shell and
accessibility integration; C0/C1 own Home and Catalogue; D0/D1 own publication
Readers; E0/E1 Catena; F0/F1 Sources; G0/G1 History; H0/H1 Law; I0/I1
Scripture; J0/J1/J2 typed search; K0/K1 cross-corpus relationships; L0/L1
responsive and accessibility refinement; M0/M1 release acceptance. Production
route, PDF, generated-data, and public-deployment changes remain outside this
foundation branch.

## Wave 1 dispatch delta — 2026-08-08

This delta selects real evidence from the unchanged A0 base for C0/C1, D0, E0,
and F0. It does not restate product decisions or execution state owned by the
corpus-browser vision and roadmap.

- Current Wave 1 base: `c27d6915319785686d1df6a1401a489aa9921f6f`.
- Accepted A0 source: commit
  `ac37b6ffa6022dbab551385d91a12e277bb816cb`, blob
  `d05efca324e4d7e181faf90687c2e9935e626dce`; reviewed design-branch head
  `3b5938a0dba88831763ec09c762ae1572007a27e`.
- Accepted implementation-reconnaissance head used for the defect cross-check:
  `af2c9613ccda48679face4e43f59c002f93056ef`.
- At the base, the generated page at `/texts/` visibly belongs to the
  **Every Document** baseline. The accepted forward-facing label is
  **Publications**; the route and the repository's one-owning-catalogue rule do
  not change.

### Required real fixtures

| Surface and route/state | Exact base fact | Why it is a useful extreme |
| --- | --- | --- |
| Home `/`; Publications `/texts/` | 133 works, 178 provider documents, 186 issues; 105 browser-readable and 73 PDF-only | Exercises task entrances, seven-portal orientation, paired and single treatments, format availability, and accurate scale without synthetic freshness. |
| Reader `/web/gpt/history/traditional-priestly-institutes/03-icksp.html` | The 107-character title is the longest provider-document title: “The Institute of Christ the King Sovereign Priest: African Origins, Canonial Identity, and Global Expansion.” | Long-title and narrow-heading stress case; preserve the repository's actual wording in evidence. |
| Reader `/web/gpt/history/catholic-exorcism/01-history-and-current-practice.html` | 120-page canonical PDF, the longest browser-readable publication at the base | Long contents, sustained reading, citation, colophon, canonical-PDF, and browser-print stress case. |
| Catena `/catena/#book=Gen&chapter=1` | 107 held fragments from 13 sources, 33 acquisition leads, 272,033 aggregate fragment words, and English/Greek/Latin voices | Densest chronological chain, multilingual state, overlapping extents, and cross-chapter fragments. |
| Catena `/catena/#book=Ps&chapter=13` | No held fragment, 35 acquisition leads, and 7 recorded refusal reasons | Held-none state where evidence must not be mistaken for commentary text. Across the projection, 561 chapters have evidence files: 50 contain held fragments and 511 are lead/refusal-only; 509 of those 511 carry leads and 16 carry refusals, with overlap. |
| Sources `/sources/#edition=edition.holy-see.acta-apostolicae-sedis.volume-22-1930` and its sibling editions | The work `work.holy-see.acta-apostolicae-sedis` has 28 editions, the maximum | Multi-edition hierarchy stress; the exact selected edition may be changed among the work's recorded edition IDs without inventing a relationship. |
| Sources `/sources/#edition=edition.ronald-conte.catholic-public-domain-version.sacredbible-original-web-2026-07-31` | One edition carries 148 artifacts, the maximum, and no addressed passage | Deep artifact hierarchy plus a truthful no-passage state. |
| Sources `/sources/#edition=edition.remigius-of-auxerre.commentarius-in-genesim.latin-migne-pl-131` | 396 of 396 passages readable, the maximum passage count in one edition | Large readable passage navigator and Latin/source-heavy stress case. |
| Sources `/sources/#edition=edition.catholic-church.codex-iuris-canonici-1983.latin-vatican-web-codex-2026-07-25` | 82 addressed passages, none redistributable; rights state `restricted` | Large withheld state in which availability and redistribution rights must remain distinct. |

The Source projection totals remain 491 works, 655 editions, 1,467 artifacts,
and 2,751 passages: 1,630 readable and 1,121 explicitly unavailable. A separate
long-metadata stress record is
`work.convocation-of-canterbury.revised-version`, whose responsible-creator
string is 131 characters.

### Defects the Wave 1 evidence must expose

| Route family | Base defect to preserve in before evidence |
| --- | --- |
| All 13 generated browser pages | The wrapper creates nested `<main>` landmarks. |
| `/` | The generator recognizes an exact README preamble; changing it without updating the transform can silently restore a duplicate title instead of producing the intended Home composition. |
| `/texts/` | 56px horizontal overflow at 320 CSS pixels; the filter plane pushes the first result below the narrow first viewport; clear/back-forward hash behavior is defective. |
| Publication Readers | No local contents, direct canonical-PDF action, citation-return enhancement, or route-family browser accessibility matrix. |
| `/catena/` | No fragment-level address; invalid selection may fall back; dense Genesis and held-none Psalm states have radically different information loads. |
| `/sources/` | 24px horizontal overflow at 320 CSS pixels; the first result falls below the narrow first viewport; work and artifact are not addressable; a mismatched passage may select passage zero. |
