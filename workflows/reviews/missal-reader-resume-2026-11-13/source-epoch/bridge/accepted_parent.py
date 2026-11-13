"""Proposed exact parent wrapper with finite d85/five-payload delivery proof."""
from hashlib import sha256
import json
import os
from pathlib import Path
import runpy
import sys

os.environ.update(GIT_NO_LAZY_FETCH='1', GIT_NO_REPLACE_OBJECTS='1')
sys.dont_write_bytecode = True
ROOT = Path.cwd().resolve()
sys.path[:0] = [str(ROOT), str(ROOT / 'scripts')]
PARENT = '80cbdbb0357d00c809049c4f44b6d42f3c7a6a7c'
FIXTURE = 'tools/tests/fixtures/missal-source-batch-20261023.json'
FIXTURE_SHA = 'f4f1b85f2abf94391a478fa0f16eac20362eea461a16cc8e3d92f083b76d3d33'
MANIFEST = 'tools/tests/fixtures/missal-source-batch-20261023-inputs.json'
MANIFEST_SHA = 'f427c98032220558654aef37d8ccc483ed8dcccb22e4678bbfcf8cdeed4c4658'
RECEIPT = 'workflows/reviews/missal-reader-resume-2026-11-12/source-epoch/source-batch-acceptance-v2.json'
RECEIPT_SHA = '31f4bd15ab80164ea60007e009c6688c1995e33d85066270a378bf0dbe8286b1'
SUPPORT = 'workflows/reviews/missal-english-completion-2026-10-29/source-guard/support_v3.py'
SUPPORT_SHA = '6fd8b3552071f4ef479bbdc6c4d693331b8ceb91e48dcb016e91033fd6ba03fc'
DELIVERY_HELPER = '.scratch/source-epoch/next-cohort/parent_delivery_ten_successor.py'
DELIVERY_HELPER_SHA = '65874a65409a53a9a6e9e401cf8c05ff670694fda8580785ba72b951f65ea8b5'
DIRECT_DECLARATION = 'workflows/reviews/missal-english-completion-2026-10-29/roman-1962/sources/direct-pd-latin-proof-declaration-v1.json'
DIRECT_DECLARATION_SHA = '70716afc9012297f8600c837b129332a1b924b9520b8861d9d6ad33ae4f47752'


def require(value, label):
    if not value:
        raise AssertionError('accepted80cb parent: ' + label)


def digest(raw):
    return sha256(raw.encode() if isinstance(raw, str) else raw).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + '\n').encode()


def current_checked(path, expected):
    raw = (ROOT / path).read_bytes()
    require(digest(raw) == expected, 'exact current implementation ' + path)
    return raw


