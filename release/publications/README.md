# Alpha Publication Records

Each migrated publication owns one independently writable JSON record at:

`release/publications/<provider>/<leaf-id>.json`

The directory structure after `<provider>/` is the publication leaf ID. A
schema-version-1 record contains exactly the publication-facing policy needed
for alpha inclusion:

```json
{
  "schema_version": 1,
  "id": "articles/example",
  "catalog": "library/faith.md",
  "status": "alpha",
  "authorization": "perpetual-public-repository-2026"
}
```

`status` is `alpha` or `hold`. An alpha record names the standing
authorization; a hold record uses `null`. PDF hashes and aggregate counts are
not tracked here. The public artifact generates its current PDF hashes,
publication inventory, counts, and checksums from the installed files.

During migration, a local record overrides the matching legacy row in
`release/public-alpha.json`. Publications without a local record continue to
use the legacy row. This permits one publication to migrate without rewriting
another publication's release data or the shared historical rights tables.
