# Corpus browser research synthesis

## Evidence boundary

This A1 synthesis records sources checked on 2026-08-08. Facts below are
observations of the cited official specifications, documentation, or live
services. Recommendations are Triptych inferences. Product interfaces and
counts are mutable; the access date remains part of each use.

The research is design evidence, not a source-library corpus. It therefore
lives in guidance rather than `src/sources/`. No third-party text, screenshot,
or asset is redistributed by this record.

## Borrow, reject, exceed

| Precedent | Borrow | Reject or exceed |
| --- | --- | --- |
| Sefaria | passage-anchored apparatus, original/translation controls, typed citation jump, facets, account-optional reading | category-as-relationship, opaque or missing edge types, unlimited panes, mobile chrome; Triptych edges stay typed and auditable |
| Scaife/Perseus | version-qualified passage identity, visible source revision, machine-readable passage services, contextual tools | numeration-only alignment, persistent three-pane layout, side-by-side mobile, foreign IDs as Triptych identity |
| Corpus Thomisticum | conventional locus plus corpus passage ID, exact fragment destinations, lexical search to passage | mutable latest-only citations, opaque filenames, siloed tools, non-shareable search state |
| IIIF/DigiVatLib | logical-to-physical navigation, Manifest/Canvas/Range distinctions, typed external actions | treating Manifest or Canvas as Triptych Artifact, inferring rights from public access/CORS, implementing a heavy viewer before a real witness requires it |
| TEI/CTS | separate file/source/edition descriptions, declared citation schemes, work/version/passage distinctions | migrating to TEI for conformance, minting unregistered `urn:cts:triptych`, equating CTS exemplar with exact artifact |
| WorldCat/JSTOR/HathiTrust/Internet Archive | work clustering with exact editions, applied filters, stable item identity, discoverable unavailable records | opaque representative-edition choice, metadata-poor tiles, inert zero states, semantic modes that disable structured facets |
| GOV.UK/USWDS | task-first entrances, restrained navigation, front-loaded labels, 60–72-character prose, strong focus | government branding, indiscriminate anchor menus, equal top-level weight for every domain |
| Holy See/USCCB | explicit authority, edition/date/language/locus, legitimate alternatives, operational citations | visual-only headings, incomplete anchors, hidden edition identity, crowded mobile utilities, branding as a proxy for authority |
| WAI/WCAG 2.2 | native links/buttons/dialogs, named landmarks, focus return, reflow, concise status, 24px AA floor | treating APG examples as proof; Triptych retains stronger 44–48px primary targets, full-focus visibility, forced-color and reduced-motion gates |
| Pagefind/DocSearch | lazy static index, worker search, compact modal, grouped typed results, keyboard precedent | selecting an engine before corpus benchmarks, crawler-only search, hosted dependency by default, personalization or AI answers |

## Durable conclusions

1. Identity needs four independent levels: conceptual Work, Source Edition,
   exact Artifact, and Passage, with Segment retained where it controls a
   passage. Provider-qualified publication treatments are a different axis and
   must not be confused with bibliographic Source Editions.
2. A stable human citation, internal object ID, external alias, and rendered
   URL are related but distinct. Displayed words require edition qualification;
   immutable research citations additionally need a revision/as-of identity.
3. Search and Related are object routers, not answer engines. Exact citation and
   ID recognizers precede lexical matching; ambiguity remains explicit; no
   nearest canon, verse, formulary, edition, or witness is substituted.
4. Context should be progressive: human identity and material availability are
   immediate; full rights basis, digest, derivation, retrieval, and technical
   provenance are one deliberate action away. A digest proves byte identity,
   not authority, correctness, verification, or reuse permission.
5. Wide contextual rails are permissible only when they do not move or narrow
   the primary text. Narrow layouts become one coherent reading order with
   modal or in-flow apparatus, not squeezed desktop panes.
6. The static core remains the architectural constraint. Generated indexes and
   relationship projections must be public-only, versioned, additive, lazy,
   and route-aware. GitHub Pages supplies no API, rewrite, request-time policy,
   or state-specific metadata for hash routes.
7. Ecclesial credibility comes from truthful authority, jurisdiction,
   recension, source, options, and limits—not parchment, heraldry, ornament,
   faux manuscript effects, or institutional imitation.

## Search feasibility conclusion

A4 may prototype a visible **Jump** dialog over synthetic static destinations.
It must not call that fixture global corpus search. A production feature earns
the name only after J1 builds a public-only typed fixture spanning
publications, Source objects, Scripture, commentary, formularies, acts, and
canons, then measures compressed bytes, chunk/request counts, cold/warm
initialization, p50/p95 query latency, main-thread time, worker memory,
mixed-language behavior, exact/ambiguous citations, mobile interaction, and
rights no-leak assertions. Pagefind custom records are a feasibility
hypothesis; no library is selected by A1-A4.

## IIIF disposition

