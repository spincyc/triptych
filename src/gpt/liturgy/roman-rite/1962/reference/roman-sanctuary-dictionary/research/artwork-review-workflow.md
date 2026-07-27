# Review-edition artwork correction workflow

Status: production instruction prepared 2026-07-27. It governs future
review-edition figures, compositions, plates, and correction rounds; it does
not record an approval for artwork that has not yet been produced.

This workflow supplements `artwork-system.md`, the structured artwork and
plate manifests, and the pictorial-dictionary profile. Review is evidence
collection, not a vote on whether a picture is attractive. A reviewer reports
observable defects against a named asset, plate, source-controlled invariant,
or print condition. The owning editor classifies the report and determines
which gate and downstream consumers it invalidates.

## Review packet

Every review packet has a stable packet key independent of pagination and
contains:

- exact review-edition PDF hash and leaf ID;
- artwork and plate manifest snapshots used by that PDF;
- one asset sheet at full pixel size for every new or corrected figure;
- actual-size plate pages and a scale statement;
- a monochrome-photocopy sample for representative dense, linen, vestment,
  and sanctuary-composition plates;
- the canonical English and Latin names, status, variant, period, and source
  keys needed to judge each depicted identity;
- the approved invariant list and deliberately simplified or omitted details;
- an issue form using the standardized questions below.

Do not ask a reviewer to infer which candidate, crop, PDF build, or object
record was examined. A packet containing changed pixels receives a new PDF
identity and review round even when its displayed title is unchanged.

## Reviewer roles

Keep conclusions separate:

- **factual-artwork reviewer:** identity, morphology, vesting, object
  relationships, ritual placement, period, variant, and status;
- **visual-production reviewer:** graphite consistency, ambiguity, crop,
  contrast, scale, label lane, and actual-size/photocopy legibility;
- **audience reviewer:** whether the selected view and compact context let the
  edition's intended reader recognize the object and its handling boundary;
- **rights reviewer:** supplied references, incorporation risk, rights status,
  and whether a correction would require a new source or permission analysis;
- **release reviewer:** confirms that all required independent results and
  exact-byte identities are recorded; does not substitute for them.

One person may fill more than one role only when the production record says
so. Record each role's result separately; `looks good` is not an independent
factual or rights review.

## Standardized reviewer questions

Ask one asset or plate at a time. The reviewer may answer `yes`, `no`, `not
applicable`, or `cannot determine`, followed by a short reason and, for a
defect, the exact location.

### Object or vestment figure

1. **Identity:** Can you identify the depicted object without reading the
   caption? What did you identify it as?
2. **Diagnostic features:** Are all source-controlled distinguishing parts
   present and correctly shaped, joined, folded, fastened, or layered?
3. **False detail:** Is any visible part, ornament, cross, clasp, seam, handle,
   stem, foot, chain, cord, tassel, opening, support, or content invented,
   duplicated, missing, fused, or impossible?
4. **State:** Does the figure show the declared state—open, folded, worn,
   placed, assembled, empty, filled, or in use—without implying another state?
5. **Variant and period:** Does the drawing belong to the named substantive
   variant and period without silently borrowing features from another?
6. **Material:** Does monochrome shading communicate the verified material
   without falsely prescribing finish, color, weave, stiffness, or ornament?
7. **Scale:** Is the scale relationship accurate where diagnostic, or is the
   lack of common scale unmistakable?
8. **Ambiguity:** Is a second view, opened view, context inset, worn view, or
   sourced cutaway still required for reliable recognition?
9. **Print:** At declared actual size and in the photocopy, do diagnostic
   outlines and tonal separations remain distinct?
10. **Decision:** Pass, pass only after a caption/plate correction, return for
    pixel correction, reject and redraw, or cannot determine pending evidence?

### Worn or in-use figure

1. Is the correct minister or handler shown?
2. Is the object correctly oriented, supported, contacted, carried, presented,
   worn, and layered?
3. Are the giver, receiver, contents, direction, and destination correct for
   the declared state?
4. Are posture, hands, anatomy, cloth behavior, and object weight plausible?
5. Does the picture imply a universal rule where the record identifies a
   branch, privilege, regional use, or representative example?

### Sanctuary or ceremonial composition

1. From which viewpoint is the scene shown, and are Gospel and Epistle sides
   mapped correctly for that viewpoint?
2. Are every enumerated architectural feature, appointment, object, person,
   count, posture, facing, vestment, and station present exactly once?
3. Is anything not in the locked composition record visibly asserted?
4. Are supports, contacts, sightlines, levels, relative distances, and traffic
   clear and physically possible?
5. Can TeX labels and callouts be placed without obscuring a diagnostic
   feature or creating a false association?
6. Does the scene remain intelligible at actual page size and in monochrome
   photocopy?
7. If paired with an overhead, frontal, or detail view, do the views describe
   the same verified composition without contradiction?

### Composed plate

1. Does each English and Latin headword point unambiguously to the correct
   figure?
2. Are common scale, sourced dimensions, scale bars, and `not to common scale`
   notices used honestly?
3. Does the page remain image-dominant while preserving enough white space to
   distinguish every object?
