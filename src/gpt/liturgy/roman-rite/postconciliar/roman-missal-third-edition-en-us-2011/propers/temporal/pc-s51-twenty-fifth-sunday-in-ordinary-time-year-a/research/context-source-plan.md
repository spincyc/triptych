# PC-S51-A: resolved source plan

Resolved 17 September 2026. The ordered inventory is in [context.md](context.md).
This plan identifies reusable evidence and remaining research; it does not
accept the preliminary interpretations or certify unperformed collation.

## Independently inspected occurrence evidence

- [USCCB, 2026 national calendar](https://www.usccb.org/resources/2026cal.pdf):
  full 61-page PDF freshly retrieved; SHA-256
  `4bd9add07512396a2323aa977bc4816a5fad6348262e12740bcee97c77372d02`,
  matching existing canonical artifact
  `artifact.united-states-conference-of-catholic-bishops.liturgical-calendar-dioceses-united-states.2026.usccb-pdf-4bd9add0`.
  Inspected book identity and cycle on printed p. 5 / PDF p. 7, and the
  September 20 entry on printed p. 38 / PDF p. 40, including its page image.
  The calendar's current edition notes include February 2025 and February 2026
  emendations. Only these relevant passages were inspected; acquisition is not
  inspection of every annual entry. Restricted bytes are not publication input.
- [USCCB, Sunday 20 September 2026](https://bible.usccb.org/bible/readings/092026.cfm):
  complete daily HTML freshly retrieved and read; SHA-256
  `9581da4f98293b2551dfbe2db4ff7939d26898ea3255c732bf4610d7b02e9015`.
  Title, Lectionary number 133, five scriptural headings, Psalm response locus,
  reading cuts and final Gospel sentence independently checked. This is an
  official dated digital witness, not a claim that the printed Volume I was
  inspected in full. Its CCD text remains outside tracked/public payloads.
- The registered `calendar-days day --date 2026-09-20 --calendar postconciliar
  --json` finding aid returned Year A and Ordinary Time week 25. Its unranked
  candidates also include the fixed-date Korean-martyrs memorial; the official
  dated calendar, rather than the unranked computation, establishes the Sunday
  appointment. The independent arithmetic is recorded in context.md.
- The Dicastery's [calendar-variations index](https://www.cultodivino.va/en/formazione/pubblicazioni/libri-liturgici/aliae/calendarium-romanum.html)
  was opened and retrieved whole (SHA-256
  `4531f6b614a851a098f40fe6f43e2f0f6f4e31804f6d7a0b4b8493a499f7cdb6`).
  Its visible list ends with 2021 entries and is not a complete currentness
  certificate. A bounded official-domain search for 2026 calendar decrees
  found the [Newman decree](https://www.cultodivino.va/en/attivita/2026/inscription-of-s-john-henry-newman-in-the-general-roman-calendar.html),
  published 3 February 2026, assigning an optional memorial to October 9;
  that date is also reflected in the annual calendar's emendation note.
  No September 20 change appeared in that bounded search. The dated national
  witness directly confirms the present target; no exhaustive future-decree
  or unknown local-calendar claim follows.

## Existing library read before acquisition

The current calendar artifact record, ICEL Antiphonary edition/artifact record,
Challoner/Gutenberg edition identity, the leaf's source bindings and source
audit, and the Week 25 shared owner were read before new retrievals. The
preliminary handoff was read in full as leads. Its claim that no shared owner
or bindings existed is superseded by the files now present. Its patristic
conclusions remain research-stage inputs, not accepted interpretation.

The shared [Week 25 owner](../../shared/ordinary-time/weeks/25/propers/verified.md)
is the sole authority for common Missal element evidence, locators, rights and
variation limits. The existing exact Antiphonary payload was hash-checked
against its canonical record and its Week 25 page image was independently
inspected to test this context's completeness, including both Communion
alternatives. Its reusable collation is not copied here. The oration identity
is referenced through the owner; full U.S. altar-book/2008-reprint collation is
not claimed by this stage.

## Lawful routes by element

The six existing complete-book artifacts are under
`src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/`:
`verse-text-27-isaias-7c9a1228`, `verse-text-21-psalms-578f023d`,
`verse-text-47-matthew-dd0ba183`, `verse-text-57-philippians-4ff760a7`,
`verse-text-51-acts-73f7a420`, and `verse-text-50-john-27b8f3ed`.
The existing [bindings](source-bindings.toml) identify their exact artifacts and
consumer bounds. Gutenberg's witness combines Challoner editions; it is not
silently renamed the 1899 American printing. Research must inspect the actual
wording before quotation and preserve the approved Lectionary's partial-verse
boundaries through an explicit study-text note.

| Inventory element | Source route and research task |
| --- | --- |
| Entrance | Week 25 owner `entrance`. Explain its role without constructing a substitute antiphon; study the identified underlying Psalm 37:39–40 in DR Psalm 36 as underlying Scripture, not the complete liturgical text. |
| Collect | Week 25 owner `collect`. Use its checked Latin incipit and original analytical description, subject to the owner's edition limits; supply no new English prayer translation. |
| First reading | Official Lectionary 133 appointment; retained Isaias 55:6–9, within chapter 55. Verify exact excerpt against the book artifact; investigate direct patristic/saintly context as recorded in scope.md. |
| Responsorial Psalm | Official appointment Psalm 145:2–3, 8–9, 17–18 and response 18a; retained DR Psalm 144. Preserve strophe and response boundaries without reproducing the approved English refrain. |
| Second reading | Official appointment Philippians 1:20c–24, 27a; retained chapter 1. Verify the partial opening and ending; verses 25–26 are context only. |
| Acclamation | Official Cf. Acts 16:14b assignment. Describe its adaptation of Lydia's narrative; a DR excerpt may be identified only as the underlying biblical passage, not as the appointed acclamation. |
| Gospel | Official Matthew 20:1–16a appointment; retained Matthew 19–20 for context. End the appointed study excerpt at the first/last saying, before the additional traditional many-called clause. |
| Offerings | Week 25 owner `offerings`; checked incipit and analysis, no reconstructed ICEL or newly composed liturgical text. |
| Communion Psalm branch | Week 25 owner `communion-ps119`; DR Psalm 118:4–5 for study. The approved locus is Hebrew Psalm 119, not Hebrew Psalm 118. |
| Communion John branch | Week 25 owner `communion-jn10`; DR John 10:14 within its Shepherd discourse. Keep this as an alternative to the Psalm branch. |
| After Communion | Week 25 owner `after-communion`; checked incipit and analysis under the owner's bounds. |

All study Scripture must be identified as historical public-domain English,
not the approved English proclaimed at Mass. Exact ICEL/CCD bodies stay out
of this leaf, PDFs and bundled web output. No source-rights conclusion is
inferred from mere availability. The source records and applicable publication
policy govern each artifact and surface.

## Work that remains for research and downstream owners

1. Complete `instance/manifest.md` and `propers/verified.md` from this context,
   without copying the shared owner's Missal collation. The edition registry
   now adopts PC-S51-A and the dated occurrence; its present context link can
   point to the completed instance manifest when that file exists.
2. Independently inspect the retained patristic and saintly passages before
   developing interpretations. Existing `scope.md`, `source-audit.md`,
   `source-bindings.toml` and `interpretations.md` are a useful corpus and claim
   map, not a predecessor's PASS. Seek the outstanding direct Isaiah reception
   and preserve negative findings and edition/transcription ceilings.
3. Complete any needed official 2008 variation-list and exact 2011 U.S.
   Missal checks in the shared owner through its authorized writer. Until
   then, the source-located study may use only the identified witness layers
   and must not claim diplomatic control over an uninspected altar book.
4. Preserve all open choice classes in context.md and branches.md. No supplied
   parish evidence selects a chant, Preface, Eucharistic Prayer, ritual
   substitution or local solemnity. The homily's working Psalm Communion
   branch is editorial scope, not a report of performance.
5. Keep reception findings in scope.md, coherent interpretation arguments in
   interpretations.md and completed production/review facts in
   production-review.md. No authoring, rendering or review has been performed
   by resolve-context. The existing comment-only main.tex was preserved.

The authorized shared-file integrator added and this stage inspected the
Makefile prerequisites linking all three PC-S51-A PDF outputs to
`temporal/shared/ordinary-time/weeks/25/propers/verified.md` beneath this
edition's propers root. The registry README, formula dispositions and 2026
occurrences now carry the narrowly dated PC-S51-A addition. Those edges settle
ownership and build invalidation; they do not close the owner's source limits.

## Research-stage completion

Research subsequently completed the instance and target audits, independently reread the retained bounded sources, performed the recorded second search, and developed three whole-formulary interpretations. The registry owner updated the occurrence link to the completed manifest and replaced transient publication wording; those exact rows were independently read before research submission. Scope.md and source-audit.md state the resulting evidence and limits. This completion note does not alter what the resolve-context worker inspected or invent a cold-review verdict. Full U.S.2011/official2008 book collation remains unperformed and is expressly bounded by the shared owner.
