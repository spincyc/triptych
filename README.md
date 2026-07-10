# Liturgical Year TLM Proper Connections

This project builds weekly LaTeX/PDF study sheets for the traditional Roman Mass propers. The first pass covers Trinity Sunday and the Second through Seventh Sundays after Pentecost, corresponding to the first seven weeks after Pentecost in the 1962 temporal cycle.

## Build

```sh
make
```

PDFs are written to `build/`. Use `make clean` to remove LaTeX intermediates and `make distclean` to remove generated PDFs too.

## Sources

The Mass proper references are keyed to the local corpus at:

- `../liturgy-history/versions/1962-missale-romanum-latin/sections/proper/011-proprium-de-tempore-after-ordinary.md`
- `../liturgy-history/versions/1962-missale-romanum-latin/metadata.json`

The Latin source is OCR and should be checked against a printed missal before publication. The weekly files use incipits, biblical references, and theological summaries rather than attempting to reproduce every proper in full.

Patristic and saintly links are given as study cross-references. They are intentionally concise and should be expanded with exact editions if this project becomes a publishable devotional or catechetical work.

## Document Structure

Each weekly `main.tex` should follow this order.

1. `\weektitle`

   Include the week title, liturgical title, and a short subtitle identifying the TLM context. For example: week number after Pentecost, Latin Sunday name, and whether the Sunday is displaced by a feast such as Trinity Sunday.

2. Optional source/rubric note

   Use this only when a week needs clarification, such as Trinity Sunday using the feast while the ferial First Sunday after Pentecost Mass remains relevant. Keep the note factual and liturgical.

3. Propers summary table

   Use `properstable` and `\properrow`. Include the major Mass propers and readings:

   - Introit
   - Collect
   - Epistle
   - Gospel
   - Offertory
   - Communion
   - Any exceptional proper or ferial note needed for that week

   Each row should include the proper, the TLM text/reference or incipit, the scriptural axis, fathers/saints for study, and the theological connection.

4. Four Senses of Scripture

   This section must come immediately after the propers summary. Use `connectionstable` with exactly these rows:

   - Literal: what the Epistle/Gospel or proper text says historically and grammatically.
   - Allegorical: how the text reveals Christ, the Church, the sacraments, or salvation history.
   - Moral: how the text calls the hearer to conversion, virtue, discernment, or concrete action.
   - Anagogical: how the text points to final judgment, heaven, resurrection, eternal communion, or the consummation of creation.

5. Homily Sketch

   This should read like a preacher's working outline, not an academic article. Include:

   - Proposition: the controlling claim of the homily.
   - Opening movement: how to enter the theme from the liturgy or Gospel image.
   - Doctrinal center: the main theological truth.
   - Moral turn: the conversion or pastoral application demanded by the text.

6. Exegetical Notes

   Use a short itemized list. Include close observations about the Sunday Epistle, Gospel, and major proper texts. Prefer interpretive notes that help preaching: repeated words, liturgical placement, contrasts, scriptural echoes, or sacramental cues.

7. Patristic and saintly witness table

   Use `witnessstable` and `\witnessrow`. Include short, carefully limited quotations or paraphrases from the Fathers, Doctors, and saints. Each row must explain how the witness helps the homily. Avoid long quotations unless the source has been verified and copyright permits it.

8. Deep connection table

   Use `connectionstable`. Show major theological links across the propers, readings, Fathers, and spiritual application. This table should make the document feel synthetic rather than a list of unrelated notes.

9. Preaching Applications

   Use a short itemized list. Give concrete pastoral applications, warnings, or practices. These should be specific enough for a homilist to use directly.

10. Primary References

   List the Missale Romanum 1962 temporal proper and any major source files or study witnesses used. Keep source notes honest about OCR quality and verification limits.

11. Full Patristic and Saintly Texts

   This must be the final section of each weekly document. Include the actual quotation text for selected Fathers, Doctors, and saints used earlier in the sheet. These are the "full quotes" for the excerpts cited in the witness material, not merely paraphrases.

   Requirements:

   - Place this section after Primary References.
   - Use `\section*{Full Patristic and Saintly Texts}`.
   - Prefer two to four quotations per week.
   - Keep each quotation short enough to remain readable in the PDF.
   - Attribute each quote by saint, work, and, when known, book/chapter/homily.
   - If exact wording has not been verified, do not present it as a direct quote.

## Future Codex/GPT Notes

When extending this project, preserve the structure above unless the user explicitly asks to change it. New weeks should feel like part of the same series.

Content standards:

- Keep the documents homiletic: they should support preaching, meditation, and liturgical study.
- Keep TLM propers central. Do not let patristic or devotional material replace the Mass texts.
- Treat the local 1962 Missale source as OCR. Use incipits and references confidently, but check full Latin text against a reliable missal before publication.
- Use the four senses as a disciplined interpretive framework, not as decorative labels.
- Prefer short quotations. If exact wording matters, verify it from a reliable public-domain or official source and cite the work.
- Distinguish quotation from paraphrase. Do not invent direct patristic quotations.
- Put the selected direct quotations in the final `Full Patristic and Saintly Texts` section, even if a shorter form already appears in the witness table.
- Make connections across the whole Mass: Introit, Collect, Epistle, Gradual/Alleluia when used, Gospel, Offertory, Secret, Communion, Postcommunion.
- Keep tables readable. Add content, but avoid turning one cell into a full essay.
- Regenerate PDFs with `make`, then run `make clean` before committing.
- Commit meaningful changes in the nested `liturgical-year` repository.
