#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Triptych contributors.
# MIT applies only to this source-specific orchestration; historical wording and
# image pixels retain their separate public-domain basis. Full grant: LICENSES/MIT.txt.
"""Exclude four proven foreign OCR spans and five authorized own folio rows only."""
import argparse,hashlib,json,os,subprocess
from pathlib import Path


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,required=True)
    p.add_argument('--recipe',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();root=a.root.resolve();out=a.out.resolve()
    assert any(out.is_relative_to(root/n) for n in ['.scratch','build'])
    recipe=json.loads(a.recipe.read_text())
    assert sha(Path(__file__).read_bytes())==recipe['implementation']['sha256']
    inputs={}
    for name,pin in recipe['inputs'].items():
        data=(root/pin['path']).read_bytes()
        assert sha(data)==pin['sha256'] and len(data)==pin['byte_size'],name
        inputs[name]=data
    parent=inputs['parent_text'];frozen=json.loads(inputs['foreign_span_disposition'])
    image_proof=json.loads(inputs['foreign_span_image_proof'])
    assert image_proof['source_sha256']==sha(parent)
    assert image_proof['frozen_span_disposition']['sha256']==sha(inputs['foreign_span_disposition'])
    for name,pin in recipe['tools'].items():
        assert sha(Path(pin['path']).read_bytes())==pin['sha256'],name
    out.mkdir(parents=True,exist_ok=False)
    native_out=out/'native';native_out.mkdir()
    native_receipts=[]
    env=dict(os.environ,OMP_THREAD_LIMIT='1',PYTHONDONTWRITEBYTECODE='1',TRIPTYCH_LIBRARY_CACHE='0')
    for evidence in image_proof['actual_freshly_viewed_context_crops']:
        number=evidence['original_pdf_page'];stem=native_out/f'original-{number}'
        commands=[[recipe['tools']['pdftoppm']['path'],'-png','-scale-to','2200','-f',str(number),'-l',str(number),'-singlefile',str(root/recipe['inputs']['facsimile']['path']),str(stem)]]
        x,y,w,h=evidence['crop_rectangle_xywh']
        commands.append([recipe['tools']['magick']['path'],str(stem.with_suffix('.png')),'-crop',f'{w}x{h}+{x}+{y}','+repage','-quality',str(evidence['quality']),str(stem.with_suffix('.jpg'))])
        for command in commands:subprocess.run(command,env=env,capture_output=True,check=True)
        assert sha(stem.with_suffix('.png').read_bytes())==evidence['source_image_sha256']
        assert sha(stem.with_suffix('.jpg').read_bytes())==evidence['sha256']
        native_receipts.append({'original_native_page':number,'source_png_sha256':evidence['source_image_sha256'],'context_crop_sha256':evidence['sha256'],'crop_rectangle_xywh':evidence['crop_rectangle_xywh'],'source_and_crop_equal_frozen_primary_evidence':True})
    assert frozen['source_sha256']==sha(parent)
    foreign=frozen['exact_four_blocks'];assert len(foreign)==4
    own_proof=json.loads(inputs['own_folio_exclusion_proof'])
    assert own_proof['source_sha256']==sha(parent)
    assert own_proof['frozen_cold_image_proof_sha256']==sha(inputs['foreign_span_image_proof'])
    own=own_proof['exclusions'];assert len(own)==5
    for evidence in own:
        number=evidence['original_pdf_page'];stem=native_out/f'original-{number}'
        if not stem.with_suffix('.png').exists():
            subprocess.run([recipe['tools']['pdftoppm']['path'],'-png','-scale-to','2200','-f',str(number),'-l',str(number),'-singlefile',str(root/recipe['inputs']['facsimile']['path']),str(stem)],env=env,capture_output=True,check=True)
        assert sha(stem.with_suffix('.png').read_bytes())==evidence['source_image_sha256']
        x,y,w,h=evidence['crop_rectangle_xywh'];crop=native_out/evidence['crop_filename']
        subprocess.run([recipe['tools']['magick']['path'],str(stem.with_suffix('.png')),'-crop',f'{w}x{h}+{x}+{y}','+repage','-strip',str(crop)],env=env,capture_output=True,check=True)
        assert sha(crop.read_bytes())==evidence['crop_sha256']
        native_receipts.append({'classification':'OWN_LAYOUT_FURNITURE','original_native_page':number,'source_png_sha256':evidence['source_image_sha256'],'folio_crop_sha256':evidence['crop_sha256'],'crop_rectangle_xywh':evidence['crop_rectangle_xywh'],'source_and_crop_equal_frozen_primary_evidence':True})
    blocks=sorted(foreign+own,key=lambda v:v['source_byte_range_half_open'][0]);assert len(blocks)==9
    source_lines=parent.splitlines(keepends=True);line_offsets=[0]
    for line in source_lines:line_offsets.append(line_offsets[-1]+len(line))
    pieces=[];cursor=0;out_cursor=0;intervals=[];removed=[]
    for block in blocks:
        start,end=block['source_byte_range_half_open'];first,last=block['source_LF_range']
        assert cursor<=start<end<=len(parent)
        assert [start,end]==[line_offsets[first-1],line_offsets[last]]
        discarded=parent[start:end]
        assert sha(discarded)==block['block_sha256']
        assert discarded.decode('utf-8')==block['block_utf8']
        assert block['classification'] in ['FOREIGN_CLIPPED_FACING_PAGE','EXTRANEOUS_RECOGNITION_OUTPUT','OWN_LAYOUT_FURNITURE']
        kept=parent[cursor:start];pieces.append(kept)
        intervals.append({'removed_parent_byte_range':[start,end],'source_LF_range':[first,last],'removed_sha256':sha(discarded),'source_classification':block['classification'],'original_native_page':block.get('original_native_page',block.get('original_pdf_page')),'printed_folio':block['printed_folio'],'retained_parent_byte_range':[cursor,start],'retained_output_byte_range':[out_cursor,out_cursor+len(kept)],'retained_sha256':sha(kept),'output_deletion_boundary':out_cursor+len(kept)})
        removed.append(discarded);out_cursor+=len(kept);cursor=end
    suffix=parent[cursor:];pieces.append(suffix);final=b''.join(pieces)
    assert sha(final)==recipe['output_sha256']
    reconstructed=b''
    for i,part in enumerate(pieces):
        reconstructed+=part
        if i<len(removed):reconstructed+=removed[i]
    assert reconstructed==parent
    (out/'text.txt').write_bytes(final)
    report={'schema':'triptych-etsi-foreign-ocr-exclusion-replay/v1','status':'pass','parent_sha256':sha(parent),'output_sha256':sha(final),'parent_bytes':len(parent),'output_bytes':len(final),'removed_bytes':sum(map(len,removed)),'input_LF_count':parent.count(b'\n'),'output_LF_count':final.count(b'\n'),'recipe_sha256':sha(a.recipe.read_bytes()),'implementation_sha256':sha(Path(__file__).read_bytes()),'foreign_span_disposition_sha256':sha(inputs['foreign_span_disposition']),'removals':intervals,'retained_suffix_parent_byte_range':[cursor,len(parent)],'retained_suffix_output_byte_range':[out_cursor,len(final)],'retained_suffix_sha256':sha(suffix),'all_other_parent_bytes_retained_exactly':True,'reinserting_only_the_nine_original_spans_restores_parent_exactly':True,'foreign_removed_bytes':sum(x['source_byte_range_half_open'][1]-x['source_byte_range_half_open'][0] for x in foreign),'own_folio_removed_bytes':sum(x['source_byte_range_half_open'][1]-x['source_byte_range_half_open'][0] for x in own),'primary_image_replay':native_receipts,'source_word_insertions':0,'whitespace_normalization':False,'limitations':'Exact native-justified exclusion only; this mechanical replay does not confer fresh independent source/PDF acceptance or body-wide lexical collation.'}
    (out/'replay-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','parent_sha256','output_sha256','removed_bytes','foreign_removed_bytes','own_folio_removed_bytes','output_LF_count','all_other_parent_bytes_retained_exactly']}))


if __name__=='__main__':main()
