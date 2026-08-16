# Map provenance: the Ark's journey and the New-Ark overlay

Checked through: 2026-08-16.

## Identity and purpose

- Stable map ID: `ARK-MAP-001`.
- Owner: `src/gpt/theology/mariology/ark-of-the-covenant/`.
- Consumer: `sections/55-map.tex`.
- Text equivalent: `sections/55-map-text-equivalent.tex`.
- Deterministic semantic layer:
  `artwork/ark-journey-vector-map.tex`.
- Active deterministic cartographic base:
  `artwork/ark-journey-cartographic-graphite-v3.png`.
- Reproduction recipe:
  `artwork/build-ark-journey-cartographic-base.mjs`.
- Input and transformation receipt:
  `research/cartographic-base-v3-receipt.json`.
- Purpose: orient the reader to Scripture's narrated Ark stations and to
  Mary's New-Ark journey without turning literary sequence, typology,
  traditional identification, or archaeological site location into a
  recovered road or event coordinate.
- Cartographic mode: two north-up EPSG:3857 physical-geography panels beneath
  an independently authored semantic overlay. It is deliberately not a
  survey, navigation chart, route reconstruction, or claim that a biblical
  event has been geolocated.

## Faithful source-control boundary

This audit belongs inside an affirmative Catholic exposition. It does not
begin from secular suspicion of sacred history, nor does it treat the Church's
received reading of Mary as the New Ark as a theory to be explained away.
Instead it distinguishes what the inspired texts narrate, what a later
tradition identifies, what archaeology can locate, and what a modern map can
only illustrate. That discipline protects rather than weakens the typology:
the theological synthesis rests on Scripture read within the Church, not on a
modern line pretending to recover an unrecorded road.

The active PNG owns physical-geography presentation only: generalized land,
coast, lakes, rivers, and relief in the declared projection and bounds. Those
features do not establish an ancient place, route, event, border, distance, or
archaeological conclusion. The base is source-derived and reproducible, but it
is still generalized modern cartography rather than survey evidence for the
Ark's movements.

The TeX/TikZ layer owns every semantic item: station position, station number,
route, line status, label, uncertainty area, traditional-site symbol, legend,
caption, and typological relationship. The textual equivalent states the same
claims without the raster or TikZ. The station and route registers below, not
the cartographic pixels, control those layers. Removing the PNG must leave the
complete narrated sequence, evidence distinctions, and typological
relationship recoverable from the overlay and textual equivalent.

The base draws no label, pseudo-text, route, arrow, station marker, political
boundary, icon, Ark, person, building, road, compass, scale, or coordinate
grid. A cartographic pixel never determines theological meaning or evidence
status.

## Station and status register

Coordinates below are source-supported locator centroids for modern,
traditional, or archaeological places.  They are not coordinates of the Ark,
an event, a house, a tent, or a recovered road.  Unlocated places receive no
coordinate.

