# Processional-cross replacement artwork audit

Audit date: 2026-07-28

## Purpose and source boundary

This audit evaluates a newly generated pencil plate as a possible replacement
for the held legacy raster associated with `obj-processional-cross`. The
checked object record remains controlled by Adrian Fortescue, revised by
J. B. O'Connell, *The Ceremonies of the Roman Rite Described*, seventh
edition (1943), printed p. 17: the processional cross is a **crucifix** fixed
to a long carrying staff that cannot stand alone. Printed pp. 78--79 control
its optional or local use at a priest's High Mass and its appointed stand.
Generated artwork supplies no evidence.

## Built-in generation record

The integrating agent received one output from the OpenAI built-in image
generation tool. The exact model identifier and runtime were not exposed. No
reference image was supplied. The parent-turn prompt intent was:

> one traditional Roman processional cross upright fully visible, plain
> warm-white paper, graphite pencil monochrome museum-catalog study, portrait
> centered no crop, one object/no corpus/no text/no people/no action/no
> dimensions/no heraldry/no ornate fantasy, recognition not ceremonial
> instruction, representative not universal.

The received 1024 x 1536 8-bit RGB PNG is 2,086,679 bytes with SHA-256
`c51202ba8c2d47cc8562fc1497cd1de307fcbc25bbc48e54b6652219a88fc52b`.
It was stripped of ancillary metadata, converted to 8-bit grayscale, and
reduced to 900 x 1350 pixels without a content edit. The normalized asset is
502,015 bytes with SHA-256
`9e62bc3462a773391e6f3a908edb1c174cf2d556c292d97523c5e254ae21d258`.
It is retained non-destructively as
`shared/artwork/pencil/processional-objects/RPD-FIG-processional-objects-0001-iso-processional-cross-v2.png`;
the held legacy raster remains unchanged.

## Visual, print, rights, and safety checks

The normalized plate is a clean, centered, fully visible graphite study of
one tall non-self-standing staff cross. It contains no text, people, action,
dimensions, heraldry, elaborate fantasy ornament, crop, duplicated parts, or
unsafe handling demonstration. At a maximum 3 x 4.5 inch placement it provides
300 effective pixels per inch and remains clear in grayscale.

The output is project-generated without a supplied reference image. Its
prompt, received and normalized identities, transformation, and checks are
recorded here; it is distributed under the repository's project-content
terms.

## Failed factual-identity gate

The prompt expressly excluded a corpus, and the output accordingly depicts a
bare cross rather than a crucifix. That is not a decorative or merely
representative variation: it omits the checked identifying feature in the
canonical source and object claim. The candidate therefore fails the factual
and consumer gates for `obj-processional-cross`.

It remains a held replacement candidate and is not rendered in the five
generated editions. The bespoke altar-server page continues to use the
unchanged legacy raster under its existing qualifications; this audit does
not infer missing custody or rights for that legacy file. A later replacement
must depict one source-bounded crucifix on a long non-self-standing staff.

Even a corrected plate would remain representative rather than universal. It
could not establish material, dimensions, ornament, proportions, one corpus
style, crossbar form, mounting detail, rank, privilege, bearer, route, grip,
stand design, or ceremonial procedure.

## Corrected crucifix-bearing candidate

A second built-in generation corrected the factual defect. Its prompt intent
was:

> single traditional Roman processional crucifix on long staff, entire
> cross/corpus/mount/staff visible, graphite monochrome warm-white paper,
> centered portrait frontal-neutral, no bearer/action/text/INRI/dimensions/
> heraldry/ornate fantasy, representative morphology not universal, avoid
> bare cross and graphic suffering.

The received 1024 x 1536 8-bit RGB PNG is 2,113,633 bytes with SHA-256
`6102ede4d34a31ba39253ad203173a992e7ead3097a16088a62ceea635b647ac`.
It was stripped of ancillary metadata, converted to 8-bit grayscale, and
reduced to 900 x 1350 pixels without a content edit. The normalized asset is
494,461 bytes with SHA-256
`5e19f4e826e3f138433d1a692ce398f5420c6cf1491e13785e48a0f74258302b`
and is retained as
`shared/artwork/pencil/processional-objects/RPD-FIG-processional-objects-0001-iso-processional-cross-v3.png`.

The corrected figure shows one coherent crucifix on one long staff. The
entire cross, restrained corpus, mounting transition, and lower endpoint are
visible. The lower endpoint has no foot or self-standing support. No bearer,
action, text, INRI, dimensions, heraldry, other object, architecture, or
graphic suffering appears. The graphite figure is clear in grayscale at a
maximum 3 x 4.5 inch placement (300 effective pixels per inch), and contains
no handling demonstration or operational instruction. The same
project-generated, no-reference-image rights disposition applies.

The factual, visual, print, rights, safety, and consumer checks therefore
pass. The corrected asset may replace the object record's artwork link and
enter the five generated editions. The bespoke altar-server page deliberately
keeps its existing teaching treatment and legacy raster. The representative
morphology ceiling above remains operative.

## Boundary-safe alpha successor

For enlarged and heterodox page placements, the canonical v3 drawing was
converted non-destructively to a grayscale-plus-alpha PNG. No generative
redrawing, crop, geometric transformation, or alteration of the depicted
crucifix was made. A soft opacity matte was derived from the v3 grayscale field and then refined
deterministically: opacity at or below 20/255 becomes zero, opacity from
20/255 to 40/255 is multiplied by a cubic smoothstep, and opacity at or above
40/255 remains unchanged. This removes the residual paper field while
retaining the substantive graphite and its stronger edge transitions.

The successor is 900 x 1350 pixels, 8-bit grayscale plus alpha, 631,322 bytes,
with SHA-256
`7d19ca898ea49ea5a142a20788dfbc16c826d6f92069d49939e12fef84c41b7b`.
It is retained as
`shared/artwork/pencil/processional-objects/RPD-FIG-processional-objects-0001-iso-processional-cross-v4-alpha.png`.
Its four corners are fully transparent. Review composites against both white
and warm page stock show no rectangular boundary or color fringe, while the
complete crucifix, corpus, mounting transition, shaft, and lower endpoint
remain isolated and legible. At the existing maximum 3 x 4.5 inch placement
it retains 300 effective pixels per inch; enlargement beyond that remains
subject to ordinary print review.

The v3 grayscale drawing remains the provenance-bearing precursor. The v4
file inherits its project-generated, no-reference-image rights disposition
and its factual and representative-morphology ceiling. The alpha derivation
adds no evidence and changes no claim.
