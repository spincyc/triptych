# Cold review of the six selected dictionaries — 2026-11-05

This review examined the current canonical renderer, selection and artwork
gates, all six existing November 5 print contact sheets, extracted text from
all six PDFs, and enlarged representative plate pages. It distinguishes
defects in admitted selections from the unadmitted inventory. No new
liturgical or morphological contradiction was confirmed by this bounded
review; that is not a claim that the unfinished corpus has been collated.

The baseline receipts and page rasters were under
`.scratch/dictionary-art/print-labels/` and
`.scratch/dictionary-art/page-review-labels/`. These are disposable review
artifacts, not distribution sources. The baseline had 11 altar-server,
14 comprehensive, 12 general-reader, 11 MC/trainer, 17 pontifical and
13 sacristan pages.

## Confirmed defects and implementation response

1. **High: exact sources were absent from every reader PDF.** Canonical
   records emitted `RSDSourceBinding`, but the object API's empty default
   remained active; the publication shell ended without references.
   The renderer now prints compact numbered object notes, exact recorded
   loci, and the selected source editions' canonical titles and publication
   statements. Superscripts connect plate names to these notes. It refuses
   unknown bindings or unidentified editions rather than inventing a title.
   This refusal exposed legacy source aliases and unregistered source names
   that require independent canonical source reconciliation. Neither old
   artifact admission nor an old claim-verified flag resolves that defect.
   The November 5 correction batch resolved the admitted selections'
   bindings; all six selections subsequently generated with exact source
   notes. This does not assert that bindings in held inventory records
   have been reconciled. See `source-audit.md` and the dated slice reports
   for the source-level corrections and witness limitations.

2. **Medium: independently fitted figures had no scale notice.** The
   scale macro existed only in the demonstration fixture; the publication
   renderer ignored the artwork scale field. The pontifical ring beside
   the crosier was a conspicuous example. Every generated comparison plate
   now states that figures are not to common scale.

3. **Medium: redundant prose burdened small captions.** Seven exact
   identity/use pairs repeated the same material facts: chalice, sanctuary
   lamp, purificator, corporal, chalice pall, burse and altar cloths.
   Only those reviewed pairs suppress the repeated use sentence. A digest
   guard restores both sentences if either claim changes; the canonical
   claims remain intact. Other identity/use pairs retain their distinct
   qualifications beside the figure. Ordinary captions and reader notes
   have slightly larger type and ragged right margins. Source apparatus
   cites evidence without repeating the canonical audit ledger.

4. **Medium: a recorded handling boundary disappeared.** For example,
   the chalice's canonical `must-not-handle` relation did not appear in
   the altar-server card. The server edition now prints the relevant
   recognition/direction boundary from the existing canonical field.
   Independent review also found that the entire canonical
   `handling.warnings` list was discarded. Those warnings now appear as
   care/limit qualifications beside figures in every edition. Existing
   audience qualifications remain visible; final page review checks the
   resulting caption space.

5. **Medium: comprehensive selection excluded admitted pontifical
   objects.** Thirteen records already passed the same object/artwork
   gates used by the pontifical edition. Removing those exclusions and
   providing four comparison plates makes the comprehensive edition
   include them. The remaining held objects and missing inventory families
   remain unfinished work; the edition title does not assert completeness.

## Scope of the added layouts

The thirteen existing pontifical records are episcopal throne, faldstool,
bugia, crosier, mitre-minister veil, mitre, pontifical buskin, pontifical
dalmatic, pontifical gloves, pontifical ring, pontifical sandal, pontifical
tunicle and vimpa. Sacred vesture, insignia, seating and ministerial
relationships receive separate comparisons. Sacristy lavatory, gremial and
pectoral cross retain explicit exclusions and their underlying holds.

The separate, source-collated clothing slice contributes cassock and
surplice, with three figures: the two isolated garments and one shared worn
ensemble. The ensemble has one rendering owner. Its isolated consumer
preview uses the production plate functions without changing canonical
admission flags; source and visual review precede promotion.

## Verification and remaining distinction

Focused regressions cover exact caption fallback, exact source
title/edition/locus rendering, source metadata dependency paths, refusal of
unknown or unidentified sources, and the shared clothing figure's owner.
The source-note metadata participates in native artwork/source closure
and edition revision closure. Make's existing phony generator dependency
regenerates the notes for each selected print build.

