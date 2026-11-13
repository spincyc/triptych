"""Two finite 1970 source-local sequences, separate from their source quotes.

This module neither appoints a current Mass nor expands a conclusion. The
prayer words are complete in their admitted sources; only checked roles,
spans, one silent action and one separately sourced response are projected.
"""
import copy
import hashlib
import json
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path
import sys
import tomllib

METHOD_ID = 'postconciliar-finite-source-local-actor-sequences-20261113'
SOURCE_SCHEMA = 'triptych-source-local-actor-source/v1'
RESULT_SCHEMA = 'triptych-source-local-actor-sequence/v1'
ACTIVE_AUTHORITY_SHA256 = '7185d96774336bf3172878119419bef8465ba696b483cd6af296f64cb53cda8d'
AUTHORITY_PATH = 'workflows/reviews/missal-english-completion-2026-11-12/postconciliar/lent-two-orations/actor-authority-v1.json'
PUBLICATION_OWNER_SCHEMA = 'triptych-source-local-publication-owner/v1'


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def sha(value):
    if not isinstance(value, (str, bytes)):
        value = canonical(value)
    return hashlib.sha256(value.encode() if isinstance(value, str) else value).hexdigest()


def require(condition, reason):
    if not condition:
        raise ValueError('source-local actors: ' + reason)


def authority(raw):
    require(bool(ACTIVE_AUTHORITY_SHA256) and sha(raw) == ACTIVE_AUTHORITY_SHA256, 'authority inactive or changed')
    value = json.loads(raw)
    require(value.get('schema') == 'triptych-finite-source-local-actor-authority/v1' and value.get('method_id') == METHOD_ID, 'unknown authority')
    rows = value['records']
    require(len(rows) == 2, 'finite owner count changed')
    indexed = {}
    for row in rows:
        public = row['public']
        key = (row['calendar'], *row['target'])
        require(key not in indexed and public['calendar'] == row['calendar'] and public['target'] == row['target'] and sha(public) == row['public_sha256'], 'source identity changed')
        indexed[key] = row
    return indexed


def bind_sources(indexed, bundles, read_source):
    """Producer seam: caller supplies actual owner dictionaries and source bytes.

    Existing mass-propers code owns locating those dictionaries. No calendar,
    body, witness, publication, or role is inferred here from prayer wording.
    """
    require(set(bundles) == set(indexed), 'finite source owners differ')
    result = {}
    for key, row in indexed.items():
        bundle = bundles[key]
        for field, hash_field in (('proper', 'proper_sha256'), ('translation', 'translation_binding_sha256'), ('provenance', 'latin_provenance_sha256')):
            require(sha(bundle[field]) == row[hash_field], 'complete ' + field + ' dictionary changed')
        for control in row['source_controls']:
            require(control['path'].startswith('src/sources/') and '..' not in control['path'].split('/'), 'source control outside library')
            require(sha(read_source(control['path'])) == control['sha256'], 'source control changed')
        public = row['public']
        english = [item for item in bundle['translation']['translations'] if item.get('lang') == 'en']
        require(len(english) == 1, 'English body is ambiguous')
        for language, text in (('la', bundle['proper']['text']), ('en', english[0]['text'])):
            require(sha(text) == public['languages'][language]['body_sha256'], 'language body changed')
        result[key] = copy.deepcopy(public)
    return result


def publication_owners(native, bundle):
    """Derive publication identities from actual bound source dictionaries.

    The actor descriptor is deliberately not an identity supplier. The English
    ledger and Latin provenance independently identify their selected text's
    publication; later agreement with the actor descriptor is a separate check.
    """
    for field, expected in (('proper', 'proper_sha256'), ('translation', 'translation_binding_sha256'), ('provenance', 'latin_provenance_sha256')):
        require(sha(bundle[field]) == native[expected], 'publication owner dictionary changed')
    english = [row for row in bundle['translation']['translations'] if row.get('lang') == 'en']
    require(len(english) == 1 and english[0].get('rights') == 'project-created' and english[0].get('source_id') is None, 'selected study English differs')
    selected = {'en': (english[0]['text'], bundle['translation'].get('study_english_passage_id')),
                'la': (bundle['proper']['text'], bundle['provenance'].get('source_id'))}
    result = {}
    for language, (text, passage) in selected.items():
        require(isinstance(passage, str) and passage.startswith('passage.'), 'selected publication owner absent')
        result[language] = {'schema': PUBLICATION_OWNER_SCHEMA, 'calendar': native['calendar'],
                            'target': native['target'], 'language': language,
                            'body_sha256': sha(text), 'passage_id': passage}
    return result


