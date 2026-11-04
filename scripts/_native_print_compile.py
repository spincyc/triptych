"""Compile every admitted native print edition from its source bundle alone.

`prepare` materializes the exact source transports the Pages build publishes
under `native-tex/sources/` for the whole admitted print universe, and refuses
when the admitted and materialized sets differ. `compile` then typesets each
edition with the engine its bundle names, under the browser's compilation
policy in `src/web/browser/shared/native-tex.js`: at least two passes, at most
the bundle's maximum, settled auxiliary files, and the same fatal-log patterns.

The gate is fail-closed. An edition fails when its engine fails, no PDF is
produced, it does not settle within the maximum passes, or it opens any file
that is neither inside its own bundle (or written by its own compilation) nor
a member of the pinned browser runtime's `texFiles` by name. Only `texmf.cnf`,
the kpathsea `ls-R` databases and the engine's own format file are exempt,
because the browser runtime ships those itself. XeTeX resolves font families
through a fontconfig configuration that contains only the runtime's OpenType
faces, and the XeTeX PDF driver's file reads are traced through kpathsea, so a
font the browser lacks fails here instead of on a reader's machine.

The native engines are not the WebAssembly engines, so a pass here proves the
bundle and runtime closure, not byte identity with a browser-generated PDF.
No PDF is retained or published; each edition leaves a JSON receipt.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import resource
import shutil
import subprocess
import sys
import threading
import time
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
INDEX_SCHEMA = "triptych-native-print-compile-index/v1"
RECEIPT_SCHEMA = "triptych-native-print-compile-receipt/v1"
SUMMARY_SCHEMA = "triptych-native-print-compile-summary/v1"
RUNTIME_SCHEMA = "triptych-native-tex-runtime/v1"
RUNTIME = "src/common/native-tex-runtime.json"
DEFAULT_OUT = ".scratch/native-print-compile"
# The only compilation policy the browser accepts (native-tex.js
# sourceRenderIdentity); `_native_print_bundles.validate_bundle` pins the same.
OPTIONS = {"shell_escape": False, "minimum_passes": 2, "max_passes": 8, "settle_auxiliary_files": True}
ENGINES = {"pdftex": "pdflatex", "xetex": "xelatex"}
EDITION_SECONDS = 20 * 60
# Browser parity: the files whose identities decide that a pass settled, and
# the log conditions that reject a pass outright or demand another. The browser
# applies both to the engine's terminal output (the WASM worker's stdout and
# stderr), never to the `.log` file, whose font-information lines would let the
# 300-character font-shape window reach an ordinary first-pass "undefined"
# reference warning; this gate reads the same stream.
AUXILIARY = re.compile(r"\.(aux|toc|out|lof|lot|lol|ent|idx|ind|bbl|bcf|nav|snm)$")
FATAL = re.compile(
    r"(?:^|\n)!|Fatal error|Emergency stop|no output PDF file|Missing character:|Font .*not loadable"
    r"|font .*not found|Font shape[\s\S]{0,300}?undefined|Some font shapes were not available,\s*defaults substituted",
    re.IGNORECASE)
UNSETTLED = re.compile(
    r"undefined references|undefined citations|There were undefined|Rerun to get|Label\(s\) may have changed"
    r"|Please (?:re)?run|Rerun .*get .*right", re.IGNORECASE)
# Read by every native engine before any document input, and supplied by the
# browser runtime's own engine packaging rather than its `texFiles`.
INFRASTRUCTURE = frozenset({"texmf.cnf", "ls-R"})
# The runtime registers some members only under their kpathsea lookup name
# (`ecrm1095`, format 3), so an opened file also matches by stem when its
# extension is the one kpathsea gives that member's format.
EXTENSION_FORMATS = {".tfm": 3, ".tex": 26, ".pfb": 32, ".vf": 33, ".ttf": 36, ".enc": 44, ".otf": 47, ".map": 11}
# Inherited settings that would change what the engines can find or run.
_STRIPPED_ENVIRONMENT = frozenset({
    "TEXINPUTS", "TEXMFHOME", "TEXMFAUXTREES", "TEXMFDOTDIR", "BIBINPUTS", "BSTINPUTS", "TFMFONTS",
    "T1FONTS", "ENCFONTS", "OPENTYPEFONTS", "TTFONTS", "VFFONTS", "TEXFONTMAPS", "TEXPSHEADERS",
    "MISCFONTS", "FONTCONFIG_FILE", "FONTCONFIG_PATH", "FONTCONFIG_SYSROOT", "KPATHSEA_DEBUG",
    "SOURCE_DATE_EPOCH", "FORCE_SOURCE_DATE", "shell_escape", "shell_escape_commands",
    "openin_any", "openout_any"})
_FOPEN = re.compile(r"^kdebug:fopen\((.*), ([rwab+]+)\) => (?!\(nil\)|0x0\b)\S+")
_HASH = re.compile(r"[0-9a-f]{64}\Z")
_REVISION = re.compile(r"[0-9a-f]{40}\Z")


class CompileError(ValueError):
    """The prepared work tree, its index or the runtime cannot be trusted."""


def _need(condition, message):
    if not condition:
        raise CompileError(message)


def _sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _write_json(path: Path, value) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, indent=1, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def directory_name(identity: str) -> str:
    """A collision-free, readable directory for one output identity."""
    slug = re.sub(r"[^A-Za-z0-9._-]+", "_", identity).strip("._-")[:80]
    return slug + "-" + _sha(identity.encode("utf-8"))[:12]


def _relative(value) -> str:
    _need(isinstance(value, str) and value and not value.startswith("/") and "\\" not in value
          and "\0" not in value and all(part not in {"", ".", ".."} for part in value.split("/"))
          and PurePosixPath(value).as_posix() == value, "unsafe path in prepared native bundle")
    return value


def _reset(out: Path) -> None:
    """Replace a previous preparation by this tool; never an unrelated directory."""
    if out.is_symlink():
        raise CompileError("the native print work directory must not be a symlink")
    if out.exists():
        _need(out.is_dir(), "the native print work path is not a directory")
        marker = out / "index.json"
        if marker.is_file():
            try:
                schema = json.loads(marker.read_text(encoding="utf-8")).get("schema")
            except (OSError, ValueError, AttributeError):
                schema = None
            _need(schema == INDEX_SCHEMA, "refusing to replace a directory this tool did not prepare")
            shutil.rmtree(out)
        else:
            _need(not any(out.iterdir()), "refusing to replace a non-empty directory this tool did not prepare")
    out.mkdir(parents=True, exist_ok=True)


def materialize(catalog: dict, documents: dict, out: Path, *, revision: str, epoch: int,
                scope: str = "admitted") -> dict:
    """Write each served bundle's mounted tree exactly as the browser receives it."""
    import _native_print_bundles as bundles
    _need(isinstance(catalog, dict) and catalog.get("schema") == bundles.CATALOG_SCHEMA,
          "unsupported native source catalog")
    _need(catalog.get("source_revision") == revision and _REVISION.fullmatch(revision or ""),
          "native source catalog names a different source revision")
    admitted, prepared = set(documents), set(catalog["bundles"])
    _need(admitted, "no native print edition is admitted")
    _need(admitted == prepared, "admitted and prepared native print editions differ: missing "
          + json.dumps(sorted(admitted - prepared)) + ", unadmitted " + json.dumps(sorted(prepared - admitted)))
    _reset(out)
    assets = catalog["assets"]
    editions = {}
    for identity in sorted(admitted):
        described = catalog["bundles"][identity]
        route = described["route"]
        payload = assets.get(route)
        _need(isinstance(payload, bytes) and len(payload) == described["bytes"]
              and _sha(payload) == described["sha256"], "served native bundle does not match its route: " + identity)
        bundle = bundles.validate_bundle(json.loads(payload))
        _need(bundle["output_id"] == identity and bundle["source_revision"] == revision,
              "served native bundle names a different output or revision: " + identity)
        _need(bundle["engine"] in ENGINES and bundle["format"] == ENGINES[bundle["engine"]]
              and bundle["options"] == OPTIONS, "unsupported native compilation contract: " + identity)
        cwd, entrypoint = _relative(bundle["cwd"]), _relative(bundle["entrypoint"])
        _need(entrypoint.startswith(cwd + "/"), "native entrypoint is outside its working directory: " + identity)
        environment = bundle.get("environment", {})
        _need(isinstance(environment, dict) and set(environment) <= {"TEXINPUTS"}
              and all(isinstance(value, str) for value in environment.values()),
              "unsupported native bundle environment: " + identity)
        name = directory_name(identity)
        base = out / "editions" / name
        files = {}
        for row in bundle["files"]:
            path = _relative(row["path"])
            if row["encoding"] == "url":
                body = assets.get(posixpath.normpath(posixpath.join(posixpath.dirname(route), row["href"])))
                _need(isinstance(body, bytes) and len(body) == row["bytes"] and _sha(body) == row["sha256"],
                      "served native asset does not match its bundle record: " + identity + " " + path)
            else:
                body = bundles.file_bytes(row)
            target = base / path
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as handle:
                handle.write(body)
            files[path] = row["sha256"]
        _need(entrypoint in files, "native bundle lacks its entrypoint: " + identity)
        (base / cwd).mkdir(parents=True, exist_ok=True)
        editions[identity] = {"directory": name, "engine": bundle["engine"], "format": bundle["format"],
                              "cwd": cwd, "entrypoint": entrypoint, "environment": environment,
                              "options": bundle["options"], "bundle_route": route,
                              "bundle_sha256": described["sha256"], "bundle_bytes": described["bytes"],
                              "render_sha256": bundle.get("render_sha256"), "files": files}
    index = {"schema": INDEX_SCHEMA, "scope": scope, "source_revision": revision,
             "source_date_epoch": epoch, "admitted": sorted(admitted), "editions": editions}
    _write_json(out / "index.json", index)
    return index


