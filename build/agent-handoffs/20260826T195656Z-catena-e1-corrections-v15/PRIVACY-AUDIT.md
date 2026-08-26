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

This file is carried forward from the previous lane with its coverage claims
intact, because the sanitizer is the copy that lane shipped, unchanged, and
the coverage is a property of the tool. A reviewer who wants that identity
first-hand can digest `logs/sanitize-and-seal.py` in this package against the
copy in the previous package; the executed-tool digests and the tool-byte
comparison table named in `HANDOFF.md` §10 are where the pipeline states it.
This lane did change other tools in `logs/`, and one of those changes bears on
this audit; it is stated below under **Elision and the command record**.

An earlier version of this file claimed coverage it did not have. The V12
review established two leaks it had missed: the tracked outer assembly and P8
logs carried the workspace path, the account name and the tool anchor, because
the sanitizer's walk root was the package directory and those siblings are
written after the manifest; and inside the archive a generic temporary root
and a dash-flattened form of the workspace path survived, because the scratch
rule required a literal substring no ordinary temporary directory carries and
the flattened form could not match a path-separated pattern. This file
therefore scopes every claim to what is actually scanned, and says so where
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
- ZIP entry metadata.

**Outside the package**, as named files rather than as a walk, because each is
written after the manifest is taken and cannot be a member. **Every outer
sibling is sanitized and then re-scanned before it is committed** — every
sibling named in `HANDOFF.md` §10, which are the archive, its
digest-and-size sidecar, the outer invocation log, the P8 transcript, the
post-P8 authority record, the executed-tool digests, the tool-byte comparison
table, the complete attempt and battery history, the authority gate's
transcript and the inventory's transcript, together with the two transcripts
this pass writes of its own work, which are described there by their suffixes
because they do not exist until it has finished. A sibling that does not pass
its re-scan is not committed, and the pass that rewrote it and the scan that
cleared it are each a transcript a reviewer can read.

That is the whole of the coverage: every archive member, every sibling in that
list, the attempt and battery history, the executed-tool table and the P8
transcript. Nothing else is scanned, and this file makes no claim about
anything else.

## Elision and the command record

The command record in `checks.txt` is a privacy mechanism as well as an
evidence one. A command is recorded with the pipeline's placeholders —
`$REPO`, `$WORKSPACE`, `$EVIDENCE` — rather than with the paths they stand
for, and a classifier decides whether each recorded command is shown
verbatim, elided, or described. Those two purposes pull in opposite
directions, and the previous lane's record shows what happens when the
classifier is wrong in the safe-looking direction: two browser-gate commands
were recorded `ELIDED` and the load-bearing parent-replay command was recorded
`PROSE`, so the commands carrying the most weight were the ones the reviewer
could not read.

Neither verdict was caused by a private value. The `ELIDED` verdicts came from
the capitalised English word `JSON` inside a quoted `echo` note the battery
composes — not from a filename, and not from the `$WORKSPACE` and `$EVIDENCE`
symbols, which the classifier exempts by design. The `PROSE` verdict came from
`cp` being absent from the classifier's list of command heads. This lane
corrected the classifier. The correction makes more command text visible, so
it is stated here rather than only in the evidence documents: the placeholder
substitution and the value-keyed scans above are what keep that text clean,
and they are unchanged. Whether the record now reads end to end is a question
`REVIEW_REQUEST.md` puts to the reviewer, because this lane's verdict on its
own classifier is not independent.

## ZIP metadata

Entry timestamps are written at a fixed DOS epoch and mode bits are derived
from the file suffix, so the archive discloses no builder timezone, no UTC
offset, no umask and no platform. This is not asserted from the writing code
alone: a test in `logs/test-sanitize-and-seal.py` inspects the built archive's
own entry metadata directly, and the V11 and V12 reviews each verified the
result independently.

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
refuse. The authority gate itself needs the archive and the post-P8 siblings,
which are not members, so its own run against this package is the sibling
transcript named in `HANDOFF.md` §10.

`logs/sanitize-and-seal.py --check-only` is also run inside P8, from a trusted
copy outside the archive, so the reviewer's run and the sealing run are the
same check from two directions. What each of those runs exited with is in
`checks.txt` and in the transcripts `logs/LOG-INDEX.md` names; it is not
stated here.

## What this audit does not claim

**One uncovered class, stated rather than glossed.** The discard and
supersession markers — a package's own `<pkg>/DISCARDED.txt`, an attempt's own
`<pkg>/logs/DISCARDED-<attempt>.txt`, a `<zip>.DISCARDED.txt` beside the
archive, a `<stamp>-<name>.SUPERSEDED.txt` beside the package, and a battery's
own discard marker — are outside every sanitize walk and outside the
named-sibling list, and the assembler skips the outer sanitization phase
entirely on a run that has already failed, which is exactly the run on which a
marker exists. Their contents are symbolic by construction, and this package's
own standard is that "by construction" is an argument and not a check. No such
marker is committed for this lane's authoritative attempt unless one exists,
and if one does it is scanned by hand with the sanitizer's file mode before it
is added. `LIMITATIONS.md` records the class.

It does not claim that the tracked corpus is free of anything, that the
repository's history is free of anything, or that any file outside this
package and its named siblings was scanned. It does not claim that a class of
private value nobody has thought of is matched by a rule that does not exist.
It claims nothing about images, because there are none. It claims nothing
about the outcome of any scan: what a scan of these member bytes, these member
names, these logs, this ledger copy, this archive's entry metadata and these
named outer siblings found is recorded in the seal transcript and in
`checks.txt`, and those are the members that carry the verdict.