def load_sources(calendar_root, calendar, owner=None):
    """Read the two actual owners; inactive authority emits no new domain."""
    if not ACTIVE_AUTHORITY_SHA256 or calendar != 'postconciliar':
        return {}
    calendar_root = Path(calendar_root)
    repository = calendar_root.resolve().parents[2]
    if owner is None:
        loader = SourceFileLoader('_actor_sequence_source_owner', str(repository / 'tools/mass-propers'))
        spec = spec_from_loader(loader.name, loader)
        owner = module_from_spec(spec)
        sys.modules[loader.name] = owner
        loader.exec_module(owner)
    indexed = authority((repository / AUTHORITY_PATH).read_bytes())
    document = owner.load_calendar(calendar_root, calendar)
    masses = {mass['key']: mass for _, mass in owner.masses_of(document)}
    inventory = calendar_root.parent / 'inventories'
    translations = tomllib.loads((inventory / 'postconciliar-proper-translations-v1.toml').read_text())
    provenance = tomllib.loads((inventory / 'postconciliar-proper-latin-provenance-v1.toml').read_text())
    bundles = {}
    for key, native in indexed.items():
        target = native['target']
        mass = masses[target[0]]
        proper = [row for label, row in owner.propers_of(mass)
                  if not row.get('takes_from') and row.get('name') == target[2]
                  and owner.form_id_for_label(mass, label) == target[1]]
        translation = [row for row in translations['entries']
                       if owner.translation_record_identity(row, document) == tuple(target)]
        proof = [row for row in provenance['entries']
                 if (row['mass'], owner.form_id_for_label(masses[row['mass']], row.get('form', '')),
                     row['proper'], row.get('cycle') or 'all', row['occurrence']) == tuple(target)]
        require(target[3:] == ['all', 1] and len(proper) == len(translation) == len(proof) == 1, 'finite source owner ambiguous')
        bundles[key] = {'proper': proper[0], 'translation': translation[0], 'provenance': proof[0]}
    bound = bind_sources(indexed, bundles, lambda path: (repository / path).read_bytes())
    return {tuple(native['target']): {'source': bound[key], 'publication_owners': publication_owners(native, bundles[key])}
            for key, native in indexed.items()}


def attach_publication_owners(proper, bound):
    """Attach metadata to the actual publishable language selections only."""
    result = copy.deepcopy(proper)
    owners = bound['publication_owners']
    latin = result.get('latin')
    require(isinstance(latin, dict) and latin.get('withheld') is False
            and isinstance(latin.get('publication'), dict)
            and latin['publication'].get('status') == 'permitted'
            and isinstance(latin.get('provenance'), dict)
            and latin['provenance'].get('source_id') == owners['la']['passage_id']
            and sha(result.get('text') or '') == owners['la']['body_sha256'], 'selected Latin publication differs')
    english = [row for row in result.get('translations') or []
               if row.get('lang') == 'en' and row.get('source_id') is None
               and row.get('rights') == 'project-created']
    require(len(english) == 1 and sha(english[0].get('text') or '') == owners['en']['body_sha256'], 'selected English publication differs')
    latin['publication_owner'] = copy.deepcopy(owners['la'])
    english[0]['publication_owner'] = copy.deepcopy(owners['en'])
    return result


def validate_public_owner(proper, bound):
    """Release gate: independently compare selected bodies and publications."""
    require(isinstance(proper, dict), 'public proper is not an object')
    require(sha(proper.get('source_local_actor_sequences')) == sha([bound['source']]), 'actor descriptor changed')
    owners = bound['publication_owners']
    latin = proper.get('latin')
    require(isinstance(latin, dict) and sha(latin.get('publication_owner')) == sha(owners['la'])
            and isinstance(latin.get('provenance'), dict)
            and latin['provenance'].get('source_id') == owners['la']['passage_id']
            and isinstance(latin.get('publication'), dict)
            and latin['publication'].get('status') == 'permitted'
            and latin.get('withheld') is False
            and sha(proper.get('text') or '') == owners['la']['body_sha256'], 'current Latin publication owner differs')
    require(isinstance(proper.get('translations'), list), 'public translations are not a list')
    english = [row for row in proper['translations']
               if isinstance(row, dict) and row.get('lang') == 'en'
               and row.get('source_id') is None and row.get('rights') == 'project-created']
    require(len(english) == 1 and sha(english[0].get('publication_owner')) == sha(owners['en'])
            and sha(english[0].get('text') or '') == owners['en']['body_sha256'], 'current English publication owner differs')
    for language, selected in owners.items():
        part = bound['source']['languages'][language]
        require(selected['passage_id'] == part['publication_passage_id'] and selected['body_sha256'] == part['body_sha256'], 'publication and actor sources differ')
    return bound['source']


