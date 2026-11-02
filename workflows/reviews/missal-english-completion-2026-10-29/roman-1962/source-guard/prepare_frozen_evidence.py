#!/usr/bin/env python3
"""Pin frozen plan-declared evidence; no source scan, installation or adoption."""
import argparse
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OWN = Path(__file__).resolve().parent


def digest(data):
    return sha256(data).hexdigest()


def read(path):
    selected = ROOT / path
    if selected.is_symlink() or not selected.resolve().is_relative_to(ROOT):
        raise ValueError('unsafe evidence input path: ' + path)
    return selected.read_bytes()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', required=True)
    parser.add_argument('--extra-receipt', action='append', default=[])
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    script_hash = digest(Path(__file__).read_bytes())
    output = ROOT / args.out
    if output.exists() or not output.resolve().is_relative_to(OWN):
        raise ValueError('fresh owned scratch output required')
    raw = read(args.manifest)
    manifest = json.loads(raw)
    inputs = {args.manifest: digest(raw)}
    links, plans, receipts = [], [], {}

    def receipt(record):
        if not record.get('path') or not record.get('sha256'):
            return
        path, expected = record['path'], record['sha256']
        if digest(read(path)) != expected:
            raise ValueError('receipt pin failed: ' + path)
        receipts[path] = expected
        inputs[path] = expected

    for qualified, selected_plans in (
            (True, manifest['plans']),
            (False, manifest.get('outside_qualified_scope', []))):
        for selected in selected_plans:
            path = selected['path']
            raw_plan = read(path)
            if digest(raw_plan) != selected['sha256']:
                raise ValueError('frozen plan pin failed: ' + path)
            inputs[path] = digest(raw_plan)
            plan = json.loads(raw_plan)
            plans.append({'path': path, 'sha256': digest(raw_plan),
                          'qualified': qualified})
            for row in plan['rows']:
                provenance = row['latin_provenance']
                body_hash = digest(row['new_proper']['text'].encode())
                if body_hash != provenance['text_sha256']:
                    raise ValueError('plan body hash failed: ' + path)
                english = row.get('english')
                english_hash = (digest(english.encode()) if isinstance(english, str)
                                else row.get('english_sha256'))
                row_review = {'path': row.get('review_path'),
                              'sha256': row.get('review_sha256')}
                source_receipts = row.get('source_evidence_receipts', [])
                links.append({
                    'identity': row['identity'], 'body_sha256': body_hash,
                    'english_sha256': english_hash, 'plan': path,
                    'qualification_basis': provenance['publication_basis'],
                    'row_review_role_as_declared': row.get('review_role',
                        'Role not separately declared; no inference from a generic review path.'),
                    'row_review': row_review,
                    'source_evidence_receipts_as_declared': source_receipts,
                })
                for item in [row_review] + source_receipts:
                    receipt(item)
            for field in ('rights_recommendations',
                          'independent_actual_source_evidence_receipts',
                          'mechanical_checks'):
                for item in plan.get(field, []):
                    receipt(item)
            if selected.get('receipt'):
                path = selected['receipt']
                receipt({'path': path, 'sha256': digest(read(path))})
    for path in args.extra_receipt:
        receipt({'path': path, 'sha256': digest(read(path))})
    result = {
        'schema': 'triptych-finite-frozen-scope-evidence-preflight/v1',
        'state': 'pending-root-adoption', 'compiler_sha256': script_hash,
        'frozen_manifest': {'path': args.manifest, 'sha256': inputs[args.manifest]},
        'plans': plans, 'cases': links,
        'declared_receipt_pins': [{'path': path, 'sha256': value}
                                 for path, value in sorted(receipts.items())],
        'role_boundary': 'Exact roles and links copied from frozen plans; verified byte hashes only. No new source-image inspection, rights judgment, gate, approval, or adoption inferred.',
        'global_source_stability_confirmed': False, 'activation_performed': False,
    }
    for path, expected in inputs.items():
        if digest(read(path)) != expected:
            raise ValueError('used evidence changed during preflight: ' + path)
    if digest(Path(__file__).read_bytes()) != script_hash:
        raise ValueError('preflight compiler source changed')
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'path': args.out, 'sha256': digest(output.read_bytes()),
                      'cases': len(links), 'receipts': len(receipts)}))


if __name__ == '__main__':
    main()
