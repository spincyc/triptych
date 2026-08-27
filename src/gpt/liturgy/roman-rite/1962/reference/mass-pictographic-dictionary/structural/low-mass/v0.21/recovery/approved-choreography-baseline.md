# Approved choreography baseline — spoken 1962 Roman Low Mass, two servers

Provenance: this file preserves, verbatim, the human-approved structural
decisions supplied with the recovery task that completed the detailed scene
corpus for checkpoint v0.21. It is a **durable record of approved directives**,
not new rubrical research and not a rubrics textbook.

Authority: this document and
[`../handoff/HANDOFF-SUMMARY.md`](../handoff/HANDOFF-SUMMARY.md) together are
the source of truth for the recovered scene corpus under
[`../scenes/`](../scenes/). Where the two speak to the same point they agree;
where this document is more detailed, it refines rather than overrides.

**Not a source of truth:** the older sibling `altar-server-guides/` tree. It
predates this checkpoint, contains superseded choices, and must never be used
to reconstruct choreography for this lane. See
[`recovery-notes.md`](recovery-notes.md).

Only the choreography and invariant sections of the approved record are
reproduced. Task-process sections (git discipline, validation mechanics,
reporting format) are deliberately omitted: they governed the recovery run, not
the corpus. Section numbers below are those of the approved record.

---

# 5. Global spatial invariants

These were explicitly approved and must be encoded structurally, not left to artistic interpretation.

## Sanctuary orientation

In a canonical nave-facing-the-altar view:

- **Gospel side = viewer left**
- **Epistle side = viewer right**

Use dimensionless/synthetic scene coordinates if coordinates are stored. Do not pretend they are physical meters.

The altar is a fixed traditional high altar with:

- **three full altar steps**
- **predella**

Secondary views may move or crop the camera but must not alter world-space side assignments or object orientations.

A true side orthographic view collapses actors with the same depth. Never move side-by-side actors into artificial front/back positions merely to make them visible.

## Missal orientation

**Missal placement side and reading orientation are independent.**

Wherever the Missal is placed, including on the Gospel side, orient it so that **when the priest reads it he is turned toward the left**.

Do not mirror the Missal simply because it moves from Epistle to Gospel side.

## Server identities

- **Acolyte 1 (AC1) = Epistle-side acolyte**
- **Acolyte 2 (AC2) = Gospel-side acolyte**

Do not model one permanent “book server.” Missal-transfer responsibility is phase-specific.

- **Pre-Gospel transfer:** AC1 moves the Missal Epistle → Gospel.
- **Post-ablution transfer:** AC2 moves the Missal Gospel → Epistle.

---


# 7. Approved scene-by-scene choreography to recover

The historical numbering evolved during review. Preserve existing committed IDs where they already exist. For missing early material, use the established LM numbering below and do not renumber existing canonical late scenes merely for aesthetics.

The exact goal is **complete deterministic coverage**, not artificial numeric neatness.

## A. Prayers at the Foot of the Altar

The Missal has already been **placed on the Epistle side and OPENED before the priest descends** for the Prayers at the Foot.

During these prayers:

- priest + both servers form a **side-to-side line**
- all have the same front/back depth
- all are **below the altar steps**

### Priest's Confiteor

- priest makes a **profound body bow**
- servers remain kneeling

### Servers' response to the priest's Confiteor

- servers' heads are **slightly bowed**
- heads turn **inward toward the priest**

### Servers' own Confiteor

- heads turn inward at **`et tibi pater`** and **`et te pater`**
- heads remain bowed
- each server strikes the breast with the right hand at each of the three **`mea culpa`** phrases

### After servers' Confiteor

At **Misereatur**:

- priest stands upright
- servers remain bowed until `Amen`

At **Indulgentiam**:

- servers become erect
- **priest and both servers all make the sign of the cross**

### Deus, tu conversus through Oremus

- priest uses a **medium body bow**
- servers are bowed

