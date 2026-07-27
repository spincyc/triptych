# Altar-server edition guide map

Status: **bounded priestly-review leaf; held from public reliance**
Audit date: 2026-07-27
Edition selection: `ed-altar-server`

## Reader and purpose

This use-derived edition is for altar servers and the priests or trainers who
supervise them. Its final scope is everything documented as possibly present
around a server, including objects the server merely recognizes or must not
handle. Its audience layer follows the server's route from sacristy to
sanctuary and back. For every selected object it emphasizes:

- encounter location and ceremony;
- ordinary handler;
- touch, carry, present, receive, prepare, recognize-only, and
  must-not-handle boundaries;
- giver, receiver, destination, and local-direction qualifications where a
  handoff is involved;
- likely visual or terminological confusions; and
- immediate safety around sacred, hot, sharp, fragile, or lighted objects.

Appearance never grants handling permission. A practical or local assignment
must remain visibly distinct from a universal Roman provision.

## Current generated selection

The present `main.tex` is a priestly-review shell that consumes only the
explicitly admitted `ed-altar-server` review selection under `build/`. The
generated manifest used by the installed snapshot admits six records and
omits 37 from the current 43-record inventory:
`obj-altar-bells`, `obj-altar-candle`, `obj-altar-candlestick`, `obj-chalice`,
`obj-paten`, and `obj-sanctuary-lamp`. These records form a bounded review
sample, not a complete server dictionary. Their admission exposes exact
source, artwork, handling, and audience questions to review; it does not make
them publication-ready or authorize reliance on the packet for training.

The authoritative `ed-altar-server` selection admits only
`publication-ready` canonical records whose
`audience_relevance.altar_server` value is `required` or `useful`. The
presence rule deliberately includes an object documented as possibly near a
server even when `handling.server_relation` is `recognizes-only` or
`must-not-handle`. Unresolved records are excluded. Neither familiarity nor
appearance is enough: possible presence must be a verified canonical claim,
and the relevance field must be assigned in that same record.

## Priestly-review selection boundary

The priestly-review edition may expose only explicitly manifested canonical
records proposed for `ed-altar-server`, with workflow, evidence, artwork, and
handling state visible. Object identity, governing rite and horizon, claimed
status, source identity and locus, distribution rights, generated provenance,
physical possibility, and safety must already satisfy the profile's
priestly-review gate. A proposed morphology, variant, contextual inset, or
local handling question must be printed as a specific question, not plausible
instruction. Review admission never converts a proposal into handling
permission.

The six-record sample is audience-specific only to the extent that its
canonical records contain verified server relationships and altar-server
notes. It currently tests direct handling of altar bells, recognition of
altar lights, and must-not-handle distinctions for chalice and paten. It does
not yet test the full sacristy route, Missal transfer, cruet and Lavabo
handoffs, Communion plate, server vesture, or the branches of sung, solemn,
ritual, Holy Week, pontifical, and related ceremonies.

## Visible omissions in the review edition

The installed 37-record omission register accounts only for canonical records
that exist and are excluded from this exact review snapshot. It is not the
completeness register. The review edition must also name omitted Mass forms,
special ceremonies, sanctuary regions, ministers, object families, and
unreviewed handling relationships. In particular, the Low-Mass candidate
register below identifies essential objects that have no canonical record and
therefore cannot appear in the generated omission register. An omitted object
must not appear to be absent from the rite or safe to ignore. Gaps in
must-not-handle, safety, handoff, and local-variation coverage require
conspicuous review notes.

## Reader order

1. Compact title with the exact priestly-review label and caveat.
2. Review-state, artwork-under-review, recognition, handling, and safety key.
3. Sanctuary orientation from the server's working places.
4. Low-Mass core route from sacristy preparation through return.
5. Objects around the server, arranged by encounter location and ceremony.
6. Vestments, ministers, and insignia the server must recognize.
7. Sung and solemn branches.
8. Objects particular to special Masses and related ceremonies within the
   comprehensive volume's declared boundary.
9. Explicit canonical-record omissions and missing-corpus disclosures.
10. Priestly-review questions and correction instructions.
11. Selective pronunciation, English--Latin and Latin--English indexes, visual
   index, variant and terminology notes, scope and qualifications, numbered
   source notes and references, generation metadata, and rights colophon.

Orientation proceeds from working-place compositions to local detail.
Non-vesture objects are grouped by encounter location and then ceremony;
vesture and insignia are grouped by minister. Objects limited to or materially
changed in special Masses, Holy Week, pontifical Mass, or related ceremonies
follow in their own section. Cross-references replace unnecessary duplicate
entries, and the plate manifest preserves intentional order within each
section.

## Questions for priestly review

1. Could a server encounter every selected object in the stated Mass or
   surrounding ceremony, and is any likely nearby object visibly missing?
2. Is the touch/carry/present/prepare/recognize-only/must-not-handle boundary
   correct for each object and branch?
3. Are ordinary handler, location, handoff, and safety statements usable
   without overriding legitimate local direction?
4. Are clergy-only objects and actions unmistakable to a young server?
5. Are special Mass, Holy Week, pontifical, and related-ceremony differences
   separated clearly enough to prevent transfer of one rule to another?
6. Which terminology or image would a server plausibly confuse in practice?

## Canonical dependency

This leaf is a curated view, not an independently editable dictionary. Object
identity, names, status, presence, handling, warnings, variants, sources,
artwork, and audience relevance must come from canonical records conforming to
`shared/schema/inventory-schema.toml`. Selection is governed by
`shared/schema/edition-selections.toml`. Any server-specific wording belongs
in the canonical record's `audience_note` and may not contradict or enlarge
the verified base claims.

## Hold and nonpublication state

There are currently zero publication-ready canonical records and no approved
public server selection. The six admitted records belong only to the exact
priestly-review snapshot and must not be treated as instructions, handling
permission, or evidence of complete object presence.

The priestly-review leaf remains held from ordinary catalog, search, web
edition, unrestricted distribution, instruction, and public reliance. Its
web-edition declaration remains ineligible. An authoritative release remains
blocked by the owner completeness matrix, the missing Low-Mass candidates,
audience-specific plate order, source and artwork gates, priestly and
intended-reader review, actual-size print and monochrome-copy review, and a
fresh exact-snapshot release decision.
