# Ordinary priestly vestment source bindings

Checked 5 November 2026. This repair covers only the existing amice, alb,
cincture, maniple, priest's stole and chasuble records. It registers the
previously unresolved material-culture references and makes their printed
bibliography reproducible. It does not close a vestment category or renew
approval of the illustrations or six rendered editions.

## Casanowicz: title, edition and page

The cited United States National Museum Bulletin 148 is Immanuel Moses
Casanowicz's *Collections of Objects of Religious Ceremonial in the United
States National Museum* (Washington: United States Government Printing
Office, 1929). “Ecclesiastical Vestments” in the former unresolved work ID
was not the book's title. The new canonical owner is
`src/sources/works/immanuel-moses-casanowicz/collections-of-objects-of-religious-ceremonial/`.

The search `Casanowicz ecclesiastical vestments bulletin 148 1929 Smithsonian`
identified the Smithsonian volume. Both its legacy PDF route and current
repository bitstream route returned HTTP 403 to direct acquisition. The
corresponding [Internet Archive item](https://archive.org/details/bulletinunitedst1481929unit)
supplied the complete 302-page PDF. Its exact hash, byte count and download
route are in the remote artifact manifest. No source PDF or text derivative
is retained in Git.

The title and imprint on PDF page 7 and all of printed page 30 on PDF page 44
were inspected as images. The uncorrected PDF text layer of printed pages
29–31 was read for context; it was a locator, not the image-collation result.
The six bindings now identify their individual numbered descriptions:

| Object | Printed page 30 item | Bounded material-culture support |
| --- | ---: | --- |
| Amice | 2 | Linen cloth, corner ties and shoulder covering. |
| Alb | 3 | Loose white linen garment reaching to the feet. |
| Cincture | 4 | Cord used to bind the alb. |
| Maniple | 5 | Short cloth strip worn on the left wrist. |
| Stole | 6 | Long band around the neck, crossed and secured by the girdle. |
| Chasuble | 7 | Outer garment, head opening and open sides. |

This catalogue remains secondary material-culture context. In particular,
it describes an amice cross at the upper edge, tasselled cincture ends and
three maniple crosses. These particulars are not adopted as universal 1962
requirements. The revised amice and maniple cross claims retain their own
Missal bindings; the catalogue does not replace them. Its origins, symbolism,
dimensions and historical color account are outside this verification.

## Metropolitan Museum: exact objects

The old `43.22.4a-d` group reference is now resolved to the particular object
used by each record. The chasuble's public description expressly identifies
the associated maniple, burse and stole; the maniple and stole also have their
own catalogue records.

| Dictionary reference | Exact accession and catalogue | Canonical work below `src/sources/works/metropolitan-museum-of-art/` |
| --- | --- | --- |
| Chasuble, French example | [43.22.4a; object 226962](https://www.metmuseum.org/art/collection/search/226962) | `chasuble-226962` |
| Maniple | [43.22.4b; object 226963](https://www.metmuseum.org/art/collection/search/226963) | `maniple-226963` |
| Priest's stole | [43.22.4d; object 226965](https://www.metmuseum.org/art/collection/search/226965) | `stole-226965` |
| Chasuble, Spanish example | [2009.300.2952a–c; object 157834](https://www.metmuseum.org/art/collection/search/157834) | `chasuble-stole-and-maniple-157834` |

Exact-accession searches for `43.22.4a`, `43.22.4b` and `43.22.4d`
resolved the separate French records. The API's retired search route returned
HTTP 410; the individual object endpoints remained available. Complete API
responses and one complete original photograph per object were acquired,
hashed and inspected. These are separately manifested remote artifacts under
each work's `2026-11-05-collection-record` edition. That date identifies the
consultation state, not the making of the vestments or the API's own
`metadataDate`, which remains separately recorded.

The public catalogue views identify the three French objects as nineteenth
century. They identify the Spanish ensemble as sixteenth-century embroidery
and seventeenth-century velvet, subsequently cut, patched and reshaped. The
acquired API responses have empty `culture` fields; the French and Spanish
labels were read in the public web catalogue, not inferred from those empty
fields. The attempted direct HTML download returned HTTP 429. Browser
retrieval made the catalogue text readable, but no exact raw HTML acquisition
or hash is claimed.

The photographed French maniple and stole show their distinct short and long
bands. Their widened ends, crosses, fringe and decoration are particular to
these objects. Both photographed chasubles are cut forms; they do not
independently establish the fuller Gothic half of the comparison plate.
The bounded Hirten check below supplies that comparison evidence. The
Spanish display arrangement, with accessories over the chasuble, is a museum
presentation and supplies no rule for vesting. The stole catalogue's inch and
centimetre dimensions are internally inconsistent; this repair adopts no
dimensions and makes no silent correction.

## Fortescue imprint correction and chasuble comparison

A follow-up check of the supposed 1917 line-art witness found a substantive
error in the July audit. The [Commons First Edition file](https://commons.wikimedia.org/wiki/File:The_Ceremonies_of_the_Roman_Rite_Described_(First_Edition).djvu)
identifies Internet Archive item `ceremoniesofroma00fort` as its source.
The complete offered PDF was acquired: 482 pages, 33,538,494 bytes, SHA-256
`5b267dc0ba963f7c04399e52950020559846945b66a8ab24b2b5c3edfa5adb07`.
Its title page, PDF page 3, was inspected and reads London, Burns & Oates
Ltd, MCMXVIII (1918). The 1917 imprimatur date is distinct from that imprint;
the Wikisource index's 1917 label does not override the scanned title.
The new `burns-oates-1918` edition and exact remote PDF artifact sit below
the existing Fortescue work. The existing 1917 edition and modern typeset
artifact are unchanged.

Printed pages 9–10 / PDF pages 43–44 were also inspected as images. Page 9
concerns church furniture. Page 10 describes the six priestly vestments in
prose. Neither page contains vestment line art, and neither supplies a
Roman/Gothic comparison. All six object records now bind their Fortescue
recognition source to the exact 1918 artifact at printed page 10 / PDF page
44. The local `src-…-fortescue-1917` keys are retained as historical
identifiers because the artwork custody manifest refers to them; their
resolved artifact and printed bibliography now identify 1918. This finding
supersedes the line-art and 1917-imprint description in
`research/priestly-vestments-alpha-audit-2026-07-28.md`; it does not erase the
usable prose descriptions or extend them into later ritual instructions.

The existing exact artifact for *Hirten Church Goods 1952* supplies the
missing comparison evidence:
`artifact.william-j-hirten-company.hirten-church-goods.hirten-1952.internet-archive-text-pdf-ccd22db7`.
The available complete 132-page PDF was rehashed and matched the registered
10,388,490 bytes and SHA-256
`ccd22db7a72a5b3e38a9e4bb9ff8fec03ebc31966d883edcfaf5e5be6d66dcb3`.
Its dated cover and printed pages 122–123 / PDF pages 124–125 were inspected
as images. The catalogue's product illustrations show fuller draped forms
(Nos. 9457, 9461, 9459, 9460 and 9462 on p. 122; No. 9455 on p. 123) and
narrower forms (No. 9458 on p. 122; Nos. 9451, 9453, 9454 and 9456 on p.
123). The tables explicitly offer Roman and Gothic chasubles; No. 9459
spells out both names. No. 9452 on p. 123 is a cope and is excluded.

The chasuble appearance claim now includes that exact Hirten artifact.
Taken with the museum photographs, these pages support the bounded
comparison of representative fuller Gothic and narrower Roman cuts. The
catalogue prices are not used, and the comparison does not reproduce a
particular product pattern or establish the artwork's individual front and
back ornament, neckline, ties, length or proportions. Those particulars
remain illustrative and nonprescriptive. This evidence repair does not
itself renew visual approval. Hirten's existing host-supplied rights record
and remote-storage boundary remain unchanged; no new clearance or scan
redistribution is claimed.

## Rights and verification boundary

The [Met Open Access policy](https://www.metmuseum.org/hubs/open-access) and
[API documentation](https://metmuseum.github.io/) were checked for the basic
data and public-domain image CC0 grant. Each acquired object response sets
`isPublicDomain` to true and names its own image route. The exact grant and
artifact identities are recorded centrally; no claim covers the entire web
page wrapper or curatorial prose. No museum image is imported into the
dictionary artwork by this repair.

All new artifacts remain remote metadata records. Reopening their exact
bytes requires the recorded public delivery; this change supplies no offline
pack. Inspection is bounded to the stated titles, pages, catalogue information
and four photographs, including the bounded Fortescue and Hirten checks
above. It establishes neither complete catalogue examination nor a new
ritual norm.

The source-library validator and dictionary inventory validator passed.
The source-note resolver was exercised with these six records and emitted
their exact edition references. Integration owns the shared inventory,
family-ledger refresh and final consumer-render checks.
