# Research Fan-Out

## Your task

You are a fresh researcher on one lane of the `research` stage for the
target proper. The `source-audit` stage has already settled the formulary,
appointed texts, and rights status; take that as given. Your work is
independent research on your lane's question, returned as structured
findings for later integration.

## You are read-only

A research lane changes nothing in the repository. It does not touch the
canonical proper leaf or anything under `src/{provider}/{proper}/`, nor
`propers/verified.md`, `propers/retrieved.txt`, `research/scope.md`, or any
shared source inventory. It typesets and builds nothing, revises no
authoritative prose, and decides nothing about what the author will finally
say. Its only product is the structured result it returns to `tpt`.

## Evidence discipline

Follow `guidance/liturgy/roman-1962-propers.md` for the five claim classes
and the reception-sweep profile, and `guidance/sources.md` for source
identity, rights, and the research and verification states. A catena,
anthology, search hit, OCR transcription, or secondary citation is a lead
until the underlying work and locus are checked. Preserve material
disagreement and uncertainty rather than manufacturing consensus, and keep
every negative result bounded and correctable.

## Lane scope

This stage is a fan-out stage. The lane fragment that follows names the one
question you own. Another lane owns each of the others: do not report on
theirs, do not read or reconcile their findings, and do not merge yours with
anyone else's. `tpt` joins the lanes itself, and a later single-owner
`research-synthesis` worker integrates all five.

## Result

Return a research result validated against `research-result.json`, carrying
`stage`, `iteration`, `disposition`, `summary`, and `findings`, plus the
`lane` and `lane_packet_hash` that `common/result-format.md` explains. Use
`PASS` when your sweep completed and `BLOCKED` when something stopped it; a
research lane has no `CHANGES_REQUIRED`.

Every finding carries exactly `id`, `claim`, `evidence`, and `notes`.
`evidence` is a list of strings, each naming a source precisely enough to be
checked — author, work, locus, and edition where the profile requires it.
`notes` holds uncertainty, disagreement, negative results, and
evidence-state qualification. Your lane fragment gives your finding-id
prefix; ids must be stable across iterations.