def prepare(root: Path, out: Path, *, only=()) -> dict:
    """Prepare the admitted universe (or an explicit subset) through the bundle API."""
    from _native_print import admitted_documents, source_revision
    import _native_print_bundles as bundles
    root = Path(root).resolve()
    documents = admitted_documents(root)
    revision = source_revision(root)
    selected = sorted(set(only))
    for identity in selected:
        _need(identity in documents, "not an admitted native print edition: " + identity)
    try:
        epoch = int(subprocess.run(["git", "show", "-s", "--format=%ct", revision], cwd=root, check=True,
                                   capture_output=True, text=True).stdout.strip())
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        raise CompileError("cannot read the source revision's commit time") from error
    catalog = bundles.prepare_catalog(root, documents=documents, revision=revision,
                                      output_ids=selected or None)
    wanted = {identity: documents[identity] for identity in selected} if selected else documents
    return materialize(catalog, wanted, out, revision=revision, epoch=epoch,
                       scope="selected" if selected else "admitted")


def load_runtime(path: Path) -> dict:
    try:
        runtime = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise CompileError("cannot read the native TeX runtime manifest") from error
    _need(isinstance(runtime, dict) and runtime.get("schema") == RUNTIME_SCHEMA
          and isinstance(runtime.get("texFiles"), list) and runtime["texFiles"],
          "unsupported native TeX runtime manifest")
    members = {}
    for row in runtime["texFiles"]:
        _need(isinstance(row, dict) and isinstance(row.get("name"), str) and row["name"]
              and "/" not in row["name"] and _HASH.fullmatch(row.get("sha256", ""))
              and type(row.get("format")) is int, "invalid native TeX runtime member")
        member = members.setdefault(row["name"], {"formats": set(), "sha256": set()})
        member["formats"].add(row["format"])
        member["sha256"].add(row["sha256"])
    return {"id": runtime.get("id", ""), "members": members,
            "fonts": sorted(name for name in members if name.lower().endswith((".otf", ".ttf")))}


