# Validation record — render underlay

Validated on 2026-08-27, against structural baseline `d2e97b5ca`.

## Why this record exists

A web artistic canary failed twice. The second failure is the one that mattered:
the compiled render contract was correct, the deterministic skeleton was
correct, and the generated image still put the Missal on the wrong side of the
altar.

The gap was the visual-conditioning hop. In the diagnostic skeleton the Missal,
burse, chalice and corporal are four identical black squares distinguished only
by adjacent text, and the actors are labelled circles. An image model working
from that has to reconstruct what an open book looks like and then guess which
square was which. It guessed wrongly.

Semantic checks all passed while that was true, which is why this lane treats
**visual inspection as a mandatory gate** rather than an optional courtesy.

## What was inspected, and what was seen

Four underlay rasters were rendered and looked at.

| Scene | What it had to prove | Result |
| --- | --- | --- |
| `LM-001A` | The canary. Open Missal recognizable, on the Epistle/page-right side, and visibly angled rather than square. | **PASS** |
| `LM-033A` | A Gospel-side reading. The same book geometry moves to page-left, at the same angle, without mirroring. | **PASS** |
| `LM-136E` | The second post-ablution crossing. Declared panels only; crossing precedence visible. | **PASS** |
| `LM-099A` | The elevation. Priest, both servers, chasuble geometry, servers reaching to its lower edge. | **PASS** |

All four were re-inspected after the second camera raise; the table records that
pass, not the earlier one. It records a pass against the geometry of that
moment. The sanctuary elevations have since been resolved, the depths resolved
with them, the actor envelopes rebuilt and the camera lowered, and visual
inspection is a gate in this lane rather than a formality: the four rasters are
owed another look before this table can be read as current.

The canary is the exception. `LM-001A` was re-rendered and inspected against
the present geometry as part of the recorded visual review, and
`sanctuary-master.yaml` holds the questions that were answered and the digest
the answers are bound to. That review names its own regression set — `LM-001A`,
`LM-039A`, `LM-009A`, `LM-014A`, `LM-035A`, `LM-061A` — chosen so that a change
of level, a kneeling figure, a figure in profile and a full mensa are each on
screen somewhere, which the four scenes above do not between them cover.

`LM-001A` and `LM-033A` are the load-bearing pair. In the first the open book
stands to the right of the corporal, its two page planes and spine clearly a
book and clearly angled; the burse on the left is a flat closed case that
cannot be mistaken for it. In the second the same book, built from the same
geometry with the same reading yaw, stands to the left. **Placement changes and
orientation does not**, and both facts are visible without reading anything.

`LM-136E` renders exactly the two panels its contract declares, the elevation
and the declared overhead plan, and no others. The plan is where ordered
precedence actually reads: the two acolytes appear at different depths rather
than side by side.

`LM-099A` shows the priest's chasuble falling visibly wider than the servers'
cassocks, with both servers kneeling slightly behind him and reaching toward its
lower edge.

## Mechanical checks

`./validate.py` now additionally proves, for every art-ready scene:

- the underlay exists and parses as XML;
- it contains **no `<text>` and no `<tspan>`** — a label in the conditioning
  drawing would let a renderer read the scene instead of seeing it, which is
  the failure being closed;
- its panel-group count equals the contract's declared panel count;
- every actor's contact patches lie on the tread of the level that actor
  stands on;
- every nave perspective panel holds the authored composition.

The last two are recorded below with their measurements, because a bound is
only worth writing down beside the number it was set against.

`./underlay.py --check` proves the tracked drawings are exactly what the
current contracts generate.

## Feet, and the levels they stand on

The envelopes had feet before they had contact. A sole was drawn at the
elevation the figure was placed on, and nothing asked where in depth it landed,
so a figure could be drawn standing off the front of its own tread and no check
would say so.

Standing, kneeling and genuflecting actors now each carry explicit flat contact
patches — soles; knees and tucked toes; the down knee and the standing foot —
and `check_foot_contact` proves two things about every one of them: that the
patch lies in the plane of its actor's level, and that the patch's centre falls
on that level's own tread rather than on the one below.

