"""Validate an exact prepared activation bundle; write only with explicit --apply."""
import argparse
import hashlib
import json
from pathlib import Path
import sys


ROOT = Path.cwd().resolve()
sys.dont_write_bytecode = True
sys.path[:0] = [str(ROOT), str(ROOT / 'scripts')]


def require(value, label):
    if not value:
        raise AssertionError('source epoch activation: ' + label)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path, expected):
    raw = path.read_bytes()
    require(sha(raw) == expected, 'exact bytes ' + str(path))
    return raw


def local(name):
    path = Path(name)
    require(not path.is_absolute() and '..' not in path.parts and path.as_posix() == name,
            'canonical relative path')
    result = ROOT
    for part in path.parts:
        result /= part
        require(not result.is_symlink(), 'no symlink ancestry ' + name)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, required=True)
    parser.add_argument('--plan-sha256', required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    plan = json.loads(read(args.plan, args.plan_sha256))
    require(plan['schema'] == 'triptych-source-epoch-activation-plan/v1', 'plan schema')
    require(sha(Path(__file__).read_bytes()) == plan['activation_driver_sha256'], 'reviewed activation driver')
    bundle = args.plan.parent / 'postimages'
    changes = plan['files']
    names = [row['path'] for row in changes]
    require(len(names) == len(set(names)), 'distinct activation paths')
    payloads = {}
    for row in changes:
        target = local(row['path'])
        raw = read(bundle / row['path'], row['after_sha256'])
        if row['before_sha256'] is None:
            require(not target.exists(), 'new evidence target remains absent ' + row['path'])
        else:
            read(target, row['before_sha256'])
        payloads[row['path']] = raw
    manifest = plan['manifest_path']
    fixture = plan['fixture_path']
    receipt_path = plan['receipt_path']
    pins = {row['path']: row['post_sha256'] for row in json.loads(payloads[manifest])}
    require(len(pins) == plan['source_epoch_paths'], 'exact full source domain')
    require(not (set(names) & set(pins)), 'activation outputs cannot mutate source input pins')
    for name, expected in plan['runtime_code_sha256'].items():
        read(local(name), expected)
    read(local('tools/tests/_source_batch_guards.py'), pins['tools/tests/_source_batch_guards.py'])
    from _artifact_store import resolve
    from _source_delivery_policy import external_source_identity
    delivery_path = 'src/sources/artifact-delivery.json'
    read(local(delivery_path), pins[delivery_path])
    for name, expected in pins.items():
        target = local(name)
        if not target.is_file():
            identity = external_source_identity(ROOT, name)
            require(identity is not None and identity['sha256'] == expected, 'exact external owner ' + name)
            target = resolve(ROOT, name, fetch=False)
        read(target, expected)
    data = json.loads(payloads[fixture])
    receipt = json.loads(payloads[receipt_path])
    require(data['acceptance'] == {'status': 'accepted', 'receipt_path': receipt_path,
                                    'receipt_sha256': sha(payloads[receipt_path])}, 'exact receipt binding')
    require(receipt['status'] == 'accepted' and receipt['scope'] == 'missal-source-batch'
            and receipt['source_input_manifest_sha256'] == sha(payloads[manifest])
            == data['source_input_manifest_sha256'], 'exact accepted manifest binding')
    core = {key: value for key, value in data.items() if key not in {'acceptance', 'state'}}
    core_raw = (json.dumps(core, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + '\n').encode()
    require(sha(core_raw) == receipt['accepted_fixture_core_sha256'], 'complete accepted fixture core')
    if args.apply:
        for row in changes:
            target = local(row['path'])
            target.parent.mkdir(parents=True, exist_ok=True)
            # Source inputs were all checked before the first write. The plan
            # orders evidence, receipt, manifest, then fixture; no symlink alias.
            with target.open('wb') as stream:
                stream.write(payloads[row['path']])
            require(sha(target.read_bytes()) == row['after_sha256'], 'written activation bytes')
    print(json.dumps({'status': 'activated' if args.apply else 'validated; no canonical writes',
                      'files': len(changes), 'source_inputs_verified': len(pins),
                      'accepted_fixture_sha256': sha(payloads[fixture]),
                      'receipt_sha256': sha(payloads[receipt_path])}))


if __name__ == '__main__':
    main()
