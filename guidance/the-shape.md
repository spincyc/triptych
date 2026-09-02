# The shape

The guidance documents that stand beside this one each govern a part of the
work. This document governs nothing. It exists because the same small set of
ideas keeps being rediscovered independently in different corners of the project
— in retrieval, in storage, in derivation, in what a page prints — and a reader
who has seen them stated once will recognise the next instance instead of
solving it again from scratch.

Every claim below is followed by the incident that produced it. None of them
were reasoned out in advance; all of them are scar tissue.

## 1. There is one defect, and it wears every costume

**A reference that resolves successfully and wrongly.**

That is the governing failure of this library. Not a broken link, not a missing
file, not a crash: those announce themselves and get fixed within the hour. The
dangerous case is the reference that returns something — plausible, well-formed,
in the right language, of the right length — that is not what it claims to be.

It has arrived through every layer:

- **Retrieval.** A versification check truncated at Psalm 27, so a statement
  about a 5.8 MB file rested on a fifth of it. A retrieval driven by Wikisource's
  own contents page would have stopped at chapter 30 of a treatise that has 31 —
  the contents page is wrong, and only fetching the bytes revealed it.
- **Cataloguing.** A passage record declared pages 31–37 while its own prose
  claimed a prayer printed on page 38. Page 38 therefore belonged to no record at
  all, and every check passed.
- **Derivation.** Four Sundays' orations were held twice. The two copies had
  already drifted five ways — `caelestis`/`coelestis` and a citation encoded as a
  contiguous range against three discrete verses — and nothing compared them.
- **Storage.** `et ego in vobis: null` sat in a propers file because an unquoted
  Latin incipit contains a comma, and YAML read half of it as a second mapping
  key; the page served the truncated antiphon. Four defects of that one class
  landed on a single day. Nothing reports any of them, because no validator
  enumerates unrecognised keys on a proper — `sources.md` states the rule and
  names the gap.
- **Composition.** An agent briefing on the oration problem contained a Latin
  incipit recalled rather than read. It scanned correctly and was invented.
- **The apparatus itself.** A comment claimed a check verified the release
  bindings; the check only verified their shape. The tool listing recorded 29
  tools against 30 registered. The apparatus is not exempt from the defect it
  exists to catch.

The common factor is **fluency**. Everything above reads correctly. That is why
the countermeasures in this project are structural rather than attentive: no
amount of care distinguishes a right answer from a well-formed wrong one at the
point of use. The distinction has to be built into where things are kept.

## 2. Derive once; a restatement is a disagreement waiting to happen

Two copies of a fact are a prediction that they will differ. The prediction has
never failed here.

The rule is that a fact is derived in exactly one place and read from there by
everyone. `resolve_propers` is one function, read by the validating gate and by
the page that renders, so the reference a gate accepts and the reference a site
resolves cannot come apart. The versification projection writes **no row** where
two editions agree, because a row that restates agreement is a row that can later
contradict it. The tool grouping lives in one table, and a check proves it names
every registered tool exactly once.

The corollary is uncomfortable and worth stating plainly: a hand-written table
beside a derived one is not documentation, it is a second source of truth. When
this project found two such tables, they already disagreed, and the wrong one was
the one being read.

## 3. Reference; do not copy

A mass says *where its text is printed* rather than reprinting it. A recension is
a base plus its departures. A missal edition's history is a minimal diff, so that
a revision looks like a revision and not a wholesale rewrite. A commentary
fragment is stored at the extent its author addressed, and the chapter view is
derived from that.

This is the positive form of §2, and it buys something beyond consistency: the
diff becomes the deliverable. When each edition stores only its departures, the
question "what changed in 1955?" is answered by the storage rather than by a
comparison someone has to perform and could perform wrongly.

## 4. Absence is data, and must have somewhere to live

If a gap cannot be represented, it will be filled — silently, plausibly, and by
whatever is nearest to hand.

So absence is written down, always with its reason:
`editio-typica-new-matter` on protected postconciliar Latin for which this
project has established no distribution basis; `latin-not-transcribed` on an
element held whole in English; `untranslated` on an oration whose witness
answers neither Latin form; `via_unrepresented` on a connector whose descent
crosses an edition this project does not carry; `unresolved` on a facsimile's
rights. The ICEL case reinforces the distinction: a conditional permission for
one web-display surface is not a basis for putting the same payload in a
downloadable, clonable public data bundle. Record the surface limitation rather
than converting either the permission or the limitation into a blanket claim
about the text. A placeholder is **counted as a placeholder** and never printed
under the heading `Collect`. A shortened transcript says how many lines it
dropped.

