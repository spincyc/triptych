#!/usr/bin/env python3
"""Replay one exact historical journal WORD-coordinate selection."""
from pathlib import Path
import json,hashlib,xml.etree.ElementTree as E,re
ROOT=Path(__file__).resolve().parent
SPEC='sim_catholic-mind_1928-02-22_26_4'
a=json.loads((ROOT/'geometry-selection.json').read_text());data=(ROOT/a['source_xml']).read_bytes();assert hashlib.sha256(data).hexdigest()==a['source_xml_sha256']
objects=E.fromstring(data).findall('.//OBJECT');blocks=[]
for page in a['pages']:
 o=objects[page['page']-1]
 for para in o.iter('PARAGRAPH'):
  text=[]
  for line in para.iter('LINE'):
   words=[]
   for w in line.iter('WORD'):
    raw=''.join(w.itertext());c=list(map(int,w.get('coords').split(',')));cx=(c[0]+c[2])/2;cy=(c[1]+c[3])/2
    if page['word_center_x_min']<=cx<=page['word_center_x_max'] and page['word_center_y_min']<=cy<=page['word_center_y_max']:words.append((raw,c))
   if words and re.fullmatch(r'\d{1,4}',' '.join(w[0] for w in words)) and min(min(w[1][1],w[1][3]) for w in words)>int(o.get('height'))*.88:words=[]
   if words:text.append(' '.join(w[0] for w in words))
  if text:blocks.append(' '.join(text))
out=('\n\n'.join(blocks)+'\n').encode();assert hashlib.sha256(out).hexdigest()==a['output_sha256'];assert len(out)==a['output_bytes'];(ROOT/a['output']).write_bytes(out)
