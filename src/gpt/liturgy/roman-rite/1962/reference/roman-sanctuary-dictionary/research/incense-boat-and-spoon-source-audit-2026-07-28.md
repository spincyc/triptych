# Incense boat and spoon source audit

## Dictionary identity

The boat and spoon retain their distinct source terms and functions but form
one subordinate functional-set entry for publication. They are prepared,
stored, presented, and understood together; separate dictionary cells would
repeat the same combined artwork without improving recognition.

## Evidence boundary

The exact 1962 *Missale Romanum*, *Ritus servandus* IV.4 and VII.10,
names the *navicula* and *cochlear* in IV.4 and assigns the deacon to minister
the boat to the celebrant; VII.10 repeats the deacon's service of the boat at
the Offertory without repeating the spoon term.
Those rubrics establish identity and the named clerical relationship, not
material, dimensions, decorative morphology, or a universal lay-server
handoff.

Met object 236950 is a directly checked material-culture exemplar: an English
silver incense boat and spoon dated 1708–9. The catalog gives lengths of
10.2 cm for the boat and 8.9 cm for the spoon. Its Open Access image shows a
lidded boat-form container and a separate spoon at one photographic scale.
It remains an exemplar rather than a Roman norm.

Loose incense is treated as consumable material, not a third vessel. No claim
about resin species, mixture, grain size, color, or composition is made.

## Artwork disposition

The older candidate drawing showed large granular contents whose composition
and morphology were unsupported. A project-owned generated edit removed only
those contents and retained the open boat, hinged lid, foot, separate spoon,
white ground, and graphite treatment. The resulting asset contains no text,
fire, charcoal, smoke, thurible, or operational action. Its decorative details
remain explicitly illustrative.

Generation prompt, built-in image edit, 2026-07-28:

> Remove only the loose granular incense contents from the open boat so the
> interior is completely empty and clean; preserve the boat, lid, foot,
> perspective, separate spoon, white background, framing, and monochrome
> graphite treatment; add no text, smoke, charcoal, fire, or watermark.

The exact prompt for the precursor generation was not durably preserved and
is not reconstructed here. The edit was made with OpenAI's built-in image
generation tool; the exact model identifier and runtime were not exposed.
No third-party reference image was supplied or identified for this edit. The
project-generated precursor is retained as a held asset at SHA-256
`98af7c63f0930855a8d65ca32fd5cb9d064b79c5abd2853882290d8870e6c421`.
The edited raster is distributed under the repository's project-content
terms; this record does not claim rights in the independently cited Met
catalog image, which served as evidence rather than transferred image input.

Normalized publication asset:
`RPD-FIG-incense-0003-empty-boat-spoon.png`, 1536 × 1024, 8-bit grayscale,
SHA-256 `af98d030c708eccefb623e37d5e8c4602e67ec0811ef2b2b6865f9ad3e206c3a`.

## Boundary-safe alpha successor

For enlarged and heterodox page placements, the normalized drawing was
converted non-destructively to an 8-bit grayscale-plus-alpha PNG. No
generative redrawing, crop, geometric transformation, or alteration of the
boat-and-spoon set was made. A soft opacity matte was derived from the
grayscale field and then refined deterministically: opacity at or below
20/255 becomes zero, opacity from 20/255 to 40/255 is multiplied by a cubic
smoothstep, and opacity at or above 40/255 remains unchanged.

The successor is 1536 × 1024 pixels and 932,863 bytes, with SHA-256
`4ab621886229f88044a53950491be555f29cf11bc6d9f4f2acdb0a2d49899bbe`.
It is retained as
`RPD-FIG-incense-0003-empty-boat-spoon-v2-alpha.png`. All four corners are
fully transparent. A zero-error color-channel comparison confirms that
the predecessor.s drawing channel is unchanged; only opacity was refined. Review composites against
white and warm page stock show no rectangular boundary or color fringe; the
open boat, hinged lid, foot, empty interior, and separate spoon remain
complete and legible as one functional set.

The grayscale predecessor remains the provenance-bearing source. The alpha
successor inherits its project-created rights disposition, evidence boundary,
functional-set treatment, and illustrative-morphology ceiling. The matte
derivation adds no evidence and changes no claim.