---

# 8. Ascent and Oramus te

The ascent assistance baseline is:

- **only AC1 / Epistle-side acolyte assists**
- AC1 briefly lifts the **front/lower hem of the priest's alb** during ascent
- AC2 does not touch the vestment
- do not model both servers assisting

The approved transition was split conceptually as:

- Oremus completion / rise
- ascent on centerline with AC1 assistance
- servers establish their positions after the ascent

## Oramus te

At center/predella:

- priest makes a **medium body bow**
- joined hands are at the mensa edge
- little-finger tips are at the edge
- third fingers are on the mensa

After **`Sanctorum tuorum`**:

- both hands go onto the altar **outside the corporal**
- priest bends low and kisses the altar

Then:

- priest stands erect
- rejoins hands
- moves squarely to the Epistle-side Missal
- do not depict a sideways shuffle

---

# 9. Introit / Kyrie / Gloria / Collect

## Introit

At the Epistle-side Missal:

- priest signs himself at the beginning
- left hand rests on breast during the sign
- both servers also sign themselves in the ordinary spoken Low Mass baseline

## Introit doxology

Label it explicitly as:

**`Introit doxology — Gloria Patri`**

Never call this simply `Gloria`.

- priest remains at the Missal
- bows toward the cross
- does not move his feet

## Kyrie

- priest returns to center first
- Kyrie begins only after he reaches center
- servers remain kneeling

## Gloria in excelsis

When prescribed:

- priest is **standing at the center of the altar**
- opening gesture: extend hands → elevate → rejoin
- bow at `Deo`
- servers remain kneeling

Use the naming invariant:

- unqualified `Gloria` = **Gloria in excelsis**
- `Gloria Patri` must always be explicitly identified as a doxology

During the Gloria:

- priest makes the prescribed profound head bows at the relevant phrases
- feet remain fixed at center
- hands joined except where rubrics require otherwise
- servers bow correspondingly while kneeling

At **`Cum Sancto Spiritu ... Amen`**:

- priest and **both servers make the sign of the cross**

## Gloria → Collect transition

After Gloria:

1. priest places hands on altar outside corporal
2. kisses altar
3. stands erect / rejoins hands
4. turns **right / toward Epistle side** to face people
5. at `Dominus vobiscum`, eyes downcast; separates hands without elevating; rejoins while saying it
6. turns **left back to altar**
7. returns to Epistle-side Missal
8. at `Oremus`: separate/rejoin hands + profound head bow toward cross
9. hands extended for Collect

Missal remains open on Epistle side.

---

# 10. Epistle → Gospel

## Epistle

- priest at open Epistle-side Missal
- both hands on Missal while reading
- server response: `Deo gratias`

The priest may signal the transfer with left hand on altar; keep customs/profile detail separate if exact cue is not universal.

## Missal transfer before Gospel

This is a locked role correction:

- **AC1 / Epistle-side acolyte** stages for and performs the transfer
- **AC2 does not handle the Missal**
- AC1 carries the open Missal **Epistle → Gospel**
- preserve the left-reading orientation
- if center genuflection is modeled, preserve the approved path and orientation

## Munda cor meum

At center:

- priest first raises eyes to cross
- lowers eyes
- makes profound body bow
- hands joined and **not resting on the altar**
- says `Munda cor meum`, `Jube Domine`, `Dominus sit in corde meo`

Then move to Gospel-side Missal.

At Gospel-side Missal:

- priest stands diagonally to altar
- Missal remains in left-reading orientation
- `Dominus vobiscum`

---

# 11. Gospel proclamation

## Opening signs

Missal:

- open on Gospel side
- reading orientation remains left

Priest sequence:

1. left hand open on Missal
2. right thumb signs first word of Gospel text at `Sequentia`
3. left hand moves to breast
4. right thumb signs forehead at `sancti Evangelii`
5. signs lips
6. signs breast above left hand at `secundum N.`
7. rejoins hands