Overhang is bounded rather than forbidden, at
`foot_contact.max_overhang_fraction_of_tread` = 0.25, because some of it is
real: altar treads are barely deeper than a foot, and a turned figure does
project past the edge. The fraction is taken **against the tread, not against
the patch**. A knee, a tucked toe and a standing sole are very different sizes,
and a bound written as a fraction of the patch held the smallest of them to the
tightest tolerance for no reason at all.

Over the whole corpus, **1754 soles rest on the level their actor stands on**.
A further **30 belong to actors in transit** and are counted separately rather
than skipped: a walking figure is mid-stride between two levels and is standing
on neither, and a check that quietly dropped them would have a hole in it the
size of every procession in the Mass.

## The composition guards, and the plate that set them

The failing plate that started this measured a step band of 0.69 and an altar
band of 0.20: a flight of stairs with an altar behind it. `check_composition`,
over `panel_composition`, now measures five quantities per panel as fractions
of the drawn subject height — step band, altar band, superstructure band, floor
below the lowest foot, and the tallest actor's height — against thresholds
authored in `sanctuary-master.yaml` under `composition:`.

Measured on the canary `LM-001A` against the current geometry:

| Quantity | Canary | Bound |
| --- | --- | --- |
| step band | 0.279 | at most 0.46 |
| altar band | 0.604 | at least 0.22 |
| superstructure band | 0.351 | at least 0.28 |
| floor below feet | 0.078 | at least 0.06 |
| actor height | 0.596 | at least 0.22 |

The nuance worth recording is that `min_altar_band_fraction` has a great deal
of slack once the elevations are resolved, because the altar body is tall by
construction. Flattening the whole superstructure onto the mensa still passes
it, so on its own it would admit an altar drawn as a slab. What can actually
vanish is the mass **above** the mensa — gradine, tabernacle, reredos, cross
and candlesticks — and that is what makes the shape read as an altar rather
than as a table, so it is measured on its own at
`min_superstructure_band_fraction` = 0.28. Built it comes to 0.35; flattened it
drops to 0.22. The bound sits between the two, which is the only way to know it
fires rather than to assume it does.

**33 in-sanctuary panels are exempt by design and counted.** Their eye already
stands altarward of the first step, so an over-the-shoulder view shows neither
the full step run nor the floor below the servers' feet, and holding it to a
whole-sanctuary proportion would be demanding that the view not be itself.

## A hole in the guard, found by its own regression lane

The page-plane check added with the pitched model decided whether a book was
being carried by asking whether its pitch was zero. That let a contract switch
the check off by zeroing the very number the check existed to police: a Missal
could publish a page normal of straight up, declare no pitch, and pass.

It now asks whether the book declares a support, which is a fact about the
object rather than a number that happens to be zero, and it additionally
compares the normal the contract publishes against the one the drawing
resolves, so the two can no longer disagree in silence. Both lying recipes are
refused; a genuinely carried book is still allowed.

Two smaller things were corrected at the same time. A carried Missal was
publishing the stand's inclination in its pitched vectors while declaring that
it stood on no stand, which was inert only because such books resolve to
actor-held with no position. And the local page-normal note still said an open
book "presents its pages upward", which had become the opposite of true.

## What is tracked, and what is not

The underlay **drawings** are tracked, one per art-ready scene, as vectors. The
**rasters** are not: they are deterministic products, regenerated by `art-seed`
into `build/` when a scene is actually handed to an artist. Tracking a hundred
and forty PNGs would add weight without adding truth, since any of them can be
reproduced byte-for-byte from the tracked SVG.

## The orientation defect, and what it turned out to be

The canary was reported again: the Missal on the correct Epistle side, but
visibly facing the wrong way — square to the nave rather than embodying its
compiled 135 degree yaw.

It was not the transform. Measured at the missal's own geometry, the drawn
page-up direction and the projection of the contract's own page-up vector agree
to within about one degree, and they agreed at every camera height tried,
including the one that failed. The yaw was applied, about the right axis, all
along.

What failed was the projection. The camera sat low enough that the horizontal
plane was seen at a grazing angle, and the book's two principal axes — the
spine running from the reader's near edge to the far edge, and the spread
running across the two pages — projected to within about twenty-two degrees of
collinear. A flat object whose axes collapse toward one line cannot look
oriented at any yaw whatever. The picture was not disobeying the contract; it
was unable to express it.

