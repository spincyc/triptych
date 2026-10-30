#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Replay the bounded Ex aliis OCR byte composition without authored text."""
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--recipe', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    recipe = json.loads(args.recipe.read_text())
    root, out = args.root.resolve(), args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    for tool, pin in recipe['tools'].items():
        run = subprocess.run([pin['executable'], pin['version_argument']], capture_output=True, check=True)
        assert run.stdout.decode().splitlines()[0] == pin['version_line'], tool
        assert sha(Path(pin['executable']).read_bytes()) == pin['sha256'], tool
    assert sha(Path(__file__).read_bytes()) == recipe['implementation']['sha256']
    inputs = {}
    for name, pin in recipe['inputs'].items():
        data = (root / pin['path']).read_bytes()
        assert sha(data) == pin['sha256'], name
        assert len(data) == pin['byte_size'], name
        inputs[name] = data
    images, models = out / 'images', out / 'tessdata'
    images.mkdir()
    models.mkdir()
    for group, target in [('images', images), ('models', models)]:
        pin = recipe['inputs'][group]
        with zipfile.ZipFile(root / pin['path']) as package:
            for member in recipe['members'][group]:
                data = package.read(member['name'])
                assert sha(data) == member['sha256']
                (target / Path(member['name']).name).write_bytes(data)
    receipts = []
    env = dict(os.environ, OMP_THREAD_LIMIT='1')
    for block in recipe['blocks']:
        stem = out / block['id']
        x, y, w, h = block['crop_xywh']
        command = [recipe['tools']['magick']['executable'], str(images / block['image_member']),
                   '-crop', f'{w}x{h}+{x}+{y}', '+repage', '-colorspace', 'Gray', '-depth', '8']
        command += block['processing']
        command += ['-bordercolor', 'white', '-border', str(block['border']), '-strip', str(stem.with_suffix('.png'))]
        commands = [command, [recipe['tools']['tesseract']['executable'], str(stem.with_suffix('.png')), str(stem),
                    '-l', block['language'], '--tessdata-dir', str(models), '--oem', '1', '--psm', str(block['psm']),
                    '-c', 'tessedit_create_tsv=1', '-c', 'tessedit_create_txt=1']]
        logs = []
        for command in commands:
            run = subprocess.run(command, env=env, capture_output=True, check=True)
            logs.append({'command': [v.replace(str(out), 'OUTPUT') for v in command],
                         'exit_status': run.returncode, 'stdout': run.stdout.decode(), 'stderr': run.stderr.decode()})
        payloads = {suffix: stem.with_suffix('.' + suffix).read_bytes() for suffix in ['png', 'txt', 'tsv']}
        receipts.append({'id': block['id'], 'commands': logs,
                         'outputs': {suffix: {'sha256': sha(data), 'byte_size': len(data)} for suffix, data in payloads.items()}})
    parent = inputs['parent_text']
    result, cursor, slices = [], 0, []
    for splice in recipe['composition']['splices']:
        a, b = splice['parent_byte_range']
        assert cursor <= a < b <= len(parent)
        assert sha(parent[a:b]) == splice['removed_sha256']
        result.append(parent[cursor:a])
        data = (out / splice['raw_txt']).read_bytes()
        start, stop = splice['raw_byte_range']
        replacement = data[start:stop]
        assert sha(replacement) == splice['inserted_sha256']
        result.append(replacement)
        slices.append({'parent_range': [a, b], 'raw_range': [start, stop],
                       'retained_prefix_sha256': sha(parent[cursor:a]), 'inserted_sha256': sha(replacement)})
        cursor = b
    result.append(parent[cursor:])
    body = b''.join(result)
    assert sha(body) == recipe['composition']['output_sha256']
    (out / 'ex-aliis.txt').write_bytes(body)
    (out / 'receipt.json').write_text(json.dumps({'recipe_sha256': sha(args.recipe.read_bytes()),
        'script_sha256': sha(Path(__file__).read_bytes()), 'blocks': receipts,
        'composition': {'splices': slices, 'retained_suffix_sha256': sha(parent[cursor:]),
                        'output_sha256': sha(body), 'output_byte_size': len(body)}}, indent=2) + '\n')
    print(json.dumps({'blocks': len(receipts), 'splices': len(slices), 'source_sha256': sha(body)}))


if __name__ == '__main__':
    main()
