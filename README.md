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

