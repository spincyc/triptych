# New Advent delivery drift: registered artifacts no longer reproduce — 2026-08-28

A research lane reported that the registered `De viris illustribus` artifact
reproduces at 154,105 bytes against a recorded 154,108. The three bytes are
real. They are not a transcription edit, not a repository regression, and not
peculiar to Jerome: every registered `newadvent.org` artifact has drifted, and
the cause is the host's own page furniture, not any translated text.

## The reported record

`artifact.jerome.de-viris-illustribus.english-richardson-npnf2-3.newadvent-2708-85587778`
is `storage = "remote"`. No bytes of it are stored here; the digest attests what
`https://www.newadvent.org/fathers/2708.htm` returned on 2026-07-25.

| | recorded 2026-07-25 | re-fetched 2026-08-28 |
|---|---|---|
| bytes | 154,108 | 154,105 (−3) |
| sha256 | `85587778…3b4309` | `e079587c…be4a580c` |

## The drift is the host's, and the text is intact

Six non-New-Advent remote artifacts registered in the same window were
re-fetched and reproduced **digest-identical**, so the acquisition procedure
records exact response bytes and the 154,108 was correct when taken.

Across all 70 registered New Advent artifacts (40 `remote`, 30 `restricted`),
**none** now reproduces:

| Delta against the recorded byte_size | Artifacts |
|---|---|
| −3 bytes | 61 |
| −2 bytes | 5 |
| −1 byte | 3 |
| HTTP 404 | 1 |

A near-constant loss that is independent of page size (7 KB to 154 KB) and of
section (`fathers/`, `summa/`, `cathen/`) is a change to the shared header and
footer, not to any work. Responses carry `x-mod-pagespeed` behind Cloudflare,
so the markup is machine-rewritten on delivery and its furniture is expected to
churn.

The translated text is unaffected. Chapter 2 of the live page, with markup
stripped, still contains the repository's checked transcription verbatim, and
that derived artifact — `…ch-2-gospel-of-the-hebrews-checked-text-f0f92de5`,
`storage = "tracked"` — reproduces exactly at 331 bytes and digest
`f0f92de5…0c8842d`. Distinctive wording quoted by other guides from chapters 5,
12, and 53 is also still present.

## Verdict: the recorded digest stands; the record is not re-pinned

The digest is an accurate historical attestation of a dated retrieval, and it
is the only surviving evidence of what was read. Overwriting it with today's
bytes while `retrieved = "2026-07-25"` remains would replace a true record with
a false one, and would do so for a delivery fingerprint that nothing published
depends on: consuming bindings cite the passage and the tracked transcription,
never the remote byte count.

No `artifact.toml` is amended by this review. Re-pinning is a single decision
about this provider across all 70 records, taken deliberately with a fresh
`retrieved` date — not a repair to one Jerome record.

## Two defects this review found and did not fix

**A registered source is dead.**
`artifact.basil-of-caesarea.de-spiritu-sancto.jackson-npnf2-8-newadvent-web-2026-07-28.complete-html`
records 51,171 bytes for `https://www.newadvent.org/fathers/320216.htm`
"chapter 16 page". That URL now returns 404, and the whole per-chapter
`3202xx` scheme returns 404. The complete work is served instead as one page at
`fathers/3203.htm` (295,456 bytes), which does contain Chapter 16. Deciding
what this edition should now point at is a source judgement, left open.

**This class of drift is structurally invisible.** `source-library validate`
passes clean and never re-fetches remote artifacts, and
`research-staleness-v1.toml` hashes the `artifact.toml` record rather than the
bytes it describes. Nothing in the gate battery would have reported any of the
above.
