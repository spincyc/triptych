# Prayer-Text Audit — The Angelus

This record controls every fixed vocal unit offered for recitation in
`src/gpt/theology/mariology/angelus/main.tex`. Expository prose, headings,
source labels, and optional-use instructions are not vocal prayer.

## Governing witness

The sole governing prayer witness is Dom Gaspar Lefebvre, O.S.B., *Daily
Missal with Vespers for Sundays and Feasts* (Lophem near Bruges: St. Andrew's
Abbey; St. Paul, Minnesota: E. M. Lohmann, 1925), printed pp. 5 and 12–14.

- Angelus Latin and facing historical English: printed p. 13.
- Complete Hail Mary used for each explicit abbreviation: printed p. 5.
- Adjacent historical recitation, posture, seasonal, and indulgence context:
  printed p. 12 and continuing context through p. 14.
- Checked scan SHA-256:
  `28c9046c5acfa19297ab9aeaa14ac4f8d8fcffab1307b51215b94fa4ca6172a2`.
- Scan citation:
  <https://archive.ccwatershed.org/media/pdfs/21/02/16/05-35-23_0.pdf>.

The page images, not OCR or memory, govern spelling, accents, ligatures,
capitalization, punctuation, pronouns, and line content. No AI or project
translation appears as prayer.

## Vocal-unit inventory

| Unit | Exact source and language status | Abbreviation or editorial action | Publication use |
| --- | --- | --- | --- |
| Three Angelus versicle-response pairs | Lefebvre p. 13, exact received Latin and facing historical English | None. Typography supplies `V.` and `R.` labels already present in the prayer's responsive structure; no words are modernized. | Printed in the bilingual prayer card. |
| Three Hail Mary directions | Lefebvre p. 13 abbreviates the repeated prayer exactly as `Ave María, etc.` / `Hail, Mary, etc.` with an explicit expectation of the known prayer; Lefebvre p. 5 prints its complete Latin and facing historical English | The publication retains each abbreviation inside the card. It prints the exact complete p. 5 Hail Mary once after the card and directs the reader to use it at each of the three marked places. | Repeated three times in recitation; complete text printed once. |
| `Ora pro nobis` versicle and response | Lefebvre p. 13, exact received Latin and historical English | None. | Printed after the third Hail Mary direction. |
| `Oremus` / “Let us pray,” collect, conclusion, response, and Amen | Lefebvre p. 13, exact received Latin and historical English | The source's complete conclusion is retained. No conclusion is borrowed from another book or current translation. | Printed as the closing prayer. |
| Historical rubrics at pp. 12–14 | Lefebvre's prose and rubrical context | Not offered as vocal prayer and not silently converted into current discipline. Only source-status explanation is paraphrased. | Research and qualification evidence only. |

The exact Hail Mary has one repository owner at
`src/gpt/devotions/novenas/10-our-lady-of-mount-carmel/prayers/hail-mary.tex`.
The Angelus imports that fragment rather than creating an editable duplicate.
The fragment's witness and printed wording agree with Lefebvre p. 5, including
the accent in `muliéribus`.

## Orthography, punctuation, and variants

- Historical Latin accents and forms—including `Maríæ`, plain `quaesumus`, and
  `ejus`—are retained from Lefebvre rather than normalized to the 1999
  *Enchiridion* or to modern `eius` orthography.
- The selected Angelus retains `Spíritu sancto`, each exact `Ave María, etc.`
  marker, and the source comma in `glóriam, perducámur`. The same-witness Hail
  Mary retains `muliéribus`; none is silently regularized.
- Historical English retains `Holy Ghost`, second-person singular forms such
  as `Thee`, `Thy`, and `thou`, `amongst`, and the source's capitalization. It
  is not described as the current approved English for any territory.
- Lefebvre's closing Latin uses `Per eúmdem Christum Dóminum nostrum`; the
  fourth *Enchiridion* prints `Per Christum Dominum nostrum`. The publication
  preserves Lefebvre because the historical witness governs the prayer text;
  the *Enchiridion* governs the current indulgence claim.
- The 2005 English *Compendium* uses a modern official form, including
  `declared unto`, `Holy Spirit`, and an appended Glory Be. Those words are not
  conflated with Lefebvre's historical English. The current indulgence grant
  itself specifies the appointed versicles and collect and prints no Glory Be
  condition.
- Line breaks in the bilingual card are presentational. They do not add,
  delete, reorder, or paraphrase a vocal word.
- The ordinary title spelling `Angelus` does not alter the selected prayer's
  Latin incipit or any source form.

## Collation performed

The following checks were completed against the page images:

1. every Latin and English Angelus line on p. 13 was compared to the rendered
   source text;
2. the three abbreviation points were identified rather than expanded from
   memory;
3. the complete Latin and English Hail Mary was checked against p. 5 and its
   repository fragment;
4. accents, ligatures, punctuation, capitalization, and the complete collect
   conclusion were preserved;
5. the adjacent p. 12–14 historical rubrics were separated from vocal text and
   from current discipline; and
6. the selected prayer was compared with the current Latin *Enchiridion* and
   the 2005 English *Compendium* to prevent silent conflation.

Independent human line-by-line collation remains outstanding and is not
claimed.

## Status and rights

The Angelus is printed as a received pious exercise. Its scriptural and
liturgical sources do not make this publication a liturgical book. The 1925
edition's imprimatur and other historical permissions govern that edition, not
Triptych's arrangement or commentary.

The 1925 edition is public domain in the United States by publication date. The
historical prayer wording remains excluded from Triptych's CC BY 4.0 grant.
The edition says “All rights reserved,” and this audit did not establish the
translator or author of the exact historical English; Lefebvre's 1966 death
therefore does not itself establish a non-US rights endpoint. Rights outside
the United States remain unresolved, and users must assess their jurisdiction
and use.

No current proprietary English Missal, Liturgy of the Hours, Bible, Compendium,
or devotional translation is reproduced. The present Latin *Enchiridion* is
cited for law and comparison rather than copied as the publication's prayer
witness. The historical English may be prayed devotionally, but it is not
represented as a competent-authority-approved vernacular text for gaining the
indulgence in every territory; *Enchiridion* norm 22 governs that question.

## Production fields

Prayer-source collation and render review completed on 21 July 2026:

- the final extracted and rendered Angelus lines match printed p. 13, and the
  separately printed complete Hail Mary matches printed p. 5;
- both prayer cards appear on physical PDF page 3 (arabic page 1);
- the cards have balanced columns, legible accents and punctuation, and no
  clipping or overlap; and
- build and installed PDFs are byte-identical at SHA-256
  `5416f7b4a6de668dcf07368887517b553cc0b28edfa88fc6dd5149f52473b13d`.
