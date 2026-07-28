# Conopaeum and ombrellino taxonomy and artwork audit

Audit date: 2026-07-28

## Corrected identity boundary

The former `obj-ombrellino` candidate combined two objects whose similar
umbrella silhouettes do not establish a common identity:

- `obj-basilical-conopaeum` is an institutional basilical insigne. The
  official acts checked below associate the *conopaeum* (also spelled
  *conopeum* or *canopaeum*, and often called a basilical *umbraculum* or
  *ombrellino*) with the *tintinnabulum* in granted basilical privileges.
  This does not make it a generic Mass implement, Eucharistic canopy, or
  pontifical insigne.
- `obj-ombrellino` now means only the small Eucharistic *umbella* or
  ombrellino. The Roman Ritual places an umbrella or baldachin over the priest
  in the where-available public Communion or Viaticum route. The small
  one-staff form remains distinct from both the larger baldachin and the
  basilical conopaeum.

The legacy fully opened generic plate remains byte-for-byte at
`shared/artwork/pencil/processional-objects/RPD-FIG-related-ceremonies-0003-open-ombrellino.png`.
It is now rejected for consumer use because its silhouette cannot resolve the
two identities. No legacy pixel, prompt, or runtime fact was reconstructed.

## Checked research paths

The institutional identity and privilege were checked against:

1. Benedict XV, *Molis amplitudine*, 19 August 1918, AAS 10 (1918),
   pp. 475-477, especially the official Vatican text's privilege paragraph:
   <https://www.vatican.va/content/benedict-xv/la/apost_letters/documents/hf_ben-xv_apl_19180819_molis-amplitudine.html>.
2. Pius XI's 1924 Marija Bistrica minor-basilica act, AAS 16 (1924),
   pp. 33-34:
   <https://www.vatican.va/archive/aas/documents/AAS-16-1924-ocr.pdf>.
3. Two 1962 basilica-privilege examples, AAS 54 (1962), pp. 844-846:
   <https://www.vatican.va/archive/aas/documents/AAS-54-1962-ocr.pdf>.
4. The Macalisang thesis, pp. 43-44, only as a historical secondary
   morphology control and lead to the cited 1836 decree. It does not control
   institutional status or make one material form universal.

The Eucharistic identity and use were checked against:

1. *Rituale Romanum*, Titulus IV, caput IV, nn. 10-13, remote PDF
   pp. 70-71:
   <https://www.liturgia.it/content/ritrom.pdf>.
2. The 1908 *Catholic Encyclopedia* article “Baldachinum of the Altar,” only
   as a historical secondary distinction between the small, flat,
   single-staff Eucharistic ombrellino and the larger rectangular baldachin:
   <https://www.newadvent.org/cathen/03297c.htm>.

The official acts and ritual control status, scope, and ceremonial relation.
The secondary witnesses control only the bounded recognition distinctions
stated in the object records. Generated images supply no evidence.

## New basilical conopaeum plate

The OpenAI built-in image generation tool was used through the image-generation
skill without a supplied reference image. Its exact model identifier and
runtime were not exposed. The exact prompt was:

> Use case: scientific-educational
> Asset type: source-controlled pictorial-dictionary plate for a Roman
> Catholic basilical-insignia reference
> Primary request: Create a restrained graphite pencil recognition study of
> one basilical conopaeum (umbraculum), shown as a partially opened conical
> canopy on a single long carrying pole.
> Scene/backdrop: plain warm-white paper, no environment or floor plane
> Subject: one institutional basilical conopaeum only; half-open/partially
> opened conical canopy with alternating fabric panels conveyed by differing
> graphite hatch densities, single pole, modest ball-and-cross finial;
> historically plausible traditional Roman Catholic form
> Style/medium: careful monochrome graphite pencil, subtle paper grain, clean
> museum-catalog object study, not photorealistic
> Composition/framing: portrait orientation, entire canopy, finial, pole, and
> foot visible, centered, generous margins, no crop
> Lighting/mood: neutral even illumination
> Constraints: no people, Eucharist, procession, church interior, text,
> labels, letters, coat of arms, ribbons, gold/silver ornament, dimensions,
> carrying posture, watermark, frame, or claim of universal morphology;
> object recognition only; one object
> Avoid: ordinary rain umbrella, fully open beach parasol, flat Eucharistic
> ombrellino, papal tiara, decorative fantasy, color, black fill, gradient
> background

