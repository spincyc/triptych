#!/usr/bin/env python3
"""Scratch adapter for an exact settled successor; this grants no permission.

The tracked compiler/support/helper remain immutable. Only parent_state and
scope_paths are replaced in memory; the original semantic derive is retained.
"""
from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sys
import types

sys.dont_write_bytecode = True
os.environ['TRIPTYCH_SOURCE_LIBRARY_CACHE'] = '0'
os.environ['TRIPTYCH_LIBRARY_CACHE'] = '0'
ROOT = Path.cwd().resolve()
OWN = ROOT / '.scratch/next-epoch-semantics-20261030'
PREFIX = 'workflows/reviews/missal-english-completion-2026-10-29/'
COMPILER = PREFIX + 'source-guard/compile_successor_v3.py'
COMPILER_SHA = '29d0add9b330248b4047881310175614d91adc82688bfc695451318696c0865b'
SUPPORT = PREFIX + 'source-guard/support_v3.py'
SUPPORT_SHA = '6fd8b3552071f4ef479bbdc6c4d693331b8ceb91e48dcb016e91033fd6ba03fc'
HELPER = 'tools/tests/_source_batch_guards.py'
HELPER_SHA = 'f60498c9c9f28f72d69d729b1d086044fa3877803327bb4e16d779c479ad55b1'
PARENT = '702f650020d69a45aa747b1c5b5e30be6c42ca59'
FIXTURE = 'tools/tests/fixtures/missal-source-batch-20261023.json'
FIXTURE_SHA = '11a3eee509b55233556f89a60d4ce978264ab215e483f354b2bcbad9b39304ee'
MANIFEST = 'tools/tests/fixtures/missal-source-batch-20261023-inputs.json'
MANIFEST_SHA = '6956adb9fc4336282ade4bce43015d51bb2b73ef9a2ccce1d62e90226022693c'
ACCEPTANCE = PREFIX + 'main-reconciliation-v1/source-batch-classification-acceptance.json'
ACCEPTANCE_SHA = '2c05072109012b7da86c21da2ab23a1b5c89c317cc6be1c21b3f70acfe8e2cca'
FUTURE_ACCEPTANCE = PREFIX + 'next-english-2026-10-30/source-batch-acceptance.json'
FINITE = 'scripts/_proper_finite_latin_20261029.py'
FINITE_BEFORE = '34c7ea2520f0917108495ea333323c33e4eb3b6993aba2e10c91fc49385dfb40'
FINITE_INTERMEDIATE = 'ecca66760debc9c0451e1b6743883c55d59390f575b4503b6af27d9923117fd3'
FINITE_AFTER = 'aa925ac3883a807498b0596ce1535a4c2b93bbc2d49913782d49ea7e4736d9f5'
FINITE_ACTIVATION = {
    'path': PREFIX + 'next-english-2026-10-30/roman-1962/actual-authority-activation.json',
    'sha256': '55a3ea92a0d4892607d7376bf16c339b7fc5e1aeb6b82fd1a4af663ded7fadff',
}
FINITE_REVIEWS = [
    {'path': '.scratch/roman-english-completion-20261029/v2-consolidation/pure-quarantine-review-v1/review.json',
     'sha256': 'b2f859809819b9a24e3a1f488bcd136cae87bcf0b918375244f5c2a349881105'},
    {'path': '.scratch/roman-english-completion-20261029/v2-consolidation/pure-quarantine-regression-v1/receipt.json',
     'sha256': 'dc5542cdc8bdfc5040f98d650a01376fd74dbc2a25512cd2a193a28224a8e030'},
]
FINITE_SUCCESSOR = {
    'kind': 'finite22-quarantine-claim-successor', 'before_sha256': FINITE_BEFORE,
    'intermediate_sha256': FINITE_INTERMEDIATE, 'after_sha256': FINITE_AFTER,
    'intermediate_activation': FINITE_ACTIVATION, 'independent_reviews': FINITE_REVIEWS,
}
FINITE_INPUTS = {
    PREFIX + 'roman-1962/finite-latin-authority-v2.json': '495e5b3672cccb8f2c3ea07398104c4b72026ffb7139de21d25087edcab1f48e',
    PREFIX + 'next-english-2026-10-30/roman-1962/root-seven-decision.json': 'd0802309d2518db774c3ad352f2eba03605e67cad735959444b422233ffd4874',
    PREFIX + 'next-english-2026-10-30/roman-1962/root-seven-decision-binding.json': 'bbfaac484a6f2f3775900288093688e068c83a7df56edfe5659753764c74022f',
    PREFIX + 'next-english-2026-10-30/roman-1962/activation-independent-review.json': '92d1933b2f6778c37059a9de6375fe79eb70dd070c96477307b69ba81915cab9',
    FINITE_ACTIVATION['path']: FINITE_ACTIVATION['sha256'],
}
EXAMPLE_TOOLS = {'tools/mass-propers', 'tools/source-library', 'tools/source-reader'}
ADAPTER_RAW = Path(__file__).read_bytes()


