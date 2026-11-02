# Cold visual review: visual-review-0000

Packet: `build/tpt-runs/0880812aa919d648/packets/visual-review-0000.txt`.
Verdict: PASS; no findings. This is this dispatch's visual verdict, not an
installation, publication, source-research or ecclesiastical approval.

## Artifact identity and coverage

All paths below share
`build/gpt/liturgy/roman-rite/1962/propers/temporal/`.

| PDF | SHA-256 from receipt, independently matched against actual bytes | Inspection |
| --- | --- | --- |
| `66-resumed-fifth-after-epiphany.pdf` | `94fd25fe31f1118927ebd03798c7e7b697fc3e692e548d4afd7f22f7d4ae7e4a` | Every physical page 1–21 |
| `66-resumed-fifth-after-epiphany-synthesis.pdf` | `61b4288d51c5c14c5fbae9aa9882d979846a64024961ad6bb6960cc171d0eaaa` | Every physical page 1–10 |
| `66-resumed-fifth-after-epiphany-homily.pdf` | `d9366042a9cfd13b205871caae258494dbe07fb86a96823e5972d2546b34825e` | Every physical page 1–3 |

Read `research/artifacts.json`; independently matched all 3 PDF hashes,
2 pagination-evidence hashes and 25 render-input hashes both initially and
against the packet's immutable seal at the end. Existing raster receipt file
hashes also matched: study 44 entries, concise 21, homily 7.

Opened the study's two contact sheets and the concise and homily contact
sheets under the build-artifacts-0 raster tree. Then opened each of the 34
individual page rasters with original detail, not merely the sheets. Reopened
the study page 2 and concise page 2 as individual reduced full-page views.
The existing pages have maximum dimension 2200 pixels. The helper also
prepared this dispatch's dedicated raster tree below `rasters/`; its cache
keys and PDF hashes match the inspected build-artifacts-0 pages exactly.

## Page-level inspection

### Expansive study

| Physical page | Inspected content and outcome |
| --- | --- |
| 1 | Full-width title, substantive introduction, first part of eleven-element map; readable single column and consistent hierarchy. |
| 2 | Remaining map rows with repeated table header, usable contents page numbers, appointed-text introduction and Introit beginning; no cell overlap on confirmed viewing. |
| 3 | Introit continuation, Collect and Epistle with distinct Latin and historical-English treatments; no clipping or intrusive furniture. |
| 4 | Gradual, Alleluia and Gospel; headings stay with content and quoted blocks remain clear. |
| 5 | Gospel continuation, Offertory, Secret and Trinity Preface; meaningful continuous pagination and legible Latin. |
| 6 | Preface English, Communion, Postcommunion and detailed-commentary start; transition clearly marked with enough text after the heading. |
| 7 | Introit/Collect/Epistle commentary and four footnotes; text and note area remain distinct. |
| 8 | Epistle continuation, Gradual, Alleluia/Offertory and Gospel start; no orphan heading, note collision or overflow. |
| 9 | Gospel continuation, Secret, Preface and Communion commentary; single-column measure and spacing remain consistent. |
| 10 | Commentary close and first keyed interpretation, “Charity preserves people who may yet become wheat”; substantial reasoning and usable citations. |
| 11 | Augustine and the correcting/forgiving community; comfortably recoverable paragraphs and distinct footnotes. |
| 12 | First interpretation's developed argument and its four-senses beginning; literal item stays intact. |
| 13 | First interpretation's remaining three senses and second keyed interpretation, “The promised salvation is received through prayer and mercy”; matching heading and sense hierarchy. |
| 14 | Penitential prayer and propitiation reasoning; no clipping, heading split or note collision. |
| 15 | Resurrection/pledge and conditions of prayer; dense but legible exposition with separate source notes. |
| 16 | Second interpretation's conclusion and all four senses, then comparison; no artificial blank-page padding. |
| 17 | Comparison ending and historical appendix/table start; rows remain intact and passage/date relationships are visible. |
| 18 | Repeated chronology header and remaining rows, followed by fuller Psalms/Jeremias evidence; no table seam loss. |
| 19 | Matthew/Mark historical explanations and precise notes; typographic hierarchy remains coherent. |
| 20 | Colossians explanation and scope appendix; long record paths wrap without clipping. |
| 21 | Scope continuation, references, visible UTC revision and compact rights colophon; complete terminal content and no rights-only page. |

The two manifest lane keys resolve to headings on physical pages 10 and 13.
Their arguments are actually present, not blank destinations: the first
explains collateral harm, future conversion and human misidentification;
the second explains why divine promise still calls for petition and why
confidence concerns saving good and mercy. Compared those distinguishing
claims with the complete `research/interpretations.md` record. Each has its
own literal, allegorical, moral and anagogical distillation. The first block
spans pages 12–13 with intact items; the second appears on page 16.

### Concise study