def parent_state(*, current_root, current_pins):
    """Bind committed receipt/manifest, all actual inputs and original oracles."""
    current_checked(SUPPORT, SUPPORT_SHA)
    current_checked(DELIVERY_HELPER, DELIVERY_HELPER_SHA)
    support = runpy.run_path(str(ROOT / SUPPORT))
    delivery = runpy.run_path(str(ROOT / DELIVERY_HELPER))
    store = support['GitObjects'](ROOT)
    require(store.kind(PARENT) == 'commit', 'exact parent is a local immutable commit')
    require(digest(store.blob(PARENT, SUPPORT)) == SUPPORT_SHA, 'committed immutable support')
    raw, manifest_raw, receipt_raw = (store.blob(PARENT, path) for path in (FIXTURE, MANIFEST, RECEIPT))
    require((digest(raw), digest(manifest_raw), digest(receipt_raw)) ==
            (FIXTURE_SHA, MANIFEST_SHA, RECEIPT_SHA), 'complete accepted parent bytes')
    prior, rows, receipt = map(json.loads, (raw, manifest_raw, receipt_raw))
    require(prior['acceptance'] == {'status': 'accepted', 'receipt_path': RECEIPT,
                                  'receipt_sha256': RECEIPT_SHA}, 'actual accepted-v2 pointer')
    require(receipt['status'] == 'accepted' and receipt['scope'] == 'missal-source-batch'
            and receipt['source_input_manifest_sha256'] == prior['source_input_manifest_sha256'] == MANIFEST_SHA,
            'exact receipt and manifest binding')
    core = {key: value for key, value in prior.items() if key not in {'acceptance', 'state'}}
    require(digest(encoded(core)) == receipt['accepted_fixture_core_sha256'], 'complete accepted fixture core')
    inputs = delivery['verify_parent_rows'](current_root, store, PARENT, rows,
                                           current_pins=current_pins)
    additions = []
    for path in delivery['added_records']():
        body = delivery['read_added_external'](current_root, path, current_pins)
        additions.append({'path': path, 'sha256': digest(body), 'bytes': len(body)})
    require(len(rows) == receipt['source_epoch_paths'] == 7449, 'exact logical parent domain')
    helper = 'tools/tests/_source_batch_guards.py'
    require(digest(store.blob(PARENT, helper)) == receipt['strict_runtime_helper_sha256'] ==
            '556bb3530c2176bfa66c7d656c81a83c976b89fea97b2592fc91f8d24be32bc0', 'unchanged strict source helper')
    anchor_raw = store.blob(support['ANCHOR'], FIXTURE)
    require(digest(anchor_raw) == support['ANCHOR_FIXTURE_SHA'], 'original historical anchor bytes')
    anchor = json.loads(anchor_raw)
    for field in support['HISTORICAL_FIELDS']:
        require(prior[field] == anchor[field], 'unchanged entire historical field ' + field)
    require(set(prior['files']) == set(anchor['files']) and len(prior['files']) == 17,
            'original seventeen replay paths')
    originals, replay_proof = {}, []
    for path, inverse in prior['files'].items():
        after = store.blob(PARENT, path)
        before = support['reverse'](after, inverse)
        require(before == store.blob(support['ORIGINAL'], path)
                and digest(before) == anchor['files'][path]['before_sha256'], 'entire original Git bytes ' + path)
        try:
            support['reverse'](after + b'changed\n', inverse)
        except AssertionError:
            pass
        else:
            raise AssertionError('altered replay bytes accepted: ' + path)
        originals[path] = before
        replay_proof.append({'path': path, 'original_sha256': digest(before),
                             'parent_sha256': digest(after), 'altered_current_bytes_refused': True})
    declaration_raw = store.blob(PARENT, DIRECT_DECLARATION)
    require(digest(declaration_raw) == DIRECT_DECLARATION_SHA, 'complete original direct25 declaration')
    declaration = json.loads(declaration_raw)
    expected = {support['canonical'](row['key']): row for row in declaration['records']}
    require(len(expected) == 25 and prior['direct_pd_permitted_specs'] == expected,
            'all original25 complete oracle dictionaries unchanged')
    proof = {'schema': 'triptych-accepted-80cb-source-parent-proof/v1', 'status': 'pass',
             'parent_git_revision': PARENT, 'fixture_sha256': digest(raw), 'manifest_sha256': digest(manifest_raw),
             'acceptance_path': RECEIPT, 'acceptance_sha256': digest(receipt_raw),
             'accepted_fixture_core_sha256': digest(encoded(core)), 'input_verification': inputs,
             'historical_fields': list(support['HISTORICAL_FIELDS']), 'original_replays': replay_proof,
             'complete_original_direct25_oracles_sha256': digest(encoded(expected)),
             'complete_original_direct25_oracles_unchanged': True,
             'direct_declaration_sha256': digest(declaration_raw),
             'delivery_helper_sha256': DELIVERY_HELPER_SHA, 'immutable_support_sha256': SUPPORT_SHA,
             'wrapper_sha256': digest(Path(__file__).read_bytes()),
             'separate_actual_current_additions': additions,
             'canonical_writes': 0, 'source_permission_created': False, 'successor_fixture_derived': False}
    return support, delivery, store, prior, rows, originals, proof


if __name__ == '__main__':
    raise SystemExit('Call parent_state with the exact current source root and selected input pins')
