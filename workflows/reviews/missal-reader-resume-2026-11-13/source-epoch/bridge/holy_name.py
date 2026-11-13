"""Exact Holy Name locator exception for the accepted 80cb positive parent.

Historical Palm, legacy-four and Pentecost corrections are already part of
that parent. They receive no exception here. This helper cannot admit a body
change, alter another positive entry, or derive a source fixture.
"""
from hashlib import sha256
import json

BASE = 'workflows/reviews/missal-reader-resume-2026-11-12/latin-two-holy-name/'
DECLARATION = BASE + 'holy-name-locator-declaration.json'
DECLARATION_SHA = '8bb9cb7eea3cc345dfeee23ba066e8f2034dc2738cfbb150136bed90137ae4d6'
ADOPTION = BASE + 'root-admission.json'
ADOPTION_SHA = 'af653c80c2398d53f742024528b9c9c02c354a3f88e78ea11673fa80c28f5e80'
TARGET = ['most-holy-name-of-jesus', 'main', 'Collect', 'all', 1]
FIELDS = {'ia_leaf', 'ia_leaf_range', 'witness_note'}
BODY_SHA = 'a0136939dba2112dfd3a0dda1cca88770218a124a024e241f8bb4390a5bdc199'


def require(value, message):
    if not value:
        raise AssertionError('exact Holy Name positive complement: ' + message)


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def digest(raw):
    return sha256(raw).hexdigest()


def bound(root, pins, path, expected):
    require(pins.get(path) == expected, 'exact declared input ' + path)
    raw = (root / path).read_bytes()
    require(digest(raw) == expected, 'exact complete physical input ' + path)
    return raw


def positive_complement(root, pins, calendar, before, current):
    changed = {key for key, row in before.items() if current.get(key) != row}
    if calendar != 'roman-1962':
        require(not changed, 'all prior non-Roman positive dictionaries remain exact')
        return before, []
    key = canonical(TARGET)
    require(changed == {key}, 'only the adopted whole Holy Name dictionary may differ')
    declaration = json.loads(bound(root, pins, DECLARATION, DECLARATION_SHA))
    adoption = json.loads(bound(root, pins, ADOPTION, ADOPTION_SHA))
    require(adoption['schema'] == 'triptych-root-latin-two-and-holy-name-corrections/v1'
            and adoption['status'] == 'accepted'
            and adoption['holy_name_declaration']['sha256'] == DECLARATION_SHA,
            'actual Root adoption of this exact declaration')
    require(declaration['schema'] == 'triptych-existing-positive-metadata-correction/v1'
            and declaration['target'] == TARGET
            and declaration['change_class'] == 'existing-positive-locator-metadata-only',
            'finite metadata declaration identity')
    old, new = declaration['before_binding'], declaration['after_binding']
    require(before.get(key) == old and current.get(key) == new,
            'entire exact admitted before and after dictionaries')
    require(old.keys() == new.keys()
            and {field for field in old if old[field] != new[field]} == FIELDS
            and set(declaration['fields_changed']) == FIELDS,
            'only three accepted locator fields change')
    require(old['translations'] == new['translations'], 'every translation remains byte-exact')
    english = [row['text'] for row in old['translations'] if row.get('lang') == 'en']
    require(len(english) == 1 and digest(english[0].encode()) == BODY_SHA
            and declaration['before_body'] == declaration['after_body'] == english[0]
            and declaration['before_body_sha256'] == declaration['after_body_sha256'] == BODY_SHA,
            'entire unchanged English expression')
    payload = declaration['source_payload_preserved']
    bound(root, pins, payload['path'], payload['sha256'])
    protected = dict(before)
    protected[key] = new
    require(all(current.get(identity) == row for identity, row in protected.items()),
            'complete positive complement retained')
    return protected, [{'calendar': calendar, 'identity': key,
                        'correction_path': DECLARATION, 'correction_sha256': DECLARATION_SHA,
                        'root_adoption_path': ADOPTION, 'root_adoption_sha256': ADOPTION_SHA,
                        'changed_fields': sorted(FIELDS), 'unchanged_body_sha256': BODY_SHA}]
