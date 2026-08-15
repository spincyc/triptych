# Review request — Catena E1 V7

**The exact head, the parent, the review answered and every count in this
package are in `DERIVED-CLAIMS.md` and `claims.json`, computed at seal time by
`logs/derive-claims.py`.** No identity or figure is typed into this file, and
`logs/head-consistency.py` refuses a package whose prose names a commit those
claims do not entitle it to name. That is the direct answer to the V6 review's
finding that this document opened by naming a head the package was not sealed
for.

This file is questions only.

---

## Blockers — decisions a reviewer should make

*(Three adversarial passes over this lane's own diff produced these. Two
confirmed findings are recorded unfixed: §1 below, and the `src/web/data/bibles.json`
sentence in `UNRESOLVED-BLOCKERS.md` §7, which is composed inside the shared
shell and is not this route's to write.)*

### 1. A record stating nothing but `source` is still a fragment held here

`{"source": "0"}` states which edition it belongs to and nothing else — no
identity, no locus, no locator, no tally. It borrows that edition's author and
work through the fold and is counted into "N fragments held here".

Refusing it means asking the fragment's own record for a name, and **every
fragment of the tracked corpus states its author and its work only through its
edition** — so that gate refuses all 1,351 of them. Narrowing it some other
way means moving the line V6 drew and this review left standing: that a
fragment whose id alone is unreadable still renders and still counts, because
it is a fragment held here minus one fact.

V6's request asked exactly this — *"whether a fragment with no usable identity
should also fall out of the count"* — and the review did not answer.

**A reviewer should decide** where the line is, in terms that do not refuse
the corpus. This lane declined to move it twice and records the case instead;
an adversarial pass over V7's own diff raised it, and it is the one confirmed
finding from that pass that is not fixed.

### 2. A carried `text_path` is accepted when its stem is the fragment's own id

Where a spine states a `text_prefix`, the request is composed from it and the
fragment's validated id, and a carried `text_path` is discarded outright.
Where a spine states **no** prefix — which is the sample corpus under
`src/web/browser/fixture/`, served by `?data=fixture` and offered by the
page's own inline notice — a carried value may stand in, but only when it
satisfies `leaf` **and its stem equals this fragment's own validated id**.

That second clause is what makes it safe: the path can address exactly one
file, the text of the fragment that carried it, so an injected path names some
other file by definition. All 47 fixture paths satisfy it unchanged.

The alternative was discarding carried paths outright, which would have told a
reader that 47 fragments of the sample corpus carry no text file — false, and
a regression in a surface this page advertises.

**A reviewer should decide** whether accepting a carried path under that
constraint is right, or whether the fixture should be regenerated to the
current contract instead — which is generator and data ownership this lane
does not hold.

### 3. `startFailed()` is not reachable from a settled route

The review asked for a regression driving a pending render through
`startFailed()` before releasing the parked work. After `start()` returns, the
only caller is `render()`'s guard `!book || !bible || !Number.isFinite(chapter)`,
and every control feeding it is populated from a validated root while the
shim's `<select>` refuses a value no option carries. None of the three can be
made unreadable once the page has started.

V7 supplies the same claim through the terminal transaction a route **can**
reach mid-flight — the invalid-address transaction — with the full sink set on
both sides of the release, for a resolution and for a rejection.
`UNRESOLVED-BLOCKERS.md` sets it out.

**A reviewer should decide** whether that is the claim the review wanted, or
whether reaching `startFailed()` requires a harness change this lane should
have made.

### 4. The refusal contract narrowed twice, and this is the second time

V6 narrowed a refusal to require a sound `note`, and asked whether that was
right. V7 narrows again: the closed `kind` the projection records, and the
`chapter` **matched against the chapter being read**. All 112 tracked refusal
rows satisfy both, so nothing real is refused — but a record carrying a
recognized kind and no note, or a note and no kind, now refuses nothing where
V5 would have printed "Boundary not established." over it.

The defect that forced it is concrete: the reviewed fixture's one well-formed
refusal states `"chapter": 1`, and V6 printed it under Genesis 2 with the
surrounding sentence interpolated to say Genesis 2.

**A reviewer should decide** whether requiring the whole typed record is
right, or whether `kind` and locus should be refinements with the note alone
establishing the refusal.

### 5. A contradiction now contributes no prose at all

Where two recognized findings disagree, V7 emits no `reason` and no `partial`
for that row. The row still stands with its author and its work and is counted
in "a finding this page cannot read".

That is a real loss: both records are individually valid and each states a
sentence somebody wrote. The argument for dropping them is that a reason
belonging to one side of a contradiction is not a fact standing apart from the
choice the page refused to make — it **is** that choice, in prose — and V6's
ranking rule chose it by length, which nothing in the contract supports.

**A reviewer should decide** whether declining the prose is right, or whether
a contradictory row should show both reasons, explicitly attributed and
explicitly marked as disagreeing.

### 6. "Carries no text file" now says three different things

A fragment shows that sentence when its `id` is not an identity of this
corpus, when its file's `text_prefix` is not a trail of this data root, and
when its text really did 404. The first two are the page REFUSING to compose a
path; only the third is a fact about the holdings.

V6 settled that an unsafe or unreadable prefix leaves every fragment standing
and saying this, and its review passed it — losing the whole chapter instead
would be worse for a reader. So V7 did not change the behaviour. But the
second adversarial pass is right that the sentence is imprecise, and it is the
kind of imprecision this correction exists to remove: a reader is told
something about the corpus where the truth is something about the page.

**A reviewer should decide** whether the three cases want three sentences, or
whether the refusal cases should say something like "this page could not
compose an address for this fragment's text". The page has no bytes for a
third string; the model does.

### 7. The weaker sentence for an unreadable root is new copy

Where a root could not be read whole, an address that cannot be matched
against it now reads:

> `bible=../../escape` is not a value this page could match; the record it
> would be matched against could not be read whole.

instead of "…is not a published edition". The neutral umbrella above it —
`Address not used`, `This address cannot be used as written`, and
`The address is unchanged; the values not used are listed.` — is unchanged
byte for byte, and the address still fails closed identically.

**A reviewer should decide** whether that sentence is the right one. It is
longer than the claim it replaces, it appears in a state a reader meets rarely,
and it says something about this page's own reading rather than about the
corpus.

---

## Optional feedback

### 8. Prose in the unbudgeted model, a third time

V5's request asked whether visible prose and argument belong in
`src/web/browser/catena/catena-model.js`. V6's asked again, about a larger
relocation. Neither was answered, and V7's relocation is larger still: the
typed projection, the payload projection, the chapter reading, the three
bootstrap roots and the whole address judgment are all asked there now.

`src/web/browser/catena/catena.js` finished V6 with **seven** gzipped bytes under its ceiling. That
is the whole of the reason, and it is arithmetic rather than preference. The
page came out smaller in both measures; the model grew, and the exact figures
— including both ways of measuring the two files' combined payload — are in
`DERIVED-CLAIMS.md`.

This lane did not treat the two silences as consent. It trimmed its own
additions twice, by measured amounts, in commits that say so, and asks again.

The one figure that makes this decidable rather than arguable is in
`DERIVED-CLAIMS.md`, derived rather than typed: the **comment share** of each
file, compressed. The model's is essentially unchanged between the parent and
this head — the growth is proportionate to the file's own established idiom
rather than a departure from it — and the page's rose only because code left
it while its comments stayed.

That is the case FOR the density, stated as plainly as this lane can state it,
so that a decision against it is made on the figures rather than on an
impression. The bytes, the ceilings, the two ways of measuring the combined
payload, and that share are all in the derived record.

**A reviewer should decide** whether the explanatory density is correct,
whether some of it belongs in `guidance/` instead, or whether the model should
carry a ceiling of its own so this stops recurring one correction at a time.

### 9. The evidence tooling still ships inside the package

`logs/sanitize-and-seal.py` (V4), the V4.1 capture tool, V5's Chromium probe,
V6's pair audit and `logs/test-sanitize-and-seal.py`, and now
`logs/derive-claims.py` and `logs/head-consistency.py` all live inside the
handoff packages rather than in `tools/`, because `tools/` requires registry
entries and `check-tool-registry` is separately owned and separately red.

The two V7 tools have the strongest claim yet to promotion, because they
answer a defect class that has now recurred in three packages running: a
number that a program could have computed, typed by a person instead, at a
moment when the value had moved. They are parameterised on the head, the
parent and the package directory, and carry no V7-specific filename, digest or
count.

### 10. The scenario plan outgrew `ARG_MAX`

The replay harness passed its whole scenario list as one `argv` element, and
the V7 additions carried it past the operating system's limit — `OSError:
[Errno 7] Argument list too long`. It now arrives as a file. Recorded because
it is a limit any successor will meet sooner than this one did, and because
the failure looks like a harness defect and is not.