def runtime_member(runtime: dict, name: str) -> dict | None:
    """The runtime member an opened basename resolves to, by name or lookup stem."""
    member = runtime["members"].get(name)
    if member is not None:
        return member
    stem, extension = os.path.splitext(name)
    member = runtime["members"].get(stem)
    if member is not None and EXTENSION_FORMATS.get(extension.lower()) in member["formats"]:
        return member
    return None


def parse_recorder(path: Path, cwd: Path) -> tuple[set[str], set[str]]:
    """Absolute normalized (reads, writes) from one `-recorder` file list."""
    reads, writes, pwd = set(), set(), str(cwd)
    if not path.is_file():
        return reads, writes
    for line in path.read_text(encoding="utf-8", errors="surrogateescape").splitlines():
        kind, _, value = line.partition(" ")
        if kind == "PWD":
            pwd = value
        elif kind in {"INPUT", "OUTPUT"}:
            (reads if kind == "INPUT" else writes).add(os.path.normpath(os.path.join(pwd, value)))
    return reads, writes


def parse_fopen_trace(text: str, cwd: Path) -> tuple[set[str], set[str]]:
    """Successful opens from a `KPATHSEA_DEBUG=4` trace, as (reads, writes)."""
    reads, writes = set(), set()
    for line in text.splitlines():
        found = _FOPEN.match(line)
        if found:
            path = os.path.normpath(os.path.join(str(cwd), found.group(1)))
            (writes if set(found.group(2)) & {"w", "a"} else reads).add(path)
    return reads, writes


