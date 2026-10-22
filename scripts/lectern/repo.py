"""Where the reader finds the checkout, its published data, and its tools."""
from __future__ import annotations

import json
import os
import subprocess
import threading
from collections import OrderedDict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "src" / "web" / "data"
STRUCTURE = DATA / "structure"
BROWSER = ROOT / "src" / "web" / "browser"
TOOLS = ROOT / "tools"
BIBLES = ROOT / "src" / "sources" / "bibles"


class Refused(Exception):
    """A request the data or a tool declined, with the reason it gave."""


class _Cache:
    """A small thread-safe LRU, so a reader paging back and forth pays once."""

    def __init__(self, size: int) -> None:
        self.size = size
        self.items: OrderedDict[object, Any] = OrderedDict()
        self.lock = threading.Lock()

    def get(self, key: object) -> Any:
        with self.lock:
            if key in self.items:
                self.items.move_to_end(key)
                return self.items[key]
        return None

    def put(self, key: object, value: Any) -> Any:
        with self.lock:
            self.items[key] = value
            self.items.move_to_end(key)
            while len(self.items) > self.size:
                self.items.popitem(last=False)
        return value


_JSON = _Cache(512)
_MISSING = object()


def load_json(path: Path, *, missing: Any = _MISSING) -> Any:
    """Read one published file. A file that is absent is an answer, not an error,
    wherever the layer says so (a chapter with nothing has no file)."""
    key = ("json", str(path))
    held = _JSON.get(key)
    if held is not None:
        return held
    try:
        with path.open(encoding="utf-8") as stream:
            value = json.load(stream)
    except FileNotFoundError:
        if missing is _MISSING:
            raise
        return missing
    return _JSON.put(key, value)


_RUNS = _Cache(256)


def run_tool(tool: str, *arguments: str, cache: bool = True, timeout: float = 300) -> Any:
    """Run `tools/<tool>` as the repository runs it and read its JSON answer.

    The tool is executed through its own shebang, not this interpreter, so it
    sees the same Python and dependencies it would see from a shell.
    """
    command = (str(TOOLS / tool), *arguments)
    if cache:
        held = _RUNS.get(command)
        if held is not None:
            return held
    env = {**os.environ, "NO_COLOR": "1"}
    done = subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if done.returncode != 0:
        detail = (done.stderr or done.stdout).strip()
        try:
            detail = json.loads(detail).get("error", detail)
        except (ValueError, AttributeError):
            pass
        raise Refused(f"{tool}: {detail or f'exit {done.returncode}'}")
    try:
        value = json.loads(done.stdout)
    except ValueError as error:
        raise Refused(f"{tool} printed no JSON: {error}") from error
    return _RUNS.put(command, value) if cache else value