def span(text, value):
    require(isinstance(value, dict) and value.get('offset_units') == 'utf16', 'unknown source span')
    start, end = value.get('start'), value.get('end')
    raw = text.encode('utf-16-le')
    require(type(start) is int and type(end) is int and 0 <= start < end and end * 2 <= len(raw), 'invalid source span')
    return raw[start*2:end*2].decode('utf-16-le')


def execute(context, indexed):
    try:
        require(bool(ACTIVE_AUTHORITY_SHA256), 'authority inactive')
        require(isinstance(context, dict) and context.get('calendar') == 'postconciliar' and context.get('executionScope') == 'source-local-1970', 'unbound source-local context')
        member = context['member']
        require(isinstance(member, dict), 'member is not an object')
        require(isinstance(member.get('id'), str) and bool(member['id']), 'unbound member')
        source = member['source']
        require(isinstance(source, dict), 'source is not an object')
        require(source.get('schema') == SOURCE_SCHEMA and source.get('method_id') == METHOD_ID, 'unknown source projection')
        key = (source['calendar'], *source['target'])
        require(key in indexed and sha(source) == indexed[key]['public_sha256'], 'unlisted or changed source projection')
        require(source['calendar'] == context['calendar'] and source['target'] == member['target'], 'different source owner')
        require(source['source_preserved'] is True and source['target_2008_authenticated'] is False and source['context']['execution_scope'] == context['executionScope'], 'source scope changed')
        selected = context['selection']
        require(selected['target'] == source['target'] and selected['source_selection'] == source['context']['source_selection'], 'different source-local selection')
        language, text = member['language'], member['text']
        require(language in ('en','la') and isinstance(text,str), 'unsupported language')
        part = source['languages'][language]
        require(sha(text) == part['body_sha256'] and member['publication_passage_id'] == part['publication_passage_id'], 'body or publication owner changed')
        result, accounted = [], []
        for spec in part['sequence']:
            unit = copy.deepcopy(spec)
            require(isinstance(unit.get('source_hooks'),list) and bool(unit['source_hooks']), 'unbound sequence source')
            if unit['kind'] == 'action':
                require(unit['role'] == unit['action'] == 'silent-prayer' and unit['participants'] == 'all' and unit['speaker'] is None and unit['dialogue_role'] is None and unit['text'] is None and unit['spoken_text'] is None and unit['source_span'] is None, 'unbound silent action')
            else:
                require(unit['kind'] == 'spoken' and unit['speaker'] in (None,'priest','people'), 'unbound spoken actor')
                if unit['source_span'] is not None:
                    unit['text'] = span(text,unit['source_span'])
                    accounted.append((unit['source_span']['start'],unit['source_span']['end']))
                else:
                    require(unit['role'] == unit['dialogue_role'] == 'response' and unit['speaker'] == 'people' and unit['response_source'] == 'separately-sourced-response' and unit['text'] == 'Amen.', 'unbound external response')
                marker = unit.get('nonspoken_role_marker')
                if marker:
                    require(unit['dialogue_role'] == 'response' and marker['text'] == 'R.' and span(text,marker) == marker['text'], 'printed response marker changed')
                    accounted.append((marker['start'],marker['end']))
            result.append(unit)
        require(sum(unit.get('dialogue_role') == 'response' for unit in result) == 1 and result[-1]['role'] == 'response', 'response count or order changed')
        raw, previous = text.encode('utf-16-le'), 0
        for start,end in sorted(accounted):
            require(start >= previous and not raw[previous*2:start*2].decode('utf-16-le').strip(), 'source words omitted or repeated')
            previous = end
        require(not raw[previous*2:].decode('utf-16-le').strip(), 'source tail omitted')
        return {'schema':RESULT_SCHEMA,'state':'source-derived-complete','execution_extent':{'state':'source-derived-complete','method_id':METHOD_ID},'execution_scope':'source-local-1970','calendar':source['calendar'],'target':source['target'],'language':language,'source_text':text,'body_sha256':part['body_sha256'],'source_preserved':True,'target_2008_authenticated':False,'qualification':source['qualification'],'source_selection':source['context']['source_selection'],'sequence':result}
    except (ValueError,KeyError,TypeError,IndexError,UnicodeError):
        return {'schema':RESULT_SCHEMA,'state':'unresolved','execution_extent':{'state':'unresolved','method_id':METHOD_ID},'reasons':['source-local-actor-source-or-context-unbound'],'sequence':[]}
