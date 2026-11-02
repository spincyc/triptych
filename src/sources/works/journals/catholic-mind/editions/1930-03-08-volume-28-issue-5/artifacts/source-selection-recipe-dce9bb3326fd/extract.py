#!/usr/bin/env python3
"""Replay the exact Quinquagesimo ante Anno 1930 literal XML-word selection."""
from pathlib import Path
import json,hashlib,xml.etree.ElementTree as E
root=Path(__file__).resolve().parent
spec=json.loads((root/'geometry-selection.json').read_text())
data=(root/spec['source_xml']).read_bytes()
assert hashlib.sha256(data).hexdigest()==spec['source_xml_sha256']
objects=E.fromstring(data).findall('.//OBJECT');blocks=[]
for page in spec['pages']:
    obj=objects[page['page']-1]
    assert obj.get('usemap')==page['usemap']
    assert int(obj.get('width'))==page['width'] and int(obj.get('height'))==page['height']
    count=0
    for para in obj.iter('PARAGRAPH'):
        lines=[]
        for line in para.iter('LINE'):
            words=[]
            for word in line.iter('WORD'):
                coords=list(map(int,word.get('coords').split(',')))
                cx=(coords[0]+coords[2])/2;cy=(coords[1]+coords[3])/2
                if page['word_center_x_min']<=cx<=page['word_center_x_max'] and page['word_center_y_min']<=cy<=page['word_center_y_max']:
                    words.append(''.join(word.itertext()));count+=1
            if words:lines.append(' '.join(words))
        if lines:blocks.append(' '.join(lines))
    assert count==page['kept_words']
out=('\n\n'.join(blocks)+'\n').encode()
assert len(out)==spec['output_bytes'] and hashlib.sha256(out).hexdigest()==spec['output_sha256']
(root/spec['output']).write_bytes(out)
