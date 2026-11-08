"""Finite reviewed noncommercial grants; never a general LicenseRef admission."""
from hashlib import sha256
import json
from pathlib import Path

INVENTORY = Path('src/sources/inventories/noncommercial-permissions-v1.json')
INVENTORY_SHA256 = '507f95f04c91e57c83b0ee45b498922443cfca6d4f245c7cdb2850a0beeeb5de'
ARTIFACT_ID = 'artifact.origen.homiliae-in-ezechielem.2014-hooker.complete-english-homily-pages-46dfd5c2'
LICENSE = 'LicenseRef-Roger-Pearse-2018-Noncommercial'


def applies(artifact):
    return (artifact.get('rights_status') == 'permission' or
            artifact.get('id') == ARTIFACT_ID or artifact.get('license') == LICENSE)


def _bytes(root, relative):
    root = Path(root).resolve()
    path = root / relative
    if path.is_symlink() or not path.resolve().is_relative_to(root):
        raise ValueError('permission evidence escapes repository')
    return path.read_bytes()


def fingerprint(root):
    """Bind the in-process corpus cache to both policy and reviewed evidence."""
    try:
        evidence = _bytes(root, INVENTORY)
    except (OSError, ValueError):
        evidence = b'missing'
    return sha256(Path(__file__).read_bytes() + evidence).hexdigest()


def problems(root, artifact, passage=None, *, text=None):
    if not applies(artifact):
        return []
    try:
        raw = _bytes(root, INVENTORY)
        if sha256(raw).hexdigest() != INVENTORY_SHA256:
            raise ValueError('missing or changed reviewed grant inventory')
        grant = json.loads(raw)['grants'][0]
        actual = sha256(json.dumps(artifact, sort_keys=True, ensure_ascii=False,
                                  separators=(',', ':')).encode()).hexdigest()
        if artifact.get('id') != grant['artifact_id'] or actual != grant['artifact_metadata_sha256']:
            raise ValueError('artifact is outside the exact reviewed noncommercial grant')
        payload = _bytes(root, artifact['path'])
        if sha256(payload).hexdigest() != grant['artifact_sha256']:
            raise ValueError('reviewed permission payload is missing or changed')
        if passage is not None:
            if passage.get('artifact_sha256') != grant['artifact_sha256']:
                raise ValueError('passage is not pinned to the reviewed permission payload')
            lines = payload.decode('utf-8').split('\n')
            ranges = passage.get('physical_line_ranges')
            if not isinstance(ranges, list) or not ranges or any(
                    not isinstance(pair, list) or len(pair) != 2 or
                    any(type(n) is not int for n in pair) or
                    not 1 <= pair[0] <= pair[1] <= len(lines) for pair in ranges):
                raise ValueError('permission passage needs exact physical line bounds')
            selected = text if text is not None else passage.get('text')
            if selected is not None:
                segments = passage.get('transcription_segments')
                if segments is None:
                    expected = '\n'.join(lines[n - 1] for first, last in ranges
                                         for n in range(first, last + 1))
                else:
                    if not isinstance(segments, list) or not segments:
                        raise ValueError('permission transcription has no exact segments')
                    previous, offset, kept = 0, 0, []
                    for segment in segments:
                        number, words = segment.get('line'), segment.get('text')
                        if (type(number) is not int or number < previous or
                                not any(first <= number <= last for first, last in ranges) or
                                not isinstance(words, str) or not words):
                            raise ValueError('permission transcription leaves its source bounds')
                        found = lines[number - 1].find(words, offset if number == previous else 0)
                        if found < 0:
                            raise ValueError('permission transcription differs from source bytes')
                        previous, offset = number, found + len(words)
                        kept.append(words)
                    expected = ' '.join(kept)
                if not isinstance(selected, str) or ' '.join(selected.split()) != ' '.join(expected.split()):
                    raise ValueError('permission reading differs from its exact source selection')
        return []
    except (OSError, ValueError, TypeError, KeyError, AttributeError, IndexError) as error:
        return ['Reviewed noncommercial permission refused: ' + str(error)]


def allowed(root, artifact, passage=None):
    return applies(artifact) and not problems(root, artifact, passage)
