# Plan Outline — Mass Pictographic Dictionary

## Project goal
Create a high-publication-quality **pictographic dictionary of the Mass** for:

- Roman 1962 Low Mass
- Roman 1962 High Mass
- Roman 1962 Pontifical Mass
- postconciliar Mass

The deliverable should support:
- Triptych integration,
- future altar server manual development,
- object compendium extraction,
- future scene-by-scene liturgical reference work.

---

## Working method

### Phase 1 — Structural corpus
Build deterministic structural scene sheets and YAML metadata first.

Goals:
- settle geometry,
- settle actor roles,
- settle object placement,
- settle action order,
- settle branch conditions,
- settle vantage requirements.

Status:
- **1962 Low Mass structural pass complete through v0.21**.

### Phase 2 — Artistic render pass
Convert approved structural scenes into high-resolution graphite / pencil instructional plates.

Requirements:
- publication quality,
- no vague or low-quality sketch treatment,
- instructional clarity,
- multiple viewpoints where necessary,
- visual consistency across the entire corpus.

### Phase 3 — Object compendium extraction
For each scene, preserve object usage metadata so the project can later generate:
- object dictionary pages,
- isolated object plates,
- object-by-scene cross references.

### Phase 4 — Form expansion
After Low Mass render pass is established:
- High Mass
- Pontifical Mass
- postconciliar Mass

### Phase 5 — Integration and packaging
- integrate into Triptych project,
- prepare reusable metadata for agentic workflows,
- prepare altar server manual downstream materials,
- create final bundles and instructions.

---

## Immediate next-step plan

### 1. Commit checkpoint
Persist the approved structural corpus in git.

### 2. Open a fresh review lane
Use a fresh web session for the artistic pass.

### 3. Begin artistic rendering with a style anchor plate
Suggested order:
1. Sanctuary master plate
2. Opening foot-of-the-altar cluster
3. Introit/Kyrie/Gloria cluster
4. Readings cluster
5. Offertory cluster
6. Canon / Consecration cluster
7. Communion / Ablutions cluster
8. Final rites cluster

### 4. Review one image at a time
Each image should be presented for approval in the web interface.

### 5. Preserve metadata for every final artistic plate
Each artistic plate should retain or link to:
- scene_id
- rite / form
- action
- actors
- objects in use
- viewpoint
- invariants
- branch conditions
- related structural source(s)

---

## Design standards for the artistic pass

- high-resolution graphite / pencil
- crisp and intentional line work
- instructional, not sentimental
- architecture and vestments should be accurate
- object identity should be unmistakable
- compositions should be clean and readable
- vantage changes should be purposeful
- visual language should remain consistent across the whole corpus
- structural invariants from v0.21 should not be casually altered
