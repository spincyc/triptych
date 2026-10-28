import hashlib, io
from pathlib import Path
import xml.etree.ElementTree as ET

def xml_word_line_text(xml_bytes: bytes) -> bytes:
    """Serialize every exact native WORD once, without inferring reading order."""
    output, expected = [], []

    def add_line(words):
        if words:
            output.append(" ".join(words))

    def walk(node):
        if node.tag == "LINE":
            add_line([token for word in node.iter("WORD") for token in "".join(word.itertext()).split()])
            return
        if node.tag == "WORD":
            add_line("".join(node.itertext()).split())
            return
        for child in node:
            walk(child)
        if node.tag in ("PARAGRAPH", "OBJECT"):
            output.append("")

    for _, obj in ET.iterparse(io.BytesIO(xml_bytes), events=("end",)):
        if obj.tag == "OBJECT":
            expected.extend(token for word in obj.iter("WORD") for token in "".join(word.itertext()).split())
            walk(obj)
            obj.clear()
    if not expected:
        raise ValueError("XML text serialization needs a nonempty native OBJECT/WORD stream")
    payload = ("\n".join(output) + "\n").encode("utf-8")
    if payload.decode("utf-8").split() != expected:
        raise ValueError("XML serialization does not preserve every native WORD token exactly once")
    return payload

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--xml", required=True, type=Path)
    p.add_argument("--xml-sha256", required=True)
    p.add_argument("--out", required=True, type=Path)
    a = p.parse_args()
    payload = a.xml.read_bytes()
    if hashlib.sha256(payload).hexdigest() != a.xml_sha256:
        raise ValueError("whole XML differs from its pinned SHA-256")
    a.out.write_bytes(xml_word_line_text(payload))