def auxiliary_state(base: Path) -> str:
    """The identity native-tex.js compares between passes: every auxiliary file."""
    rows = []
    for path in sorted(base.rglob("*")):
        if path.is_file() and AUXILIARY.search(path.name):
            rows.append([path.relative_to(base).as_posix(), _file_sha(path)])
    return _sha(json.dumps(rows, separators=(",", ":")).encode("utf-8"))


def _clean_environment(extra: dict) -> dict:
    environment = {key: value for key, value in os.environ.items() if key not in _STRIPPED_ENVIRONMENT}
    environment.update({"shell_escape": "f", "openout_any": "p", "LC_ALL": "C.UTF-8"})
    environment.update(extra)
    return environment


class Gate:
    """One compile run over a prepared work tree."""

    def __init__(self, out: Path, runtime: dict):
        self.out = out
        self.runtime = runtime
        self.hashes: dict[str, str] = {}
        self.lock = threading.Lock()

    def host_sha(self, path: str) -> str | None:
        with self.lock:
            known = self.hashes.get(path)
        if known is None:
            try:
                known = _file_sha(Path(path))
            except OSError:
                return None
            with self.lock:
                self.hashes[path] = known
        return known

    def closure(self, reads, writes, base: Path, files: dict, engine_format: str):
        """Violations, and runtime members whose host bytes differ (informational)."""
        violations, differing, runtime_opened, bundle_opened = [], set(), set(), set()
        prefix = str(base) + os.sep
        exempt = INFRASTRUCTURE | {engine_format + ".fmt"}
        for path in sorted(reads):
            if path.startswith(prefix):
                relative = path[len(prefix):].replace(os.sep, "/")
                if relative in files:
                    bundle_opened.add(relative)
                elif path not in writes:
                    violations.append("opened a work-tree file outside the bundle: " + relative)
                continue
            if path in writes:
                continue
            name = os.path.basename(path)
            if name in exempt:
                continue
            member = runtime_member(self.runtime, name)
            if member is None:
                violations.append("opened a file outside the bundle and the runtime: " + path)
                continue
            runtime_opened.add(name)
            digest = self.host_sha(path)
            if digest is not None and digest not in member["sha256"]:
                differing.add(name)
        return violations, differing, len(runtime_opened), len(bundle_opened)

    def compile(self, identity: str, edition: dict, environment: dict) -> dict:
        started = time.monotonic()
        base = self.out / "editions" / edition["directory"]
        cwd = base / edition["cwd"]
        entry = os.path.relpath(base / edition["entrypoint"], cwd)
        stem = os.path.splitext(os.path.basename(entry))[0]
        engine = edition["engine"]
        binary = ENGINES[engine]
        maximum = edition["options"]["max_passes"]
        minimum = edition["options"]["minimum_passes"]
        extra = {"SOURCE_DATE_EPOCH": str(environment["SOURCE_DATE_EPOCH"])}
        if "TEXINPUTS" in edition["environment"]:
            extra["TEXINPUTS"] = edition["environment"]["TEXINPUTS"]
        if engine == "xetex":
            extra["FONTCONFIG_FILE"] = str(self.out / "fonts.conf")
            extra["XDG_CACHE_HOME"] = str(self.out / "font-cache")
        env = _clean_environment(extra)
        reads, writes, problems = set(), set(), []
        output, passes, settled, previous = "", 0, False, None
        for passes in range(1, maximum + 1):
            remaining = EDITION_SECONDS - (time.monotonic() - started)
            argv = [binary, "-recorder", "-no-shell-escape", "-interaction=nonstopmode",
                    "-halt-on-error", "-file-line-error"] + (["-no-pdf"] if engine == "xetex" else []) + [entry]
            try:
                run = subprocess.run(argv, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                     timeout=max(remaining, 1))
            except subprocess.TimeoutExpired:
                problems.append(f"pass {passes} exceeded the {EDITION_SECONDS}-second edition limit")
                break
            except OSError as error:
                problems.append(f"cannot run {binary}: {error}")
                break
            found_reads, found_writes = parse_recorder(cwd / (stem + ".fls"), cwd)
            reads |= found_reads
            writes |= found_writes
            output = run.stdout.decode("utf-8", "replace")
            if run.returncode != 0:
                problems.append(f"{binary} exited {run.returncode} on pass {passes}")
                break
            fatal = FATAL.search(output)
            if fatal:
                problems.append(f"pass {passes} output reports: " + fatal.group(0).strip()[:200])
                break
            product = cwd / (stem + (".xdv" if engine == "xetex" else ".pdf"))
            if not product.is_file():
                problems.append(f"pass {passes} produced no {product.suffix[1:].upper()} output")
                break
            current = auxiliary_state(base)
            if passes >= minimum and current == previous and not UNSETTLED.search(output):
                settled = True
                break
            previous = current
        if not problems and not settled:
            problems.append(f"references or contents did not settle within {maximum} passes")
        pdf = cwd / (stem + ".pdf")
        if not problems and engine == "xetex":
            trace_env = dict(env, KPATHSEA_DEBUG="4")
            try:
                driver = subprocess.run(["xdvipdfmx", "-q", "-E", "-o", pdf.name, stem + ".xdv"], cwd=cwd,
                                        env=trace_env, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                        stderr=subprocess.PIPE, timeout=max(EDITION_SECONDS - (time.monotonic() - started), 1))
                trace = driver.stderr.decode("utf-8", "replace")
                driver_reads, driver_writes = parse_fopen_trace(trace, cwd)
                reads |= driver_reads
                writes |= driver_writes
                messages = "\n".join(line for line in trace.splitlines() if not line.startswith("kdebug:"))
                fatal = FATAL.search(messages)
                if driver.returncode != 0:
                    problems.append(f"xdvipdfmx exited {driver.returncode}")
                elif fatal:
                    problems.append("xdvipdfmx reports: " + fatal.group(0).strip()[:200])
                output += "\n" + messages
            except (OSError, subprocess.TimeoutExpired) as error:
                problems.append("the XeTeX PDF driver failed: " + str(error))
        pages = pdf_sha = pdf_bytes = None
        if not problems:
            if not pdf.is_file() or pdf.read_bytes()[:5] != b"%PDF-":
                problems.append("no PDF was produced")
            else:
                pdf_sha, pdf_bytes = _file_sha(pdf), pdf.stat().st_size
                try:
                    info = subprocess.run(["pdfinfo", pdf.name], cwd=cwd, capture_output=True, text=True,
                                          timeout=120)
                    found = re.search(r"^Pages:\s+(\d+)\s*$", info.stdout, re.M)
                    pages = int(found.group(1)) if info.returncode == 0 and found else None
                except (OSError, subprocess.TimeoutExpired):
                    pages = None
                if not pages:
                    problems.append("pdfinfo could not read a positive page count")
        violations, differing, runtime_opened, bundle_opened = self.closure(
            reads, writes, base, edition["files"], edition["format"])
        problems.extend(violations)
        receipt = {"schema": RECEIPT_SCHEMA, "id": identity, "engine": engine, "format": edition["format"],
                   "status": "fail" if problems else "pass", "passes": passes, "pages": pages,
                   "pdf_sha256": pdf_sha, "pdf_bytes": pdf_bytes,
                   "seconds": round(time.monotonic() - started, 2),
                   "bundle_sha256": edition["bundle_sha256"], "render_sha256": edition["render_sha256"],
                   "closure": {"bundle_files": len(edition["files"]), "bundle_files_opened": bundle_opened,
                               "runtime_members_opened": runtime_opened,
                               "runtime_members_with_other_host_bytes": sorted(differing)},
                   "problems": problems}
        if problems:
            receipt["output_tail"] = output.splitlines()[-40:]
        return receipt