Servers:

- stand facing Gospel
- left hand flat on breast
- each makes three small crosses: forehead, lips, breast
- response: `Gloria tibi, Domine`

## Gospel reading

- priest reads with hands joined
- required bows, including at the Holy Name, are toward the Missal unless Blessed Sacrament exposed variant applies
- servers stand facing Gospel and bow at required cues

AC1 may remain briefly after placement before returning to his ordinary Epistle-side position. Exact return cue was intentionally left as a serving-profile parameter rather than hard-coded.

## Gospel conclusion

- servers respond `Laus tibi, Christe`
- priest takes Missal off stand with **both hands**
- lifts it
- stoops and kisses the **beginning/first word of the Gospel text** while saying `Per evangelica dicta`
- replaces it while saying `deleantur nostra delicta`
- moves Missal + stand toward center, just left of corporal
- hands joined, returns to center

Requiem variant:

- omit book kiss
- omit `Per evangelica dicta`

Branch:

- Credo if prescribed
- otherwise directly to Offertory transition

---

# 12. Credo branch

When Credo is prescribed:

## Opening

At center:

- extend hands
- elevate hands
- rejoin
- lower joined hands to breast
- profound head bow to cross at `Deum`

Servers remain kneeling and make slight bow at `Deum`.

## `Jesum Christum`

- priest: profound head bow toward cross
- servers: slight bow
- no actor changes position

## Incarnation

After `descendit de caelis` through `Et homo factus est`:

Priest:

- place both hands on mensa
- genuflect
- remain genuflected through `Et homo factus est`
- rise
- rejoin hands

Servers:

- remain kneeling
- make a **moderate bow**
- do not attempt a second genuflection while already kneeling

## `simul adoratur`

- priest: profound head bow
- servers: slight bow

## `Et vitam venturi saeculi. Amen.`

- priest + AC1 + AC2 all make the sign of the cross

No-Credo branch skips this cluster entirely.

---

# 13. Convergence into Offertory

Both Credo and no-Credo branches converge at center:

1. priest places both hands on altar outside corporal
2. kisses altar
3. stands erect
4. joins hands
5. turns right to people
6. separates hands without elevating for `Dominus vobiscum`
7. rejoins
8. turns left back to altar

Then:

- `Oremus`: separate/rejoin + profound head bow toward cross
- read Offertory antiphon with hands joined

---

# 14. Offertory entry object state

This was a major correction.

The **corporal is already unfolded from the beginning of Mass**. Do not depict the priest unfolding it at the Offertory.

At Offertory entry:

- corporal: unfolded at center
- burse: empty on Gospel side
- Missal: near center/left of corporal after Gospel
- veiled chalice stack: center on corporal
- purificator over chalice cup
- paten with Host above purificator
- pall above paten
- chalice empty

---

# 15. Offertory preparation

## Remove chalice veil

Priest:

- removes chalice veil with both hands
- hands veil to AC1

AC1:

- rises
- approaches Epistle side
- receives veil
- folds it
- places folded veil near Epistle-side Lavabo card / equivalent approved location

AC2:

- rises
- goes to center below steps
- genuflects
- proceeds to credence

## Dismantle chalice stack

Priest:

- left hand on altar outside corporal
- right hand moves chalice stack off corporal to Epistle side at arm's length
- left hand remains on altar
- right hand removes pall
- pall placed against Epistle altar card
- takes paten with Host in both hands
- brings it over corporal

## Offering of Host — `Suscipe, sancte Pater`

- raise eyes to cross
- lower immediately
- hold paten at breast height
- look at Host
- recite prayer
- lower paten just above corporal
- make horizontal sign of cross with paten over destination
- tilt paten
- slide Host onto front-center fold of corporal
- Host is not touched directly by fingers during slide
- place paten halfway under right edge of corporal

## Wine and water cruets

Canonical two-server role split:

