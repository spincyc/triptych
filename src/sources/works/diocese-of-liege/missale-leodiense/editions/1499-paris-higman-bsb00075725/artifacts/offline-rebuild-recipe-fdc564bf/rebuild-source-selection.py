#!/usr/bin/env python3
"""Rebuild the exact Liège selected-source ZIP from retained PDF JPEG streams.

Requires Python 3 and Poppler's pdfimages. No network access is used.
The expected SHA-256 is the remote parent artifact manifest's sha256 value.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def write_zip(output, members):
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_STORED) as archive:
        archive.comment = b''
        for name, raw in sorted(members.items()):
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = 0o100644 << 16
            info.extra = b''
            info.comment = b''
            archive.writestr(info, raw)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf', required=True, type=Path)
    parser.add_argument('--index', required=True, type=Path)
    parser.add_argument('--manifest', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--expect-sha', required=True)
    args = parser.parse_args()
    index_raw = args.index.read_bytes()
    index = json.loads(index_raw)
    manifest_raw = args.manifest.read_bytes()
    assert sha256(args.pdf.read_bytes()) == index['retained_pdf']['sha256']
    assert sha256(manifest_raw) == index['holding_library_manifest']['sha256']
    assert shutil.which('pdfimages'), 'Poppler pdfimages is required'
    with tempfile.TemporaryDirectory(dir=args.output.parent) as temporary:
        prefix = Path(temporary) / 'image'
        subprocess.run(['pdfimages', '-j', str(args.pdf), str(prefix)], check=True)
        extracted = sorted(Path(temporary).glob('image-*.jpg'))
        assert len(extracted) == len(index['pages']) == 40
        members = {'sequence.json': index_raw, 'support/iiif-manifest.json': manifest_raw}
        for file, page in zip(extracted, index['pages']):
            raw = file.read_bytes()
            assert sha256(raw) == page['sha256'], page['member']
            assert len(raw) == page['byte_size'], page['member']
            members[page['member']] = raw
        write_zip(args.output, members)
    result = sha256(args.output.read_bytes())
    assert result == args.expect_sha, (result, args.expect_sha)
    print(json.dumps({'sha256': result, 'byte_size': args.output.stat().st_size, 'exact_source_images': 40, 'network_used': False}))


if __name__ == '__main__':
    main()
