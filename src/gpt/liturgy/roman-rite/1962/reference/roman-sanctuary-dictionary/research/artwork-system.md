# Roman pictorial dictionary artwork system

Status: production specification prepared 2026-07-27; no dictionary artwork
has yet been generated under this record.

This record extends the altar-server series' established monochrome graphite
grammar to the planned comprehensive Roman pictorial dictionary and its
use-based extracts. It does not authorize generation, approve an image, or
establish the identity, period, use, or handling of any depicted object.
Those facts must come from the dictionary's verified inventory and source
audit before a prompt is issued.

The dictionary is an image-dense US Letter portrait visual atlas for a broad
adult audience. Its comprehensive edition is authoritative; server,
sacristan, MC/trainer, general-reader, and pontifical extracts reuse selected
figures and plates rather than creating independently maintained artwork.
English and Latin names are typeset outside the images. Pronunciation belongs
in terminal apparatus, not on the plates.

## Stable identity

Artwork IDs are semantic inventory identities, never page numbers:

```text
art-<object-key>-<view-or-state>
art-<composition-key>-composition
plt-<section-key>-<comparison-key>
```

- `art-...` identifies one object, inseparable object set, or contextual
  composition in one stable view or state. Its `object_ids` field, rather than
  a filename inference, is the authoritative link to the canonical inventory.
  Allowed view values are controlled by
  `shared/schema/artwork-manifest-schema.toml`.
- `plt-...` identifies a composed, TeX-labelled comparison plate. A plate
  consumes approved figures and ordinarily introduces no new generated
  pixels.
- An artwork record with view `composition` identifies a contextual scene
  whose spatial relationships
  are themselves the subject: a sanctuary, vested minister, ceremony-specific
  arrangement, or object-transfer state.
- All IDs follow the repository-wide lowercase kebab-case namespace contract
  in `shared/schema/inventory-schema.toml`.
- A correction receives a new complete ID. The rejected precursor remains in
  the manifest as a non-consumed provenance object. Do not add `corrected`,
  `final`, `new`, a date, or a page number to an ID.
- Materially different varieties receive distinct figure IDs linked by one
  variant-set key. Alternate angles of the same specimen share the object
  inventory ID but remain distinct artwork IDs.
- A cropped or scaled placement is not new artwork. A genuinely redrawn
  detail or materially different state is.

Each artwork entry must record its logical ID, object and variant-set IDs,
file, purpose, exact depicted state, period and use status, source-controlled
features, deliberately omitted details, generation or correction relationship,
generator interface, date, received and normalized technical properties,
hash, baked-in-content audit, TeX overlays, consumers, rights state, and review
state. Exact prompts must be preserved verbatim for future assets; a normalized
prompt summary does not replace them.

The canonical entry format is
`shared/schema/artwork-manifest-schema.toml`; production records live only in
`research/artwork-manifest.toml`. The exact prompt is preserved as a multiline
TOML string. If an interface does not expose a model or version, say so in the
generator field; do not infer it. Record every supplied project-artwork or
canonical source-artifact ID and its role in the brief. A plate assembled
entirely in TeX from approved figures belongs in the plate manifest and names
those dependencies; it is not a generated artwork record.

## Figure and plate grouping

The normal plate contains six to ten simple distinctive figures. Use four to
six where objects are easily confused, and two to three where vestments need
front, back, and worn views. Reserve a full spread for a sanctuary composition,
complete vested minister, complex pontifical group, or ceremony-specific
arrangement.

Group figures by the visual question a reader must answer:

- **recognition sets:** objects likely to be confused, especially corporal,
  purificator, pall, lavabo towel, credence cloth, communion cloth, amice,
  chalice veil, burse, humeral veil, gremial, and vimpa;
- **functional families:** chalice sets, incense equipment, cruets and
  lavabo equipment, book families, candles and carriers, pontifical insignia;
- **construction comparisons:** Roman and Gothic chasubles, dalmatic and
  tunicle, mitre forms, monstrance forms, processional-cross forms;
- **placement sets:** altar appointments, credence table, sedilia, episcopal
  throne or faldstool, Requiem and Holy Week arrangements;
- **historical sets:** chronological first, then functional within each
  period, never silently mixed into the normative 1962 plates;
- **handling sets:** only in use-based extracts, selected from canonical
  figures and accompanied by TeX-owned handling marks.

An ambiguous object receives at least one additional view or small context
figure. White rectangles and folded textiles normally require folded and
unfolded views plus a placed, worn, or in-use inset. Objects whose size is an
identifying feature appear at common scale. Otherwise the plate prints a scale
bar, approximate verified dimensions, or `not to common scale`. Never imply
common scale through equal bounding boxes.

Atmospheric scenes are exceptional. Most figures are isolated on clean white
ground so plates can remain dense, differences remain legible, and monochrome
photocopies remain useful. Context is normally a tightly cropped figure rather
than a second full scene.

## Prompt grammar

Dictionary generation uses the built-in image-generation interface by default,
one call per distinct asset or variant. Do not use one multi-subject generation
as a substitute for separately reviewable figures. Reference inputs, when
used, must be project-created composition sheets or lawful, manifested source
artifacts, and their role must be named explicitly. An existing local image
must be visually inspected before an edit call.