- AC1 presents **wine**
- AC2 presents **water**
- wine first, water second
- both from Epistle side
- each kisses cruet before presentation and after receiving it back
- present with right hand, handle toward priest
- receive back with left hand

## Prepare chalice

At Epistle side:

- right hand on altar
- left hand draws chalice toward priest
- priest purifies cup once with purificator
- remove purificator
- left thumb holds purificator at node
- receive wine from AC1, pour wine
- return wine
- bless water with right hand
- receive water from AC2, add small amount
- return water
- wipe drops from rim with purificator
- set chalice toward center
- join hands
- bow at `Jesus Christus`
- return center

Requiem:

- omit water blessing
- still say `Deus, qui humanae substantiae...`

---

# 16. Chalice offering → Lavabo

## `Offerimus tibi`

- lay purificator on exposed half of paten, open ends toward back
- take chalice at node with right hand
- support base with left fingers/thumb as approved
- raise chalice to **eye height**
- priest looks at cross during entire prayer
- lower just above corporal
- make horizontal sign of cross with chalice
- set chalice on back-center fold of corporal
- steady base with left hand
- cover with pall using right hand

## `In spiritu humilitatis`

- medium body bow for entire prayer
- hands joined on mensa edge
- chalice remains covered

## `Veni sanctificator`

- stand erect
- separate hands
- elevate hands
- join
- lower
- raise eyes to cross, lower immediately
- left hand on altar outside corporal
- right hand makes Greek cross over Host + chalice together
- rejoin hands
- move to Epistle side for Lavabo

## Lavabo — original service-role structural baseline before later ablution correction

Do not confuse the **Offertory Lavabo** with the **post-Communion ablutions**.

At the Offertory Lavabo:

- AC1 = towel
- AC2 = water cruet + lavabo dish
- both approach Epistle side
- priest washes only tips of thumbs and forefingers
- priest receives towel, turns toward altar while drying, refolds/returns towel
- after returning towel, joins hands
- bow toward cross at `Gloria Patri`
- begin return center at `Sicut erat`

Servers return items to credence, meet at center, genuflect together, and resume kneeling positions.

Requiem / Passiontide variant for Lavabo psalm doxology must remain represented as a branch/profile rule.

---

# 17. Suscipe sancta Trinitas → Orate fratres → Secrets

## `Suscipe, sancta Trinitas`

- raise eyes to cross then lower
- medium body bow
- joined hands on altar edge
- low voice throughout

## Altar kiss

- both hands palm-down on altar
- outside corporal
- kiss altar
- stand erect
- join hands

## `Orate, fratres`

- turn right to face people
- eyes downcast
- while facing people separate hands
- rejoin while saying `Orate, fratres`
- only `Orate, fratres` is loud
- remainder in low voice
- continue turning right
- complete full circle back to altar
- do not linger facing people

## Servers' `Suscipiat`

Canonical baseline:

- begin only after priest fully faces altar again
- both servers kneeling erect
- hands joined
- **no bow**
- both respond together

Priest answers `Amen` in low voice.

## Secrets

- no `Oremus`
- priest extends/joins as before Collects
- extends hands again
- reads Secret prayer(s) in low voice

---

# 18. Last Secret → Preface → Sanctus → opening Canon

## Preface dialogue

After last Secret:

- `Per omnia saecula saeculorum` aloud
- `Dominus vobiscum` aloud
- `Sursum corda`: raise hands to breast height
- `Gratias agamus`: join hands
- `Deo nostro`: raise eyes to cross then bow head
- after server response `Dignum et justum est`, extend hands for Preface

Servers remain kneeling, make responses, and bow with priest at `Deo nostro`.

## Sanctus / Benedictus

Priest:

- finish Preface
- join hands
- medium body bow for Sanctus
- hands joined before breast, **not on altar**
- stand erect at Benedictus
- make sign of cross on himself through conclusion

AC1:

- bows
- rings at each `Sanctus` in the established Sanctus profile

AC2:

- bows

## Enter Canon / Te igitur

After Benedictus:

- right hand on altar
- left hand turns to Canon
- join hands
- separate/elevate
- join/lower
- eyes to cross then lower
- profound body bow
- joined hands on altar edge
- begin `Te igitur` in low voice

Remain bowed through `supplices rogamus ac petimus`, then:

- hands outside corporal
- altar kiss
- stand erect
- join hands
- left hand on altar
- three crosses over Host + chalice at `haec dona`, `haec munera`, `haec sancta sacrificia illibata`

## Memento of living / Communicantes

At `Memento, Domine`:

- join and raise hands toward face/breast
- head slightly inclined
- silent commemoration
- extend hands again

Communicantes:

- bow at `Jesu Christe`
- join hands at `Per eundem`

## Hanc igitur

- both hands extended over oblations
- bare palms face downward
- do not touch oblations
- hold through `Per Christum Dominum nostrum`
- join hands at conclusion

Warning bell shortly before Consecration remains a distinct bell cue in the spoken Low Mass service profile.

## Quam oblationem

Five crosses total:

- 3 over Host + chalice together: `benedictam`, `adscriptam`, `ratam`
- 1 over Host only: `Corpus`
- 1 over chalice only: `Sanguis`

Then:

- elevate/join hands at `Domini nostri Jesu Christi`
- bow head to cross
- if needed clean fingers on corporal
- take Host between thumb/index of both hands
- raise eyes to heaven then lower
- bow head at `tibi gratias agens`
- hold Host with left thumb/index
- bless Host with right hand at `benedixit`
- stop immediately before words of Consecration

---

# 19. Consecration and elevations

## Bell profile — locked spoken Low Mass baseline

Acolyte 1 is the bell operator.

Separate warning cue shortly before Consecration remains distinct.

For the Host:

1. **one ring at first priest genuflection**
2. **one ring at elevation**
3. **one ring at second priest genuflection**

For the chalice:

1. **one ring at first priest genuflection**
2. **one ring at elevation**
3. **one ring at second priest genuflection**

Do not encode “three rings concentrated at the elevation” as the canonical spoken Low Mass baseline.

## Server elevation positions

After warning cue:

- both acolytes rise
- ascend to predella
- kneel one on each side of priest, **slightly behind him**
- AC1 remains Epistle side
- AC2 remains Gospel side
- do not turn this into a front/back arrangement

AC1 holds bell in right hand and uses left hand for chasuble.

## Words over Host

Priest:

- elbows on altar
- head inclined
- Host between both thumb/index pairs
- secret voice

Servers:

- kneeling erect
- do **not** bow during the words

## First Host genuflection

- priest genuflects/adore Host
- both servers moderate bow
- **AC1 rings once**

This begins the post-Consecration thumb/index constraint.

## Host elevation

Priest:

- stand
- elevate Host as high as comfortably possible
- eyes on Host
- show to people

AC1:

- left hand lifts outside Epistle lower edge of chasuble
- right hand rings **once**

AC2:

- right hand lifts outside Gospel lower edge of chasuble

Both lift only slightly; do not expose underside of chasuble.

## Second Host genuflection

- lower Host
- replace Host on corporal with right hand only
- thumb/index discipline preserved
- priest genuflects
- servers lower/release chasuble and moderate bow
- **AC1 rings once**

## Chalice Consecration

- rise from Host genuflection
- uncover chalice with right hand
- if needed wipe fragments over corporal
- take chalice near node with both hands
- elevate slightly then replace
- bow head at `item tibi gratias agens`
- left hand supports below cup / right blesses at `benedixit`
- take chalice with left at foot and right at node
- elbows on altar
- head inclined
- pronounce words secretly
- replace chalice
- say `Haec quotiescumque...`

Servers remain kneeling erect during the words.

## First chalice genuflection

