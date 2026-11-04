"""What a browser product family reads: its code closure, and the audit proving it.

A family's input key covers the data its recipe declares, the Python code
reachable from its producer entrypoint, and the harness modules that run and
identify it. The code closure is computed here from the current source, never
listed by hand: a static AST scan follows `import` statements, literal
`importlib.import_module`/`__import__` names, package-prefix dynamic imports,
and literals that name files under `scripts/` or `tools/` where they are used
as paths (the `SourceFileLoader(ROOT / "tools" / "citations")`, `sibling(
"mass-propers")` and `runpy.run_path` idioms). The harness is followed by
imports only: its recipe table names every producer as data.

The scan over-approximates; `audit` is the executable proof that it does not
under-approximate. It runs each producer cold under an audit hook, in every
Python subprocess too, and fails if the producer opens, probes or lists any
repository path outside that family's key.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import tempfile

CODE_TREES = ("scripts", "tools")
# Tests and their fixtures are never producer code. The audit would report a
# producer that opened one; a static literal naming them is not evidence.
NEVER_CODE = ("tools/tests",)
HARNESS = (
    "scripts/_browser_products.py",
    "scripts/_browser_product_recipes.py",
    "scripts/_browser_product_inputs.py",
)
# Families whose cold runner is not their argv entrypoint. The recipe runner
# reads this same table, so the closure and the executed code cannot diverge.
ADAPTERS = {"act-history": "scripts/_act_history_replay.py"}
_IMPORTERS = {"import_module", "__import__"}
_PATH_CALLS = {"Path", "PurePath", "PurePosixPath", "with_name", "joinpath", "join", "open",
               "SourceFileLoader", "spec_from_file_location", "run_path"}
_PARSED: dict[str, tuple] = {}


class ClosureError(ValueError):
    """The code closure could not be computed from the current checkout."""


class _Index:
    """Regular files and directories under the code trees, without following links.

    A link or special file anywhere in the code trees fails closed, as it does
    for any canonical input: Python would import through a link whose target
    no key could see. Regular bytecode caches are never code.
    """

    def __init__(self, root: Path):
        self.root = Path(root)
        self.files: set[str] = set()
        self.dirs: set[str] = set()
        for tree in CODE_TREES:
            self._walk(tree)

    def _walk(self, relative: str):
        path = self.root / relative
        try:
            mode = os.lstat(path).st_mode
        except FileNotFoundError:
            return
        if not stat.S_ISDIR(mode):
            raise ClosureError(f"code tree must be a regular directory: {relative}")
        self.dirs.add(relative)
        for entry in sorted(os.scandir(path), key=lambda entry: entry.name):
            name = relative + "/" + entry.name
            if _never(name):
                continue
            mode = entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                self._walk(name)
            elif not stat.S_ISREG(mode):
                raise ClosureError(f"code must be a regular file or directory: {name}")
            elif not ("__pycache__" in PurePosixPath(name).parts and PurePosixPath(name).suffix in {".pyc", ".pyo"}):
                self.files.add(name)

    def under(self, directory: str) -> set[str]:
        return {name for name in self.files if name.startswith(directory + "/")}


def _never(name: str) -> bool:
    return any(name == path or name.startswith(path + "/") for path in NEVER_CODE)


def _is_python(name: str, body: bytes) -> bool:
    if name.endswith(".py"):
        return True
    if PurePosixPath(name).suffix:
        return False
    first = body.split(b"\n", 1)[0]
    return first.startswith(b"#!") and b"python" in first


def _called(node: ast.Call) -> str | None:
    function = node.func
    return function.attr if isinstance(function, ast.Attribute) else getattr(function, "id", None)


def _division(node) -> list:
    """Operands of a `ROOT / "tools" / name` chain."""
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        return _division(node.left) + _division(node.right)
    return [node]


def _path_operands(node) -> list:
    """Expressions that name a path: division operands and path-call arguments."""
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        return _division(node)
    if isinstance(node, ast.Call):
        called = _called(node)
        if called == "join":
            # Only os.path.join; str.join takes no positional path pieces.
            function = node.func
            if not (isinstance(function, ast.Attribute) and isinstance(function.value, ast.Attribute)
                    and function.value.attr == "path"):
                return []
        if called in _PATH_CALLS:
            return list(node.args)
    return []


def _literal(node) -> str | None:
    if (isinstance(node, ast.Constant) and isinstance(node.value, str)
            and 0 < len(node.value) < 256 and not any(character.isspace() or character == "\0" for character in node.value)):
        return node.value
    return None


def _references(body: bytes, name: str) -> tuple:
    """Parse once per exact source: imports, dynamic imports, path literals.

    A bare literal such as "citations" counts only where it names a path: as a
    `/` operand, a path-call argument, or an argument to a local function whose
    parameter reaches one (the `sibling("mass-propers")` idiom). A literal that
    itself contains `/` counts anywhere. A registry of tool names or help text
    is therefore not mistaken for code the producer runs.
    """
    digest = hashlib.sha256(body).hexdigest()
    if digest in _PARSED:
        return _PARSED[digest]
    try:
        tree = ast.parse(body, filename=name)
    except (SyntaxError, ValueError):
        # Python compiles a module before running any of it, so source that
        # does not parse imports nothing. It stays in the key as a leaf.
        _PARSED[digest] = ((), (), frozenset())
        return _PARSED[digest]
    imports, dynamic, literals = [], [], set()
    statements = {id(node.value) for node in ast.walk(tree)
                  if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant)}
    # Local functions whose parameters reach a path: name -> positions/names.
    path_functions: dict[str, set] = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            parameters = [argument.arg for argument in (*node.args.posonlyargs, *node.args.args)]
            used = {operand.id for inner in ast.walk(node) for operand in _path_operands(inner)
                    if isinstance(operand, ast.Name)}
            reached = {position for position, parameter in enumerate(parameters) if parameter in used}
            reached |= {parameter for parameter in parameters if parameter in used}
            if reached:
                path_functions.setdefault(node.name, set()).update(reached)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend((0, alias.name, ()) for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append((node.level, node.module or "", tuple(alias.name for alias in node.names)))
        elif isinstance(node, ast.Call) and node.args and _called(node) in _IMPORTERS:
            argument = node.args[0]
            if isinstance(argument, ast.Constant) and isinstance(argument.value, str):
                imports.append((0, argument.value, ()))
            elif isinstance(argument, ast.JoinedStr) and argument.values:
                head = argument.values[0]
                if isinstance(head, ast.Constant) and isinstance(head.value, str) and head.value.endswith("."):
                    dynamic.append(("package", head.value[:-1]))
                elif (isinstance(head, ast.FormattedValue) and isinstance(head.value, ast.Name)
                      and head.value.id == "__name__"):
                    dynamic.append(("self", ""))
                else:
                    dynamic.append(("unknown", ast.unparse(argument)))
            else:
                dynamic.append(("unknown", ast.unparse(argument)))
        for operand in _path_operands(node):
            value = _literal(operand)
            if value is not None:
                literals.add(value)
        if isinstance(node, ast.Call) and _called(node) in path_functions:
            reached = path_functions[_called(node)]
            for position, argument in enumerate(node.args):
                if position in reached and _literal(argument) is not None:
                    literals.add(argument.value)
            for keyword in node.keywords:
                if keyword.arg in reached and _literal(keyword.value) is not None:
                    literals.add(keyword.value.value)
        value = _literal(node)
        if value is not None and "/" in value and id(node) not in statements:
            literals.add(value)
    result = (tuple(imports), tuple(dynamic), frozenset(literals))
    _PARSED[digest] = result
    return result


def _normal(path: str) -> str | None:
    parts = []
    for part in path.split("/"):
        if part in {"", "."}:
            continue
        if part == "..":
            if not parts:
                return None
            parts.pop()
            continue
        parts.append(part)
    return "/".join(parts)


def _module(index: _Index, base: str, parts: list[str]) -> list[str] | None:
    """Files executed by importing `parts` from search directory `base`."""
    found = []
    current = base
    for position, part in enumerate(parts):
        if not part:
            return None
        current = f"{current}/{part}" if current else part
        package = current + "/__init__.py"
        if position == len(parts) - 1 and current + ".py" in index.files:
            return [*found, current + ".py"]
        if package in index.files:
            found.append(package)
        elif current not in index.dirs:
            return None
    return found


def _resolve_import(index: _Index, module_dir: str, level: int, dotted: str, names: tuple) -> set[str]:
    if level:
        base = module_dir
        for _ in range(level - 1):
            base = str(PurePosixPath(base).parent) if "/" in base else ""
        bases = [base]
    else:
        # Producers run with their own directory and scripts/ on sys.path;
        # a few import `scripts.<name>` from the repository root.
        bases = list(dict.fromkeys([module_dir, "scripts", ""]))
    parts = dotted.split(".") if dotted else []
    found = set()
    for base in bases:
        files = _module(index, base, parts) if parts else []
        if files is None:
            continue
        found.update(files)
        if level and not parts and base + "/__init__.py" in index.files:
            found.add(base + "/__init__.py")
        for name in names:
            if name != "*":
                found.update(_module(index, base, [*parts, name]) or [])
    return found


def _literal_files(index: _Index, module_dir: str, literal: str) -> set[str]:
    if literal.startswith("/") or "://" in literal or "\\" in literal:
        return set()
    found = set()
    for base in (module_dir, "", "scripts", "tools"):
        candidate = _normal(f"{base}/{literal}" if base else literal)
        if not candidate or not candidate.startswith(tuple(tree + "/" for tree in CODE_TREES)) or _never(candidate):
            continue
        if candidate in index.files:
            found.add(candidate)
        elif candidate in index.dirs:
            # A named code or resource directory is read as a whole.
            found.update(index.under(candidate))
    return found


def code_closure(root: Path, entrypoints, *, index: _Index | None = None, unresolved=None,
                 literals: bool = True, opaque=frozenset()) -> set[str]:
    """Every file under scripts/ or tools/ reachable from these entrypoints.

    With `literals=False`, or for a module in `opaque`, only imports are
    followed. The harness is opaque: its recipe table names every producer as
    data, and it is in every family's key in its own right.
    """
    root = Path(root)
    index = _Index(root) if index is None else index
    pending = [name for name in entrypoints if name in index.files]
    closure: set[str] = set()
    while pending:
        name = pending.pop()
        if name in closure:
            continue
        closure.add(name)
        try:
            body = (root / name).read_bytes()
        except OSError as error:
            raise ClosureError(f"cannot read producer code {name}: {error}") from error
        if not _is_python(name, body):
            continue
        module_dir = str(PurePosixPath(name).parent)
        imports, dynamic, named = _references(body, name)
        found = set()
        for level, dotted, names in imports:
            found.update(_resolve_import(index, module_dir, level, dotted, names))
        for kind, value in dynamic:
            if kind == "self":
                found.update(index.under(module_dir))
            elif kind == "package":
                for base in (module_dir, "scripts", ""):
                    directory = _normal(f"{base}/{value.replace('.', '/')}" if base else value.replace(".", "/"))
                    if directory in index.dirs:
                        found.update(index.under(directory))
            elif unresolved is not None:
                unresolved.append((name, value))
        for literal in named if literals and name not in opaque else ():
            found.update(_literal_files(index, module_dir, literal))
        pending.extend(sorted(found - closure))
    return closure


def entrypoints(recipe: dict) -> list[str]:
    """The producer's own code: its argv entrypoint and any runner adapter."""
    names = []
    argv = recipe.get("argv") or []
    if argv and isinstance(argv[0], str):
        names.append(argv[0])
    if recipe.get("id") in ADAPTERS:
        names.append(ADAPTERS[recipe["id"]])
    return names


