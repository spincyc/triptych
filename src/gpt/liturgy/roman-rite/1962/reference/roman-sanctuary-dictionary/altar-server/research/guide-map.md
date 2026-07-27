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

## Reader order

1. Compact title and recognition/handling key.
2. Sanctuary orientation from the server's working places.
3. Objects around the server, arranged by where and when they are encountered.
4. Vestments, ministers, and insignia the server must recognize.
5. Objects particular to special Masses and related ceremonies within the
   comprehensive volume's declared boundary.
6. Selective first-use pronunciation only where helpful, followed by the
   shared terminal apparatus required for the leaf.

Orientation proceeds from working-place compositions to local detail.
Non-vesture objects are grouped by encounter location and then ceremony;
vesture and insignia are grouped by minister. Objects limited to or materially
changed in special Masses, Holy Week, pontifical Mass, or related ceremonies
follow in their own section. Cross-references replace unnecessary duplicate
entries, and the plate manifest preserves intentional order within each
section.

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
server selection or artwork. The generated held notice must not be treated as
instructions, handling permission, or evidence that an object may be present.
This leaf remains on hold and must not be installed or published. A scaffold
PDF, if built, is a production test only. Plate-manifest order remains a
publication blocker.
