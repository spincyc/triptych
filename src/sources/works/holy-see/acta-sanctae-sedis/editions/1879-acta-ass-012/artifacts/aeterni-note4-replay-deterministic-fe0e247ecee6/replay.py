"""Replay one image OCR insertion and source-note byte permutation.

MIT License; copyright 2026 Triptych contributors. Permission is granted to
use, copy, modify, merge, publish, distribute, sublicense and/or sell copies
subject to retaining this notice. THE SOFTWARE IS PROVIDED AS IS, WITHOUT
WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY.
"""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path

def sha(b): return hashlib.sha256(b).hexdigest()
def replay(recipe_path,root,out):
    recipe=json.loads(recipe_path.read_text()); out.mkdir(parents=True,exist_ok=False)
    for tool,pin in recipe['tools'].items():
        if sha(Path(tool).read_bytes())!=pin['sha256']:raise ValueError('tool hash differs: '+tool)
    for name,pin in recipe['inputs'].items():
        if sha((root/pin['path']).read_bytes())!=pin['sha256']:raise ValueError('input hash differs: '+name)
    h=recipe['helper']; assert sha((root/h['path']).read_bytes())==h['sha256']
    sys.path.insert(0,str(root/'scripts'))
    from _papal_source_order import derive
    witness=root/recipe['inputs']['witness']['path']
    subprocess.run(['/usr/bin/pdfimages','-png',str(witness),str(out/'native')],check=True,capture_output=True)
    native=out/'native-000.png'; assert sha(native.read_bytes())==recipe['outputs']['native_png_sha256']
    crop=out/'crop.png'
    subprocess.run(['/usr/bin/magick',str(native),'-crop',recipe['crop']['geometry'],'+repage','-resize',recipe['crop']['resize'],'-bordercolor','white','-border',str(recipe['crop']['border']),'-strip',str(crop)],check=True,capture_output=True)
    assert sha(crop.read_bytes())==recipe['outputs']['crop_sha256']
    model=root/recipe['inputs']['model']['path']; ocr=out/'ocr'
    command=['/usr/bin/tesseract',str(crop),str(ocr),'--tessdata-dir',str(model.parent),'-l','eng','--psm','6','-c','tessedit_create_txt=1','-c','tessedit_create_tsv=1']
    result=subprocess.run(command,capture_output=True,check=True)
    (out/'ocr.stdout').write_bytes(result.stdout);(out/'ocr.stderr').write_bytes(result.stderr)
    raw=ocr.with_suffix('.txt').read_bytes(); tsv=ocr.with_suffix('.tsv').read_bytes()
    assert sha(raw)==recipe['outputs']['ocr_text_sha256'] and sha(tsv)==recipe['outputs']['ocr_tsv_sha256']
    spec=json.loads((root/recipe['inputs']['order_spec']['path']).read_text())
    ordered,report=derive(spec,root); assert sha(ordered)==recipe['outputs']['ordered_old_sha256']
    (out/'ordered-old.txt').write_bytes(ordered)
    offset=recipe['insertion']['ordered_old_byte_offset']
    addition=b'\n'+raw+b'\n'
    final=ordered[:offset]+addition+ordered[offset:]
    assert sha(final)==recipe['outputs']['final_sha256']
    assert final[:offset]+final[offset+len(addition):]==ordered
    (out/'text.txt').write_bytes(final)
    report.update({'recovery_schema':recipe['schema'],'status':'pass','ocr_bytes':len(raw),'insertion_byte_offset':offset,'only_added_source_bytes_sha256':sha(raw),'final_sha256':sha(final),'deleting_added_note_and_two_LFs_restores_ordered_old_bytes':True})
    (out/'replay-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,sort_keys=True))
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--recipe',type=Path,required=True);p.add_argument('--root',type=Path,default=Path.cwd());p.add_argument('--out',type=Path,required=True);a=p.parse_args();replay(a.recipe,a.root.resolve(),a.out)