def require(value, label):
    if not value:
        raise AssertionError('settled semantic adapter: ' + label)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + '\n').encode()


def relative(value):
    require(isinstance(value, str) and bool(value), 'path string')
    path = Path(value)
    require(not path.is_absolute() and '..' not in path.parts and path.as_posix() == value, 'canonical relative path')
    return value


def ordinary(root, name):
    path = root / relative(name)
    require(path.is_file() and not path.is_symlink(), 'ordinary input ' + name)
    require(path.resolve().is_relative_to(root.resolve()) and not any(
        p.is_symlink() for p in path.parents if p != root and p.is_relative_to(root)), 'ordinary input ancestors ' + name)
    return path


def pinned_json(root, ref):
    require(set(ref) == {'path', 'sha256'}, 'exact path/hash reference fields')
    raw = ordinary(root, ref['path']).read_bytes()
    require(sha(raw) == ref['sha256'], 'exact reference bytes ' + ref['path'])
    return json.loads(raw), raw


def rows_to_map(rows):
    require(isinstance(rows, list) and all(isinstance(r, dict) and set(r) == {'path', 'post_sha256'} for r in rows), 'manifest row schema')
    result = {}
    for row in rows:
        name = relative(row['path'])
        require(name not in result, 'duplicate source path')
        require(isinstance(row['post_sha256'], str) and len(row['post_sha256']) == 64
                and all(c in '0123456789abcdef' for c in row['post_sha256']), 'SHA256 pin')
        result[name] = row['post_sha256']
    require([r['path'] for r in rows] == sorted(result), 'source rows must be sorted')
    return result


def examples_only(before, after):
    """Require byte-exact non-EXAMPLES code and unchanged example commands."""
    def split(raw):
        text = raw.decode()
        tree = ast.parse(text)
        found = [n for n in tree.body if isinstance(n, ast.Assign)
                 and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
                 and n.targets[0].id == 'EXAMPLES']
        require(len(found) == 1, 'one EXAMPLES assignment')
        node = found[0]
        # AST columns count UTF-8 bytes. Exclude precisely the assignment node,
        # retaining even statements/comments sharing its opening/closing line.
        # Only Python physical newlines count here; e.g. form feeds do not.
        starts = [0, *(m.end() for m in re.finditer(rb'\r\n|\r|\n', raw))]
        start = starts[node.lineno - 1] + node.col_offset
        end = starts[node.end_lineno - 1] + node.end_col_offset
        require(0 <= start < end <= len(raw), 'exact EXAMPLES byte span')
        prefix, suffix = raw[:start], raw[end:]
        normal = copy.deepcopy(node)
        for item in ast.walk(normal):
            if isinstance(item, ast.Call):
                require(isinstance(item.func, ast.Name) and item.func.id == 'Example'
                        and 2 <= len(item.args) <= 3 and not item.keywords, 'literal Example contract')
                value = ast.literal_eval(item.args[1])
                require(isinstance(value, tuple) and all(isinstance(v, str) or v is Ellipsis for v in value), 'literal captured transcript')
                item.args[1] = ast.Constant(value=None)
        return prefix, suffix, ast.dump(normal, include_attributes=False)
    a, b = split(before), split(after)
    require(a == b, 'only captured EXAMPLES transcripts may change')


