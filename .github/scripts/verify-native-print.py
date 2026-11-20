"""Reconcile all native print shard receipts with the Pages build that will ship."""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
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
    args = parser.parse_args()
    try:
        if args.verb == "site-key":
            print(site_key(args.site, args.revision))
        else:
            count = join(args.receipts, args.shards, args.revision, args.site_key)
            print(f"Verified {count} compiled native print editions against the Pages artifact.")
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"native print verification: {error}\n")


if __name__ == "__main__":
    main()
