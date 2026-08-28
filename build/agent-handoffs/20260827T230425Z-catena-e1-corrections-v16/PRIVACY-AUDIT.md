# Privacy audit

**Read the tense.** This file separates two kinds of statement, because
conflating them is how a privacy claim becomes untrue without anyone lying.

- **Present tense** describes the *tool*: what the sanitizer looks for and
  what it does about it. Those statements are true when this file is written,
  and they are checkable by reading `logs/sanitize-and-seal.py` and running
  `logs/test-sanitize-and-seal.py`.
- **Past tense** describes *this package*: what a scan of these exact bytes
  found. Those statements only become true at the seal, and the figures behind
  them are derived by the pipeline, not typed here. `checks.txt` and the seal
  transcript named in `logs/LOG-INDEX.md` carry them.

**No verdict in this file is asserted by this file.** Where a scan result
belongs, the transcript that carries it is named instead. A clean seal is a
thing the pipeline's own logs establish, and a document that announced it in
advance would be describing an intention.

This file is carried forward with its coverage claims intact, because the
sanitizer is the copy the previous lane shipped, unchanged, and the coverage is
a property of the tool. A reviewer who wants that identity first-hand can digest
`logs/sanitize-and-seal.py` in this package against the copy in the previous
package; the executed-tool digests and the tool-byte comparison table named in
`HANDOFF.md` §10 are where the pipeline states it. This lane did change other
tools in `logs/`, and one of those changes bears on this audit; it is stated
below under **The command record, and what it now shows**.

An earlier version of this file claimed coverage it did not have. Two leaks it
had missed were established by review: the tracked outer assembly and
verification logs carried the workspace path, the account name and the tool
anchor, because the sanitizer's walk root was the package directory and those
siblings are written after the manifest; and inside the archive a generic
temporary root and a dash-flattened form of the workspace path survived, because
the scratch rule required a literal substring no ordinary temporary directory
carries and the flattened form could not match a path-separated pattern. This
file therefore scopes every claim to what is actually scanned, and says so where
the answer is "not by this tool".

No figure in this file is typed. Where a count belongs, it is named and the
member that carries it is named beside it.

## What is looked for

The sanitizer derives the identities to remove at run time rather than
carrying them as literals — an account name, a hostname, a numeric user id and
a home directory — and then applies two families of rule.

**Value-free classes**, matched by shape, so the rule works for a value it has
never seen: **any** temporary root rather than one bearing a particular
substring; a home path; the agent workspace path, **in path-separated and in
flattened form**, because a slug with its separators replaced is the same
disclosure with different punctuation; the lane evidence directory; a process
directory; a labelled process id; an email address; a D-Bus name; a UUID in
either spelling; a loopback address with a port; an RFC1918 address; a UTC
offset on a date or a time; a tokenized local time; and an IANA timezone by
area or by bare name. A local-offset timestamp is rewritten to its UTC instant
rather than deleted, so ordering and elapsed time survive while the offset
does not.

**Value-keyed checks**, run independently of whether any rule fired, so the
scan cannot report clean while the identity survives: the account name, the
hostname, the literal home directory, the session bus path, the user slice,
the uid pair, a labelled uid, the repository path, and the tool anchor.

**Member names are scanned as well as member bodies.** A name is a leak with a
filesystem in front of it.

**The sanitizer refuses to seal if its own source contains a private value as
a literal**, because a scanner that carries the string it is looking for
cannot see its own leak.

## Where it looks

The sanitizer has two modes, because the things it must scan do not all live
in one place and are not all written at the same time.

**Inside the package**, walking the package directory as its root. The seal is
refused unless every one of these is clean:

- every archive member's bytes;
- every archive member's **name**;
- the logs, including every attempt's log root;
- the in-package ledger copy;
- archive entry metadata.

**Several members are new in V16 and are covered by that walk like any other**,
named here so a reviewer does not have to infer that they are in scope:
`commands.json`, the machine-readable command record from which `checks.txt` is
derived; `logs/catena_command.py`, the command-classification module;
`logs/replay-command.py`, the parent-replay driver;
`logs/attempt-history.json`, the derived attempt history; and
`logs/divergence-reconciliation.json`, the derived example-figure
reconciliation.

**One of those carries a higher exposure than prose does, and it is named
rather than left to the walk to discover.** `commands.json` carries argument
vectors and environment bindings; it is scanned by value as bytes and by name
like every other member, and the legend it carries binds tokens to symbolic
roles, never to real paths.

