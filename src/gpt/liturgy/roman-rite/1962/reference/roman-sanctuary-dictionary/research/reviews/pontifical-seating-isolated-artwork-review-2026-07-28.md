# Pontifical-seating isolated artwork review

Date: 2026-07-28

Assets:

- `shared/artwork/pencil/RPD-FIG-pontifical-seating-0001-episcopal-throne-alpha.png`
- `shared/artwork/pencil/RPD-FIG-pontifical-seating-0002-covered-faldstool-alpha.png`

Asset-side provenance:

- `shared/artwork/pencil/RPD-FIG-pontifical-seating-0001-episcopal-throne-alpha.toml`
- `shared/artwork/pencil/RPD-FIG-pontifical-seating-0002-covered-faldstool-alpha.toml`

## Scope and source boundary

The two corrected drawings replace the old plate's misleading dependence on a
single four-object comparison. The throne is controlled by *Caeremoniale
Episcoporum* I.XIII.3 and the admitted HABS Baltimore witness: it is fixed,
high, and elevated on exactly three covered steps, with the seat itself
visibly covered in silk. Textile is visible over every tread and riser. The
isolated drawing omits the
canopy because the Ceremonial makes that feature conditional; the HABS
witness's marble, heraldry, curtains, attendant chairs, and architecture are
also omitted.

The faldstool is controlled by *Caeremoniale Episcoporum* I.XII.10-11 and the
Metropolitan Museum's Open Access exemplar. The drawing shows the checked
covered ceremonial state: a plain cushion beneath a continuous plain covering
that rests fully on the ground. Concealing the construction, cushion edge,
feet, and supports is deliberate. The drawing
therefore neither repeats the old plate's universal-looking X-frame nor
promotes the museum exemplar's backlessness, rails, finials, fringe, or
materials into a general rule.

These are isolated identity assets, not a complete pontifical-station
composition. A later TeX-owned side-by-side layout may safely compare
`fixed / high / three steps` with `portable / covered ceremonial state`,
provided its labels preserve the conditional canopy and morphology limits.
No generated spatial-comparison asset was admitted because the governing
sources do not yet close every placement and ceremony branch needed for one
universal scene.

## Generation and boundary treatment

The built-in image-generation tool produced each graphite study on a flat
green chroma field. The installed imagegen helper sampled the border, made a
soft alpha matte, and despilled the subject. The accepted outputs were then
converted deterministically to stripped 8-bit grayscale-alpha PNGs while
preserving alpha.

The exact final prompts are retained in the asset-side TOML records.

## Visual acceptance

- the throne drawing contains one chair and exactly three visible steps, with
  textile over every tread and riser;
- the throne seat is unmistakably covered rather than bare;
- the throne reads as fixed, high, and elevated;
- no canopy or copied HABS ornament appears;
- the faldstool drawing contains one compact covered seat with a plain
  unbuttoned cushion beneath the continuous covering;
- the covering rests fully on the ground, with no exposed foot or support;
- the covering conceals rather than invents a universal folding mechanism;
- no exposed X-frame, throne, platform, kneeler, or person appears in the
  faldstool asset;
- neither asset contains text, semantic marks, borders, scenery, or cast
  shadows;
- ImageMagick reports the throne as `1133x1388`, `graya 2.0`, 8-bit, with
  corner pixel `graya(0,0)` and mean alpha `0.43193`;
- ImageMagick reports the faldstool as `1389x1132`, `graya 2.0`, 8-bit, with
  corner pixel `graya(0,0)` and mean alpha `0.535916`;
- warm-paper composites show clean, blended boundaries without a floating
  rectangular field or visible green fringe.

SHA-256:

- throne:
  `34d9ddd00dcdaf4f1e67577b2efdf8cdedbf741fd8ad83d8c0c31918d5f3a6d0`;
- covered faldstool:
  `4abae4e603908cb2b7a02fa813eeff70664b04ef454a795e2e67e77470eea9c6`.

Status: accepted as source-bounded Alpha educational illustrations, pending
canonical manifest admission, placement, and whole-publication review by the
dictionary integration lane.