- priest genuflects/adore Precious Blood
- servers moderate bow
- **AC1 rings once**

## Chalice elevation

- priest takes uncovered chalice with both hands
- elevates high enough to show people
- eyes on chalice
- AC1 lifts Epistle chasuble edge with left hand and rings **once** with right
- AC2 lifts Gospel edge with right hand

## Second chalice genuflection

- lower chalice
- replace in former place
- cover with pall using right hand
- priest genuflects
- servers lower/release chasuble and moderate bow
- **AC1 rings once**

## Post-Consecration finger invariant

From the Host Consecration until finger ablutions:

- thumb/index fingertips of both hands remain joined
- separate only as necessary to touch/handle Sacred Host
- every later close-hand illustration must show this correctly

---

# 20. Canon after Consecration → minor elevation

## Servers return

Immediately after chalice second genuflection:

- both servers rise
- turn inward
- descend without casually turning their backs to Blessed Sacrament
- meet at center below steps
- genuflect together
- return to ordinary lowest-step sides
- kneel

## Unde et memores

- hands extended through `de tuis donis ac datis`
- join hands
- left hand on corporal
- five crosses:
  - 3 over Host + chalice: `hostiam puram`, `hostiam sanctam`, `hostiam immaculatam`
  - 1 over Host: `Panem sanctum vitae aeternae`
  - 1 over chalice: `Calicem salutis perpetuae`
- extend hands again for `Supra quae`

## Supplices te rogamus

- profound body bow
- joined hands on altar edge through `quotquot`
- separate hands
- palms on corporal without touching Host
- altar kiss
- stand erect
- briefly join at `Filii tui`
- left hand on corporal
- cross Host at `Corpus`
- cross chalice at `Sanguinem`
- left hand to breast
- sign self through `omni benedictione ... repleamur`
- join hands
- no bow at this brief conclusion

## Memento of dead

Distinct from Memento of living:

- begin hands extended
- slowly bring hands together before breast without elevating through `in somno pacis`
- only then raise joined hands to chin height
- eyes on consecrated Host
- silent remembrance
- extend hands again
- join at `deprecamur`
- bow to Host during `Per eundem Christum Dominum nostrum. Amen.`

## Nobis quoque peccatoribus

- opening words `Nobis quoque peccatoribus` aloud
- left palm down on corporal
- strike breast **once** with last three right-hand fingers
- thumb/index remain joined and clear of chasuble
- extend hands and continue low
- conditional bow to Missal if named saint requires
- join at `Per Christum Dominum nostrum`
- no bow at this conclusion

## Per quem haec omnia

- three crosses over Host + chalice: `sanctificas`, `vivificas`, `benedicis`
- uncover chalice
- palms on corporal
- genuflect
- use left index to raise Host edge
- take Host with right thumb/index
- left hand to chalice node

## Per ipsum / minor elevation

Using Host:

- 3 horizontal crosses over chalice: `Per ipsum`, `et cum ipso`, `et in ipso`
- 2 crosses between chalice and priest
- then Host + chalice raised together **only a few inches** at `omnis honor et gloria`

Then:

- replace chalice
- replace Host
- rub thumb/index over chalice to release fragments
- cover chalice with pall
- hands on corporal
- genuflect/rise
- `Per omnia saecula saeculorum` aloud
- servers answer `Amen`

**No bell at minor elevation in the canonical spoken Low Mass profile.**
A local custom bell may exist only as an explicit variant.

---

# 21. Pater noster → Fraction → Agnus Dei

## Pater noster

- after server `Amen`, join hands before breast
- bow to Host while saying `Oremus`
- raise head after `audemus dicere`
- extend hands
- **look at Sacred Host throughout the entire Pater noster**
- hands extended through `et ne nos inducas in tentationem`
- servers answer `Sed libera nos a malo`

## Recover / purify paten

After priest's `Amen`:

