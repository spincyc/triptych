"""ASS26 pages199–203 native WORD whitespace witness; MIT under LICENSE."""
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser()
parser.add_argument('--bbox', required=True, type=Path)
parser.add_argument('--out', required=True, type=Path)
parser.add_argument('--map', required=True, type=Path)
args = parser.parse_args()
pages = ET.parse(args.bbox).findall('.//{*}page')
assert len(pages) == 5
results, rows, used, gaps = [], [], [], []
for number, page in enumerate(pages, 199):
    groups = []
    for line in sorted(page.findall('.//{*}line'), key=lambda item: float(item.attrib['yMin'])):
        y = float(line.attrib['yMin'])
        group = next((group for group in groups if abs(group[0] - y) <= 0.5), None)
        if group is None:
            groups.append([y, list(line.findall('{*}word'))])
        else:
            group[1].extend(line.findall('{*}word'))
    output = []
    for y, words in groups:
        words.sort(key=lambda item: float(item.attrib['xMin']))
        line_gaps = [float(b.attrib['xMin']) - float(a.attrib['xMax'])
                     for a, b in zip(words, words[1:])]
        assert all(gap >= 0 for gap in line_gaps)
        text = ''.join((' ' if i and line_gaps[i - 1] >= 2.5 else '') + (word.text or '')
                       for i, word in enumerate(words))
        output.append(text)
        gaps.extend(line_gaps)
        used.extend(id(word) for word in words)
        rows.append({'native_page': number, 'y_min': y, 'text': text,
                     'words': [{'value': word.text, **word.attrib} for word in words],
                     'inter_word_gaps_pt': line_gaps})
    results.append('\n'.join(output) + '\n')
original = [id(word) for page in pages for word in page.findall('.//{*}word')]
assert len(used) == len(set(used)) == len(original) and set(used) == set(original)
for target, payload in [(args.out, ('\f'.join(results) + '\f').encode()),
                        (args.map, (json.dumps(rows, ensure_ascii=False, indent=2) + '\n').encode())]:
    assert not target.exists() or target.read_bytes() == payload
    target.write_bytes(payload)
print(json.dumps({'status': 'pass', 'native_pages': list(range(199, 204)),
                  'native_words_preserved_once': len(used),
                  'line_y_min_tolerance_pt': 0.5, 'space_gap_threshold_pt': 2.5,
                  'max_joined_gap_pt': max(gap for gap in gaps if gap < 2.5),
                  'min_separated_gap_pt': min(gap for gap in gaps if gap >= 2.5),
                  'output_sha256': hashlib.sha256(args.out.read_bytes()).hexdigest(),
                  'map_sha256': hashlib.sha256(args.map.read_bytes()).hexdigest()}, sort_keys=True))
