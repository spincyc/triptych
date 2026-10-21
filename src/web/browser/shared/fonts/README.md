# Triptych Punctus Elevatus

This browser fallback contains U+2E4E only, plus `.notdef`; it is not a
replacement text font. The source text remains literal Unicode. CSS limits
both the character range and the reading selectors. The font is served only
through the explicit `tools/public-alpha` browser-asset map; this README and
its recipes are source material and are not published as browser assets.

## Origin and rights

Upstream: https://github.com/psb1558/Junicode-font
Commit: `180ce3c94bf051f9457422b87e87e9b1cb41107e`, tag `v2.218`.
Input embedded version: `Version 2.003` (distinct from the tag).
Input URL: https://raw.githubusercontent.com/psb1558/Junicode-font/180ce3c94bf051f9457422b87e87e9b1cb41107e/webfiles/JunicodeVF-Roman.woff2
Input WOFF2 SHA-256: `a5838c9ed2cd6eca5a013220932bcddd1825523b85ceb5561393313c754e4639` (1001940 bytes).
Licence URL: https://raw.githubusercontent.com/psb1558/Junicode-font/180ce3c94bf051f9457422b87e87e9b1cb41107e/OFL.txt
Verbatim licence SHA-256: `6078ed582d53a416f761fd2fdeb384320b69191bf316234c21aabe71e2416822`.
Font copyright: © 1998–2023 Peter S. Baker. Licence-file copyright: © 2025 Peter S. Baker.
SIL Open Font License 1.1; no Reserved Font Names are specified.
See the adjacent verbatim `OFL-Junicode.txt`; the font remains under that licence.

## Derivative identity

Family: `Triptych Punctus Elevatus`; full name: `Triptych Punctus Elevatus Regular`;
PostScript name: `TriptychPunctusElevatus-Regular`.
Names 1/3/4/6 are renamed; description 10 identifies the modification.
Copyright 0, version 5, licence 13 and licence URL 14 remain byte-identical.
All variable axes are pinned to upstream defaults, then only U+2E4E is retained.
The upstream glyph outline and advance are unchanged; the derivative has no
cmap entry for Latin, e-cauda or other ordinary text.
Final WOFF2: 1536 bytes; SHA-256 `93fdffe7318755b04f77de90b1bec035513b60a8c4315369344ea9aee9b4abac`.
Intermediate renamed TTF: 3044 bytes; SHA-256 `4b9038dd22c923a612a888e3729889a138dbba807c76e27a1650f19faddad872`.

## Deterministic recipe

Validated with Python 3.14.8, HarfBuzz 14.6.0 and system `woff2_decompress` /
`woff2_compress` (woff2 1.0.2). No font installation, Python package or source
text transformation is required. Run in a fresh repository `.scratch` directory;
all intermediate output belongs there. First download the two pinned input URLs
above and confirm their hashes. Decompress the WOFF2 with `woff2_decompress
JunicodeVF-Roman.woff2`. The decompressed TTF SHA-256 must be
`dee372223b0124472d7bd2076c8ad2e71d137f667785a4a784b1ff26d08145dc`.
Save the following as `subset_font_v2.py` beside that TTF and run it; the
resulting subset TTF SHA-256 must be
`41cc9dd5840bb24c8c1abb375e33cc1d2f3f36b5d657903f5062d574f86f5484`.

