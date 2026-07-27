# Independent exact-snapshot review

Date: 27 July 2026
Verdict: **PASS**

## Snapshot

- Source-tree aggregate SHA-256 before this review record:
  `ba7c0ebe777388cac8b5737894a688f11f4807abecba11a74361a09a6948b3ba`
- Installed PDF SHA-256:
  `d156647962b94febbd3fa60b7ac7d163e21cb89a7273747c4e95df851f3b1dd1`
- Installed PDF: 38 letter-size pages, 579,180 bytes
- The installed snapshot differs from the visually reviewed
  `cd3725e6cd1c7b15c8d40d64ef0403a81241e6cf4902deb82813485cd8bddd90`
  snapshot only by the corrected generation timestamp. Page count, content,
  layout, fonts, and image resources are unchanged.
- `main.tex` SHA-256:
  `1ea777070b4c6f4c4d9c5536f954c9f81111673951d3f941cd6d5adccaac5433`
- `source-bindings.toml` SHA-256:
  `69059b2e07b9395206d3d219fe0393094aa6f1413992a24c1eaf13596874c25d`

The build log is clean of fatal errors, undefined references, and overfull or
underfull box warnings. Fresh review rasters were generated with
`scripts/pdf-review`; all 38 pages were inspected. No clipping, collision,
unreadable type, broken running matter, or visibly defective page was found.
Page 38 ends naturally with publication metadata and usable white space.

## Controls that pass

- The forty-two former appointed-text transcriptions have been reduced to
  focused locators. The work no longer functions as a recitation substitute.
- The rights audit separates inherited prayer wording, the 1962 edition and
  rubrics, the Saint Joseph insertion, and the CMAA/ABBYY artifact. It reaches
  no blanket public-domain conclusion and keeps the facsimile remote with
  rights unresolved.
- The Communion discussion now distinguishes the controlling 1962 Missal
  nn. 502–503 from the registered 1925 Ritual used as a historical control. It
  expressly records the absence of an exact checked 1952 Ritual witness.
- The principal earlier errors concerning the Creed recension, Saint Joseph
  word count, Canon secrecy, the Milanese comparison, typography, epiclesis,
  `offerimus`/`offerunt`, and the presence of a congregation have been
  corrected or bounded.
- The second-pass records distinguish direct evidence, bounded comparison,
  unresolved questions, and leads not yet admitted as publication evidence.

## Resolution of the former hold

The targeted record `final-five-claims-second-pass-2026-07-27.md` accurately
states the evidence ceilings applied to the five residual claims. Exact
search and contextual reading confirm that the corrected publication:

1. reports only the bounded procedural change established by the 1925 Ritual
   and the 1962 Missal, without calling every element recent or the remainder
   unchanged since 1570;
2. reports the rubrical voice distinctions without equating `secreto` with
   necessary inaudibility or assigning an undocumented purpose to them;
3. limits the Lucan Lord's Prayer observation to the checked 1861 and 1962
   witnesses;
4. describes the first-person singular grammar of the priest's Communion
   prayers without claiming uniqueness; and
5. removes the unsupported universal statement about Eastern anaphoras.

The source library validates, the source diff passes whitespace checking, and
no theological, historical, source, rights, Rituale-provenance, or visual
blocker remains in this reviewed snapshot. This pass concerns the source and
built PDF identified above; installation, cataloging, and exact-snapshot
release authorization remain separate repository actions.