def _fonts(out: Path, runtime: dict) -> int:
    """A fontconfig world holding only the runtime's OpenType faces, by name."""
    fonts = out / "fonts"
    fonts.mkdir()
    (out / "font-cache").mkdir()
    located = 0
    if runtime["fonts"] and shutil.which("kpsewhich"):
        found = subprocess.run(["kpsewhich", *runtime["fonts"]], capture_output=True, text=True,
                               env=_clean_environment({}), timeout=300).stdout.splitlines()
        for path in found:
            name = os.path.basename(path)
            if name in runtime["members"] and not (fonts / name).exists():
                (fonts / name).symlink_to(os.path.realpath(path))
                located += 1
    (out / "fonts.conf").write_text(
        '<?xml version="1.0"?>\n<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">\n<fontconfig>\n'
        f"  <dir>{escape(str(fonts))}</dir>\n  <cachedir>{escape(str(out / 'font-cache'))}</cachedir>\n"
        "</fontconfig>\n", encoding="utf-8")
    if shutil.which("fc-cache"):
        subprocess.run(["fc-cache", str(fonts)], env=_clean_environment({"FONTCONFIG_FILE": str(out / "fonts.conf")}),
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=300)
    return located


def _version(binary: str) -> str:
    try:
        return subprocess.run([binary, "--version"], capture_output=True, text=True,
                              timeout=60).stdout.splitlines()[0].strip()
    except (OSError, IndexError, subprocess.TimeoutExpired):
        return ""