Use this grammar, omitting inapplicable lines:

```text
Use case: scientific-educational
Asset type: monochrome reference figure for a US Letter portrait Roman
liturgical pictorial dictionary
Primary request: Draw <one exact verified object, set, view, or state>.
Input images: <Image 1: edit target / composition reference / construction
reference; repeat as needed>
Identity and period: <preferred object name; Latin headword for prompt
disambiguation only; universal 1962 Roman / authorized regional /
religious-order / historical period>
Required construction: <short source-controlled checklist of shape, parts,
folds, fastening, material behavior, and distinguishing features>
Required state: <empty/assembled/open/folded/worn/placed/in use; exact contents
and relationships>
Composition/framing: <orthographic or three-quarter view; full object visible;
consistent eye level; generous crop safety; relation to comparison-set scale>
Style/medium: elegant historically attentive monochrome graphite drawing,
fine controlled pencil line, restrained tonal modelling, white paper ground,
matching the approved RPD reference figures
Lighting/mood: even neutral studio illumination; quiet reference-plate clarity
Color palette: grayscale only; white ground; no colored wash
Materials/textures: <verified metal, textile, wood, leather, glass, etc.>;
render enough texture to distinguish construction without decorative invention
TeX-owned additions: leave clear space for externally typeset name, Latin
name, scale, handling mark, and callouts
Constraints: depict only the requested subject and specified context; preserve
all listed construction invariants; no clipped parts; no cast scene background
Avoid: all lettering, numerals, arrows, labels, captions, watermarks, borders,
color, architectural scenery unless requested, extra objects, invented
ornament, invented crosses, invented clasps, impossible folds, duplicate
parts, extra stems/feet/handles, reflections that obscure construction, and
anachronistic details
```

For an edit, append:

```text
Edit boundary: change only <named defect>. Preserve <complete invariant list:
silhouette, construction, viewpoint, scale, lighting, graphite treatment,
crop, and all already approved details>.
```

For a cutaway or construction detail, append:

```text
Cutaway purpose: reveal <verified interior construction or layer relationship>.
Cut plane and retained shell: <exact plane; what remains intact>.
Visible interior: <only the verified layers, seams, stiffening, cavity,
fastening, lining, support, or contents>.
Graphic treatment: use a clean graphite sectional edge and slightly lighter
interior tones; no color coding, exploded parts, invented mechanism, or
engineering-style labels.
Pairing: match <approved exterior figure ID> in orientation, proportions,
scale, crop, lighting, and ornament.
```

A cutaway is permitted only when hidden construction materially aids
identification or correct handling and the interior is source-supported.
Where evidence supports layers but not exact concealed construction, use an
opened, unfolded, or displaced-layer view instead and state the limit. Never
let a visually plausible invented interior become evidence.

For a contextual scene, state every actor, object, orientation, support,
contact, and spatial relationship. Do not ask the model to infer a rubric from
the ceremony name. TeX continues to own role names, movement routes, level
numbers, and explanatory callouts.

Use this sanctuary-composition supplement:

```text
Scene identity: <exact ceremony and state, edition horizon, universal or
qualified local model>.
Viewer and orientation: nave-facing / overhead / oblique; explicitly map
picture-left and picture-right to liturgical Gospel and Epistle sides.
Architecture: <verified altar type, number of levels, predella, rail, throne,
credence, sedilia, doors, and only other required features>.
Appointments: <complete enumerated object list with exact placement and count>.
People: <complete enumerated ministers, posture, facing, vesture, carried
objects, support/contact relationships, and relative station>.
Empty zones: preserve clear label lanes and crop safety at <locations>.
Do not infer: omit every architectural feature, person, object, flame, book,
textile, or ornament not enumerated above.
```

Generate frontal and overhead members of a pair separately from the same
verified composition record. Do not ask the model to create a multi-panel
labelled diagram. TeX assembles panels and owns correspondence marks.

Prompts must not request imitation of a named living artist. They must not
name an unverified ceremonial fact, silently merge variants, or use a museum
or vendor image without the required source and rights record. Generated text
is prohibited even when the model could plausibly spell it.

## Review gates

Review proceeds per figure before plate composition, then per rendered plate,
then per publication consumer.

### Figure factual review

- Inventory identity, Latin association, period, status, ceremony, and variant
  agree with the verified record.
- Silhouette, components, proportions, fastening, folds, openings, supports,
  and material behavior are plausible and source-supported.
- No extra, missing, duplicated, fused, floating, or impossible component is
  present; explicitly check stems, feet, handles, chains, clasps, crosses,
  cords, tassels, book hardware, fingers, and vestment openings.
- A worn object is worn by the correct minister, in the correct orientation
  and layer, without impossible anatomy or cloth behavior.
- An in-use object has the correct giver, receiver, support, contact point,
  contents, direction, and destination.
- Ornament is either source-controlled or generic and non-assertive; the
  drawing does not manufacture a universal rule from one decorative example.
- Historical, regional, and religious-order forms remain visibly and
  editorially distinct from universal 1962 use.