- left hand on corporal
- remove paten from under right edge with right hand
- fold purificator once
- polish upper paten surface
- replace purificator unfolded to right of corporal
- hold paten upright off corporal between right index/middle fingers
- concave surface faces Gospel side

## Libera nos — sign with paten

- hold paten upright in right hand
- left hand on corporal
- required bows to Missal at Mary/saints
- after `omnibus Sanctis`, left hand to breast
- sign self **with the paten itself**:
  - forehead at `da propitius`
  - breast at `pacem`
  - left shoulder at `in diebus`
  - right shoulder at `nostris`
- kiss edge of paten silently

## Host onto paten / uncover chalice

- lower paten almost horizontally
- rest left edge beside Host
- use left index to push Host sideways onto paten
- do not pass Host over kissed part of paten
- paten near chalice base/right of former Host location
- finish `Libera nos`
- left hand on chalice base
- remove pall with right hand
- palms on corporal
- genuflect

## Fraction

- rise
- push Host off right side of paten near top
- take Host with right thumb/index
- hold over chalice between both thumb/index pairs
- divide Host **vertically beginning at top**, bending outer edges toward priest
- bow at Holy Name during conclusion
- place right half on paten

Then:

- from left half break a small particle from **bottom edge** with right thumb/index
- retain particle over chalice in right hand
- place remaining left half on paten
- arrange two large halves to resemble complete Host

## Pax Domini

- left hand at chalice node
- small particle in right thumb/index over chalice
- `Per omnia...` aloud; servers `Amen`
- three horizontal crosses with particle over chalice:
  - `Pax Domini`
  - `sit semper`
  - `vobiscum`
- particle does not touch chalice
- servers: `Et cum spiritu tuo`

## Commingling

- drop particle into chalice as `Haec commixtio` begins
- bow at Holy Name
- after prayer rub thumb/index of each hand together over chalice so fragments fall into cup
- left hand at chalice base
- replace pall with right
- palms on corporal
- genuflect

## Agnus Dei

- medium body bow throughout
- hands initially joined between breast and altar, **not resting on altar**
- after each `mundi`, left hand palm-down on corporal
- three breast strikes using last three right-hand fingers:
  - first `miserere nobis`
  - second `miserere nobis`
  - `dona nobis pacem`
- thumb/index remain joined and clear of chasuble
- servers remain kneeling and bow through Agnus Dei

Requiem:

- `dona eis requiem` substitutions
- omit breast strikes
- hands remain joined

---

# 22. Priest Communion preparation and Communion

The current repository has detailed later assets, but preserve these approved details exactly.

## Three private Communion prayers

Priest:

- medium body bow throughout
- hands joined on altar edge
- eyes fixed on Sacred Host
- low voice
- no additional Holy Name bow because he is already bowed in reverence

Prayers:

1. `Domine Jesu Christe, qui dixisti Apostolis tuis...`
2. `Domine Jesu Christe, Fili Dei vivi...`
3. `Perceptio Corporis tui...`

Requiem:

- omit first prayer

## Panem caelestem

- palms on corporal
- genuflect
- while rising say `Panem caelestem accipiam...`
- arrange the two Host halves and paten as in current canonical late assets

## Domine non sum dignus

Three repetitions.

Priest:

- medium body bow until final `anima mea`
- left hand holds Host + paten
- right hand strikes breast **once per repetition** using last three fingers
- opening `Domine, non sum dignus` aloud
- remainder low

**AC1 rings the bell once at each of the three opening `Domine, non sum dignus`.**

Total = 3 rings.

AC2 remains kneeling/reverent.

## Priest receives Host

- stand erect
- align Host halves
- take in right thumb/index
- make large **vertical sign of cross with Host over paten**
- keep Host within paten edges
- say `Corpus Domini...` low
- bow at Holy Name
- bow low over altar
- forearms on altar
- paten under chin
- consume Host
- stand
- paten to front/right of chalice
- rub fingers over paten
- rejoin thumb/index tips
- joined hands before face for brief swallowing/meditation pause