def family_code(root: Path, recipes) -> dict[str, set[str]]:
    """Code closure per family, each including the shared harness closure."""
    index = _Index(Path(root))
    harness = code_closure(root, HARNESS, index=index, literals=False)
    return {recipe["id"]: code_closure(root, entrypoints(recipe), index=index, opaque=harness) | harness
            for recipe in recipes}


# The audit hook is injected through a temporary `sitecustomize` on
# PYTHONPATH, so it is installed before any producer or child code runs and is
# inherited by every Python subprocess that keeps the environment.
_SITECUSTOMIZE = r'''
import json as _json
import os as _os
import sys as _sys
import threading as _threading

_log_dir = _os.environ.get("TRIPTYCH_BROWSER_AUDIT_LOG")
if _log_dir:
    _system_open = _os.open
    _log = open(_os.path.join(_log_dir, "%d-%s.jsonl" % (_os.getpid(), _os.urandom(4).hex())), "a", encoding="utf-8", buffering=1)
    _local = _threading.local()
    _seen = set()

    def _directory(descriptor):
        try:
            return _os.readlink("/proc/self/fd/%d" % descriptor)
        except OSError:
            return None

    def _absolute(path, directory=None):
        if isinstance(path, int):
            return _directory(path)
        try:
            path = _os.fsdecode(path)
        except TypeError:
            return None
        if _os.path.isabs(path):
            return path
        parent = _os.getcwd() if directory is None else _directory(directory)
        return None if parent is None else _os.path.join(parent, path)

    _library = _os.path.dirname(_os.__file__) + _os.sep
    _guard = {"_guard_original", "_audit_original"}

    def _caller():
        """The first caller outside the standard library and the cold guard.

        None for the guard's own path resolution, which is not a producer
        read; "import-system" for the import system listing sys.path.
        """
        frame = _sys._getframe(2)
        resolving = importing = False
        while frame is not None:
            code = frame.f_code
            if code.co_filename.startswith((_library, "<frozen")) or code.co_filename == __file__:
                resolving = resolving or code.co_name in ("realpath", "_joinrealpath")
                importing = importing or code.co_name == "_fill_cache"
            elif code.co_filename == "<string>" and (code.co_name in _guard or resolving):
                return None
            elif not (code.co_filename == "<string>" and code.co_name == "_descriptor_open"):
                return "import-system" if importing else "%s:%d" % (code.co_filename, frame.f_lineno)
            frame = frame.f_back
        return "import-system" if importing else "?"

    def _record(kind, path, extra=None):
        if path is None:
            return
        where = _caller()
        if where is None:
            return
        path = _os.path.normpath(path)
        if kind != "spawn":
            if (kind, path, where == "import-system") in _seen:
                return
            _seen.add((kind, path, where == "import-system"))
        try:
            _log.write(_json.dumps({"event": kind, "path": path, "extra": extra, "where": where}) + "\n")
        except Exception:
            pass

    def _descriptor_open(path, flags, mode=0o777, *, dir_fd=None):
        _record("open", _absolute(path, dir_fd), flags)
        _local.inside = True
        try:
            return _system_open(path, flags, mode, dir_fd=dir_fd)
        finally:
            _local.inside = False

    def _prober(function):
        # Existence and type checks decide output as surely as reads do.
        # Imports probe through posix.stat directly and are not recorded.
        def probe(path, *arguments, dir_fd=None, **keywords):
            _record("probe", _absolute(path, dir_fd))
            if dir_fd is not None:
                keywords["dir_fd"] = dir_fd
            return function(path, *arguments, **keywords)
        return probe

    def _hook(event, arguments):
        if getattr(_local, "inside", False):
            return
        if event == "open":
            flags = arguments[2] if len(arguments) > 2 else None
            _record("open", _absolute(arguments[0]), flags)
        elif event in ("os.listdir", "os.scandir"):
            _record("list", _absolute(arguments[0] if arguments[0] is not None else "."))
        elif event == "subprocess.Popen":
            executable, argv, cwd, environment = arguments
            inherited = environment is None or environment.get("TRIPTYCH_BROWSER_AUDIT_LOG") == _log_dir
            _record("spawn", str(executable), {"argv": [str(item) for item in (argv or [])], "cwd": None if cwd is None else str(cwd),
                                                "audited_environment": inherited, "via": event})
        elif event in ("os.system", "os.exec", "os.posix_spawn", "os.spawn"):
            _record("spawn", str(arguments[0]), {"argv": [], "cwd": None, "audited_environment": False, "via": event})

    # Wrappers keep the capability sets that shutil and pathlib consult, so an
    # observed run takes the same code paths as an unobserved one.
    for _name, _wrapper in (("open", _descriptor_open), ("stat", _prober(_os.stat)),
                            ("lstat", _prober(_os.lstat)), ("access", _prober(_os.access))):
        _original = getattr(_os, _name)
        for _capability in (_os.supports_dir_fd, _os.supports_fd, _os.supports_follow_symlinks,
                            _os.supports_effective_ids):
            if _original in _capability:
                _capability.add(_wrapper)
        setattr(_os, _name, _wrapper)
    _sys.addaudithook(_hook)
'''