**`logs/divergence-reconciliation.json` was formerly named beside it, and that
note no longer describes the member and has been withdrawn rather than left
standing.** The regenerated artifact names every transcript of this package by
its PACKAGE-ROOT-RELATIVE member path and by nothing else: it does not carry the
builder's filesystem location of any authoritative log, and any earlier sentence
in this package's narrative saying that it does — or asking a privacy reader to
look at it on that ground — is now false and is removed rather than softened.
The policy the artifact states in its own `path_policy` field is the policy this
audit holds it to: **all artifact member names and evidence references are
package-root-relative, and builder-local absolute filesystem paths are excluded
because they are not part of the portable evidence identity.** They are not
tokenised into placeholders merely to preserve them, because a placeholder
standing where a builder path was is still a record that a builder path was
thought worth keeping; the reviewer resolves every name against the extracted
package root, which is the only root that exists once the archive is unpacked.
That is deliberate evidence design and not an omission, and it is the reason
this member is no longer in the elevated-exposure list.

**What remains in that member, stated exactly rather than glossed, is
historical.** Two fields under its HISTORICAL V15 transcript entries —
`transcripts.v15_parent.local_path_read` and
`transcripts.v15_head.local_path_read` — record the temporary directory the
PREDECESSOR package's logs were extracted to in order to be parsed. That is a
temporary root, one of the exact shapes the value-free rules are written for,
and the value-keyed checks run against it independently of whether any rule
fired; it is retained only to record where the predecessor's evidence was read
from, and the figures it supports are ones this package carries as historical
context and derives nothing from. No path in that
member describes an authoritative V16 log, and the seal is refused rather than
reported if any of these bytes is not clean.

**`logs/attempt-history.json` holds no path of that kind** — its file
references are bare ledger names — but it does hold every attempt id, every
ordinal and every terminal reason this lane recorded, in free text written by
the operators of those attempts. Free text is scanned by the same rules as any
other member's bytes, and it is scanned by value; nothing about a reason field
is exempt from the walk because it is a reason field.

**Outside the package**, as named files rather than as a walk, because each is
written after the manifest is taken and cannot be a member. **Every outer
sibling is sanitized and then re-scanned before it is committed** — every
sibling named in `HANDOFF.md` §10, which are the archive, its
digest-and-size sidecar, the outer invocation log, the final-verification
transcript, the post-verification authority record, the executed-tool digests,
the tool-byte comparison table, this lane's attempt and battery history as the
live ledger carries it, the
authority gate's transcript, the inventory's transcript, and the two transcripts
this pass writes of its own work. A sibling that does not pass its re-scan is
not committed, and the pass that rewrote it and the scan that cleared it are
each a transcript a reviewer can read.

**Those last two are named by filename in this package, where the previous one
named them by suffix.** They are written after the inventory and the authority
gate, precisely so that this pass can rewrite and re-scan the transcripts those
gates produce. Naming them by suffix meant the completeness verdict was taken
before they existed and went stale the moment they did. They are named, and the
verdict this package ships is the one taken after they exist. Their coverage is
unchanged: this pass has always rewritten and re-scanned its own records; only
the record of their names has changed.

That is the whole of the coverage: every archive member, every sibling in that
list, the attempt and battery history, the executed-tool table and the
verification transcript. Nothing else is scanned, and this file makes no claim
about anything else.

## The command record, and what it now shows

The command record in `checks.txt` is a privacy mechanism as well as an
evidence one. A command is recorded with the pipeline's tokens rather than with
the paths they stand for, and the record decides whether each invocation is
shown as it ran, elided, or described. Those two purposes pull in opposite
directions, and the previous lane's record shows what happens when the
mechanism is wrong in the safe-looking direction and in the unsafe-looking one
at once: the commands carrying the most weight were recorded as strings whose
quoting could not expand, so a reviewer could read them and not run them.

This lane changed that representation, and the derivation now ships: the
machine-readable source is `commands.json`, the classifier is
`logs/catena_command.py`, and the parent replay's own driver is
`logs/replay-command.py`, which binds one variable per location instead of
overloading `$REPO` for two. What a row now carries is the working
directory, the argument vector a shell was handed, and the environment bindings
it ran under, with each token bound to exactly one location by a legend the
package derives. **That shows more of the STRUCTURE of an invocation and no more
about the machine it ran on.** The substitution is unchanged: a token stands
where a value stood, and the value-keyed scans above run independently of
whether any rule fired, so a record that is more legible is not thereby more
disclosive. A legend that bound a token to a real path would be exactly the
leak this file exists to refuse, and the legend binds tokens to symbolic roles
rather than to locations.

Whether the record now reads and runs end to end is a question
`REVIEW_REQUEST.md` puts to the reviewer, because this lane's verdict on its own
tooling is not independent.

## Archive metadata

Entry timestamps are written at a fixed DOS epoch and mode bits are derived
from the file suffix, so the archive discloses no builder timezone, no UTC
offset, no umask and no platform. This is not asserted from the writing code
alone: a test in `logs/test-sanitize-and-seal.py` inspects the built archive's
own entry metadata directly, and two earlier reviews each verified the result
independently.

## No image scan, because there are no images

