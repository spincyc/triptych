import hashlib, json, re
from pathlib import Path
import xml.etree.ElementTree as ET

def sha(data):
    return hashlib.sha256(data).hexdigest()

def lines(data):
    result = data.decode("utf-8").split("\n")
    if result and not result[-1]:
        result.pop()
    return [line.removesuffix("\r") for line in result]

def page_map(ocr, xml_path, labels):
    """Compare every token; never join page maps by array position."""
    raw = lines(ocr)
    tokens,token_lines = [],[]
    for number,line in enumerate(raw,1):
        words = line.split()
        tokens.extend(words)
        token_lines.extend([number]*len(words))
    label_map = {int(p["leafNum"]):p for p in labels["pages"]}
    pages,cursor = [],0
    for _,obj in ET.iterparse(xml_path,events=("end",)):
        if obj.tag != "OBJECT":
            continue
        match = re.search(r"_(\d+)\.djvu$",obj.get("usemap",""))
        if not match:
            raise ValueError("XML OBJECT has no explicit leaf identifier")
        leaf,width,height = int(match[1]),int(obj.get("width")),int(obj.get("height"))
        words = [part for word in obj.iter("WORD") for part in "".join(word.itertext()).split()]
        stop = cursor+len(words)
        if tokens[cursor:stop] != words:
            raise ValueError(f"TXT/XML token mismatch at leaf {leaf}")
        sequence,wide = [],[]
        for line in obj.iter("LINE"):
            boxes = [list(map(int,word.get("coords").split(","))) for word in line.iter("WORD") if word.get("coords")]
            if not boxes:
                continue
            x0,x1 = min(b[0] for b in boxes),max(b[2] for b in boxes)
            y0,y1 = min(min(b[1],b[3]) for b in boxes),max(max(b[1],b[3]) for b in boxes)
            # Full-width headers and very narrow marginal notes do not define
            # body-column order. Wide tables remain conservatively suspect.
            if y0 < height*.10 or y1 > height*.93 or x1-x0 < width*.17:
                continue
            if x1-x0 > width*.55:
                wide.append([x0,y0,x1,y1])
                continue
            side = "L" if (x0+x1)/2 < width*.47 else "R"
            if not sequence or sequence[-1] != side:
                sequence.append(side)
        reasons = []
        if wide:
            reasons.append("wide-body-lines-cross-columns-or-tables")
        if "R" in sequence and "L" in sequence[sequence.index("R")+1:]:
            reasons.append("body-column-order-reverses")
        pages.append({"artifact_page":len(pages)+1,"leaf":leaf,"tokens":len(words),
            "physical_line_start":token_lines[cursor] if stop>cursor else None,
            "physical_line_end":token_lines[stop-1] if stop>cursor else None,
            "source_page_label_raw":label_map.get(leaf,{}).get("pageNumber"),
            "layout_hold_reasons":reasons,"body_column_sequence":sequence,"wide_body_line_count":len(wide)})
        cursor=stop
        obj.clear()
    if cursor != len(tokens):
        raise ValueError("XML does not account for every TXT token")
    return {"schema":"triptych-bullarium-line-map/v1","method":"exact-whitespace-token-equality-v1",
        "ocr_sha256":sha(ocr),"xml_sha256":sha(xml_path.read_bytes()),"physical_line_count":len(raw),
        "token_count":cursor,"pagination":"Leaf IDs are exact XML filename suffixes. Automated page labels are unverified; blank separator lines are unmapped.",
        "layout":"A conservative geometry screen finds some column-order defects; passing it does not establish reading order.","pages":pages}

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--ocr", required=True, type=Path)
    p.add_argument("--xml", required=True, type=Path)
    p.add_argument("--labels", type=Path)
    p.add_argument("--recipe-id", required=True)
    p.add_argument("--out", required=True, type=Path)
    a = p.parse_args()
    labels = json.loads(a.labels.read_text()) if a.labels else {"pages": []}
    result = page_map(a.ocr.read_bytes(), a.xml, labels)
    digest = sha(Path(__file__).read_bytes())
    if not a.recipe_id.endswith(".recipe-" + digest[:12]):
        raise ValueError("recipe artifact ID does not identify these exact bytes")
    result["replay_recipe_artifact_id"] = a.recipe_id
    result["replay_recipe_sha256"] = digest
    result["source_inputs"] = {"ocr": "ocr.txt"}
    if a.labels:
        result["source_inputs"]["labels"] = "page_numbers.json"
    a.out.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
