"""Replay only the declared, independently OCR-corroborated encoding spans.

Source wording comes from the input bytes. This recipe performs no OCR,
word recognition, dictionary correction, translation, or source rewriting.
"""
import argparse
import bisect
import hashlib
import json
from pathlib import Path
import re


def sha(data):
    return hashlib.sha256(data).hexdigest()


def folded(text):
    chars, offsets = [], []
    for match in re.finditer(r'\s+|\S', text):
        chars.append(' ' if match.group().isspace() else match.group())
        offsets.append(match.start())
    return ''.join(chars), offsets


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--ocr', required=True, type=Path)
    parser.add_argument('--audit', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    audit = json.loads(args.audit.read_bytes())
    source_bytes, ocr_bytes = args.source.read_bytes(), args.ocr.read_bytes()
    assert sha(source_bytes) == audit['ws']['sha256']
    assert sha(ocr_bytes) == audit['ia']['sha256']
    source, ocr = source_bytes.decode('utf8'), ocr_bytes.decode('utf8')
    rows = audit['occurrences']
    assert len(rows) == 205
    chunks, previous, size, counts = [], 0, 0, {}
    for row in rows:
        assert row['status'] == 'CORROBORATED_EXACT_OCR_CONTEXT'
        start, end = row['start'], row['end']
        assert previous <= start < end
        assert source[start:end] == row['before']
        assert len(source[:start].encode('utf8')) == row['ws_utf8_byte_offset']
        assert len(row['after']) == 1 and not row['after'].isalnum()
        method = row['method']
        counts[method] = counts.get(method, 0) + 1
        if method == 'inverse-cp1252-utf8':
            assert row['before'].encode('cp1252').decode('utf8') == row['after']
        else:
            assert method == 'partial-black-square-hypothesis'
            assert [ord(c) for c in row['before']] == [0x00e2, 0x2013]
            assert ord(row['after']) == 0x25a0
        head = source[previous:start]
        chunks.append(head)
        size += len(head)
        assert size == row['proposed_character_offset']
        chunks.append(row['after'])
        size += len(row['after'])
        previous = end
    chunks.append(source[previous:])
    result = ''.join(chunks)
    assert counts == {'inverse-cp1252-utf8': 193, 'partial-black-square-hypothesis': 12}
    ocr_folded, ocr_offsets = folded(ocr)
    result_folded, result_offsets = folded(result)
    for row in rows:
        context = row['matching_space_folded_context']
        assert ocr_folded.count(context) == 1
        match = ocr_folded.index(context)
        target = bisect.bisect_left(ocr_offsets, row['ia_character_offset'])
        assert match <= target < match + len(context)
        assert context[target-match] == row['after']
        assert ocr[row['ia_character_offset']] == row['after']
        assert len(ocr[:row['ia_character_offset']].encode('utf8')) == row['ia_utf8_byte_offset']
        pos = bisect.bisect_left(result_offsets, row['proposed_character_offset'])
        left, right = row['requested_left_context'], row['requested_right_context']
        assert result_folded[max(0,pos-left):min(len(result_folded),pos+1+right)] == context
    assert ''.join(c for c in source if ord(c)<128) == ''.join(c for c in result if ord(c)<128)
    assert len(source.splitlines()) == len(result.splitlines()) == 3602
    assert source.count('\n') == result.count('\n')
    restored = result
    for row in reversed(rows):
        pos = row['proposed_character_offset']
        assert restored[pos:pos+1] == row['after']
        restored = restored[:pos]+row['before']+restored[pos+1:]
    assert restored.encode('utf8') == source_bytes
    payload = result.encode('utf8')
    assert sha(payload) == audit['proposed_derivative']['sha256']
    assert len(payload) == audit['proposed_derivative']['bytes']
    args.out.write_bytes(payload)
    print(json.dumps({'sha256':sha(payload),'bytes':len(payload),'changes':len(rows),'methods':counts}))


if __name__ == '__main__':
    main()