This package ships no screenshot and no other raster, for the reason
`LIMITATIONS.md` records; the artifact inventory in `HANDOFF.md` §10 is the
authority on what the members are. The image rules the sanitizer carries — the
PNG chunk inspection that admits only `IHDR`, `IDAT` and `IEND`, and rejects
`tEXt`, `iTXt`, `zTXt`, `eXIf`, `tIME` and `iCCP` — therefore have nothing to
run against here, and no claim is made about image or PNG metadata in this
package. The archive's own entry metadata is a separate matter and is claimed
above.

## What a reviewer can run

These are the invocations that reproduce the audit against the extracted
package. Each is read-only.

    python3 logs/test-sanitize-and-seal.py
    python3 logs/sanitize-and-seal.py . --check-only
    python3 logs/test-authority-coherence.py
    python3 logs/test-attempt-history.py

The first proves the tool; the second proves these bytes are at the
sanitizer's fixpoint; the third and fourth prove that the gate reading this
package's authority records and the rules governing its ledger can actually
refuse. The authority gate itself needs the archive and the post-verification
siblings, which are not members, so its own run against this package is the
sibling transcript named in `HANDOFF.md` §10.

`logs/sanitize-and-seal.py --check-only` is also run inside the final
verification, from a trusted copy outside the archive, so the reviewer's run and
the sealing run are the same check from two directions. What each of those runs
exited with is in `checks.txt` and in the transcripts `logs/LOG-INDEX.md` names;
it is not stated here.

## What this audit does not claim

**The boundary is shipped-versus-builder-local, and it is stated rather than
glossed.** Four classes of artifact this lane's build produces sit outside every
sanitize walk and outside the named-sibling list:

- the discard and supersession markers — a package's own discard marker, an
  attempt's own marker under its log root, a marker beside an archive, and a
  battery's own — which carry local-offset timestamps and free-text failure
  reasons, and which the assembler cannot reach because it skips the outer
  sanitization phase entirely on a run that has already failed, which is exactly
  the run on which a marker exists;
- any retired attempt ledger, whose `command` fields hold raw pre-sanitization
  absolute paths;
- the lane-wide executed-tool journal;
- any retained discarded package tree, including one that dies before its seal
  and therefore still holds raw absolute paths throughout.

**This lane has concrete instances of the second and fourth classes, and names
them rather than describing the class abstractly.** Its retired ledger
`build/agent-handoffs/attempt-ledger.jsonl` is one, and so is each of the five
retained cohorts kept under `spincyc/v16-retired/` — `attempt-01-refused`,
`attempt-03-warm`, `attempt-04-07-driver-drift`, `attempt-05-superseded-head`
and `attempt-06-abandoned` — together with the lane-wide
`build/agent-handoffs/executed-tools.jsonl`. **The word `retired` in that first
name is load-bearing and this audit does not let it pass unexplained.** This
lane's history is not inside one file: that ledger spent ordinals 01 to 03 and
was retired, `build/agent-handoffs/attempt-ledger-02.jsonl` opened at ordinal 04
in its place, and no row in either was rewritten or deleted — the history is
whole only across the pair, which `logs/attempt-history.json` derives and which
`PROVENANCE.md` §15 records with both files' identities. The third of those
holds the two cohorts that were recorded `authoritative` and then superseded,
retained on
exactly the same terms as the rest: outside the package, outside every
sanitize walk, supporting no figure, and digested file by file in its own
sidecar. Each is
named by the repository path it actually occupies in the builder's checkout,
because naming one as though it were a package member is exactly the claim this
audit exists to refuse. Every one of them is builder-local: none is a member,
none is a named sibling, none is committed to an evidence branch, and none is
inside any sanitize walk. They are retained so that the history is not
destroyed and they are outside the package because they support nothing in it.
**No authoritative claim in this package requires any of them**, which is the
property that makes their exclusion honest rather than convenient, and
`LIMITATIONS.md` and `PROVENANCE.md` §15 state the same boundary in their own
words.

Every one of those is builder-local: none is a member, none is a named sibling,
and none is committed to an evidence branch. The published archive and its named
siblings are what is scanned and re-scanned. **No broader
all-retained-artifacts privacy claim is made here, and the independent review
that examined the previous package declined that claim; this lane does not
renew it.** The markers' contents are symbolic by construction, and this
package's own standard is that "by construction" is an argument and not a check.
No such marker is committed for this lane's authoritative attempt unless one
exists, and if one does it is scanned by hand with the sanitizer's file mode
before it is added. `LIMITATIONS.md` records the class.

It does not claim that the tracked corpus is free of anything, that the
repository's history is free of anything, or that any file outside this
package and its named siblings was scanned. It does not claim that a class of
private value nobody has thought of is matched by a rule that does not exist.
It claims nothing about images, because there are none. It claims nothing
about the outcome of any scan: what a scan of these member bytes, these member
names, these logs, this ledger copy, this archive's entry metadata and these
named outer siblings found is recorded in the seal transcript and in
`checks.txt`, and those are the members that carry the verdict.
