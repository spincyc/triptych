# Altar-server edition guide map

Status: **held structural prototype; not approved for publication**
Audit date: 2026-07-27
Edition selection: `ed-altar-server`

## Reader and purpose

This use-derived edition is for altar servers. It is designed to show
everything documented as possibly present around a server, including objects
the server merely recognizes or must not handle. Its eventual audience layer
emphasizes location, ordinary handler, the server's handling boundary,
handoffs, common confusions, and immediate safety.

## Current generated selection

The present `main.tex` is a publication-capable shell that consumes only the
generator-admitted `ed-altar-server` selection under `build/`. That generated
selection is empty because there are no publication-ready canonical objects.
It therefore renders a held notice, not verified object presence or a claim
that coverage is complete.

When populated, `ed-altar-server` selects only `publication-ready` canonical
records whose `audience_relevance.altar_server` value is `required` or
`useful`. The presence rule deliberately includes an object documented as
possibly near a server even when `handling.server_relation` is
`recognizes-only` or `must-not-handle`. Unresolved records are excluded.
Neither familiarity nor appearance is enough: possible presence must be a
verified canonical claim, and the relevance field must be assigned in that
same record.

## Priestly-review selection boundary

The priestly-review edition may expose only explicitly manifested canonical
records proposed for `ed-altar-server`, with workflow and evidence state
visible. It may include a proposed presence or handling relationship so the
reviewer can correct it, but it must not convert that proposal into handling
permission. The public selection remains limited to `publication-ready`
records with `required` or `useful` altar-server relevance and verified
possible presence around a server.

## Visible omissions in the review edition

The review edition must name omitted Mass forms, special ceremonies,
sanctuary regions, ministers, object families, and unreviewed handling
relationships. An omitted object must not appear to be absent from the rite or
safe to ignore. Gaps in “must not handle,” safety, handoff, and local-variation
coverage require conspicuous review notes.

## Reader order

1. Compact title with a conspicuous priestly-review/hold notice.
2. Visible omissions and review-state key.
3. Recognition and handling key.
4. Sanctuary orientation from the server's working places.
5. Objects around the server, arranged by where and when they are encountered.
6. Vestments, ministers, and insignia the server must recognize.
7. Objects particular to special Masses and related ceremonies within the
   comprehensive volume's declared boundary.
8. Priestly-review questions and correction instructions.
9. Selective pronunciation, English--Latin and Latin--English indexes, visual
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
public server selection. The generated held or review notice must not be
treated as instructions, handling permission, or evidence that an object may
be present.
This leaf remains on hold and must not be installed or published. A scaffold
PDF, if built, is a production test only. Plate-manifest order remains a
publication blocker.
