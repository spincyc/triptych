#!/usr/bin/env python3
"""Retain the original printed page images of Pii IX Acta I/3, pp.687–717.

MIT-licensed project-created extraction recipe. Source images retain their own
rights; this script grants no rights in input PDFs or their modern wrappers.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import zlib

SOURCE_SHA256 = '7ce7f56c91dfeea894474e2bb30be573eab1aab355cced00db5a3d4906f3123d'
FIRST, LAST = 697, 727
ALLOWED_DIMENSIONS = {(3376, 5262), (3358, 5254)}
DPI = 600


def original_images(source, scratch):
    listing = subprocess.run(['pdfimages', '-f', str(FIRST), '-l', str(LAST),
                              '-list', str(source)], check=True, capture_output=True,
                             text=True).stdout
    selected = []
    for line in listing.splitlines():
        fields = line.split()
        if len(fields) > 7 and fields[0].isdigit() and fields[2] == 'image':
            width, height = int(fields[3]), int(fields[4])
            if (width, height) in ALLOWED_DIMENSIONS:
                selected.append((int(fields[0]), int(fields[1]), width, height))
    if [page for page, *_ in selected] != list(range(FIRST, LAST + 1)):
        raise ValueError('expected exactly one historical full-page image on each selected page')
    with tempfile.TemporaryDirectory(prefix='papal-native-pages-', dir=scratch) as temporary:
        prefix = Path(temporary) / 'image'
        subprocess.run(['pdfimages', '-f', str(FIRST), '-l', str(LAST),
                        '-j', str(source), str(prefix)], check=True)
        result = []
        for page, ordinal, width, height in selected:
            payload = prefix.with_name(f'image-{ordinal:03}.pbm').read_bytes()
            header = re.match(br'P4\s+(\d+)\s+(\d+)\n', payload)
            if not header or tuple(map(int, header.groups())) != (width, height):
                raise ValueError('unexpected native historical image representation')
            bits = payload[header.end():]
            if len(bits) != ((width + 7) // 8) * height:
                raise ValueError('truncated historical image bitstream')
            result.append((page, width, height, bits))
        return result


def pdf_bytes(images):
    objects = [b'', b'<< /Type /Catalog /Pages 2 0 R >>', b'']
    kids = []
    for page, width, height, pixels in images:
        width_pt, height_pt = width * 72 / DPI, height * 72 / DPI
        page_id, image_id, content_id = len(objects), len(objects) + 1, len(objects) + 2
        kids.append(f'{page_id} 0 R')
        objects.append((f'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {width_pt:.4f} {height_pt:.4f}] '
                        f'/Resources << /XObject << /Im0 {image_id} 0 R >> >> '
                        f'/Contents {content_id} 0 R >>').encode('ascii'))
        data = zlib.compress(pixels, level=9)
        objects.append((f'<< /Type /XObject /Subtype /Image /Width {width} /Height {height} '
                        '/ColorSpace /DeviceGray /BitsPerComponent 1 /Decode [1 0] '
                        f'/Filter /FlateDecode /Length {len(data)} >>\nstream\n').encode('ascii')
                       + data + b'\nendstream')
        content = f'q {width_pt:.4f} 0 0 {height_pt:.4f} 0 0 cm /Im0 Do Q\n'.encode('ascii')
        objects.append(f'<< /Length {len(content)} >>\nstream\n'.encode('ascii') + content + b'endstream')
    objects[2] = f'<< /Type /Pages /Kids [{" ".join(kids)}] /Count {len(images)} >>'.encode('ascii')
    output = bytearray(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n')
    offsets = [0]
    for ordinal, value in enumerate(objects[1:], 1):
        offsets.append(len(output))
        output += f'{ordinal} 0 obj\n'.encode('ascii') + value + b'\nendobj\n'
    xref = len(output)
    output += f'xref\n0 {len(objects)}\n0000000000 65535 f \n'.encode('ascii')
    for offset in offsets[1:]:
        output += f'{offset:010} 00000 n \n'.encode('ascii')
    output += f'trailer\n<< /Size {len(objects)} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n'.encode('ascii')
    return bytes(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_pdf', type=Path)
    parser.add_argument('output_pdf', type=Path)
    parser.add_argument('--receipt', type=Path, required=True)
    parser.add_argument('--scratch', type=Path, required=True, help='owned transient directory')
    args = parser.parse_args()
    source_hash = hashlib.sha256(args.source_pdf.read_bytes()).hexdigest()
    if source_hash != SOURCE_SHA256:
        raise ValueError('source PDF does not match the reviewed exact witness')
    args.scratch.mkdir(parents=True, exist_ok=True)
    images = original_images(args.source_pdf, args.scratch)
    data = pdf_bytes(images)
    args.output_pdf.parent.mkdir(parents=True, exist_ok=True)
    args.output_pdf.write_bytes(data)
    receipt = {'source_sha256': source_hash, 'artifact_pages': [FIRST, LAST],
               'printed_pages': [687, 717], 'pages': len(images),
               'bits_per_component': 1,
               'dpi': DPI, 'output_sha256': hashlib.sha256(data).hexdigest(),
               'output_byte_size': len(data),
               'method': 'Extract the one native historical image per page (3376x5262 or 3358x5254). Omit the separate Google watermark image/mask objects. Preserve all historical image bits without crop or resampling. Repackage those bits in ordered PDF image streams using lossless Flate compression and an explicit inverted gray decode for PBM polarity.',
               'page_image_sha256': [{'artifact_page': page, 'printed_page': page - 10,
                                     'width': width, 'height': height,
                                     'sha256': hashlib.sha256(bits).hexdigest()}
                                    for page, width, height, bits in images]}
    args.receipt.write_text(json.dumps(receipt, sort_keys=True, indent=2) + '\n')
    print(json.dumps({'pages': len(images), 'bytes': len(data), 'sha256': receipt['output_sha256']}))


if __name__ == '__main__':
    main()