def _within(name: str, scopes) -> bool:
    return any(name == scope or name.startswith(scope + "/") for scope in scopes)


def audit(root: Path, product_ids=None, *, log=None) -> dict:
    """Run each selected producer cold and compare what it touched with its key.

    The hook records every file opened, every path probed with stat/lstat/
    access, and every directory listed, in the producer and in each Python
    child. A family passes when:

    - every repository file it opened or probed (present or absent) is a key
      member, a declared input file, or inside a declared tree;
    - every directory it listed is inside a declared tree or the code trees
      (the import system lists those), so membership changes are covered;
    - it read nothing from ignored state (`build/`, `.git`, `.scratch/` other
      than its private cold scratch and staging), which no key can cover;
    - every Python child kept the audit environment. A non-Python child (the
      `node -e` model checks) is reported; repository paths named in its
      arguments are judged as reads. Its own further reads are not observed,
      so a child program that opens other files needs its own review.

    Reads of the descriptor, which identities exclude by design, are
    reported, not failed.
    """
    import _browser_products as products
    import _browser_product_recipes as recipes

    root = Path(root).resolve()
    selected = [recipe for recipe in products._recipes()
                if product_ids is None or recipe["id"] in set(product_ids)]
    if product_ids is not None and {recipe["id"] for recipe in selected} != set(product_ids):
        raise ClosureError(f"unknown browser product families: {sorted(set(product_ids) - {r['id'] for r in selected})}")
    identities = products._identity_batch(root)
    scratch = root / ".scratch/browser-product-audit"
    scratch.mkdir(parents=True, exist_ok=True)
    report = {}
    with tempfile.TemporaryDirectory(prefix="audit-", dir=scratch) as temporary:
        hook = Path(temporary) / "hook"
        hook.mkdir()
        (hook / "sitecustomize.py").write_text(_SITECUSTOMIZE, encoding="utf-8")
        for recipe in selected:
            if log is not None:
                print(f"browser-products audit: {recipe['id']} ...", file=log, flush=True)
            logs = Path(temporary) / "logs" / recipe["id"]
            logs.mkdir(parents=True)
            out = Path(temporary) / "out" / recipe["id"]
            environment = {"TRIPTYCH_BROWSER_AUDIT_LOG": str(logs),
                           "PYTHONPATH": os.pathsep.join(filter(None, [str(hook), os.environ.get("PYTHONPATH")]))}
            recipes.generate(root, out, [recipe["id"]], environment=environment)
            events = []
            for path in sorted(logs.iterdir()):
                events.extend(json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line)
            if not any(event["event"] == "open" for event in events):
                raise ClosureError(f"{recipe['id']}: the audit hook recorded nothing; it was not installed")
            report[recipe["id"]] = _judge(root, recipe, identities[recipe["id"]], events, products.EXCLUDED)
            shutil.rmtree(out, ignore_errors=True)
    return report