4. Are status, period, handling, symbolism, and note marks accurate and
   visually subordinate?
5. Are confusable objects compared closely enough to teach the difference?
6. Is any needed view too small, too faint, clipped, or separated from its
   comparison?
7. Does the plate answer the intended audience's recognition or handling
   question without relying on extended prose?

### Rights and evidence

1. Were all visual references named in the manifest, with their role and
   rights status?
2. Does the candidate reproduce a distinctive protected composition,
   ornament, photograph-specific defect, background, or museum/vendor
   presentation not required by the verified object facts?
3. Is every criticized or approved construction feature supported by a
   source appropriate to morphology, rather than inferred from ritual use?
4. Is more evidence needed before a correction prompt can describe the
   desired pixels?

## Issue record

Every actionable report receives an issue key and this minimum record:

```text
Issue:
Review packet:
Reviewer role:
Asset or plate ID:
PDF leaf and hash:
Observed location:
Classification:
Severity:
Observation:
Expected invariant or plate rule:
Evidence/source key:
Can the existing pixels remain?:
Requested disposition:
Editor triage:
Affected gates:
Affected plates and consumers:
Resolution asset or change:
Verification result:
```

Classifications are `factual-pixel`, `visual-pixel`, `composition-pixel`,
`caption-label`, `scale-layout`, `audience-selection`, `rights`,
`insufficient-evidence`, or `out-of-scope`. Severities are:

- **critical:** false identity, wrong ritual relationship, anachronism,
  materially misleading handling, unlicensed incorporation risk, or defect
  that could teach unsafe conduct;
- **major:** missing diagnostic feature, ambiguous confusable, impossible
  construction, wrong scale implication, or unreadable required view;
- **minor:** local tonal, crop, spacing, or caption defect that does not change
  identity or use;
- **suggestion:** optional preference outside the locked requirements.

`Cannot determine` creates an `insufficient-evidence` issue, not a pass. A
reviewer's proposed artistic solution is advisory; the observation and
violated invariant control triage.

## Correction decision

Use the smallest correction class that honestly resolves the defect:

1. **TeX-only correction:** labels, captions, note keys, handling marks, scale
   notices, selection, or plate spacing; preserve artwork bytes and invalidate
   the affected plate and consumers.
2. **Pixel edit:** one localized defect with a complete preservation list;
   create a new artwork ID, preserve the precursor relationship and exact edit
   instruction, and rerun factual and visual review.
3. **Redraw:** identity, silhouette, viewpoint, material construction,
   composition, or multiple interacting defects cannot be safely isolated;
   generate under a new artwork ID from the locked brief.
4. **Evidence hold:** the desired correction is not source-supported; do not
   generate. Amend the inventory or source audit only after verification.
5. **Reject without replacement:** the figure is unnecessary, duplicative, or
   outside the declared corpus; remove its planned consumers transparently.

Never fix a wrong picture by weakening a true caption. Never use an edit to
preserve attractive pixels whose morphology is not independently verified.
Never overwrite the reviewed precursor or reuse its ID.

## Standard correction brief

The owning editor, not the reviewer, converts an accepted pixel issue into:

```text
Correction target: <asset ID and exact file identity>.
Issue being corrected: <one observable defect and location>.
Source-controlled replacement: <exact verified required appearance>.
Change only: <bounded pixel region or relationship>.
Preserve exactly: <identity, silhouette, all approved components, viewpoint,
scale, crop, graphite line, tonal range, lighting, background, ornament, and
every other invariant that must not move>.
Forbidden changes: <specific likely collateral errors plus the universal
no-text, no-color, no-extra-object rules>.
Acceptance test: <observable result that closes the issue>.
```

If this cannot be written without phrases such as `make it more correct`,
`traditional`, `beautiful`, or `liturgically accurate`, the brief is not ready.
Return to the invariant record or select a redraw.

## Verification and closure

The correcting editor first performs a side-by-side invariant audit against
the precursor, then routes the new asset to a reviewer competent for the
invalidated gate. The original reporter need not approve a correction, but
the closure record must answer the original observation exactly.

A correction closes only when:

- the new asset has a new manifest identity and complete provenance;
- every requested invariant changed or remained fixed as specified;
- no collateral factual or visual defect was introduced;
- the issue record names the resolving asset or TeX change;
- invalidated plate and consumer reviews were rerun;
- actual-size and photocopy checks were rerun when diagnostic pixels, scale,
  tonal separation, or placement changed; and
- the superseded or rejected asset has no active consumer.

Batch feedback may be collected in one packet, but each defect remains an
individually closeable issue. Do not mark a round passed merely because a
later candidate looks better overall.

## Review-edition status language

Use only:

- `review edition — artwork review incomplete`;
- `review edition — factual artwork review passed; print review pending`;
- `review edition — correction round open`;
- `review edition — artwork gates passed; publication gates remain`; or
- `release edition` only after every profile and repository gate closes.

Review-edition circulation, reviewer approval, and user authorization to
prepare for publication do not establish ecclesiastical approval, completeness,
release approval, or permission to publish an unreviewed replacement.
