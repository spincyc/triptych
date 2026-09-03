# Lane: Source and Citation Coverage

## Your lane

You own a diagnostic coverage audit of the sources this proper will need,
and nothing else. Another lane owns Scriptural context, reception,
liturgical history, and theological synthesis; do not report on theirs. You
are read-only, as the shared fragment above states: this lane is purely
diagnostic, it repairs no citation anywhere, and its only product is your
returned result.

Survey the appointed texts against `guidance/sources.md` and the
repository's own source library, and collate:

- important claims this proper will rest on that still lack a source
- gaps in the source families — a tradition, corpus, language, or genre
  left unswept
- support that is weak, second-hand, or still only a lead
- primary sources the repository already holds that would replace a
  second-hand or derivative citation
- citation, rights, edition-identity, and provenance risks likely to matter
  during authoring

Name in `evidence` what you actually checked, including the library records
and holdings you consulted. Keep in `notes` the bound of your survey and the
severity you judge a gap to carry.

## A record the library lacks is not a claim the research lacks

Two of the things you survey read alike in a finding and are not the same
defect, and which one you have decides whether the run can continue.

- **Evidence the research has not reached** — no witness checked, a locus
  nobody opened, a claim standing on a catena, an anthology, or an
  aggregator. Report it plainly. The stage that reads your findings can send
  the lanes back for it, and that is a request this workflow can act on.
- **A source the library has not registered** — the witness was checked and
  its work, edition, and locus are known, but `src/sources/` holds no record
  for it and the publication's `research/source-bindings.toml` binds nothing
  to it. Report it as the provenance risk it is, and say whose work it is:
  registering a source is maintainer work that no stage of this workflow may
  perform. Nothing here writes `src/sources/`, and a further pass through
  these lanes cannot produce what the lanes are forbidden to write.

Never phrase the second as a condition of publishing. "Register and bind
before publishing" and "publication waits on these controls" name work no
stage owns; carried forward as preconditions they hand the author a bar it is
forbidden to clear, and the run stops at `author-proper` over evidence it was
holding all along. Omitting a claim is a different matter and stays available,
because the author can do it: name the one claim that should go and why, never
every unbound claim at once. `guidance/sources.md`
settles the standing rule: a schema version 1 binding file does not require a
machine ID for every sentence, and stable ids "do not replace intelligible
citations". A claim whose work, edition, and locus you checked is publishable
on that citation, and its unregistered state is a note in the audit rather
than a defect in the guide.

Where an absent record does control what may be published — a rights basis
only an artifact record can settle, or published English, which the profile
requires be quoted from a witness the library registers — say that, and say
it about the claim it actually reaches. That is a
narrow finding about one claim, not a standing condition over every source
the library has yet to hold.

## Result

Return a research result for this lane, per the shared contract above.
`PASS` when your survey completed, `BLOCKED` when something stopped it.

Finding IDs must use the `COV-` prefix and be stable across iterations.
