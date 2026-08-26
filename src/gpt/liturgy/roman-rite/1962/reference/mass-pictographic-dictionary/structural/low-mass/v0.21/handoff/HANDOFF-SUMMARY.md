# Mass Pictographic Dictionary Handoff — v0.21

## Purpose

This package captures the approved **structural pass** for the **spoken 1962 Roman Low Mass with two servers** as developed in the web review workflow.

It is intended to be handed to an agent so the current work can be:

1. persisted in the repository with a clean commit,
2. summarized in project documentation,
3. used as the authoritative structural baseline for the later artistic rendering pass.

---

## What is complete

The **structural corpus for the 1962 Low Mass** is complete through the end of Mass and has been approved by the user through **v0.21**.

This includes:

- sanctuary geometry / spatial invariants
- two-server role mapping
- Prayers at the Foot of the Altar
- ascent / Introit / Kyrie / Gloria / Collects
- Epistle / Gospel transfer / Gospel
- Credo branch
- Offertory
- Canon
- Consecration
- post-Consecration Canon
- Pater noster / Libera nos / Fraction / Pax Domini / Commingling / Agnus Dei
- priest's Communion under both species
- ablutions
- coordinated post-ablution transfers
- Communion antiphon / Postcommunion / dismissal / blessing / Last Gospel
- Leonine prayers appendix

---

## Important approved corrections / invariants

These are especially important and should be treated as locked unless the user later changes them.

### Service form / staffing
- Baseline is **spoken 1962 Low Mass**.
- Show **two servers** as the ordinary/common form.

### Missal transfer roles
- **Acolyte 1** (Epistle-side acolyte) moves the missal **to the Gospel side** for the Gospel.
- **Acolyte 2** moves the missal **back to the Epistle side after the vessels have been cleansed**.
- Missal orientation invariant: when being read, it is oriented so the priest reads **facing left**, even on the Gospel side.

### Early posture / arrangement corrections
- Priest and servers are together **in a line side-to-side**, not front-to-back.
- In the Confiteor response plate, the servers' heads are turned inward and slightly bowed.
- The altar must show the **full set of steps**.

### Consecration bell profile
- Spoken Low Mass baseline:
  - one warning bell before the Consecration,
  - then for each species: **1 ring at first genuflection, 1 ring at elevation, 1 ring at second genuflection**.
- Minor elevation bell is **not part of the canonical spoken-Low-Mass baseline**; if included later, it must be marked as a local/customary variant only.

### Indulgentiam
- For **Indulgentiam**, **all three** make the sign of the cross.

### Oramus te / ascent assistance
- At the point discussed in the ascent, the assisting server is only **Acolyte 1**, who lifts the hem of the priest's cassock/alb as specified.

### Gloria
- The priest says the **Gloria standing at the center of the altar**.

### Post-Consecration hand invariant
- After the Consecration, the priest maintains the thumb/index discipline until the finger ablutions, except as required to handle the Sacred Host.

### Pater noster / Agnus / Domine non sum dignus
- During the **Pater noster**, the priest's gaze remains on the Sacred Host.
- During the **Agnus Dei**, the priest makes three breast strikes with the three free fingers.
- **Acolyte 1 rings once at each of the three priestly "Domine, non sum dignus" openings**.

### Ablutions and coordinated transfer
This was a major approved correction and must be preserved exactly.

- **Acolyte 1 alone performs the ablution service.**
- **First ablution:** wine first, with the **chalice on the altar**.
- **Second ablution:** water second, with the **priest holding the chalice**, and **Acolyte 1 stepping down one step** to pour.
- **Acolyte 2 does not assist in the ablutions.**
- After the vessels are cleansed:
  - **Acolyte 1** takes the **chalice cloth to the Gospel side**.
  - **Acolyte 2** takes the **missal back to the Epistle side**.
  - On the **first crossing**, **Acolyte 2 is in front**.
  - Once the priest takes the chalice cloth, they cross again, **this time with Acolyte 1 in front**.
  - Then both resume their kneeling positions.

### 1962 ending branch correction
- In the 1962 rubrics, the dismissal is **not** chosen based on whether the Gloria was said.
- Baseline:
  - **Ite, missa est** normally,
  - **Benedicamus Domino** only when another liturgical function/procession follows,
  - **Requiescant in pace** for Requiems.

---

## What is in the artifacts directory

`artifacts/mass-pictographic-core-v0.21/` contains the structural corpus as of the last approved checkpoint.

This includes:
- PNG storyboard sheets,
- SVG sources for those sheets,
- YAML scene metadata,
- YAML object / branch / service-profile metadata,
- earlier approved intermediate sheets retained in the bundle.

The key bundle file already produced in the web workflow is also present inside the copied directory as:
- `mass-pictographic-core-v0.21.tar.gz` (if retained in source set), or the equivalent unpacked content.

---

## What is not complete yet

The following are **not** yet complete:

1. the **publication-quality pencil render pass**,
2. the object-by-object compendium extraction,
3. High Mass structural pass,
4. Pontifical Mass structural pass,
5. postconciliar Mass structural pass,
6. the final Triptych integration wiring,
7. the final altar server manual packaging.

---

## Recommended next step after commit

After this checkpoint is committed, start a fresh web review instance and begin the **artistic rendering phase**, using the approved structural corpus as the deterministic underlay.

Recommended first artistic plate:
- either the **sanctuary master plate**, or
- the **first opening Low Mass plate at the foot of the altar**.

The artistic pass should lock:
- graphite / pencil language,
- figure proportions,
- vestment treatment,
- altar architecture,
- object clarity,
- label style,
- multi-vantage conventions for action plates.
