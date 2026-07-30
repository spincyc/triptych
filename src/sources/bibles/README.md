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
publishable: true              # may this text be served from the public site?
notice: ''                     # required when rights is licensed
passages:
  'Psalm 24:1-3': 'The earth is the Lord's, and the fulness thereof...'
```

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