CACHE_MARKER = ".browser-products-cache-v1"
_PRIVATE = (".scratch/browser-product-audit", ".scratch/browser-product-recipes",
            ".scratch/act-history-replay", ".scratch/next-product-store")


def _judge(root: Path, recipe: dict, identity: dict, events: list, excluded=frozenset()) -> dict:
    members = set(identity["source_paths"])
    trees = tuple(recipe["input_trees"])
    declared = set(recipe["input_files"])
    excludes = tuple(recipe["exclude_paths"])
    prefix = str(root) + os.sep

    def relative(path):
        if path == str(root):
            return ""
        return path[len(prefix):] if path.startswith(prefix) else None

    def covered_file(name):
        return name in members or name in declared or (_within(name, trees) and not _within(name, excludes))

    ancestors = {""}
    for scope in (*trees, *declared, *members):
        parts = scope.split("/")
        ancestors.update("/".join(parts[:index]) for index in range(1, len(parts)))

    def covered_directory(name, listing):
        if _within(name, trees) or _within(name, CODE_TREES):
            return True
        # Probing an ancestor of the key's scope reveals nothing outside it.
        return not listing and name in ancestors

    opened, probed, listed = set(), set(), set()
    outside, listed_outside, ignored, excluded_reads = set(), set(), set(), set()
    unaudited, children = [], []
    launched = {os.path.basename(event["path"]) for event in events
                if event["event"] == "spawn" and event["extra"]["via"] == "subprocess.Popen"}
    touched, where = [], {}
    for event in events:
        path = event["path"]
        if event["event"] != "spawn":
            if not (event["event"] == "list" and event.get("where") == "import-system"):
                touched.append((event["event"], path))  # sys.path listings are the import system's
                where.setdefault(path, event.get("where"))
            continue
        extra = event["extra"]
        if extra["via"] != "subprocess.Popen" and os.path.basename(path) in launched:
            continue  # subprocess's own posix_spawn/exec of a recorded Popen
        child = {"executable": path, "argv": extra["argv"][:6], "via": extra["via"]}
        if "python" in os.path.basename(path):
            if not extra["audited_environment"]:
                unaudited.append(child)
            continue
        if extra["via"] != "subprocess.Popen":
            unaudited.append(child)
            continue
        children.append(child)
        base = extra["cwd"] or str(root)
        touched.extend(("open", os.path.normpath(os.path.join(base, item))) for item in extra["argv"][1:]
                       if os.path.join(base, item).startswith(prefix) and os.path.lexists(os.path.join(base, item)))
    for kind, path in touched:
        name = relative(path)
        if name is None or _within(name, _PRIVATE):
            continue
        if PurePosixPath(name).name == CACHE_MARKER and kind == "probe":
            continue  # the harness refusing to write into a sealed cache
        directory = os.path.isdir(path) and not os.path.islink(path)
        if kind != "list" and directory and any(private.startswith(name + "/") for private in _PRIVATE):
            continue  # traversing to the producer's private scratch
        if _within(name, (".scratch", "build", ".git")):
            ignored.add(name)
            continue
        if (name.startswith(("scripts/", "tools/")) and "__pycache__" in PurePosixPath(name).parts
                and PurePosixPath(name).suffix in {".pyc", ".pyo"}):
            continue
        if kind == "list" or directory:
            (listed if kind == "list" else probed).add(name)
            if not covered_directory(name, kind == "list"):
                listed_outside.add(name or ".")
            continue
        (opened if kind == "open" else probed).add(name)
        if name in excluded:
            excluded_reads.add(name)
        elif not covered_file(name):
            outside.add(name)
    flagged = outside | listed_outside | ignored
    return {"opened": len(opened), "probed": len(probed), "listed": len(listed), "members": len(members),
            "opened_paths": sorted(opened), "probed_paths": sorted(probed), "listed_paths": sorted(listed),
            "outside": sorted(outside), "listed_outside": sorted(listed_outside),
            "non_canonical": sorted(ignored), "excluded_reads": sorted(excluded_reads),
            "where": {name: where.get(str(root / name) if name != "." else str(root)) for name in sorted(flagged)},
            "unaudited_children": unaudited, "children": children,
            "ok": not (outside or listed_outside or ignored or unaudited)}
