# Catena composition-date amendment — 2026-10-23

The coordinator adopted an explicit **Composition date not established** class
for otherwise admissible checked commentary. This changes the Catena's date
admission contract and presentation; it supplies no invented composition year.
The accepted backend, reader and source-data patches are identified in
[the final freeze record](catena-phase2-final-freezes.json). The independent
[source-contract check](catena-phase2-source-independent.json) preserves all
1,356 earlier rows and verifies the three additional rows with no ordinary
admission errors. Those are bounded source and patch-review findings; final
integrated generation, reader checks and publication remain separate events.

## Contract

An undated fragment explicitly declares `composition_date_unestablished` as a
nonempty plain-text statement of the actual reviewed evidence and its limit.
Missing or malformed dates do not create this class. The declaration is
mutually exclusive with a numeric fragment `text_date` or a numeric year in
the work's `composed`. An old `text_date_basis` without its integer override
remains invalid. Later establishment of a work date requires review and removal
of a stale unestablished-date declaration.

The emitted representation is `date: null`,
`composition_date_status: "unestablished"` and the trimmed statement as
`composition_date_basis`; the same reason remains in the ordinary lazy
`date_basis` payload. Existing dated rows keep their dates, meaning and order.
Browser and terminal readers display these fragments separately from the dated
chronological chain under **Composition date not established**, ordered by
author, work, natural extent and passage identity. No surrogate year or relative
chronology is asserted for that section. Admitted-fragment and book/chapter
counts include both classes, while source details retain the dating reason.

All ordinary admission requirements remain: explicit checked text, truthful
work/author and anthology ownership, effective controller and hash, lawful
publication rights, original/translation voice and actual credits, required
English-absence findings, canonical natural extents, projection refusals and
disputed-parallel handling. Possession, discovery confidence and an incidental
prooftext still cannot substitute for a fragment. Source manifests, source
fingerprints and consumer bindings are not changed by these three date-class
declarations.

## Exact first applications

| Checked passage | Canonical natural extent | Dating evidence and limit |
| --- | --- | --- |
| `passage.john-chrysostom.homilies-on-philippians.ccel-web-2026-09-17.3` | Philippians 1:18-24 | Pauline Allen's actual publisher PDF introduction, 2013, printed pages xii-xiii, was read. Its conclusion does not securely date the individual homilies; the older Oxford/NPNF Constantinople assignment supplies no secure year for Homily III. |
| `passage.john-chrysostom.homilies-on-philippians.ccel-web-2026-09-17.4` | Philippians 1:22-30 | The same actually read modern discussion limits the dating of Homily IV. Its extent includes the continuing lemmata through verse 30, beyond the initial 1:22-26 quotation. |
| `passage.bede.in-marci-evangelium-expositio.2026-10-13-latin-wikisource-migne.mark-10-42-45` | Mark 10:42-45 | The retained preface and checked block establish no calendar year. Direct CNRS/IRHT Bibale/FAMA retrieval failed; the indexed 725-730 estimate remains an unadopted lead. This is the project's bounded unresolved dating, not a claim that scholarship knows no date. |

The Philippians texts are complete checked historical English bodies with
editorial note prose and numeric callouts excluded. Their actual edition
credits W. C. Cotton as translator and John A. Broadus as reviser and note
author; neither an original-Greek nor a new print-image collation is asserted.
The exact protected Allen PDF is registered at
`artifact.john-chrysostom.homilies-on-philippians.2013-sbl-allen.publisher-pdf-861fbb6c`
without publishing its bytes. No locality, author-life, translation, printing or
retrieval year is substituted for composition.

Bede's exact Latin at retained lines 312-313 was compared with PL92 column
236A-B; the generated extraction prefixes alone are omitted. The digital
expression is not silently identified with that 1862 printing. The page-only
print passage remains unmapped as the same text. The work's prefatory account
of inherited patristic material and Bede's additions remains; this amendment
does not authenticate each sentence's origin. Its use beside a weekly study's
Matthew 22 reading remains an analogue, not direct Matthew commentary.

Bede's English record is honestly `not-surveyed`, checked 2026-10-23. It claims
no completed translation/rights survey, no universal absence of an English
translation and no permission to supply one. The inaccessible catalogue notice
is registered as unavailable at
`artifact.cnrs-irht.bibale-bede-in-marci.2026-10-23-web.bibale-entry-39610`,
without invented acquired bytes or hash.

The resulting admitted source map has 1,359 fragments across seven canonical
books, including three explicitly unestablished-date rows. The prior 1,356 rows
and all their known dates are preserved. The
[2026-10-22 research audit](../corpus-catena-cross-reference-2026-10-22/RECORD.md)
and its zero-admission-ready finding remain unchanged historical evidence under
the original contract. This amendment does not retroactively reseal that audit
or claim whole-corpus transcription, research or publication completion.
