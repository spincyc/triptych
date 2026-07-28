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

The active inventory consists of these local records. The loader remains
compatible with an unmigrated legacy row, but migration does not rewrite
another publication's record or the shared historical rights tables.