That distinction matters, because the two failures need opposite fixes. A
wrong-axis transform is fixed in the model. A degenerate projection is fixed in
the camera, and fixing it in the model would mean rotating the book away from
its compiled orientation to make it look right, which is the exact class of
error this whole layer exists to prevent.

Measured separations for the canary's Missal, by camera eye height. The
measurement is `projected_orientation()` in `underlay.py`, run over `LM-001A`
against the current geometry — the mensa at 1.55, the station point at
`y = -5.6`, a 1520 px lens — varying nothing but the eye. The book is measured
twice at each height: as it was modelled then, flat on the mensa, and as it is
modelled now, pitched 24 degrees on its stand.

| Eye height | Flat on the mensa | Pitched on its stand | Fidelity |
| --- | --- | --- | --- |
| 1.52, the current preset | 0.5 degrees | 29.7 degrees | exact |
| 1.85, the previous preset | 4.9 degrees | 34.5 degrees | exact |
| 2.35, the reported failure | 12.9 degrees | 41.4 degrees | exact |
| 3.60, the earlier over-correction | 31.2 degrees | 56.5 degrees | exact |

Fidelity is exact in all eight measurements: 0.00 degrees between the drawn
page-up axis and the projection of the contract's own vector. Only legibility
moves.

The legibility floor is 25 degrees. Read down the flat column and the old
history repeats itself exactly: a flat book fails at every ordinary eye height
and only clears the floor at 3.6, which is how the camera came to be up there.
Read across any row and the same book, pitched, clears the floor at every
height including the lowest. The elevation resolution sharpened this rather
than softening it — with the mensa at 1.55 the current camera looks at the
altar table from very slightly below, so a flat Missal now measures half a
degree, which is not a foreshortened book but a smear. The 24 degree pitch is
the whole of why the book reads, and it is a property of the object.

## Three different questions

The lane above conflated two of these, and a later lane conflated the second
and third. They are separate, and each needs its own evidence.

**Orientation fidelity** asks whether the drawing embodies the compiled
transform. It is a comparison between the drawn axis and the projection of the
contract's own vector, and it was satisfied even when the picture was useless.

**Orientation legibility** asks whether that orientation survives projection.
Two axes of a flat object seen at a grazing angle collapse toward collinear,
and once they do no yaw can look like anything. This is what failed first.

**Physical plausibility** asks whether the object is modelled as the thing it
is. This is what failed next, and it is the one that had been quietly funding
the other two. The Missal had been modelled with its pages horizontal, its
page normal asserted as straight up independently of any transform, and a
purely decorative stand. A real altar Missal rests on an inclined stand and is
pitched toward the priest.

That mattered because the first repair for illegibility was to raise the
camera until a flat book's axes separated — eye 2.35, then 3.6. It worked, and
it was the wrong instrument. The camera was being moved to compensate for the
object.

> A mathematically faithful orientation can still be visually unreadable if the
> physical page plane is modelled incorrectly or the camera grazes it. Fix the
> object first, and only then ask what the camera should mean.

With the book pitched 24 degrees on its stand it is legible from standing eye
height, and the canonical camera returned to a publication nave-front viewpoint
— first at an eye of 1.85, and now at 1.52 and 6.9 from the altar behind a
longer lens. The page normal is now derived from yaw and pitch rather than
asserted, so it points where the priest stands rather than at the ceiling.

A bug surfaced in the measurement itself while this was done: the fidelity
check built its expected direction while dropping the vector's vertical
component. That was invisible for as long as every axis was horizontal, and
reported a spurious 22 degree error the instant pitch existed. It is fixed, and
a regression pins it.

## What now guards it

`validate.py` measures both properties for every oriented object in every
art-ready scene, and refuses on either. A mirrored yaw fails fidelity by 135
degrees. The flat book at the camera at which the defect was reported fails the
legibility floor of 25 degrees — measured against the current geometry it
separates by 12.9. Both refusals were demonstrated before the floor was set, so
the check is known to bite rather than assumed to.

True side elevations are exempt. Collapsing one horizontal axis is what that
view is for, and requiring orientation to survive there would be requiring the
view not to be itself. The two such scenes are counted in the validator's
output rather than quietly skipped, so a scene that comes to need orientation
is known to need another declared panel.