```python
"""Create a static U+2E4E-only research subset without installing tools/fonts."""
import ctypes as C,hashlib,json
from pathlib import Path
P=Path(__file__).resolve().parent
hb=C.CDLL('/usr/lib/libharfbuzz.so.0');sub=C.CDLL('/usr/lib/libharfbuzz-subset.so.0')
def fn(lib,name,restype,*args):
 f=getattr(lib,name);f.restype=restype;f.argtypes=list(args);return f
blob_file=fn(hb,'hb_blob_create_from_file_or_fail',C.c_void_p,C.c_char_p)
face_create=fn(hb,'hb_face_create',C.c_void_p,C.c_void_p,C.c_uint)
input_create=fn(sub,'hb_subset_input_create_or_fail',C.c_void_p)
unicode_set=fn(sub,'hb_subset_input_unicode_set',C.c_void_p,C.c_void_p)
set_add=fn(hb,'hb_set_add',None,C.c_void_p,C.c_uint)
pin_axes=fn(sub,'hb_subset_input_pin_all_axes_to_default',C.c_int,C.c_void_p,C.c_void_p)
subset=fn(sub,'hb_subset_or_fail',C.c_void_p,C.c_void_p,C.c_void_p)
face_blob=fn(hb,'hb_face_reference_blob',C.c_void_p,C.c_void_p)
blob_data=fn(hb,'hb_blob_get_data',C.c_void_p,C.c_void_p,C.POINTER(C.c_uint))
version=fn(hb,'hb_version_string',C.c_char_p)
blob=blob_file(str(P/'JunicodeVF-Roman.ttf').encode());assert blob
face=face_create(blob,0);assert face
cfg=input_create();assert cfg
set_add(unicode_set(cfg),0x2e4e)
name_set=fn(sub,'hb_subset_input_set',C.c_void_p,C.c_void_p,C.c_int)(cfg,4)
for name_id in [0,13,14]:set_add(name_set,name_id)
assert pin_axes(cfg,face)
result=subset(face,cfg);assert result
output_blob=face_blob(result);length=C.c_uint();pointer=blob_data(output_blob,C.byref(length));assert pointer and length.value
raw=C.string_at(pointer,length.value);out=P/'triptych-punctus-elevatus-v2.ttf';assert not out.exists();out.write_bytes(raw)
metadata={'method':'HarfBuzz subset CAPI through Python ctypes; no new package or global font changes.','harfbuzz_version':version().decode(),'input_sha256':hashlib.sha256((P/'JunicodeVF-Roman.ttf').read_bytes()).hexdigest(),'unicode_set':['U+2E4E'],'axes':'All variable axes pinned to upstream defaults.','output_file':str(out),'output_sha256':hashlib.sha256(raw).hexdigest(),'output_bytes':len(raw),'license':'SIL OFL 1.1; upstream copyright/licence retained; no Reserved Font Names specified.'}
(P/'subset-generation-v2.json').write_text(json.dumps(metadata,indent=2)+'\n');print(json.dumps(metadata))
```

Save the following as `rename_sfnt.py`, then run:

```sh
python3 rename_sfnt.py --input triptych-punctus-elevatus-v2.ttf --license OFL-Junicode.txt --out renamed
woff2_compress renamed/triptych-punctus-elevatus.ttf
```

Confirm the final TTF and WOFF2 hashes above before replacing any asset.

