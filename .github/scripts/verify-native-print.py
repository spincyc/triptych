"""Reconcile all native print shard receipts with the Pages build that will ship."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from _native_print_compile import join, site_key


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    verbs = parser.add_subparsers(dest="verb", required=True)
    site = verbs.add_parser("site-key", help="hash every native print render in the verified artifact")
    site.add_argument("--site", type=Path, required=True)
    site.add_argument("--revision", required=True)
    check = verbs.add_parser("join", help="check all current-run receipt sets against the site")
    check.add_argument("--receipts", type=Path, required=True)
    check.add_argument("--shards", type=int, required=True)
    check.add_argument("--revision", required=True)
    check.add_argument("--site-key", required=True)
    merge = verbs.add_parser("merge", help="assemble the full source catalog from authenticated same-run shards")
    merge.add_argument("--references", type=Path, required=True)
    merge.add_argument("--expected-keys", type=Path, required=True)
    merge.add_argument("--out", type=Path, required=True)
    merge.add_argument("--shards", type=int, required=True)
    merge.add_argument("--revision", required=True)
    merge.add_argument("--run-id", required=True)
    merge.add_argument("--run-attempt", required=True)
    args = parser.parse_args()
    try:
        if args.verb == "site-key":
            print(site_key(args.site, args.revision))
        elif args.verb == "merge":
            from _native_print import admitted_documents, source_revision
            from _native_print_reference import merge_reference_catalogs, write_reference_catalog
            if args.revision != source_revision(ROOT):
                raise ValueError("reference revision differs from this checkout")
            result = merge_reference_catalogs(args.references, root=ROOT, documents=admitted_documents(ROOT),
                                              revision=args.revision, run_id=args.run_id, run_attempt=args.run_attempt,
                                              shards=args.shards, expected_keys=json.loads(args.expected_keys.read_bytes()))
            print(write_reference_catalog(args.out, result, run_id=args.run_id, run_attempt=args.run_attempt))
        else:
            count = join(args.receipts, args.shards, args.revision, args.site_key)
            print(f"Verified {count} compiled native print editions against the Pages artifact.")
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"native print verification: {error}\n")


if __name__ == "__main__":
    main()
