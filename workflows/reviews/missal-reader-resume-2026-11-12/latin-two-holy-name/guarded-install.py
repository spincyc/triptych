#!/usr/bin/env python3
"""Prepare exact-node corrections; apply only an explicitly approved fresh plan.

No generic source_epoch authority is introduced. Root must separately admit the
two original declarations, rebind the supplemental ending descriptor, and run
the source/producer/consumer gates. --checkpoint-released is the operator's
assertion of release, not a generated or inferred approval receipt.
"""
from pathlib import Path
import argparse
import copy
import difflib
import hashlib
import json
import os
import re
import tomllib
import yaml

EVIDENCE = Path('workflows/reviews/missal-reader-resume-2026-11-12/latin-two-holy-name')
PROPER = 'src/sources/calendars/roman-1962/propers.yaml'
LATIN = 'src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml'
ENGLISH = 'src/sources/inventories/roman-1962-proper-translations-v1.toml'
KEYS = ('mass', 'form', 'proper', 'course', 'cycle', 'occurrence')


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def sha(obj):
    return hashlib.sha256(obj if isinstance(obj, bytes) else canonical(obj)).hexdigest()


def require(test, message):
    if not test:
        raise ValueError(message)


def json_bytes(obj):
    return (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode()


def read_json(path):
    return json.loads(path.read_bytes())


def value(obj):
    if isinstance(obj, bool):
        return str(obj).lower()
    if isinstance(obj, int):
        return str(obj)
    if isinstance(obj, list):
        return '[' + ', '.join(value(x) for x in obj) + ']'
    require(isinstance(obj, str), 'Unsupported approved TOML value')
    return json.dumps(obj, ensure_ascii=False)


def latin_key(row):
    return [str(row.get(k) or '') for k in KEYS[:-1]] + [int(row.get('occurrence') or 0)]


def english_key(row):
    return [row.get('mass'), row.get('form_id'), row.get('proper'), row.get('cycle'), row.get('occurrence')]


def proper_node(document, target):
    mass, form, proper, cycle, occurrence = target
    require(form == 'main' and cycle == 'all' and occurrence == 1, 'Unsupported target shape')
    found = [p for s in document['sections'].values() if isinstance(s, dict)
             for m in s.get('masses', []) if m.get('key') == mass
             for p in m.get('propers', []) if p.get('name') == proper and p.get('text')]
    require(len(found) == 1, f'Proper identity not unique: {target}')
    return found[0]


def row_block(text, before, key_function, key):
    # Top-level boundaries only: nested [[entries.translations]] stays in its row.
    starts = list(re.finditer(r'(?m)^\[\[?[^].\n]+\]\]?\s*\n', text))
    found = []
    for i, match in enumerate(starts):
        if match.group().strip() != '[[entries]]':
            continue
        end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        block = text[match.start():end]
        obj = tomllib.loads(block)['entries'][0]
        if key_function(obj) == key:
            found.append((block, obj))
    require(len(found) == 1, f'Ledger identity not unique: {key}')
    block, obj = found[0]
    require(obj == before, f'Exact ledger dictionary preimage changed: {key}')
    return block


def one_replace(text, before, after, label):
    require(text.count(before) == 1, f'Literal preimage not unique: {label}')
    return text.replace(before, after, 1)


def row_pair(before, after):
    return {'before': before, 'after': after, 'before_sha256': sha(before), 'after_sha256': sha(after)}


def prepare(root, package):
    manifest_path = package / EVIDENCE / 'package-manifest.json'
    manifest = read_json(manifest_path)
    for item in manifest['files']:
        require(sha((package / item['path']).read_bytes()) == item['sha256'], 'Package pin changed: ' + item['path'])
    la = read_json(package / EVIDENCE / 'latin-correction-declarations.json')
    en = read_json(package / EVIDENCE / 'holy-name-locator-declaration.json')
    metadata = read_json(package / EVIDENCE / 'source-metadata-successor.json')
    require(len(metadata['changes']) == 3, 'Not exact three-field metadata successor')
    overrides = {}
    for change in metadata['changes']:
        p = change['path']; old = change['before_document']; new = change['after_document']
        require(p not in overrides, 'Duplicate metadata override')
        expected = copy.deepcopy(old)
        if change['kind'] == 'remove-optional-page-range':
            require('/vatican-typica-1962/passages/latin-cleanliness-' in p, 'Metadata removal outside admitted target passages')
            require('artifact_page_ranges' in expected, 'Missing declared old range')
            del expected['artifact_page_ranges']
        elif change['kind'] == 'restore-work-locus-grammar':
            require(p == en['changed_files'][1]['path'], 'Locus correction outside Holy Name verification')
            expected['locus'] = 'most-holy-name-of-jesus/collect'
        else:
            raise ValueError('Unknown metadata successor kind')
        require(expected == new and tomllib.loads((package / p).read_text()) == new, 'Undeclared source metadata changed')
        require(sha((package / p).read_bytes()) == change['after_sha256'], 'Source metadata successor bytes changed')
        overrides[p] = change
    require(sum(x['kind'] == 'remove-optional-page-range' for x in metadata['changes']) == 2, 'Not exact two target range removals')
    def candidate_digest(p, original_digest):
        if p not in overrides:
            return original_digest
        require(overrides[p]['before_sha256'] == original_digest, 'Metadata successor is not based on original declaration')
        return overrides[p]['after_sha256']
    require(la['correction_count'] == 2 and len(la['corrections']) == 2, 'Not exact Latin2 declaration')
    require(en['fields_changed'] == ['ia_leaf', 'ia_leaf_range', 'witness_note'], 'Not exact Holy Name declaration')
    before = {p: (root / p).read_bytes() for p in (PROPER, LATIN, ENGLISH)}
    after = dict(before)
    old_doc = yaml.safe_load(before[PROPER])
    expected_doc = copy.deepcopy(old_doc)
    old_latin = tomllib.loads(before[LATIN].decode())
    expected_latin = copy.deepcopy(old_latin)
    old_english = tomllib.loads(before[ENGLISH].decode())
    expected_english = copy.deepcopy(old_english)
    raw_rows = {}
    preserved = {}
    for change in la['corrections']:
        target = change['target']
        proper = proper_node(old_doc, target)
        require(proper == change['proper_before'], f'Proper dictionary changed: {target}')
        require(sha(proper) == change['proper_before_sha256'], 'Declared proper hash mismatch')
        require(sha(proper['text'].encode()) == change['body_before_sha256'], 'Declared body hash mismatch')
        require(change['body_before'].count(change['replacement']['before']) == 1, 'Declared substitution not unique')
        require(change['body_before'].replace(change['replacement']['before'], change['replacement']['after'], 1) == change['body_after'], 'Not single declared substitution')
        require(sha(change['body_after'].encode()) == change['body_after_sha256'], 'Successor body hash mismatch')
        before_yaml = ''.join('          ' + s for s in change['body_before'].splitlines(keepends=True))
        after_yaml = ''.join('          ' + s for s in change['body_after'].splitlines(keepends=True))
        after[PROPER] = one_replace(after[PROPER].decode(), before_yaml, after_yaml, str(target)).encode()
        node = proper_node(expected_doc, target)
        node.clear(); node.update(copy.deepcopy(change['proper_after']))
        prior = change['owner_row_before']; successor = change['owner_row_after']
        key = latin_key(prior)
        block = row_block(after[LATIN].decode(), prior, latin_key, key)
        require(sha(block.encode()) == change['owner_row_before_raw_sha256'], 'Raw Latin row preimage changed')
        new_block = '[[entries]]\n' + '\n'.join(k + ' = ' + value(v) for k, v in successor.items()) + '\n\n'
        require(sha(new_block.encode()) == change['owner_row_after_raw_sha256'], 'Raw Latin successor mismatch')
        after[LATIN] = one_replace(after[LATIN].decode(), block, new_block, str(key)).encode()
        matches = [i for i, row in enumerate(expected_latin['entries']) if latin_key(row) == key]
        require(len(matches) == 1 and expected_latin['entries'][matches[0]] == prior, 'Latin semantic identity changed')
        expected_latin['entries'][matches[0]] = copy.deepcopy(successor)
        raw_rows[tuple(target)] = {'before_sha256': sha(block.encode()), 'after_sha256': sha(new_block.encode())}
        for item in change['old_source_files_preserved']:
            require(sha((root / item['path']).read_bytes()) == item['sha256'], 'Old source changed: ' + item['path'])
            preserved[item['path']] = item['sha256']
    require(yaml.safe_load(after[PROPER]) == expected_doc, 'Undeclared calendar value changed')
    require(tomllib.loads(after[LATIN].decode()) == expected_latin, 'Undeclared Latin ledger value changed')
    block = row_block(after[ENGLISH].decode(), en['before_binding'], english_key, en['target'])
    new_block = block
    for field in en['fields_changed']:
        pattern = re.compile(r'(?m)^' + re.escape(field) + r' = .*\n')
        matches = list(pattern.finditer(new_block))
        require(len(matches) == 1, 'English field not unique: ' + field)
        new_block = new_block[:matches[0].start()] + field + ' = ' + value(en['after_binding'][field]) + '\n' + new_block[matches[0].end():]
    require(tomllib.loads(new_block)['entries'][0] == en['after_binding'], 'English change exceeds declared three fields')
    after[ENGLISH] = one_replace(after[ENGLISH].decode(), block, new_block, 'Holy Name English row').encode()
    matches = [i for i, row in enumerate(expected_english['entries']) if english_key(row) == en['target']]
    require(len(matches) == 1, 'English target not unique')
    expected_english['entries'][matches[0]] = copy.deepcopy(en['after_binding'])
    require(tomllib.loads(after[ENGLISH].decode()) == expected_english, 'Undeclared English ledger value changed')
    require(en['before_binding']['translations'] == en['after_binding']['translations'], 'English body altered')
    for item in en['changed_files'][1:]:
        p = item['path']; before[p] = (root / p).read_bytes()
        require(sha(before[p]) == item['before_sha256'], 'Holy Name passage preimage changed: ' + p)
        after[p] = (package / p).read_bytes()
        require(sha(after[p]) == candidate_digest(p, item['after_sha256']), 'Holy Name passage successor changed: ' + p)
    immutable = en['source_payload_preserved']
    require(sha((root / immutable['path']).read_bytes()) == immutable['sha256'], 'Immutable English payload changed')
    preserved[immutable['path']] = immutable['sha256']
    for item in la['new_source_files']:
        p = item['path']; require(not (root / p).exists(), 'New source destination already exists: ' + p)
        before[p] = None; after[p] = (package / p).read_bytes()
        require(sha(after[p]) == candidate_digest(p, item['sha256']), 'New source pin mismatch: ' + p)
    rows = []
    defaults = old_latin['defaults']
    for target in [c['target'] for c in la['corrections']] + [en['target']]:
        p0 = proper_node(old_doc, target); p1 = proper_node(expected_doc, target)
        key = [target[0], '', target[2], '', '', target[4]]
        l0s = [x for x in old_latin['entries'] if latin_key(x) == key]
        l1s = [x for x in expected_latin['entries'] if latin_key(x) == key]
        e0s = [x for x in old_english['entries'] if english_key(x) == target]
        e1s = [x for x in expected_english['entries'] if english_key(x) == target]
        require(len(l0s) == len(l1s) == len(e0s) == len(e1s) == 1, 'Read-map identities not unique')
        for field in ('publication_status', 'publication_basis', 'surfaces', 'provenance_status', 'relationship', 'provenance_authority', 'provenance_confidence'):
            require({**defaults, **l0s[0]}.get(field) == {**defaults, **l1s[0]}.get(field), 'Latin permissions/grade changed')
        raw_latin = raw_rows.get(tuple(target))
        if raw_latin is None:
            b = row_block(before[LATIN].decode(), l0s[0], latin_key, key)
            raw_latin = {'before_sha256': sha(b.encode()), 'after_sha256': sha(b.encode())}
        eb0 = row_block(before[ENGLISH].decode(), e0s[0], english_key, target)
        eb1 = row_block(after[ENGLISH].decode(), e1s[0], english_key, target)
        rows.append({'target': target, 'latin_key': key, 'latin_key_mapping': dict(zip(KEYS, key)),
                     'proper': row_pair(p0, p1), 'latin_proof_raw_dictionary': row_pair(l0s[0], l1s[0]),
                     'latin_proof_default_resolved': row_pair({**defaults, **l0s[0]}, {**defaults, **l1s[0]}),
                     'latin_raw_toml_row': raw_latin, 'english_binding': row_pair(e0s[0], e1s[0]),
                     'english_raw_toml_row': {'before_sha256': sha(eb0.encode()), 'after_sha256': sha(eb1.encode())}})
    read_map = {'schema': 'triptych-latin-two-holy-name-exact-node-read-map/v1',
                'authority': 'Preparation only; original declarations and actual Root adoption govern source_epoch. No generic transition schema is activated.',
                'hash_serialization': "Dictionary SHA256: ensure_ascii=False, sort_keys=True, separators=(',',':'); raw hashes use exact UTF-8 bytes.",
                'package_manifest_sha256': sha(manifest_path.read_bytes()), 'rows': rows,
                'files': [{'canonical_path': p, 'postimage_path': 'postimages/' + p,
                           'before_sha256': sha(before[p]) if before[p] is not None else None,
                           'after_sha256': sha(after[p]), 'byte_size': len(after[p])} for p in sorted(after)],
                'preserved_files': [{'path': p, 'sha256': s} for p, s in sorted(preserved.items())],
                'invariants': {'two_single_substitution_latin_changes': True, 'only_three_english_binding_fields_changed': True,
                               'all_english_bodies_unchanged': True, 'all_unrelated_owner_values_and_bytes_preserved': True,
                               'permissions_and_grades_unchanged': True, 'native_754_authority_untouched': True},
                'ending_integration': {'gorgonius_postcommunion_en': 'Rebind proper and Latin proof only in the supplemental descriptor; English binding/body/formula unchanged.',
                                       'holy_name_collect_la': 'Entire descriptor unchanged; this Latin descriptor binds no English row.',
                                       'native_754': 'No writes or mutation allowed by this installer.'}}
    patch = ''.join(''.join(difflib.unified_diff((before[p] or b'').decode().splitlines(True), after[p].decode().splitlines(True), fromfile='a/' + p if before[p] is not None else '/dev/null', tofile='b/' + p)) for p in sorted(after))
    return before, after, read_map, patch


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--package', type=Path, required=True, help='Prepared directory containing source candidates and durable evidence')
    parser.add_argument('--out', type=Path, required=True, help='Fresh scratch directory for postimages and read-map')
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--checkpoint-released', action='store_true')
    parser.add_argument('--approved-read-map-sha256')
    args = parser.parse_args()
    root = args.root.resolve(); out = args.out.resolve(); package = args.package.resolve()
    require('.scratch' in out.relative_to(root).parts, 'Output must be under repository scratch')
    require(not out.exists(), 'Output must be a fresh directory')
    before, after, read_map, patch = prepare(root, package)
    serialized = json_bytes(read_map); digest = sha(serialized)
    if args.apply:
        require(args.checkpoint_released, 'Root checkpoint release must be explicitly asserted')
        require(args.approved_read_map_sha256 == digest, 'Fresh plan differs from the approved read-map')
    for item in read_map['files']:
        p = out / item['postimage_path']; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(after[item['canonical_path']])
    (out / 'read-map.json').write_bytes(serialized)
    (out / 'source-owner.patch').write_text(patch)
    if args.apply:
        # Fresh all-file preflight, then atomic replacement per file. This is not
        # a multi-file transaction; Root's exclusive install window is required.
        for p, raw in before.items():
            require(((root / p).read_bytes() if (root / p).exists() else None) == raw, 'Install race/preimage drift: ' + p)
        for p, raw in after.items():
            dest = root / p; dest.parent.mkdir(parents=True, exist_ok=True)
            temp = out / 'install-stage' / p
            temp.parent.mkdir(parents=True, exist_ok=True)
            require(not temp.exists(), 'Pending destination already exists')
            with temp.open('xb') as stream:
                stream.write(raw)
            os.replace(temp, dest)
        require(all((root / p).read_bytes() == raw for p, raw in after.items()), 'Installed postimage mismatch')
    (out / 'receipt.json').write_bytes(json_bytes({'status': 'applied' if args.apply else 'dry-run-only', 'read_map_sha256': digest,
                                                'files': len(after), 'canonical_writes': len(after) if args.apply else 0}))
    print(json.dumps({'status': 'applied' if args.apply else 'dry-run-only', 'read_map_sha256': digest, 'files': len(after)}))


if __name__ == '__main__':
    main()