Object-local axes are now explicit data in `underlay-objects.yaml`: a page-up
axis, a spine axis, a spread axis and a page normal, with the open book's spine
declared parallel to page-up because that is how an open book lies. A yaw
applied about the wrong local axis is no longer invisible to a reader of the
library.

## Two objects remodelled, not re-lit

The Missal was not the only object modelled as something it is not. Two more
were found by the same check, and both were fixed in the object.

The **burse** was lying flat on the altar cloth. Measured that way it projected
**2.9 degrees from collinear** at a nave eye, and the legibility check did what
it is built to do and advised raising the camera — the move this layer forbids,
and the exact instrument that produced the 2.35 and 3.60 raises. From a
standing eye the mensa is very nearly edge-on, and a flat square lying on it
genuinely cannot be seen; the camera was not the fault. A burse is a stiff
square case, and on the mensa it stands upright against the gradine. It now
declares `support.pitch_deg: 78.0`, and the picture shows what it is.

A defect in the measurement surfaced with it. `projected_orientation()` built
its expected direction from the yaw alone whenever an object published no
pitched vector, so the drawing applied the declared support pitch and the
expectation did not — the fidelity comparison was between a pitched drawing and
an unpitched expectation, and it silently exempted every pitched object that
publishes no vector of its own. The expectation is now built from the yaw
**and** the declared support pitch.

The **paten** went the other way. Lying flat on the linen it is a plain disc
with no readable page-up in the picture, because it has none in the room: turn
it on the corporal and nothing about it looks different. The legibility floor
exists to catch an orientation the drawing fails to communicate, and here there
is no orientation to communicate. It is exempted by
`legibility.exempt_when_flat` in `underlay-objects.yaml`, and the exemption is
narrow on purpose:

- it never applies to fidelity, which is enforced as for everything else;
- it dies the moment the disc is pitched or picked up;
- held under the chin at the Communion the same paten measures **90 degrees**
  of separation, so the check still has teeth on the object that took the
  exemption;
- **72 flat unpitched objects** take it, and the count is printed, so an
  exemption can never be silent.

## The gate a machine cannot pass for you

Every automated check in this layer passed while the picture was wrong. The
composition thresholds close part of that gap, but a threshold only refuses the
failures somebody already thought of, so the publication composition is also
gated on someone having looked.

`sanctuary-master.yaml` records the review under `underlay_visual_review:`: the
status, the canary `LM-001A`, the preset, and a digest over the five files
that decide what the picture looks like — `sanctuary-master.yaml`,
`camera-model.yaml`, `underlay.py`, `underlay-objects.yaml` and `_contract.py`.
The object library and the compiler are in the digest because the first decides
what the furniture is shaped like and the second decides where the actors
stand. The recorded digest line is excluded
from its own input, or refreshing it would always invalidate it.
`require_visual_review()` in `scripts/_pictographic.py` makes `art-seed` refuse
**both** an unapproved preset and an approval whose geometry has since moved;
`tools/pictographic composition-review roman-1962 low-mass [--refresh]` reports
and refreshes it.

It was verified in both directions before being relied on: with the digest
stale, `art-seed` refused and wrote nothing; with the review recorded, the same
scene seeded. A gate demonstrated only in the passing direction is not known to
be a gate.

## What a close camera showed, and the near plane

The composition guards measure nave panels and exempt the thirty-three shot
from inside the sanctuary, because a view whose eye already stands on the
predella shows neither the full step run nor the floor under the servers' feet.
Exempt is not the same as unexamined, and rendering one of them found it
broken: `LM-016B`, the priest bowing low over the altar, drew two enormous
diverging funnels and almost nothing else.

The cause was not the station point. `Camera.project` clamped depth to a floor
rather than clipping, so a point a few centimetres in front of the eye did not
disappear, it projected to an enormous coordinate; the fit then zoomed out to
contain it and everything real collapsed to a speck. From the nave nothing is
ever that close, which is why the fault had never appeared. Parts with any
point nearer than `Camera.near` are now out of shot, which is what a close view
does in life as well.

