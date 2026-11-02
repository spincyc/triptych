# Papal catalogue and source-pipeline review

Reviewed on 2026-10-26, independently of the catalogue and acquisition
implementation. This review covers identity, discovery boundaries, source
registration, and rights-gated acquisition. PDF layout and the individual
historical publication approvals have separate reviews.

## Findings and dispositions

| Finding | Disposition |
| --- | --- |
| Genre filtering omitted acts indexed both as apostolic letters and as motu proprio. The original filter omitted *Traditionis custodes* and 51 other secondary motu-proprio memberships. | Corrected: `document_types` preserves overlapping source categories, and filtering considers every membership. The focused regression and a real-catalogue CLI query pass. |
| Identical unlinked headings from different interface pages received the same ID without being merged, making discovery fail. | Corrected: an unlinked row retains its source-page identity; only repeated rows from the same page merge. Independent reproduction now returns two distinct IDs for two source pages and deduplicates an exact repeated row. |
| A later selected acquisition batch discarded previous retained entries from the emitted manifest. | Corrected: acquisition receipts accumulate by identity, retain previously admitted witnesses, and continue reporting failures from the current attempt. The acquisition regression suite passes. |
| Latin-interface expansion exposed spelling, date-token, route, and erroneous-filename aliases. Filename similarity alone would also merge genuinely different acts. | Nineteen same-work URL pairs were checked against complete acquired deliveries; the reviewed alias record preserves their hashes and differences. *Quantum utilitatis* of 1964 and *Catholica Ecclesia* of 1976 remain distinct from other acts with those incipits. |
| The previously catalogued two *Divina disponente* routes represent the same Joan of Arc canonization act. | The independent early-publications review identified identical normalized text and AAS 12 (1920), pp. 514–529. The alias decision preserves both source genres and URLs. |
| Some index entries identify parts, front matter, incomplete deliveries, or multiple acts rather than one complete papal act. | The reviewed observations distinguish the three CCEO parts and its preface, an incomplete Russia delivery, and the Bogdánffy composite. These observations must govern canonical registration; index-item counts must not be presented as counts of distinct complete acts. |

Same-work identity does not imply identical wording. The two 2007 papal-election
deliveries differ in their operative paragraph; their URLs and textual variation
must survive the identity merge. The *Ecclesia in Urbe* alternate delivery has
substantial OCR and layout defects. The Messico alternate has Italian headings
before the Latin act; its operative wording and dating clause identify the same
15 November 2005 act.

The Bogdánffy delivery contains the acts concerning Szilárd Bogdánffy
(29 October 2010), Barbara Maix (6 November 2010), and Ioannes Scheffler
(3 July 2011), including journal running matter. Its Latin-index label instead
names André Bessette. Treating the response as a single complete letter would
misidentify its extent and attribution.

## Evidence and verification

Six complete live index responses were independently retrieved and compared
with the catalogue. Their item counts and all linked document URLs agreed:

| Official index | Rows |
| --- | ---: |
| [Benedict XIV, English interface](https://www.vatican.va/content/benedictus-xiv/en.html) | 43 |
| [Leo XIII, encyclicals](https://www.vatican.va/content/leo-xiii/en/encyclicals.index.html) | 86 |
| [Pius XI, encyclicals](https://www.vatican.va/content/pius-xi/en/encyclicals.index.html) | 33 |
| [Francis, apostolic letters](https://www.vatican.va/content/francesco/en/apost_letters.index.html) | 111 |
| [Francis, motu proprio](https://www.vatican.va/content/francesco/en/motu_proprio.index.html) | 75 |
| [John Paul II, apostolic constitutions](https://www.vatican.va/content/john-paul-ii/en/apost_constitutions.index.html) | 623 |

The identity review retrieved 106 complete document responses: all 78 newly
discovered Latin-interface records and selected existing counterparts. No
response fetch or document-body extraction failed. This establishes the stated
comparison boundary, not whole-corpus textual verification. Raw modern
responses remain outside tracked inputs; the durable alias observations retain
exact source hashes and intelligible reasons.

The focused verification commands passed after the three implementation
repairs: 27 catalogue tests and 13 source-acquisition tests.

After the reviewed aliases were applied, the three-interface candidate contains
2,814 source-index records across 237 requested pages. Six historical Latin
root URLs return not-found and remain reported; their English/Italian roots
are separate coverage records. The candidate preserves 58 date-conflict records
and 57 unresolved dates. Its roles distinguish four CCEO constituents, one
three-act composite, and one index mislink. The remaining `whole-work` role is
the provisional index classification, not a whole-text verification event.
The catalogue SHA-256 at this review checkpoint is
`1fd5a762bbe46ec5de2321e6126c2073e20fd07d97402b0f05f633b6de4ae37e`.

```sh
python3 -m unittest discover -s tools/tests -p 'test_papal_documents.py'
python3 -m unittest discover -s tools/tests -p 'test_papal_sources.py'
tools/papal-documents list --type motu-proprio --json
```

Review of the acquisition code confirmed that an old act date is only a
candidate filter. Promotion requires exact HTML and normalized-text hashes,
identified historical publication evidence, an original-Latin assertion, and a
United States public-domain basis. An unapproved candidate remains outside
tracked source payloads. Exact delivery URLs reuse existing canonical works;
ambiguous existing ownership raises an error rather than merging by incipit.
The initial catalogue had no existing work missed solely through an alternate
URL already recorded in its `url_aliases`.

## Remaining limits

The catalogue is an inventory of the named index boundary. It does not prove
all historical papal acts have been recovered, every delivery is complete,
every title is correct, every URL-language label matches every body, or every
source-index item is an independent work. Conflicting dates and filename-only
dates remain explicit. Ordinary correspondence, journal segmentation,
historical collections, rights clearance, and full-text collation retain their
own recorded boundaries. Successful parsing or metadata registration grants no
new publication permission.
