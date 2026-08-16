# Ark and sanctuary illustration audit

## Identity and purpose

The five print illustrations governed by this audit are:

| Asset ID | Tracked asset | Role |
| --- | --- | --- |
| `ARK-PLATE-001` | `artwork/ark-form-graphite-v2.png` | Ark form and commanded-feature study |
| `ARK-SETTING-001` | `artwork/tabernacle-graphite-v2.png` | Wilderness Tabernacle teaching reconstruction |
| `ARK-SETTING-002` | `artwork/shiloh-graphite-v2.png` | Deliberately unresolved Shiloh setting |
| `ARK-SETTING-003` | `artwork/david-tent-graphite-v2.png` | Davidic tent teaching illustration |
| `ARK-SETTING-004` | `artwork/solomon-temple-graphite-v2.png` | Solomon's Temple teaching reconstruction |

Their print consumer is `sections/57-ark-and-sanctuaries.tex`. The complete web
and accessibility equivalent is
`sections/57-ark-and-sanctuaries-text-equivalent.tex`.

Purpose: answer the reader's concrete questions about the Ark's commanded
features and its attested sanctuary settings while preventing illustrative
convention from becoming archaeological or exegetical evidence. The generated
pixels are illustrations, not recovered portraits, excavation records,
architectural evidence, or independent support for any claim in the study.
Scripture and the cited witnesses control the claims; the images do not.

These plates supersede the rejected random-step TikZ studies. On 2026-08-16 the
maintainer rejected their rough, wavy, DOT/Graphviz-like appearance and required
very finely detailed pencil drawings. The replacement brief therefore required
precise geometry, controlled line weight, fine cross-hatching or stippling,
coherent perspective, clean white paper, and detail that remains intentional at
full printed size. Rough contours, random-step lines, pseudo-labels, and diagram
generator aesthetics are explicit rejection conditions.

All five semantic images were generated through the built-in image-generation
interface without external reference artwork. Three selected assets are
refinements of an immediately preceding generated image; the two prompt stages
and both generated identities are recorded below. No machine-local generation
path is retained in this tracked record.

## Final asset register

| Asset ID | Final identity | Generated-source identity | Production disposition |
| --- | --- | --- | --- |
| `ARK-PLATE-001` | 1536×1024, stripped 8-bit grayscale PNG, 707,566 bytes; SHA-256 `01d6a3762691df0f7591f70ecc3d1dcaaef587c54a44899b52642f78dff48fa8` | Base: `abdfae923a628920207bcf01e21e95784a22656c7ba76417e85e1f6c72937e50`; first generated refinement: `0a058222c41d03be3c76c1c78d9c2ba30c33223b04db6a30ca96f4a4c95c2d55`; first normalized plate, rejected for naturalistic bird forms and separate plinths: `7f961d33b5887b247616db7ff3949c2d0369090c613744326ccdd47bba7382ee`; first guardian correction: RGB `53df742da150d40faaa177488e8a1257b441969503cd2a4607965a4f284da9cd`, then grayscale `73e43a88cf72d32b0d83c9fcc5551035e0ad7f50039b3bcac5a00db6f00d3956`, rejected because the guardians still read as avian; selected second guardian correction: 1536×1024, 8-bit RGB, 2,403,209 bytes; SHA-256 `390a873c7449cc40863e3356df5bc1ab12d63d72b580bdfa84bcbfbaabfb25c4`. | Latest correction converted to grayscale, reduced to 8-bit, and stripped without resizing. Generated-to-final MAE 70.3288/65535; PSNR 52.2879 dB. Final guardians are abstract, non-avian, and integral with the cover. |
| `ARK-SETTING-001` | 1536×1024, stripped 8-bit grayscale PNG, 897,156 bytes; SHA-256 `79761dbe70224f7fd0faa4639b26962fc7372868f3105ef0aa62943b1f6f472b` | 1536×1024, 8-bit RGB, 2,900,702 bytes; SHA-256 `1714512c1e5fecf943430cee186b73f0923de45275210ced990bb2bc5b94ce99`. | Normalized with `tools/artwork-library normalize`; no resizing. Source-to-final RMSE 227.143/65535. No refinement pass was required after full-resolution inspection. |
| `ARK-SETTING-002` | 1536×1024, 8-bit grayscale PNG, 347,654 bytes; SHA-256 `8e87f6536c92cd96ca10c5d59e049ea68846b357caf41662b62e2887a1a65515` | First selected RGB plate, rejected because its postholes, grids, footing traces, and ground shadow could read as recovered site evidence: `973e39341f4ed52387490e573752e62661f6bc3400aac01d4af68db06c465ef5`. Selected correction: 1536×1024, 8-bit RGB, 1,190,031 bytes; SHA-256 `6569a353605c7f11d52ee8cb77d6a0790a449977bac9984da1c8b4d82ec1fcdd`. | Latest correction converted to 8-bit grayscale and stripped of ancillary PNG text/time/background chunks without crop, resize, compositing, geometry change, or retouching. Final plate has no excavation, site-plan, ground, or location cues. |
| `ARK-SETTING-003` | 1536×1024, stripped 8-bit grayscale PNG, 521,460 bytes; SHA-256 `7e6f8e9de90135c9fade4cc0add29289ead22be3569ca8ead2fa48eda16e1727` | Base: `bcffc2edc85a965f0f0be16c3dc9539a14a865805aae92ad087698d052ff90c0`; first generated refinement: `49487d85feb0358117cf0296c7be8a185cd0ddc32824817a1113caa656379ca5`; first normalized plate, rejected because the landscape implied an identifiable setting and the tent read too definitively: `6febe23241e428a2544e4c758e36d9eaf1cf15543bd144a9e4eb9e119f891ecd`; selected correction: 1536×1024, 8-bit non-grayscale PNG; SHA-256 `076ab7ed80876c4fde70af3a303e13a586a51201da5bffb207611a97bab09bbe`. | Latest correction normalized with `tools/artwork-library normalize`; metadata stripped and grayscale conversion applied without resizing. Final setting is white paper with only a faint contact shadow and a generic shelter whose edges dissolve. |
| `ARK-SETTING-004` | 1536×1024, stripped 8-bit grayscale PNG, 883,207 bytes; SHA-256 `e764c4e655dae82bec6d78b069bc1692514f0c03aa6bdd1f9e3b5b64a12d1951` | Base: `7a04fecce957b2fc1c1b702f8836e09703ba0b25be75b0209aa143bd56e266a3`; first generated refinement: `69f779d934a8ca9dd9c46e10ba157c0e0e654f4f35259fb27b1bdd1538404944`; first normalized plate, rejected because the inner-sanctuary guardians did not express the commanded wall-to-wall four-wing span and the porch carried speculative floral styling: `f0c7aaf0e56f861f2cefe85c05ee04885df35d4381aa5ae0cba9362be249b58a`; first fidelity correction: RGB `be3d687f4188e0129536becb9ce5a02538d1beaf195ee6c684143476825b6b04`, then grayscale `b32289ee356fc2693af4e8380213ea864635f77424dfff429252ae098d148a41`, rejected because the inner wingtips retained a central gap; selected zero-gap correction: 1536×1024, 8-bit RGB, 2,803,896 bytes; SHA-256 `845bda327ed81a25699cbe4c5acc193753fc996855879c7359707b416558db0a`. | Latest correction converted to grayscale, reduced to 8-bit, and stripped without resizing. Original-resolution inspection confirms plain pillars and a continuous left-wall-to-center-to-right-wall four-wing chain with direct central wingtip contact and no visible gap. |