Two further things surfaced with it, and both are recorded here because they
are the same kind of error as the ones this document already catalogues. The
preset carried no focal length of its own, so it inherited the publication
lens, which at that range magnified the altar far past the plate; a preset now
owns its lens. And its station point had been authored against the unresolved
depths, where the priest at the predella stood at 1.5 rather than 1.29. Moved
back for room it lands among the kneeling servers; dropped to the priest's own
head height the near-plane cull removes the figure the view exists to show. It
sits at `[0.0, 0.72, 2.62]` behind and above him, which is the only band that
satisfies both.

## The calibration sheet

`camera-calibration.py` writes `review/camera-calibration-v1.svg`: six
candidate cameras drawn against the same scene and the same sanctuary, with the
published one boxed. The rejected raises to 2.35 and 3.60 are on the sheet on
purpose, because the argument against moving a camera to rescue an object is
much easier to make when the raised camera is beside the published one. The
cells are drawn and styled by `underlay.py`, so the sheet cannot come to
disagree with the plate.

It is a **debug artifact**: never a panel, never part of an art-seed package,
never shown to an artistic agent. Like the other generators it has a `--check`
mode, so a sheet that no longer matches its inputs is a failure rather than a
stale picture.

## The camera changes, recorded

`nave-centre` was raised twice and then lowered twice, and the shape of that
history is the argument.

It was raised from a 1.6 standing eye to 2.35, because from standing height the
mensa was edge-on and everything resting on it foreshortened to nothing. Then
from 2.35 to 3.6, because 2.35 made the surface visible without making
orientation within it legible. Both raises were the same mistake: the Missal
was modelled flat, and the viewpoint was being moved to compensate for the
object. Pitching the book on its stand made both raises unnecessary, and the
eye came back down to 1.85.

It was lowered again, to `[0.0, -5.6, 1.52]` with `focal_length_px: 1520`, when
the sanctuary elevations were resolved. The preset now stands 6.9 from the
altar and reads at 1.61 m equivalent — a standing worshipper's eye, further
back behind a longer lens. The targets moved with the elevations they name:
`altar-centre` to `[0.0, 1.35, 1.42]`, `mensa-centre` to `[0.0, 1.5, 1.55]`,
`foot-of-altar` to `[0.0, 0.0, 0.95]`, `sanctuary-floor` to `[0.0, 0.64, 0.0]`.

That last move is not the forbidden one, and the distinction is worth stating
because the two look alike from a distance. A camera expresses a viewpoint, and
must never be moved to rescue geometry that is modelled inadequately; that is
exactly what the two raises did. This change lowers the eye toward what a
worshipper actually sees and pulls it back behind a longer lens. It climbs
nowhere and rescues nothing. What was repaired was the model: the level
elevations in `sanctuary-master.yaml`, the actor envelopes, and the altar's own
mass. The plate convention for this dictionary is therefore a standing nave
view, close to eye level, with the figures against the steps.

This is a render-contract change, not a choreography change. No structural
value moved, and `structural/low-mass/v0.21` is untouched.

## The figure envelopes, and what they are for

The envelopes were flat cut-outs, one outline apiece. That is a solid only from
the side it was drawn for: an actor facing along the view axis vanished to a
vertical spike, which is not a coarse figure but no figure at all.

They now carry two outlines a body depth apart, tied together so the pair reads
as one mass; a head built in two planes; a cincture; a hem; feet with soles
resting on the level the figure stands on; and a chasuble for the priest. The
altar was thin in the same way, and for the same reason — its cross and four
candlesticks were not drawn, so the modelled mass read as a cupboard on a slab.
Both are now in the geometry, anchored in `sanctuary-master.yaml`.

They remain blocking envelopes and not anatomy: enough to show where three
people stand, which way each faces, and who is kneeling, which is what blocking
geometry owes an artist. Kneeling and walking figures are still the weakest of
them. An artist editing the underlay is expected to render real bodies inside
those envelopes; what may not move is where the envelope stands and which way
it faces.

## The crop, and what set its scale

The auto-fit framed every panel around the widest thing in it, which was the
in-plano floor — the emptiest element in the drawing was choosing the scale of
the subject, and shrinking it. The fit now composes around the subject, the
altar and the actors, and lets the floor run past the frame. What the result
must hold is written as numbers in `sanctuary-master.yaml` under `composition:`
— the share of frame height the step band may take, the share the altar must
take, the floor visible below the feet, and the height an actor must reach — so
a later change to the composition has to argue with a threshold rather than
with a preference.
