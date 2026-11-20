"""Source-phase publication checks and identities partitioned across current-run Pages workers."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

import _document_schema as schema
import _native_print_bundles as bundles
from _native_print_reference import _origin

VERSION = "triptych-publication-source-reference/v1"
DOMAINS = ("content", "evidence", "render")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")


def _need(condition, message):
    if not condition:
        raise ValueError("publication source reference: " + message)


def _assign(root, documents, count):
    """Put an admitted owner with a worker that already ran its native assembly."""
    _need(type(count) is int and count > 0, "invalid partition count")
    owners = schema.publication_owners(root)
    numbers = {key: index % count + 1 for index, key in enumerate(sorted(documents))}
    selections = {}
    for key, doc in sorted(documents.items()):
        if key.startswith("publication:"):
            owner = doc["document"].removeprefix("publication:")
            _need(owner in owners, "admission has no discovered source owner")
            selections.setdefault(owner, []).append(key)
    assigned = {}
    for owner in sorted(owners):
        if owner in selections:
            canonical = "publication:" + owner
            preferred = canonical if canonical in selections[owner] else selections[owner][0]
            assigned[owner] = numbers[preferred]
        else:
            # Held/Markdown sources remain in the source validation census.
            digest = hashlib.sha256(owner.encode()).digest()
            assigned[owner] = 1 + int.from_bytes(digest[:8], "big") % count
    return assigned


def prepare_partition(root, documents, revision, run_id, attempt, shard, assembly):
    _origin(revision, run_id, attempt)
    number, count = shard
    _need(1 <= number <= count and assembly.root == root, "invalid source partition or assembly")
    assigned = _assign(root, documents, count)
    owners = {owner for owner, spot in assigned.items() if spot == number}
    rows = {}
    for record in schema.discover(root, assembly=assembly, owners=owners):
        owner = record["id"]
        report = schema.validate(root, record, phase="source", run_gates=False, assembly=assembly)
        _need(report["ok"], owner + ": " + "; ".join(report["errors"]))
        _need(owner in owners and owner not in rows, "invalid or duplicate source owner")
        row = rows[owner] = {"record": record}
        if any("publication:" + output["id"] in documents for output in record["outputs"]):
            identity = schema.identities(root, record, assembly=assembly)
            # Virtual pages are the actual generated sources read by this
            # Assembly, even when a tracked snapshot has different bytes.
            paths = {name for key in DOMAINS for name in identity[key]["inputs"]}
            virtual = assembly.files(root / record["source_dir"])
            row.update(identity={key: value for key, value in identity.items() if key != "outputs"},
                       virtual={name: hashlib.sha256(virtual[root / name].encode()).hexdigest()
                                for name in paths if root / name in virtual},
                       output_hashes={role: value["sha256"] for role, value in identity["outputs"].items()})
    _need(rows.keys() == owners, "incomplete canonical source discovery")
    return {"schema": VERSION, "revision": revision, "run_id": run_id, "attempt": attempt,
            "shard": list(shard), "records": rows}


def _verify_identity(root, record, row, file_hashes, web_hashes):
    """Reproduce each owning domain and output digest from its exact ordered inputs."""
    directory = record["source_dir"]
    identity, virtual = row["identity"], row["virtual"]
    _need(set(identity) == {*DOMAINS, "limitations"} and isinstance(identity["limitations"], list)
          and all(isinstance(item, str) for item in identity["limitations"]), "invalid source identity")
    all_paths, used_virtual = set(), set()
    for domain in DOMAINS:
        descriptor = identity[domain]
        names = descriptor["inputs"]
        _need(set(descriptor) == {"inputs", "sha256"} and isinstance(names, list)
              and names == sorted(set(names)), "invalid or unordered source input list")
        all_paths.update(names)
        digests = {}
        for name in names:
            bundles._relative(name)
            if name == directory + "/web-edition.toml":
                if name not in web_hashes:
                    web_hashes[name] = schema._web_declaration_identity(bundles._source(root, name))
                digest = web_hashes[name]
            elif name in virtual:
                used_virtual.add(name)
                _need(name.startswith(directory + "/") and SHA256.fullmatch(virtual[name]),
                      "invalid virtual source seal")
                digest = bytes.fromhex(virtual[name])
            else:
                if name not in file_hashes:
                    file_hashes[name] = schema._file_hash(bundles._source(root, name))
                digest = file_hashes[name]
            digests[root / name] = digest
        declaration = schema._raw_manifest(record) if domain == "content" else None
        _need(schema._digest(root, digests, declaration, projections=digests) == descriptor,
              "changed " + domain + " source")
    _need(set(virtual) == used_virtual, "unused virtual source")
    _need(set(row["output_hashes"]) == {o["role"] for o in record["outputs"]}, "unexpected output roles")
    combined = sorted(all_paths)
    output_identities = {}
    for output in record["outputs"]:
        declaration = {"output": {k: v for k, v in output.items() if k in schema.OUTPUT_FIELDS},
                       **{domain: identity[domain]["sha256"] for domain in DOMAINS}}
        result = schema._digest(root, set(), declaration)
        _need(row["output_hashes"][output["role"]] == result["sha256"], "changed output identity")
        output_identities[output["role"]] = {**result, "inputs": combined}
    return {**identity, "outputs": output_identities}


def verify_partitions(root, documents, revision, run_id, attempt, count, parts):
    """Verify the bodies obtained from this consumer's authenticated merged native catalog."""
    _origin(revision, run_id, attempt)
    owners = _assign(root, documents, count)
    _need(isinstance(parts, dict) and set(parts) == {str(i) for i in range(1, count + 1)},
          "incomplete source partition set")
    records, identities, file_hashes, web_hashes = {}, {}, {}, {}
    seen_admitted = set()
    for number in range(1, count + 1):
        part = parts[str(number)]
        _need(isinstance(part, dict) and set(part) == {"schema", "revision", "run_id", "attempt", "shard", "records"}
              and part["schema"] == VERSION and part["revision"] == revision
              and part["run_id"] == run_id and part["shard"] == [number, count], "wrong origin or partition")
        _origin(revision, run_id, part["attempt"])
        _need(int(part["attempt"]) <= int(attempt), "future producer attempt")
        _need(set(part["records"]) == {owner for owner, n in owners.items() if n == number},
              "unexpected or missing publication owners")
        for owner, row in part["records"].items():
            record = row["record"]
            directory = "src/" + owner
            _need(record["id"] == owner == record["provider"] + "/" + record["leaf"]
                  and record["source_dir"] == directory and record["manifest_path"] == directory + "/publication.toml",
                  "wrong source owner")
            actual = schema.tomllib.loads(bundles._source(root, record["manifest_path"]).read_text(encoding="utf-8"))
            _need(actual == record["manifest_declared"], "changed source declaration")
            admitted = False
            for output in record["outputs"]:
                key = schema._id(output["id"])
                _need(key[0] == record["provider"] and key not in records, "duplicate or foreign output")
                _need(output["source_path"] == directory + "/" + output["entrypoint"], "wrong output source")
                records[key] = record, output
                selection = "publication:" + output["id"]
                if selection in documents:
                    _need(documents[selection]["document"] == "publication:" + owner, "wrong admitted output owner")
                    seen_admitted.add(selection)
                    admitted = True
            if admitted:
                _need(set(row) == {"record", "identity", "virtual", "output_hashes"}, "incomplete admitted owner")
                identities[owner] = _verify_identity(root, record, row, file_hashes, web_hashes)
            else:
                _need(set(row) == {"record"}, "unexpected identity for unadmitted owner")
    _need(seen_admitted == {key for key in documents if key.startswith("publication:")},
          "incomplete admitted publication universe")
    return records, identities
