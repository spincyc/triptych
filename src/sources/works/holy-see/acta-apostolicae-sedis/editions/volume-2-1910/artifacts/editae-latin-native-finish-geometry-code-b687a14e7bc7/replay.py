"""Editae saepe AAS2 pages357–380 native WORD whitespace preparation; MIT."""
import argparse,hashlib,json,xml.etree.ElementTree as ET
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--bbox',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--map',type=Path,required=True);a=p.parse_args()
pages=ET.parse(a.bbox).findall('.//{*}page');assert len(pages)==24
results=[];rows=[];used=[];joined=[];separated=[]
for number,page in enumerate(pages,357):
 groups=[]
 for line in sorted(page.findall('.//{*}line'),key=lambda e:float(e.get('yMin'))):
  y=float(line.get('yMin'));small=float(line.get('yMax'))-y<4
  group=next((g for g in groups if g['small']==small and abs(g['y']-y)<3),None)
  if group is None:group={'y':y,'small':small,'words':[]};groups.append(group)
  group['words'].extend(line.findall('{*}word'))
 output=[]
 for group in sorted(groups,key=lambda g:g['y']):
  words=sorted(group['words'],key=lambda e:float(e.get('xMin')));gaps=[float(b.get('xMin'))-float(a.get('xMax')) for a,b in zip(words,words[1:])];assert min(gaps,default=0)>=0
  text='';join_flags=[]
  for i,w in enumerate(words):
   value=w.text or '';join=False
   if i:
    previous=words[i-1].text or ''
    # Native OCR splits letterspaced words into single-character WORDs.
    # Multi-character WORDs remain separated even in tightly set headings/notes.
    join=(not group['small'] and gaps[i-1]<2 and len(previous)==len(value)==1 and (previous.isalnum() or value.isalnum()))
    (joined if join else separated).append(gaps[i-1]);text+=('' if join else ' ')
   text+=value;join_flags.append(join)
  output.append(text);used.extend(id(w) for w in words)
  rows.append({'native_page':number,'native_line':len(output),'y_min':group['y'],'marker_size_line':group['small'],'text':text,'inter_word_gaps_pt':gaps,'join_before':join_flags,'words':[{'value':w.text,**w.attrib} for w in words]})
 results.append('\n'.join(output)+'\n')
original=[id(w) for p in pages for w in p.findall('.//{*}word')];assert len(used)==len(set(used))==len(original) and set(used)==set(original)
for target,payload in [(a.out,('\f'.join(results)+'\f').encode()),(a.map,(json.dumps(rows,ensure_ascii=False,indent=2)+'\n').encode())]:
 assert not target.exists() or target.read_bytes()==payload;target.write_bytes(payload)
print(json.dumps({'status':'pass','native_words_preserved_once':len(used),'lines':len(rows),'maximum_joined_gap_pt':max(joined),'minimum_separated_gap_pt':min(separated),'joined_gaps':len(joined),'out_sha256':hashlib.sha256(a.out.read_bytes()).hexdigest(),'map_sha256':hashlib.sha256(a.map.read_bytes()).hexdigest()},sort_keys=True))
