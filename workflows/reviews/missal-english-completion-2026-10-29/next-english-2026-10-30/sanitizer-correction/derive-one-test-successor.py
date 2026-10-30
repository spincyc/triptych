#!/usr/bin/env python3
"""One current-checksum test pin and raw inverse; no semantic derivation."""
import argparse
import ast
import copy
import hashlib
import json
from pathlib import Path
import runpy
import sys

sys.dont_write_bytecode = True
OWN = '.scratch/next-epoch-semantics-20261030/sanitizer-test-pin-successor'
PARENT = '61a2b2ae6a80d61b19f409097d07016b50fb8f48'
FIXTURE = 'tools/tests/fixtures/missal-source-batch-20261023.json'
FIXTURE_SHA = 'ae34d8450f42835523ee6c5c2ec44cf5d99f6289adc83654853aa47c3fbe1b97'
MANIFEST = 'tools/tests/fixtures/missal-source-batch-20261023-inputs.json'
MANIFEST_SHA = '13505e8e805b221f78f8004586ca2b4e8f2f2de0c20a2a5e28799af589464e84'
RECEIPT = 'workflows/reviews/missal-english-completion-2026-10-29/next-english-2026-10-30/source-batch-acceptance.json'
RECEIPT_SHA = '5ae2464f2e7a73218262bf91473de8cbcc98e54840dc19d22b02dcb89b110072'
SUPPORT = 'workflows/reviews/missal-english-completion-2026-10-29/source-guard/support_v3.py'
SUPPORT_SHA = '6fd8b3552071f4ef479bbdc6c4d693331b8ceb91e48dcb016e91033fd6ba03fc'
HELPER = 'tools/tests/_source_batch_guards.py'
HELPER_SHA = 'f60498c9c9f28f72d69d729b1d086044fa3877803327bb4e16d779c479ad55b1'
TEST = 'tools/tests/test_roman_1962_latin22_phase5.py'
BEFORE_SHA = '01d6e0490f4b84683823795b2917a8804d17b8b32b38af49b2caa97fca0f015d'
ORIGINAL_SHA = '7dc3a1569140e14f32fa2c98e607577b05871f3c197a307db67107d731d6afca'
OLD_CODE = 'd94a4301e865dc7d7f9fc8d657761201675e0123041e3ef00973b36565199376'
NEW_CODE = '852acb6a88084aba5729e5f60e807ca4e10f9c4436f5db2b23a9fdd3fbe2da1a'
APPLICATION = 'workflows/reviews/missal-english-completion-2026-10-29/next-english-2026-10-30/sanitizer-correction/actual-application.json'
APPLICATION_SHA = '5d8c6804c0c2b83dca5d0f08b4ee0b91df1aaa72a26ac0c837ba2b5ab79fded4'
FUTURE_RECEIPT = 'workflows/reviews/missal-english-completion-2026-10-29/next-english-2026-10-30/sanitizer-correction/source-batch-acceptance.json'
RAW = Path(__file__).read_bytes()