### Figure visual and technical review

- Graphite line, tonal range, white ground, viewpoint, crop safety, and scale
  agree with the approved comparison family.
- The object reads at its largest and smallest declared print placements and
  after grayscale photocopying.
- No baked-in text, pseudo-text, arrow, number, label, watermark, border, color
  cast, or unintended background is present.
- Ambiguous figures have an adequate second view or context inset; recognition
  does not depend on a paragraph.
- Received and normalized dimensions, mode, bytes, hash, comparison metric,
  and full-size visual comparison are recorded. Publication input is an
  8-bit grayscale PNG at at least 300 effective dpi; repository review
  triggers in `guidance/repository.md` remain applicable.

### Plate review

- Every TeX label points unambiguously to the intended figure and agrees with
  the canonical English and Latin inventory names.
- Similar items are compared at common scale when scale distinguishes them;
  otherwise the scale treatment is explicit.
- The portrait page remains image-dominant, normally six to ten figures, with
  sufficient white space and no collision among figures, captions, source-note
  keys, scale marks, or handling symbols.
- Brief purpose and symbolism lines do not displace necessary recognition
  views. Symbolism is included only when sourced and is labelled as a
  traditional association when appropriate.
- A figure's status marker distinguishes universal Roman use, authorized or
  regional variant, religious-order use, and historical example.
- Numbered endnote keys lead to sources actually used; disputed
  identifications alone receive an on-plate qualification.

### Consumer review

- Comprehensive and use-based editions consume the same approved figure or
  an explicitly different view; no silent redrawing or drifting duplicate
  exists.
- Server extracts include everything that may be present around the server,
  not only objects the server handles, and TeX accurately distinguishes
  touch, carry, present, prepare, and recognize-only boundaries.
- Every affected PDF is rebuilt, its logs checked, and every rendered page
  visually inspected through the repository review tooling.
- Actual-size print, grayscale photocopy, intended-reader, independent
  liturgical/ceremonial, and rights reviews are recorded separately. Screen
  approval does not imply those gates passed.

## Candidate lifecycle

Every new candidate begins `unreviewed` and may advance only through
`factual-review-passed`, `visual-review-passed`, `plate-review-passed`, and
`consumer-review-passed`. A failed candidate is `rejected` with a concrete
defect and no publication consumer. A corrected candidate has a new ID and
names its precursor. Only a consumer-reviewed normalized asset may be
installed. Release approval remains separate from artwork approval.

The built-in interface's received-file location is transient. Project-bound
selected outputs must be copied into the authoritative workspace artwork path
and entered in the artwork manifest. Rejected alternatives need not be kept
unless they are used as correction inputs; retained precursors are manifest
records and may never be rendered by a publication consumer.

## Asset-manifest workflow

1. **Inventory lock.** Assign the object, variant, period, status, ceremony,
   and handling data; cite sources controlling depicted construction and use.
   Artwork does not begin while a visual invariant is an unverified lead.
2. **Figure plan.** Assign the semantic figure ID and view/state. Name its
   comparison family, intended plate, print placements, scale policy, and
   whether ambiguity requires another view, context inset, or cutaway.
3. **Prompt record.** Save the exact prompt before generation, with every
   input image and role. Generate one distinct asset or variant per call
   through the built-in interface unless the user explicitly authorizes the
   documented CLI fallback.
4. **Received candidate.** Inspect at full size before copying it into the
   workspace. If selected, record dimensions, mode, and exposed interface
   metadata. Do not overwrite an existing asset.
5. **Factual gate.** Compare pixels against the locked invariants. Reject with
   a concrete defect or advance; do not repair an evidentiary error only in
   caption text.
6. **Correction.** Give a correction a new ID, preserve its exact edit prompt,
   name the precursor, and list all invariants to preserve. A retained rejected
   precursor has no consumers.
7. **Normalization.** Copy the selected asset to the authoritative artwork
   path; create a loss-minimizing 8-bit grayscale PNG; record before/after
   bytes, mode, dimensions, transformed hash, comparison metric, and full-size
   comparison. Never normalize acquired evidence artifacts.
8. **Plate assembly.** Compose approved figures with TeX-owned names, Latin
   headwords, scale treatment, status and handling marks, note keys, and
   callouts. Record every figure dependency in the plate entry.
9. **Plate and consumer gates.** Review the portrait page at actual size and
   under photocopy conditions, then build and inspect every comprehensive and
   derived consumer. Record each gate independently.
10. **Installation and release.** Only normalized, consumer-reviewed assets
    may enter reviewed PDFs. Artwork approval, PDF installation, release
    approval, public push, and deployment remain distinct authorizations.

The dependency graph is:

```text
verified inventory record
  -> exact prompt record
  -> received candidate
  -> approved normalized RPD-FIG or RPD-SCN
  -> TeX-composed RPD-PLT
  -> comprehensive dictionary
  -> one or more use-based extracts
```

A change to a source-controlled feature invalidates the figure's factual gate
and every downstream plate and consumer review. A caption-only, label-only, or
selection-only change invalidates only the affected plate and consumers unless
it reveals that the pixels themselves are wrong.
