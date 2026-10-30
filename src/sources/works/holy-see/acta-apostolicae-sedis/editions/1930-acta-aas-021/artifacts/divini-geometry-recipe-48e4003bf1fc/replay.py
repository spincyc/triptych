# SPDX-License-Identifier: MIT
"""Replay explicitly reviewed source byte partitions; infer no text or geometry."""
from pathlib import Path
import argparse,collections,hashlib,json
SCHEMA='triptych-papal-source-byte-partition/v1'
def sha(data):return hashlib.sha256(data).hexdigest()
def nonspace(data):return ''.join(data.decode('utf-8').split())
def replay(spec,root):
 if spec.get('schema')!=SCHEMA:raise ValueError('unsupported recipe schema')
 path=Path(spec['source_path'])
 if path.is_absolute() or '..' in path.parts:raise ValueError('source path must remain relative')
 root=root.resolve();source=(root/path).resolve()
 if not source.is_relative_to(root):raise ValueError('source escapes root')
 raw=source.read_bytes()
 if sha(raw)!=spec['source_sha256']:raise ValueError('source hash mismatch')
 raw.decode('utf-8');lines=raw.split(b'\n');selected=set();previous=0
 for pair in spec['physical_line_ranges']:
  a,b=pair
  if type(a)is not int or type(b)is not int or not previous<a<=b<=len(lines):raise ValueError('invalid source ranges')
  selected.update(range(a,b+1));previous=b
 remaining={n:lines[n-1] for n in selected};used=set();anchors={}
 for group in spec['margin_groups']:
  anchor=group['anchor_source_line']
  if anchor not in selected or anchor in anchors:raise ValueError('invalid or duplicate anchor')
  chunks=[];ordinals=[]
  for item in group['slices']:
   n=item['source_line'];a,b=item['utf8_bytes']
   if n not in selected or n in used:raise ValueError('source slice outside selection or repeated')
   line=lines[n-1]
   if not (type(a)is int and type(b)is int and 0<=a<b<=len(line) and (a==0 or b==len(line))):raise ValueError('slice must be a complete prefix or suffix')
   part=line[a:b];part.decode('utf-8');line[:a].decode('utf-8');line[b:].decode('utf-8')
   if sha(part)!=item['slice_sha256']:raise ValueError('source slice hash mismatch')
   cut=a if a else b
   left=line[:cut].decode('utf-8');right=line[cut:].decode('utf-8')
   if left and right and not (left[-1].isspace() or right[0].isspace()):raise ValueError('boundary splits a source token')
   if not part.strip():raise ValueError('empty marginal source unit')
   remaining[n]=line[:a]+line[b:];chunks.append(part.strip());used.add(n);ordinals.append(n)
  if ordinals!=sorted(ordinals) or anchor!=min(ordinals):raise ValueError('marginal source order or anchor changed')
  anchors[anchor]=b'\t'+b' '.join(chunks)
 before=set();after=set();previous=0
 for a,b in spec['page_foot_block_ranges']:
  if not previous<a<=b or not any(x<=a<=b<=y for x,y in spec['physical_line_ranges']):raise ValueError('invalid page-foot block range')
  if any(n in used for n in range(a,b+1)):raise ValueError('page-foot block overlaps marginal source unit')
  before.add(a);after.add(b);previous=b
 pieces=[]
 for a,b in spec['physical_line_ranges']:
  output=[]
  for n in range(a,b+1):
   if n in anchors:output.extend([b'',anchors[n],b''])
   if n in before:output.append(b'')
   output.append(remaining[n].strip())
   if n in after:output.append(b'')
  pieces.append(b'\n'.join(output))
 result=b'\n\n'.join(pieces)+b'\n'
 original=b'\n\n'.join(b'\n'.join(lines[a-1:b]) for a,b in spec['physical_line_ranges'])+b'\n'
 if collections.Counter(nonspace(original))!=collections.Counter(nonspace(result)):raise ValueError('source non-whitespace units changed')
 if sha(result)!=spec['output_sha256']:raise ValueError('output hash differs')
 return result,{'source_sha256':sha(raw),'output_sha256':sha(result),'margin_groups':len(anchors),'marginal_slices':len(used),'page_foot_blocks':len(before),'nonwhitespace_characters':len(nonspace(result)),'source_units_preserved':True,'body_source_order_preserved':True,'inference':False}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--spec',type=Path,required=True);p.add_argument('--root',type=Path,default=Path('.'));p.add_argument('--out',type=Path,required=True);p.add_argument('--check',action='store_true');a=p.parse_args()
 result,report=replay(json.loads(a.spec.read_text()),a.root);target=a.out.resolve()
 if a.check:
  if target.read_bytes()!=result:raise ValueError('retained output differs')
 else:
  root=a.root.resolve()
  if not (target.is_relative_to(root/'.scratch') or target.is_relative_to(root/'build')):raise ValueError('write output must remain scratch/build')
  target.parent.mkdir(parents=True,exist_ok=True)
  if target.exists() and target.read_bytes()!=result:raise ValueError('refusing to overwrite different output')
  target.write_bytes(result)
 print(json.dumps(report,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
