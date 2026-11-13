"""Activate an exact reviewed test-only successor after all old bytes validate."""
import argparse
import hashlib
import json
from pathlib import Path
import runpy
import sys

ROOT = Path.cwd().resolve()
sys.dont_write_bytecode = True
sys.path[:0] = [str(ROOT), str(ROOT / 'scripts')]
FIXTURE = 'tools/tests/fixtures/missal-source-batch-20261023.json'
MANIFEST = 'tools/tests/fixtures/missal-source-batch-20261023-inputs.json'
TESTS = {
    'tools/tests/test_proper_latin.py',
    'tools/tests/test_roman_1962_common_virgin_ii_english_phase4.py',
    'tools/tests/test_roman_1962_common_virgin_ii_word_repair.py',
    'tools/tests/test_roman_1962_octnov_commemoration_source_repair.py',
    'tools/tests/test_roman_1962_winter_ursula_source_repair.py',
    'tools/tests/test_roman_1962_latin22_phase5.py',
    'tools/tests/test_missal_coverage.py',
}
PINNED_TESTS = TESTS - {'tools/tests/test_missal_coverage.py'}


def require(value, label):
    if not value:
        raise AssertionError('test bookkeeping activation: ' + label)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + '\n').encode()


def local(name):
    path = Path(name)
    require(not path.is_absolute() and '..' not in path.parts and path.as_posix() == name,
            'canonical relative path')
    result = ROOT
    for part in path.parts:
        result /= part
        require(not result.is_symlink(), 'no symlink ancestry ' + name)
    return result