The test of this principle is whether the gap survives contact with a renderer.
A page that shows nothing where a prayer belongs has told the reader that the
Mass omits it. A page that names the specific witness, rights, exactness, or
surface reason for the absence has told the truth.

## 5. Refusal is a first-class output

A tool that always answers is a tool that lies when it does not know.

This calendar states no general table of precedence, so a date carrying two
Masses reports both — 124 of 365 dates in 2026 carry unranked candidates —
rather than picking one. The
family-migration ledger will not refresh without an `--audited-on` date, because
re-pinning asserts a review.

The sanctoral pointers into the Commons are the fullest case. The Missal prints,
under each saint, which Mass of the Commune Sanctorum he takes. Two lanes
recovered those lines by a linear scan and **landed none**, because such a scan
loses its date headings and a pointer with the right Common under the wrong
saint reads perfectly — one pass put eleven consecutive pointers under 21
December. A third lane recovered all 148 geometrically instead and landed
**five**, the five read on the page image; 143 stayed out, 87 of them because
the day prints orations nobody has transcribed and the Common's *beati N.*
would be served in their place.

Where a witness exists, refusing to write is also the answer: a lane authorised
to supply its own English for the 1962 orations supplied **zero**, having found
242 public-domain ones nobody had opened. Where none exists the project may
compose, and then it says so — the 70 postconciliar orations translated from
their ancient sources are labelled as the project's own, unreviewed and
non-liturgical. The refusal is not a preference for silence; it is a refusal to
let a composition pass as a witness.

The strongest evidence that a rule is real is that it deletes work. When the act
tracer was given seven candidate nodes it kept three, and the line it removed was
the one proposed most confidently.

## 6. Provenance travels with the artifact, not beside it

A hash, the witness it came from, the pages actually read, the model that
contributed and in what role, the aliases a retrieval searched under, the date a
review happened. These are not metadata in the weak sense of being *about* the
artifact; they are the only thing distinguishing it from an identical string
someone typed.

Hence the separation of **attestation** from **residence**: a text resides in the
base, and its witnesses are recorded per witness, so a text attested by a single
printing says so. Hence release authorization meaning that someone reviewed the
bytes — which is why adopting another lane's uncommitted files into it, as
happened here, is a real fault even when the bytes turn out to be fine.

## 7. The station is the act, not the state

A history of changes is a history of **acts**: a constitution, a decree, an
instruction, a documented refusal. Books are witnesses to acts. Two printings of
one prayer differ constantly, and no act stands behind those differences, so a
printing does not become a station by being different.

This is what keeps a history from becoming a list of everything that was ever
different. It also forces honesty about gaps, because an act is dateable and
citable: where the descent runs through something unrepresented, the line is
drawn broken and named, rather than joined as though nothing sat between.

One narrow exception, and it declares itself. Before Trent there are missals no
act has been located for, and refusing them left the record silent about books
that demonstrably survive. So a station states its kind: `promulgated`, or
`printed` where a missal survives and **no act is claimed at all**. A printed
station is the weaker claim and reads as one everywhere — it must name the
printing it stands on and say why that printing is a distinct edition rather
than a rescan of one already carried, which is the whole hazard of letting a
book be a station. `time-machine.md` Rule 1 owns the rule and its exception;
`tools/act-history` enforces both.

## What this is, underneath

The project looks like a library and is not one. It is an **apparatus for keeping
what is attested apart from what is inferred**, operating in a domain where the
inferred version is fluent, confident, and frequently indistinguishable from the
real one at a glance.

Every rule above is a countermeasure to the same pressure. Derive once, so the
two versions cannot diverge unobserved. Reference rather than copy, so the
difference is the record. Give absence a home, so nothing fills it. Let tools
refuse, so ignorance has an expression. Carry provenance, so a claim can be
walked back to a page someone read.

The reason the discipline has to be this heavy is that the failure is not noisy.
Nothing breaks. A wrong collect is said, a saint is given another saint's Mass, a
date is asserted from a table that resolved successfully — and the apparatus,
unless it was built to notice, reports that everything is fine.