def compile_all(out: Path, *, runtime_path: Path, jobs: int) -> dict:
    out = Path(out).resolve()
    try:
        index = json.loads((out / "index.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise CompileError("no prepared native print work tree; run prepare first") from error
    _need(isinstance(index, dict) and index.get("schema") == INDEX_SCHEMA
          and index.get("scope") in {"admitted", "selected"}, "unsupported native print work index")
    editions = index["editions"]
    _need(isinstance(editions, dict) and sorted(editions) == index["admitted"],
          "admitted and materialized native print editions differ")
    _need(editions, "the prepared work tree admits no native print edition")
    on_disk = {path.name for path in (out / "editions").iterdir()} if (out / "editions").is_dir() else set()
    expected = {edition["directory"] for edition in editions.values()}
    _need(on_disk == expected and len(expected) == len(editions),
          "the materialized native print directories differ from the admitted editions")
    _need(not (out / "receipts").exists(), "this work tree was already compiled; run prepare again")
    for identity, edition in editions.items():
        _need(edition.get("engine") in ENGINES and edition.get("format") == ENGINES[edition["engine"]]
              and edition.get("options") == OPTIONS, "unsupported native compilation contract: " + identity)
        base = out / "editions" / edition["directory"]
        for path, digest in edition["files"].items():
            target = base / _relative(path)
            _need(target.is_file() and not target.is_symlink() and _file_sha(target) == digest,
                  "materialized native source changed after preparation: " + identity + " " + path)
    runtime = load_runtime(runtime_path)
    engines = sorted({edition["engine"] for edition in editions.values()})
    required = [ENGINES[engine] for engine in engines] + ["pdfinfo"] + (["xdvipdfmx"] if "xetex" in engines else [])
    missing = [binary for binary in required if not shutil.which(binary)]
    _need(not missing, "missing TeX toolchain programs: " + ", ".join(missing))
    located = _fonts(out, runtime)
    (out / "receipts").mkdir()
    gate = Gate(out, runtime)
    environment = {"SOURCE_DATE_EPOCH": int(index["source_date_epoch"])}
    order = sorted(editions, key=lambda identity: (-editions[identity]["bundle_bytes"], identity))
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    started = time.monotonic()

    def one(identity):
        edition = editions[identity]
        try:
            receipt = gate.compile(identity, edition, environment)
        except Exception as error:  # A defect in one edition must not hide the others.
            receipt = {"schema": RECEIPT_SCHEMA, "id": identity, "engine": edition["engine"],
                       "status": "fail", "problems": ["gate error: " + repr(error)]}
        _write_json(out / "receipts" / (edition["directory"] + ".json"), receipt)
        if receipt["status"] != "pass":
            print("FAIL " + identity + ": " + "; ".join(receipt["problems"][:3]), file=sys.stderr, flush=True)
        return receipt

    with ThreadPoolExecutor(max_workers=max(1, jobs)) as pool:
        receipts = list(pool.map(one, order))
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    wall = time.monotonic() - started
    failed = sorted(receipt["id"] for receipt in receipts if receipt["status"] != "pass")
    passes, by_engine, differing = {}, {}, set()
    for receipt in receipts:
        key = str(receipt.get("passes"))
        passes[key] = passes.get(key, 0) + 1
        by_engine[receipt["engine"]] = by_engine.get(receipt["engine"], 0) + 1
        differing.update(receipt.get("closure", {}).get("runtime_members_with_other_host_bytes", ()))
    summary = {"schema": SUMMARY_SCHEMA, "status": "fail" if failed else "pass", "scope": index["scope"],
               "source_revision": index["source_revision"], "runtime": runtime["id"],
               "toolchain": {binary: _version(binary) for binary in required if binary != "pdfinfo"},
               "editions": len(receipts), "failed": failed, "engines": dict(sorted(by_engine.items())),
               "passes": dict(sorted(passes.items(), key=lambda item: int(item[0]) if item[0].isdigit() else 99)),
               "pages": sum(receipt.get("pages") or 0 for receipt in receipts),
               "runtime_fonts_located": located, "runtime_fonts": len(runtime["fonts"]),
               "runtime_members_with_other_host_bytes": sorted(differing),
               "jobs": jobs, "wall_seconds": round(wall, 1),
               "cpu_seconds": round(after.ru_utime + after.ru_stime - before.ru_utime - before.ru_stime, 1)}
    _write_json(out / "summary.json", summary)
    return summary


def _out(root: Path, value: str | None) -> Path:
    path = Path(value) if value else root / DEFAULT_OUT
    return (path if path.is_absolute() else Path.cwd() / path).absolute()


def main(argv=None, *, examples=None) -> int:
    from _tooling import examples_live_on_the_verbs, with_examples
    parser = argparse.ArgumentParser(prog="native-print-compile", description=__doc__.split("\n\n")[0])
    examples_live_on_the_verbs(parser, "native-print-compile")
    verbs = parser.add_subparsers(dest="verb", required=True)
    first = verbs.add_parser("prepare", help="materialize every admitted native print bundle")
    with_examples(first, (examples or {}).get("prepare", ()))
    first.add_argument("--out", help=f"work directory (default: {DEFAULT_OUT})")
    first.add_argument("--only", action="append", default=[], metavar="ID",
                       help="prepare only this admitted edition; repeatable; never a deployment gate")
    second = verbs.add_parser("compile", help="typeset each prepared edition and fail closed")
    with_examples(second, (examples or {}).get("compile", ()))
    second.add_argument("--out", help=f"work directory written by prepare (default: {DEFAULT_OUT})")
    second.add_argument("--runtime", default=RUNTIME, help=f"native TeX runtime manifest (default: {RUNTIME})")
    second.add_argument("--jobs", type=int, default=os.cpu_count() or 1, help="parallel editions (default: CPUs)")
    arguments = parser.parse_args(argv)
    root = ROOT
    try:
        out = _out(root, arguments.out)
        if arguments.verb == "prepare":
            index = prepare(root, out, only=arguments.only)
            engines = {}
            for edition in index["editions"].values():
                engines[edition["engine"]] = engines.get(edition["engine"], 0) + 1
            print(json.dumps({"editions": len(index["editions"]), "engines": dict(sorted(engines.items())),
                              "scope": index["scope"], "status": "prepared"}, sort_keys=True))
            return 0
        _need(arguments.jobs >= 1, "--jobs requires a positive integer")
        runtime = Path(arguments.runtime)
        summary = compile_all(out, runtime_path=runtime if runtime.is_absolute() else root / runtime,
                              jobs=arguments.jobs)
        print(json.dumps({key: summary[key] for key in ("editions", "engines", "failed", "passes", "scope", "status")},
                         sort_keys=True))
        return 0 if summary["status"] == "pass" else 1
    except (CompileError, ValueError, OSError) as error:
        print("native-print-compile: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