## Quid retribuam / fragments

- left hand to chalice base
- uncover chalice
- palms on corporal
- genuflect while saying `Quid retribuam Domino`
- use paten edge to scrape corporal for fragments even if none visible
- purify paten over chalice so fragments fall into cup

## Precious Blood

- left hand holds paten on corporal
- right hand takes chalice under node
- `Calicem salutaris...`
- raise chalice to eye height
- make large vertical sign of cross with chalice
- say `Sanguis Domini...`
- bow at Holy Name
- paten horizontally under chin
- consume Precious Blood in one draught if possible
- keep chalice at mouth until finished
- lower
- place paten/chalice down together
- immediately extend chalice toward Epistle side for ablution
- no post-chalice meditation pause before ablutions

---

# 23. Post-Communion ablutions — locked user correction

This is one of the most important late corrections and must override any older draft or general guide.

**The ablutions are done only by AC1. AC2 does not assist.**

## First ablution

- **wine first**
- chalice remains **on the altar**
- AC1 alone supplies the wine

## Second ablution

- **water second**
- priest is **holding the chalice**
- AC1 alone supplies the water
- AC1 **steps down exactly one altar step** while doing so

Do not encode an AC1-wine / AC2-water split for these post-Communion ablutions. That was explicitly corrected and superseded.

The post-Consecration thumb/index constraint ends only with the finger ablution.

---

# 24. Coordinated post-ablution transfer — locked user correction

Only after the vessels are cleansed:

- **AC1 takes the chalice cloth to the Gospel side**
- **AC2 takes the Missal back to the Epistle side**

They move simultaneously and cross.

## First crossing

- **AC2 is in front**

Then:

- priest takes the chalice cloth from AC1

## Second crossing

They cross again.

- **AC1 is now in front**

Then:

- both resume their ordinary kneeling positions

Missal on Epistle side must retain the left-reading orientation.

This coordinated crossing order must be represented explicitly as structural paths / ordering constraints rather than as prose only.

---

# 25. Communion antiphon → Postcommunion

After vessels cleansed and coordinated transfer:

- priest moves to Epistle-side Missal
- reads Communion antiphon
- Missal oriented for priest to read facing left

Then return through the established center transition:

- altar kiss as required
- `Dominus vobiscum`
- `Oremus`
- Postcommunion prayer(s)

Preserve any already committed detailed late-scene choreography rather than replacing it with a new paraphrase.

---

# 26. Ending branches — 1962-specific correction

Do not choose dismissal based on whether Gloria was said.

1962 baseline:

- ordinary Mass: **`Ite, missa est`**
- **`Benedicamus Domino`** only when a procession or another liturgical function immediately follows
- Requiem: **`Requiescant in pace`**

Preserve the committed ending-branch YAML, including the minimally repaired canonical version and the original invalid transport bytes under `transport-originals/`.

Do not silently “clean up” that provenance history.

---

# 27. Placeat / blessing / Last Gospel / Leonine prayers

Preserve the already committed late structural assets, but ensure the complete corpus registry includes them.

## Placeat / blessing

- `Placeat tibi`
- altar kiss
- blessing when prescribed
- eyes to cross
- hands elevated/rejoined as prescribed
- bow at `Deus`
- turn right
- large blessing over people

## Last Gospel

For normal John 1 Last Gospel:

- servers stand
- priest + servers make three small crosses
- all genuflect at **`Et Verbum caro factum est`**

Keep 1962 Last Gospel exceptions as explicit branches, including omission after certain `Benedicamus Domino` cases tied to following functions and the other already documented 1962 exceptions.

## Leonine prayers

Model as a **post-Mass appendix**, not as part of the Mass proper.

- priest + servers descend
- servers kneel in plano slightly behind priest
- servers lead/respond as appropriate
- then recessional

---