Design for future typed external Manifest, Canvas, image-service, viewer, and
Content-State identities, but do not implement IIIF in the foundation. A live
Vatican example was Presentation/Image API 2, carried sparse Range metadata and
no manifest licence, and served mutable/no-store responses. Public technical
access did not grant redistribution permission. Any later integration must pin
retrieval/version evidence, preserve Triptych IDs, and undergo artifact-specific
rights, accessibility, performance, privacy, and failure review.

## Checked primary sources

All links were checked 2026-08-08 unless a more specific date is stated.

- Sefaria: [Library](https://www.sefaria.org/texts),
  [Resource Panel](https://help.sefaria.org/hc/en-us/articles/18472472138652-Quick-Guide-Meet-the-Sefaria-Library-Resource-Panel),
  [search](https://help.sefaria.org/hc/en-us/articles/20334027958684-The-Sefaria-Library-Search-Bar-How-to-Search-for-Sources),
  [Text References](https://developers.sefaria.org/docs/text-references), and
  [Links API](https://developers.sefaria.org/reference/get-links).
- Scaife/Perseus: [Scaife Viewer](https://scaife.perseus.org/),
  [Iliad record](https://scaife.perseus.org/library/urn:cts:greekLit:tlg0012.tlg001/),
  [passage reader](https://scaife.perseus.org/reader/urn:cts:greekLit:tlg0012.tlg001.perseus-grc2:1.1-1.7/),
  [CapiTainS guidelines](https://capitains.org/pages/guidelines), and
  [Perseus text help](https://www.perseus.tufts.edu/hopper/help/texts).
- Corpus Thomisticum: [project](https://www.corpusthomisticum.org/),
  [Opera Omnia](https://www.corpusthomisticum.org/iopera.html), and
  [representative passage](https://www.corpusthomisticum.org/sth1001.html#28236).
- IIIF/Vatican: [DigiVatLib](https://digi.vatlib.it/about),
  [live manifest](https://digi.vatlib.it/iiif/MSS_Vat.lat.6251/manifest.json),
  [Presentation API 3](https://iiif.io/api/presentation/3.0/),
  [Image API 3](https://iiif.io/api/image/3.0/), and
  [Content State 1](https://iiif.io/api/content-state/1.0/).
- TEI/CTS: [TEI Header](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/HD.html),
  [TEI reference systems](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/CO.html),
  [CTS URN specification](https://cite-architecture.github.io/ctsurn_spec/),
  [RFC 8141](https://www.rfc-editor.org/rfc/rfc8141.html), and
  [IANA URN registry](https://www.iana.org/assignments/urn-namespaces/urn-namespaces.xhtml).
- Catalogues: [WorldCat grouping](https://help.oclc.org/Discovery_and_Reference/WorldCat_Discovery/Search_in_WorldCat_Discovery/020Filter_search_results),
  [JSTOR facets](https://support.jstor.org/hc/en-us/articles/4405598751255-Searching-Using-Filters-and-Facets),
  [Internet Archive search](https://archivesupport.zendesk.com/hc/en-us/articles/360018359991-Search-A-Basic-Guide), and
  [HathiTrust searching](https://hathitrust.atlassian.net/wiki/spaces/GS/pages/2386919535/Searching%2Bthe%2BCollection).
- Public-service design: [GOV.UK layout](https://design-system.service.gov.uk/styles/layout/),
  [GOV.UK navigation](https://www.gov.uk/guidance/content-design/navigation),
  [USWDS typography](https://designsystem.digital.gov/components/typography/), and
  [USWDS search](https://designsystem.digital.gov/components/search/).
- Accessibility: [WCAG 2.2](https://www.w3.org/TR/WCAG22/),
  [APG landmarks](https://www.w3.org/WAI/ARIA/apg/practices/landmark-regions/),
  [modal dialog](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/),
  [disclosure](https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/), and
  [combobox](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/).
- Search implementations: [Pagefind](https://pagefind.app/),
  [Pagefind API](https://pagefind.app/docs/api/),
  [Pagefind custom records](https://pagefind.app/docs/py-api/), and
  [Algolia DocSearch](https://docsearch.algolia.com/docs/packages/js/getting-started/).
- Ecclesial references: [Holy See encyclicals](https://www.vatican.va/content/francesco/en/encyclicals.html),
  [Catechism index](https://www.vatican.va/archive/ENG0015/_INDEX.HTM),
  [USCCB Luke 4](https://bible.usccb.org/bible/luke/4), and
  [USCCB daily readings](https://bible.usccb.org/bible/readings/memorial-saint-dominic-priest).

## Research limitations

Several commercial/catalogue search result pages were rate-limited or blocked,
so their mobile/result claims rely only on current first-party documentation
and directly reachable item pages. No native mobile application was installed.
Headless Chromium observations do not replace real device or assistive-
technology review. Mutable interface counts are dated snapshots, not corpus
completeness claims.