The received 1024 x 1536 RGB PNG is 2,269,487 bytes with SHA-256
`95c75923f04fb5c278b8f83633105bad11f6694b1a5ee4b7fb1f9b0ba5c58409`.
The generated original remains intact outside the repository. A copied
working asset was stripped of ancillary metadata, converted to 8-bit
grayscale, and reduced to 900 x 1350 pixels without a content edit. The
normalized source-controlled asset is 544,491 bytes with SHA-256
`2bc2433289c6fc6d119354c61c53ae800f10405a3dd711fa262d5ff8d5db51bc`.

The complete staff, foot, partially opened conical canopy, alternating
graphite panels, and ball-and-cross finial are visible. No person, Eucharist,
procession, church, text, label, letter, arms, ribbon, gold or silver
ornament, dimensions, carrying posture, other object, crop, duplication,
color, watermark, frame, or gradient appears.

The plate is representative. It cannot establish universal color, fabric,
panel count, fringe, finial, arms, dimensions, construction, ornament, staff
form, or opening state.

## New Eucharistic ombrellino plate

The same built-in generation mode and no-reference-image condition apply. The
exact prompt was:

> Use case: scientific-educational
> Asset type: source-controlled pictorial-dictionary plate for a Roman
> Catholic liturgical-object reference
> Primary request: Create a restrained graphite pencil recognition study of
> one Eucharistic ombrellino (small processional umbrella or umbella), shown
> as a compact, shallow, nearly flat circular canopy on one long single
> carrying staff.
> Scene/backdrop: plain warm-white paper, no environment or floor plane
> Subject: one Eucharistic ombrellino only; small shallow flat canopy, modest
> fringe, long central single pole and simple foot; alternating very light
> graphite hatch values may suggest traditional white or cloth-of-gold fabric
> without asserting color
> Style/medium: careful monochrome graphite pencil, subtle paper grain, clean
> museum-catalog object study, not photorealistic
> Composition/framing: portrait orientation, entire canopy, staff, and foot
> visible, centered, generous margins, no crop
> Lighting/mood: neutral even illumination
> Constraints: no people, Eucharist, monstrance, pyx, procession, church
> interior, text, labels, letters, coat of arms, cross finial, red-yellow
> alternating panels, dimensions, carrying posture, watermark, frame, or
> claim of universal morphology; object recognition only; one object
> Avoid: tall conical basilical conopaeum, half-open basilical insignia,
> ordinary rain umbrella, beach parasol, fully domed canopy, papal tiara,
> decorative fantasy, color, black fill, gradient background

The received 1024 x 1536 RGB PNG is 2,160,847 bytes with SHA-256
`68ece54fb10b6553a1edf017377a028024176026cbfa5a0a3dd3c31f6acef9d8`.
The generated original remains intact outside the repository. The normalized
900 x 1350 8-bit grayscale asset is 517,708 bytes with SHA-256
`bcdffc7d0ae4677ab7490fc2a25e727df8fbc0b2947c50bccd57bff8f6d4ceca`.

The complete shallow canopy, modest fringe, central long staff, and foot are
visible. No person, Eucharist, monstrance, pyx, procession, church, text,
label, letter, arms, cross finial, dimensions, carrying posture, other
object, crop, duplication, color, watermark, frame, or gradient appears.

The plate is representative. It cannot establish universal fabric, color,
panel pattern, fringe, dimensions, staff, foot, ornament, or construction.

## Audience routing and checks

The comprehensive and general-reader editions admit both records. The
sacristan and MC/trainer editions admit them as conditional preparation and
branch-recognition records. The pontifical edition receives cross-reference
context only and is told that neither object is pontifical insignia. The
ordinary altar-server route excludes the basilical conopaeum; it admits the
Eucharistic ombrellino only for a specifically appointed public Communion,
Viaticum, or transfer context.

Both normalized plates pass factual, visual, monochrome, crop, rights, safety,
consumer, and release checks at a maximum 3 x 4.5 inch placement, providing
300 effective pixels per inch. TeX retains the identity, scope, privilege,
where-available branch, confusable distinctions, morphology ceilings,
audience notes, source keys, and scale qualification.
