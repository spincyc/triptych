# Alpha Publication Records

Each migrated publication owns one independently writable JSON record at:

`release/publications/<provider>/<leaf-id>.json`

The directory structure after `<provider>/` is the publication leaf ID. A
record holds only the publication-facing policy that nothing else states:

```json
{
  "status": "alpha",
  "authorization": "perpetual-public-repository-2026"
}
```

Its `schema_version` (1), its `id` (the path below the provider) and its
`catalog` (the library page the owning leaf's kind registers in
`src/common/document-schemas/registry.toml`) are derived by
`_document_schema.release_record`; an explicit value must agree. A kind whose
leaves live in more than one catalog (calendar references, Ordinary
expositions, historical accounts) has no registered catalog, and each of its
records states its own `catalog`.

`status` is `alpha` or `hold`. An alpha record names the standing
authorization; a hold record uses `null`. PDF hashes and aggregate counts are
not tracked here. The public artifact generates its current PDF hashes,
publication inventory, counts, and checksums from the installed files.

The active inventory consists of these local records. The loader remains
compatible with an unmigrated legacy row, but migration does not rewrite
another publication's record or the shared historical rights tables.
