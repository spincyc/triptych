# Shared sanctuary scene revision — 7 November 2026

This record identifies the reusable artwork and source composition introduced
for the Low Mass child booklet and trainer manual, Missa Cantata guide and
Solemn Mass guide. These are project-created teaching illustrations. Their
architecture, spacing and route geometry are a declared rehearsal model;
neither an image nor a successful build establishes a ceremonial rule.

The source distinctions and action assignments remain those in
[`ceremonial-inventory.md`](ceremonial-inventory.md) and the
[shared-scene source audit](source-audit.md#shared-scene-audit-2026-11-07).
This revision does not claim a new facsimile collation of the received Latin
or a new verification of the underlying source loci.

## Architectural and movement contract

`shared/sanctuary-scenes.tex` composes every position view with the same
`ASG-ART-032` backdrop. The altar, tabernacle, crucifix, steps and credence
stay fixed. Gospel remains picture-left and Epistle picture-right, viewed
from the nave. The numbered levels are 1, lowest step; 2, second step; and
3, predella. The floor is separate. Actual steps, distances, reverences and
side lanes must be mapped at the church before rehearsal.

The form changes the candle count through reusable `ASG-ART-036` layers:
two for the Low Mass model, six for the sung models. Actor layers change
position, posture or facing without redrawing the sanctuary. TeX supplies
role capsules, object stations, side names, level numbers and route marks;
these are not baked into the PNGs. Label capsules occupy a separate drawing
layer above the figures. Dashed arrows show travel; lettered stops mark
successive places without duplicating an actor. A side-by-side plan inset
clarifies the stationary Low Mass cruet and Lavabo pairs.

A neutral figure locates the named actor. It does not purport to show a
simultaneous bow, genuflection, pour or elevation. Separate close views retain
the hand actions. The Low Mass elevation and ablution images are cropped by
TeX to the relevant details so their earlier architecture cannot compete
with the shared position backdrop.

The shared movement-field macro and every sung atlas panel use five fields:
cue, who/object, route, finish and waiting. The Low Mass Gospel,
post-elevation and book/veil return
sequences expose distinct states. At the book/veil crossing A, First waits
for Second to clear the crossing; this is the recorded LOCAL traffic choice.
The sung atlas preserves the different ablution assignments: First alone in
Low Mass; A1 wine and A2 water in Missa Cantata; SD pouring with A1 supplying
both cruets in Solemn Mass. Station labels for sacred ministers do not assign
their offices to the lay-server figure layers.

## New asset catalogue and composition briefs

All selected files are under `shared/artwork/pencil/`. These descriptions
record the intended composition and use, not verbatim generation prompts.

| ID | Filename | Composition and role |
| --- | --- | --- |
| `ASG-ART-032` | `ASG-ART-032-sanctuary-master.png` | Fixed nave-facing altar, tabernacle, crucifix, three levels and picture-right credence; no people or scene-specific route marks |
| `ASG-ART-033` | `ASG-ART-033-server-standing.png` | Standing server seen from behind; neutral station layer |
| `ASG-ART-034` | `ASG-ART-034-server-kneeling.png` | Kneeling server seen from behind; posture distinguishable by silhouette |
| `ASG-ART-035` | `ASG-ART-035-priest-standing.png` | Standing priest seen from behind; neutral station layer |
| `ASG-ART-036` | `ASG-ART-036-altar-candle.png` | One upright altar candle, repeated at the form's declared positions |
| `ASG-ART-037` | `ASG-ART-037-server-facing-left.png` | Standing server facing picture-left for the Epistle-side handoff station |
| `ASG-ART-038` | `ASG-ART-038-priest-facing-right.png` | Standing priest facing picture-right toward the Epistle-side servers |

Production used the built-in OpenAI image-generation interface on
2026-11-07. The interface exposed no generator model or version. Each asset
was a new generation from a textual composition brief; no reference-image
path was supplied. The generating agent viewed the older project-created
`ASG-ART-011` for style understanding, but it was not supplied as an image
input. No third-party image bytes or named artist's work were incorporated.
These are AI-generated pencil-style images, not human-made drawings.
Distribution follows repository terms only to the extent applicable rights
exist.

The exact prompts were not durably retained and are not reconstructed here.
No SVG or code-drawn image was an intermediate source. ImageMagick performed
technical grayscale conversion, proportional reduction of the actor/candle
layers and metadata stripping. The generated alpha channel was preserved on
`033`–`038`; `032` remains opaque. The normalized files are 8-bit grayscale
or grayscale-alpha PNGs. There was no semantic retouching or crop in this
normalization. TeX cropping of older detail images is a separate presentation
operation, declared above.

## Exact received and selected identities

The received hashes identify the outputs available during this audit. They
do not assert durable distribution of the larger received files. The selected
normalized PNGs are the canonical render inputs.

| ID | Received pixels | Received bytes | Received SHA-256 |
| --- | --- | ---: | --- |
| `032` | 1536 × 1024 | 1637911 | `2776ccc9b2cc42637c0e79c61990c44023eeafdfba3fe1e240ec9f156921435c` |
| `033` | 1024 × 1536 | 1666400 | `1e1a33fd94406122e97ecaebd1f84a4fdcbcad43427dd7598c2d01f4a52008a2` |
| `034` | 1024 × 1536 | 1956856 | `51b7b917e7581df9996f5a71975f47e64d644f670b59d1a28595321cfc9967c7` |
| `035` | 1024 × 1536 | 1941143 | `62b3737e9318d2cf67c0b82d462ea4eb535d1f5cf0cfb248a3a1453c514b36e2` |
| `036` | 1024 × 1536 | 1223543 | `688547f803639cd4dba2326f53eb834d6ebed78f65f41216ceed6bfefdea058c` |
| `037` | 1024 × 1536 | 1659314 | `25724f4ff9ff5c808132156e5bcf6bad975335bfb6159d02b2e6dad4635a585d` |
| `038` | 1024 × 1536 | 1710110 | `d7bf8f423528bf9cb7379aeb58169732df2f58c610431bcc383907f51356bcfa` |

| ID | Selected pixels | Selected bytes | Selected SHA-256 |
| --- | --- | ---: | --- |
| `032` | 1536 × 1024 | 499721 | `96955ab253fe20bd0be7afb94cb3fb3cc68b8970bb1bfd00a477f6a9fb1704ed` |
| `033` | 427 × 640 | 78965 | `f4b6b312e3db2967e5bfa338280896714a38b405a741a55582666472324a861d` |
| `034` | 320 × 480 | 58294 | `01588c45449cce4ca16cd74e60c981630c51c2fd3c2e68239a67d9b45b3ebee7` |
| `035` | 427 × 640 | 93664 | `5ca65a5637af0d7da6f50671478308d74cdb8c5082de35317ad5a99df761e33a` |
| `036` | 213 × 320 | 12417 | `0ae9c90aaf97c5cd2e86c3a6f3522b6105d668cc0a3754e67186942eb53a3c0f` |
| `037` | 427 × 640 | 72956 | `3779728dd0c0dc204e17a36df664b088eccb24514ceeaeba110505cb47076bb9` |
| `038` | 427 × 640 | 75678 | `4f616515ff36815567d04c3896391e8dc3269ab03b071e231692d732e5028d93` |

## Composition coverage and positive selection

The Low Mass source defines fifteen position states, all used. The arrival
state also appears in the preparation appendix,
giving sixteen rendered position views in each edition. `LMSceneCruets`
is an alias for `LMSceneCruetService`, not a further state.
Four retained raster assets supply the Lavabo, elevation-hand,
Communion-plate and ablution details. The empty compatibility macro
`LMSceneFingerWashing` adds no separate drawing.

The sung diagram source defines thirteen distinct position states. The
movement atlas uses them in sixteen panels, eight per sung form, with the
Lavabo, Canon and departure states shared between forms. Missa Cantata also
uses its Gospel position state in the role-sheet Gospel explanation.
The catalogue distinguishes reusable definitions, rendered panels and
selected image files; those counts are not interchangeable.

| Edition | New layer files selected | Retained detail files selected | Total PNGs in native source bundle |
| --- | ---: | ---: | ---: |
| Low Mass child | 7 | 4 | 11 |
| Low Mass trainer | 7 | 4 | 11 |
| Missa Cantata | 7 | 5 | 12 |
| Solemn Mass | 6 | 5 | 11 |
| Each of the three card companions | 0 | 0 | 0 |

`scripts/_native_print_artwork.py` follows the macros actually called by the
selected form, including position macros passed as panel arguments. It reads
the shared scene source into the input identity and keeps unused definitions,
inactive branches and historical sibling PNGs out of the selected binary
set. A regression fixture changes shared geometry and confirms that both
bundle content and render identities change.

## Review extent

The generating agent inspected all seven normalized assets at full size and
checked the transparent layers composited on white. This is a bounded asset
inspection, not an integrated-page review or a source-locus verification.
Every-page screen review of all four composed guides, including the
independent Solemn review, and the exact final print identities are recorded
in [`production-manifest.md`](production-manifest.md). The final four proofs
contain 33, 33, 39 and 35 pages. Source-frozen rebuilds retain the accepted
page pixels, apart from three terminal revision-stamp pages inspected again.
Earlier
5 November PDF hashes and approvals do not apply to the new source state.

The native print page and source-bundle suite passed all 32 tests. Preparation
of all seven actual source bundles passed the metadata and declared-build-graph
checks and matched each bundle's PNG set to positive artwork selection.
The working receipts are under `.scratch/native-assets/`; they describe
source assembly, not browser-WASM execution, physical printing or
ecclesiastical approval. The final source-closure report is
`.scratch/native-assets/bundle-closure-final.json`; final proof and
source-freeze receipts are recorded separately in the production manifest.
