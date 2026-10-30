#!/usr/bin/env python3
"""Names53-only source accounting. Pending output grants no permission."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import runpy
import sys
import types
import yaml

sys.dont_write_bytecode = True
os.environ['TRIPTYCH_SOURCE_LIBRARY_CACHE'] = '0'
os.environ['TRIPTYCH_LIBRARY_CACHE'] = '0'
OWN = '.scratch/next-epoch-semantics-20261030/naming-metadata-successor'
NAMES = '.scratch/missal-version-nomenclature-20261030/implementation/reconcile-next-english-v1'
READY_SHA = '0bd17f84edb995c2e93efd123ba5087dc055e2652a4d2feaab22aa2c8fd33efb'
FIXTURE = 'tools/tests/fixtures/missal-source-batch-20261023.json'
FIXTURE_SHA = 'ae34d8450f42835523ee6c5c2ec44cf5d99f6289adc83654853aa47c3fbe1b97'
MANIFEST = 'tools/tests/fixtures/missal-source-batch-20261023-inputs.json'
MANIFEST_SHA = '13505e8e805b221f78f8004586ca2b4e8f2f2de0c20a2a5e28799af589464e84'
PARENT_RECEIPT = 'workflows/reviews/missal-english-completion-2026-10-29/next-english-2026-10-30/source-batch-acceptance.json'
RECEIPT_SHA = '5ae2464f2e7a73218262bf91473de8cbcc98e54840dc19d22b02dcb89b110072'
FUTURE_RECEIPT = 'workflows/reviews/missal-version-nomenclature-2026-10-30/source-batch-acceptance.json'
SUPPORT = 'workflows/reviews/missal-english-completion-2026-10-29/source-guard/support_v3.py'
SUPPORT_SHA = '6fd8b3552071f4ef479bbdc6c4d693331b8ceb91e48dcb016e91033fd6ba03fc'
HELPER = 'tools/tests/_source_batch_guards.py'
HELPER_SHA = 'f60498c9c9f28f72d69d729b1d086044fa3877803327bb4e16d779c479ad55b1'
PC = 'src/sources/calendars/postconciliar/propers.yaml'
ROMAN = 'src/sources/calendars/roman-1962/propers.yaml'
HEADERS = {'edition', 'edition_short', 'advisory'}
METADATA = {'src/sources/calendars/README.md', 'src/sources/calendars/recensions.json', PC,
            'src/sources/calendars/roman-pre-1955/propers.yaml'}
RAW = Path(__file__).read_bytes()


def require(value, label):
    if not value:
        raise AssertionError('Names53 metadata: ' + label)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + '\n').encode()


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)


def producer_semantics(value):
    """Only declared top-level presentation fields may differ in producer data."""
    require(isinstance(value, dict), 'producer object')
    metadata = HEADERS | {'reader_version', 'reader_contribution'}
    return {k: v for k, v in value.items() if k not in metadata}


def ordinary(root, name):
    p = Path(name)
    require(isinstance(name, str) and bool(name) and not p.is_absolute()
            and '..' not in p.parts and p.as_posix() == name, 'relative path')
    target = root / p
    require(target.is_file() and not target.is_symlink() and target.resolve().is_relative_to(root)
            and not any(q.is_symlink() for q in target.parents if q != root and q.is_relative_to(root)),
            'ordinary repository input ' + name)
    return target


def pinned(root, name, expected):
    raw = ordinary(root, name).read_bytes()
    require(sha(raw) == expected, 'exact bytes ' + name)
    return raw


def header_only(before, after):
    require(isinstance(before, dict) and isinstance(after, dict), 'YAML objects')
    require(canonical({k: v for k, v in before.items() if k not in HEADERS})
            == canonical({k: v for k, v in after.items() if k not in HEADERS}), 'header-only YAML change')


def catalog_only(before, after):
    """The accepted Names53 catalog transition, including explicit downgrades."""
    require(before['schema'] == 'triptych-roman-recensions/v1'
            and after['schema'] == 'triptych-roman-recensions/v2', 'catalog schema transition')
    require(set(after) == set(before) | {'books', 'reader_views'}, 'catalog top-level fields')
    old, new = copy.deepcopy(before), copy.deepcopy(after)
    for d in (old, new):
        for key in ('schema', 'as_of', 'books', 'reader_views'):
            d.pop(key, None)
    # These two scholarly identities cease to own mixed reader projections.
    for index in (0, 7):
        old['recensions'][index].pop('calendar')
    old['recensions'][0].pop('coverage_ref')
    for name in ('calendar', 'ordinary', 'rubrics'):
        old['recensions'][0]['capabilities'][name].update(
            collation='unestablished', data_availability='unavailable', publication_availability='unavailable')
    language = old['recensions'][0]['language_capabilities'][0]
    language.pop('coverage_ref')
    language.update(collation='unestablished', data_availability='unavailable', publication_availability='unavailable')
    require(canonical(old) == canonical(new), 'catalog preserved scholarly identities and all other capabilities')
    require(len(after['books']) == 9 and [r['calendar'] for r in after['reader_views']]
            == ['roman-1962', 'postconciliar', 'roman-pre-1955'], 'exact book/view inventory')


def names_context(root):
    ready = json.loads(pinned(root, NAMES + '/READY.json', READY_SHA))
    for key in ('exact_patch', 'before_after_paths', 'review'):
        ref = ready[key]
        pinned(root, ref['path'], ref['sha256'])
    updates = {r['path']: r for r in ready['source_epoch_followup']['four_source_pin_updates']}
    require(set(updates) == METADATA, 'exact four metadata paths')
    for name, row in updates.items():
        before = pinned(root, NAMES + '/before/' + name, row['before_sha256'])
        after = pinned(root, NAMES + '/postimages/' + name, row['after_sha256'])
        if name.endswith('.yaml'):
            header_only(yaml.load(before, Loader=yaml.CSafeLoader), yaml.load(after, Loader=yaml.CSafeLoader))
        elif name.endswith('recensions.json'):
            catalog_only(json.loads(before), json.loads(after))
    runtime = {r['path']: r['post_sha256'] for r in ready['source_epoch_followup']['runtime_closure']}
    require(len(runtime) == 7 and runtime.get('scripts/_missal_versions.py')
            == 'f91067f45611c813b7ac10dd7144668a56876d8004941d73bd124053a310cde2', 'exact Names7 runtime closure')
    return ready, updates, runtime


def successor(prior, rows, before, after, originals, support):
    """Pure bookkeeping; all unsupported changes fail before output."""
    require(all(isinstance(r, dict) and set(r) == {'path', 'post_sha256'} for r in rows), 'manifest row schema')
    require(len(rows) == len({r['path'] for r in rows}) == 7264, 'exact7264 scope')
    old = {r['path']: r['post_sha256'] for r in rows}
    require(set(before) == set(after) == METADATA and set(after) <= set(old), 'four existing paths only')
    for name in after:
        require(sha(before[name]) == old[name], 'declared metadata preimage ' + name)
    for name in (PC, 'src/sources/calendars/roman-pre-1955/propers.yaml'):
        header_only(yaml.load(before[name], Loader=yaml.CSafeLoader), yaml.load(after[name], Loader=yaml.CSafeLoader))
    catalog_only(json.loads(before['src/sources/calendars/recensions.json']),
                 json.loads(after['src/sources/calendars/recensions.json']))
    result = copy.deepcopy(prior)
    require(set(prior['files']) & set(after) == {PC}, 'one affected archival replay')
    result['files'][PC] = support['replay_spec'](originals[PC], after[PC])
    new_rows = [{'path': p, 'post_sha256': sha(after[p]) if p in after else old[p]} for p in sorted(old)]
    result['source_input_manifest_sha256'] = sha(encoded(new_rows))
    result['acceptance'] = {'status': 'pending', 'receipt_path': FUTURE_RECEIPT, 'receipt_sha256': None}
    result['state'] = 'Names53 metadata-only successor candidate; independent accounting and runtime review pending'
    allowed = {'files', 'source_input_manifest_sha256', 'acceptance', 'state'}
    require(all(canonical(result[k]) == canonical(prior[k]) for k in prior if k not in allowed), 'every semantic oracle exact')
    require(all(canonical(result['files'][p]) == canonical(prior['files'][p]) for p in prior['files'] if p != PC), 'other16 replay specifications exact')
    return result, new_rows


class Runtime:
    def __init__(self, root, store, parent, names):
        self.root, self.store, self.parent, self.names = root, store, parent, names
        self.observed = {}

    def check(self, path):
        path = path if path.is_absolute() else self.root / path
        require('..' not in path.parts, 'canonical runtime path')
        if not path.is_relative_to(self.root):
            require(not path.resolve().is_relative_to(self.root), 'external runtime alias into repository')
            return
        prefix = Path(sys.prefix).resolve()
        if path.is_relative_to(prefix):
            resolved = path.resolve()
            require(not resolved.is_relative_to(self.root) or resolved.is_relative_to(prefix),
                    'interpreter runtime alias into repository')
            return  # Interpreter packages are environment inputs, not repo code.
        if path == Path(__file__).absolute():
            return
        name = path.relative_to(self.root).as_posix()
        raw = ordinary(self.root, name).read_bytes()
        if name in self.names:
            want = self.names[name]  # Mandatory final hash, including parent-equal cases.
        else:
            require(name in self.store.tree(self.parent), 'unreviewed new runtime ' + name)
            want = sha(self.store.blob(self.parent, name))
        require(sha(raw) == want, 'exact fresh-parent-or-Names runtime ' + name)
        self.observed[name] = want

    def audit(self, event, args):
        if event == 'exec' and isinstance(args[0], types.CodeType):
            name = args[0].co_filename
            if name and not name.startswith('<'):
                self.check(Path(name))


def parent_state(root, revision, support):
    require(isinstance(revision, str) and len(revision) == 40
            and all(c in '0123456789abcdef' for c in revision), 'root must supply fresh accepted parent commit')
    store = support['GitObjects'](root)
    require(store.kind(revision) == 'commit', 'actual parent commit')
    require({FIXTURE, MANIFEST, PARENT_RECEIPT} <= set(store.tree(revision)), 'accepted English parent binding paths')
    prior_raw, rows_raw, receipt_raw = (store.blob(revision, p) for p in (FIXTURE, MANIFEST, PARENT_RECEIPT))
    require((sha(prior_raw), sha(rows_raw), sha(receipt_raw)) == (FIXTURE_SHA, MANIFEST_SHA, RECEIPT_SHA), 'exact accepted English parent binding')
    prior, rows, receipt = map(json.loads, (prior_raw, rows_raw, receipt_raw))
    require(prior['acceptance'] == {'status': 'accepted', 'receipt_path': PARENT_RECEIPT, 'receipt_sha256': RECEIPT_SHA}
            and receipt['status'] == 'accepted' and receipt['scope'] == 'missal-source-batch'
            and prior['source_input_manifest_sha256'] == receipt['source_input_manifest_sha256'] == MANIFEST_SHA,
            'accepted source epoch, not historical runtime authority')
    store.verify_rows(revision, rows)
    require(sha(store.blob(revision, HELPER)) == HELPER_SHA, 'immutable f604 at fresh parent')
    anchor = json.loads(store.blob(support['ANCHOR'], FIXTURE))
    for field in support['HISTORICAL_FIELDS']:
        require(canonical(prior[field]) == canonical(anchor[field]), 'historical partition ' + field)
    originals = {p: support['reverse'](store.blob(revision, p), spec) for p, spec in prior['files'].items()}
    require(len(originals) == 17 and all(raw == store.blob(support['ORIGINAL'], p)
            for p, raw in originals.items()), 'all17 actual original Git streams')
    return store, prior, rows, originals


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--parent', required=True)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    root, out = args.root.resolve(), args.out.resolve()
    require(out.is_relative_to(root / OWN) and not out.exists(), 'fresh own scratch output')
    ready, updates, runtime = names_context(root)
    support = runpy.run_path(str(ordinary(root, SUPPORT))) if sha(ordinary(root, SUPPORT).read_bytes()) == SUPPORT_SHA else None
    require(support is not None, 'immutable support')
    store, prior, rows, originals = parent_state(root, args.parent, support)
    before = {p: store.blob(args.parent, p) for p in updates}
    after = {p: pinned(root, p, r['after_sha256']) for p, r in updates.items()}
    require(all(sha(before[p]) == updates[p]['before_sha256'] for p in before), 'actual new-parent metadata preimages')
    code = Runtime(root, store, args.parent, runtime)
    for name in runtime:
        code.check(root / name)
    for row in rows:
        require(sha(ordinary(root, row['path']).read_bytes()) == (sha(after[row['path']]) if row['path'] in after else row['post_sha256']), 'entire named physical scope ' + row['path'])
    roman_before = yaml.load(store.blob(args.parent, ROMAN), Loader=yaml.CSafeLoader)
    roman_after = yaml.load(ordinary(root, ROMAN).read_bytes(), Loader=yaml.CSafeLoader)
    require(sha(canonical(roman_before).encode()) == prior['current_roman_document_sha256']
            and canonical(roman_before) == canonical(roman_after), 'Names leaves current parsed Roman document exact')
    result, new_rows = successor(prior, rows, before, after, originals, support)
    for row in new_rows:
        pinned(root, row['path'], row['post_sha256'])
    for name in runtime:
        code.check(root / name)
    names_context(root)
    require(Path(__file__).read_bytes() == RAW, 'driver bytes stable')
    require(not (root / FUTURE_RECEIPT).exists(), 'unused future acceptance identity')
    delta = [{'path': p, 'before_sha256': sha(before[p]), 'post_sha256': sha(after[p])} for p in sorted(after)]
    proof = {'schema': 'triptych-Names53-metadata-successor-proof/v1', 'status': 'pending-independent-accounting-and-runtime-review',
             'parent_git_revision': args.parent, 'parent_fixture_sha256': FIXTURE_SHA, 'parent_manifest_sha256': MANIFEST_SHA,
             'parent_receipt_sha256': RECEIPT_SHA, 'driver_sha256': sha(RAW), 'Names_READY_sha256': READY_SHA,
             'source_paths': 7264, 'source_delta': delta, 'manifest_sha256': sha(encoded(new_rows)),
             'pending_fixture_sha256': sha(encoded(result)), 'original17_before': {p: sha(v) for p, v in originals.items()},
             'historical_fields_exact': list(support['HISTORICAL_FIELDS']), 'semantic_oracles_exact': True,
             'parsed_Roman_document_exact': True, 'runtime_closure': code.observed,
             'Names_runtime_preimages': {p: sha(store.blob(args.parent, p)) if p in store.tree(args.parent) else None for p in runtime},
             'runtime_basis': 'Actual fresh parent commit for unchanged modules; exact reviewed Names7 successors. Prior V3 runtime proof remains history.',
             'runtime_evidence_scope': 'Mandatory Names7 bytes checked here; actual transitive producer imports are recorded by the separate source-root behavior checker.',
             'producer_body_eligibility_alias_review': 'pending separate fresh source-root behavior check',
             'publication_permission_created': False, 'canonical_writes': 0}
    out.mkdir(parents=True)
    for name, raw in ((FIXTURE, encoded(result)), (MANIFEST, encoded(new_rows))):
        target = out / 'postimages' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    (out / 'metadata-proof.json').write_bytes(encoded(proof))
    print(json.dumps({'status': proof['status'], 'paths': 7264, 'metadata_changes': 4,
                      'pending_fixture_sha256': proof['pending_fixture_sha256']}, sort_keys=True))


if __name__ == '__main__':
    main()
