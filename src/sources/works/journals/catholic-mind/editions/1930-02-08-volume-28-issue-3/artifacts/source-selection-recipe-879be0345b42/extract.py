#!/usr/bin/env python3
"""Replay the pinned Mens nostra historical WORD-node selection."""
from pathlib import Path
import argparse,collections,hashlib,json,re,xml.etree.ElementTree as E
IDENT='sim_catholic-mind_1930-02-08_28_3'
XML_SHA='d85c949a1c9a7f8f57f0fca0923ba8d5e1506cd92e53fce1b5da4253928664e4'
PDF_SHA='1e93c54004e910d0f920c181b6e7bf52a39844582f132553e1de33cb3abbb39d'
# Separately reviewed source-page rectangles, not a generic journal template.
MASKS={1:[0,1782,340,2694],2:[0,1680,280,2686],3:[150,1782,280,2686],4:[0,1680,280,2686],5:[150,1782,280,2686],6:[0,1680,280,2703],7:[150,1782,280,2703],10:[0,1680,280,2694],11:[150,1782,280,2694],12:[0,1680,280,2686],13:[150,1782,280,2686],14:[0,1680,280,2678],15:[150,1782,280,2678],16:[0,1680,280,2678],17:[150,1782,280,2678],18:[0,1680,280,2686],19:[150,1782,280,2686],20:[0,1680,280,700]}
def sha(b):return hashlib.sha256(b).hexdigest()
def jb(o):return (json.dumps(o,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
def wordhash(ws):return sha(jb([w['text'] for w in ws]))
def run(source,out):
 xml=(source/(IDENT+'_djvu.xml')).read_bytes();pdf=(source/(IDENT+'.pdf')).read_bytes()
 assert sha(xml)==XML_SHA and sha(pdf)==PDF_SHA
 objects=E.fromstring(xml).findall('.//OBJECT');assert len(objects)==22
 blocks=[];audit=[];ordered_refs=[]
 for n,mask in MASKS.items():
  o=objects[n-1];xmin,xmax,ymin,ymax=mask
  page={'page':n,'source_usemap':o.get('usemap'),'width':int(o.get('width')),'height':int(o.get('height')),'mask':{'word_center_x_min':xmin,'word_center_x_max':xmax,'word_center_y_min':ymin,'word_center_y_max':ymax},'excluded_words':[],'kept_words':0,'kept_word_ids_in_output_order':[]}
  paras={};word_id=0
  for pi,p in enumerate(o.iter('PARAGRAPH')):
   pl=[]
   for li,l in enumerate(p.iter('LINE')):
    ws=[]
    for w in l.iter('WORD'):
     coords=list(map(int,w.get('coords').split(',')));cx=(coords[0]+coords[2])/2;cy=(coords[1]+coords[3])/2
     val={'word_id':word_id,'paragraph':pi,'line':li,'text':''.join(w.itertext()),'coords':coords};word_id+=1
     reason='neighboring-page gutter or scan-border noise' if not xmin<=cx<=xmax else 'upper journal masthead or printed running header/folio' if cy<ymin else 'following independent Retreat Congress article' if cy>ymax else None
     if reason:page['excluded_words'].append({**val,'reason':reason})
     else:ws.append(val)
    if ws and re.fullmatch(r'\d{1,4}',' '.join(w['text'] for w in ws)) and min(min(w['coords'][1],w['coords'][3]) for w in ws)>int(o.get('height'))*.88:
     page['excluded_words'] += [{**w,'reason':'isolated printed lower-margin folio'} for w in ws];ws=[]
    if ws:pl.append((li,ws))
   if pl:paras[pi]=pl
  page_blocks=[]
  if n==2:
   # The native p.42 first note line is split into three XML paragraphs.
   # Restore only this proven printed note order; every selected node stays once.
   refs=[(10,0),(9,0),(13,0),(11,0),(11,1),(12,0)]
   expected={9,10,11,12,13};assert expected.issubset(paras)
   before=[w for pi in sorted(expected) for _,ws in paras[pi] for w in ws]
   lookup={(pi,li):ws for pi,pl in paras.items() for li,ws in pl}
   notes=[[w for ref in refs[:4] for w in lookup[ref]],[w for ref in refs[4:] for w in lookup[ref]]]
   after=[w for ws in notes for w in ws]
   assert collections.Counter(w['word_id'] for w in before)==collections.Counter(w['word_id'] for w in after)
   assert len({w['word_id'] for w in after})==len(after)
   for pi,pl in paras.items():
    if pi not in expected:page_blocks.append([w for _,ws in pl for w in ws])
    elif pi==9:page_blocks.extend(notes)
   page['ordering_override']={'kind':'native-image-proven-exact-WORD-node-permutation','printed_page':'42','zero_based_paragraph_line_order':[[list(ref) for ref in refs[:4]],[list(ref) for ref in refs[4:]]],'before_word_ids':[w['word_id'] for w in before],'after_word_ids':[w['word_id'] for w in after],'before_word_text_sequence_sha256':wordhash(before),'after_word_text_sequence_sha256':wordhash(after),'all_nodes_retained_once':True,'before_source_words':before,'after_source_words':after,'basis':'Native printed p.42 shows the isolated closing quote and right-hand date fragment on note 2’s first line, its volume/page continuation on the next line, then note 3. Only exact XML nodes are reordered; no spelling or punctuation is corrected.'}
  else:
   page_blocks=[[w for _,ws in pl for w in ws] for pl in paras.values()]
  for ws in page_blocks:
   blocks.append(' '.join(w['text'] for w in ws));page['kept_word_ids_in_output_order'] += [w['word_id'] for w in ws]
   ordered_refs += [[n,w['word_id']] for w in ws]
  page['kept_words']=len(page['kept_word_ids_in_output_order']);assert page['kept_words']+len(page['excluded_words'])==word_id
  audit.append(page)
 payload=('\n\n'.join(blocks)+'\n').encode()
 report={'schema':'triptych-english-word-geometry-selection/v2','source_xml':IDENT+'_djvu.xml','source_xml_sha256':XML_SHA,'source_pdf':IDENT+'.pdf','source_pdf_sha256':PDF_SHA,'source_artifact_page_count':22,'selected_artifact_pages':list(MASKS),'printed_pages':'41–58','omitted_duplicate_artifact_pages':[{'page':8,'duplicate_of_selected_page':6,'printed_page':'46'},{'page':9,'duplicate_of_selected_page':7,'printed_page':'47'}],'following_independent_article_pages':[20,21,22],'method':'Select literal XML WORD nodes by the reviewed page-specific center-coordinate masks; retain XML paragraph/line/word order except the explicitly listed native-print-proven p.42 note-node permutation. Concatenate retained word strings with spaces and retained paragraphs with blank LF. Exclude only masthead/running furniture, gutter or scan-border noise, one repeated scan of printed pp.46–47, and the following independent article. Do not generate, correct, dehyphenate or modernize lexical content.','output':'mens-nostra-geometry-text.txt','output_sha256':sha(payload),'output_bytes':len(payload),'output_XML_WORD_count':len(ordered_refs),'ordered_source_word_references_sha256':sha(jb(ordered_refs)),'pages':audit}
 out.mkdir(parents=True,exist_ok=True);(out/report['output']).write_bytes(payload);(out/'geometry-selection.json').write_bytes(jb(report))
 return report
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--input-dir',type=Path,default=Path(__file__).resolve().parent);ap.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parent);args=ap.parse_args();r=run(args.input_dir,args.output_dir);print(json.dumps({k:r[k] for k in ['output','output_sha256','output_bytes','output_XML_WORD_count']},indent=2))
