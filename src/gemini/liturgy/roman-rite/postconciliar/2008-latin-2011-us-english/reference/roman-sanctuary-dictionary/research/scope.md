# Scope — Postconciliar Illustrated Dictionary of the Roman Sanctuary

- **Family owner root:** `src/gemini/liturgy/roman-rite/postconciliar/2008-latin-2011-us-english/reference/roman-sanctuary-dictionary`
- **Governing profile:** `guidance/liturgy/postconciliar-pictorial-dictionaries.md` (with `guidance/editorial.md`, `guidance/the-shape.md`, `guidance/document-schemas.md`, `guidance/web-editions.md`, and `guidance/liturgical-text-publication-policy.md`)
- **Document kind & type:** `pictorial-dictionary-postconciliar` / `liturgy-reference-v1`
- **As-of date:** `2026-11-25`

## Controlling Edition, Territory, and Jurisdiction

1. **Universal Latin typical edition:** *Missale Romanum*, *editio typica tertia* (CDWDS decree *Missale Romanum*, 20 April 2000; published 2002, Typis Vaticanis) and its *reimpressio emendata* (2008, announced in *Notitiae* 44 [2008], nos. 503–504), incorporating the *Institutio Generalis Missalis Romani* (IGMR / GIRM).
2. **Approved territorial English edition and adaptations:** *The Roman Missal, Third Edition*, for use in the Dioceses of the United States of America (CDWDS confirmation 26 March 2010; USCCB GIRM adaptations confirmed 24 July 2010; mandatory effective First Sunday of Advent, 27 November 2011), incorporating the official USCCB online GIRM emendations through 22 October 2021 (Prot. n. 228/20 on no. 54; Prot. n. 394/21 / *Postquam Summus Pontifex*, 22 October 2021), alongside Pope Francis's Motu Proprio *Spiritus Domini* (10 January 2021, amending CIC can. 230 §1).
3. **Associated postconciliar universal and U.S. particular law:** *Codex Iuris Canonici* (1983), *Ordo lectionum Missae* (*editio typica altera*, 1981), *Caeremoniale Episcoporum* (*editio typica*, 1984), *De sacra communione et de cultu mysterii eucharistici extra Missam* (1973), *Ordo benedicendi oleum* (1970), *Redemptionis Sacramentum* (25 March 2004), USCCB *Norms for the Distribution and Reception of Holy Communion under Both Kinds in the Dioceses of the United States of America* (2002; revised 2011; reflecting October 2006 CDWDS non-renewal of the U.S. EMHC purification indult), and USCCB *Excerpts from the Roman Missal* ("Book of the Chair", 2018).
4. **1962 comparison horizon:** *Missale Romanum*, *editio typica* (1962) with *Rubricae Generales Missalis Romani* (1960/1962) and *Ritus Servandus*, consulted strictly for direct edition-to-edition counterpart collation — never imported as postconciliar law.

## Publication Family Architecture

One canonical structured inventory (`shared/objects/**/*.toml`) and one shared monochrome artwork asset set (`shared/artwork/graphite/*.png`, ten 8-bit grayscale plates) drive four coordinated publication leaves via a deterministic Python validator and TeX projection engine (`shared/generate_editions.py`):

1. **`comprehensive/`** — Comprehensive Adult Reference Dictionary (40 current sanctuary objects across 7 functional categories + 3 historically superseded postconciliar forms in a strictly separated chronological section + full terminal apparatus).
2. **`altar-server/`** — Altar Server Visual Dictionary (all 40 current sanctuary objects a server encounters, including clergy-reserved items the server recognizes without touching, emphasizing handling boundaries, handoffs, confusion risks, and immediate safety).
3. **`sacristan/`** — Sacristan Visual Dictionary (all 40 current objects framed for preparation, assembly, placement, linen folding, liturgical-book setting, seasonal color changes, and vessel care).
4. **`general-reader/`** — General Reader Visual Dictionary (concise illustrated survey of all 40 current objects plus the 1962 continuity summary and separated historical transitions).

## Bounded Corpus Limits

This initial alpha corpus covers forty core objects of Mass and closely joined parish rites together with three historically superseded postconciliar transitions (1967–2011). Deferred categories — including episcopal and pontifical insignia, dedicated Paschal Triduum apparatus, funeral furnishings, and specialized rites of ordination and dedication — are documented explicitly in `research/remaining-gaps.md` and stated honestly in the terminal scope appendix of every edition.

## Rights and Non-Authority Boundary

Modern official postconciliar liturgical books (LEV Latin *Missale Romanum*, ICEL/USCCB English *Roman Missal* and GIRM, CCD *Lectionary*) are rights-restricted. All reader-facing prose in this family is original analytical description and paraphrase, avoiding verbatim reproduction of protected liturgical texts and honoring the 29 November 2026 effective date of the 2025 USCCB *Guidelines for the Publication of Liturgical Books*. Scripture quotations, where included, follow the public-domain Douay–Rheims (Challoner) witness in `src/sources/bibles/douay-rheims/`. All ten monochrome graphite plates are original project-created assets licensed under CC BY 4.0. This work is a study and preparation reference, not an official liturgical book or ecclesiastical enactment.