The grayscale conversions were production normalization, not semantic edits.
All five final tracked assets are now verified 1536×1024, 8-bit grayscale PNGs.
Semantic corrections occurred only through the exact image-edit prompts below;
the later deterministic normalization did not alter composition or geometry.
The final dimensions, colorspaces, byte counts, and SHA-256 identities were
rechecked directly against the tracked files on 2026-08-16. The consumer-PDF
review and installation results are recorded in Production acceptance below.

### Distribution and output-rights boundary

The five selected plates were commissioned through OpenAI's image-generation
service without a third-party reference image or a named-artist style request.
The [OpenAI Services Agreement](https://openai.com/policies/services-agreement/),
effective 1 January 2026, was checked on 16 August 2026. Section 4.1 allocates
Output to the Customer, to the extent permitted by applicable law, and assigns
OpenAI's right, title, and interest in that Output to the Customer. Section 4.4
also states that Output may not be unique. This contractual allocation is the
recorded basis for distributing the selected pixels under repository terms; it
is not a legal conclusion that the images are copyrightable, original in the
legal sense, unique, or free of every possible third-party right. Scripture,
archaeological facts, cited works, and the live factual captions remain distinct
from the generated illustrations and retain their own status.

## Exact generation prompts

### `ARK-PLATE-001`: Ark form

Base generation prompt (verbatim):

```text
Use case: historical-scene
Asset type: full-page monochrome publication illustration for a source-controlled theological and archaeological study
Primary request: Create a museum-quality archaeological reconstruction drawing of the Ark of the Covenant as a finely drafted monochrome graphite plate on perfectly clean white paper. This is a restrained study of commanded construction features, not a claim to recover its historical appearance.
Scene/backdrop: no scene, floor, landscape, people, architecture, props, or atmospheric background; isolated object with generous clean white margins.
Subject: one closed rectangular wooden chest in a clear elevated three-quarter view, with relative proportions exactly 2.5 length : 1.5 width : 1.5 height. The wood core is completely overlaid with hammered gold on the exterior and understood to be overlaid within; keep the chest closed and expose no contents. Show the lid as a clearly separate, thin, pure-gold mercy-seat cover seated immediately above the chest.
Required construction: exactly four substantial gold carrying rings attached low at the four corners, two on each long side; all four rings must be readable in perspective, with far-side rings naturally partly occluded if necessary. Exactly two long straight wooden carrying poles overlaid with gold, parallel to the chest's long axis, passing continuously and mechanically through the paired rings on each long side and remaining in the rings. Both poles extend well beyond both ends of the chest. No pole may float, bend, cross, terminate inside the chest, or miss its rings.
Cherubim: exactly two restrained hammered-gold cherubim integrated at the two opposite ends of the separate cover, in a sober ancient sacred-object reconstruction vocabulary. Their bodies remain compact at the cover ends; their faces angle downward and inward toward the cover; their raised wings stretch inward and overshadow the cover, approaching one another above its center. Avoid later European angel iconography: no Renaissance angels, no putti, no robes, no halos, no sentimental human faces, no large human figures.
Style/medium: exceptionally fine graphite archaeological illustration, crisp controlled construction lines, exact rectilinear perspective, meticulous fine cross-hatching, delicate stippling, subtle graphite tonal modeling, precise joinery and convincing material texture. Fine museum-catalog plate or nineteenth-century archaeological draftsmanship translated into clean contemporary graphite. Elegant and restrained, highly resolved at full resolution, not ornate.
Composition/framing: horizontal plate, object fills most of the canvas without touching edges; clear three-quarter view that reveals the top, one long side, one end, all required hardware, and the continuity of both poles through their rings.
Lighting/mood: neutral archival studio illumination rendered only through restrained graphite values; white paper stays pure and untextured outside the object.
Color palette: strictly monochrome neutral graphite grayscale only; no color, gold color, sepia, cream, beige, or warm paper.
Materials/textures: use subtle surface distinctions to make the wood-core chest, hammered-gold overlay, pure-gold cover, cast/hammered rings, and gold-overlaid wooden poles intelligible without labels; no exposed interior and no cutaway.
Text: none.
Constraints: exact count of one chest, one distinct cover, four rings, two poles, two cherubim; geometrically plausible construction; controlled straight edges and smooth deliberate curves; no invented relief panels or decorative scenes; no contents exposed.
Avoid: all words, labels, letters, numbers, captions, arrows, dimension marks, callouts, borders, pseudo-text, watermark, signature, crop marks; rough sketchiness, wavy or trembling contours, scribble, charcoal, ink wash, watercolor, painterly blur, noisy paper, rough .dot-style rendering, ornamental filigree, relief panels, jewels, handles, extra rings, extra poles, extra cherubim, people, setting, open lid, visible tablets or objects.
```

Selected refinement prompt (verbatim):

```text
Use case: precise-object-edit
Asset type: full-page monochrome publication illustration for a source-controlled theological and archaeological study
Input image: Image 1 is the edit target.
Primary request: Preserve the excellent crisp, high-resolution museum-catalog graphite drafting, white background, chest geometry, separate cover, hammered-metal texture, clean three-quarter perspective, and two long straight poles. Change only the ring visibility and cherubim design described below.
Ring correction: show exactly four substantial circular gold carrying rings, one low at each of the chest's four corners, two on each long side. Arrange the perspective so all four rings are distinctly readable, including both far-side rings. Each of exactly two long straight gold-overlaid wooden poles must pass continuously and mechanically through its pair of rings along one long side; both poles remain parallel to the chest's long axis and extend beyond both ends. No ring may float away from a chest corner, no pole may miss a ring, and no extra ring or pole.
Cherubim correction: replace the kneeling humanoid angels with exactly two compact, restrained hammered-gold cherubim as sober abstract ancient sacred-object guardian forms integrated into the opposite ends of the separate pure-gold cover. Avoid a recovered-specific portrait: use stylized non-European, non-Renaissance, non-humanlike forms, no kneeling people, no robes, no halos, no sentimental human faces, no putti. Give each a small face/head surface angled downward and inward toward the cover. Their raised wings stretch inward, overshadow the cover, and approach each other above the center without touching.
Invariants: one closed chest at 2.5 length : 1.5 width : 1.5 height; one distinct thin pure-gold mercy-seat cover; exact counts of four rings, two poles, two cherubim; no exposed contents or cutaway; monochrome neutral graphite grayscale only; perfectly clean white paper; meticulous fine cross-hatching and controlled construction lines; no scene, people, text, labels, letters, numbers, arrows, border, pseudo-text, watermark, signature, relief panels, filigree, jewels, roughness, wavy contours, color, or sepia.
```

First guardian-correction prompt (verbatim; retained because its selected result
was the input to the final edit):

```text
Use case: precise-object-edit
Asset type: monochrome museum-catalog archaeological illustration
Input image: Image 1 is the edit target.
Primary request: Change only the two cherubim on the mercy-seat cover. Preserve every other pixel-level design feature as closely as possible: the finely controlled graphite draftsmanship, exact chest and separate-cover geometry, three-quarter perspective, hammered-metal textures, clean white background, exactly four corner carrying-ring assemblies, exactly two long straight gold-overlaid poles passing through those rings, and all framing and tonal balance.
Cherubim replacement: Remove both naturalistic bird/swan/eagle figures and their separate plinths completely. Replace them with exactly two compact, restrained, abstract ancient sacred guardian forms, one emerging integrally from each opposite end of the SAME pure-gold mercy-seat cover. They must be visibly hammered from and continuous with the cover itself: seamless rising transitions from the cover surface, no separate base, pedestal, plinth, plaque, platform, feet, sockets, attachment blocks, or visible join.
Form language: sober abstract sacred metalwork, schematic and deliberately non-reconstructive; neither naturalistic birds nor naturalistic humans. Use compact geometric guardian bodies, small stylized face/head planes angled downward and inward toward the cover, and simplified hammered wing planes rather than anatomically realistic feathered animals. No swan necks, eagle beaks, bird torsos, bird tails, talons, kneeling people, robes, halos, putti, sentimental faces, or Renaissance/European angel iconography.
Wing arrangement: each integral figure raises wings inward from its end; the paired wings visibly overshadow the cover and extend toward one another above the center while remaining two distinct forms. Faces look down and toward the central cover surface.
Craft and finish: match the existing image's crisp exact graphite construction lines, meticulous fine cross-hatching, subtle stippling, restrained grayscale modeling, and clean rectilinear museum-plate quality. Keep the guardian forms elegant, compact, and materially plausible as hammered gold, but not ornate.
Invariants: one closed chest, one distinct thin mercy-seat cover, exactly four carrying rings, exactly two poles, exactly two cover-integral cherubim; no exposed contents; no changes to the chest, poles, rings, viewpoint, canvas, or background.
Avoid: any separate cherub base; naturalistic bird or animal anatomy; extra figures, wings, rings, or poles; added ornament, relief panels, jewels, text, labels, letters, numbers, arrows, border, pseudo-text, watermark, signature, color, sepia, roughness, wavy contours, scene, people, architecture, or props.
```

That result was rejected because the figures remained recognizably avian. Final
guardian-correction prompt (verbatim):

```text
Use case: precise-object-edit
Asset type: monochrome museum-catalog archaeological illustration
Input image: Image 1 is the edit target.
Primary request: Edit ONLY the two cover-integral guardian forms. Preserve everything else exactly: the chest, separate mercy-seat cover, geometry, viewpoint, framing, white background, graphite line quality, hammered metal surfaces, exactly four corner carrying-ring assemblies, and exactly two continuous long poles through the rings.
Required guardian redesign: Replace every feather texture, scale-like feather row, beak, eye, neck, tail, leg, talon, bird-body curve, human anatomy, and other recognizable animal or human feature. Create exactly two restrained ABSTRACT hammered-gold sacred guardian forms emerging seamlessly and integrally from the opposite ends of the SAME mercy-seat cover.
Heads/faces: each guardian has a small, simple, stylized geometric head-and-face plane—an abstract folded or faceted mask-like volume, not a human face and not an animal head. Angle each face plane inward and downward toward the cover. No beak, muzzle, nose profile, naturalistic eye, hair, ears, halo, or expression.
Wings: each guardian has broad geometric wing planes rising inward to overshadow the cover and approach the other above the center. Wings must be smooth planar hammered-metal fans articulated only by sparse straight incised lines and large angular facets. NO feathers, feather silhouettes, layered plumage, scales, quills, bird wing anatomy, rounded feather tips, or decorative organic pattern. Keep the two wings clearly distinct.
Bodies/integration: reduce each body to a compact abstract folded-metal support volume flowing directly upward out of the cover end. The transition must be continuous hammered metal with no seam, base, plinth, pedestal, platform, socket, foot, or attachment block. The total form should resemble intentionally non-identifiable ancient sacred metalwork, not a bird, eagle, swan, animal, person, or European angel.
Style: preserve the existing extremely fine, crisp graphite archaeological drafting, precise rectilinear construction, meticulous cross-hatching, clean white paper, and restrained museum reconstruction tone. The new guardian surfaces may use subtle graphite shading and hammered texture but no organic anatomy.
Invariants: exactly one closed chest, one distinct thin cover, four carrying rings, two poles, and two cover-integral abstract guardians; faces inward/downward; wings overshadow toward center; no exposed contents.
Avoid: all recognizable birds or humans; beaks; feathers; scales; animal eyes; swan/eagle silhouettes; separate bases; extra figures, wings, rings, or poles; changes to hardware or chest; ornament, relief panels, jewels, text, labels, letters, numbers, arrows, border, pseudo-text, watermark, signature, color, sepia, roughness, wavy contours, scene, people, architecture, or props.
```

### `ARK-SETTING-001`: wilderness Tabernacle

Generation prompt (verbatim):

```text
Use case: historical-scene
Asset type: monochrome publishing illustration for a source-first theological reference PDF
Primary request: Create a very finely detailed, precise graphite architectural cutaway reconstruction of the wilderness Tabernacle, suitable for a scholarly museum catalogue. It must read as a beautifully observed hand drawing, not a schematic diagram.
Scene/backdrop: A luminous clean white paper ground, with only faint graphite contact shadows and no horizon, landscape, people, or narrative scene.
Subject: A long rectangular curtained courtyard oriented east-to-west, viewed in a slightly elevated three-quarter cutaway from the east-southeast toward the west. Make the eastern entrance unmistakably open at the near short end. Within the court, show the rectangular tent along the long axis. Cut away part of the tent roof and near wall so the east-facing Holy Place is spatially legible, then show a suspended textile veil dividing it from the smaller Most Holy Place at the western rear. Place a small, carefully rendered Ark behind that veil in the innermost western chamber; it should be visible only because of the cutaway, clearly separated from the outer chamber. Preserve a strong nested spatial hierarchy: courtyard, tent, Holy Place, veil, Most Holy Place, Ark.
Style/medium: Extremely refined monochrome graphite and carbon-pencil architectural illustration; confident straight ruled geometry softened only by authentic pencil grain; very fine cross-hatching, delicate tonal modeling, crisp structural joins, museum reconstruction drawing, high craft and dense observational detail. Fine textile weave in court hangings and tent curtains; precise posts, cords, pegs, wooden framing, rings and modest metal glints. Elegant, restrained, accurate-looking, not theatrical.
Composition/framing: Wide three-quarter axonometric view with generous white margins and the entire rectangular enclosure visible. Use coherent perspective, clean alignment, clear doorway openings, and an unambiguous sectional cut through roof and near wall. The veil must remain visibly distinct from the Ark behind it.
Lighting/mood: Soft diffuse studio light over white paper; subtle depth, no dramatic sky or scenery.
Color palette: Pure monochrome neutral graphite grayscale only; bright white paper, no sepia, beige, brown, blue, gold, or color tint.
Constraints: This is an acknowledged illustrative reconstruction, not an archaeological claim. Include no labels or textual content. Make every contour precise, stable, and clean rather than rough.
Avoid: Israelites, human figures, animals, sacrifices, fire, smoke, later Temple masonry, stone building, monumental columns, invented inscriptions, labels, letters, numbers, arrows, diagram keys, border, frame, cartouche, pseudo-text, watermark, signature, color, sepia, rough sketchiness, wavy contours, random-step lines, loose doodling, fuzzy geometry, flat floor-plan appearance, infographic style, comic style, photorealism, clutter.
```

### `ARK-SETTING-002`: Shiloh

Generation prompt (verbatim):

```text
Use case: stylized-concept
Asset type: full-page archaeological uncertainty study for a scholarly theological publication
Primary request: Create a very finely detailed monochrome graphite conceptual plate communicating one distinction: the Ark is securely attested at Shiloh, while the sanctuary’s architectural form is unrecovered.
Subject: Place a meticulously rendered Ark of the Covenant at the exact visual center as the only visually resolved object. Treat the Ark as a disciplined source-conscious conceptual study, not a recovered portrait: rectangular chest with distinct cover, four ring attachments implied where perspective permits, two long carrying poles left in place, and two restrained abstract opposed wing forms above the cover. Avoid invented decorative reliefs, inscriptions, figurative faces, botanical wood grain, or archaeological patina.
Scene/backdrop: On clean white paper, surround the Ark with deliberately incomplete archaeological ground traces: a few crisp interrupted footing marks, sparse post-hole stippling, partial soil-edge notation, and eraser-softened construction lines. Add several mutually incompatible, very pale architectural possibilities that overlap without resolving into one structure: one discontinuous fold of tent cloth, one isolated threshold or door-jamb fragment, and a lamp glow suggested only by an extremely faint pale graphite halo with no drawn lamp. Each possibility must stop abruptly, be rubbed out, or dissolve into untouched white paper before forming a wall, roof, enclosure, floor plan, elevation, or complete building. Leave generous white negative space around the page margins.
Style/medium: sophisticated museum-catalogue archaeological uncertainty plate; technically exact graphite draughtsmanship; crisp controlled 0.2 mm pencil line, fine cross-hatching, delicate stippling, precise short straight strokes, subtle erasure ghosts, immaculate white archival paper. Intentionally unresolved but fully finished and polished. No loose sketchiness, no rough or wavy outlines, no DOT/Graphviz diagram aesthetic.
Composition/framing: landscape plate, centered Ark in a measured three-quarter view; strongest value and sharpest edges only on the Ark; archaeological traces form an incomplete broken orbit around it; architectural ghosts remain peripheral, fragmented, mutually contradictory, and much lighter than the Ark; absolutely no enclosing silhouette.
Lighting/mood: quiet scholarly clarity; tonal hierarchy from dark, crisp central Ark to extremely pale, vanishing peripheral traces.
Color palette: pure grayscale only—graphite black, neutral gray, white paper; no color and no sepia.
Constraints: The image must communicate architectural uncertainty more strongly than architectural form. The Ark’s presence is certain; everything around it is hypothetical and unrecovered. This is not a factual reconstruction. Finish every chosen graphite mark with refined control even where forms deliberately fade.
Avoid: any complete building, complete tent, continuous perimeter, room, roof, façade, columns, intact walls, resolved floor plan, definite footprint, perspective interior, people, priests, animals, landscape panorama, hills, trees, sky, excavated ruin scene, labels, letters, numbers, arrows, captions, scale bars, pseudo-text, decorative border, color, sepia, smudgy charcoal, coarse hatch, rough/wavy lines, watermark, signature.
```

The selected result from that prompt was rejected because its survey grids,
postholes, footing traces, and contact shadow could be mistaken for site
evidence. Final correction prompt (verbatim):

```text
Use case: precise-object-edit
Asset type: revised full-page scholarly graphite conceptual plate
Input image: edit target; preserve its landscape canvas, central Ark design, meticulous graphite finish, restrained grayscale-on-white aesthetic, and generous negative space.
Primary edit: Remove every element that can resemble excavated evidence, an archaeological site plan, or an exact plan coordinate. Completely erase all survey grids, dotted or dashed plan lines, postholes, stake marks, footing stones, trenches, soil traces, masonry fragments, perimeter traces, map marks, hatching keys, and the Ark’s ground/contact shadow. Restore those areas to immaculate blank white paper with no residual artifacts.
Central subject: Preserve the highly resolved, finely cross-hatched three-quarter Ark as an explicitly emblematic isolated object centered on the page—not an object standing at a recovered location. Keep the distinct chest and cover, two carrying poles, restrained abstract opposed wing forms, crisp controlled fine graphite, and current tonal authority. Let it float as a museum study on white paper with no floor line, ground plane, shadow, coordinate mark, plinth, excavation context, or spatial connection to anything around it.
Surrounding uncertainty: Retain or redraw only three mutually incompatible, extremely pale, non-geographic thought-fragments, spatially detached from one another and from the Ark: (1) a single incomplete fold of possible tent cloth whose edges are partly erased and dissolve before suggesting a full tent; (2) one isolated erased threshold/jamb idea, broken into only a few nonjoining straight strokes and never forming a doorway or wall; (3) an almost invisible graphite halo suggesting possible lamp light, with no lamp, flame, fixture, room, or supporting surface. These fragments are visual hypotheses, not finds. Give them no shared horizon, scale, orientation, alignment, enclosure, or spatial relationship. Each must fade decisively into untouched white paper.
Style/medium: sophisticated finished archaeological-uncertainty study in exact technical graphite draughtsmanship; very fine 0.2 mm pencil line, controlled micro-cross-hatching and stippling only on the Ark, subtle clean erasure ghosts on the three pale thought-fragments, no smudgy charcoal and no rough or wavy line.
Composition: landscape, central emblematic Ark as the sole resolved form; the three peripheral fragments sparse, independent, much lighter, and suspended in white negative space. Architectural uncertainty must dominate; no reader should infer a building, room, site, excavation, footprint, plan coordinate, or recovered setting.
Color palette: neutral monochrome graphite black and gray on clean white paper only; no color, tint, or sepia.
Constraints: Change only the surrounding evidence language and remove the ground shadow; preserve the Ark’s refined form, proportions, fine line quality, and central visual weight. The result must look deliberately complete and publication-ready even though the peripheral hypotheses remain intentionally unresolved.
Avoid: survey grids, coordinate grids, graph paper, postholes, pits, trenches, excavated ruins, footings, foundations, masonry, floor plan, site plan, map, contour, landscape, horizon, ground plane, shadows, complete tent, complete doorway, continuous walls, roof, façade, enclosure, building, room, people, priests, animals, labels, letters, numbers, arrows, captions, pseudo-text, scale bars, legend marks, decorative border, watermark, signature, color, sepia, rough lines, wavy outlines, unfinished sketch aesthetic.
```

### `ARK-SETTING-003`: David's tent

Base generation prompt (verbatim):

```text
Use case: historical-scene
Asset type: monochrome publication illustration for a source-controlled theological study
Primary request: Create a very finely detailed museum-quality graphite pencil plate showing the Ark of the Covenant resting within the simple tent David pitched on Zion, as an explicitly interpretive scene rather than a recovered reconstruction.
Scene/backdrop: A restrained ancient textile shelter, opened in a modest cutaway so its interior can be seen. The tent should be materially plausible yet deliberately generic: simple woven cloth panels, plain cords and pegs, uncomplicated poles, no fixed architectural plan, no identifiable excavated site. The surrounding ground is minimal, quiet, and intentionally non-specific, with only faint natural terrain.
Subject: Center the Ark inside the shelter as the calm visual focus. Show a rectangular chest and distinct cover, with two long carrying poles clearly passing through ring fittings and remaining in place. Treat the Ark's ornament and cherubim, if suggested at all, with restrained interpretive abstraction rather than archaeological certainty; do not make a detailed claim about their lost appearance.
Style/medium: True monochrome graphite on clean white paper; crisp controlled draughtsmanship; extremely fine pencil linework; disciplined straight geometry; delicate textile weave; refined wood grain and metal cross-hatching; layered hatching and soft graphite tonal modeling; subtle depth; precise edges; publication-grade finish. The result should resemble a scholarly museum illustration or a master architectural-object pencil study, not a rough diagram, not a .dot rendering, and not wavy random-step line art.
Composition/framing: Landscape plate, balanced three-quarter view into the open tent. Ark centered and fully readable, poles unobstructed enough to understand their relation to the rings. Shelter occupies most of the composition with generous white-paper breathing room. No theatrical perspective or cinematic spectacle.
Lighting/mood: Diffuse natural light, low contrast, quiet dignity, contemplative restraint.
Color palette: Pure neutral grayscale only on white paper; no color, cream, tan, brown, or sepia cast.
Materials/textures: Fine woven linen/wool texture, plain rope fibers, subtle wood grain, restrained metallic sheen expressed only through graphite hatching.
Constraints: Interpretive illustration only; simple ancient textile tent; no claim of recovered architecture; no people; no city skyline; no later Temple; no palace; no masonry shrine; no furniture; no offerings; no dramatic smoke, rays, glow, supernatural light, or spectacle.
Avoid: modern camping tent, military tent, Bedouin luxury pavilion, ornate canopy, excessive drapery, monumental architecture, pseudo-archaeological certainty, labels, letters, numbers, arrows, border, caption, pseudo-text, color, sepia, rough sketchiness, scribbles, wavy contours, thick cartoon outlines, graphic-novel style, watermark, logo, or signature.
```

Selected refinement prompt (verbatim):

```text
Use case: precise-object-edit
Asset type: monochrome publication illustration for a source-controlled theological study
Input image 1: edit target
Primary request: Refine only the visual specificity of the shelter and Ark so the scene reads as a restrained interpretive illustration, not a reconstruction. Preserve the landscape composition, clean white-paper ground, extremely fine graphite craftsmanship, centered Ark, visible carrying poles in rings, delicate textile weave, cross-hatching, subtle depth, and quiet dignity.
Change the shelter: make it simpler, older, and more provisional—an unadorned pitched ancient textile cover with fewer visible structural assumptions, irregular handwoven cloth, plain cords and stakes, and a restrained open cutaway. Remove the fully built-out framed interior, regimented upright wall posts, tailored pavilion effect, and any modern camping or military-tent character. Keep the terrain minimal and non-specific.
Change the Ark: remove the pedestal/altar impression, paneled furniture styling, layered ornamental moldings, carved decorative bands, and excessive archaeological certainty. Show a simpler low rectangular chest with a distinct plain cover and two long carrying poles clearly passing through four ring fittings and remaining in place. Suggest the two cherubim only as restrained, generalized hammered forms with wings oriented inward and overshadowing the cover; do not assert a precise lost appearance.
Change the floor: remove the fitted carpet or decorative floor mat; use only bare, lightly rendered ground beneath the Ark.
Style/medium: true neutral monochrome graphite on clean white paper, museum-quality pencil plate, crisp controlled geometry, very fine linework, textile-fiber detail, refined wood/metal cross-hatching, soft tonal modeling. Do not reduce detail or make contours rough, wavy, sketchy, or diagram-like.
Constraints: no people, city skyline, later Temple, masonry shrine, palace, furniture, offerings, labels, letters, numbers, arrows, border, caption, pseudo-text, color, sepia, glow, theatrical rays, watermark, logo, or signature.
Invariants: Keep the Ark centered inside the open shelter; keep both poles legible through rings; keep the calm balanced framing and generous white space; keep the same high technical pencil finish.
```

The selected result from that prompt was rejected because its landscape could
suggest a recovered location and its complete tent silhouette carried too much
architectural certainty. Final setting-correction prompt (verbatim):

```text
Use case: precise-object-edit
Asset type: monochrome graphite publication illustration for a source-controlled theological study
Input image 1: edit target
Primary request: Remove the entire contextual landscape and make the textile shelter read clearly as a restrained interpretive sign rather than a recovered reconstruction. Preserve the finely detailed graphite craftsmanship and the Ark resting centrally beneath the shelter.
Change only the setting and the shelter's degree of definition: erase every distant hill, horizon line, desert panorama, scrub plant, tuft of grass, rock, pebble, uneven terrain texture, and site-specific environmental feature. Replace all surroundings and foreground with luminous blank white paper. Retain only the faintest soft neutral graphite contact shadow immediately beneath the Ark and shelter, with no depicted soil, floor, landscape, or location.
Simplify the shelter into a provisional, generic ancient textile cover with minimal implied support. Keep beautiful controlled fine weave and fiber detail near the center, but let selected outer cloth edges, cords, stakes, and structural intersections taper gently into incomplete graphite and dissolve into the white page. Use refined fading lines and reduced tonal certainty—not roughness, wavy contours, torn fabric, blur, or unfinished scribbling. Avoid a complete architectural enclosure, fixed interior plan, modern camping-tent engineering, military tent, pavilion, or ethnographic/Bedouin specificity.
Invariants: Preserve the Ark as the calm central focus; preserve its scale, position, rectangular chest, distinct cover, restrained inward-facing winged forms, two long carrying poles, and visible ring fittings. Preserve the landscape aspect ratio, three-quarter view, crisp controlled geometry, museum-quality graphite linework, subtle wood/metal cross-hatching, neutral grayscale, clean white paper, balanced negative space, and quiet dignity.
Constraints: no people, buildings, skyline, Temple, palace, masonry, vegetation, hills, horizon, rocks, terrain, labels, letters, numbers, arrows, border, caption, pseudo-text, color, cream, tan, sepia, theatrical light, glow, smoke, rough sketching, wavy lines, watermark, logo, or signature.
```

### `ARK-SETTING-004`: Solomon's Temple

Base generation prompt (verbatim):

```text
Use case: historical-scene
Asset type: full-page teaching illustration for a monochrome theological reference PDF
Primary request: Create a very finely detailed monochrome graphite architectural cutaway of Solomon’s Temple, explicitly a bounded teaching reconstruction based only on the textual spatial arrangement. Show a coherent single building along one continuous longitudinal axis: an exterior porch at the entrance, then a clearly long rectangular Holy Place, then a smaller inner sanctuary at the far end. Inside that inner sanctuary, show the Ark of the Covenant as a small rectangular chest placed beneath and between exactly two monumental cherubim; their great outstretched wings overshadow the Ark and span the chamber. Make the spatial sequence instantly legible without any words.
Scene/backdrop: isolated architectural study on bright clean white paper; no landscape and no modern site context
Style/medium: exceptionally refined museum-catalogue archaeological illustration in controlled graphite; rigorous architectural draftsmanship; crisp straight perspective lines; dense fine cross-hatching and delicate stippling that distinguish dressed stone, carved cedar paneling, and restrained gleaming gold surfaces through tonal value alone; highly resolved joinery, beams, wall thicknesses, floor courses, doors and architectural ornament, but no invented inscriptions
Composition/framing: landscape format; slight elevated three-quarter longitudinal cutaway, with one side wall and part of the roof cleanly removed; entrance porch nearest the viewer and inner sanctuary visible at the far end; show the full building without cropping; calm, precise one-point or two-point perspective; clear tonal separation between porch, long Holy Place, and inner sanctuary; the inner chamber and Ark remain visible rather than hidden by walls
Lighting/mood: neutral museum-display lighting, disciplined tonal hierarchy, white paper highlights, deep graphite only where needed for spatial depth
Color palette: pure black, white, and neutral graphite gray only; absolutely no color or sepia
Materials/textures: minute straight-rule stone courses, cedar grain and carved botanical ornament treated as careful reconstruction conventions, subtle gold sheen represented only by white highlights and fine parallel hatching
Constraints: exactly two great cherubim in the inner sanctuary; Ark directly below their overshadowing wings; teaching reconstruction rather than archaeological certainty; no modern Temple Mount claim; no exact footprint or dimensional annotation; no later Second Temple, Herodian, Roman, Byzantine, Islamic, or modern features; no people; no smoke or cloud obscuring the arrangement
Avoid: labels, captions, letters, numbers, arrows, scale bars, border, inset panels, pseudo-text, inscriptions, watermark, signature, rough sketch marks, random-step lines, wavy outlines, fuzzy charcoal, loose concept art, fantasy palace, colossal impossible scale, decorative symmetry that obscures the long interior sequence, extra cherubim, winged human crowds, angels outside the inner sanctuary, modern skyline, colored paper, cream paper, aged paper, vignette or dark background
```

Selected refinement prompt (verbatim):

```text
Edit the immediately preceding generated image with one focused historical-restraint correction while preserving its landscape framing, elevated longitudinal cutaway, bright-white-paper background, excellent crisp perspective, fine museum-grade graphite linework, and dense controlled cross-hatching.

Change the interior so it is a sober bounded teaching reconstruction and the porch → long Holy Place → inner sanctuary sequence is even clearer. Remove the ox-supported basin entirely (the great sea must not be inside this hall). Remove the menorah and all other freestanding ritual furniture, tables, vessels, and speculative props from the Holy Place; leave the long central floor open so the longitudinal sequence reads cleanly. Simplify the wall ornament enough that it does not resemble a fantasy palace or a later monumental style. Add a clear full-width architectural partition or threshold at the far end that unmistakably separates the inner sanctuary while still exposing it through the cutaway.

In the inner sanctuary, retain exactly two monumental cherubim and the small Ark beneath and between their overshadowing wings, but replace the lifelike kneeling human angels with deliberately restrained, non-naturalistic ancient guardian sculptures: simplified, solemn carved forms with no portrait-like human faces, no Christian angel iconography, no living-person gestures. Their two great wings should dominate and overshadow the Ark, spanning the chamber. Keep the Ark unmistakably smaller than the cherubim.

Preserve: monochrome neutral graphite only; finely ruled stone, cedar grain, crisp straight lines, controlled tonal hierarchy; exterior porch at the near end, long Holy Place, smaller inner sanctuary at the far end; full building visible without cropping; no smoke or cloud.

Do not add: any people, priests, animals, basins, menorahs, furniture, altar, incense, curtains that hide the layout, courtyard, landscape, modern Temple Mount, exact footprint or dimension marks, later Second Temple/Herodian/Roman/Byzantine/Islamic/modern features, labels, captions, letters, numbers, arrows, pseudo-text, inscriptions, border, watermark, signature, color, sepia, aged paper, rough/wavy lines, charcoal blur, fantasy ornament, or extra cherubim.
```

The selected result from that prompt was rejected because its guardian geometry
did not render the commanded wall-to-wall span and its porch capitals remained
too culturally specific. Final fidelity-correction prompt (verbatim):

```text
Use case: precise-object-edit
Asset type: full-page monochrome teaching illustration for a theological reference PDF
Input image: Image 1 is the edit target. Preserve its overall landscape framing, slight elevated three-quarter longitudinal cutaway, building proportions, porch → long Holy Place → inner sanctuary sequence, bright white paper, refined graphite medium, crisp straight perspective, fine stone and cedar cross-hatching, open uncluttered Holy Place, and clear visibility into the inner sanctuary.

Primary correction — inner sanctuary cherubim and Ark geometry:
Replace the existing eagle-like guardian statues and upright arched wings. Show EXACTLY TWO monumental great cherubim inside the inner sanctuary, positioned side by side across the 20-cubit width of that chamber. Each cherub has EXACTLY TWO horizontally outstretched wings, for exactly four wings total. All four wings are equal in represented length, each corresponding to 5 cubits. The four wings must create one continuous straight wall-to-wall horizontal span across the chamber: the left cherub’s outer wing extends left until its tip physically touches the left wall; its inner wing extends right until its tip physically touches the other inner wing at the exact chamber center; the right cherub’s inner wing extends left to that same central contact point; its outer wing extends right until its tip physically touches the right wall. No gaps at the side walls or center and no overlap. Make the wall contacts and center wingtip-to-wingtip contact visually unmistakable without labels. Wings extend laterally, nearly level, not upright, raised, folded, arched, or merely hovering above separate bodies.

Place the Ark of the Covenant visibly on the inner-sanctuary floor directly beneath the central meeting of the two inner wingtips, under the overarching wall-to-wall span. The Ark is much smaller than the monumental cherubim and is not fused to them. Retain exactly one Ark.

Cherubim body convention: restrained, hieratic, non-naturalistic carved guardian forms with compact simplified bodies and deliberately ambiguous anatomy; no identifiable human portrait, no Christian angel, no eagle or bird statue, no beaks, talons, naturalistic animal pose, or fantasy creature display. Their bodies support the wing roots but the commanding visual fact is the precise four-wing span. Treat all body details as subdued reconstruction convention.

Secondary correction — porch columns and speculative ornament:
Remove every Egyptian, papyrus, lotus, floral, or blossom-like capital and base. If the two porch pillars remain, give them plain undecorated cylindrical shafts, simple low rectilinear block capitals, and simple geometric bases, with no rival named historical style. Remove the pointed decorative roof-edge cresting and any conspicuously culture-specific or fantasy ornament. Keep architecture sober: dressed stone, cedar paneling, restrained rectilinear joinery.

Preserve invariants: one coherent building on a single long axis; exterior porch nearest viewer; clearly long Holy Place; smaller bounded inner sanctuary at far end; full building visible without cropping; wall thickness, beams, floor courses, and material textures finely resolved; controlled museum-catalogue graphite tonal hierarchy; pure neutral black, white, and gray on clean white paper.

Do not add: labels, captions, letters, numbers, dimension lines, arrows, scale bars, pseudo-text, inscriptions, borders, people, priests, animals, extra cherubim, extra wings, extra Arks, smoke, cloud, curtains hiding the layout, ritual furniture, basins, menorahs, tables, vessels, altars, incense, courtyard, landscape, modern Temple Mount context, exact footprint annotation, later Second Temple/Herodian/Roman/Byzantine/Islamic/modern features, color, sepia, cream or aged paper, watermark, signature, rough or wavy lines, charcoal blur, loose concept-art strokes, fantasy palace styling, or speculative decorative clutter.
```

That result corrected the ornament and general wing orientation but was rejected
because the two inner wingtips still left a visible central gap. Final zero-gap
correction prompt (verbatim):

```text
Use case: precise-object-edit. Preserve the full image and all graphite architecture. Edit ONLY the two large cherubim inside the dark rear sanctuary. The current inner wings still stop with a visible gap: REMOVE THAT GAP COMPLETELY. Give each of the exactly two standing cherubim exactly two wings. From the left figure, one wing must extend left until it visibly touches the left rear wall, and its other wing must extend far inward above the Ark to the exact center. From the right figure, one wing must extend inward above the Ark to that same center and the two inner wing tips must be drawn in direct physical contact—one continuous joined outline, zero white pixels or wall background between the tips. The right figure's other wing must visibly touch the right wall. The four-wing chain must be unmistakable at thumbnail size: left wall TOUCHES outer-left wing; wing joins left body; inner-left wing TOUCHES inner-right wing directly at center above Ark; wing joins right body; outer-right wing TOUCHES right wall. Enlarge and lengthen the two inner wings as needed; do not merely move the bodies. Keep exactly two bodies and exactly four wings total. Keep the Ark centered below the joined inner wingtips. Abstract monumental cherubim, no extra figures, no text, no labels, no color, no other composition changes.
```

## Source-control matrix

| Diagram claim | Controlling loci | Status | Rendering rule |
| --- | --- | --- | --- |
| Chest of acacia/setim wood, gold inside and outside | Ex 25:10–11; 37:1–2 | direct | State the wooden core in live text; do not let visible texture imply botanical certainty. |
| Relative dimensions: 2.5 by 1.5 by 1.5 cubits | Ex 25:10; 37:1 | direct | State cubits; do not convert to a supposedly exact modern length. |
| Four rings and two overlaid poles left in them | Ex 25:12–15; 37:3–5 | direct | Four rings may be partly occluded in perspective; state the commanded count and permanence in live text. |
| Pure-gold cover/mercy seat/propitiatory | Ex 25:17; 37:6 | direct | Keep cover distinct from the wood-and-overlay chest. |
| Two hammered cherubim, wings overshadowing, faces toward cover | Ex 25:18–20; 37:7–9 | direct features, unknown appearance | Use restrained abstract forms and print the non-reconstruction boundary. |
| Tablets inside; manna, rod, and law-book descriptions differ by locus | Ex 16:32–34; 25:16, 21; Num 17:4–10; Deut 10:1–5; 31:24–26; Heb 9:4; 1 Kgs 8:9 | direct, witness-sensitive | Explain in prose; do not invent an interior still life or a transfer history. |
| Ark behind the Tabernacle veil | Ex 26:31–34; 40:18–21 | direct arrangement | Use a bounded teaching cutaway and make no recovered-footprint claim. |
| Ark at Shiloh amid Tent/house/temple, door, and lamp language | Josh 18:1; 1 Sam 1:9; 3:3, 15; 4:3–4 | direct presence, form uncertain | Resolve the Ark but leave the setting visibly incomplete; do not draw a factual building. |
| Ark within the tent David pitched; old Tabernacle at Gibeon | 2 Sam 6:17; 1 Chr 16:1, 39–40 | direct, complementary | A symbolic tent is permitted only with a non-reconstruction label. |
| Ark in Solomon's inner sanctuary beneath great cherubim | 1 Kgs 6:19–28; 8:1–11; 2 Chr 5:2–14 | direct textual arrangement | Use a bounded teaching cutaway, not a precise Temple Mount footprint or recovered elevation. |
| Two equal great cherubim; each wing five cubits; outer wings touch the walls and inner wings touch one another | 1 Kgs 6:23–28; 2 Chr 3:10–13 | direct commanded geometry, unknown body appearance | Make the four-wing wall-to-wall span legible while keeping the bodies hieratic and non-reconstructive. |

The matrix controls the captions and text equivalent even when an image cannot
visually carry a distinction. The following boundary is therefore mandatory:

- **Commanded Ark facts:** one chest; acacia/setim-wood core; overlay inside and
  outside; the stated relative dimensions; a distinct pure-gold cover; four
  rings; two overlaid poles remaining in the rings; and two hammered cherubim
  whose wings overshadow the cover and whose faces turn toward it.
- **Interpretive Ark ornament:** every visible surface texture, joinery choice,
  molding, hammered pattern, ring profile, pole end, cherub body, faceted wing
  articulation, facial plane, precise proportion in perspective, and tonal
  indication of gold is an illustrator's convention. The final Ark plate's
  guardians are deliberately non-avian and non-human. The commanded species of
  wood does not license a claimed botanical portrait. The images disclose no
  interior.
- **Tabernacle:** the Ark-behind-the-veil relationship and the east-to-west
  nested arrangement are text-controlled. The visible fabrics, framing,
  hardware, courtyard detailing, proportions in perspective, and cutaway
  treatment are an interpretive reconstruction, not a recovered structure.
- **Shiloh:** only the Ark's presence is resolved. The detached dissolving tent
  fold, broken threshold/jamb idea, and faint lamp-light halo are mutually
  incompatible thought-fragments, not evidence of a footprint, excavation, or
  building. They share no horizon, scale, orientation, alignment, enclosure,
  ground plane, or relation to the Ark. The sanctuary form is intentionally
  unresolved.
- **David's tent:** Scripture attests a tent David pitched and the Ark placed
  within it, but the tent's appearance, plan, material details, terrain, and
  location are unrecovered. The plate is a deliberately generic interpretive
  shelter, not a reconstruction.
- **Solomon's Temple:** the longitudinal sequence, the Ark beneath the great
  cherubim, and the two cherubim's equal four-wing wall-to-wall span are
  text-controlled. Their body form and every other visible elevation, façade,
  masonry, cedar, ornament, floor, wall thickness, door, pillar, and precise
  scale choice are interpretive reconstruction conventions. The plain pillars
  are an anti-speculative visual convention, not a recovered style. The plate
  makes no claim about a recoverable Temple Mount footprint or later sanctuary.

## Exclusions

The plates do not claim:

- a recovered portrait of the Ark or cherubim;
- a fixed modern length for the cubit;
- that the law-book was inside the Ark;
- an explanation for how the manna vessel or rod entered or left;
- an excavated Ark, Tabernacle, Shiloh sanctuary, Davidic tent, or First-Temple
  Holy of Holies;
- a single architectural continuity among the four settings;
- that generated detail is historical evidence merely because it looks
  precise;
- that an omitted, occluded, or visually simplified feature changes the
  controlling textual claim; or
- that Mary is an object, building, or container of the divine nature.

## Production acceptance

Final state: `internal consumer review and installation identity pass;
deployment identity pending`.

The accepted 46-page consumer PDF has SHA-256
`0d995ac1d447f53cc55496fa8907c16a7940639b986fee02579b16e87d7164da`.
Its review manifest is
`build/pdf-review/gpt-ark-postff-2026-08-16/review-run.json`. The generated web
edition has SHA-256
`8083f51e35ce1d72fdd306d23c378361e70f778ee27f1a7acaeb915c1e27a2d4`.
The installed GPT PDF and web edition are byte-identical to those reviewed
artifacts at the same respective identities.
Pages 17--19 passed full-size inspection. The consistent fine 0.25 pt frames
make the five images' paper fields intentional plate boundaries rather than
accidental gray-background seams.

- [x] Each final tracked hash above matches the asset consumed by the source.
- [x] Each plate is rendered at sufficient effective resolution for its final
  physical size, with no visible resampling artifacts.
- [x] Full-size inspection confirms fine, stable graphite detail rather than
  rough, wavy, random-step, or DOT/Graphviz-like linework.
- [x] The Ark plate preserves readable counts of one chest, one distinct cover,
  four rings, two poles, and two cherubim without asserting that their visible
  ornament is recovered fact; the two guardians remain cover-integral,
  abstract, non-avian, and non-human.
- [x] The Tabernacle and Solomon plates remain visibly subordinate to their
  reconstruction cautions; the Solomon plate preserves the wall-to-wall
  four-wing span, direct zero-gap central wingtip contact, and plain,
  non-style-specific pillars.
- [x] The Shiloh plate communicates uncertainty more strongly than its
  deliberately incomplete architectural ghosts communicate form, with no
  excavation, site-plan, ground, or location cues.
- [x] The Davidic plate's caption states that the tent's form and site are
  unrecovered, and the white-ground shelter does not imply a landscape or fixed
  architectural plan.
- [x] Every live TeX title, caption, and caution extracts from the PDF in
  reading order and no text collides with the artwork or exits the page.
- [x] Each grayscale illustration remains legible in the printed PDF and in a
  grayscale photocopy simulation.
- [x] The text equivalent preserves every visible factual feature and every
  nonclaim in the web edition.
- [x] Every rendered page of the consumer PDF has been inspected, with the five
  illustration placements also checked at full size.
- [x] The installed PDF and web-edition identities have been compared with the
  reviewed build and recorded here.
- [ ] The deployed PDF and web-edition identities have been compared with the
  reviewed and installed artifacts and recorded here.

The parent publication task owns the remaining deployment identity check and
will close it only after deployment verification. Earlier acceptance hashes for
the superseded TikZ plates do not apply to these replacement assets.
