# Remote chronology deliveries re-fetched, 2026-10-01

Known issue KI-014: five registered remote deliveries that chronology claims
cite no longer reproduced their registered SHA-256 when a proper's research
lane fetched them on 2026-09-30, so the leaves bound them at `cataloged` only.
Each was fetched again here, over HTTPS with `curl`, hashed before use, and
compared; three further fetches of each New Advent page the same day returned
the same bytes. No source text passed through a language model.

`guidance/sources.md` prescribes the disposition: artifacts are immutable by
identity, changed bytes receive a new artifact record, and consumers remain
pinned until reviewed. This record is that review. It asserts nothing about
Scripture and no tool reads it.

## What was fetched

| Page | Cited by the corpus | Registered | Fetched 2026-10-01 | Current delivery |
| --- | --- | --- | --- | --- |
| CE `05485a` Ephesians | `…volume-5.new-york-1909.newadvent-05485a-66d722ae` | `66d722ae…`, 67 653 B (2026-08-26) | `e144286e…`, 67 294 B | already registered: `…newadvent-05485a-e144286e` (2026-09-05), reproduced byte for byte |
| CE `10057a` Matthew | `…volume-10.new-york-1911.newadvent-10057a-e7b6ccef` | `e7b6ccef…`, 95 482 B | `d1a6e39a…`, 95 123 B | registered now: `…newadvent-10057a-d1a6e39a` |
| CE `11567b` St. Paul | `…volume-11.new-york-1911.newadvent-11567b-bff0dda8` | `bff0dda8…`, 150 014 B | `7c2dd20c…`, 149 655 B | registered now: `…newadvent-11567b-7c2dd20c` |
| CE `14530a` New Testament | `…volume-14.new-york-1912.newadvent-14530a-0a19aa2c` | `0a19aa2c…`, 77 046 B | `4247717c…`, 76 687 B | registered now: `…newadvent-14530a-4247717c` |
| NABRE Psalms introduction | `passage…english-usccb-web-2026-07-28.psalms-introduction` (artifact `edaba4b4…`, 74 094 B, 2026-07-28) | as cited | `ee7d086f…`, 74 081 B | already registered: `…english-usccb-web-2026-07-28.psalms-introduction-2026-09-28`, reproduced byte for byte |

Every New Advent delivery is exactly 359 bytes shorter than the one
registered, the class `…newadvent-05485a-e144286e` records, and the host still
sends an `x-mod-pagespeed` header.

## Whether what the claims rest on changed

**The four Catholic Encyclopedia articles did not.** Each registered delivery
has its article text retained beside it as a tracked `-article-text`
derivative, extracted from those exact bytes by the transformation that
derivative's record states. Re-applying that transformation, by script, to
the 2026-10-01 bytes reproduces each retained file byte for byte:

| Retained article text | SHA-256 | Reproduced from the 2026-10-01 delivery |
| --- | --- | --- |
| `…newadvent-05485a-66d722ae-article-text` | `c101da65d2c3cd40ef206bf013e2e3aae5f544b413a3006fcdd8f4909b566b1b` | yes |
| `…newadvent-10057a-e7b6ccef-article-text` | `3d9a35cc773f774ed3b423c890956ba655c61ceb7096fbd7c01a197f062168c2` | yes |
| `…newadvent-11567b-bff0dda8-article-text` | `c0f08396eca9b37415747eb06790ce986acc5bb650b2675d76af8449458bce1d` | yes |
| `…newadvent-14530a-0a19aa2c-article-text` | `c4e12a4a6127e8af8b7ac8e2176448f78a2be2cb2080ab5ffb6f885f8fcaa259` | yes |

The whole difference therefore lies in New Advent's page apparatus outside
the article. Which part of it is inference: the earlier bytes were not
retained, so this is not a diff.

**The NABRE Psalms introduction is restricted**, so nothing of it is retained
and no byte comparison with the 2026-07-28 delivery is possible. The
2026-10-01 delivery was read locally: it still says that no psalm can be dated
with certainty and that none is as late as the Maccabean period, about 165,
which is all `critical.psalms.latest-composition-boundary` rests on. The
2026-09-21 passage record on artifact `…psalms-intro-ccbbc6b9` verified the
same on that date.

## Disposition

- **Registered** the three New Advent deliveries the library did not hold, as
  `remote` artifacts under the rights basis their editions already state. Each
  record names the retained article text it reproduces. No second extraction
  was retained, because it would put the same words in the tree twice.
- **No claim was rebound.** The corpus claims stay pinned to the deliveries
  they were read from: the words they quote are the retained extraction of
  those bytes, and that extraction is now shown to be what the host serves
  today. Rebinding would change no word a claim rests on, and would leave the
  leaves' own source bindings, which name the cited artifacts, naming sources
  their records no longer cite.
- **What a leaf can now bind.** A proper that wants an `acquired` or
  `inspected` binding for one of these sources has a reproducible delivery to
  bind (the current artifacts above), and, offline, the tracked
  `-article-text` derivative whose hash any reader can check. Raising a leaf's
  binding is that leaf's own revision.
- A remote delivery is a hash of what a host served once; it is not a promise
  that the host will serve it again (`guidance/sources.md`). The retained
  derivative is what makes these claims checkable without the network, and it
  is unchanged.
