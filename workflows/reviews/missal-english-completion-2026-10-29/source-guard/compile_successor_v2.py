#!/usr/bin/env python3
"""Prepare a pending bounded source-batch successor; never accept or install it."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tomllib

import yaml

sys.dont_write_bytecode = True
os.environ['TRIPTYCH_SOURCE_LIBRARY_CACHE'] = '0'
os.environ['TRIPTYCH_LIBRARY_CACHE'] = '0'

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
COMPILER_RAW = Path(__file__).read_bytes()
PARENT = '6aeb96a392a61e216310c3bf71834863afb229f8'
FIXTURE = 'tools/tests/fixtures/missal-source-batch-20261023.json'
MANIFEST = 'tools/tests/fixtures/missal-source-batch-20261023-inputs.json'
HELPER = 'tools/tests/_source_batch_guards.py'
HELPER_SHA = 'f60498c9c9f28f72d69d729b1d086044fa3877803327bb4e16d779c479ad55b1'
ORIGINAL = '2e030b564f4413b735ddbea3061082ebe981b11a'
SUPPORT_SHA = '3622fc1bcbf6e21e09e65be3cff50786930564de6be8640edd72b5be279d95ae'
EXCLUDED_REGISTRIES = {
    'src/sources/inventories/claude-publications-v1.toml',
    'src/sources/inventories/source-containment-v1.toml',
    'src/sources/inventories/source-family-migration-v1.toml',
}
REVIEW_PREFIX = 'workflows/reviews/missal-english-completion-2026-10-29/'
PALM_CORRECTION = REVIEW_PREFIX + 'roman-1962/sources/palm-distribution-hyphen-correction.json'
PALM_CORRECTION_SHA = '5e59471a53dba5425468ee10d0d943be1eccaa2dedd936854c63a8485fff56d2'
PALM_TARGET = ['palm-sunday', 'main', 'First Antiphon at the Distribution of Palms', 'all', 1]
HISTORICAL_FIELDS = (
    'schema', 'baseline_revision', 'baseline_roman_document_sha256',
    'latin_baseline_rows', 'latin_baseline_bodies', 'latin_baseline_present_keys',
    'latin_baseline_supplemented_keys', 'projection_baseline_source_files',
    'english_219_keys', 'english_baseline_source_files',
    'english_historical_source_files', 'english_historical_absence_scope',
)


def digest(raw):
    return hashlib.sha256(raw.encode() if isinstance(raw, str) else raw).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def serialized(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()


def require(condition, label):
    if not condition:
        raise AssertionError('bounded successor: ' + label)


def relative(value):
    path = Path(value)
    require(isinstance(value, str) and bool(value) and not path.is_absolute()
            and '..' not in path.parts and str(path) == value, 'canonical relative path')
    return value


def libraries():
    path = HERE / 'support.py'
    require(digest(path.read_bytes()) == SUPPORT_SHA, 'exact tracked support definitions')
    module = runpy.run_path(str(path))
    return module, module


def parent_state():
    binder, compiler = libraries()
    store = binder['GitObjects'](REPO)
    fixture_raw = store.blob(PARENT, FIXTURE)
    manifest_raw = store.blob(PARENT, MANIFEST)
    prior = json.loads(fixture_raw)
    require(prior['schema'] == 'triptych-test-source-batch/v1', 'parent schema')
    require(prior['acceptance']['status'] == 'accepted', 'accepted parent')
    receipt_path = relative(prior['acceptance']['receipt_path'])
    receipt_raw = store.blob(PARENT, receipt_path)
    receipt = json.loads(receipt_raw)
    require(digest(receipt_raw) == prior['acceptance']['receipt_sha256'], 'parent exact receipt')
    require(receipt['status'] == 'accepted' and receipt['scope'] == 'missal-source-batch', 'parent receipt scope')
    require(receipt['successor_kind'] == 'reader-scope-narrowing', 'parent is the V4 bounded epoch')
    require(digest(manifest_raw) == prior['source_input_manifest_sha256']
            == receipt['source_input_manifest_sha256'], 'parent exact manifest')
    rows = json.loads(manifest_raw)
    require(len(rows) == len({r['path'] for r in rows}) == receipt['source_epoch_paths'] == 5615,
            'exact V4 bounded parent domain')
    require(not (set(EXCLUDED_REGISTRIES) & {r['path'] for r in rows}), 'shared registry exclusions preserved')
    store.verify_rows(PARENT, rows)
    require(digest(store.blob(PARENT, HELPER)) == HELPER_SHA, 'strict immutable parent helper')
    anchor = json.loads(store.blob(binder['ANCHOR'], FIXTURE))
    require(prior['baseline_revision'] == ORIGINAL == anchor['baseline_revision'], 'original historical identity')
    for field in HISTORICAL_FIELDS:
        require(canonical(prior[field]) == canonical(anchor[field]), 'original historical field ' + field)
    require(set(prior['files']) == set(anchor['files']) and len(prior['files']) == 17, 'original17 replay paths')
    originals = {}
    for path, spec in prior['files'].items():
        originals[path] = binder['reverse'](store.blob(PARENT, path), spec)
        require(originals[path] == store.blob(ORIGINAL, path), 'raw original17 Git bytes ' + path)
        require(digest(originals[path]) == anchor['files'][path]['before_sha256'], 'original before hash ' + path)
    return binder, compiler, store, prior, rows, originals, {
        'schema': 'triptych-bounded-source-guard-parent/v1',
        'git_revision': PARENT,
        'publication_state': 'immutable-local-commit-no-remote-claim',
        'fixture_sha256': digest(fixture_raw),
        'manifest_sha256': digest(manifest_raw),
        'receipt_path': receipt_path,
        'receipt_sha256': digest(receipt_raw),
        'strict_helper_sha256': HELPER_SHA,
        'source_epoch_paths': len(rows),
        'historical_fields': list(HISTORICAL_FIELDS),
        'original17_before': {path: digest(raw) for path, raw in originals.items()},
        'support_sha256': SUPPORT_SHA,
    }


def capture(out):
    binder, compiler, store, prior, rows, originals, proof = parent_state()
    require(not out.exists(), 'capture output already exists')
    out.mkdir(parents=True)
    for path in (FIXTURE, MANIFEST, prior['acceptance']['receipt_path'], HELPER):
        target = out / 'parent' / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(store.blob(PARENT, path))
    for path, raw in originals.items():
        target = out / 'originals' / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    (out / 'parent-binding.json').write_bytes(serialized(proof))
    print(json.dumps({'status': 'captured', 'parent_paths': len(rows), 'historical_replays': len(originals),
                      'parent_binding_sha256': digest(serialized(proof))}, sort_keys=True))


def scope_paths(root, prior_rows, extra_inputs):
    paths = {relative(row['path']) for row in prior_rows}
    # Add changed/new source records only. Never rebuild a whole-repository freeze.
    changed = subprocess.check_output(['git', 'diff', '--name-only', '-z', PARENT, '--', 'src/sources'], cwd=root)
    untracked = subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard', '-z', '--', 'src/sources'], cwd=root)
    additions = {value.decode() for raw in (changed, untracked) for value in raw.split(b'\0') if value}
    paths |= additions - EXCLUDED_REGISTRIES
    for path in extra_inputs:
        extra_input(path)
        paths.add(path)
    require(not (paths & EXCLUDED_REGISTRIES), 'shared registry scope cannot be silently widened')
    require(FIXTURE not in paths and MANIFEST not in paths, 'fixture/manifest self cycles excluded')
    return paths


def extra_input(path):
    relative(path)
    source = path.startswith('src/sources/') and path not in EXCLUDED_REGISTRIES
    authority = path.startswith(REVIEW_PREFIX) and path.endswith('.json') and not path.startswith(REVIEW_PREFIX + 'source-guard/')
    require(source or authority, 'explicit extra input must be a reader source or this task\'s JSON review authority')


def input_delta(root, old_rows, store, extra_inputs):
    paths = scope_paths(root, old_rows, extra_inputs)
    pins = read_epoch(root, paths)
    old_pins = {row['path']: row['post_sha256'] for row in old_rows}
    changes = []
    parent_paths = store.tree(PARENT)
    for path in sorted(paths):
        if pins[path] != old_pins.get(path):
            changes.append({'path': path,
                            'before_sha256': digest(store.blob(PARENT, path)) if path in parent_paths else None,
                            'post_sha256': pins[path]})
    return paths, pins, changes


def inspect_inputs(root, out, extra_inputs):
    _, _, store, _, rows, _, parent_proof = parent_state()
    require(not out.exists(), 'inspection output already exists')
    for path in extra_inputs:
        extra_input(path)
    _, _, changes = input_delta(root, rows, store, extra_inputs)
    output = {'schema': 'triptych-bounded-source-input-delta/v1', 'parent_git_revision': PARENT,
              'parent_manifest_sha256': parent_proof['manifest_sha256'],
              'extra_inputs': sorted(extra_inputs), 'files': changes,
              'source_acceptance_claimed': False}
    out.mkdir(parents=True)
    raw = serialized(output)
    (out / 'source-input-delta.json').write_bytes(raw)
    print(json.dumps({'status': 'candidate-input-delta', 'files': len(changes), 'sha256': digest(raw)}))


def declared_inputs(root, old_rows, store, path, expected_sha256, parent_proof):
    raw = path.read_bytes()
    require(digest(raw) == expected_sha256, 'exact explicitly supplied input delta')
    data = json.loads(raw)
    require(data['schema'] == 'triptych-bounded-source-input-delta/v1', 'input delta schema')
    require(data['parent_git_revision'] == PARENT and data['parent_manifest_sha256'] == parent_proof['manifest_sha256'], 'input delta parent identity')
    extra = data['extra_inputs']
    require(isinstance(extra, list) and len(extra) == len(set(extra)), 'distinct explicit extra source inputs')
    for item in extra:
        extra_input(item)
    rows = data['files']
    require(isinstance(rows, list) and len(rows) == len({row['path'] for row in rows}), 'distinct declared input deltas')
    paths, pins, observed = input_delta(root, old_rows, store, extra)
    require(canonical(rows) == canonical(observed), 'complete observed file delta must equal the exact supplied path/before/after allowlist')
    return paths, pins, observed, extra, raw


def read_epoch(root, paths):
    result = {}
    for path in sorted(paths):
        target = root / relative(path)
        require(target.is_file() and not target.is_symlink(), 'ordinary source input missing or symlinked ' + path)
        require(target.resolve().is_relative_to(root.resolve())
                and not any(parent.is_symlink() for parent in target.parents if parent != root and parent.is_relative_to(root)),
                'source input has an escaped or symlinked ancestor ' + path)
        result[path] = digest(target.read_bytes())
    require(result[HELPER] == HELPER_SHA, 'strict helper must remain byte-exact')
    return result


def row_transitions(before, after, label):
    removed = sorted(set(before) - set(after))
    added = sorted(set(after) - set(before))
    changed = sorted(key for key in set(before) & set(after) if canonical(before[key]) != canonical(after[key]))
    return {'label': label, 'removed': {key: before[key] for key in removed},
            'added': {key: after[key] for key in added},
            'changed': {key: {'before': before[key], 'after': after[key]} for key in changed}}


def check_english_complements(old_positive, old_absent, positive, absent):
    require(not (set(positive) & set(absent)), 'current English partitions overlap')
    require(all(key in positive and canonical(value) == canonical(positive[key]) for key, value in old_positive.items()),
            'all prior positive English dictionaries preserved')
    require(all(key in positive or (key in absent and canonical(value) == canonical(absent[key])) for key, value in old_absent.items()),
            'prior English refusal cannot change unless consumed by an English admission')
    require((set(old_positive) | set(old_absent)) <= (set(positive) | set(absent)), 'prior English owner domain removed')
    for key in set(positive) - set(old_positive):
        require(any(isinstance(row, dict) and row.get('lang') == 'en'
                    and isinstance(row.get('text'), str) and row['text'].strip()
                    for row in positive[key].get('translations', []) or []),
                'new English positive has no literal nonempty English body')


def positive_complement(root, pins, calendar, before, current):
    """Recognize one exact recorded correction; all other positives stay literal."""
    changed = {key for key, value in before.items() if current.get(key) != value}
    if not changed:
        return before, []
    identity = canonical(PALM_TARGET)
    require(calendar == 'roman-1962' and changed == {identity}, 'unrecorded prior English positive correction')
    require(pins.get(PALM_CORRECTION) == PALM_CORRECTION_SHA, 'exact Palm correction must be a declared input')
    correction_raw = (root / PALM_CORRECTION).read_bytes()
    require(digest(correction_raw) == PALM_CORRECTION_SHA, 'entire exact Palm correction receipt bytes')
    correction = json.loads(correction_raw)
    require(correction['schema'] == 'triptych-historical-translation-correction/v1'
            and correction['target'] == PALM_TARGET, 'exact Palm correction identity')
    review_path = relative(correction['source_review'])
    extra_input(review_path)
    require(pins.get(review_path) == correction['source_review_sha256'], 'exact linked Palm source review must be a declared input')
    require(before[identity] == correction['old_entry'] and current.get(identity) == correction['new_entry'],
            'entire recorded Palm before and after dictionaries')
    expected = dict(before)
    expected[identity] = correction['new_entry']
    return expected, [{'calendar': calendar, 'identity': identity, 'correction_path': PALM_CORRECTION,
                       'correction_sha256': PALM_CORRECTION_SHA, 'source_review_path': review_path,
                       'source_review_sha256': correction['source_review_sha256']}]


def derive(root, out, receipt_path, delta_path, delta_sha256, compiler_sha256):
    binder, compiler, store, prior, old_rows, originals, parent_proof = parent_state()
    require(digest(COMPILER_RAW) == compiler_sha256, 'exact review-selected compiler bytes at startup')
    require(not out.exists(), 'candidate output already exists')
    relative(receipt_path)
    receipt_target = root / receipt_path
    require(receipt_path.startswith('workflows/reviews/') and receipt_target.resolve().is_relative_to(root)
            and not receipt_target.is_symlink(), 'ordinary repository review receipt identity required')
    paths, pins, source_delta, extra_inputs, delta_raw = declared_inputs(root, old_rows, store, delta_path, delta_sha256, parent_proof)
    require(receipt_path not in paths, 'new receipt self cycle excluded')
    old_pins = {row['path']: row['post_sha256'] for row in old_rows}
    require(set(old_pins) <= set(pins), 'no V4 kept source pin dropped')
    read = lambda path: (root / path).read_bytes()
    sys.path[:0] = [str(root), str(root / 'scripts')]
    from _proper_latin import LatinKey, body_owners, read_sidecar, publication_records
    from _calendars import load_document
    owner = runpy.run_path(str(root / 'tools/mass-propers'))
    fixture = copy.deepcopy(prior)
    fixture['files'] = {path: binder['replay_spec'](raw, read(path)) for path, raw in originals.items()}
    require(all(pins[path] == spec['after_sha256'] for path, spec in fixture['files'].items()), 'all17 current replay inputs pinned')
    docs, parsed, old_parsed, bodies, english, absences, auxiliary, transitions = {}, {}, {}, {}, {}, {}, {}, {}
    positive_corrections = []
    for calendar in ('roman-1962', 'postconciliar'):
        docs[calendar] = load_document(root / 'src/sources/calendars', calendar)
        sidecar = f'src/sources/inventories/{calendar}-proper-latin-provenance-v1.toml'
        rows, errors = read_sidecar(root / sidecar)
        require(not errors, 'current Latin sidecar errors: ' + str(errors))
        parsed[calendar] = {canonical(key.as_dict()): row for key, row in rows.items()}
        bodies[calendar] = {canonical(key.as_dict()): {'state': state, 'body_sha256': digest(text) if text is not None else None}
                            for key, text, state in body_owners(docs[calendar])}
        require(set(parsed[calendar]) == set(bodies[calendar]), 'all current Latin body/proof owners ' + calendar)
        old = compiler['ledger'](store.blob(PARENT, sidecar), LatinKey)
        old_parsed[calendar] = old
        require(compiler['hashrows'](old) == prior['latin_current_rows'][calendar], 'exact immutable parent Latin maps')
        transitions[calendar + '_latin'] = row_transitions(old, parsed[calendar], 'complete Latin proof dictionaries')
        require(not transitions[calendar + '_latin']['removed'], 'prior Latin owner removed')
        old_document = yaml.load(store.blob(PARENT, f'src/sources/calendars/{calendar}/propers.yaml'), Loader=yaml.CSafeLoader)
        old_bodies = {canonical(key.as_dict()): {'state': state, 'body_sha256': digest(text) if text is not None else None}
                      for key, text, state in body_owners(old_document)}
        transitions[calendar + '_latin_bodies'] = row_transitions(old_bodies, bodies[calendar], 'complete Latin body states and hashes')
        ledger_path = f'src/sources/inventories/{calendar}-proper-translations-v1.toml'
        positive, absent, aux = compiler['english_ledger'](read(ledger_path), docs[calendar], owner)
        old_positive, old_absent, old_aux = compiler['english_ledger'](
            store.blob(PARENT, ledger_path), yaml.load(store.blob(PARENT, f'src/sources/calendars/{calendar}/propers.yaml'), Loader=yaml.CSafeLoader), owner)
        for partition, old_map, new_map in (('positive', old_positive, positive), ('absence', old_absent, absent)):
            prior_field = ('roman' if calendar == 'roman-1962' else 'postconciliar') + '_current_english_' + partition
            require(compiler['hashrows'](old_map) == prior[prior_field], 'exact immutable parent English map ' + prior_field)
            transitions[calendar + '_english_' + partition] = row_transitions(old_map, new_map, 'complete English dictionaries')
        protected, corrections = positive_complement(root, pins, calendar, old_positive, positive)
        positive_corrections.extend(corrections)
        check_english_complements(protected, old_absent, positive, absent)
        transitions[calendar + '_english_auxiliary'] = row_transitions(old_aux, aux, 'full auxiliary dictionaries')
        english[calendar], absences[calendar], auxiliary[calendar] = positive, absent, aux
    pre_records, errors = publication_records(root / 'src/sources/calendars', 'roman-pre-1955')
    require(not errors, 'pre55 current proof errors: ' + str(errors))
    parsed['roman-pre-1955'] = {canonical(key.as_dict()): row for key, row in pre_records.items()}
    pre_sidecar = 'src/sources/inventories/roman-pre-1955-proper-latin-provenance-v1.toml'
    direct = compiler['ledger'](store.blob(PARENT, pre_sidecar), LatinKey)
    inherited = {key: {**row, 'publication_status': 'unresolved', 'publication_basis': 'unresolved', 'surfaces': [],
                       'note': 'Provenance inherited from roman-1962; target-recension attestation for roman-pre-1955 is not established.'}
                 for key, row in old_parsed['roman-1962'].items()}
    inherited.update(direct)
    targets_path = 'src/sources/inventories/roman-pre-1955-proper-target-overrides-v1.toml'
    targets = tomllib.loads(store.blob(PARENT, targets_path).decode())
    for entry in targets['entries']:
        row = {**entry['provenance'], '_target_context': targets['target_context']}
        inherited[canonical(LatinKey.from_mapping(row).as_dict())] = row
    require(compiler['hashrows'](inherited) == prior['latin_current_rows']['roman-pre-1955'], 'exact immutable pre55 effective proof map')
    transitions['roman-pre-1955_latin_effective'] = row_transitions(inherited, parsed['roman-pre-1955'], 'complete effective pre55 proof dictionaries')
    for path in ('src/sources/inventories/roman-pre-1955-proper-translations-v1.toml',
                 'src/sources/inventories/roman-1962-ordo-missae-v1.toml',
                 'src/sources/inventories/roman-pre-1955-ordo-missae-v1.toml',
                 'src/sources/inventories/postconciliar-ordo-missae-v1.toml'):
        require(path in pins, 'semantic inventory source must be in bounded epoch ' + path)
        before = tomllib.loads(store.blob(PARENT, path).decode())
        after = tomllib.loads(read(path).decode())
        transitions[path] = row_transitions(before, after, 'complete inventory top-level dictionaries including entries and exclusions')
    fixture['current_roman_document_sha256'] = digest(canonical(docs['roman-1962']))
    fixture['latin_current_rows'] = {calendar: compiler['hashrows'](rows) for calendar, rows in parsed.items()}
    fixture['latin_current_bodies'] = bodies['roman-1962']
    baseline = prior['latin_baseline_rows']['roman-1962']
    current = fixture['latin_current_rows']['roman-1962']
    require(set(baseline) <= set(current), 'historical Latin proof owner removed')
    fixture['new_latin_keys'] = sorted(set(current) - set(baseline))
    fixture['corrected_latin_keys'] = sorted(key for key in baseline if baseline[key] != current[key])
    fixture['latin_permitted_keys'] = sorted(key for key, row in parsed['roman-1962'].items() if row['publication_status'] == 'permitted')
    fixture['latin_current_supplements'] = {key: row['publication_source_ids'][2:] for key, row in parsed['roman-1962'].items()
                                            if row['publication_status'] == 'permitted' and len(row.get('publication_source_ids', [])) > 2}
    parent_latin = prior['latin_current_rows']['roman-1962']
    new_parent_keys = sorted(set(current) - set(parent_latin))
    changed_parent_keys = sorted(key for key in parent_latin if parent_latin[key] != current[key])
    editions, artifacts, cross, _ = compiler['projection_oracles'](
        root, prior, parsed['roman-1962'], new_parent_keys, changed_parent_keys)
    fixture['new_projection_specs'] = editions
    fixture['new_projection_artifact_specs'] = artifacts
    fixture['cross_supplement_specs'] = cross
    for calendar in ('roman-1962', 'postconciliar'):
        prefix = 'roman' if calendar == 'roman-1962' else calendar
        fixture[prefix + '_current_english_positive'] = compiler['hashrows'](english[calendar])
        fixture[prefix + '_current_english_absence'] = compiler['hashrows'](absences[calendar])
    fixture['roman_current_english_owner_universe'] = sorted(set(english['roman-1962']) | set(absences['roman-1962']))
    fixture['roman_current_execution_source_hashes'] = [digest(canonical(row)) for row in auxiliary['roman-1962'].get('execution_sources', [])]
    fixture['english_coverage'] = {}
    for calendar, fields in prior['english_coverage'].items():
        report = owner['english_coverage'](root / 'src/sources/calendars', calendar)
        require(report is not None, 'owning English coverage unavailable ' + calendar)
        require(all(report[field] == 0 for field in ('unaccounted', 'unmatched_records', 'stale_translation_records', 'outside_the_ledger')),
                'owning English coverage has unaccounted/mismatched/stale/outside rows ' + calendar)
        fixture['english_coverage'][calendar] = {field: report[field] for field in fields}
    for field, prefixes in (
            ('projection_baseline_source_files', ('src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/',)),
            ('english_baseline_source_files', tuple('src/sources/works/' + name + '/' for name in
                                                    ('francis-xavier-lasance', 'eugene-cummiskey', 'edward-caswall')))):
        expected = dict(prior[field])
        expected.update({path: sha256 for path, sha256 in pins.items() if path.startswith(prefixes)})
        actual = {str(path.relative_to(root)): digest(path.read_bytes())
                  for prefix in prefixes for path in (root / prefix).rglob('*') if path.is_file()}
        require(actual == expected, 'entire current source namespace must equal historical complement plus final manifest: ' + field)
    manifest_raw = serialized([{'path': path, 'post_sha256': pins[path]} for path in sorted(pins)])
    fixture['source_input_manifest_path'] = MANIFEST
    fixture['source_input_manifest_sha256'] = digest(manifest_raw)
    fixture['acceptance'] = {'status': 'pending', 'receipt_path': receipt_path, 'receipt_sha256': None}
    fixture['state'] = 'Bounded source successor candidate; independent source and fixture acceptance pending'
    contract = {'schema': 'triptych-bounded-source-successor-delta/v1', 'parent': parent_proof,
                'files': source_delta, 'explicit_input_delta_sha256': delta_sha256, 'semantic_transitions': transitions,
                'exact_recorded_positive_corrections': positive_corrections,
                'english_coverage': fixture['english_coverage'], 'source_permissions_claimed': False}
    fixture['reviewed_transition_contract_sha256'] = digest(serialized(contract))
    for field in HISTORICAL_FIELDS:
        require(canonical(fixture[field]) == canonical(prior[field]), 'all original historical fields exact ' + field)
    require(read_epoch(root, paths) == pins and scope_paths(root, old_rows, extra_inputs) == paths, 'source epoch drift during derivation')
    require(delta_path.read_bytes() == delta_raw, 'explicit source delta drift during derivation')
    require(Path(__file__).read_bytes() == COMPILER_RAW, 'compiler bytes drift during derivation')
    libraries()
    proof = {'schema': 'triptych-bounded-source-successor-proof/v1', 'status': 'pending-independent-review',
             'source_acceptance_claimed': False, 'canonical_writes': 0,
             'parent_git_revision': PARENT, 'parent_fixture_sha256': parent_proof['fixture_sha256'],
             'parent_manifest_sha256': parent_proof['manifest_sha256'],
             'strict_helper_sha256': HELPER_SHA, 'historical_fields_preserved': list(HISTORICAL_FIELDS),
             'original17_before': parent_proof['original17_before'],
             'source_epoch_paths': len(pins), 'preserved_V4_paths': len(old_pins), 'dropped_V4_paths': 0,
             'added_input_paths': sorted(set(pins) - set(old_pins)),
             'changed_input_paths': [row['path'] for row in source_delta if row['path'] in old_pins],
             'source_input_manifest_sha256': digest(manifest_raw), 'pending_fixture_sha256': digest(serialized(fixture)),
             'transition_contract_sha256': digest(serialized(contract)),
             'compiler_sha256': digest(COMPILER_RAW), 'support_sha256': SUPPORT_SHA,
             'explicit_input_delta_sha256': delta_sha256,
             'exact_recorded_positive_corrections': positive_corrections,
             'english_coverage': fixture['english_coverage'],
             'new_V4_projection_oracle_keys': new_parent_keys + changed_parent_keys}
    out.mkdir(parents=True)
    for path, raw in ((FIXTURE, serialized(fixture)), (MANIFEST, manifest_raw)):
        target = out / 'postimages' / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    (out / 'transition-contract.json').write_bytes(serialized(contract))
    (out / 'data-proof.json').write_bytes(serialized(proof))
    print(json.dumps({'status': proof['status'], 'source_epoch_paths': len(pins), 'source_delta_files': len(source_delta),
                      'dropped_V4_paths': 0, 'english_coverage': proof['english_coverage'],
                      'pending_fixture_sha256': proof['pending_fixture_sha256']}, sort_keys=True))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('capture', 'inspect', 'derive'))
    parser.add_argument('--root', type=Path, default=REPO)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--receipt-path')
    parser.add_argument('--extra-input', action='append', default=[])
    parser.add_argument('--source-delta', type=Path)
    parser.add_argument('--source-delta-sha256')
    parser.add_argument('--compiler-sha256')
    args = parser.parse_args()
    root, out = args.root.resolve(), args.out.resolve()
    require(out.is_relative_to(REPO / '.scratch') and not out.is_symlink(), 'output must belong to repository scratch')
    if args.command == 'capture':
        capture(out)
    elif args.command == 'inspect':
        inspect_inputs(root, out, args.extra_input)
    else:
        require(args.receipt_path is not None, 'derive requires a new receipt path')
        require(not args.extra_input, 'derive extras belong in the explicitly supplied input delta')
        require(args.source_delta is not None and args.source_delta_sha256 is not None and args.compiler_sha256 is not None,
                'derive requires exact source-delta and compiler hashes')
        derive(root, out, args.receipt_path, args.source_delta.resolve(), args.source_delta_sha256, args.compiler_sha256)


if __name__ == '__main__':
    main()
