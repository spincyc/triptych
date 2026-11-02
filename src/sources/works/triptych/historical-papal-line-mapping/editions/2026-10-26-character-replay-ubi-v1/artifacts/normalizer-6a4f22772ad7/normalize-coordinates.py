"""Replay only nominated five-to-four-coordinate XML attribute projections."""
import argparse
import hashlib
from pathlib import Path
import re

def normalize(data):
    chunks = []
    cursor = 0
    for match in re.finditer(rb'<OBJECT\b.*?</OBJECT>', data, re.S):
        header = match[0].split(b'>', 1)[0]
        leaf_match = re.search(rb'usemap="[^"]*_(\d+)\.djvu"', header)
        if not leaf_match or int(leaf_match[1]) not in {26, 27, 28}:
            continue
        def project(word):
            fields = word[2].split(b',')
            if len(fields) != 5 or any(not re.fullmatch(rb'-?\d+', value) for value in fields):
                raise ValueError('nominated source WORD does not carry exactly five integer coordinates')
            return word[1] + b','.join(fields[:4]) + word[3]
        replacement, count = re.subn(rb'(<WORD\b[^>]*\bcoords=")([0-9,-]+)(")', project, match[0])
        if count == 0:
            raise ValueError('nominated page contains no projected WORD attributes')
        chunks.extend([data[cursor:match.start()], replacement])
        cursor = match.end()
    chunks.append(data[cursor:])
    return b''.join(chunks)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--xml', required=True, type=Path)
    parser.add_argument('--xml-sha256', required=True)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    source = args.xml.read_bytes()
    if hashlib.sha256(source).hexdigest() != args.xml_sha256:
        raise ValueError('original whole source XML hash differs')
    args.out.write_bytes(normalize(source))
