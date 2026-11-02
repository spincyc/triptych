"""Whole-byte Bullarium acquisition and conservative raw-line reconstruction."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tomllib
import urllib.request
import xml.etree.ElementTree as ET

from _tooling import examples_live_on_the_verbs, with_examples

ROOT = Path(__file__).resolve().parents[1]
CATALOG = "src/sources/papal-documents/bullarium-catalog.json"
MANIFEST = "src/sources/papal-documents/bullarium-manifest.json"
FRAGMENT_MANIFEST = "src/sources/papal-documents/bullarium-fragment-manifest.json"
METHOD = "bullarium-raw-line-discovery-v1"
BOUNDS = {1:(2782,96426),2:(1501,115448),3:(236,98909),4:(275,90724),5:(476,98525),6:(826,68217),
    7:(342,119617),8:(350,118313),9:(757,77422),10:(1131,107116),11:(6980,86729),12:(10292,110256),
    13:(6815,88047),14:(12601,101138),15:(8571,99135),16:(6837,95312),17:(7359,100772),18:(8912,87827),
    19:(6502,114638),20:(10094,116534),21:(8896,117319),22:(9068,107749),23:(3579,77220),24:(5567,83550),
    "appendix":(293,83246)}
EXTRA = {1:[2782],2:[1501],7:[342],8:[350],10:[1131],13:[6815],16:[6837],18:[79552],23:[3579,5615]}
TRANSITIONS = {7:[52713],8:[65007],9:[28111,44692,44799,59970,61609],11:[28274,29733],12:[68330],
    15:[46151],17:[65034],20:[28860],21:[106446]}
PROTOCOL = re.compile(r"\b([A-ZÀ-Ý][A-Za-zÀ-ÿ'’]{2,20}(?:[ \t]+[IVXLCDMivxlcdm1]{1,8})?)[ \t\r\n]+([Ee]piscop[A-Za-zÀ-ÿ]{1,8}|[Pp]apa)\b")
NAME_ROOTS = ("leo","greg","alex","inno","clem","clcm","pius","plus","paul","paui","urban","drban","urbann",
    "bened","ioan","ioh","iuli","juli","sixt","sist","felix","felic","gelas","symm","horm","silv","bonif",
    "vigili","pelag","marc","nicol","adri","hadr","pasch","eugen","call","calix","luc","honor","mart",
    "steph","serg","formos","anast","simpli","hilar","zach","coeles","celes")
DATE = re.compile(r"\b(?:Dat(?:um|a|ae|am)?\.?|Datura|Datumque)\b", re.I)
APPENDIX_FILES = {
    "ocr": ("BR%20Tomo%2001-appendix_djvu.txt",1978453,"ddc5888aa6556fd74bb0ed850c8acbad39b22982"),
    "xml": ("BR%20Tomo%2001-appendix_djvu.xml",24593322,"4a3f7a25f9033cfda2c992b3e515c969181973dc"),
    "labels": ("BR%20Tomo%2001-appendix_page_numbers.json",122031,"338aff634f7c04ececf77b7428251b75609d9118")}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def lines(data):
    result = data.decode("utf-8").split("\n")
    if result and not result[-1]:
        result.pop()
    return [line.removesuffix("\r") for line in result]


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_bytes() != data:
        path.write_bytes(data)


def json_bytes(data):
    return (json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2)+"\n").encode()


def durable_review(value):
    """Retain the evidence itself, without dead links to disposable packets."""
    if isinstance(value,dict):
        return {key:durable_review(item) for key,item in value.items()
                if not (isinstance(item,str) and item.startswith(".scratch/"))}
    if isinstance(value,list):
        return [durable_review(item) for item in value]
    return value


def toml_value(value):
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, list):
        return "["+", ".join(toml_value(item) for item in value)+"]"
    raise ValueError("unsupported TOML field")


def record_bytes(data):
    return ("\n".join(f"{key} = {toml_value(value)}" for key,value in data.items())+"\n").encode()


def check_source_write(path, data):
    if path.exists() or path.is_symlink():
        if not path.is_file() or path.read_bytes()!=data:
            raise ValueError("existing source bytes are immutable; an explicitly new source/selection identity is required")
        return True
    return False


def write_source(path, data):
    """Retain source bytes without replacing an existing or concurrent witness."""
    if check_source_write(path,data):
        return
    path.parent.mkdir(parents=True,exist_ok=True)
    try:
        with path.open("xb") as stream:
            stream.write(data)
    except FileExistsError:
        if not check_source_write(path,data):
            raise


def record(path, data):
    write_source(path,record_bytes(data))


def roman(number):
    result = ""
    for value,token in ((1000,"M"),(900,"CM"),(500,"D"),(400,"CD"),(100,"C"),(90,"XC"),(50,"L"),
                        (40,"XL"),(10,"X"),(9,"IX"),(5,"V"),(4,"IV"),(1,"I")):
        count,number = divmod(number,value)
        result += token*count
    return result


def numeral(raw):
    token = "".join("I" if c in "il1!" else c.upper() for c in raw if not c.isspace())
    if not re.fullmatch("[IVXLCDM]+", token):
        return None
    total,prior = 0,0
    for char in reversed(token):
        value = {"I":1,"V":5,"X":10,"L":50,"C":100,"D":500,"M":1000}[char]
        total += -value if value < prior else value
        prior = max(prior,value)
    return total if 0 < total < 4000 and roman(total) == token else None


def heading(value, appendix=False):
    value = value.strip()
    if appendix:
        match = re.fullmatch(r"EPISTOLA\s+([0-9IVXLCDMivxlcdml1]+)[.,*\s]*",value)
        return (match[1], int(match[1]) if match[1].isdigit() else numeral(match[1])) if match else None
    value = re.sub(r"^An[.,]?\s*[^\d]{0,12}[0-9iI:;»]{3,5}\s+", "",value)
    match = re.fullmatch(r"([IVXLCDMivxlcdml1!][IVXLCDMivxlcdml1!\s]{0,18})[.,\-\\]*",value)
    return (match[1].strip(),numeral(match[1])) if match else None


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


def discover(ocr,volume,mapping):
    raw=lines(ocr)
    first,last=BOUNDS[volume]
    candidates=[]
    for number in range(first,min(last,len(raw))+1):
        parsed=heading(raw[number-1],volume=="appendix")
        explicit=number in EXTRA.get(volume,[])
        if not parsed and not explicit:
            continue
        token,integer=parsed or (raw[number-1].strip(),None)
        if (volume,number) in {(1,2782),(7,342),(10,1131)}:
            integer=None
        start=number
        while start<last and not raw[start].strip():
            start+=1
        title=[]
        for value in raw[start:min(start+35,last)]:
            if not value.strip():
                break
            title.append(value.strip())
        title=" ".join(title)
        if not explicit and (len(re.sub("[^A-Za-zÀ-ÿ]","",title))<18 or re.match(r"^(?:§|Cap\.|[0-9]|[IVX]+\.)",title)):
            continue
        proto=None
        window="\n".join(raw[number-1:min(number+240,last)])
        for match in PROTOCOL.finditer(window):
            if match[1].lower().startswith(NAME_ROOTS):
                proto={"raw":" ".join(match[0].split()),"line":number+window[:match.start()].count("\n")}
                break
        if not proto and not explicit and not re.match(r"^(?:De |Declar|Confirm|Constitut|Erect|Privileg|Praecept|Litter|Ad |Quod |Prohib|Facult|Indul)",title):
            continue
        candidates.append({"heading_line":number,"act_number_raw":token,"act_number":integer,
            "title_raw":title or raw[number-1].strip(),"protocol":proto})
    units=[]
    for i,item in enumerate(candidates):
        start=item["heading_line"]
        end=candidates[i+1]["heading_line"]-1 if i+1<len(candidates) else last
        while end>=start and not raw[end-1].strip():
            end-=1
        if item["protocol"] and item["protocol"]["line"]>end:
            item["protocol"]=None
        pages=[p for p in mapping["pages"] if p["physical_line_start"] is not None and p["physical_line_start"]<=end and p["physical_line_end"]>=start]
        dates=[{"line":n,"raw":" ".join(raw[n-1:min(n+5,end)]).strip()} for n in range(start,end+1) if DATE.search(raw[n-1])]
        reasons=["uncollated-ocr-boundaries-and-reading-order"]
        if not item["protocol"]:
            reasons.append("papal-self-attribution-not-established")
        if item["act_number"] is None:
            reasons.append("unreadable-act-number")
        next_number=candidates[i+1]["act_number"] if i+1<len(candidates) else None
        if item["act_number"] is not None and next_number not in {item["act_number"]+1,1}:
            reasons.append("next-number-gap-or-final-extent")
        if any(start<=boundary<=end for boundary in TRANSITIONS.get(volume,[])):
            reasons.append("pontificate-or-subcollection-transition")
        reasons.extend(sorted({reason for p in pages for reason in p["layout_hold_reasons"]}))
        units.append({**item,"id":f"bullarium.{('appendix-01' if volume=='appendix' else f'volume-{volume:02d}')}.unit-{i+1:04d}",
            "volume":volume,"date":None,"date_raw":dates,"physical_line_ranges":[[start,end]],
            "artifact_page_range":[pages[0]["artifact_page"],pages[-1]["artifact_page"]] if pages else None,
            "leaf_bounds":[pages[0]["leaf"],pages[-1]["leaf"]] if pages else None,
            "printed_page_labels_raw":[p["source_page_label_raw"] for p in pages],
            "boundary_evidence":{"next_heading_line":candidates[i+1]["heading_line"] if i+1<len(candidates) else None,
                "next_act_number":next_number,"protocol_search_lines":[start,min(start+240,last)],
                "flagged_pages":[{key:p[key] for key in ("artifact_page","leaf","layout_hold_reasons","body_column_sequence","wide_body_line_count")} for p in pages if p["layout_hold_reasons"]]},
            "status":"held","hold_reasons":reasons})
    return units


def archive_volumes(root):
    data=json.loads((root/"src/sources/papal-documents/archives.json").read_text())
    return {("appendix" if ".appendix-" in v.get("id","") else v["volume"]):v for v in data["volumes"]
            if v.get("series")=="Bullarium Romanum" and v.get("identifier")}


def inputs(root,volume):
    key="appendix" if volume=="appendix" else f"{volume:02d}"
    found=list((root/".scratch/bullarium_reconstruction").glob(f"volumes_*/{key}/ocr.txt"))
    if len(found)>1:
        raise ValueError(f"{key}: duplicate whole acquired inputs")
    directory=found[0].parent if found else root/".scratch/bullarium_reconstruction/acquired"/key
    paths={"ocr":directory/"ocr.txt","xml":directory/"ocr.xml","labels":directory/"page_numbers.json"}
    old=root/CATALOG
    if not found and old.exists():
        entry=next((v for v in json.loads(old.read_text())["volumes"] if v["volume"]==volume),None)
        if entry:
            for kind in ("ocr","labels"):
                manifest=tomllib.loads((root/entry["container"]["artifacts"][kind]["manifest"]).read_text())
                paths[kind]=root/manifest["path"]
    if not all(path.is_file() for path in paths.values()):
        raise ValueError(f"{key}: missing whole OCR/XML/page map")
    return paths


def source_routes(archive,paths):
    result={}
    formats={"ocr":"DjVuTXT","xml":"Djvu XML","labels":"Page Numbers JSON"}
    for key,path in paths.items():
        data=path.read_bytes()
        source=next((d for d in archive.get("downloads",[]) if d.get("source_format")==formats[key]),None)
        if not source:
            filename,size,source_sha1=APPENDIX_FILES[key]
            source={"url":"https://archive.org/download/BR-Tomo-01-appendix/"+filename,
                    "size_bytes":size,"source_declared_sha1":source_sha1}
        if len(data)!=source["size_bytes"] or hashlib.sha1(data).hexdigest()!=source["source_declared_sha1"]:
            raise ValueError("whole acquired bytes differ from source size/SHA1")
        result[key]={"source_url":source["url"],"byte_size":len(data),"sha256":sha(data)}
    return result


def acquire(root,selected):
    archives=archive_volumes(root)
    downloaded,reused,total=0,0,0
    formats={"ocr":"DjVuTXT","xml":"Djvu XML","labels":"Page Numbers JSON"}
    for volume in selected:
        try:
            paths=inputs(root,volume)
        except ValueError:
            key="appendix" if volume=="appendix" else f"{volume:02d}"
            directory=root/".scratch/bullarium_reconstruction/acquired"/key
            paths={"ocr":directory/"ocr.txt","xml":directory/"ocr.xml","labels":directory/"page_numbers.json"}
            if (root/CATALOG).exists():
                entry=next((v for v in json.loads((root/CATALOG).read_text())["volumes"] if v["volume"]==volume),None)
                if entry:
                    for kind in ("ocr","labels"):
                        item=tomllib.loads((root/entry["container"]["artifacts"][kind]["manifest"]).read_text())
                        paths[kind]=root/item["path"]
        for kind,path in paths.items():
            if path.is_file():
                reused+=1
                continue
            if volume=="appendix":
                filename,_,_=APPENDIX_FILES[kind]
                url="https://archive.org/download/BR-Tomo-01-appendix/"+filename
            else:
                url=next(d["url"] for d in archives[volume]["downloads"] if d.get("source_format")==formats[kind])
            request=urllib.request.Request(url,headers={"User-Agent":"Triptych-Bullarium/1 (public historical-source acquisition)"})
            with urllib.request.urlopen(request,timeout=180) as response:
                payload=response.read()
            write_source(path,payload)
            downloaded+=1
        routes=source_routes(archives.get(volume,{}),paths)
        total+=sum(item["byte_size"] for item in routes.values())
    return {"status":"ok","whole_containers":len(selected),"responses_downloaded":downloaded,
            "responses_reused":reused,"whole_response_bytes":total}


def admit(root,review_paths,revision,manifest_path=MANIFEST,fragment_manifest_path=FRAGMENT_MANIFEST,reader_notes=None,*,input_paths=()):
    root=Path(root).resolve()
    review_paths=[Path(path) for path in review_paths]
    manifest_target=(root/manifest_path).resolve()
    fragment_target=(root/fragment_manifest_path).resolve()
    targets=(manifest_target,fragment_target)
    source_records={}
    source_inputs={(root/CATALOG).resolve(),*(path.resolve() for path in review_paths),
        *(Path(path).resolve() for path in input_paths)}
    def aliases(first,second):
        return first==second or (first.exists() and second.exists() and first.samefile(second))
    def check_manifest_targets():
        if any(not target.is_relative_to(root) for target in targets):
            raise ValueError("manifest destinations must remain inside the repository")
        if aliases(*targets):
            raise ValueError("manifest output destinations must be distinct")
        if any(target.is_relative_to((root/"src/sources/works").resolve()) for target in targets):
            raise ValueError("manifest output destinations cannot alias the source-record namespace")
        protected=source_inputs|{path.resolve() for path in source_records}
        if any(aliases(target,path) for target in targets for path in protected):
            raise ValueError("manifest output destination aliases a catalog, source or review input")
    def read_source(path):
        path=Path(path)
        resolved=path.resolve()
        if any(aliases(target,resolved) for target in targets):
            raise ValueError("manifest output destination aliases a catalog, source or review input")
        source_inputs.add(resolved)
        return path.read_bytes()
    check_manifest_targets()
    catalog=json.loads(read_source(root/CATALOG))
    units={u["id"]:u for u in catalog["units"]}
    volumes={v["volume"]:v for v in catalog["volumes"]}
    for volume in volumes.values():
        container=volume["container"]
        if container.get("line_map_path"):
            source_inputs.add((root/container["line_map_path"]).resolve())
        for declaration in container["artifacts"].values():
            source_inputs.add((root/declaration["manifest"]).resolve())
            if declaration.get("line_map_path"):
                source_inputs.add((root/declaration["line_map_path"]).resolve())
    check_manifest_targets()
    existing=json.loads(manifest_target.read_text()) if manifest_target.exists() else {"documents":[]}
    existing_bytes=manifest_target.read_bytes() if manifest_target.exists() else None
    document_index={document["id"]:document for document in existing["documents"]}
    fragment_existing=json.loads(fragment_target.read_text()) if fragment_target.exists() else {"documents":[]}
    fragment_existing_bytes=fragment_target.read_bytes() if fragment_target.exists() else None
    fragment_index={document["id"].removesuffix(".fragment"):document for document in fragment_existing["documents"]}
    old_documents=json.loads(json.dumps(existing["documents"]))
    old_fragments=json.loads(json.dumps(fragment_existing["documents"]))
    for state in (existing,fragment_existing):
        if state.get("revision"):
            for document in state["documents"]:
                document.setdefault("revision",state["revision"])
    seen=set()
    source_cache={}
    reader_notes=reader_notes or {}
    def stage_record(path,data):
        path=path.resolve()
        payload=record_bytes(data)
        check_source_write(path,payload)
        if path in source_records and source_records[path]!=payload:
            raise ValueError("conflicting source registrations require an explicitly new source/selection identity")
        source_records[path]=payload
    def reviewed_child(parent,item,identifier):
        source_id=item.get("source_artifact_id",parent["artifact_id"])
        digest=item.get("artifact_sha256",parent["artifact_sha256"])
        if source_id==parent["artifact_id"]:
            if digest!=parent["artifact_sha256"]:
                raise ValueError("additional discovery changed its controlling source")
        else:
            container=volumes[parent["volume"]]["container"]
            matches=[a for a in container["artifacts"].values() if a["id"]==source_id]
            if len(matches)!=1:
                raise ValueError("source-order child requires a registered volume controller")
            derived=tomllib.loads(read_source(root/matches[0]["manifest"]).decode())
            if (derived["id"]!=source_id or derived["sha256"]!=digest or
                    derived["edition_id"]!=container["edition_id"] or
                    derived.get("derived_from")!=parent["artifact_id"] or
                    derived.get("artifact_type")!="coordinate-reading-order-ocr"):
                raise ValueError("source-order child requires the exact raw parent and volume edition")
        ranges=item["physical_line_ranges"]
        child={**parent,"id":identifier,"parent_unit_id":parent["id"],"status":"held",
            "heading_line":ranges[0][0],"physical_line_ranges":ranges,
            "act_number_raw":item.get("act_number_raw","not recovered"),"act_number":None,
            "artifact_id":source_id,"artifact_sha256":digest}
        child.pop("review",None)
        for field in ("review_history","active_reader_status","reader_withdrawal","active_render_selection",
                      "canonical_identity_resolution","canonical_match_candidates","work_id","edition_id","segment_id","segment_path","extent_kind",
                      "reading_selection_variant_of","prior_reading_selection"):
            child.pop(field,None)
        if source_id!=parent["artifact_id"]:
            child["source_order_parent"]={"unit_id":parent["id"],"artifact_id":parent["artifact_id"],
                "artifact_sha256":parent["artifact_sha256"],"physical_line_ranges":parent["physical_line_ranges"]}
            for field in ("protocol","date_raw","boundary_evidence","line_map_id","artifact_page_range","leaf_bounds","printed_page_labels_raw"):
                child.pop(field,None)
        else:
            child["date_raw"]=[lead for lead in parent.get("date_raw",[]) if type(lead.get("line")) is int
                and any(a<=lead["line"]<=z for a,z in ranges)]
            if parent.get("protocol") and not any(a<=parent["protocol"]["line"]<=z for a,z in ranges):
                child.pop("protocol",None)
        return child
    for path in review_paths:
        review=json.loads(read_source(path))
        if review.get("schema")!="triptych-bullarium-boundary-reviews/v1":
            raise ValueError("unknown boundary review schema")
        pending=list(review["reviews"])+list(review.get("extra_dispositions",[]))
        for item in pending:
            if item["decision"] not in {"admit","fragment","hold","duplicate","non-papal","non-act","split"}:
                raise ValueError("unknown source-review disposition")
            item=durable_review(item)
            overlay=reader_notes.get(item["unit_id"],{})
            for key,value in overlay.items():
                if key=="reader_source_note" and item.get(key) and value not in item[key]:
                    item[key]+=" "+value
                else:
                    item[key]=value
            if item["unit_id"] not in units:
                parent=units.get(item.get("parent_unit_id"))
                if not parent or not re.fullmatch(r"[a-z0-9.-]+",item["unit_id"]):
                    raise ValueError("additional discovery requires its exact cataloged parent")
                unit=reviewed_child(parent,item,item["unit_id"])
                units[unit["id"]]=unit
            else:
                unit=units[item["unit_id"]]
            if unit.get("review") and unit["review"]!=item:
                unit.setdefault("review_history",[]).append(unit["review"])
            if item["decision"]=="split":
                if unit.get("segment_path"):
                    raise ValueError("registered witnesses require a new selection identity; split review cannot replace their source pins")
                if item["artifact_sha256"]!=unit["artifact_sha256"] or not item.get("constituents"):
                    raise ValueError("split requires exact source and reviewed constituents")
                if unit["id"] in document_index:
                    raise ValueError("previously admitted composite requires explicit source reconciliation")
                unit.update({"status":"split-into-constituents","review":item})
                for index,child in enumerate(item["constituents"],1):
                    child_id=unit["id"]+f".part-{index:02d}"
                    child_unit=reviewed_child(unit,child,child_id)
                    registered=units.get(child_id)
                    if registered and registered.get("segment_path"):
                        if any(registered.get(key)!=child_unit.get(key) for key in ("artifact_id","artifact_sha256","physical_line_ranges")):
                            raise ValueError("a split child already has immutable registered source pins")
                    else:
                        units[child_id]=child_unit
                    pending.append({**child,"unit_id":child_id,"artifact_sha256":child_unit["artifact_sha256"],"decision":child.get("decision","admit")})
                continue
            if item["decision"] not in {"admit","fragment"}:
                if item["artifact_sha256"]!=unit["artifact_sha256"]:
                    raise ValueError("held review does not pin exact source")
                if unit.get("segment_path"):
                    raise ValueError("registered reader withdrawals require PDF-pinned withdrawal metadata; historical source records remain immutable")
                document_index.pop(unit["id"],None)
                fragment_index.pop(unit["id"],None)
                unit["review"]=item
                unit["status"]={"duplicate":"duplicate-witness","non-papal":"non-papal-source-unit","non-act":"not-an-independent-act"}.get(item["decision"],"specifically-held")
                continue
            if unit.get("active_reader_status")=="source-order-hold":
                raise ValueError("withdrawn source-order witnesses require a new source/selection identity, not a reader-note override")
            if unit["id"] in seen:
                raise ValueError("duplicate boundary admission")
            seen.add(unit["id"])
            is_fragment=item["decision"]=="fragment"
            if is_fragment and (item.get("extent_kind")!="fragment" or "fragment" not in item["title"].lower()):
                raise ValueError("a fragment requires explicit extent_kind and fragment title")
            if item["artifact_sha256"]!=unit["artifact_sha256"]:
                raise ValueError("boundary review does not pin exact source")
            if not all(isinstance(item.get(k),str) and item[k].strip() for k in ("printed_attribution","title","review_note","reviewed_extent")):
                raise ValueError("incomplete boundary review")
            container=volumes[unit["volume"]]["container"]
            source_id=unit["artifact_id"]
            if source_id not in source_cache:
                matches=[a for a in container["artifacts"].values() if a["id"]==source_id]
                if len(matches)!=1:
                    raise ValueError("constituent controller is not registered to its volume")
                declaration=matches[0]
                source=tomllib.loads(read_source(root/declaration["manifest"]).decode())
                payload=read_source(root/source["path"])
                if source["id"]!=source_id or declaration["sha256"]!=source["sha256"] or sha(payload)!=source["sha256"] or len(payload)!=source["byte_size"]:
                    raise ValueError("exact source bytes changed before admission")
                map_path=container.get("line_map_path") if source_id==container["artifacts"]["ocr"]["id"] else declaration.get("line_map_path")
                mapping=json.loads(read_source(root/map_path)) if map_path else {"pages":[]}
                for page in mapping["pages"]:
                    if "output_lf_range_1" in page:
                        span=page["output_lf_range_1"]
                        page.update(physical_line_start=span[0] if span else None,physical_line_end=span[1] if span else None)
                source_cache[source_id]=(source,lines(payload),mapping)
            source,raw,mapping=source_cache[source_id]
            if source["sha256"]!=unit["artifact_sha256"]:
                raise ValueError("unit and controlling artifact disagree")
            ranges=item["physical_line_ranges"]
            prior=0
            for start,end in ranges:
                if not prior<start<=end<=len(raw):
                    raise ValueError("reviewed ranges overlap or escape source")
                prior=end
            attribution=item.get("source_attribution_lines")
            if not isinstance(attribution,list) or len(attribution)!=2 or not all(type(n) is int for n in attribution):
                raise ValueError("admission requires exact source attribution lines")
            astart,aend=attribution
            if not 1<=astart<=aend<=len(raw) or not any(start<=astart<=aend<=end for start,end in ranges):
                raise ValueError("source attribution is outside the selected constituent")
            literal=" ".join(" ".join(raw[astart-1:aend]).split())
            if " ".join(item["printed_attribution"].split()) not in literal:
                item["reviewed_identity_label"]=item["printed_attribution"]
                item["printed_attribution"]=literal
            replay_document=None
            if unit.get("segment_path"):
                prior_document=(fragment_index if is_fragment else document_index).get(unit["id"])
                if item!=unit.get("review") or prior_document is None:
                    raise ValueError("registered source reviews require a new versioned selection or correction identity")
                replay_document=json.loads(json.dumps(prior_document))
            selected_pages=[page for page in mapping["pages"] if page["physical_line_start"] is not None and any(
                page["physical_line_start"]<=end and page["physical_line_end"]>=start for start,end in ranges)]
            unit["reviewed_scan_leaf_ids"]=[page["leaf"] for page in selected_pages]
            unit["reviewed_artifact_pages"]=[page["artifact_page"] for page in selected_pages]
            owner=unit["id"].removeprefix("bullarium.")
            language=item.get("language","la")
            work_id="work.bullarium-romanum."+owner
            edition_key=Path(container["edition_path"]).name
            if language!="la":
                edition_key=edition_key.removesuffix("-latin")+{"it":"-italian","mul":"-multilingual"}.get(language,"-"+language)
            base=root/"src/sources/works/bullarium-romanum"/owner.replace(".","-")
            identity_namespace="bullarium-romanum."+owner
            canonical=item.get("canonical_work_id")
            if canonical:
                if not item.get("identity_evidence") or item["identity_evidence"].get("existing_work_id")!=canonical:
                    raise ValueError("canonical joins require reviewed issuer/date/incipit/source evidence")
                matches=[path for path in (root/"src/sources/works").glob("*/*/work.toml") if tomllib.loads(read_source(path).decode()).get("id")==canonical]
                if len(matches)!=1:
                    raise ValueError("canonical work identity is absent or ambiguous")
                base=matches[0].parent
                work_id=canonical
                identity_namespace=canonical.removeprefix("work.")
                edition_key=edition_key.removesuffix("-latin")+"-bullarium-"+("appendix-01" if unit["volume"]=="appendix" else f"volume-{unit['volume']:02d}")+"-latin"
            edition_id="edition."+identity_namespace+"."+edition_key
            parent=base/"editions"/edition_key
            segment_id="segment."+identity_namespace+"."+edition_key+".source-ocr"
            segment_path=parent/"segments/source-ocr.toml"
            note=(("Fragment witness; the source omits part of the act. " if is_fragment else "")+"The exact selected raw OCR extent and surrounding boundary context were inspected. "
                "Printed attribution is preserved; this is not modern authentication, critical dating or image-collated text. "+item["review_note"])
            prior_selection=None
            if item.get("reading_selection_variant_of"):
                prior_selection=units.get(item["reading_selection_variant_of"])
                if (not prior_selection or prior_selection.get("work_id")!=work_id or
                        prior_selection.get("artifact_id")==source["id"] or
                        source.get("artifact_type")!="coordinate-reading-order-ocr"):
                    raise ValueError("a repaired reading selection requires the same reviewed work and a genuinely new ordered controller")
            if replay_document is None:
                if not canonical:
                    stage_record(base/"work.toml",{"schema":1,"record_type":"work","id":work_id,"title":item["title"],
                        "responsible":item["printed_attribution"],"work_type":"historical-papal-act-fragment" if is_fragment else "historically-attributed-papal-act","languages":item.get("component_languages",[language]),
                        "description":note,"relations":[container["work_id"]]})
                elif (parent/"edition.toml").exists() and not segment_path.exists():
                    raise ValueError("an existing canonical edition requires an explicitly new source/selection identity for a new join")
                stage_record(parent/"edition.toml",{"schema":1,"record_type":"edition","id":edition_id,"work_id":work_id,
                    "title":item["title"]+" — "+edition_key,"language":language,"date":edition_key[:4],
                    "publication":"Constituent in "+container["work_id"]+", source unit "+unit["act_number_raw"]+".","notes":note})
                stage_record(segment_path,{"schema":2,"record_type":"segment","id":segment_id,"edition_id":edition_id,
                    "artifact_id":source["id"],"artifact_sha256":source["sha256"],"segment_type":"constituent-fragment" if is_fragment else "constituent-work",
                    "physical_line_ranges":ranges,"states":["cataloged","acquired","inspected"],"context":note,
                    "notes":"Review extent: "+item["reviewed_extent"]+" Source text remains uncorrected OCR, with historical synopsis, dating/signatures and apparatus in the selected extent. No image collation or historical authentication is claimed."})
            unit.update({"status":"admitted-fragment" if is_fragment else "admitted-mechanical-ocr-extent","extent_kind":"fragment" if is_fragment else "printed-act",
                "work_id":work_id,"edition_id":edition_id,
                "segment_id":segment_id,"segment_path":str(segment_path.relative_to(root)),"review":item})
            unit["reviewed_protocol"]={"physical_line_ranges":[[astart,aend]],"literal":literal,"artifact_sha256":source["sha256"]}
            if prior_selection is not None:
                unit["reading_selection_variant_of"]=prior_selection["id"]
                unit["prior_reading_selection"]={key:prior_selection[key] for key in
                    ("id","artifact_id","artifact_sha256","segment_id","segment_path") if key in prior_selection}
            if canonical:
                unit["canonical_identity_resolution"]=item["identity_evidence"]
                if unit.get("parent_unit_id"):
                    units[unit["parent_unit_id"]].setdefault("canonical_match_candidates",{})[canonical]={
                        "status":"reviewed-and-joined","unit_id":unit["id"],"physical_line_ranges":ranges,
                        "evidence":item["identity_evidence"]}
            extent="; ".join(f"{start}-{end}" for start,end in ranges)
            locator=("Source-derived reading-order LF lines " if source.get("artifact_type")=="coordinate-reading-order-ocr" else "Raw OCR LF lines ")+extent+". "
            if selected_pages:
                locator+=f"Exact scan leaf bounds {selected_pages[0]['leaf']}-{selected_pages[-1]['leaf']}; automated printed-page labels remain unverified. "
            source_note=(("Fragment witness: part of the act is absent from this printing. " if is_fragment else "")+"From Bullarium Romanum, "+container["work_id"].removeprefix("work.bullarium-romanum.")+", "+edition_key+". "+locator+"Uncorrected, uncollated source OCR. "
                "The selected witness retains its source headings, identified historical notes, dating/signatures and literal abbreviations without expansion. Attribution is the printing's; source dates remain literal and no normalized act date is supplied.")
            if is_fragment:
                source_note+=" "+item.get("reader_source_note",item.get("source_extent_limit",item["review_note"]))
            elif item.get("reader_source_note"):
                source_note+=" "+item["reader_source_note"]
            document={"id":unit["id"]+(".fragment" if is_fragment else ""),"title":item["title"],"pope":item["printed_attribution"],"date":None,
                "revision":revision,
                "document_type":item.get("document_type","Historical papal act fragment (printed attribution)" if is_fragment else "Historical papal act (printed attribution)"),"language":language,"source_url":source["source_url"],
                "text_path":source["path"],"sha256":source["sha256"],"artifact_id":source["id"],
                "rights_status":source["rights_status"],"rights_basis":source["rights_basis"],"segment_id":segment_id,
                "rights_notice":edition_key[:4]+" "+edition_key.split("-")[1].title()+" printing: public domain in the United States.",
                "segment_path":str(segment_path.relative_to(root)),"physical_line_ranges":ranges,"source_note":source_note,
                "extent_kind":"fragment" if is_fragment else "printed-act"}
            if item.get("language_label"):
                document["language_label"]=item["language_label"]
            if replay_document is not None:
                document=replay_document
            if is_fragment:
                document_index.pop(unit["id"],None)
                fragment_index[unit["id"]]=document
            else:
                fragment_index.pop(unit["id"],None)
                document_index[unit["id"]]=document
    documents=sorted(document_index.values(),key=lambda document:document["id"])
    fragments=sorted(fragment_index.values(),key=lambda document:document["id"])
    catalog["revision"]=revision
    catalog["units"]=sorted(units.values(),key=lambda unit:unit["id"])
    for unit in catalog["units"]:
        if unit.get("review"):
            unit["review"]=durable_review(unit["review"])
        if unit.get("review_history"):
            unit["review_history"]=durable_review(unit["review_history"])
    catalog["coverage"].update({"independent_papal_acts_admitted":sum(u["status"]=="admitted-mechanical-ocr-extent" for u in units.values()),
        "units_held":sum(u["status"] in {"held","specifically-held"} for u in units.values()),
        "split_source_units":sum(u["status"]=="split-into-constituents" for u in units.values()),
        "additional_source_units":sum("parent_unit_id" in u for u in units.values()),
        "additional_split_constituents":sum("parent_unit_id" in u and bool(re.search(r"\.part-[0-9]+$",u["id"])) for u in units.values()),
        "identified_additional_source_units":sum("parent_unit_id" in u and not re.search(r"\.part-[0-9]+$",u["id"]) and not u.get("reading_selection_variant_of") for u in units.values()),
        "additional_reading_selections":sum(bool(u.get("reading_selection_variant_of")) for u in units.values()),
        "coordinate_reading_order_constituents":sum("source_order_parent" in u for u in units.values()),
        "active_source_order_withdrawals":sum(u.get("active_reader_status")=="source-order-hold" for u in units.values()),
        "specifically_reviewed_holds":sum(u["status"]=="specifically-held" for u in units.values()),
        "duplicate_witnesses":sum(u["status"]=="duplicate-witness" for u in units.values()),
        "non_papal_units":sum(u["status"]=="non-papal-source-unit" for u in units.values()),
        "not_independent_acts":sum(u["status"]=="not-an-independent-act" for u in units.values())})
    catalog["coverage"]["fragment_witnesses_admitted"]=sum(u["status"]=="admitted-fragment" for u in units.values())
    catalog["source_extent_policy"]={"complete_printed_witness":"Independent, bounded historical printing; literal conventional boilerplate abbreviations remain disclosed and unexpanded.",
        "missing_substantive_content":"An explicitly absent opening/proem or substantive body never counts as a recovered complete act. Cross-references are not expanded from another act.",
        "fragment_witness":"A cleanly bounded, clearly attributed surviving substantive fragment is titled and counted separately, with extent_kind=fragment and exact missing-content disclosure.",
        "calibration_correction":"Volume4 unit0110 was withdrawn from complete-act admission because raw LF54844–54846 replace its proem with a cross-reference; the surviving operative clauses can be offered only as a fragment.",
        "extraction_limited_text":"A clean prefix of a complete printing is not published as a historical fragment merely to bypass unresolved OCR geometry. Clean research ranges and exact blockers remain recorded separately.",
        "shared_editorial_apparatus":"A joint container-level synopsis may remain with the retained container when individual instruments have separable complete bodies and all their own historical notes. Exclusions are declared explicitly.",
        "reported_papal_response":"An explicitly attributed, cleanly bounded reported papal decision can be retained with its petition and narration, labeled as a reported response; no first-person/autograph or juridical-weight claim is inferred.",
        "roster_only":"A detached beneficiary roster with the whole operative grant absent is research-only documentary material, not a recovered papal-act fragment.",
        "date_absence":"An empty lexical date lead or null normalized date is not an eligibility barrier. Missing substantive source text is assessed independently."}
    catalog["source_extent_policy"]["inline_body_margin_fusion"]="Known marginal ownership does not clear word interleaving inside the substantive body. A separately bounded summary can remain literal; confirmed inline fusion stays held until a separately identified derivative restores source order. Frozen prior witnesses remain historical records and are not silently edited."
    catalog["boundary_limit"]="Exact LF ranges identify source candidates. Only explicitly reviewed extents have constituent records; unreviewed candidates remain held. OCR column order, historical attribution and authenticity are independent questions."
    catalog["identity_matching"]="Canonical joins require explicit reviewed incipit, printed issuer, raw dating and distinctive source-context evidence. No title-only merge is made; other unresolved identities remain separate candidates."
    check_manifest_targets()
    for path,payload in source_records.items():
        check_source_write(path,payload)
    for path,payload in source_records.items():
        write_source(path,payload)
    write(root/CATALOG,json_bytes(catalog))
    for target,state,prior_bytes,prior_documents,new_documents,extra in (
            (manifest_target,existing,existing_bytes,old_documents,documents,{}),
            (fragment_target,fragment_existing,fragment_existing_bytes,old_fragments,fragments,
             {"extent_kind":"fragment","source_note":"Surviving historical fragments only; never included in complete-act counts. Each source note states the missing portion."})):
        result={**state,**extra,"schema":"triptych-papal-typeset/v1","revision":revision,"documents":new_documents}
        if prior_documents and prior_bytes and (prior_documents!=new_documents or state.get("revision")!=revision):
            digest=sha(prior_bytes)
            write(root/".scratch/bullarium_reconstruction/manifest-history"/(digest+".json"),prior_bytes)
            history=list(state.get("input_history",[]))
            entry={"revision":state["revision"],"sha256":digest,"document_ids":[d["id"] for d in prior_documents],"archive_key":"sha256:"+digest}
            if not history or history[-1]!=entry:
                history.append(entry)
            result["input_history"]=history
        write(target,json_bytes(result))
    return {"status":"ok",**catalog["coverage"]}


def register(root,volume,archive,paths,mapping):
    key="appendix-01" if volume=="appendix" else f"volume-{volume:02d}"
    year="1867" if volume=="appendix" else "1883" if volume==8 else str(archive["publication_year"])
    city="naples" if volume==8 else "turin"
    edition=f"{year}-{city}-latin"
    base=root/"src/sources/works/bullarium-romanum"/key
    work_id=f"work.bullarium-romanum.{key}"
    edition_id=f"edition.bullarium-romanum.{key}.{edition}"
    parent=base/"editions"/edition
    title="Appendix volume I, first installment (Leo I–Silverius)" if volume=="appendix" else "Volume "+roman(volume)
    rights=(f"United States: the identified {city.title()} {year} printing, {title}, was published before 1931. "
        "Its historical Latin and contemporary editorial apparatus have an expired-term basis under the repository papal-documents-rights-v1.toml assessment (17 USC 104A, 304, 305). "
        "Mechanical OCR and generated page data add no original authorship (Compendium 313.4(A)); factual digitization/library marks introduce no modern creative introduction or translation. "
        "No worldwide public-domain claim or Triptych license over source wording is asserted.")
    record(base/"work.toml",{"schema":1,"record_type":"work","id":work_id,"title":"Bullarium Romanum — "+title,
        "responsible":"Historical Bullarium editors and the act authors attributed within the printing","work_type":"historical-document-container",
        "languages":["la","it"],"description":"A separately owned historical container: papal/curial acts, inserted instruments, biographies and editorial apparatus. Possession establishes no census or authentication of its attributed acts."})
    record(parent/"edition.toml",{"schema":1,"record_type":"edition","id":edition_id,"work_id":work_id,
        "title":f"{title} — {city.title()} {year}","language":"la","date":year,
        "publication":f"Bullarum diplomatum et privilegiorum sanctorum Romanorum pontificum, {title}; {city.title()}, {year}.",
        "notes":"Printing identified from title-page imprint, with volume inventory corroboration. Generic archive date1857 does not identify each printing. " +
        ("VolumeVIII is the Naples1883 reprint despite the library index's Turin1863 label; title-page image inspected. " if volume==8 else "")+
        ("Only the first appendix installment through Silverius is in these bytes; the promised remainder is absent. " if volume=="appendix" else "")+
        "Raw OCR and automated page labels are finding aids; no whole-text image collation or act authentication is claimed."})
    routes=source_routes(archive,paths)
    artifacts={}
    for kind,info in routes.items():
        artifact_id=f"artifact.bullarium-romanum.{key}.{edition}.{kind}-{info['sha256'][:12]}"
        directory=parent/"artifacts"/f"{kind}-{info['sha256'][:12]}"
        data={"schema":1,"record_type":"artifact","id":artifact_id,"edition_id":edition_id,
            "artifact_type":{"ocr":"uncorrected-ocr","xml":"ocr-layout-xml","labels":"automated-pagination-map"}[kind],
            "media_type":{"ocr":"text/plain","xml":"application/xml","labels":"application/json"}[kind],
            "storage":"remote" if kind=="xml" else "tracked","rights_status":"public-domain","rights_basis":rights,
            "rights_jurisdiction":"United States","retrieved":"2026-10-26",**info,
            "provenance":"Whole response acquired mechanically; full byte size and SHA1 matched the acquired source file inventory; complete SHA256 computed. No source wording regenerated by a model.",
            "notes":(f"The exact {info['byte_size']:,}-byte verbose XML is remote because of measured size and source-machine attributes. Offline alternatives: complete raw OCR and compact exact token/line/leaf map retained in this edition. " if kind=="xml" else "Complete uncorrected response. ")+"Token identity and physical bounds do not establish column reading order or verified printed pagination."}
        if kind!="xml":
            target=directory/paths[kind].name
            write_source(target,paths[kind].read_bytes())
            data["path"]=str(target.relative_to(root))
        if kind=="ocr":
            data.update({"indexable":True,"encoding":"utf-8"})
        record(directory/"artifact.toml",data)
        artifacts[kind]={"id":artifact_id,"manifest":str((directory/"artifact.toml").relative_to(root)),"sha256":info["sha256"]}
    proof=paths["ocr"].parent/"pdf_receipt.json"
    title_image=paths["ocr"].parent/"title-page.png"
    if proof.exists() and title_image.exists():
        evidence=json.loads(proof.read_text())
        pdf_path=root/evidence["path"]
        pdf_bytes=pdf_path.read_bytes()
        if sha(pdf_bytes)!=evidence["sha256"] or hashlib.sha1(pdf_bytes).hexdigest()!=evidence["sha1"]:
            raise ValueError("imprint facsimile differs from acquisition receipt")
        pdfinfo=subprocess.run(["pdfinfo",str(pdf_path)],capture_output=True,text=True,check=True).stdout
        page_count=int(re.search(r"^Pages:\s+(\d+)$",pdfinfo,re.M)[1])
        if page_count!=len(mapping["pages"]):
            raise ValueError("facsimile and exact XML page counts disagree")
        pdf_id=f"artifact.bullarium-romanum.{key}.{edition}.facsimile-{sha(pdf_bytes)[:12]}"
        pdf_dir=parent/"artifacts"/f"facsimile-{sha(pdf_bytes)[:12]}"
        pdf_record={"schema":2,"record_type":"artifact","id":pdf_id,"edition_id":edition_id,
            "artifact_type":"facsimile-pdf","media_type":"application/pdf","storage":"remote",
            "rights_status":"public-domain","rights_basis":rights,"rights_jurisdiction":"United States",
            "source_url":evidence.get("source_url",evidence.get("url")),"retrieved":"2026-10-26",
            "sha256":sha(pdf_bytes),"byte_size":len(pdf_bytes),"page_count":page_count,
            "provenance":"Whole source PDF acquired mechanically; complete byte size/SHA1 matched archive file metadata and SHA256 was computed. Title-page image inspected for imprint only.",
            "notes":f"This exact {len(pdf_bytes):,}-byte facsimile is remote because of measured size compared with the retained complete OCR and exact title-page image derivative. An offline reader can inspect the retained imprint image and reopen all acquired OCR. Body wording was not image-collated."}
        record(pdf_dir/"artifact.toml",pdf_record)
        artifacts["facsimile"]={"id":pdf_id,"manifest":str((pdf_dir/"artifact.toml").relative_to(root)),"sha256":pdf_record["sha256"]}
        image_bytes=title_image.read_bytes()
        image_id=f"artifact.bullarium-romanum.{key}.{edition}.imprint-{sha(image_bytes)[:12]}"
        image_dir=parent/"artifacts"/f"imprint-{sha(image_bytes)[:12]}"
        image_path=image_dir/"title-page.png"
        write_source(image_path,image_bytes)
        page=2 if volume=="appendix" else 9
        scale=1800 if volume==8 else 1400
        record(image_dir/"artifact.toml",{"schema":1,"record_type":"artifact","id":image_id,"edition_id":edition_id,
            "artifact_type":"title-page-image-derivative","media_type":"image/png","storage":"tracked",
            "rights_status":"public-domain","rights_basis":rights,"rights_jurisdiction":"United States",
            "retrieved":"2026-10-26","sha256":sha(image_bytes),"byte_size":len(image_bytes),"path":str(image_path.relative_to(root)),
            "derived_from":pdf_id,"transformation":f"Poppler pdftoppm26.10.0: -f {page} -singlefile -scale-to {scale} -png; main19–24 and appendix additionally used -l {page}. No explicit DPI override; final dimensions controlled by -scale-to.",
            "provenance":"Exact retained derivative used in the recorded title-page imprint inspection; no image correction or recompression.",
            "notes":"Imprint evidence only; no act wording or whole-volume image collation is asserted."})
        artifacts["imprint"]={"id":image_id,"manifest":str((image_dir/"artifact.toml").relative_to(root)),"sha256":sha(image_bytes)}
        record(parent/"passages/title-imprint.toml",{"schema":2,"record_type":"passage",
            "id":f"passage.bullarium-romanum.{key}.{edition}.title-imprint","edition_id":edition_id,
            "artifact_id":pdf_id,"artifact_sha256":pdf_record["sha256"],"artifact_page_ranges":[[page,page]],
            "locus":"title-page","states":["cataloged","acquired","inspected"],
            "context":f"Only the printed title-page imprint was visually inspected: {city.title()} {year}. The retained title-page derivative permits offline review. Body text remains uncollated."})
    payload=json_bytes(mapping)
    map_id=f"artifact.bullarium-romanum.{key}.{edition}.line-map-{sha(payload)[:12]}"
    directory=parent/"artifacts"/f"line-map-{sha(payload)[:12]}"
    target=directory/"line-map.json"
    write_source(target,payload)
    record(directory/"artifact.toml",{"schema":1,"record_type":"artifact","id":map_id,"edition_id":edition_id,
        "artifact_type":"mechanical-line-leaf-map","media_type":"application/json","storage":"tracked",
        "rights_status":"public-domain","rights_basis":rights,"rights_jurisdiction":"United States",
        "retrieved":"2026-10-26","sha256":sha(payload),"byte_size":len(payload),"path":str(target.relative_to(root)),
        "derived_from":artifacts["xml"]["id"],
        "provenance":"Project mechanical mapping of the complete exact source responses, not a model transcription.",
        "transformation":"exact-whitespace-token-equality-v1: derive OBJECT leaf locations and layout flags from the entire exact XML. Compare every XML WORD token with the entire exact TXT token stream to assign raw LF positions; the map pins both SHA256 values. Join the separately registered automated labels by leaf ID. Blank separators remain unmapped. The registered OCR and labels are auxiliary correspondence inputs; the exact XML is the controlling transformation parent.",
        "notes":"Identity/locators only. Geometry screen flags some reading-order defects and never certifies their absence; automated printed-page labels remain unverified."})
    return {"work_id":work_id,"edition_id":edition_id,"edition_path":str(parent.relative_to(root)),
        "artifacts":artifacts,"line_map_id":map_id,"line_map_path":str(target.relative_to(root)),"rights_basis":rights}


def reconstruct(root,selected,revision):
    previous=json.loads((root/CATALOG).read_text()) if (root/CATALOG).exists() else {"volumes":[],"units":[]}
    if any(unit.get("segment_id") for unit in previous["units"]):
        raise ValueError("registered constituent witnesses are immutable; use reviewed admission/correction updates instead of discovery replay")
    archives=archive_volumes(root)
    previous_units={unit["id"]:unit for unit in previous["units"]}
    volumes=[v for v in previous["volumes"] if v["volume"] not in selected]
    units=[u for u in previous["units"] if u["volume"] not in selected]
    for volume in selected:
        paths=inputs(root,volume)
        ocr=paths["ocr"].read_bytes()
        mapping=page_map(ocr,paths["xml"],json.loads(paths["labels"].read_text()))
        container=register(root,volume,archives.get(volume,{}),paths,mapping)
        found=discover(ocr,volume,mapping)
        for unit in found:
            unit.update({"artifact_id":container["artifacts"]["ocr"]["id"],"artifact_sha256":sha(ocr),"line_map_id":container["line_map_id"]})
            old=previous_units.get(unit["id"],{})
            if old.get("review"):
                if old["artifact_sha256"]!=unit["artifact_sha256"] or old["heading_line"]!=unit["heading_line"]:
                    raise ValueError("reconstruction changed a reviewed source identity; reconcile its review explicitly")
                unit.update({k:old[k] for k in ("status","work_id","edition_id","segment_id","segment_path","review","review_history","extent_kind") if k in old})
        for old in previous["units"]:
            if old.get("parent_unit_id") and old["volume"]==volume:
                parent=next((u for u in found if u["id"]==old["parent_unit_id"]),None)
                if parent and parent["artifact_sha256"]==old["artifact_sha256"]:
                    found.append(old)
        units.extend(found)
        volumes.append({"volume":volume,"container":container,"whole_ocr_bytes":len(ocr),"whole_ocr_sha256":sha(ocr),
            "physical_lines":mapping["physical_line_count"],"artifact_pages":len(mapping["pages"]),"token_count":mapping["token_count"],
            "body_bounds":list(BOUNDS[volume]),"candidate_units":len(found),
            "geometry_flagged_pages":sum(bool(p["layout_hold_reasons"]) for p in mapping["pages"])})
    volumes.sort(key=lambda v:str(v["volume"]).zfill(3))
    units.sort(key=lambda u:u["id"])
    admitted=sum(unit["status"]=="admitted-mechanical-ocr-extent" for unit in units)
    coverage={"whole_containers_acquired":len(volumes),"raw_candidate_units":sum("parent_unit_id" not in u for u in units),"independent_papal_acts_admitted":admitted,
        "units_held":sum(u["status"] in {"held","specifically-held"} for u in units),"authenticity_verified":0,
        "fragment_witnesses_admitted":sum(u["status"]=="admitted-fragment" for u in units),
        "note":"Candidates include false positives and non-papal units; they are not recovered independent papal act counts."}
    catalog={"schema":"triptych-bullarium-catalog/v1","revision":revision,"method":METHOD,
        "scope":"The 24 complete main-volume archive OCR responses plus the available first appendix installment; bounded discovery, not a census of every historical papal act.",
        "boundary_limit":"Exact LF ranges locate candidate headings through the next recognized heading. Lost numerals, inserted acts, biographies and merged/reversed columns can make those extents overinclusive. Only explicitly reviewed extents receive constituent records.",
        "authenticity":"Printed attributions are historical source claims. No act is modern-authenticated or critically dated by this reconstruction.",
        "identity_matching":"No title-only merges into existing papal works; constituent identities await source-based review.",
        "coverage":coverage,"volumes":volumes,"units":units}
    if previous.get("source_extent_policy"):
        catalog["source_extent_policy"]=previous["source_extent_policy"]
    catalog["date_lead_limit"]="date_raw preserves lexical dating leads. The pattern can also match ordinary uses of data/datum or a historical citation. These are not normalized act dates; all unestablished ISO dates remain null."
    write(root/CATALOG,json_bytes(catalog))
    manifest=json.loads((root/MANIFEST).read_text()) if (root/MANIFEST).exists() else {"schema":"triptych-papal-typeset/v1","documents":[]}
    manifest["revision"]=revision
    manifest["source_note"]="No placeholder/whole-volume papal PDFs. Raw-line candidates remain held until independent act boundaries and reading order are established."
    write(root/MANIFEST,json_bytes(manifest))
    return coverage


def check(root,path):
    data=json.loads(path.read_text())
    if data.get("schema")!="triptych-bullarium-catalog/v1":
        raise ValueError("unknown catalog schema")
    hashes={}
    for volume in data["volumes"]:
        for artifact in volume["container"]["artifacts"].values():
            item=tomllib.loads((root/artifact["manifest"]).read_text())
            if item["id"]!=artifact["id"] or item["sha256"]!=artifact["sha256"]:
                raise ValueError("artifact identity changed")
            if item["storage"]=="tracked":
                payload=(root/item["path"]).read_bytes()
                if sha(payload)!=item["sha256"] or len(payload)!=item["byte_size"]:
                    raise ValueError("artifact bytes changed")
            hashes[item["id"]]=item["sha256"]
    ids=set()
    for unit in data["units"]:
        if unit["id"] in ids or hashes.get(unit["artifact_id"])!=unit["artifact_sha256"]:
            raise ValueError("candidate identity/hash conflict")
        ids.add(unit["id"])
        if unit["status"] in {"specifically-held","duplicate-witness","non-papal-source-unit","not-an-independent-act","split-into-constituents"}:
            if not unit.get("review") or not unit["review"].get("review_note"):
                raise ValueError("specific hold lacks source evidence")
        elif unit["status"]!="held":
            if unit["status"] not in {"admitted-mechanical-ocr-extent","admitted-fragment"} or not unit.get("review"):
                raise ValueError("unreviewed candidate promoted")
            segment=tomllib.loads((root/unit["segment_path"]).read_text())
            if segment["artifact_sha256"]!=unit["artifact_sha256"] or segment["physical_line_ranges"]!=unit["review"]["physical_line_ranges"]:
                raise ValueError("reviewed constituent changed")
    return {"status":"ok",**data["coverage"]}


def main(argv=None,examples=None):
    argv=list(sys.argv[1:] if argv is None else argv)
    # The independently tested adapters own their argument contracts. Preserve
    # the global root option when forwarding to either adapter.
    prefix=[]
    rest=argv
    if rest[:1]==["--root"] and len(rest)>2:
        prefix=rest[:2]
        rest=rest[2:]
    elif rest and rest[0].startswith("--root="):
        prefix=rest[:1]
        rest=rest[1:]
    if rest and rest[0] in {"series","corrections","geometry","screen"}:
        if rest[0]=="series":
            from _bullarium_series import main as adapter
        elif rest[0]=="corrections":
            from _bullarium_corrections import main as adapter
        elif rest[0]=="geometry":
            from _bullarium_geometry import main as adapter
        else:
            from _bullarium_screen import main as adapter
        return adapter(prefix+rest[1:],examples=examples)
    parser=examples_live_on_the_verbs(argparse.ArgumentParser(prog="bullarium",description=__doc__),"bullarium")
    parser.add_argument("--root",type=Path,default=ROOT)
    sub=parser.add_subparsers(dest="verb",required=True)
    for name in ("acquire","reconstruct","admit","check","status"):
        command=sub.add_parser(name)
        command.add_argument("--json",action="store_true")
        command.add_argument("--catalog",type=Path,default=Path(CATALOG))
        command.add_argument("--volume",action="append")
        if name in {"reconstruct","admit"}:
            command.add_argument("--revision",required=True)
        if name=="admit":
            command.add_argument("--review",action="append",type=Path,required=True)
            command.add_argument("--manifest-out",default=MANIFEST)
            command.add_argument("--fragment-manifest-out",default=FRAGMENT_MANIFEST)
            command.add_argument("--reader-notes",action="append",type=Path,default=[])
        with_examples(command,(examples or {}).get(name,()))
    sub.add_parser("series",help="Acquire configured historical series and review their constituents.")
    sub.add_parser("corrections",help="Append separately identified corrections with exact PDF supersessions.")
    sub.add_parser("geometry",help="Replay exact XML WORD reading-order recipes without source correction.")
    sub.add_parser("screen",help="Screen native geometry for advisory research leads without clearing sources.")
    args=parser.parse_args(argv)
    try:
        root=args.root.resolve()
        selected=["appendix" if value=="appendix" else int(value) for value in args.volume] if args.volume else list(range(1,25))+["appendix"]
        if any(value not in BOUNDS for value in selected):
            raise ValueError("volume must be 1-24 or appendix")
        if len(set(selected))!=len(selected):
            raise ValueError("duplicate volume selection")
        if args.verb in {"reconstruct","admit"}:
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z",args.revision):
                raise ValueError("revision requires explicit whole-second UTC")
            dt.datetime.fromisoformat(args.revision.replace("Z","+00:00"))
            if args.verb=="reconstruct":
                result=reconstruct(root,selected,args.revision)
            else:
                reader_notes={}
                for path in args.reader_notes:
                    for key,value in json.loads(path.read_text()).items():
                        prior=reader_notes.setdefault(key,{})
                        for field,data in value.items():
                            if field=="reader_source_note" and prior.get(field) and data not in prior[field]:
                                prior[field]+=" "+data
                            else:
                                prior[field]=data
                result=admit(root,args.review,args.revision,args.manifest_out,args.fragment_manifest_out,reader_notes,input_paths=args.reader_notes)
        elif args.verb=="acquire":
            result=acquire(root,selected)
        else:
            path=args.catalog if args.catalog.is_absolute() else root/args.catalog
            if not path.is_file():
                raise ValueError("Bullarium catalog has not been reconstructed")
            result=check(root,path) if args.verb=="check" else json.loads(path.read_text())["coverage"]
        print(json.dumps({"v":1,**result},ensure_ascii=False,sort_keys=True,separators=(",",":")) if args.json else "\n".join(f"{k}: {v}" for k,v in result.items()))
        return 0
    except (ValueError,OSError,KeyError,ET.ParseError) as error:
        print(json.dumps({"v":1,"status":"error","code":"input","error":str(error)},sort_keys=True,separators=(",",":")) if args.json else f"bullarium: {error}",file=sys.stderr)
        return 2
