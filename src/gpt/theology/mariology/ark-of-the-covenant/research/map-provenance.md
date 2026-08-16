# Map provenance: the Ark's journey and the New-Ark overlay

Checked through: 2026-08-16.

## Identity and purpose

- Stable map ID: `ARK-MAP-001`.
- Owner: `src/gpt/theology/mariology/ark-of-the-covenant/`.
- Consumer: `sections/55-map.tex`.
- Text equivalent: `sections/55-map-text-equivalent.tex`.
- Deterministic semantic layer:
  `artwork/ark-journey-vector-map.tex`.
- Optional nonsemantic texture:
  `artwork/ark-journey-pencil-base.png`.
- Purpose: orient the reader to Scripture's narrated Ark stations and to
  Mary's New-Ark journey without turning literary sequence, typology,
  traditional identification, or archaeological site location into a
  recovered road or event coordinate.
- Cartographic mode: north-up schematic locator plus central enlargement.
  It is deliberately not a navigation chart, a scale map, or an
  archaeological route reconstruction.

## Layer boundary

The TeX/TikZ layer owns every meaningful item: coastline and water orientation,
panel boundary, station position, station number, route, line status, label,
uncertainty area, traditional-site symbol, legend, caption, and typological
relationship.  The PNG may contribute only light graphite texture.  Removing
the PNG must leave the complete meaning, sequence, and distinction of the map
intact.

The generated texture must contain no actual or implied coastline, sea, river,
road, border, city, settlement, building, landmark, mountain peak, route,
station, dot, pin, halo, icon, Ark, person, compass, scale, legend, frame,
label, letter, number, arrow, watermark, signature, pseudo-text, or recognizable
map outline.  A generated pixel never determines geography or evidence status.

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

## Texture-generation history

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

That first output (`exec-c5aa0096-8795-4b74-8b6c-e2381ec257fa.png`,
1566 by 1004 sRGB, 2,192,124 bytes, SHA-256
`b6537fb2e758c721bb1f38ca5380246bff61a395937b44f3eebbe40646b63e31`)
was rejected because broad relief marks could be read as mountains or terrain.
A first corrective edit (`exec-d28eb21b-7d88-4e85-9b99-c26da58fc36d.png`,
1566 by 1004 sRGB, 2,157,269 bytes, SHA-256
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

## Raster identity and admission

The final received output was generated on 2026-08-16 UTC through the interface
identified above. It is 1566 by 1004 pixels, opaque sRGB, 1,865,994 bytes,
SHA-256
`13a53894dd83c8b06f130acca8dfe9c913e27f94f08679acfa2a5f3b6282133b`.
It was an edit of the preceding generated texture; no semantic map, external
artwork, or third-party reference image was supplied.

The admitted active file is
`artwork/ark-journey-pencil-base.png`: 1900 by 1218 pixels, opaque 8-bit
grayscale, 823,279 bytes, SHA-256
`21305bdfb549960d771d53e84b01e8f5419d7de4b9c6ed52cd62052860a7b7d2`.
Normalization performed only a proportional resize from 1566 by 1004 to 1900
by 1218 and conversion from opaque sRGB to opaque 8-bit grayscale; there was
no crop, semantic edit, transparency synthesis, or sharpening. At the maximum
15.6 by 10 cm placement the active file supplies approximately 309 pixels per
inch. The slightly-above-two-megapixel size is justified by that print
placement and was compared at full resolution rather than accepted by file
size alone.

Full-size inspection found only flat, uniform paper tooth and microscopic dust
speckle: no terrain, ridge, basin, gradient, recognizable geography, symbol,
lettering, or object. The composite PDF uses the raster at opacity 0.18; the
semantic vector remains complete and intelligible when the optional file is
absent. The final deterministic sources at this review point are:

- `artwork/ark-journey-vector-map.tex`, SHA-256
  `e1edb99ba30be4f06e356a6881e7ba0594f133ab3684e6200919fd9009793f64`;
- `sections/55-map-text-equivalent.tex`, SHA-256
  `890762aa5319bf73e2f1f8757b9546e7b4b5891ca41ce4e331ea63c64e7a4b39`.

## Rights and attribution

The deterministic map geometry, labels, editorial selection, and composition
are project-created.  The texture is commissioned AI-generated material and
may be distributed under repository terms only to the extent applicable
rights exist.  No third-party map image, screenshot, artwork, or named-artist
style reference is incorporated.  Scripture wording, official pages,
archaeological records, coordinate sources, fonts, and other external material
retain their own rights and are cited rather than reproduced as assets.

The official [OpenAI Services
Agreement](https://openai.com/policies/services-agreement/), effective 1
January 2026, was checked on 16 August 2026. Section 4.1 states the allocation
between Customer and OpenAI: to the extent permitted by applicable law, the
Customer owns Output, and OpenAI assigns to the Customer any OpenAI right,
title, and interest in that Output. Section 4.4 states that Output may not be
unique and that other users may receive similar content. This is a contractual
allocation as between the parties, qualified by applicable law; it is not a
determination that the texture is copyrightable, original in the legal sense,
unique, or free of third-party rights. This record does not claim that image
generation created copyright in the texture.

## Admission and consumer review

The PNG is rejected if full-size inspection finds any prohibited semantic
content, invented recognizable geography, lettering or pseudo-lettering,
watermark, signature, color cast, hard rectangular field, clipping, halo, or
contrast strong enough to obscure the vector layer.  It must be normalized as
an 8-bit grayscale or grayscale-alpha PNG, ordinarily at 300--450 effective
dpi at maximum placement.  A file above 1 MiB, above two megapixels without
placement need, above 450 effective dpi, or stored as RGB triggers the
repository investigation and recorded comparison required by
`guidance/repository.md`; those thresholds are review triggers rather than
automatic rejection.

Final consumer review must confirm:

1. every station, number, line, status, caption, and legend item comes from the
   deterministic layer and reconciles to this register;
2. the map has the same meaning with the PNG absent;
3. all status classes remain distinct in monochrome, a grayscale photocopy,
   and low-resolution display;
4. every label is legible at actual size, no route merges accidentally, and no
   leader has an ambiguous endpoint;
5. text extraction returns all labels, caption language, and the full textual
   equivalent without replacement characters;
6. the PDF has no fatal, reference, overflow, font, metadata, or structural
   defect, every rendered page is visually inspected, and the installed PDF is
   byte-identical to the reviewed build; and
7. no post-Temple route, precise Ein Karem claim, direct Shiloh-to-Kiriath-
   jearim shortcut, Aphek/Gaza stop, version-unlabeled Ashkelon claim, or
   Perez-uzzah/Obed-edom pin has entered the composed plate.

Current state: accepted for the alpha publication. All seven consumer-review
criteria above were checked against the final 42-page render. In particular,
the map was inspected at full size after its line key was moved beneath the
panel, leaving every station and terminus unobscured; all 42 page rasters and
bounded contact sheets were inspected; text extraction contained no
replacement character; and the log had no fatal, undefined-reference, or
overflow warning. The reviewed build and installed PDF are byte-identical at
SHA-256
`a520adb39130bb3b65a3bd7d92926fbc77126650fdf593d0680fc10bee125843`.
The generated and installed web editions are byte-identical at SHA-256
`3a5e96c2405e1d311acf65ef931a45ebee502e459817f5a744833858ce62d1bc`
and retain the common introduction, line key, interpretive caption,
correspondence box, and complete text equivalent while excluding only TikZ.
