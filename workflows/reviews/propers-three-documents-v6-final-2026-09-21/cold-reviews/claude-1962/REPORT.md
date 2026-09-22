# Final cold review — Claude 1962 TLM three-document set

## Verdict

**PASS.** The exact three-PDF set identified below is release-ready. I found no
blocking defect or advisory repair in the frozen bytes.

## Review boundary

This review is confined to the Claude publication tree for the 1962 Roman
Missal's Seventeenth Sunday after Pentecost:

- expansive study: `57-seventeenth-after-pentecost.pdf`;
- concise synthesis: `57-seventeenth-after-pentecost-synthesis.pdf`;
- homily: `57-seventeenth-after-pentecost-homily.pdf`.

No postconciliar proper, calendar identity, reading set, or formulary was used
as evidence for this set. I made no tracked edit.

## Exact artifact identity

| Artifact | SHA-256 | Pages | Bytes |
|---|---|---:|---:|
| Expansive study | `60812b8145520e0ef05706e7b63680aa7880681ae293859bd51f38d67728ab68` | 31 | 540,318 |
| Concise synthesis | `1f829093361895e89919ce3a9f3eec488decdecb066ab26b61b5d371ea138bf0` | 10 | 450,164 |
| Homily | `01f1a71b949cb783d2a8125ae9ba43a2bfa59c7223101dfee54c612f3c7ca3d1` | 3 | 275,035 |

All three are US Letter PDFs, revision-stamped
`2026-09-21T23:18:36Z`. The refreshed `research/artifacts.json` receipt names
these exact hashes, and both artifact checkers accept every edition.

## Substantive assessment

### Expansive study

The 31-page study treats all ten appointed elements of the 1962 formulary:
Introit, Collect, Epistle, Gradual, Alleluia, Gospel, Offertory, Secret,
Communion, and Postcommunion. It establishes three internally coherent
readings of the whole formulary:

1. the whole heart and the one body;
2. David's son and David's Lord;
3. the just judge and merciful hearer.

Each reading is supported by multiple patristic, saintly, or received
ecclesiastical witnesses, follows every proper element, and ends with its own
literal, allegorical, moral, and anagogical distillation. The study identifies
differences instead of flattening them, including Augustine and Cassiodorus on
the speaker of Psalm 101, Jerome and Augustine on Daniel's confession, the
Greek and Latin readings of Ephesians 4:6, and Hilary and Augustine on the
beginning of mercy. The comparison section explains what the readings share
and where each places the weight of the Mass.

### Concise synthesis

The ten-page synthesis is independently intelligible and interleaves the
witnesses by exegetical question. Its fixed opening is correct:

- physical page 1 contains the complete ten-element inventory and exactly four
  overview-sense rows;
- physical page 2 contains only the Scriptural Date and Location dossier;
- physical pages 3–4 give substantive themes and movement;
- physical page 5 begins the detailed comparative commentary.

The corrected page-2 chronology is compact but comfortably readable. Its
Matthew ranges preserve the source labels' uncertainty (`c. A.D. 38–45`,
`c. A.D. 40–42`, `A.D. 40–45`, `c. A.D. 60–68`, `c. A.D. 64–67`, and
`c. A.D. 50`), and the Catholic-critical comparison remains separately
labelled. The commentary makes disagreements and alternative emphases
intelligible without reducing the three readings to separate miniatures.

### Homily

The homily is continuous, speakable prose for an adult parish assembly. Its
1,416-word body supports an unhurried eleven-to-twelve-minute delivery. It
moves from the Gospel's questions and silence through Augustine's undivided
heart, Chrysostom's reciprocity between the two commandments, Paul's sevenfold
unity, the Collect, the Introit and Danielic Offertory, the Creed, Communion,
and the Postcommunion. Repetition, concrete parish examples, contrast, direct
questions, a return to the opening image, and one practicable weekly response
give it usable pedagogy without inserting citation machinery into the speech.
The terminal note discloses audience, pace, derivation, text routes, and exact
loci.

The speech is safe for different legitimate 1962 ceremonial circumstances:
it says that bread and wine will be offered, that the hearers will offer
themselves with them and *may* receive, and that the Church *appoints* the
Communion verse. It does not presume a particular offertory procession,
Communion chant performance, or universal reception.

## Rite isolation

The manifest declares `calendar = "roman-1962"`; its document, three output
paths, ten-element inventory, and every component path remain under the 1962
tree. The publication metadata, rubrics, calendar name, appointed readings and
chants, source bindings, chronology, and terminal apparatus all identify the
1962 Missal and this Sunday after Pentecost.

A late cold review had found `Ordinary Time` and the postconciliar heightened
`semi-continuous` premise in two internal research records. The frozen source
has replaced them with evidence-specific language about this 1962 Sunday, its
sequential Epistle, and the separately travelled parts of the formulary. A
fresh scan finds neither phrase in live source outside historical evaluation
packets, and no postconciliar-family term occurs in any of the three extracted
PDF texts. The two remaining uses of *postconciliar* in live research files are
explicit boundary statements that those records were not opened; they import
no content.

## Visual and stylistic assessment

All 44 pages of the frozen set were inspected at original raster size. The
design is stylistically consistent across the set and restores the established
historical book style: embedded Latin Modern type, monochrome rules and text,
compact title blocks, stable running heads and margins, restrained tables, and
a small terminal apparatus. The study and synthesis use a readable single
column; the spoken homily uses two columns, with no running head on page 1 and
the semantic `Homily` head thereafter.

No clipping, collision, missing glyph, accidental blank page, orphaned
colophon, or continuation-only spill appears. The deliberately shorter
lane-ending pages keep their four-sense blocks as semantic units. The final
references, revision stamps, and reuse colophons are balanced and legible.

`pdffonts` reports every font embedded, subsetted, and Unicode-mapped. Extracted
text contains no replacement character. The three build logs contain no
Overfull/Underfull box report, TeX or package warning, missing-character report,
undefined reference, or error.

## Mechanical evidence

For each of `research`, `synthesis`, and `homily`, all of the following passed:

- `tools/check-content-preflight`;
- `tools/check-proper-components --phase content`;
- `tools/check-proper-components --phase artifacts`;
- `scripts/_proper_study.py check --phase content --require-presentation --require-format`;
- `scripts/_proper_study.py check --phase artifacts --require-presentation --require-format`.

The preflight reports 75 valid, fingerprinted bindings; current chronology
annotations for seven scriptural elements and fifteen corpus assertions;
supported chronology claims; three whole-proper interpretive lanes with all
four senses; used references; no restricted-source reproduction; and clean
house voice and structural labels. The component checks accept the complete
ten-element manifest. A scoped `git diff --check` is clean.

## Findings

No release blocker or advisory remains for these exact bytes.
