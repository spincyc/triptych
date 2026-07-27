# Research slice: pontifical insignia and attendants' objects

Audit date: 2026-07-27 (America/Chicago).

Status: **source-checked working slice; held from publication**.

This standalone slice owns the initial records and one comparison asset for
the crosier, three mitre forms, gremial, bugia, and the pair of shoulder veils
commonly called vimpae. It does not alter the canonical aggregate. Promotion
requires schema migration, independent ceremonial review, a morphology
source, and actual-size monochrome print review.

## Source inspected

`Cæremoniale Episcoporum`, editio typica, 1948 printing of the
Leo XIII recension (1886), complete local scan and OCR inspected
2026-07-27:

- book I, chapter XI, sections 1, 5, 6, and 9: the ministers of the
  pastoral staff, mitre, candle, and gremial; the oblong silk veil hung from
  the mitre minister's neck; and the handling of the gremial;
- book I, chapter XVII, sections 1--6: the three forms of mitre and the
  bishop's use of the pastoral staff;
- book I, chapter XX, section 1: the small silver implement commonly called
  the *bugia*, bearing a lit candle beside the book.

Source-binding candidate:
`edition.catholic-church.caeremoniale-episcoporum.typica-1948`.
That binding is not yet registered in `src/sources/`; this slice therefore
records exact checked loci but remains held.

The twelfth revised 1962 edition of Fortescue--O'Connell is a registered
contemporary ceremonial-manual lead:
`edition.adrian-fortescue.ceremonies-of-the-roman-rite-described.twelfth-revised-1962`.
Only its bibliographic record and Google Books index were available in this
pass; no object claim below is attributed to an uninspected page of it.

## Held object records

### `obj-crosier`

- Preferred English name: crosier
- Latin headword: *baculus pastoralis*
- Category/status: pontifical and prelatial; universal Roman at the 1962
  horizon
- Checked identity/use: the *Cæremoniale* assigns a minister to keep and
  carry the pastoral staff and describes the bishop's use of it in his city
  or diocese and in specified processions and functions (I.XI.5;
  I.XVII.4--6).
- Handling boundary: a server may encounter the designated minister carrying
  and presenting it; the bishop's own use and jurisdictional conditions must
  not be reduced to a generic “bishop always carries it” caption.
- Artwork: `DIC-ART-PI-001`, isolated comparison view.
- Workflow: source-audited claim lead; artwork not approved.

### `obj-mitre`

- Preferred English name: mitre
- Latin headword: *mitra*
- Category/status: pontifical and prelatial; universal Roman at the 1962
  horizon
- Checked identity/use: the *Cæremoniale* names three species and supplies
  their construction and use distinctions (I.XVII.1--4). It also describes
  the mitre minister and the dependent lappets, *vittæ* or *infulæ*
  (I.XI.6).
- Substantive variants:
  - `var-mitre-pretiosa` — *mitra pretiosa*, customarily enriched with gems,
    precious stones, or gold or silver work;
  - `var-mitre-auriphrygiata` — *mitra auriphrygiata*, without the precious
    plaques or gems of the first form, but with restrained pearls, gold-worked
    white silk, or cloth of gold;
  - `var-mitre-simplex` — *mitra simplex*, without gold, in plain white silk
    or linen, with dependent lappets and red fringe as specified by the
    source.
- Artwork: all three forms appear in `DIC-ART-PI-001`; the grayscale
  distinction is ornament density rather than unsourced color.
- Workflow: source-audited identity/variant lead; generated forms need an
  independent vestment-morphology check.

### `obj-gremial`

- Preferred English name: gremial
- Latin headword: *gremiale*
- Category/status: linens and textiles; pontifical and prelatial; universal
  Roman at the 1962 horizon
- Checked identity/use: a dedicated minister receives the gremial after an
  assistant removes it from the seated bishop's lap, holds it folded at the
  breast in both hands, returns it through the assistant when needed, and
  finally replaces it on the credence after the Offertory handwashing
  (I.XI.9).
- Evidence ceiling: the checked locus establishes the lap placement,
  folding, minister, and ceremonial handling. It does not by itself establish
  every material, dimension, ornament, or fastening shown by the generated
  specimen.
- Artwork: `DIC-ART-PI-001`, isolated unfolded editorial specimen.
- Workflow: source-audited use lead; morphology held.

### `obj-bugia`

- Preferred English name: bugia
- Latin headword: *bugia*
- Alternate English name: hand-candle
- Category/status: service objects; pontifical and prelatial; universal Roman
  at the 1962 horizon
- Checked identity/use: the *Cæremoniale* describes the small silver
  instrument commonly called the *bugia*, with a lit candle above it, held by
  the candle minister beside the minister presenting the book even when
  ambient light is sufficient (I.XX.1).
- Artwork: `DIC-ART-PI-001`, isolated side-handled candlestick.
- Workflow: source-audited identity/use lead; exact form held for morphology
  review.

