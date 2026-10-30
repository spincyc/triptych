#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Triptych contributors.
# Software only: the MIT grant at LICENSES/MIT.txt applies to this source-specific
# orchestration. Historical source wording, source images, and recognition-model
# bytes retain their separately identified public-domain/Apache-2.0 terms.
"""Reproduce bounded original-page OCR and exact raw-byte selections."""
import argparse, hashlib, json, os, shutil, subprocess, zipfile
from pathlib import Path


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--recipe', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    recipe = json.loads(args.recipe.read_text())
    out = args.out.resolve()
    assert any(out.is_relative_to(root / n) for n in ['.scratch', 'build'])
    out.mkdir(parents=True, exist_ok=False)
    assert digest(Path(__file__).read_bytes()) == recipe['implementation']['sha256']
    for name, item in recipe['tools'].items():
        assert digest(Path(item['path']).read_bytes()) == item['sha256'], name
    inputs = {}
    for name, item in recipe['inputs'].items():
        data = (root / item['path']).read_bytes()
        assert digest(data) == item['sha256'] and len(data) == item['byte_size'], name
        inputs[name] = data
    models = out / 'models'
    models.mkdir()
    for model in recipe['models']:
        with zipfile.ZipFile(root / recipe['inputs'][model['archive']]['path']) as archive:
            data = archive.read(model['member'])
        assert digest(data) == model['sha256']
        (models / model['member']).write_bytes(data)
    env = dict(os.environ, OMP_THREAD_LIMIT='1', PYTHONDONTWRITEBYTECODE='1', TRIPTYCH_LIBRARY_CACHE='0')
    native = out / 'native.png'
    command = [recipe['tools']['pdftoppm']['path'], '-f', str(recipe['page']), '-singlefile', '-r', str(recipe['dpi']), '-png', str(root / recipe['inputs']['facsimile']['path']), str(native.with_suffix(''))]
    subprocess.run(command, env=env, capture_output=True, check=True)
    assert digest(native.read_bytes()) == recipe['native_png_sha256']
    receipts = []
    for block in recipe['blocks']:
        stem = out / block['id']
        x,y,w,h = block['crop_xywh']
        commands = [[recipe['tools']['magick']['path'], str(native), '-crop', f'{w}x{h}+{x}+{y}', '+repage', '-colorspace', 'Gray', '-depth', '8', *block['processing'], '-bordercolor', 'white', '-border', str(block['border']), '-strip', str(stem.with_suffix('.png'))],
                    [recipe['tools']['tesseract']['path'], str(stem.with_suffix('.png')), str(stem), '--tessdata-dir', str(models), '-l', block['language'], '--psm', str(block['psm']), '--oem', '1', *block['configuration'], '-c', 'tessedit_create_txt=1', '-c', 'tessedit_create_tsv=1']]
        logs = []
        for command in commands:
            run = subprocess.run(command, env=env, capture_output=True, check=True)
            logs.append({'command': [v.replace(str(root), 'ROOT').replace(str(out), 'OUTPUT') for v in command], 'exit_status': run.returncode, 'stdout': run.stdout.decode(), 'stderr': run.stderr.decode()})
        for suffix, expected in block['outputs'].items():
            assert digest(stem.with_suffix('.'+suffix).read_bytes()) == expected, (block['id'],suffix)
        receipts.append({'id':block['id'], 'commands':logs,'outputs':block['outputs']})
    parent = inputs['parent_text']
    result, cursor, intervals = [], 0, []
    for edit in recipe['edits']:
        a,b = edit['parent_byte_range']
        assert cursor <= a <= b <= len(parent)
        assert digest(parent[a:b]) == edit['removed_sha256']
        unchanged = parent[cursor:a]
        result.append(unchanged)
        replacement = b''
        for selection in edit['raw_selections']:
            data = (out / (selection['block']+'.txt')).read_bytes()
            start,end = selection['byte_range']
            assert 0 <= start < end <= len(data)
            part = data[start:end]
            assert digest(part) == selection['sha256']
            replacement += part
        assert digest(replacement) == edit['inserted_sha256']
        result.append(replacement)
        intervals.append({'parent_byte_range':[a,b], 'output_byte_range':[sum(map(len,result[:-1])),sum(map(len,result))], 'removed_sha256':digest(parent[a:b]),'inserted_sha256':digest(replacement),'unchanged_parent_byte_range':[cursor,a],'unchanged_sha256':digest(unchanged)})
        cursor = b
    result.append(parent[cursor:])
    final = b''.join(result)
    assert digest(final) == recipe['output_sha256']
    (out/'text.txt').write_bytes(final)
    report = {'status':'pass','recipe_sha256':digest(args.recipe.read_bytes()),'implementation_sha256':digest(Path(__file__).read_bytes()),'parent_sha256':digest(parent),'source_sha256':digest(final),'source_bytes':len(final),'edits':intervals,'unchanged_suffix_parent_byte_range':[cursor,len(parent)],'unchanged_suffix_sha256':digest(parent[cursor:]),'all_parent_bytes_outside_declared_ranges_retained_exactly':True,'blocks':receipts,'limitation':'Bounded OCR protocol recovery only; unselected OCR bytes are not source corrections. This replay and PDF fidelity do not establish body-wide source accuracy or independent cold acceptance.'}
    (out/'replay-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','source_sha256','source_bytes','all_parent_bytes_outside_declared_ranges_retained_exactly']}))


if __name__ == '__main__':
    main()