def read(path, expected):
    raw = path.read_bytes()
    require(sha(raw) == expected, 'exact bytes ' + str(path))
    return raw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, required=True)
    parser.add_argument('--plan-sha256', required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    plan = json.loads(read(args.plan, args.plan_sha256))
    require(plan['schema'] == 'triptych-test-bookkeeping-activation-plan/v1', 'plan schema')
    require(sha(Path(__file__).read_bytes()) == plan['activation_driver_sha256'], 'reviewed driver')
    parent_fixture_raw = read(local(FIXTURE), plan['parent_fixture_sha256'])
    parent_manifest_raw = read(local(MANIFEST), plan['parent_manifest_sha256'])
    parent_fixture = json.loads(parent_fixture_raw)
    parent_manifest = json.loads(parent_manifest_raw)
    parent_pins = {row['path']: row['post_sha256'] for row in parent_manifest}
    require(len(parent_pins) == len(parent_manifest) == 7449, 'exact parent domain')
    review_ref = plan['root_review']
    review = json.loads(read(local(review_ref['path']), review_ref['sha256']))
    require(review['status'] == 'accepted', 'actual Root review')
    changes = plan['files']
    names = [row['path'] for row in changes]
    require(len(names) == len(set(names)), 'distinct activation outputs')
    require(set(names) & set(parent_pins) == PINNED_TESTS, 'only six captured test changes')
    require(TESTS <= set(names), 'all seven reviewed test changes')
    payloads = {}
    bundle = args.plan.parent / 'postimages'
    for row in changes:
        target = local(row['path'])
        if row['before_sha256'] is None:
            require(not target.exists(), 'new evidence remains absent ' + row['path'])
        else:
            read(target, row['before_sha256'])
        payloads[row['path']] = read(bundle / row['path'], row['after_sha256'])
    # Entire old source epoch validates before any test or accounting write.
    from _artifact_store import resolve
    from _source_delivery_policy import external_source_identity
    read(local('src/sources/artifact-delivery.json'), parent_pins['src/sources/artifact-delivery.json'])
    for name, expected in parent_pins.items():
        path = local(name)
        if not path.is_file():
            identity = external_source_identity(ROOT, name)
            require(identity is not None and identity['sha256'] == expected, 'exact external owner ' + name)
            path = resolve(ROOT, name, fetch=False)
        read(path, expected)
    for path, expected in plan['runtime_code_sha256'].items():
        read(local(path), expected)
    read(local('tools/tests/test_roman_1962_boniface_annual_source_repair.py'),
         '2faf9225873fd7e05dbcd44fba32098dc3c6cf14d386caa8c4c8aaba086e269e')
    next_manifest = json.loads(payloads[MANIFEST])
    next_pins = {row['path']: row['post_sha256'] for row in next_manifest}
    require([row['path'] for row in parent_manifest] == [row['path'] for row in next_manifest],
            'same ordered source domain')
    require({name for name in parent_pins if parent_pins[name] != next_pins[name]} == PINNED_TESTS,
            'only exact six input pins')
    for name in PINNED_TESTS:
        require(sha(payloads[name]) == next_pins[name], 'postimage test input ' + name)
    data = json.loads(payloads[FIXTURE])
    changed_fields = {key for key in parent_fixture if parent_fixture[key] != data[key]}
    require(set(parent_fixture) == set(data) and changed_fields ==
            {'files', 'source_input_manifest_sha256', 'acceptance', 'state'}, 'all semantic fields exact')
    require(set(data['files']) == set(parent_fixture['files']) and len(data['files']) == 17,
            'original seventeen replay domain')
    require({name for name in data['files'] if data['files'][name] != parent_fixture['files'][name]}
            == PINNED_TESTS, 'only six replay specifications')
    support_path = 'workflows/reviews/missal-english-completion-2026-10-29/source-guard/support_v3.py'
    read(local(support_path), '6fd8b3552071f4ef479bbdc6c4d693331b8ceb91e48dcb016e91033fd6ba03fc')
    reverse = runpy.run_path(str(local(support_path)))['reverse']
    for name, before_spec in parent_fixture['files'].items():
        before = local(name).read_bytes()
        after = payloads.get(name, before)
        require(reverse(before, before_spec) == reverse(after, data['files'][name]),
                'same entire original replay ' + name)
    delta = json.loads(payloads[plan['delta_path']])
    require(set(delta['test_code_inverses_to_c5']) == TESTS, 'seven test inverses')
    for name, spec in delta['test_code_inverses_to_c5'].items():
        require(reverse(payloads[name], spec) == local(name).read_bytes(), 'entire c5 test preimage ' + name)
    reconstruction = delta['c5_reconstruction']
    restored = json.loads(payloads[FIXTURE])
    restored.update(reconstruction['replace_top_level_fields'])
    restored['files'].update(reconstruction['replace_six_file_specs'])
    require(encoded(restored) == parent_fixture_raw, 'reconstruct entire accepted c5 fixture')
    restored_manifest = json.loads(payloads[MANIFEST])
    for row in restored_manifest:
        if row['path'] in reconstruction['replace_six_input_pins']:
            row['post_sha256'] = reconstruction['replace_six_input_pins'][row['path']]
    require(encoded(restored_manifest) == parent_manifest_raw, 'reconstruct entire accepted c5 manifest')
    receipt_path = plan['receipt_path']
    receipt = json.loads(payloads[receipt_path])
    require(data['acceptance'] == {'status': 'accepted', 'receipt_path': receipt_path,
                                  'receipt_sha256': sha(payloads[receipt_path])}, 'exact acceptance binding')
    require(receipt['status'] == 'accepted' and receipt['scope'] == 'missal-source-batch' and
            receipt['source_input_manifest_sha256'] == sha(payloads[MANIFEST]) ==
            data['source_input_manifest_sha256'], 'exact accepted manifest')
    require(receipt['root_test_compatibility_review'] == review_ref, 'accepted exact Root review')
    core = {key: value for key, value in data.items() if key not in {'acceptance', 'state'}}
    require(sha(encoded(core)) == receipt['accepted_fixture_core_sha256'], 'complete fixture core')
    if args.apply:
        for row in changes:
            target = local(row['path'])
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payloads[row['path']])
            require(sha(target.read_bytes()) == row['after_sha256'], 'written exact output ' + row['path'])
    print(json.dumps({'status': 'activated' if args.apply else 'validated; no canonical writes',
                      'files': len(changes), 'entire_old_inputs_verified': 7449,
                      'changed_test_input_pins': 6, 'original_replays_preserved': 17,
                      'accepted_fixture_sha256': sha(payloads[FIXTURE]),
                      'accepted_manifest_sha256': sha(payloads[MANIFEST]),
                      'receipt_sha256': sha(payloads[receipt_path])}))


if __name__ == '__main__':
    main()