| ID | Display | Status and allowed geometry | Controlling loci / geographic source |
| --- | --- | --- | --- |
| 1 | Sinai/Horeb | Textual region; biblical mountain disputed. Jebel Musa/Saint Catherine may appear only as a traditional locator, 28.56, 33.98. | Ex 40:20--21; Nm 10:11--36; [UNESCO Saint Catherine](https://whc.unesco.org/en/list/954/) |
| 2 | Kadesh region | Region/candidate only; optional Tell el-Qudeirat locator 30.65, 34.42 is not proof of the narrated camp. | Nm 13:26; 14:44; 20:1; [IAA Reports 44](https://publications.iaa.org.il/iaareports/44/) |
| 3 | Moab/Shittim | Textual region; no event coordinate. | Nm 21:10--20; 33:44--49; Jos 3:1 |
| 4 | Jordan/Gilgal | Broad area only; exact crossing and Gilgal unlocated. | Jos 3:1--4:20; [Na'aman 2024](https://doi.org/10.1080/03344355.2024.2327800) |
| 5 | Jericho | Ancient-site locator at Tell es-Sultan, 31.87, 35.44; no claim that archaeology locates Joshua's procession. | Jos 6; [UNESCO Tell es-Sultan](https://whc.unesco.org/en/list/1687/) |
| 6 | Ebal/Gerizim | Paired-mountain zone; the map does not identify a disputed structure as Joshua's altar. | Jos 8:30--35 |
| 7 | Shiloh | Strong site identification at Khirbet Seilun, 32.056, 35.290; no Ark/tabernacle footprint. | Jos 18:1; 1 Sm 3:3, 21; 4:1--12; [ODB Shiloh](https://www.odb.bibelwissenschaft.de/ortsnamen/ortsname.php?n=162) |
| side | Bethel | Majority identification at Beitin, 31.926, 35.237; episodic Ark presence, no route. | Jgs 20:18, 26--28; [ODB Bethel](https://www.odb.bibelwissenschaft.de/ortsnamen/ortsname.php?n=18) |
| 8 | Ebenezer? | Textual battle camp unlocated; `Izbet Sartah--candidate` may be plotted only as a hollow candidate. | 1 Sm 4:1--11; 5:1; [AUSS 36.1](https://www.andrews.edu/library/car/cardigital/Periodicals/AUSS/1998-1/1998-1-05.pdf) |
| 9 | Ashdod | Tel Ashdod locator 31.7560, 34.6561; no Dagon-temple coordinate. | 1 Sm 5:1--7; [Trismegistos place 37278](https://www.trismegistos.org/place/37278) |
| 10 | Gath | Widely accepted Tell es-Safi locator 31.7013, 34.8468. | 1 Sm 5:8--9; [Tell es-Safi/Gath project](https://gath.wordpress.com/about/project-overview/) |
| 11 | Ekron | Secure Tel Miqne identification, locator 31.7797, 34.8484. | 1 Sm 5:10--6:16; [ORACC/Pleiades record](https://oracc.museum.upenn.edu/geonames/cbd/qpn/x000000170.html) |
| 12 | Beth-shemesh | Strong Tel Beth-shemesh identification, locator 31.7505, 34.9747; Joshua's field unlocated. | 1 Sm 6:9--21; [Tel Aviv University excavation](https://en-humanities.tau.ac.il/beth-shemesh) |
| 13 | Kiriath-jearim/Baalah | Secure Deir el-Azar identification, locator 31.8094, 35.1036; Abinadab's house unlocated. | 1 Sm 6:21--7:2; 2 Sm 6:2--4; [TAU/College de France project](https://kiriathjearim.wordpress.com/) |
| 14 | Perez-uzzah | No point or coordinate. Nacon/Nachon/Nodan--Chidon names one unlocated event-place. | 2 Sm 6:6--9; 1 Chr 13:9--11 |
| 15 | Obed-edom | No point or coordinate. `Gittite` is not a geocode for the house. | 2 Sm 6:10--12; 1 Chr 13:13--14; 15:25 |
| 16 | City of David / biblical Zion | Area marker; the tent is unlocated. Do not substitute modern western Mount Zion. | 2 Sm 5:7; 6:12--17; 1 Chr 15:1--3; [IAA southeastern-hill report](https://hadashot.iaa.org.il/report_detail_eng.aspx?id=27736&mag_id=139) |
| 17 | Solomon's Temple | Sacred-precinct area marker; exact First-Temple/Holy-of-Holies footprint unresolved. | 1 Kgs 8:1--11; 2 Chr 5:2--14 |
| N1 | Nazareth | Text-named city. A shrine coordinate, if retained elsewhere, is a modern traditional proxy rather than the event point. | Lk 1:26--38; [IAA Nazareth excavation](https://publications.iaa.org.il/atiqot/vol98/iss1/3/) |
| N2 | Town in Judah's hill country | Text-named region; town unnamed. Area only, never a coordinate. | Lk 1:39--56 |
| tradition | Ein Karem | Later Christian traditional identification; double-outline symbol separate from N2's textual status. | [Custody of the Holy Land, Visitation](https://www.custodia.org/en/sanctuaries/ain-karem-visitation/) |

## Route register

| Route | Evidence class | Visual grammar and boundary |
| --- | --- | --- |
| Sinai to first rest | Ark movement explicit for one three-day journey | Solid line that fades into the wilderness uncertainty; do not extend the leading-Ark claim to the entire itinerary. |
| Wilderness to Kadesh and Moab | Israel/camp movement; Ark accompaniment inferred | Long-dashed schematic corridor. Numbers 21 and 33 remain distinct textual sequences. |
| Shittim/Jordan/Gilgal | Ark carried explicitly; endpoints broad | Solid within an uncertainty area; no exact crossing or road. |
| Jericho circuit | Ark procession explicit | Small symbolic loop, not a surveyed wall circuit. |
| Gilgal to Ebal/Gerizim; Ebal/Gerizim to Shiloh | Separately attested Ark presences; intervening legs not narrated | Dotted connectors. |
| Shiloh to Ebenezer candidate; Ebenezer candidate to Ashdod | Movement narrated, candidate location uncertain | Long-dashed connectors. Aphek is battle context, not an Ark stop. |
| Ashdod--Gath--third Philistine city | Version-sensitive narrated sequence | The map follows the Hebrew/Vulgate/Douay branch, which names Ekron; the registered Brenton Septuagint names Ascalon/Ashkelon. The chosen branch and the alternative are printed in the key. Gaza remains only in the five-lord offering list. |
| Third Philistine city to Beth-shemesh | Departure is implied by narrative continuity; the destination is explicit | Long-dashed connector, followed by a solid schematic link from Beth-shemesh to Kiriath-jearim. |
| Kiriath-jearim to City of David | Direction and destination narrated; Perez-uzzah and Obed-edom unlocated | Dotted-edged broad corridor with events in a non-geographic narrative box. |
| City of David to Temple | Transfer explicitly narrated | Short solid schematic connector. |
| After Temple | No recoverable earthly itinerary | Faded terminus and stop bar; no Babylon, Nebo, Ethiopia, or other speculative arrow. |
| Nazareth to Judah's hill country | Departure point inferred from narrative context; destination region explicit, route absent | White-cored dashed double line into a region, not a pin. |
| Ein Karem | Traditional association only | Dash-dot leader to N2 region; never inherits Luke's textual status. |
| Ein Karem to Jerusalem | Not narrated | Prohibited: no line. Luke closes the Visitation before the later infancy sequence begins. |

## Active v3 cartographic base

### Projection and panel geometry

Both panels are north-up EPSG:3857 Web Mercator crops. The bounding boxes in
the receipt are expressed in WGS84 longitude and latitude in the order west,
south, east, north; the recipe projects them before drawing. Pixel rectangles
refer to the 3800 by 2436 output canvas.

| Panel | WGS84 bounding box | Output rectangle |
| --- | --- | --- |
| Regional | 31.0, 27.4, 36.5, 33.5 | x 84; y 98; width 1739.71069; height 2240 |
| Levant enlargement | 33.1, 31.2, 36.2, 33.5 | x 1916; y 427.485612; width 1800; height 1581.028777 |

The regional panel supplies the Sinai-to-Levant frame. The enlargement gives
the closely spaced biblical stations enough room for legible live labels. The
projection and bounds make the geographic base reproducible; they do not make
the map a survey, a recovered itinerary, or a statement that disputed biblical
locations have been settled.

### Exact cartographic inputs

The vector base uses four exact Natural Earth 1:10m GeoJSON layers from release
5.1.2, commit `f1890d9f152c896d250a77557a5751a93d494776`. Their complete upstream
files are registered as remote source artifacts; the recipe verifies each file
before cropping or drawing.

| Layer | Upstream file | SHA-256 |
| --- | --- | --- |
| Land | `ne_10m_land.geojson` | `1ac90796408bc6ad6911d69448485d3c4dbf2190370080368a09976e1c9f7416` |
| Coastline | `ne_10m_coastline.geojson` | `6f75ae0e0de157b14946e2255eb1f5486d9a13819032e26d4610852d296788f6` |
| Lakes | `ne_10m_lakes.geojson` | `2d036f53dedec578001c5c30c2959ee7d4eebc1306900fa4367c49929ec8f2d9` |
| Rivers and lake centerlines | `ne_10m_rivers_lake_centerlines.geojson` | `bb854a900ecbd3b408df46d5e16e3e0f974ba55993f9d8b5c26e855273c0905a` |

Relief comes from exactly 88 Mapzen Terrarium PNG tiles at zoom 9: x 300--307
and y 205--215. Every request is pinned to an S3 `versionId`, not merely to a
mutable tile URL. For every tile, the tracked receipt records z/x/y, versioned
URL, version ID, SHA-256, byte size, and the exact
`X-Imagery-Sources` response-header value. On acquisition the recipe requires
both `x-amz-version-id` and `x-amz-meta-x-imagery-sources` to match the pin;
cached bytes are still hash-checked. The 88 per-tile header values name the
actual mixture of SRTM, GMTED2010, and ETOPO1 source files rather than assigning
one guessed lineage to the whole crop.

`research/cartographic-base-v3-receipt.json` is the complete machine-readable
manifest. This narrative deliberately does not duplicate its 88-row tile table,
because a second manually maintained copy would be a weaker audit record.

### Declared transformation

The recipe decodes the pinned Terrarium RGB values under Mapzen's documented
elevation formula, builds an 8-by-11 tile mosaic, and creates restrained
grayscale relief with the following fixed ImageMagick settings: DEM levels
49--52 percent, shade azimuth 315 degrees, shade elevation 38 degrees,
auto-level, and a 35-percent white blend.

One horizontal source seam in the derived hillshade is corrected before panel
projection. Rows 1998--2008 are replaced by a linear image-space interpolation
between uncontaminated control rows 1997 and 2009. The receipt names the method
and all four row numbers. This limited repair suppresses a tile-source artifact;
it does not invent a mountain, watercourse, settlement, route, or station.

Natural Earth supplies land, coastline, lake, and river geometry. The recipe
does not load political boundaries. It expressly excludes the named modern
`Suez Canal` and `Ismailiya Canal` features from the river layer so that modern
engineered channels do not masquerade as part of the ancient geographic frame.
No label, marker, route, legend, or theological correspondence is drawn into
the base.

### Deterministic reproduction and artifact boundary

The authoritative recipe is
`artwork/build-ark-journey-cartographic-base.mjs`. It refuses an unpinned
toolchain and records the exact versions used:

- Node.js `v26.7.0`;
- ImageMagick `7.1.2-29 Q16-HDRI`; and
- `rsvg-convert` `2.62.3`, with Cairo 1.18.4, Pango 1.58.2, HarfBuzz 14.3.1,
  and Fontconfig 2.18.3.

The recipe verifies all Natural Earth inputs and every Terrarium tile, produces
the receipt, constructs an SVG, rasterizes it through the pinned toolchain,
strips nondeterministic PNG chunks, converts to opaque 8-bit grayscale, and
fails unless the 3800 by 2436 PNG matches the pinned output hash. Reproduction
is byte-deterministic given the pinned tools and exact inputs; this does not
promise that a remote host will retain every versioned object forever.

The tracked JSON receipt contains the output and recipe hashes along with the
full source and transformation record. The released PNG intentionally embeds
no receipt: rasterization and final stripping produce clean image bytes, so the
binding is the tracked receipt plus the hashes recorded below. The generated
SVG embeds the receipt as metadata for diagnostic inspection, but the release
workflow directs that transient reproducible intermediate under ignored
`build/` and does not retain it as an authority or publication asset.

Final source identities, rechecked after the recipe and label overlay
stabilized:

| Component | SHA-256 |
| --- | --- |
| Active PNG `ark-journey-cartographic-graphite-v3.png` | `ceb958487d6e0173f8bb74327a46fc88aface5206dd223c1473bc6194a05a2b2` |
| Reproduction recipe `build-ark-journey-cartographic-base.mjs` | `21d0f766afa39e37119653af3d3c0a1dd9900c9117858ed2e34506bd9ab656b3` |
| Tracked receipt `cartographic-base-v3-receipt.json` | `a70a89dd95fc9e893c39a4183b4c9d88949480e0d10208a3487746b3037746a8` |
| Semantic overlay `ark-journey-vector-map.tex` | `d321d4df113820bcada089f8991d4671198439f58825b758bbc137de392cd5f5` |
| Text equivalent `55-map-text-equivalent.tex` | `9cfe9240b51c19d2159f44033a64de938a9626048dafa6580ed8501b2b779910` |

On 2026-08-16 an empty-build reproduction produced the same active PNG byte
for byte, and the source-first cartographic checker reconciled the recipe,
receipt, and output without findings. Original-resolution inspection found the
former terrain seam absent. Those base-level checks do not substitute for the
composed-PDF review below.

At its maximum 31.2 by 20 cm composite placement, the 3800 by 2436 raster
supplies approximately 309 pixels per inch in both dimensions. Its approximately
9.26-megapixel dimensions and 1,430,038-byte file size are justified by that
full-width atlas use; the above-two-megapixel and above-one-MiB review triggers
are therefore recorded rather than ignored. The source-controlled PNG is
grayscale and remains subject to the repository's normal full-size artwork
review.

### Rights and attribution

Natural Earth's official Terms of Use place its raster and vector map data in
the public domain and permit modification. This statement applies to the four
Natural Earth data layers, not to the Terms page's own HTML. Natural Earth also
disclaims survey accuracy; this publication makes no stronger claim for the
derived crop.

The relief is derived from Mapzen Terrain Tiles and must not be described under
one blanket Mapzen data license. Mapzen's exact attribution document says that
the terrain product combines upstream sources and leaves the user responsible
for their respective conditions. The receipt therefore preserves each tile's
server-supplied imagery lineage, which in this crop names NASA SRTM, USGS
GMTED2010, and NOAA ETOPO1 files. Mapzen's documentation is CC BY 4.0; that
documentation license is not asserted over all elevation pixels. Attribution
for the derivative identifies Mapzen Terrain Tiles, Natural Earth, and the
per-tile upstream lineages retained in the receipt.

The recipe, semantic overlay, editorial selection, and composition are
project-created. External datasets retain their own rights status. Source
attribution neither transfers ecclesiastical approval to the data providers
nor makes a modern cartographic base an authority for the study's theological
claims.

## Rejected and superseded map bases

Neither asset below is active, consumed by the final v3 map, or evidence for a
geographic claim. Their identities remain only so the rejected design history
cannot be mistaken for the current source-first base.

### Rejected paper-tooth base generation

- Intended canvas: wide landscape 39:25 (1.56:1).
- Maximum publication placement: 15.6 by 10 cm.
- Tool/interface: Codex's built-in OpenAI image-generation interface. The
  underlying generator model/version was not exposed and is not inferred.
- Generator model/version: unexposed unless the interface returns a more exact
  identity; never infer it.
- First generation reference inputs: none. The semantic TeX map was never
  supplied to generation, so generated pixels could not acquire geographic
  authority. Corrective edits referenced only the immediately preceding
  generated texture, never the semantic map.

Exact prompt:

> Create a wide landscape monochrome graphite terrain wash for a
> source-controlled scholarly biblical cartographic plate. Transparent
> background if supported, otherwise uniform pure white. Use only very light,
> sparse hand-drawn graphite hatching, broken contour-like strokes, and soft
> relief wash, with generous quiet areas for later labels. This is a
> NONSEMANTIC texture layer: do not draw or imply any real coastline, sea,
> river, road, border, city, settlement, building, landmark, mountain peak,
> route, station, dot, pin, halo, icon, Ark, human figure, compass, scale bar,
> legend, panel frame, label, letter, number, arrow, watermark, signature,
> pseudo-text, or recognizable map outline. Pure grayscale, low contrast, no
> color cast, no hard rectangular edge, no corner ornament, no paper shadow.
> The exact geography, stations, routes, symbols, labels, legend, and
> accessibility content will be added independently as editable vector/TeX
> overlays.

That first output (1566 by 1004 sRGB, 2,192,124 bytes, SHA-256
`b6537fb2e758c721bb1f38ca5380246bff61a395937b44f3eebbe40646b63e31`)
was rejected because broad relief marks could be read as mountains or terrain.
A first corrective edit (1566 by 1004 sRGB, 2,157,269 bytes, SHA-256
`4016edfe76b7d210dc9b0c59e95c8e4180e5110d8c6827d2a9b8e5b8b25548ee`)
was also rejected after independent full-size review found residual ridge-like
forms. The exact intermediate corrective wording was not retained and is not
reconstructed.

The final corrective edit used this exact prompt:

> Edit this texture into an indisputably non-topographic, flat close-up of
> nearly white natural sketch paper. Preserve the wide landscape canvas. Show
> only extremely subtle, evenly distributed microscopic paper fibers and
> random graphite dust speckles at very low contrast. Remove every broad
> smudge, diagonal sweep, ridge, peak, basin, horizon, contour, cluster,
> gradient, vignette, directional stroke, recognizable form, map-like feature,
> geographic suggestion, lettering, symbol, or object. The result must read
> immediately as uniform blank paper tooth, not terrain or a drawing. Pure
> grayscale, matte, quiet, suitable beneath black vector linework and highly
> legible text.

### Rejected paper-tooth identity and former review

The final received output was generated on 2026-08-16 UTC through the interface
identified above. It is 1566 by 1004 pixels, opaque sRGB, 1,865,994 bytes,
SHA-256
`13a53894dd83c8b06f130acca8dfe9c913e27f94f08679acfa2a5f3b6282133b`.
It was an edit of the preceding generated texture; no semantic map, external
artwork, or third-party reference image was supplied.

The formerly admitted file is
`artwork/ark-journey-pencil-base.png`: 1900 by 1218 pixels, opaque 8-bit
grayscale, 823,279 bytes, SHA-256
`21305bdfb549960d771d53e84b01e8f5419d7de4b9c6ed52cd62052860a7b7d2`.
Normalization performed only a proportional resize from 1566 by 1004 to 1900
by 1218 and conversion from opaque sRGB to opaque 8-bit grayscale; there was
no crop, semantic edit, transparency synthesis, or sharpening. At the maximum
15.6 by 10 cm placement the former file supplied approximately 309 pixels per
inch. The slightly-above-two-megapixel size is justified by that print
placement and was compared at full resolution rather than accepted by file
size alone.

Full-size inspection found only flat, uniform paper tooth and microscopic dust
speckle: no terrain, ridge, basin, gradient, recognizable geography, symbol,
lettering, or object. The composite PDF used the raster at opacity 0.18; the
semantic vector remained complete and intelligible when the optional file was
absent. The deterministic sources at that review point were:

- `artwork/ark-journey-vector-map.tex`, SHA-256
  `e1edb99ba30be4f06e356a6881e7ba0594f133ab3684e6200919fd9009793f64`;
- `sections/55-map-text-equivalent.tex`, SHA-256
  `890762aa5319bf73e2f1f8757b9546e7b4b5891ca41ce4e331ea63c64e7a4b39`.

That superseded consumer was a 42-page PDF. Its reviewed build and installed
PDF were byte-identical at SHA-256
`a520adb39130bb3b65a3bd7d92926fbc77126650fdf593d0680fc10bee125843`;
its generated and installed web editions were byte-identical at SHA-256
`3a5e96c2405e1d311acf65ef931a45ebee502e459817f5a744833858ce62d1bc`.

That paper-tooth raster was semantically harmless, but its composite used the
former TikZ rendering's deliberately irregular, wavy route and boundary
strokes. The reader rejected the result as a rough DOT/Graphviz-like diagram,
not the finely detailed pencil map promised by the publication. This was a
visual and pedagogical rejection, not a change to the route or source matrix.
The former raster and vector hashes above remain an audit record rather than
an endorsement of the superseded presentation.

### Rejected AI graphite v2 generation

- Intended canvas: wide landscape, approximately 1.56:1.
- Maximum publication placement: 15.6 by 10 cm.
- Tool/interface: Codex's built-in OpenAI image-generation interface. The
  underlying generator model/version was not exposed and is not inferred.
- Reference input: the final corrective edit used only the immediately
  preceding project-generated north-up physical map as its edit target. No
  third-party map, photograph, or artwork was supplied.
- Initial generation: the exact first-pass prompt and intermediate file
  identity were not retained. They are not reconstructed.
- Design boundary: detailed physical geography only; all claims, labels,
  routes, stations, and evidence classes remain independently authored in
  TikZ and in the text equivalent.

The final corrective edit used this exact prompt:

> Use case: precise-object-edit
> Input images: Image 1 is the edit target, a north-up monochrome graphite
> physical map.
> Primary request: Correct only the geography and framing while preserving the
> same exceptionally refined, crisp, museum-atlas hard-graphite style. Zoom
> out enough that the full Sinai Peninsula is visible with generous white
> margin around its southern tip at Ras Muhammad and around both gulfs. Make
> the eastern Mediterranean coast, Carmel projection, Sea of Galilee, narrow
> Jordan Valley, long Dead Sea, Arabah, Gulf of Aqaba, Gulf of Suez, Negev, and
> Sinai read in their plausible relative positions and proportions. The Sea
> of Galilee must be a small pear-shaped lake well north of the long Dead Sea,
> connected by a narrow Jordan corridor; the Dead Sea must be a single long
> north-south lake; the Arabah continues south to the narrow Gulf of Aqaba.
> Keep the coast and water shapes clean, natural, and geographically
> recognizable. Remove invented islets and stray shoreline artifacts.
> Preserve generous pale quiet areas over plains and beside geographic
> features for later live TeX labels and routes.
> Constraints: change only framing and geographic plausibility. Preserve the
> white natural paper, pure neutral grayscale, precise thin contours,
> controlled line weights, very fine cross-hatching and stippling, delicate
> low-contrast relief, and strict north-up top-down landscape presentation.
> PHYSICAL GEOGRAPHY ONLY. Absolutely no labels, letters, numbers, words,
> pseudo-text, routes, arrows, dots, pins, station markers, boxes, legends,
> compass, scale, coordinate grid, icons, buildings, people, Ark, ships,
> roads, political borders, signature, watermark, folds, torn edges, color,
> sepia, dark background, panel divisions, or ornamental frame.
> Avoid: rough or wavy strokes, trembling contour lines,
> DOT/Graphviz/network-diagram appearance, schematic blobs, fantasy geography,
> heavy mountains, charcoal smears, 3D perspective, satellite look, text-like
> strokes.

### Rejected AI graphite v2 identity and normalization

The received corrective output was generated on 2026-08-16 UTC through the
interface identified above. It is 1565 by 1005 pixels, opaque sRGB, SHA-256
`18000c3ca71439b216cfe4ebd1f5e4c605639ae672678aa96fb7eaf808182250`.

The normalized but rejected candidate is
`artwork/ark-journey-graphite-v2.png`: 1900 by 1218 pixels, opaque 8-bit
grayscale, SHA-256
`4f9c4d0a719398fd3b1972bbc42b16c901a769a56783857d20fe2621c3a8b22f`.
Normalization performed a proportional resize and conversion from opaque sRGB
to opaque 8-bit grayscale for the declared 15.6 by 10 cm maximum placement;
it did not add a label, route, station, evidentiary symbol, or other semantic
claim. At that placement it supplies approximately 309 pixels per inch in
both dimensions. The above-threshold file size is justified by that print
placement and requires full-resolution inspection under the repository's
normal artwork review rule.

The raster depicts plausible broad physical geography for orientation, but it
does not claim survey accuracy. Its coastlines, water forms, and relief remain
illustration. Exact station status, route status, and source conclusions are
those in the registers above and in the deterministic consumer layers.

This v2 candidate is not active. It was rejected because a generative image,
however detailed, did not provide the exact source inputs, projection,
transformation receipt, or deterministic reproduction chain required for the
final cartographic base. No v2 pixel controls the v3 panel geometry or the live
route overlay.

### Rights record for rejected generated assets

The deterministic map geometry, labels, editorial selection, and composition
are project-created. The graphite physical-geography layer is commissioned
AI-generated material and may be distributed under repository terms only to
the extent applicable rights exist. No third-party map image, screenshot,
artwork, or named-artist style reference is incorporated. Scripture wording,
official pages, archaeological records, coordinate sources, fonts, and other
external material retain their own rights and are cited rather than reproduced
as assets.

The official [OpenAI Services
Agreement](https://openai.com/policies/services-agreement/), effective 1
January 2026, was checked on 16 August 2026. Section 4.1 states the allocation
between Customer and OpenAI: to the extent permitted by applicable law, the
Customer owns Output, and OpenAI assigns to the Customer any OpenAI right,
title, and interest in that Output. Section 4.4 states that Output may not be
unique and that other users may receive similar content. This is a contractual
allocation as between the parties, qualified by applicable law; it is not a
determination that the output is copyrightable, original in the legal sense,
unique, or free of third-party rights. Image-generation output may be
non-unique, and this record does not claim that generation created copyright
in the illustration.

## Final consumer review

The v3 PNG is not admitted merely because the recipe reproduces it. Reject the
consumer if a recorded input, tool version, output hash, recipe hash, or receipt
hash fails to reconcile; if full-size inspection finds a source seam, modern
canal line, political boundary, clipping, halo, color cast, or contrast that
obscures the overlay; or if any route or theological meaning has leaked into
the raster. File-size and resolution thresholds in `guidance/repository.md`
remain review triggers rather than automatic rejection.

Final consumer review must confirm:

1. every station, number, line, status, caption, and legend item comes from the
   deterministic layer and reconciles to this register;
2. the map has the same meaning with the PNG absent;
3. a clean recipe run reproduces the active PNG byte for byte, and its tracked
   receipt reconciles every input, transformation, panel, output, and recipe
   identity recorded here;
4. the physical geography reads as generalized orientation, does not imply
   survey accuracy, and does not displace any source-status qualification;
5. neither panel shows the repaired terrain seam, a named modern canal,
   political borders, generated lettering, or rasterized semantic content;
6. all status classes remain distinct in monochrome, a grayscale photocopy,
   and low-resolution display;
7. every label is legible at actual size, no route merges accidentally, and no
   leader has an ambiguous endpoint;
8. text extraction returns all labels, caption language, and the full textual
   equivalent without replacement characters;
9. the PDF has no fatal, reference, overflow, font, metadata, or structural
   defect, every rendered page is visually inspected, and the installed PDF is
   byte-identical to the reviewed build; and
10. no post-Temple route, precise Ein Karem claim, direct Shiloh-to-Kiriath-
   jearim shortcut, Aphek/Gaza stop, version-unlabeled Ashkelon claim, or
   Perez-uzzah/Obed-edom pin has entered the composed plate.

Composed-consumer review: **accepted**. The final 46-page GPT PDF, SHA-256
`0d995ac1d447f53cc55496fa8907c16a7940639b986fee02579b16e87d7164da`, was
reviewed through
`build/pdf-review/gpt-ark-postff-2026-08-16/review-run.json`; every rendered page and
both map plates were inspected. The review reconciled the stations, routes,
line classes, labels, legends, caption, text equivalent, source distinctions,
and prohibited-map claims above. It also confirmed legibility and status
distinction in the rendered monochrome plates, clean text extraction, and no
fatal, reference, overflow, font, metadata, or structural defect. The
source-first cartographic reproduction and receipt checks remained clean.

The generated and installed web edition, SHA-256
`8083f51e35ce1d72fdd306d23c378361e70f778ee27f1a7acaeb915c1e27a2d4`,
is byte-identical and passed map and textual-equivalence review against the
same registers. The installed GPT PDF is likewise byte-identical to the
reviewed 46-page build at SHA-256
`0d995ac1d447f53cc55496fa8907c16a7940639b986fee02579b16e87d7164da`.
The prior 42-page PDF and web hashes above remain only the
superseded-presentation record and do not establish the v3 review.

This acceptance records the composed and installed PDF and web consumers.
Deployment has not yet been claimed; it remains a separate release gate.
