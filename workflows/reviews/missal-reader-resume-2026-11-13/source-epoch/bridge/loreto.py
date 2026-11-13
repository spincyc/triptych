"""Finite pending compiler amendment for the accepted Loreto model correction.

This neither publishes a text nor changes its status. It preserves three exact
removed-body Latin rows as historical evidence while accounting for the actual
one-Collect appointment and its one English no-exemplar disposition.
"""
from hashlib import sha256
import json
import tomllib
import yaml

PARENT = '80cbdbb0357d00c809049c4f44b6d42f3c7a6a7c'
ADOPTION = 'workflows/reviews/missal-reader-resume-2026-11-13/common-additions/root-source-model-admission.json'
ADOPTION_SHA = '505b625ea5501c0a2fbcbcd04bd53a7d7ce5b10c31c6c2f2b52e9948c0206549'
DECLARATION = 'workflows/reviews/missal-reader-resume-2026-11-13/common-additions/loreto-correction-and-history-v7.json'
DECLARATION_SHA = '7c69a2ce1fbba78db143bcad3be86c7153b20248308a43ef10da1a384b549dc1'
CALENDAR = 'src/sources/calendars/postconciliar/propers.yaml'
ENGLISH = 'src/sources/inventories/postconciliar-proper-translations-v1.toml'
LATIN = 'src/sources/inventories/postconciliar-proper-latin-provenance-v1.toml'
NAMES = ('Collect', 'Prayer after Communion', 'Prayer over the Offerings')
ENGLISH_KEYS = tuple(('our-lady-loreto', 'main', name, 'all', 1) for name in NAMES)
LATIN_KEYS = tuple({'mass': 'our-lady-loreto', 'form': '', 'proper': name,
                    'course': '', 'cycle': '', 'occurrence': 1} for name in NAMES)


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def require(value, message):
    if not value:
        raise AssertionError('finite Loreto transition: ' + message)


def digest(raw):
    return sha256(raw).hexdigest()


def english_key(row):
    return canonical([row['mass'], row.get('form_id', 'main'), row['proper'],
                      row.get('cycle', 'all'), row.get('occurrence', 1)])


def selected_mass(raw):
    document = yaml.safe_load(raw)
    rows = [mass for section in document['sections'].values() for mass in section.get('masses', [])
            if mass.get('key') == 'our-lady-loreto']
    require(len(rows) == 1, 'one exact current Mass owner')
    return rows[0]


def bind(root, pins, store):
    """Require exact already-adopted source facts before either finite exception."""
    for relative, expected in ((ADOPTION, ADOPTION_SHA), (DECLARATION, DECLARATION_SHA)):
        require(pins.get(relative) == expected, 'complete adoption/declaration belongs to current source epoch')
        require(digest((root / relative).read_bytes()) == expected, 'complete adopted evidence bytes')
    for relative in (CALENDAR, ENGLISH, LATIN):
        require(pins.get(relative) == digest((root / relative).read_bytes()), 'complete current source owner pin')
    declaration = json.loads((root / DECLARATION).read_bytes())
    require(selected_mass(store.blob(PARENT, CALENDAR)) == declaration['mass_before'], 'entire committed former Mass')
    require(selected_mass((root / CALENDAR).read_bytes()) == declaration['mass_after'], 'entire accepted current Mass')
    before = {english_key(row): row for row in declaration['superseded_prior_gaps']}
    after = {english_key(row): row for row in declaration['gap_after']}
    keys = {canonical(list(key)) for key in ENGLISH_KEYS}
    require(set(before) == keys and set(after) == {canonical(list(ENGLISH_KEYS[0]))}, 'exact three-to-one English owner set')
    require(all(row['availability'] == 'unavailable' and row['reason'] == {'kind': 'no-exemplar'}
                for row in after.values()), 'no new English publication state')
    for raw, expected in ((store.blob(PARENT, ENGLISH), before), ((root / ENGLISH).read_bytes(), after)):
        ledger = tomllib.loads(raw.decode())
        selected = {english_key(row): row for row in ledger['untranslated'] if row.get('mass') == 'our-lady-loreto'}
        require(selected == expected, 'entire exact refusal dictionaries')
        require(not any(row.get('mass') == 'our-lady-loreto' for row in ledger['entries']), 'no Loreto positive English introduced')
    tombstones = declaration['untouched_latin_tombstones']
    require(tombstones['inventory'] == LATIN and len(tombstones['entries']) == 3, 'three historical Latin tombstones')
    wanted = {canonical(key) for key in LATIN_KEYS}
    require({canonical({field: row[field] for field in LATIN_KEYS[0]}) for row in tombstones['entries']} == wanted,
            'exact Latin historical owner identities')
    for raw in (store.blob(PARENT, LATIN), (root / LATIN).read_bytes()):
        ledger = tomllib.loads(raw.decode())
        selected = [row for row in ledger['entries'] if row.get('mass') == 'our-lady-loreto']
        require(sorted(selected, key=canonical) == sorted(tombstones['entries'], key=canonical),
                'all complete removed Latin dictionaries remain unchanged')
    require(all(row['body_status'] == 'removed' for row in tombstones['entries']), 'only removed bodies retained')
    return {'old_absences': before, 'new_absences': after, 'latin_keys': wanted,
            'adoption_path': ADOPTION, 'adoption_sha256': ADOPTION_SHA,
            'declaration_path': DECLARATION, 'declaration_sha256': DECLARATION_SHA}


def latin_domain(calendar, parsed, bodies, parent_parsed, binding):
    if calendar != 'postconciliar':
        require(set(parsed) == set(bodies), 'ordinary complete Latin owner domain')
        return []
    keys = binding['latin_keys']
    require(set(parsed) - set(bodies) == keys and not (set(bodies) - set(parsed)),
            'only exact three retained historical tombstones lack current body owners')
    for key in keys:
        row = parsed[key]
        require(row == parent_parsed[key], 'complete resolved historical proof dictionary unchanged')
        require(row['body_status'] == 'removed' and row['publication_status'] == 'unresolved'
                and row['publication_basis'] == 'unresolved' and row['surfaces'] == [],
                'retained historical proof cannot publish a body')
    return sorted(keys)


def english_absence_complement(calendar, before, current, binding):
    if calendar != 'postconciliar':
        return before
    old, new = binding['old_absences'], binding['new_absences']
    require(all(before.get(key) == row for key, row in old.items()), 'exact former English refusals in semantic parent')
    require({key: current[key] for key in old if key in current} == new,
            'exact current no-exemplar disposition and no obsolete extra owners')
    protected = dict(before)
    for key in old:
        del protected[key]
    protected.update(new)
    return protected