### `obj-vimpa`

- Preferred English name: vimpa
- Latin headword: *velum*; terminology lead *vimpa*
- Preferred printed plural: vimpae
- Category/status: linens and textiles; pontifical and prelatial; universal
  Roman at the 1962 horizon
- Checked identity/use: the mitre minister wears an oblong silk veil or cloth
  hanging from his neck and uses it to support the mitre so that it is not
  touched with bare hands, unless he wears a cope (I.XI.6).
- Evidence ceiling: the checked governing text calls the article *velum, seu
  mappa sericea oblonga*; it does not use the headword *vimpa* in the
  inspected passage. The familiar headword and the existence of a matching
  pair need a lexical/morphology source before publication.
- Artwork: `DIC-ART-PI-001`, paired isolated editorial specimens;
  `DIC-ART-PI-002`, in-use context candidate.
- Workflow: function source-audited; terminology and paired morphology held.

## Artwork record: `DIC-ART-PI-001`

- Asset:
  `shared/artwork/pontifical-insignia/DIC-ART-PI-001-pontifical-insignia.png`
- Depicts: `obj-crosier`, `obj-mitre` and its three listed variants,
  `obj-gremial`, `obj-bugia`, and `obj-vimpa`
- View: dense isolated comparison; not to common scale
- Generator: built-in OpenAI image-generation interface; no model/version
  exposed
- Created: 2026-07-27
- Reference images supplied to the generator: none
- Prompt summary: a US-Letter-portrait, white-ground, museum-catalog graphite
  plate of one traditional crozier, precious/gold/simple mitres grouped for
  comparison, one unfolded gremial, one small side-handled bugia with candle,
  and a matching pair of draped vimpae; no people, text, labels, arrows,
  borders, color, or unrelated objects
- Received dimensions: 1024 by 1536 pixels
- Repository file: stripped 8-bit grayscale PNG, 662,265 bytes
- SHA-256:
  `3b910adc92b1a9743cd91646c61d1c137f0e719f7a94942d343889e0f610712a`
- Personal screen review completed: correct requested object count; three
  visibly distinct mitres with two lappets each; crozier, lap-cloth specimen,
  hand-candle, and paired veil specimens remain visually separated; no
  generated lettering, arrows, border, color, people, or unrelated ceremonial
  object detected
- Known review limitations: the crozier uses one ornate figural crook rather
  than a neutral morphology; the gremial's ties and the exact construction of
  the bugia and vimpae are not established by the checked loci; the vimpae
  can still resemble stoles without an in-use inset; the raster does not
  provide 300 effective dpi at a large full-page placement
- Review state: **identity-checked editorial candidate; not liturgically,
  print, independently, or release approved**

## Artwork record: `DIC-ART-PI-002`

- Asset:
  `shared/artwork/pontifical-insignia/DIC-ART-PI-002-vimpa-in-use.png`
- Depicts: `obj-vimpa` in use with `obj-mitre`
- View: context inset; scale not applicable
- Generator: built-in OpenAI image-generation interface; no model/version
  exposed
- Created: 2026-07-27
- Reference images supplied to the generator: none
- Prompt summary: a single adult clerical mitre minister in black cassock and
  white cotta/surplice, wearing one continuous oblong silk shoulder veil whose
  two broad ends cover both hands as he supports one mitre at chest height;
  white-ground graphite, no bishop, second minister, text, labels, arrows, or
  color
- Received dimensions: 1024 by 1536 pixels
- Repository file: stripped 8-bit grayscale PNG, 668,413 bytes
- SHA-256:
  `474fbdd235e8d2d07edc899fcff41c16ed8a9aea584eb26f251871cd02c844a0`
- Personal screen review completed: exactly one minister and one mitre; the
  continuous veil passes from the neck across both forearms and covers the
  hands; cassock and surplice are distinct; the mitre's dependent lappets are
  visible; no generated text, labels, arrows, color, or unrelated ceremonial
  object detected
- Known review limitations: the image reads clearly as a handling context but
  does not by itself prove the conventional headword *vimpa*; the precise
  breadth and drape require independent morphology review; the raster does
  not provide 300 effective dpi at a large full-page placement
- Review state: **function-checked editorial candidate against I.XI.6; not
  independently, print, or release approved**

## Required next pass

1. Register and rights-audit the exact `Cæremoniale Episcoporum` edition and
   artifact under `src/sources/`, with passage records for the loci above.
2. Inspect the 1962 Fortescue--O'Connell pages for contemporary English
   terminology and practical morphology.
3. Add a reliable textile/material-culture source for gremial and vimpae and
   a metalwork source for crozier and bugia forms.
4. Independently review the in-use context inset for the mitre minister's
   veil and replace any generated construction not supported by the source
   audit.
5. Run independent pontifical ceremonial review and actual-size monochrome
   print review before migrating these records into the canonical inventory.
