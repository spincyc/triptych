# Ark and sanctuary diagram audit

## Identity and purpose

- `ARK-DIAGRAM-001` is the deterministic TikZ pencil study of the Ark in
  `sections/57-ark-and-sanctuaries.tex`.
- `ARK-DIAGRAM-002` is the deterministic four-panel sanctuary study in the
  same source.
- The complete web and accessibility equivalent is
  `sections/57-ark-and-sanctuaries-text-equivalent.tex`.
- Purpose: answer the reader's concrete questions about the Ark's commanded
  features and its attested sanctuary settings while preventing illustrative
  convention from becoming archaeological or exegetical evidence.

Both diagrams are project-authored vector linework. They contain no external
raster, traced artifact, archaeological reconstruction, or AI-generated
semantic content. The random-step TikZ decoration supplies only a reproducible
pencil-line convention. Live TeX owns every label.

## Source-control matrix

| Diagram claim | Controlling loci | Status | Rendering rule |
| --- | --- | --- | --- |
| Chest of acacia/setim wood, gold inside and outside | Ex 25:10–11; 37:1–2 | direct | Show a wooden core by label, not by invented grain or botanical certainty. |
| Relative dimensions: 2.5 by 1.5 by 1.5 cubits | Ex 25:10; 37:1 | direct | State cubits; do not convert to a supposedly exact modern length. |
| Four rings and two overlaid poles left in them | Ex 25:12–15; 37:3–5 | direct | Four ring symbols may be partly occluded in perspective; label the commanded count and permanence. |
| Pure-gold cover/mercy seat/propitiatory | Ex 25:17; 37:6 | direct | Keep cover distinct from the wood-and-overlay chest. |
| Two hammered cherubim, wings overshadowing, faces toward cover | Ex 25:18–20; 37:7–9 | direct features, unknown appearance | Use abstract outlines and print the non-reconstruction boundary. |
| Tablets inside; manna, rod, and law-book descriptions differ by locus | Ex 16:32–34; 25:16, 21; Num 17:4–10; Deut 10:1–5; 31:24–26; Heb 9:4; 1 Kgs 8:9 | direct, witness-sensitive | Explain in prose; do not invent an interior still life or a transfer history. |
| Ark behind the Tabernacle veil | Ex 26:31–34; 40:18–21 | direct arrangement | Use a schematic plan and no recovered footprint claim. |
| Ark at Shiloh amid Tent/house/temple, door, and lamp language | Josh 18:1; 1 Sam 1:9; 3:3, 15; 4:3–4 | direct presence, form uncertain | Use a dashed precinct with an explicit unknown-form notice; do not draw a factual building. |
| Ark within the tent David pitched; old Tabernacle at Gibeon | 2 Sam 6:17; 1 Chr 16:1, 39–40 | direct, complementary | A symbolic tent is permitted only with a non-reconstruction label. |
| Ark in Solomon's inner sanctuary beneath great cherubim | 1 Kgs 6:19–28; 8:1–11; 2 Chr 5:2–14 | direct textual arrangement | Use a simplified teaching plan, not a precise Temple Mount footprint or elevation. |

## Exclusions

The plates do not claim:

- a recovered portrait of the Ark or cherubim;
- a fixed modern length for the cubit;
- that the law-book was inside the Ark;
- an explanation for how the manna vessel or rod entered or left;
- an excavated Ark, Tabernacle, Shiloh sanctuary, Davidic tent, or First-Temple
  Holy of Holies;
- a single architectural continuity among the four settings; or
- that Mary is an object, building, or container of the divine nature.

## Production acceptance

Final state: `accepted for alpha publication; consumer review complete on
2026-08-16`.

- [x] Every live label extracts from the PDF in reading order.
- [x] No label collides with linework or exits the page.
- [x] The four-panel plate remains legible at actual printed size and in a
  grayscale photocopy simulation.
- [x] The Shiloh and Davidic panels communicate uncertainty more strongly than
  their conventional outlines communicate form.
- [x] The text equivalent preserves every visible factual feature and every
  nonclaim in the web edition.
- [x] The installed PDF and generated web edition were compared against these
  sources after final rendering.

The final full-size checks covered physical PDF page 15 (Ark study) and page
16 (four sanctuary settings), including the repaired Shiloh and Davidic
labels. All 42 pages were inspected through final page rasters and bounded
contact sheets. The reviewed build and installed PDF are byte-identical at
SHA-256
`a520adb39130bb3b65a3bd7d92926fbc77126650fdf593d0680fc10bee125843`;
the generated and installed web editions are byte-identical at SHA-256
`3a5e96c2405e1d311acf65ef931a45ebee502e459817f5a744833858ce62d1bc`.