```python
#!/usr/bin/env python3
"""Deterministically rename the pinned two-glyph Junicode derivative.

Only SFNT name-table data, its directory checksum/length, and the required
head.checkSumAdjustment are changed. No font package or network is used.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct

INPUT_SHA256 = '41cc9dd5840bb24c8c1abb375e33cc1d2f3f36b5d657903f5062d574f86f5484'
LICENSE_SHA256 = '6078ed582d53a416f761fd2fdeb384320b69191bf316234c21aabe71e2416822'
FAMILY = 'Triptych Punctus Elevatus'
POSTSCRIPT = 'TriptychPunctusElevatus-Regular'
DESCRIPTION = ('Modified single-glyph subset of Junicode VF Regular, Version 2.003, '
               'with upstream variable axes pinned to their defaults. '
               'Renamed Triptych Punctus Elevatus. The retained character is U+2E4E. '
               'Upstream copyright and SIL Open Font License 1.1 remain unchanged.')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def checksum(data):
    padded = bytes(data) + b'\0' * (-len(data) % 4)
    return sum(struct.unpack('>' + 'I' * (len(padded) // 4), padded)) & 0xffffffff

def rename(source):
    if sha(source) != INPUT_SHA256:
        raise ValueError('input is not the pinned subset')
    if checksum(source) != 0xb1b0afba:
        raise ValueError('input whole-font checksum is invalid')
    count = struct.unpack_from('>H', source, 4)[0]
    tables = {}
    for i in range(count):
        at = 12 + i * 16
        tag, stored, offset, length = struct.unpack_from('>4sIII', source, at)
        data = bytearray(source[offset:offset + length])
        if tag == b'head':
            data[8:12] = bytes(4)
        if checksum(data) != stored:
            raise ValueError('invalid input table checksum: ' + tag.decode('ascii'))
        tables[tag] = (at, offset, length)
    entry, start, old_length = tables[b'name']
    if any(offset > start for _, offset, _ in tables.values()):
        raise ValueError('recipe requires the pinned name table to be last')
    old = source[start:start + old_length]
    fmt, records, storage = struct.unpack_from('>HHH', old)
    if fmt != 0:
        raise ValueError('recipe requires the pinned format-0 name table')
    names = []
    for i in range(records):
        platform, encoding, language, name_id, length, offset = struct.unpack_from('>HHHHHH', old, 6 + 12 * i)
        if (platform, encoding, language) != (3, 1, 0x409):
            raise ValueError('unexpected name platform/encoding/language')
        value = old[storage + offset:storage + offset + length]
        replacement = {1: FAMILY, 3: '2.003;NONE;' + POSTSCRIPT,
                       4: FAMILY + ' Regular', 6: POSTSCRIPT}.get(name_id)
        if replacement is not None:
            value = replacement.encode('utf-16-be')
        names.append((platform, encoding, language, name_id, value))
    if any(row[3] == 10 for row in names):
        raise ValueError('input unexpectedly already contains description metadata')
    names.append((3, 1, 0x409, 10, DESCRIPTION.encode('utf-16-be')))
    names.sort(key=lambda row: row[:4])
    strings = bytearray()
    strings_at = {}
    name_records = bytearray()
    for platform, encoding, language, name_id, value in names:
        if value not in strings_at:
            strings_at[value] = len(strings)
            strings.extend(value)
        name_records.extend(struct.pack('>HHHHHH', platform, encoding, language, name_id,
                                        len(value), strings_at[value]))
    name = struct.pack('>HHH', 0, len(names), 6 + 12 * len(names)) + name_records + strings
    result = bytearray(source[:start]) + name
    result.extend(b'\0' * (-len(result) % 4))
    # Keep every existing table offset and all directory records except name.
    struct.pack_into('>I', result, entry + 4, checksum(name))
    struct.pack_into('>I', result, entry + 12, len(name))
    head_at = tables[b'head'][1]
    result[head_at + 8:head_at + 12] = bytes(4)
    struct.pack_into('>I', result, head_at + 8, (0xb1b0afba - checksum(result)) & 0xffffffff)
    if checksum(result) != 0xb1b0afba:
        raise ValueError('output whole-font checksum did not settle')
    return bytes(result)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--license', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True, help='fresh output directory')
    args = parser.parse_args()
    source, license_data = args.input.read_bytes(), args.license.read_bytes()
    if sha(license_data) != LICENSE_SHA256:
        raise ValueError('license is not the pinned upstream OFL file')
    output = rename(source)
    args.out.mkdir()
    (args.out / 'triptych-punctus-elevatus.ttf').write_bytes(output)
    (args.out / 'OFL-Junicode.txt').write_bytes(license_data)
    receipt = {'input_sha256': sha(source), 'output_sha256': sha(output), 'output_bytes': len(output),
               'license_sha256': sha(license_data), 'family': FAMILY,
               'full_name': FAMILY + ' Regular', 'postscript_name': POSTSCRIPT,
               'unique_id': '2.003;NONE;' + POSTSCRIPT,
               'source_version_unchanged': 'Version 2.003', 'added_description': DESCRIPTION,
               'changed_name_ids': [1, 3, 4, 6], 'added_name_ids': [10],
               'preserved_origin_license_ids': [0, 5, 13, 14],
               'method': 'Rewrite final SFNT name table; retain other table bytes; recalculate name checksum and head.checkSumAdjustment.'}
    (args.out / 'rename.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))

if __name__ == '__main__':
    main()
```
