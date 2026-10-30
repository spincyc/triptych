#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Replay one exact image-note OCR and localized byte composition."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import zipfile


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--recipe', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    recipe = json.loads(args.recipe.read_text())
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    for name, item in recipe['tools'].items():
        assert sha(Path(item['path']).read_bytes()) == item['sha256'], name
    def read_input(name):
        item = recipe['inputs'][name]
        data = (root / item['path']).read_bytes()
        assert sha(data) == item['sha256'], name
        return data
    for name in recipe['inputs']:
        read_input(name)
    models = out / 'models'
    models.mkdir()
    with zipfile.ZipFile(root / recipe['inputs']['models']['path']) as archive:
        for language, item in recipe['models'].items():
            data = archive.read(item['member'])
            assert sha(data) == item['sha256']
            (models / item['member']).write_bytes(data)
    with zipfile.ZipFile(root / recipe['inputs']['images']['path']) as archive:
        data = archive.read(recipe['image']['member'])
        assert sha(data) == recipe['image']['sha256']
        native = out / 'native.jpg'
        native.write_bytes(data)
    receipts = []
    environment = dict(os.environ, OMP_THREAD_LIMIT='1')
    for mode in recipe['modes']:
        image = out / (mode['id'] + '.png')
        x, y, width, height = recipe['crop_xywh']
        command = [recipe['tools']['magick']['path'], str(native), '-crop',
                   f'{width}x{height}+{x}+{y}', '+repage', '-colorspace', 'Gray', '-depth', '8']
        if 'threshold' in mode:
            command += ['-threshold', mode['threshold']]
        command += ['-units', 'PixelsPerInch', '-density', '300', '-strip', str(image)]
        subprocess.run(command, capture_output=True, check=True, env=environment)
        for language in recipe['models']:
            for psm in recipe['psm']:
                stem = out / f"{mode['id']}-{language}-{psm}"
                command = [recipe['tools']['tesseract']['path'], str(image), str(stem),
                           '--tessdata-dir', str(models), '-l', language, '--oem', '1',
                           '--psm', str(psm), '-c', 'tessedit_create_txt=1',
                           '-c', 'tessedit_create_tsv=1']
                process = subprocess.run(command, capture_output=True, check=True, env=environment)
                receipts.append({'id': stem.name, 'returncode': process.returncode,
                                 'stdout': process.stdout.decode(), 'stderr': process.stderr.decode(),
                                 'txt_sha256': sha(stem.with_suffix('.txt').read_bytes()),
                                 'tsv_sha256': sha(stem.with_suffix('.tsv').read_bytes())})
    parent = read_input('parent_text')
    replacement = (out / recipe['selected_raw_member']).read_bytes().strip()
    start, end = recipe['composition']['parent_byte_range_half_open']
    assert sha(parent[start:end]) == recipe['composition']['removed_span_sha256']
    assert sha(replacement) == recipe['composition']['replacement_span_sha256']
    combined = parent[:start] + replacement + parent[end:]
    assert sha(combined) == recipe['composition']['output_sha256']
    (out / 'nemo.txt').write_bytes(combined)
    receipt = {'recipe_sha256': sha(args.recipe.read_bytes()),
               'script_sha256': sha(Path(__file__).read_bytes()),
               'raw': receipts, 'output_sha256': sha(combined),
               'prefix_byte_identity': combined[:start] == parent[:start],
               'suffix_byte_identity': combined[start + len(replacement):] == parent[end:]}
    (out / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'output_sha256': sha(combined), 'raw_outputs': len(receipts)}))


if __name__ == '__main__':
    main()