def require(value, message):
    if not value:
        raise AssertionError('sanitizer one-test accounting: ' + message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encode(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + '\n').encode()


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--after-sha256', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    root, out = Path.cwd().resolve(), args.out.resolve()
    require(out.is_relative_to(root / OWN) and not out.exists(), 'fresh exclusive scratch output')
    require(len(args.after_sha256) == 64 and all(c in '0123456789abcdef' for c in args.after_sha256), 'exact root-selected applied test digest')
    require(sha((root / SUPPORT).read_bytes()) == SUPPORT_SHA, 'immutable replay support')
    support = runpy.run_path(str(root / SUPPORT))
    store = support['GitObjects'](root)
    before_fixture, before_manifest, receipt_raw = (store.blob(PARENT, p) for p in (FIXTURE, MANIFEST, RECEIPT))
    require((sha(before_fixture), sha(before_manifest), sha(receipt_raw)) == (FIXTURE_SHA, MANIFEST_SHA, RECEIPT_SHA), 'exact accepted parent')
    prior, rows, receipt = map(json.loads, (before_fixture, before_manifest, receipt_raw))
    require(prior['acceptance'] == {'status': 'accepted', 'receipt_path': RECEIPT, 'receipt_sha256': RECEIPT_SHA}
            and receipt['status'] == 'accepted' and receipt['source_input_manifest_sha256'] == MANIFEST_SHA, 'actual parent receipt binding')
    require(len(rows) == len({r['path'] for r in rows}) == 7264, 'exact7264 parent inputs')
    store.verify_rows(PARENT, rows)
    require(sha((root / FIXTURE).read_bytes()) == FIXTURE_SHA and sha((root / MANIFEST).read_bytes()) == MANIFEST_SHA, 'parent still installed')
    require(sha((root / HELPER).read_bytes()) == sha(store.blob(PARENT, HELPER)) == HELPER_SHA, 'immutable f604')
    require(sha((root / APPLICATION).read_bytes()) == APPLICATION_SHA and sha((root / 'scripts/_proper_latin.py').read_bytes()) == NEW_CODE, 'already accepted sanitizer context')
    before, after = store.blob(PARENT, TEST), (root / TEST).read_bytes()
    require(sha(before) == BEFORE_SHA and sha(after) == args.after_sha256, 'exact selected test pre/postimages')
    require(before.count(('"' + OLD_CODE + '"').encode()) == 1, 'one stale current checksum literal')
    expected = before.replace(('"' + OLD_CODE + '"').encode(), ('"' + NEW_CODE + '"').encode())
    require(ast.dump(ast.parse(after), include_attributes=False) == ast.dump(ast.parse(expected), include_attributes=False), 'only accepted current-code checksum AST changes')
    originals = {p: support['reverse'](store.blob(PARENT, p), spec) for p, spec in prior['files'].items()}
    require(len(originals) == 17 and sha(originals[TEST]) == ORIGINAL_SHA, 'exact original target stream')
    require(all(raw == store.blob(support['ORIGINAL'], p) for p, raw in originals.items()), 'all17 actual original Git streams')
    new = copy.deepcopy(prior)
    new['files'][TEST] = support['replay_spec'](originals[TEST], after)
    new_rows = [{**r, 'post_sha256': args.after_sha256} if r['path'] == TEST else r for r in rows]
    new['source_input_manifest_sha256'] = sha(encode(new_rows))
    new['acceptance'] = {'status': 'pending', 'receipt_path': FUTURE_RECEIPT, 'receipt_sha256': None}
    new['state'] = 'One current sanitizer-checksum test input successor; independent accounting acceptance pending'
    require(all(canonical(new[k]) == canonical(prior[k]) for k in prior if k not in {'files', 'source_input_manifest_sha256', 'acceptance', 'state'}), 'all other semantic/oracle fields exact')
    require(all(canonical(new['files'][p]) == canonical(prior['files'][p]) for p in prior['files'] if p != TEST), 'other16 inverse specifications exact')
    for row in new_rows:
        require(sha((root / row['path']).read_bytes()) == row['post_sha256'], 'entire named current input ' + row['path'])
    require(Path(__file__).read_bytes() == RAW and not (root / FUTURE_RECEIPT).exists(), 'stable driver and unused pending receipt')
    core = {k: v for k, v in new.items() if k not in {'acceptance', 'state'}}
    old_core = {k: v for k, v in prior.items() if k not in {'acceptance', 'state'}}
    proof = {'schema': 'triptych-exact-one-test-input-successor/v1', 'status': 'pending-independent-accounting-review',
             'parent_git_revision': PARENT, 'parent_fixture_sha256': FIXTURE_SHA, 'parent_manifest_sha256': MANIFEST_SHA,
             'parent_acceptance_sha256': RECEIPT_SHA, 'driver_sha256': sha(RAW), 'source_paths': 7264,
             'source_delta': [{'path': TEST, 'before_sha256': BEFORE_SHA, 'post_sha256': args.after_sha256}],
             'old_fixture_core_sha256': sha(encode(old_core)), 'new_fixture_core_sha256': sha(encode(core)),
             'pending_fixture_sha256': sha(encode(new)), 'manifest_sha256': sha(encode(new_rows)),
             'original17_before': {p: sha(raw) for p, raw in originals.items()}, 'other16_inverse_specifications_exact': True,
             'all_other_semantic_oracles_exact': True, 'historical_fields_exact': list(support['HISTORICAL_FIELDS']),
             'unchanged_semantic_transition_contract_sha256': prior['reviewed_transition_contract_sha256'],
             'accepted_sanitizer_application': {'path': APPLICATION, 'sha256': APPLICATION_SHA},
             'current_sanitizer_code_sha256': NEW_CODE, 'runtime_permission_or_source_judgment_created': False,
             'scope': 'One test checksum pin/raw inverse only. No current runtime imported, semantic compiler run or Names metadata mixed in.',
             'canonical_writes': 0}
    out.mkdir(parents=True)
    for name, raw in ((FIXTURE, encode(new)), (MANIFEST, encode(new_rows))):
        target = out / 'postimages' / name;target.parent.mkdir(parents=True, exist_ok=True);target.write_bytes(raw)
    (out / 'bookkeeping-proof.json').write_bytes(encode(proof))
    print(json.dumps({'status': proof['status'], 'pending_fixture_sha256': proof['pending_fixture_sha256'],
                      'manifest_sha256': proof['manifest_sha256'], 'new_core_sha256': proof['new_fixture_core_sha256']}, sort_keys=True))


if __name__ == '__main__':
    main()