| Physical page | Inspected content and outcome |
| --- | --- |
| 1 | No cover displacement; complete eleven-element map in liturgical order followed immediately by exactly Literal, Allegorical, Moral and Anagogical overview rows. |
| 2 | Only Scriptural Date and Location and its source pointer; complete generated orientation table stays on the page and can be used for the lookups below. |
| 3 | Themes and Movement: exile/promise and the forgiven community, with textual reasoning and four source notes; substantial readable page. |
| 4 | Themes and Movement: threatened crop and prayer/pledge; substantial second page with three separate notes. |
| 5 | Developed commentary begins at the top; compares Chrysostom and Augustine on the servants' knowledge and risk, without lane-summary miniatures. |
| 6 | Forgiveness/correction comparison and promise/petition question; contributions to the two interpretations meet at the point of comparison. |
| 7 | Promise, waiting and penitential confidence; note area remains legible and separate. |
| 8 | Saving object of prayer and completion of the pledge; explicit comparison of the two interpretations with intact qualifications. |
| 9 | Commentary conclusion, scope and beginning of references; dense but readable, without a stranded heading. |
| 10 | Remaining references, revision and compact rights colophon; terminal remainder contains substantial bibliography rather than a rights-only spill. |

Actual pages agree with the sealed `.aux` absolute-page markers: inventory and
overview start/end 1; all four overview sense markers 1; chronology start/end
2; themes start 3/end 4; commentary start 5. Physical lengths 21 and 10 are
within the required 20–50 and 10–12 ranges. No page-counter reset or enlarged
body type is involved.

### Homily

| Physical page | Inspected content and outcome |
| --- | --- |
| 1 | Full-width title followed by two-column speech; clear paragraph breaks and no inline scholarly notes. The column transition is recoverable. |
| 2 | Two-column speech continues and concludes; balanced final columns, semantic Homily running head and no apparatus inserted into the speech. |
| 3 | Separate full-width source/delivery note, references, UTC revision and compact rights colophon; all readable and unclipped. |

The spoken argument is continuous prose about preserving people who can still
change, forgiving/correcting, the petitioner's own need for mercy, and hope
after the pledge. No recurring register defect or unsupported theatrical
device was found in the visual read. The delivery figures are explicitly
estimates, not a claimed timed human event.

## Concrete chronology lookups

Performed on concise physical page 2 as an individual full-page view, then
checked at original raster detail. The table is set at the shared 9.5-point
size, not microscopic fitted text.

1. **Epistle, Colossians 3:12–17:** found the final table row, read the
   composition subject and “Traditional Roman captivity; recipients at
   Colossae,” and paired it directly with “Disputed: A.D. 61; A.D. 61–63.”
   The same row visibly qualifies the wider authorship/prison-site question.
   No excursion through another column's paragraph was needed.
2. **Communion, Mark 11:24:** found its two adjacent rows. The traditional
   composition row names Rome, separately identifies the instruction's
   Jerusalem/Bethania narrative setting, and retains the several traditional
   dating alternatives. The next row is explicitly a Catholic-critical
   comparison, names the tentative anonymous-author/Syria proposal, and pairs
   it with “Perhaps shortly after A.D. 70.” The displayed distinction
   prevents taking the Gospel's composition date as the instruction's date.
3. **Alleluia and Offertory, Psalm 129:1–2:** found the shared historical-setting
   row with unknown occasions/places and unresolved date, then the separate
   composition row with an unknown writing site and the explicitly
   Psalter-wide “Before c. 165 B.C.” bound. Consolidated labels are long but
   do not obscure the different dated subjects.

The appendix on study pages 17–20 preserves fuller explanations and the
source loci pointed to from the concise table. This inspection checked the
presentation and accurate recovery of displayed relationships, not a new
exhaustive historical-source adjudication.

## Other verification and limits

- `pdfinfo` and `pdffonts` succeeded for all three: letter pages, no encryption,
  expected titles/subjects, a modification time matching the displayed
  revision, and every font embedded with Unicode mapping. Fonts are Latin
  Modern. File sizes are 457652, 406678 and 267807 bytes for study, concise
  and homily respectively; no size threshold investigation is triggered.
- Read the three literal entrypoints and shared format owners. The baseline
  is `article[11pt]`, Latin Modern and 0.75-inch geometry. Both studies are
  single column; only the homily imports the two-column environment.
- Inspected the settled build logs: no actual Overfull, Underfull, undefined
  reference or layout-warning lines were found. The matched `Rerun` text is
  the package-identification line for `rerunfilecheck`, not a rerun warning.
- Text extraction succeeded for all PDFs and corroborates page content,
  complete terminal notices and speech/apparatus separation.
- Investigated an apparent map-cell collision on study page 2. PDF bounding
  boxes put “Deus” at x=254.628831–276.154025 points and “Those” at
  x=287.720603–313.780773: an 11.566578-point gap. The second individual
  viewing confirms the gap. This candidate was rejected, not reported as a
  defect.
- This is a new leaf, not a formatting migration; no historical substantive
  text-preservation comparison was claimed. No physical print, audible
  rehearsal, timed human delivery, fresh exhaustive source audit, installed
  mirror comparison or web acceptance was performed. Those are not inferred
  from these screenshots.
- No reviewed source or PDF was edited, no engine transition submitted, no
  commit/push/branch switch, no nested agent and no tooling/workflow/tmt edit.
  Created only this dispatch's scratch results, extractions and dedicated
  raster tree. Every invoked command completed; no live session, background
  process or unreconciled operation handle remains.
