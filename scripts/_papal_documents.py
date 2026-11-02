"""Vatican index discovery; source wording never passes through a model."""
from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import threading
import time
import unicodedata
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "triptych-papal-documents/v1"
BASE = "https://www.vatican.va"
POPE_NAMES = {
    "benedictus-xiv": "Benedict XIV", "clemens-xiii": "Clement XIII",
    "clemens-xiv": "Clement XIV", "pius-vi": "Pius VI", "pius-vii": "Pius VII",
    "leo-xii": "Leo XII", "pius-viii": "Pius VIII", "gregorius-xvi": "Gregory XVI",
    "pius-ix": "Pius IX", "leo-xiii": "Leo XIII", "pius-x": "Pius X",
    "benedict-xv": "Benedict XV", "pius-xi": "Pius XI", "pius-xii": "Pius XII",
    "john-xxiii": "John XXIII", "paul-vi": "Paul VI", "john-paul-i": "John Paul I",
    "john-paul-ii": "John Paul II", "benedict-xvi": "Benedict XVI",
    "francesco": "Francis", "leo-xiv": "Leo XIV",
}
HISTORICAL = set(list(POPE_NAMES)[:9])
CATEGORIES = {
    "encyclicals": "encyclical", "bulls": "bull", "briefs": "brief",
    "apost_constitutions": "apostolic-constitution",
    "apost_exhortations": "apostolic-exhortation",
    "apost_letters": "apostolic-letter", "motu_proprio": "motu-proprio",
}
DOCUMENT_TYPES = set(CATEGORIES.values()) | {"letter", "address", "other"}
OVERRIDES_SCHEMA = "triptych-papal-overrides/v1"
RECORD_ROLES = {"whole-work", "constituent", "composite", "index-mislink"}
OVERRIDE_FIELDS = {"record_role", "issues", "constituents", "body_language_conflicts", "resolved_date", "date_resolution", "resolved_title", "title_resolution", "parent_work_id", "part", "observed_languages", "delivery_issues", "source_unit_identity", "source_responsible", "display_responsible", "source_work_type"}
OVERRIDE_FIELDS.update({"source_work_id", "delivery_ownership"})
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
MONTHS = {}
for n, words in enumerate((
    "january gennaio ianuarii januarii", "february febbraio februarii",
    "march marzo martii", "april aprile aprilis", "may maggio maii",
    "june giugno iunii junii", "july luglio iulii julii", "august agosto augusti",
    "september settembre septembris", "october ottobre octobris",
    "november novembre novembris", "december dicembre decembris",
), 1):
    for word in words.split():
        MONTHS[word] = n
        if len(word) > 3:
            MONTHS.setdefault(word[:3], n)


@dataclass
class Node:
    tag: str = "root"
    attrs: dict = field(default_factory=dict)
    children: list = field(default_factory=list)
    parent: "Node | None" = None

    def walk(self, tag=None):
        for child in self.children:
            if isinstance(child, Node):
                if tag is None or child.tag == tag:
                    yield child
                yield from child.walk(tag)

    def has_class(self, name):
        return name in self.attrs.get("class", "").split()

    def text(self):
        return " ".join("".join(c.text() if isinstance(c, Node) else c for c in self.children).split())


class TreeParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node()
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = Node(tag, dict(attrs), parent=self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def parse_html(raw):
    parser = TreeParser()
    parser.feed(raw.decode("utf-8", errors="replace") if isinstance(raw, bytes) else raw)
    return parser.root


def normalize_url(url, base=BASE):
    parsed = urlsplit(urljoin(base, url))
    if parsed.scheme not in {"https", "http"} or parsed.hostname not in {"www.vatican.va", "vatican.va"}:
        raise ValueError("expected a public Vatican HTTP URL")
    return urlunsplit(("https", "www.vatican.va", parsed.path, parsed.query, ""))


def slug(value):
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def language_of(url):
    match = re.match(r"/content/[^/]+/([^/]+)/", urlsplit(url).path)
    return match.group(1).lower() if match else None


def category_of(url, title=""):
    path = urlsplit(url).path
    for category, kind in {**CATEGORIES, "letters": "letter", "speeches": "address"}.items():
        if f"/{category}/" in path or f"/{category}.index" in path:
            return kind
    text = title.lower().strip()
    for prefix, kind in (
        (r"(?:encyclical|enciclica|encicliche|lettera enciclica|litterae encyclicae|(?:epistola|epistula|littera) encyclica)\b", "encyclical"),
        (r"(?:bull|bolla|bulla)\b", "bull"),
        (r"(?:brief|breve)\b", "brief"),
        (r"(?:apostolic constitution|costituzione apostolica|constitutio apostolica|dogmatic constitution)\b", "apostolic-constitution"),
        (r"(?:apostolic exhortation|esortazione apostolica)\b", "apostolic-exhortation"),
        (r"(?:apostolic letter|lettera apostolica)\b", "apostolic-letter"),
        (r"motu\s+proprio\b", "motu-proprio"),
        (r"(?:letter|lettera|epistola)\b", "letter"),
        (r"(?:address|discorso|allocution|allocuzione)\b", "address"),
    ):
        if re.match(prefix, text):
            return kind
    # Earlier URLs spell the genre when a vernacular heading does not.
    tail = Path(path).stem
    for word, kind in (("enciclica", "encyclical"), ("bolla", "bull"), ("breve", "brief"), ("costituzione", "apostolic-constitution"), ("lettera-apostolica", "apostolic-letter")):
        if tail.startswith(word):
            return kind
    return "other"


def parse_date(raw):
    """Parse explicit index dates; ambiguity and impossible dates remain absent."""
    text = raw.lower().replace("\xa0", " ")
    text = re.sub(r"(?<=\d)(?:st|nd|rd|th)\b", "", text)
    matches = []
    for pattern, order in ((r"\b(\d{1,2})\s+(?:m(?:ensis)?\.?\s+)?([a-z]+)\.?\s*,?\s*(?:(?:a(?:nno)?\.?|a\.d\.)\s*)?(\d{4})\b", "dmy"),
                           (r"\b([a-z]+)\.?\s+(\d{1,2})\s*,?\s*(\d{4})\b", "mdy")):
        for match in re.finditer(pattern, text):
            a, b, y = match.groups()
            day, month = (a, MONTHS.get(b)) if order == "dmy" else (b, MONTHS.get(a))
            if month:
                try:
                    matches.append(date(int(y), month, int(day)).isoformat())
                except ValueError:
                    pass
    for match in re.finditer(r"\b(\d{4})-(\d{2})-(\d{2})\b", text):
        try:
            matches.append(date(*map(int, match.groups())).isoformat())
        except ValueError:
            pass
    unique = sorted(set(matches))
    return unique[0] if len(unique) == 1 else None


def date_from_filename(url):
    candidates = set()
    for token in re.findall(r"(?<!\d)(\d{8})(?!\d)", Path(urlsplit(url).path).stem):
        for year, month, day in ((token[:4], token[4:6], token[6:]), (token[4:], token[2:4], token[:2])):
            try:
                candidate = date(int(year), int(month), int(day))
                if 1000 <= candidate.year <= 2100:
                    candidates.add(candidate.isoformat())
            except ValueError:
                pass
    return next(iter(candidates)) if len(candidates) == 1 else None


def filename_identity(url):
    """Fold unambiguous DDMMYYYY/YYYYMMDD aliases without comparing titles."""
    stem = Path(urlsplit(url).path).stem.lower()
    explicit = date_from_filename(url)
    if explicit:
        compact = explicit.replace("-", "")
        stem = re.sub(r"(?<!\d)\d{8}(?!\d)", compact, stem)
    return stem


def title_parts(raw):
    groups = re.findall(r"\(([^()]*)\)", raw)
    date_raw = next((group for group in reversed(groups) if re.search(r"\b\d{4}\b", group)), "")
    title = raw
    if date_raw:
        title = raw[:raw.rfind("(" + date_raw + ")")].strip()
    elif parse_date(raw):
        # Latin catalogue headings often carry a date after the description.
        date_raw = raw
    title = re.sub(r"^(?:Encyclical|Bull|Brief|Apostolic Constitution|Apostolic Exhortation|Apostolic Letter|Letter)\s+", "", title, flags=re.I)
    return title, date_raw


def parse_index(raw, url):
    root = parse_html(raw)
    rows = []
    for item in root.walk():
        if not item.has_class("item"):
            continue
        ancestor = item.parent
        while ancestor and not ancestor.has_class("vaticanindex"):
            ancestor = ancestor.parent
        if ancestor is None:
            continue
        heading = next(item.walk("h2"), None)
        if heading is None:
            continue
        raw_title = heading.text()
        title, date_raw = title_parts(raw_title)
        languages = {}
        for part in item.walk():
            if part.has_class("translation-field"):
                for link in part.walk("a"):
                    if "href" not in link.attrs:
                        continue
                    try:
                        target = normalize_url(link.attrs["href"], url)
                    except ValueError:
                        continue
                    lang = language_of(target) or slug(link.text())
                    if lang and "/documents/" in target:
                        languages[lang] = target
        for link in heading.walk("a"):
            if "href" in link.attrs:
                try:
                    target = normalize_url(link.attrs["href"], url)
                except ValueError:
                    continue
                lang = language_of(target)
                if lang and "/documents/" in target:
                    languages.setdefault(lang, target)
        rows.append({"title": title, "index_title_raw": raw_title, "date_raw": date_raw,
                     "date": parse_date(date_raw), "languages": dict(sorted(languages.items())),
                     "document_type": category_of(url, raw_title), "source_index_url": url})
    links = []
    for link in root.walk("a"):
        if "href" not in link.attrs:
            continue
        try:
            target = normalize_url(link.attrs["href"], url)
        except ValueError:
            continue
        links.append(target)
    return rows, sorted(set(links))


class Fetcher:
    def __init__(self, cache, pace=.3, timeout=35, refresh=False):
        self.cache = Path(cache)
        if ".scratch" not in self.cache.resolve().parts:
            raise ValueError("index cache must be under a .scratch directory")
        self.cache.mkdir(parents=True, exist_ok=True)
        self.pace, self.timeout, self.refresh = pace, timeout, refresh
        self.lock = threading.Lock()
        self.next_request = 0.

    def fetch(self, url):
        url = normalize_url(url)
        key = hashlib.sha256(url.encode()).hexdigest()
        receipt_path = self.cache / (key + ".json")
        payload_path = self.cache / (key + ".html")
        if receipt_path.exists() and not self.refresh:
            receipt = json.loads(receipt_path.read_text())
            if receipt.get("status") == "not-found":
                return None, receipt
            if receipt.get("status") == "ok" and payload_path.exists():
                raw = payload_path.read_bytes()
                if hashlib.sha256(raw).hexdigest() != receipt.get("sha256"):
                    raise ValueError(f"cached index hash mismatch: {url}")
                return raw, receipt
        for attempt in range(3):
            with self.lock:
                delay = max(0., self.next_request - time.monotonic())
                self.next_request = max(self.next_request, time.monotonic()) + self.pace
            if delay:
                time.sleep(delay)
            receipt = {"url": url, "retrieved_on": datetime.now(timezone.utc).date().isoformat()}
            try:
                request = Request(url, headers={"User-Agent": "Triptych-papal-documents/1.0 (+https://github.com/spincyc/triptych)", "Accept-Encoding": "identity"})
                with urlopen(request, timeout=self.timeout) as response:
                    raw = response.read()
                    expected = response.headers.get("Content-Length")
                    if expected and int(expected) != len(raw):
                        raise ValueError(f"incomplete HTTP response: {url}")
                    if not raw:
                        raise ValueError(f"empty HTTP response: {url}")
                    receipt.update(status="ok", http_status=response.status, final_url=normalize_url(response.url),
                                   sha256=hashlib.sha256(raw).hexdigest(), byte_size=len(raw))
                payload_path.write_bytes(raw)
                receipt_path.write_text(json.dumps(receipt, sort_keys=True, indent=2) + "\n")
                return raw, receipt
            except HTTPError as exc:
                receipt.update(status="not-found" if exc.code == 404 else "http-error", http_status=exc.code)
                exc.close()
                if exc.code not in {429, 500, 502, 503, 504} or attempt == 2:
                    break
            except (OSError, URLError, ValueError) as exc:
                receipt.update(status="fetch-error", error=type(exc).__name__)
                if attempt == 2:
                    break
            time.sleep(1 + attempt)
        receipt_path.write_text(json.dumps(receipt, sort_keys=True, indent=2) + "\n")
        return None, receipt


def index_links(links, pope, interface, include_letters=False):
    categories = set(CATEGORIES) | ({"letters"} if include_letters else set())
    base = f"/content/{pope}/{interface}"
    found = []
    for target in links:
        path = urlsplit(target).path
        suffix = path.removeprefix(base)
        if not path.startswith(base):
            continue
        if pope in HISTORICAL and re.fullmatch(r"\.index(?:\.[a-z0-9_-]+)*\.html", suffix):
            found.append(target)
        elif any(re.fullmatch(r"/" + re.escape(category) + r"\.index(?:\.[a-z0-9_-]+)*\.html", suffix) for category in categories):
            found.append(target)
    return sorted(set(found))


def validate_overrides(overrides):
    if not overrides:
        return {"schema": OVERRIDES_SCHEMA, "aliases": [], "records": {}}
    if overrides.get("schema") != OVERRIDES_SCHEMA:
        raise ValueError("unsupported papal override schema")
    for alias in overrides.get("aliases", []):
        urls = alias.get("urls", [])
        if len(set(urls)) < 2 or not alias.get("evidence"):
            raise ValueError("reviewed aliases require at least two exact URLs and evidence")
        for url in urls:
            if normalize_url(url) != url:
                raise ValueError("reviewed alias URL must be canonical")
        if not re.fullmatch(r"papal\.[a-z0-9-]+\.[a-z0-9-]+", alias.get("canonical_id", "")):
            raise ValueError("reviewed aliases require a stable canonical_id")
        owners = {urlsplit(url).path.split("/")[2] for url in urls if urlsplit(url).path.startswith("/content/")}
        if len(owners) != 1 or not alias["canonical_id"].startswith("papal." + next(iter(owners)) + "."):
            raise ValueError("reviewed aliases must preserve the pontiff identity")
    for key, values in overrides.get("records", {}).items():
        if not isinstance(values, dict) or set(values) - OVERRIDE_FIELDS:
            raise ValueError(f"unsupported record override fields: {key}")
        if values.get("record_role", "whole-work") not in RECORD_ROLES:
            raise ValueError(f"unsupported record role: {key}")
        if {"source_work_id", "delivery_ownership"}.intersection(values):
            if (not re.fullmatch(r"work\.[a-z0-9.-]+", str(values.get("source_work_id", "")))
                    or not isinstance(values.get("delivery_ownership"), dict)
                    or not values["delivery_ownership"]):
                raise ValueError(f"compound delivery requires a canonical child and controller: {key}")
            for language, controller in values["delivery_ownership"].items():
                if (not re.fullmatch(r"[a-z][a-z0-9_]*", language)
                        or not isinstance(controller, dict)
                        or not re.fullmatch(r"work\.[a-z0-9.-]+", str(controller.get("container_work_id", "")))
                        or not re.fullmatch(r"artifact\.[a-z0-9.-]+", str(controller.get("artifact_id", "")))
                        or not re.fullmatch(r"[a-f0-9]{64}", str(controller.get("source_sha256", "")))
                        or not isinstance(controller.get("reason"), str) or not controller["reason"].strip()
                        or not isinstance(controller.get("source_url"), str)):
                    raise ValueError(f"compound delivery requires exact owner, source hash and reason: {key}")
                if normalize_url(controller["source_url"]) != controller["source_url"]:
                    raise ValueError(f"compound delivery URL must be canonical: {key}")
        attribution = {"source_unit_identity", "source_responsible", "display_responsible", "source_work_type"}
        if attribution.intersection(values):
            unit = values.get("source_unit_identity")
            if (not attribution.issubset(values) or not isinstance(unit, dict)
                    or unit.get("kind") != "related-regulation"
                    or any(not isinstance(unit.get(field), str) or not unit[field].strip()
                           for field in ("source_url", "locus", "basis"))
                    or values["source_work_type"] != "curial-regulation"
                    or any(not isinstance(values[field], str) or not values[field].strip()
                           for field in ("source_responsible", "display_responsible"))):
                raise ValueError(f"related regulation requires its own attribution and source proof: {key}")
        for value_name, proof_name in (("resolved_date", "date_resolution"), ("resolved_title", "title_resolution")):
            if (value_name in values) != (proof_name in values):
                raise ValueError(f"{value_name} requires its source proof: {key}")
            if value_name in values and not isinstance(values[proof_name], dict):
                raise ValueError(f"{proof_name} must be a primary-source evidence object: {key}")
            if value_name in values and not (values[proof_name].get("source_url") and values[proof_name].get("locus")):
                raise ValueError(f"{proof_name} must identify the primary source and exact locus: {key}")
            if value_name in values and values[proof_name].get("source_sha256") and not re.fullmatch(r"[a-f0-9]{64}", values[proof_name]["source_sha256"]):
                raise ValueError(f"invalid primary-source hash: {key}")
        if "resolved_date" in values:
            date.fromisoformat(values["resolved_date"])
    return overrides


def merge_rows(rows, previous=None, overrides=None):
    """Use explicit URL/file aliases; repeated incipits are never identities."""
    overrides = validate_overrides(overrides)
    parents = list(range(len(rows)))
    def find(i):
        while parents[i] != i:
            parents[i] = parents[parents[i]]
            i = parents[i]
        return i
    aliases, prior_ids, prior_unlinked, reviewed_urls = {}, {}, {}, {}
    for alias in overrides.get("aliases", []):
        for url in alias["urls"]:
            if url in reviewed_urls and reviewed_urls[url] != alias["canonical_id"]:
                raise ValueError("reviewed alias URL has conflicting canonical identities")
            reviewed_urls[url] = alias["canonical_id"]
    for document in (previous or {}).get("documents", []):
        for url in [*document.get("languages", {}).values(), *document.get("url_aliases", [])]:
            prior_ids[url] = document["id"]
        if not document.get("languages"):
            for source_url in document["source_index_urls"]:
                prior_unlinked[(source_url, document["index_title_raw"])] = document["id"]
    for i, row in enumerate(rows):
        pope = row["pope_id"]
        if not row["languages"]:
            key = (pope, row["source_index_url"], row["index_title_raw"])
            if key in aliases:
                parents[find(i)] = find(aliases[key])
            else:
                aliases[key] = i
        for url in row["languages"].values():
            keys = [url, (pope, filename_identity(url))]
            if url in reviewed_urls:
                keys.append(("reviewed-alias", reviewed_urls[url]))
            for key in keys:
                if key in aliases:
                    parents[find(i)] = find(aliases[key])
                else:
                    aliases[key] = i
    groups = {}
    for i, row in enumerate(rows):
        groups.setdefault(find(i), []).append(row)
    documents = []
    for group in groups.values():
        group.sort(key=lambda row: (not ("/en/" in row["source_index_url"] or "/en." in row["source_index_url"]), row["source_index_url"], row["index_title_raw"]))
        first = group[0]
        languages, language_conflicts, edition_aliases = {}, [], {}
        for row in group:
            for lang, url in row["languages"].items():
                if lang in languages and languages[lang] != url:
                    if filename_identity(languages[lang]) == filename_identity(url):
                        edition_aliases.setdefault(lang, set()).update((languages[lang], url))
                    else:
                        language_conflicts.append({"language": lang, "urls": sorted({languages[lang], url})})
                else:
                    languages[lang] = url
        all_urls = [url for row in group for url in row["languages"].values()]
        # A title with no linked edition is retained as an unresolved index row.
        seed_url = next((languages[lang] for lang in ("en", "la", "it") if lang in languages), next(iter(languages.values()), ""))
        tail = Path(urlsplit(seed_url).path).stem if seed_url else "unlinked-" + hashlib.sha256((first["source_index_url"] + "\n" + first["index_title_raw"]).encode()).hexdigest()[:16]
        old_ids = sorted({prior_ids[url] for url in all_urls if url in prior_ids})
        if not all_urls:
            old_ids = sorted({prior_unlinked[(row["source_index_url"], row["index_title_raw"])] for row in group if (row["source_index_url"], row["index_title_raw"]) in prior_unlinked})
        identity = old_ids[0] if old_ids else f"papal.{first['pope_id']}.{slug(tail)}"
        reviewed_ids = {reviewed_urls[url] for url in all_urls if url in reviewed_urls}
        if len(reviewed_ids) > 1:
            raise ValueError("reviewed aliases join conflicting canonical identities")
        if reviewed_ids:
            identity = next(iter(reviewed_ids))
        dates = sorted({row["date"] for row in group if row["date"]})
        filename_date = date_from_filename(seed_url) if seed_url else None
        kind_candidates = sorted({row["document_type"] for row in group if row["document_type"] != "other"})
        kind = first["document_type"] if first["document_type"] != "other" else (kind_candidates[0] if kind_candidates else "other")
        document = {
            "id": identity, "pope_id": first["pope_id"], "pope": POPE_NAMES[first["pope_id"]],
            "title": first["title"], "date": dates[0] if len(dates) == 1 else None,
            "date_raw": first["date_raw"], "date_basis": "index-title" if len(dates) == 1 else "unresolved",
            "index_title_raw": first["index_title_raw"], "document_type": kind,
            "document_types": kind_candidates or ["other"],
            "source_index_urls": sorted({row["source_index_url"] for row in group}),
            "languages": dict(sorted(languages.items())),
            "url_aliases": sorted(set(all_urls)),
            "record_role": "whole-work",
        }
        historic_ids = {alias for old in (previous or {}).get("documents", []) if old["id"] in old_ids for alias in old.get("identity_aliases", [])}
        document["identity_aliases"] = sorted((set(old_ids) | historic_ids) - {identity})
        if not dates and filename_date:
            document.update(date=filename_date, date_basis="filename-unverified")
        if len(dates) > 1:
            document["date_conflicts"] = [{"date": row["date"], "date_raw": row["date_raw"], "source_index_url": row["source_index_url"]} for row in group if row["date"]]
        if language_conflicts:
            document["language_url_conflicts"] = language_conflicts
        if edition_aliases:
            document["edition_url_aliases"] = {lang: sorted(values) for lang, values in sorted(edition_aliases.items())}
        if not languages:
            document["availability"] = "index-row-without-linked-edition"
        document["index_titles"] = sorted({row["index_title_raw"] for row in group})
        matching = {identity, *document["identity_aliases"], *all_urls}
        for key, values in overrides.get("records", {}).items():
            if key in matching:
                for name, value in values.items():
                    if name in document and name in OVERRIDE_FIELDS and document[name] not in (value, "whole-work"):
                        raise ValueError(f"contradictory reviewed metadata for {identity}: {name}")
                    document[name] = value
        matched_aliases = [entry for entry in overrides.get("aliases", []) if entry["canonical_id"] == identity]
        if matched_aliases:
            document["reviewed_aliases"] = matched_aliases
        documents.append(document)
    return sorted(documents, key=lambda row: (row.get("resolved_date") or row.get("date") or "9999", row["pope_id"], row["id"]))


def discover(cache, popes=None, workers=4, pace=.3, refresh=False, include_letters=False, previous=None, interfaces=None, overrides=None):
    selected = list(popes or POPE_NAMES)
    interfaces = list(interfaces or ("en", "it", "la"))
    fetcher = Fetcher(cache, pace=pace, refresh=refresh)
    pending = {f"{BASE}/content/{pope}/{lang}.html": (pope, lang) for pope in selected for lang in interfaces}
    seen, rows, coverage = set(), [], []
    while pending:
        batch, pending = pending, {}
        seen.update(batch)
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {pool.submit(fetcher.fetch, url): (url, info) for url, info in sorted(batch.items())}
            for future in as_completed(futures):
                url, (pope, interface) = futures[future]
                raw, receipt = future.result()
                entry = {**receipt, "pope_id": pope, "interface": interface, "rows": 0}
                if raw is not None:
                    page_rows, links = parse_index(raw, url)
                    # Modern roots feature recent documents outside the formal category boundary.
                    is_root = urlsplit(url).path == f"/content/{pope}/{interface}.html"
                    if pope in HISTORICAL or not is_root:
                        for row in page_rows:
                            row["pope_id"] = pope
                            if row["document_type"] == "other" and row["languages"]:
                                row["document_type"] = category_of(next(iter(row["languages"].values())), row["index_title_raw"])
                        rows.extend(page_rows)
                        entry["rows"] = len(page_rows)
                    entry["navigation_root"] = is_root
                    for target in index_links(links, pope, interface, include_letters):
                        if target not in seen:
                            pending[target] = (pope, interface)
                    entry["index_links_followed"] = len(index_links(links, pope, interface, include_letters))
                coverage.append(entry)
    overrides = validate_overrides(overrides)
    documents = merge_rows(rows, previous=previous, overrides=overrides)
    return {"schema": SCHEMA, "retrieved_on": datetime.now(timezone.utc).date().isoformat(),
            "scope": {"provider": "Holy See Vatican website", "pope_ids": selected,
                      "interface_languages": interfaces, "modern_categories": sorted(set(CATEGORIES) | ({"letters"} if include_letters else set())),
                      "historical_mixed_indexes": True, "all_historical_papal_documents": False,
                      "extent": "All linked rows reached from the declared Vatican navigation and index pages; not all historical papal acts, ASS/AAS contents, or Bullarium documents.",
                      "text_acquisition": "Catalog metadata only; linked full texts have not been retrieved by this command."},
            "overrides_sha256": hashlib.sha256(json.dumps(overrides, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
            "coverage": sorted(coverage, key=lambda row: row["url"]), "documents": documents}


def check_catalog(catalog):
    errors, ids, urls = [], set(), {}
    if catalog.get("schema") != SCHEMA:
        errors.append("unsupported catalog schema")
    if not isinstance(catalog.get("scope"), dict) or catalog.get("scope", {}).get("all_historical_papal_documents") is not False:
        errors.append("scope must explicitly refuse historical completeness")
    for document in catalog.get("documents", []):
        identity = document.get("id")
        if not isinstance(identity, str) or not re.fullmatch(r"papal\.[a-z0-9-]+\.[a-z0-9-]+", identity):
            errors.append(f"invalid id: {identity}")
        if identity in ids:
            errors.append(f"duplicate id: {identity}")
        ids.add(identity)
        if document.get("document_type") not in DOCUMENT_TYPES:
            errors.append(f"unknown document type: {identity}")
        if any(kind not in DOCUMENT_TYPES for kind in document.get("document_types", [])):
            errors.append(f"unknown document type membership: {identity}")
        if document.get("pope_id") not in POPE_NAMES:
            errors.append(f"unknown pope: {identity}")
        if document.get("record_role", "whole-work") not in RECORD_ROLES:
            errors.append(f"unknown source record role: {identity}")
        if document.get("resolved_date"):
            try:
                date.fromisoformat(document["resolved_date"])
                if not document.get("date_resolution"):
                    errors.append(f"resolved date has no source proof: {identity}")
            except (TypeError, ValueError):
                errors.append(f"invalid resolved date: {identity}")
        if not document.get("title") or not document.get("source_index_urls"):
            errors.append(f"missing title/index evidence: {identity}")
        if document.get("date"):
            try:
                date.fromisoformat(document["date"])
            except (TypeError, ValueError):
                errors.append(f"invalid date: {identity}")
        for lang, url in document.get("languages", {}).items():
            try:
                if normalize_url(url) != url or language_of(url) != lang:
                    errors.append(f"noncanonical edition URL: {identity}/{lang}")
            except (ValueError, TypeError):
                errors.append(f"invalid edition URL: {identity}/{lang}")
            if url in urls and urls[url] != identity:
                errors.append(f"edition URL assigned twice: {identity}")
            urls[url] = identity
    if not catalog.get("documents"):
        errors.append("catalog has no documents")
    known_indexes = {row.get("url") for row in catalog.get("coverage", []) if row.get("status") == "ok"}
    for document in catalog.get("documents", []):
        if not set(document.get("source_index_urls", [])) <= known_indexes:
            errors.append(f"unacquired index evidence: {document.get('id')}")
    return {"ok": not errors, "errors": errors, "documents": len(ids),
            "document_types": dict(sorted(Counter(row.get("document_type") for row in catalog.get("documents", [])).items())),
            "languages": dict(sorted(Counter(lang for row in catalog.get("documents", []) for lang in row.get("languages", {})).items())),
            "coverage_pages": len(catalog.get("coverage", [])),
            "failed_pages": [row["url"] for row in catalog.get("coverage", []) if row.get("status") != "ok"],
            "unresolved_dates": sum(not (row.get("resolved_date") or row.get("date")) for row in catalog.get("documents", [])),
            "raw_unresolved_dates": sum(not row.get("date") for row in catalog.get("documents", [])),
            "resolved_dates": sum(bool(row.get("resolved_date")) for row in catalog.get("documents", [])),
            "record_roles": dict(sorted(Counter(row.get("record_role", "whole-work") for row in catalog.get("documents", [])).items())),
            "filename_dates_unverified": sum(row.get("date_basis") == "filename-unverified" for row in catalog.get("documents", [])),
            "date_conflicts": sum(bool(row.get("date_conflicts")) for row in catalog.get("documents", [])),
            "discovery_complete": not any(row.get("status") != "ok" for row in catalog.get("coverage", [])),
            "unlinked_rows": sum(not row.get("languages") for row in catalog.get("documents", []))}


def parser(examples=None):
    result = argparse.ArgumentParser(description="Discover and inspect Vatican papal-document index metadata.",
        epilog="examples (real invocations; `make check-examples` replays each one):\n  $ tools/papal-documents check --help\n  $ tools/papal-documents list --help", formatter_class=argparse.RawDescriptionHelpFormatter)
    from _tooling import examples_live_on_the_verbs, with_examples
    examples_live_on_the_verbs(result, "papal-documents")
    subparsers = result.add_subparsers(dest="verb", required=True)
    for verb in ("discover", "check", "list", "show", "export"):
        p = subparsers.add_parser(verb, epilog=f"examples (real invocations; `make check-examples` replays each one):\n  $ tools/papal-documents {verb} --help\n  $ tools/papal-documents --help", formatter_class=argparse.RawDescriptionHelpFormatter)
        if examples is not None:
            with_examples(p, examples.get(verb, ()))
        p.add_argument("--catalog", type=Path, default=ROOT / "src/sources/papal-documents/catalog.json")
        p.add_argument("--json", action="store_true", help="print machine-readable output")
        if verb == "discover":
            p.add_argument("--cache", type=Path, default=ROOT / ".scratch/papal-documents/indexes")
            p.add_argument("--pope", choices=POPE_NAMES, action="append")
            p.add_argument("--interface", choices=("en", "it", "la"), action="append", help="index interface to crawl (repeatable; default: en, it, la)")
            p.add_argument("--workers", type=int, default=4)
            p.add_argument("--pace", type=float, default=.3, help="minimum seconds between request starts")
            p.add_argument("--refresh", action="store_true", help="retrieve new index snapshots instead of using cached exact bytes")
            p.add_argument("--include-letters", action="store_true", help="also follow ordinary letter indexes")
            p.add_argument("--overrides", type=Path, default=ROOT / "src/sources/papal-documents/overrides.json", help="reviewed exact-URL aliases, source bounds, and primary-source date resolutions")
        if verb in {"list", "show", "export"}:
            p.add_argument("--pope", choices=POPE_NAMES)
            p.add_argument("--type", choices=sorted(DOCUMENT_TYPES), dest="kind")
            p.add_argument("--language", help="preferred reading edition" if verb == "export" else "require this linked edition language")
        if verb in {"show", "export"}:
            p.add_argument("--document", required=verb == "show")
        if verb == "export":
            p.add_argument("--format", choices=("json", "csv", "biblatex", "beamer"), required=True)
            p.add_argument("--out", type=Path)
    return result


def main(argv=None, examples=None):
    args = parser(examples).parse_args(argv)
    try:
        if args.verb == "discover":
            if not 1 <= args.workers <= 8 or args.pace < 0:
                raise ValueError("workers must be 1..8 and pace must be nonnegative")
            previous = json.loads(args.catalog.read_text()) if args.catalog.exists() else None
            overrides = json.loads(args.overrides.read_text()) if args.overrides.exists() else None
            catalog = discover(args.cache, args.pope, args.workers, args.pace, args.refresh, args.include_letters, previous, args.interface, overrides)
            report = check_catalog(catalog)
            if report["errors"]:
                raise ValueError("; ".join(report["errors"][:10]))
            args.catalog.parent.mkdir(parents=True, exist_ok=True)
            args.catalog.write_text(json.dumps(catalog, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
            payload = {"catalog": str(args.catalog), **report}
        else:
            catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
            report = check_catalog(catalog)
            if not report["ok"]:
                raise ValueError("; ".join(report["errors"][:10]))
            if args.verb == "check":
                payload = report
            else:
                rows = [row for row in catalog["documents"] if (not args.pope or row["pope_id"] == args.pope) and (not args.kind or args.kind in row.get("document_types", [row["document_type"]])) and (args.verb == "export" or not args.language or args.language in row["languages"])]
                if args.verb == "export":
                    from _papal_exports import export_catalog
                    if args.document:
                        rows = [row for row in rows if args.document in [row["id"], *row.get("identity_aliases", [])]]
                        if len(rows) != 1:
                            raise ValueError("document does not resolve to exactly one catalog row")
                    result = export_catalog({**catalog, "documents": rows}, args.format, language=args.language or "en")
                    if args.out:
                        args.out.parent.mkdir(parents=True, exist_ok=True)
                        args.out.write_text(result, encoding="utf-8")
                        print(json.dumps({"out": str(args.out), "documents": len(rows)}, sort_keys=True) if args.json else f"Exported {len(rows)} documents.")
                    else:
                        print(result, end="" if result.endswith("\n") else "\n")
                    return 0
                if args.verb == "show":
                    rows = [row for row in rows if args.document in [row["id"], *row.get("identity_aliases", [])]]
                    if len(rows) != 1:
                        raise ValueError("document does not resolve to exactly one catalog row")
                    payload = rows[0]
                else:
                    payload = {"documents": rows, "count": len(rows)}
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        elif args.verb in {"check", "discover"}:
            print(f"{payload['documents']} documents; {payload['coverage_pages']} index pages; {len(payload['failed_pages'])} failed pages; {payload['unresolved_dates']} unresolved dates.")
            for kind, count in payload["document_types"].items():
                print(f"  {kind}: {count}")
        elif args.verb == "list":
            for row in payload["documents"]:
                kinds = " / ".join(row.get("document_types", [row["document_type"]]))
                shown_date = row.get("resolved_date") or row["date"] or "undated"
                shown_title = row.get("resolved_title") or row["title"]
                print(f"{shown_date}  {row['pope']}  {kinds}  {shown_title}  {row['id']}")
        else:
            print(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        payload = {"ok": False, "error": str(exc)}
        print(json.dumps(payload, sort_keys=True) if args.json else f"papal-documents: {exc}", file=sys.stdout if args.json else sys.stderr)
        return 2