Final print receipts, all-page visual review, source corrections and
admission results belong in the current delivery and artwork records.
This review records the initial findings and rationale; it must not be
read as a second, competing completion ledger or as approval of held
objects.

## Final screen-proof receipt

The final six selected print recipes passed on November 5. Thirty focused
generator and native-artwork tests passed. All six build logs were free of
overfull/underfull boxes, missing glyphs and undefined references. Extracted
PDF checks found each References heading with its first entry, a substantive
final page containing the rights/revision colophon, the expected scale
notice on every comparison plate, and no raw structured publication audit
data. These checks supplement visual review: the first candidates had
actual text collisions despite clean TeX logs.

The shared pontifical cutaway now renders once per active consumer under
the explicit dalmatic owner. The tunicle entry supplies an inside-to-outside
key naming tunicle, dalmatic and chasuble; both canonical entries, their
source numbers and qualifications remain. Exact duplicate warning/audience
sentences render once; changed or distinct text remains visible. Enlarged
card rows and adjusted appendix paragraph spacing resolved the observed
collisions, stranded headings and colophon-only spill page without reducing
type sizes.

Coverage was divided and independently checked as follows. Page numbers
here are physical PDF pages, including the title page.

- The independent cold reviewer inspected every page of comprehensive and
  altar-server candidate v2, then all 15 changed final pages; hashes proved
  the other 20 pages unchanged. All 401 numbered source/reference links in
  the two final PDFs resolved to their expected targets. Comprehensive's
  final colophon shares page 21 with references.
- The coordinator reviewed every general-reader and sacristan page in the
  contact sheets, enlarged the dense v2 pages, and enlarged final
  general-reader pages 6, 9, 13–15 and sacristan pages 8, 13–16. The lavabo
  collisions were gone; references and rights remained with their content.
- The renderer reviewer inspected the MC/trainer and pontifical contact
  sheets and enlarged every body plate in v2. Final changed MC/trainer
  pages 2, 3, 9, 12–14 and pontifical pages 4, 18–20 were enlarged again;
  the unchanged body pages were verified by raster hashes. No remaining
  overlap, clipped figure, missing qualification or stray appendix page
  was found.
- The clothing/source reviewer independently collated the clothing and
  ombrellino pages in all six v2 editions. The final raster comparison
  confirmed all six clothing pages unchanged. Ombrellino-page approval
  transferred only where the final raster hash matched; changed pages,
  including general-reader page 9 and sacristan page 13, received enlarged
  final inspection by the respective reviewer. Source ceilings, the
  combined clothing label and the 1952 Ritual non-collation qualification
  remained visible.

An independent follow-up checked all 1,165 parsed numbered links in the
six final PDFs: altar-server 180, comprehensive 221, general-reader 179,
MC/trainer 184, pontifical 217 and sacristan 184. There were no target
mismatches among those numbered source/reference links.

The exact final proof PDFs were built beneath
`.scratch/dictionary-cold-review/print-final/`, with print receipts beside
them; all-page rasters were beneath `final-pages-complete/` in the same
scratch owner. The proofs contain uncommitted-source revision stamps.
They establish screen-proof and consumer review, not a physical ink/paper
test or independent admission of any held object.

| Edition | Pages | SHA-256 of final proof PDF |
| --- | ---: | --- |
| Altar-server | 14 | `12914d86260d6d6efcfb2fb1c58dcc9cfd8b7ce4e94775affdac981522343db6` |
| Comprehensive | 21 | `52ccf0670077634ac1d3ba65f846175a4662d99ee20353f2a4a711ea49e57002` |
| General-reader | 15 | `d1a73ea89ef0764e313647b66a270240ddd75947dfc89c6c4fb76af558fec3d6` |
| MC/trainer | 14 | `30a5bac53e748e12334b11b332abd94c292ae05381e46316d93e5d88bb007931` |
| Pontifical | 20 | `922c3390a7f4adc63c112c57ad0947b1c225623e804be791e28126ba1707167c` |
| Sacristan | 16 | `2393b5f0f7213a62d6925840370fd9df97584bcbdbb4f95a6356aed5e1aa82f7` |