def load_compiler(root=None):
    root = ROOT if root is None else root
    for name, expected in ((COMPILER, COMPILER_SHA), (SUPPORT, SUPPORT_SHA), (HELPER, HELPER_SHA)):
        require(sha(ordinary(root, name).read_bytes()) == expected, 'immutable code ' + name)
    spec = importlib.util.spec_from_file_location('_immutable_next_english_v3', root / COMPILER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Adapter:
    def __init__(self, compiler, root=None):
        self.compiler = compiler
        self.root = (ROOT if root is None else root).resolve()
        self.parent_cache = None
        self.declaration = None
        self.pins = None
        self.observed_code = {}

    def parent_state(self):
        if self.parent_cache is not None:
            return self.parent_cache
        c = self.compiler
        binder, semantic = c.libraries()
        store = binder['GitObjects'](self.root)
        require(store.kind(PARENT) == 'commit', 'immutable702 commit')
        fixture_raw = store.blob(PARENT, FIXTURE)
        manifest_raw = store.blob(PARENT, MANIFEST)
        receipt_raw = store.blob(PARENT, ACCEPTANCE)
        require(sha(fixture_raw) == FIXTURE_SHA and sha(manifest_raw) == MANIFEST_SHA
                and sha(receipt_raw) == ACCEPTANCE_SHA, 'exact7071 parent binding')
        prior, rows, receipt = json.loads(fixture_raw), json.loads(manifest_raw), json.loads(receipt_raw)
        require(prior['schema'] == 'triptych-test-source-batch/v1' and prior['acceptance'] == {
            'status': 'accepted', 'receipt_path': ACCEPTANCE, 'receipt_sha256': ACCEPTANCE_SHA}, 'actual parent acceptance')
        require(prior['source_input_manifest_sha256'] == receipt['source_input_manifest_sha256'] == MANIFEST_SHA,
                'actual parent manifest binding')
        require(receipt['status'] == 'accepted' and receipt['scope'] == 'missal-source-batch'
                and receipt['source_epoch_paths'] == len(rows) == 7071, 'actual accepted7071 parent')
        require(len({r['path'] for r in rows}) == 7071, 'distinct parent source rows')
        store.verify_rows(PARENT, rows)
        require(not (set(c.EXCLUDED_REGISTRIES) & {r['path'] for r in rows}), 'shared registry exclusions')
        require(sha(store.blob(PARENT, HELPER)) == HELPER_SHA, 'original strict helper')
        anchor_raw = store.blob(binder['ANCHOR'], FIXTURE)
        require(sha(anchor_raw) == binder['ANCHOR_FIXTURE_SHA'], 'exact historical anchor fixture')
        anchor = json.loads(anchor_raw)
        require(prior['baseline_revision'] == c.ORIGINAL == binder['ORIGINAL'] == anchor['baseline_revision'], 'historical revision')
        for field in c.HISTORICAL_FIELDS:
            require(c.canonical(prior[field]) == c.canonical(anchor[field]), 'historical field ' + field)
        require(set(prior['files']) == set(anchor['files']) and len(prior['files']) == 17, 'exact17 historical owners')
        originals = {}
        for name, inverse in prior['files'].items():
            raw = binder['reverse'](store.blob(PARENT, name), inverse)
            require(raw == store.blob(c.ORIGINAL, name) and sha(raw) == anchor['files'][name]['before_sha256'],
                    'actual original Git replay ' + name)
            originals[name] = raw
        proof = {'schema': 'triptych-bounded-source-guard-current-parent/v1', 'git_revision': PARENT,
                 'fixture_sha256': FIXTURE_SHA, 'manifest_sha256': MANIFEST_SHA,
                 'receipt_path': ACCEPTANCE, 'receipt_sha256': ACCEPTANCE_SHA,
                 'strict_helper_sha256': HELPER_SHA, 'source_epoch_paths': 7071,
                 'historical_fields': list(c.HISTORICAL_FIELDS),
                 'original17_before': {n: sha(raw) for n, raw in originals.items()}, 'support_sha256': SUPPORT_SHA}
        self.parent_cache = binder, semantic, store, prior, rows, originals, proof
        return self.parent_cache

    def configure(self, declaration_path, declaration_sha):
        raw = declaration_path.read_bytes()
        require(sha(raw) == declaration_sha, 'exact root-selected declaration')
        d = json.loads(raw)
        require(d['schema'] == 'triptych-settled-next-english-semantic-inputs/v1', 'declaration schema')
        require(d['parent_git_revision'] == PARENT and d['parent_fixture_sha256'] == FIXTURE_SHA
                and d['parent_manifest_sha256'] == MANIFEST_SHA and d['parent_acceptance_sha256'] == ACCEPTANCE_SHA,
                'declaration exact702 parent')
        require(d['adapter_sha256'] == sha(ADAPTER_RAW), 'exact review-selected adapter at startup')
        rows, rows_raw = pinned_json(self.root, d['source_input_rows'])
        require(rows_raw == self.compiler.serialized(rows), 'canonical final source-map bytes')
        pins = rows_to_map(rows)
        old = {r['path']: r['post_sha256'] for r in self.parent_state()[4]}
        require(set(old) <= set(pins), 'every7071 parent path retained')
        require(not ({FIXTURE, MANIFEST, FUTURE_ACCEPTANCE} & set(pins)), 'no fixture/receipt self cycles')
        require(not (set(self.compiler.EXCLUDED_REGISTRIES) & set(pins)), 'excluded registry scope')
        for name in set(pins) - set(old):
            self.compiler.extra_input(name)
        for name, expected in FINITE_INPUTS.items():
            require(pins.get(name) == expected, 'exact finite adoption context ' + name)
        delta, _ = pinned_json(self.root, d['source_delta'])
        require(delta['schema'] == 'triptych-bounded-source-input-delta/v1'
                and delta['parent_git_revision'] == PARENT and delta['parent_manifest_sha256'] == MANIFEST_SHA,
                'explicit delta parent')
        require(delta['extra_inputs'] == sorted(set(pins) - set(old)), 'exact added input set')
        changes = delta['files']
        require(isinstance(changes, list) and all(isinstance(r, dict) and set(r) == {
            'path', 'before_sha256', 'post_sha256'} for r in changes), 'exact delta row fields')
        wanted = sorted(p for p in pins if old.get(p) != pins[p])
        require([r['path'] for r in changes] == wanted, 'delta rows equal sorted final-map changes')
        store = self.parent_state()[2]
        parent_paths = store.tree(PARENT)
        for row in changes:
            name = row['path']
            before = sha(store.blob(PARENT, name)) if name in parent_paths else None
            require(row['before_sha256'] == before and row['post_sha256'] == pins[name], 'delta and source-map hashes agree ' + name)
        for name, status, flag in (('sources', 'SOURCESETTLED', 'source_writers_closed'),
                                    ('generators', 'GENSETTLED', 'generators_closed')):
            marker, _ = pinned_json(self.root, d['settlement'][name])
            require(marker['status'] == status and marker[flag] is True and marker['parent_git_revision'] == PARENT,
                    'explicit settled marker ' + name)
            if name == 'generators':
                require(marker['source_input_rows_sha256'] == d['source_input_rows']['sha256'], 'generator marker binds final source map')
            require(d['settlement'][name]['path'] not in pins, 'settlement marker self cycle')
        require(set(d['runtime_successors']) <= EXAMPLE_TOOLS | {FINITE}, 'only named runtime successors')
        require(d['runtime_successors'].get(FINITE) == FINITE_SUCCESSOR,
                'exact F34-ECCA-functional successor declaration')
        finite_refs = [FINITE_ACTIVATION, *FINITE_REVIEWS]
        for ref in finite_refs:
            pinned_json(self.root, ref)
        self.declaration, self.pins = d, pins
        self.declaration_raw, self.declaration_path = raw, declaration_path
        self.config_refs = [d['source_input_rows'], d['source_delta'], *d['settlement'].values(), *finite_refs]
        for name in {FINITE} | EXAMPLE_TOOLS:
            self.check_code(self.root / name)
        return d

    def scope_paths(self, root, prior_rows, extra_inputs):
        require(self.declaration is not None and self.pins is not None, 'settled declaration configured')
        require(root.resolve() == self.root, 'exact physical root')
        old = {r['path']: r['post_sha256'] for r in prior_rows}
        require(old == {r['path']: r['post_sha256'] for r in self.parent_state()[4]}, 'exact parent rows passed to scope selector')
        require(extra_inputs == sorted(set(self.pins) - set(old)), 'exact declared scope extras')
        return set(self.pins)

    def check_code(self, path):
        path = path if path.is_absolute() else self.root / path
        if not path.is_relative_to(self.root):
            return
        name = path.relative_to(self.root).as_posix()
        if name.startswith('.scratch/'):
            require(path.resolve().is_relative_to(Path(sys.prefix).resolve()) or path.resolve() == Path(__file__).resolve(),
                    'no scratch code dependency ' + name)
            return
        # Do not resolve away an internal symlink before rejecting it: that
        # would misclassify an escaped repository module as trusted external code.
        current = ordinary(self.root, name).read_bytes()
        digest = sha(current)
        store = self.parent_state()[2]
        require(name in store.tree(PARENT), 'no newly authored runtime module ' + name)
        before = store.blob(PARENT, name)
        successor = self.declaration['runtime_successors'].get(name)
        if successor is not None:
            require(successor['before_sha256'] == sha(before)
                    and successor['after_sha256'] == digest, 'explicit runtime code change ' + name)
        if name == FINITE:
            require(successor == FINITE_SUCCESSOR and sha(before) == FINITE_BEFORE
                    and digest == FINITE_AFTER, 'exact reviewed finite helper chain')
        elif successor is not None or current != before:
            require(successor is not None, 'explicit runtime code change ' + name)
            require(name in EXAMPLE_TOOLS and successor['kind'] == 'examples-only', 'only counter transcript successor ' + name)
            examples_only(before, current)
        self.observed_code[name] = digest

    def audit(self, event, args):
        if event == 'exec' and isinstance(args[0], types.CodeType):
            filename = args[0].co_filename
            if filename and not filename.startswith('<'):
                self.check_code(Path(filename))

    def recheck(self):
        require(Path(__file__).read_bytes() == ADAPTER_RAW, 'adapter bytes drift after startup')
        require(self.declaration_path.read_bytes() == self.declaration_raw, 'declaration drift')
        for ref in self.config_refs:
            require(sha(ordinary(self.root, ref['path']).read_bytes()) == ref['sha256'], 'declaration reference drift ' + ref['path'])
        for name, want in self.observed_code.items():
            require(sha(ordinary(self.root, name).read_bytes()) == want, 'consumed runtime code drift ' + name)
        for name, expected in ((COMPILER, COMPILER_SHA), (SUPPORT, SUPPORT_SHA), (HELPER, HELPER_SHA)):
            require(sha(ordinary(self.root, name).read_bytes()) == expected, 'immutable code drift ' + name)


def main():
    global ROOT, OWN
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['verify-parent', 'derive'])
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--declaration', type=Path)
    parser.add_argument('--declaration-sha256')
    args = parser.parse_args()
    ROOT = args.root.resolve()
    OWN = ROOT / '.scratch/next-epoch-semantics-20261030'
    out = args.out.resolve()
    require(out.is_relative_to(OWN.resolve()) and not out.exists(), 'fresh exclusive scratch output')
    compiler = load_compiler(ROOT)
    adapter = Adapter(compiler, ROOT)
    if args.command == 'verify-parent':
        proof = adapter.parent_state()[-1]
        out.mkdir(parents=True)
        (out / 'parent-proof.json').write_bytes(encoded(proof))
        print(json.dumps({'status': 'exact702-parent-verified', 'paths': 7071, 'original_streams': 17,
                          'source_candidate_derived': False, 'proof_sha256': sha(encoded(proof))}))
        return
    require(args.declaration is not None and args.declaration_sha256 is not None, 'derive requires exact settled declaration')
    declaration = adapter.configure(args.declaration.resolve(), args.declaration_sha256)
    require(not (ROOT / FUTURE_ACCEPTANCE).exists(), 'unused root-selected acceptance identity')
    compiler.PARENT = PARENT
    compiler.parent_state = adapter.parent_state
    compiler.scope_paths = adapter.scope_paths
    original_derive_code = compiler.derive.__code__
    sys.addaudithook(adapter.audit)
    compiler.derive(ROOT, out, FUTURE_ACCEPTANCE, ROOT / declaration['source_delta']['path'],
                    declaration['source_delta']['sha256'], COMPILER_SHA)
    require(compiler.derive.__code__ is original_derive_code, 'semantic derive unchanged')
    adapter.recheck()
    manifest = out / 'postimages' / MANIFEST
    require(rows_to_map(json.loads(manifest.read_bytes())) == adapter.pins, 'derived manifest equals explicit settled union')
    proof = {'schema': 'triptych-reviewed-current-parent-semantic-adapter-proof/v1',
             'status': 'pending-independent-candidate-review', 'new_publication_permission': False,
             'canonical_writes': 0, 'adapter_sha256': sha(ADAPTER_RAW),
             'immutable_compiler_sha256': COMPILER_SHA, 'immutable_support_sha256': SUPPORT_SHA,
             'strict_helper_sha256': HELPER_SHA, 'parent': adapter.parent_state()[-1],
             'replaced_in_memory_functions': ['parent_state', 'scope_paths'],
             'source_input_count': len(adapter.pins), 'declaration_sha256': args.declaration_sha256,
             'runtime_code_sha256': adapter.observed_code,
             'finite_helper_successor': FINITE_SUCCESSOR,
             'compatibility_note': 'Legacy V4-named proof keys emitted by immutable derive describe this exact accepted7071 parent, not a new claim about the old5615 state.',
             'acceptance': 'Only root may accept/install this pending candidate after independent exact review.'}
    (out / 'adapter-proof.json').write_bytes(encoded(proof))
    print(json.dumps({'adapter_status': proof['status'], 'source_inputs': len(adapter.pins),
                      'adapter_proof_sha256': sha(encoded(proof))}))


if __name__ == '__main__':
    main()
