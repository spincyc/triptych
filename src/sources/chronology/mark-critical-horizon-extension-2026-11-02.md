# Mark: a tentative critical composition horizon

This extension adds `critical.gospel-of-mark` under `catholic-critical-v1`.
The source's tentative modern proposal supplies an open lower bound after
A.D. 70, with perhaps and shortly retained. It supplies no terminal year,
closed interval, secure date, consensus, or date for a predecessor text.

## Source and scope

The complete official NABRE Mark introduction and divisions were independently
read in the registered 2 November 2026 web-tool text extraction and reopened
at <https://bible.usccb.org/bible/mark/0>:

- artifact: `artifact.united-states-conference-of-catholic-bishops.new-american-bible-revised-edition.english-usccb-web-2026-11-02.mark-introduction-web-text-272bcce7`;
- exact extracted-text SHA-256: `272bcce72d0d78287acadd7157648f2444589a4900f1433e148eb25a5410e44a`;
- extent: 13,635 bytes; source lines 47–84 contain the introduction and divisions;
- controlling loci: source lines 62–64, 72–75, and 81–84.

Line 75 reports the modern proposal, including an unknown Hellenistic Jewish
Christian author and a possible Syrian location. Its dating phrase is
“perhaps shortly after the year 70.” The preceding paragraph separately
reports the traditional Roman account. The new title identifies the tentative
proposal, the raw label preserves the quoted phrase, and the structured
boundary's statement preserves its uncertainty in generated displays.

Lines 62–63 distinguish the Gospel ending at 16:8 from endings attached by
other hands; the divisions repeat that distinction. The new unit therefore
spans Mark 1:1–16:8. The longer ending at 16:9–20 and the other appended
endings receive no composition date from this claim. This scope follows the
source's explicit textual distinction rather than a newly inferred partition.

The controlling representation is an authenticated extracted-text delivery,
not acquired raw HTML or a printed-page collation. Direct HTTP acquisition
returned 403 according to its registered provenance. Its protected body is
not retained in Git, and no source metadata or payload was changed here.
The quotation test declares exactly this artifact's single quoted phrase
unreopenable from an ordinary checkout, with its hash and inspection limit;
it introduces no general skip for USCCB material.

## Query and consumer impact

Public CLI queries were compared before and after at Mark 1:1, 11:24, 16:1,
16:8, 16:9, and 16:20 under the critical, traditional, and comprehensive
profiles. The first four critical answers gain the tentative composition
bound; 16:9 and 16:20 retain their exact-witness attestation answer.

An exhaustive comparison of all 677 canonical Mark loci against the saved
pre-extension corpus found zero traditional or default answer/status changes.
The new critical composition claim reaches 665 loci, and all twelve loci of
16:9–20 have unchanged critical answers. The default `coverage.tsv` rebuild
is byte-identical at 1,898 rows. All prior textual units, including every
Jeremias unit, are semantically unchanged.

Both providers' comparison declarations were inventoried: none selected an
existing Mark composition comparison. The active GPT Proper 66 queries
Mark 11:24 and may now explicitly select this subject for its comparison;
its owner must add that selection and regenerate after independent review.
The two existing postconciliar `pc-s55-twenty-ninth-sunday-in-ordinary-time-year-a`
records, GPT and Claude, query Mark 10:45 under the comprehensive profile;
their default answers are unchanged. No publication file was edited.

## Verification

The 34 focused hard-case and source-quotation tests pass. Authored chronology
validation and `make check-scripture-chronology` pass. The gated review manifest
was regenerated against its unchanged pinned base, from 532 to 533 rows;
regeneration records no acceptance or review verdict. The full 271-test
chronology suite passes 270 tests and reproduces only the previously established
Psalm-attribution scope expectation failure; its five extra Psalm scopes are
unchanged. Independent source review remains separate from these checks.
