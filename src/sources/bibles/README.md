# Indexed bibles

Verse text keyed by scripture reference, so `mass-propers --bible <id>` can
render a proper's appointed passages instead of bare references.

## Layout

One directory per edition, each with an `index.yaml`:

```yaml
schema: triptych-bible-index/v1
edition: The Holy Bible, Douay-Rheims (Challoner revision)
source_id: work.douay-rheims.challoner
rights: public-domain          # public-domain | licensed | project-created
numbering: vulgate             # vulgate | hebrew — psalm numbering system
publishable: true              # may this text be served from the public site?
notice: ''                     # required when rights is licensed
passages:
  'Psalm 24:1-3': 'The earth is the Lord's, and the fulness thereof...'
```

## An index is generated, not written

`index-bible` builds an edition's `index.yaml` from the per-book verse files
already registered under that edition in `src/sources/works/`, so a rebuild is
offline and reproducible and no text is transcribed twice:

```sh
tools/tpt index-bible check          # is the tracked index current?
tools/tpt index-bible build          # rewrite it
```

`passages` is keyed by the reference string, which cannot enumerate a whole
bible: `Psalm 24:1-3` and `Psalm 24:4` are separate keys and the key space is
open. An index therefore covers the references the tracked calendars actually
cite, and `coverage` in each index says so. A calendar that gains a reference
needs a rebuild, and `check` fails until it gets one.

Book names are mapped through the edition's own book index rather than a table
kept here. The Douay-Rheims prints Vulgate names, and the trap is not the
spelling but the shift: Douay 1 and 2 Kings are modern 1 and 2 Samuel, while
Douay 3 and 4 Kings are modern 1 and 2 Kings.

## Psalm numbering is not cosmetic

Vulgate and Hebrew psalm numbering diverge across most of the psalter. The same
Advent chant *Ad te levavi* is Psalm 24 in the 1962 missal and Psalm 25 in the
postconciliar one, and Douay-Rheims Psalm 25 is *Iudica me* — a different psalm.
Resolving a reference against a bible in the other system therefore returns the
wrong text under a correct-looking reference.

Every index declares its `numbering`, every calendar declares its
`psalm_numbering`, and `mass-propers` refuses to resolve across a mismatch
rather than rendering something plausible and wrong.

Keys are the reference as the calendar indexes write it, which is what
`mass-propers` looks up. Deriving them from the structured `book`/`ranges`
rather than the display string is the more robust choice and is the direction
the calendar data is moving.

## Rights govern where a text may live

An edition being reachable online does not place it under this project's
licence, and permission to *use* a text is not always permission to
*redistribute* it. `THIRD_PARTY.md` is the controlling record.

- `rights: public-domain` — may be tracked here and served publicly.
- `rights: licensed` — carries `notice`, and `publishable` reflects whether the
  permission extends to public redistribution. When it does not, keep the index
  outside the repository and point at it with
  `mass-propers --bible-root <path>`; the tool resolves any root, so a licensed
  text stays usable locally without ever being committed or published.
- `rights: project-created` — CC BY 4.0 only where the project authorship is
  identified as such.

Only editions marked `publishable: true` may be baked into the public-alpha
artifact. The public site is built by `public-alpha build` and verified before
deployment; an unpublishable edition reaching that artifact is a rights defect,
not a formatting one.
