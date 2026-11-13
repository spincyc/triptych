#!/usr/bin/env python3
"""Pending source successor with separate accepted-data and current-code parents.

The historical compiler retains all semantic transitions, English conservation,
original raw replays and direct-PD proof checks. A single source-namespace read
uses the delivery resolver; parent, path selection and byte-reading functions
are replaced explicitly. This preparation never accepts or installs a fixture.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import runpy
import sys
import types

sys.dont_write_bytecode = True
os.environ.update(TRIPTYCH_SOURCE_LIBRARY_CACHE='0', TRIPTYCH_LIBRARY_CACHE='0',
                  GIT_NO_LAZY_FETCH='1', GIT_NO_REPLACE_OBJECTS='1')
# Invoke from the repository root; the reviewed driver may be retained under
# workflows/reviews without changing the source or code parents it selects.
ROOT = Path.cwd().resolve()
OWN = ROOT / '.scratch/source-epoch'
sys.path[:0] = [str(ROOT), str(ROOT / 'scripts')]
SOURCE_PARENT = 'c448036bd6a407cea691be69aabf2f281a08db81'
CODE_PARENT = '92032f517865220d7ec7019a31b23f8a3217a78e'
PREFIX = 'workflows/reviews/missal-english-completion-2026-10-29/'
COMPILER = PREFIX + 'source-guard/compile_successor_v3.py'
COMPILER_SHA = '29d0add9b330248b4047881310175614d91adc82688bfc695451318696c0865b'
SUPPORT = PREFIX + 'source-guard/support_v3.py'
SUPPORT_SHA = '6fd8b3552071f4ef479bbdc6c4d693331b8ceb91e48dcb016e91033fd6ba03fc'
HELPER = 'tools/tests/_source_batch_guards.py'
OLD_HELPER_SHA = 'f60498c9c9f28f72d69d729b1d086044fa3877803327bb4e16d779c479ad55b1'
HELPER_SHA = '556bb3530c2176bfa66c7d656c81a83c976b89fea97b2592fc91f8d24be32bc0'
FIXTURE = 'tools/tests/fixtures/missal-source-batch-20261023.json'
FIXTURE_SHA = '3bcf736daf2c6afd3eabb2bfd3f3e8528beddb513d1c496051a25255b9b933b3'
MANIFEST = 'tools/tests/fixtures/missal-source-batch-20261023-inputs.json'
MANIFEST_SHA = 'ea29e0b2f4ae20bb73626f88070608a5a7b76a2dead18a3d7daee32ebc3c9f2b'
ACCEPTANCE = PREFIX + 'next-english-2026-10-30/sanitizer-correction/source-batch-acceptance.json'
ACCEPTANCE_SHA = '4d35419fbb3f7a9cf59c2e2934addfeba0327f832f436d3f9fe0de83a4c23871'
DELIVERY_INDEX = 'src/sources/artifact-delivery.json'
# Code-owned exact successors are filled only after their independent review.
# A source/declaration record cannot authorize an unlisted Python module.
RUNTIME_SUCCESSORS = {
    'scripts/_calendars.py': {
        'before_sha256': '54f37042b07ae107a9bea59fe6080d5699f70290335ae7ddee453752f35eb7d4',
        'after_sha256': 'fa14a540f00ede6a13835cc65e50656a2384934f4d94e9d946d84a9a92d269f7',
    },
    'scripts/_oration_endings.py': {
        'before_sha256': None,
        'after_sha256': '6450ff3667f74fedcbd3874e928d46de23a3f9186519ed63f61f41204cb1113c',
    },
    'scripts/_proper_finite_latin_20261029.py': {
        'before_sha256': 'aa925ac3883a807498b0596ce1535a4c2b93bbc2d49913782d49ea7e4736d9f5',
        'after_sha256': '265855db9750c54cc9bd503ba867cd72d17072ffe3ea80b0af8a27f45416fbf3',
    },
    'tools/mass-propers': {
        'before_sha256': '1e6ed563783d81d510d63d43a81e9fe14d195107de4d796225fd633f127b780a',
        'after_sha256': 'c7b7e58cec3bcc88b2e5d22aa82e8f1e9a03ce55f899401e84fe090a9af9481f',
    },
}
RUNTIME_REVIEW = {
    'path': 'workflows/reviews/missal-reader-resume-2026-11-12/source-epoch/runtime-code-review-v2.json',
    'sha256': '1ab3d4b4328eeb223d067d8844986fad6907c31530a6151b6644cd79d125370d',
}
LEGACY4_CORRECTION = {
    'path': 'workflows/reviews/missal-reader-resume-2026-11-12/postconciliar-legacy-four/correction-declaration.json',
    'sha256': '0916fb56c38eaf8e9d43b34c71d52e0755f6d6674a0453b95f05a30779d7994c',
}
LEGACY4_ADOPTION = {
    'path': 'workflows/reviews/missal-reader-resume-2026-11-12/postconciliar-legacy-four/root-adoption.json',
    'sha256': '55f05c49294a80843a9423ab19196ba99c16cba5b0acf33caf48e7695778fc13',
}
PENTECOST_ADMISSION = {
    'path': PREFIX + 'postconciliar/2026-11-12-pentecost-latin-admission.json',
    'sha256': '44ef8380662dbc72ec152a13741f405111119b1c5b527e612b1493fcc24145c8',
}
PENTECOST_IDENTITY = ('pentecost', 'extended-vigil', 'Prayer after the Third Reading', 'all', 1)
PENTECOST_FIELDS = {'source_latin_sha256', 'source_latin_passage_id', 'source_latin_publication_source_ids'}
LEGACY4_IDENTITIES = (
    ('advent-2', 'main', 'Prayer over the Offerings', 'all', 1),
    ('advent-3', 'main', 'Prayer over the Offerings', 'all', 1),
    ('easter-4', 'main', 'Collect', 'all', 1),
    ('easter-4', 'main', 'Prayer over the Offerings', 'all', 1),
)
RAW = Path(__file__).read_bytes()
NAMESPACE_BEFORE = """        actual = {str(path.relative_to(root)): digest(path.read_bytes())
                  for prefix in prefixes for path in (root / prefix).rglob('*') if path.is_file()}"""
NAMESPACE_AFTER = """        actual = _delivery_namespace(root, prefixes, pins)"""
SUPPORT_DELIVERY_EXPRESSIONS = (
    ('digest((source / dependency).read_bytes())',
     'digest(_source_input_path(source, dependency, pins).read_bytes())'),
    ('== (source / payload).stat().st_size',
     '== _source_input_path(source, payload, pins).stat().st_size'),
)


def require(value, label):
    if not value:
        raise AssertionError('source epoch adapter: ' + label)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + '\n').encode()


def relative(name):
    require(isinstance(name, str) and bool(name), 'path string')
    path = Path(name)
    require(not path.is_absolute() and '..' not in path.parts and path.as_posix() == name, 'canonical relative path')
    return name


def ordinary(name):
    target = ROOT / relative(name)
    current = ROOT
    for part in Path(name).parts:
        current /= part
        require(not current.is_symlink(), 'ordinary path ancestry ' + name)
    require(target.is_file(), 'ordinary file ' + name)
    return target


def reference(ref):
    require(set(ref) == {'path', 'sha256'}, 'exact reference fields')
    raw = ordinary(ref['path']).read_bytes()
    require(sha(raw) == ref['sha256'], 'exact selected reference ' + ref['path'])
    return json.loads(raw), raw


class Adapter:
    def __init__(self):
        self.parent_cache = None
        self.pins = None
        self.declaration = None
        self.observed_code = {}
        for name, expected in ((COMPILER, COMPILER_SHA), (SUPPORT, SUPPORT_SHA)):
            require(sha(ordinary(name).read_bytes()) == expected, 'immutable historical implementation ' + name)
        self.support = self.load_support()
        self.store = self.support['GitObjects'](ROOT)

    def load_support(self):
        raw = ordinary(SUPPORT).read_bytes()
        require(sha(raw) == SUPPORT_SHA, 'immutable support immediately before execution')
        text = raw.decode()
        for before, after in SUPPORT_DELIVERY_EXPRESSIONS:
            require(text.count(before) == 1, 'one exact historical direct-PD delivery expression')
            text = text.replace(before, after)
        module = types.ModuleType('_delivery_compatible_source_support')
        module.__file__ = str(ROOT / SUPPORT)
        module._source_input_path = self.delivery_path
        exec(compile(text, '<delivery-compatible-source-support>', 'exec'), module.__dict__)
        return module.__dict__

    def delivery_path(self, root, name, pins):
        """Resolve one explicit proof dependency without changing its byte checks."""
        require(root.resolve() == ROOT and pins == self.pins, 'delivery sees exact declared source pins')
        relative(name)
        require(name in pins, 'direct-PD dependency belongs to exact source epoch ' + name)
        target = ROOT / name
        if target.is_file():
            target = ordinary(name)
        else:
            from _artifact_store import resolve
            from _source_delivery_policy import external_source_identity
            require(sha(ordinary(DELIVERY_INDEX).read_bytes()) == pins.get(DELIVERY_INDEX),
                    'exact current delivery sidecar for direct-PD dependency')
            identity = external_source_identity(ROOT, name)
            require(identity is not None and identity['sha256'] == pins[name],
                    'exact relocated direct-PD source identity ' + name)
            target = resolve(ROOT, name, fetch=False)
        require(sha(target.read_bytes()) == pins[name], 'entire direct-PD dependency bytes ' + name)
        return target

    def parent_state(self):
        if self.parent_cache is not None:
            return self.parent_cache
        raw, mraw, rraw = (self.store.blob(SOURCE_PARENT, p) for p in (FIXTURE, MANIFEST, ACCEPTANCE))
        require((sha(raw), sha(mraw), sha(rraw)) == (FIXTURE_SHA, MANIFEST_SHA, ACCEPTANCE_SHA), 'exact accepted source parent')
        prior, rows, receipt = map(json.loads, (raw, mraw, rraw))
        require(prior['acceptance'] == {'status': 'accepted', 'receipt_path': ACCEPTANCE,
                                      'receipt_sha256': ACCEPTANCE_SHA}, 'actual source-parent acceptance')
        require(receipt['status'] == 'accepted' and receipt['scope'] == 'missal-source-batch'
                and receipt['source_input_manifest_sha256'] == prior['source_input_manifest_sha256'] == MANIFEST_SHA,
                'source-parent receipt binding')
        require(len(rows) == len({r['path'] for r in rows}) == receipt['source_epoch_paths'] == 7264, 'exact7264 parent domain')
        self.store.verify_rows(SOURCE_PARENT, rows)
        require(sha(self.store.blob(SOURCE_PARENT, HELPER)) == OLD_HELPER_SHA, 'historical strict helper')
        anchor_raw = self.store.blob(self.support['ANCHOR'], FIXTURE)
        require(sha(anchor_raw) == self.support['ANCHOR_FIXTURE_SHA'], 'immutable historical anchor')
        anchor = json.loads(anchor_raw)
        for field in self.support['HISTORICAL_FIELDS']:
            require(prior[field] == anchor[field], 'original historical field ' + field)
        require(set(prior['files']) == set(anchor['files']) and len(prior['files']) == 17, 'original17 replay paths')
        originals = {}
        for name, inverse in prior['files'].items():
            before = self.support['reverse'](self.store.blob(SOURCE_PARENT, name), inverse)
            require(before == self.store.blob(self.support['ORIGINAL'], name)
                    and sha(before) == anchor['files'][name]['before_sha256'], 'original raw Git replay ' + name)
            originals[name] = before
        proof = {'schema': 'triptych-missal-reader-source-parent/v1', 'git_revision': SOURCE_PARENT,
                 'code_parent_git_revision': CODE_PARENT, 'fixture_sha256': FIXTURE_SHA,
                 'manifest_sha256': MANIFEST_SHA, 'receipt_path': ACCEPTANCE,
                 'receipt_sha256': ACCEPTANCE_SHA, 'strict_helper_sha256': OLD_HELPER_SHA,
                 'source_epoch_paths': len(rows), 'historical_fields': list(self.support['HISTORICAL_FIELDS']),
                 'original17_before': {p: sha(b) for p, b in originals.items()}, 'support_sha256': SUPPORT_SHA}
        self.parent_cache = self.support, self.support, self.store, prior, rows, originals, proof
        return self.parent_cache

    def configure(self, path, expected):
        raw = path.read_bytes()
        require(sha(raw) == expected, 'review-selected declaration bytes')
        d = json.loads(raw)
        require(d['schema'] == 'triptych-missal-reader-source-successor/v1', 'declaration schema')
        require(d['source_parent'] == SOURCE_PARENT and d['code_parent'] == CODE_PARENT
                and d['parent_fixture_sha256'] == FIXTURE_SHA and d['adapter_sha256'] == sha(RAW), 'exact selected parents and adapter')
        rows, _ = reference(d['source_input_rows'])
        require(isinstance(rows, list) and all(set(r) == {'path', 'post_sha256'} for r in rows), 'source-map rows')
        pins = {relative(r['path']): r['post_sha256'] for r in rows}
        require(len(rows) == len(pins) and [r['path'] for r in rows] == sorted(pins), 'distinct sorted source paths')
        prior = {r['path']: r['post_sha256'] for r in self.parent_state()[4]}
        require(set(prior) <= set(pins), 'all7264 parent paths retained')
        require(pins.get(HELPER) == HELPER_SHA and DELIVERY_INDEX in pins, 'reviewed helper and delivery index bound')
        require(pins.get(RUNTIME_REVIEW['path']) == RUNTIME_REVIEW['sha256'], 'exact runtime review belongs to source epoch')
        runtime_review, _ = reference(RUNTIME_REVIEW)
        require(runtime_review.get('schema') == 'triptych-source-epoch-runtime-code-review/v2'
                and runtime_review.get('status') == 'accepted'
                and runtime_review.get('code_parent') == CODE_PARENT
                and runtime_review.get('accepted_code_owned_successors') == RUNTIME_SUCCESSORS,
                'Root runtime review matches exact code-owned constants')
        self.receipt = relative(d['receipt_path'])
        require(self.receipt.startswith('workflows/reviews/') and self.receipt.endswith('.json'), 'review receipt path')
        require(not ({FIXTURE, MANIFEST, self.receipt} & set(pins)) and not (ROOT / self.receipt).exists(), 'no fixture or receipt cycle')
        excluded = {'src/sources/inventories/claude-publications-v1.toml', 'src/sources/inventories/source-containment-v1.toml',
                    'src/sources/inventories/source-family-migration-v1.toml'}
        require(not (set(pins) & excluded), 'historical shared-registry exclusions')
        for name in set(pins) - set(prior):
            require(name.startswith('src/sources/') or (name.startswith('workflows/reviews/') and name.endswith('.json')),
                    'bounded source/review addition ' + name)
        delta, _ = reference(d['source_delta'])
        require(delta['parent_git_revision'] == SOURCE_PARENT and delta['parent_manifest_sha256'] == MANIFEST_SHA,
                'input delta parent')
        require(delta['extra_inputs'] == sorted(set(pins) - set(prior)), 'complete explicit input additions')
        changes = []
        tree = self.store.tree(SOURCE_PARENT)
        for name in sorted(pins):
            if pins[name] != prior.get(name):
                changes.append({'path': name, 'before_sha256': sha(self.store.blob(SOURCE_PARENT, name)) if name in tree else None,
                                'post_sha256': pins[name]})
        require(delta['files'] == changes, 'exact complete changed input dictionaries')
        refs = [d['source_input_rows'], d['source_delta'], *d['reviews']]
        require(bool(d['reviews']), 'independent review references required')
        for kind, flag in [('sources', 'source_writers_closed'), ('generators', 'generators_closed')]:
            marker, _ = reference(d['settlement'][kind])
            require(marker.get(flag) is True and marker['source_parent'] == SOURCE_PARENT, 'explicit settled ' + kind)
            require(marker['source_input_rows_sha256'] == d['source_input_rows']['sha256'], 'settlement binds full final source map')
            require(d['settlement'][kind]['path'] not in pins, 'settlement/source-map cycle')
            refs.append(d['settlement'][kind])
        for ref in refs:
            reference(ref)
        self.pins, self.declaration = pins, d
        self.declaration_path, self.declaration_raw, self.references = path, raw, refs
        self.read_epoch(ROOT, set(pins))

    def read_epoch(self, root, paths):
        require(root.resolve() == ROOT and self.pins is not None and set(paths) == set(self.pins), 'explicit complete current scope')
        from _artifact_store import resolve
        from _source_delivery_policy import external_source_identity
        require(sha(ordinary(DELIVERY_INDEX).read_bytes()) == self.pins[DELIVERY_INDEX], 'exact current delivery sidecar')
        result = {}
        for name in sorted(paths):
            target = ROOT / name
            if target.is_file():
                raw = ordinary(name).read_bytes()
            else:
                identity = external_source_identity(ROOT, name)
                require(identity is not None and identity['sha256'] == self.pins[name], 'exact relocated source identity ' + name)
                raw = resolve(ROOT, name, fetch=False).read_bytes()
            result[name] = sha(raw)
            require(result[name] == self.pins[name], 'entire current input ' + name)
        require(result[HELPER] == HELPER_SHA, 'strict delivery helper successor')
        return result

    def namespace(self, root, prefixes, pins):
        require(root.resolve() == ROOT and pins == self.pins, 'namespace sees exact declared source pins')
        from _artifact_store import delivery_entries, resolve
        names = {p.relative_to(ROOT).as_posix() for prefix in prefixes for p in (ROOT / prefix).rglob('*') if p.is_file()}
        names.update(e['path'] for e in delivery_entries(ROOT) if e['path'].startswith(prefixes))
        result = {}
        for name in names:
            path = ROOT / name
            if not path.is_file():
                require(name in pins, 'external namespace member must be explicitly pinned ' + name)
                path = resolve(ROOT, name, fetch=False)
            result[name] = sha(path.read_bytes())
        return result

    def positive_complement(self, root, pins, calendar, before, current):
        """Finite exact corrections and one source binding preserve other positives."""
        if calendar != 'postconciliar':
            return self.original_positive_complement(root, pins, calendar, before, current)
        require(root.resolve() == ROOT and pins == self.pins, 'correction uses exact current source scope')
        canonical = self.support['canonical']
        protected = dict(before)
        proofs = []
        expected_keys = set()
        if LEGACY4_CORRECTION is not None:
            require(LEGACY4_ADOPTION is not None, 'exact Root correction adoption required')
            for ref in (LEGACY4_CORRECTION, LEGACY4_ADOPTION):
                require(pins.get(ref['path']) == ref['sha256'], 'exact correction/adoption must belong to source epoch')
            correction, _ = reference(LEGACY4_CORRECTION)
            adoption, _ = reference(LEGACY4_ADOPTION)
            require(correction.get('schema') == 'triptych-exact-positive-english-corrections/v1'
                    and correction.get('calendar') == calendar, 'exact correction schema and calendar')
            require(adoption.get('schema') == 'triptych-postconciliar-legacy-four-root-adoption/v1'
                    and adoption.get('status') == 'accepted'
                    and adoption.get('correction_declaration') == LEGACY4_CORRECTION,
                    'Root acceptance bound to exact correction declaration')
            rows = correction['rows']
            require(isinstance(rows, list) and len(rows) == 4, 'exact four correction dictionaries')
            by_key = {canonical(row['identity']): row for row in rows}
            legacy_keys = {canonical(list(key)) for key in LEGACY4_IDENTITIES}
            require(set(by_key) == legacy_keys, 'exact four correction owner identities')
            expected_keys.update(legacy_keys)
            for key in sorted(legacy_keys):
                row = by_key[key]
                require(before[key] == row['old_entry'] and current.get(key) == row['new_entry'],
                        'entire reviewed positive before/after dictionary ' + key)
                protected[key] = row['new_entry']
                proofs.append({'calendar': calendar, 'identity': key,
                               'correction_path': LEGACY4_CORRECTION['path'],
                               'correction_sha256': LEGACY4_CORRECTION['sha256'],
                               'root_adoption_path': LEGACY4_ADOPTION['path'],
                               'root_adoption_sha256': LEGACY4_ADOPTION['sha256']})
        if PENTECOST_ADMISSION is not None:
            ref = PENTECOST_ADMISSION
            require(pins.get(ref['path']) == ref['sha256'], 'exact Pentecost admission must belong to source epoch')
            admission, _ = reference(ref)
            require(admission['schema'] == 'triptych-finite-exact-target-latin-admission/v1'
                    and admission['target'] == list(PENTECOST_IDENTITY), 'exact Pentecost admission identity')
            review = {'path': admission['source_review_path'], 'sha256': admission['source_review_sha256']}
            require(pins.get(review['path']) == review['sha256'], 'exact Pentecost source review belongs to source epoch')
            reference(review)
            key = canonical(list(PENTECOST_IDENTITY))
            old, new = admission['before_english_entry'], admission['after_english_entry']
            require(set(admission['english_delta_fields']) == PENTECOST_FIELDS
                    and not (set(old) & PENTECOST_FIELDS)
                    and set(new) - set(old) == PENTECOST_FIELDS
                    and {k: v for k, v in new.items() if k not in PENTECOST_FIELDS} == old,
                    'Pentecost adds only three source binding fields; all prior dictionaries stay exact')
            require(before[key] == old and current.get(key) == new, 'entire exact Pentecost before/after English entry')
            english = [row['text'] for row in old['translations'] if row.get('lang') == 'en']
            require(len(english) == 1 and sha(english[0].encode()) == admission['english_body_unchanged_sha256'],
                    'unchanged complete Pentecost English body')
            protected[key] = new
            expected_keys.add(key)
            proofs.append({'calendar': calendar, 'identity': key, 'correction_path': ref['path'],
                           'correction_sha256': ref['sha256'], 'source_review_path': review['path'],
                           'source_review_sha256': review['sha256'], 'added_fields': sorted(PENTECOST_FIELDS)})
        changed = {key for key, value in before.items() if current.get(key) != value}
        require(changed == expected_keys, 'no missing or additional prior-positive correction')
        return protected, proofs

    def scope_paths(self, root, rows, extra):
        require(root.resolve() == ROOT and rows == self.parent_state()[4], 'source scope parent')
        old = {r['path'] for r in rows}
        require(extra == sorted(set(self.pins) - old), 'exact declared extras')
        return set(self.pins)

    def check_code(self, path):
        path = Path(path)
        if not path.is_absolute():
            path = ROOT / path
        if not path.is_relative_to(ROOT):
            return
        name = path.relative_to(ROOT).as_posix()
        if name.startswith('.scratch/'):
            require(path.resolve().is_relative_to(Path(sys.prefix).resolve()) or path.resolve() == Path(__file__).resolve(),
                    'no additional scratch runtime code ' + name)
            return
        raw = ordinary(name).read_bytes()
        if name not in self.store.tree(CODE_PARENT):
            require(RUNTIME_SUCCESSORS.get(name) == {'before_sha256': None, 'after_sha256': sha(raw)},
                    'no unreviewed new runtime module ' + name)
            self.observed_code[name] = sha(raw)
            return
        parent = self.store.blob(CODE_PARENT, name)
        if raw != parent:
            require(name in RUNTIME_SUCCESSORS and RUNTIME_SUCCESSORS[name] == {'before_sha256': sha(parent), 'after_sha256': sha(raw)},
                    'code-owned exact runtime successor required ' + name)
        self.observed_code[name] = sha(raw)

    def audit(self, event, args):
        if event == 'exec' and isinstance(args[0], types.CodeType):
            filename = args[0].co_filename
            if filename and not filename.startswith('<'):
                self.check_code(filename)

    def load_compiler(self):
        raw = ordinary(COMPILER).read_bytes()
        require(sha(raw) == COMPILER_SHA, 'immutable compiler immediately before execution')
        text = raw.decode()
        require(text.count(NAMESPACE_BEFORE) == 1, 'one exact historical namespace expression')
        changed = text.replace(NAMESPACE_BEFORE, NAMESPACE_AFTER)
        module = types.ModuleType('_delivery_compatible_source_compiler')
        module.__file__ = str(ROOT / COMPILER)
        exec(compile(changed, '<delivery-compatible-source-compiler>', 'exec'), module.__dict__)
        module.PARENT = SOURCE_PARENT
        module.HELPER_SHA = HELPER_SHA
        module.parent_state = self.parent_state
        module.scope_paths = self.scope_paths
        module.read_epoch = self.read_epoch
        module._delivery_namespace = self.namespace
        self.original_positive_complement = module.positive_complement
        module.positive_complement = self.positive_complement
        # Scope is already a complete root-selected path/hash declaration.
        module.extra_input = lambda name: require(name in self.pins, 'explicit named input only ' + name)
        return module

    def recheck(self):
        require(Path(__file__).read_bytes() == RAW and self.declaration_path.read_bytes() == self.declaration_raw, 'adapter/declaration drift')
        for ref in self.references:
            reference(ref)
        for name, expected in self.observed_code.items():
            require(sha(ordinary(name).read_bytes()) == expected, 'consumed runtime code drift ' + name)
        self.read_epoch(ROOT, set(self.pins))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['verify-parent', 'derive'])
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--declaration', type=Path)
    parser.add_argument('--declaration-sha256')
    args = parser.parse_args()
    out = args.out.resolve()
    require(out.is_relative_to(OWN) and not out.exists(), 'fresh exclusive scratch output')
    adapter = Adapter()
    if args.command == 'verify-parent':
        proof = adapter.parent_state()[-1]
        out.mkdir(parents=True)
        (out / 'parent-proof.json').write_bytes(encoded(proof))
        print(json.dumps({'status': 'exact accepted source parent verified', 'source_inputs': 7264,
                          'original_streams': 17, 'candidate_derived': False}))
        return
    require(args.declaration is not None and args.declaration_sha256 is not None, 'exact settled declaration required')
    # Audit repository code before the first delivery/runtime dependency loads.
    sys.addaudithook(adapter.audit)
    adapter.configure(args.declaration.resolve(), args.declaration_sha256)
    compiler = adapter.load_compiler()
    delta = adapter.declaration['source_delta']
    compiler.derive(ROOT, out, adapter.receipt, ROOT / delta['path'], delta['sha256'], COMPILER_SHA)
    adapter.recheck()
    result = json.loads((out / 'postimages' / FIXTURE).read_bytes())
    require(result['acceptance']['status'] == 'pending', 'preparation cannot accept source epoch')
    require(result['direct_pd_permitted_specs'] == adapter.parent_state()[3]['direct_pd_permitted_specs'], 'exact original25 direct-PD oracle complement')
    proof = {'schema': 'triptych-missal-reader-source-adapter-proof/v1', 'status': 'pending-independent-review',
             'canonical_writes': 0, 'source_permission_created': False, 'adapter_sha256': sha(RAW),
             'historical_compiler_sha256': COMPILER_SHA, 'historical_support_sha256': SUPPORT_SHA,
             'source_parent': SOURCE_PARENT, 'code_parent': CODE_PARENT, 'helper_sha256': HELPER_SHA,
             'compiler_namespace_expression': {'before': NAMESPACE_BEFORE, 'after': NAMESPACE_AFTER},
             'support_delivery_expressions': [{'before': before, 'after': after}
                                              for before, after in SUPPORT_DELIVERY_EXPRESSIONS],
             'replaced_functions': ['parent_state', 'scope_paths', 'read_epoch', 'extra_input', 'positive_complement'],
             'exact_positive_correction': LEGACY4_CORRECTION, 'exact_positive_correction_adoption': LEGACY4_ADOPTION,
             'exact_pentecost_binding_admission': PENTECOST_ADMISSION,
             'exact_runtime_review': RUNTIME_REVIEW,
             'code_owned_runtime_successors': RUNTIME_SUCCESSORS, 'runtime_code_sha256': adapter.observed_code,
             'declaration_sha256': args.declaration_sha256, 'source_inputs': len(adapter.pins)}
    (out / 'adapter-proof.json').write_bytes(encoded(proof))
    print(json.dumps({'status': proof['status'], 'source_inputs': len(adapter.pins), 'adapter_proof_sha256': sha(encoded(proof))}))


if __name__ == '__main__':
    main()
