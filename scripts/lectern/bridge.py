"""Ask the browser's own scripts, under node, for what they alone derive."""
from __future__ import annotations

import itertools
import json
import shutil
import subprocess
import threading
from pathlib import Path
from typing import Any

from .repo import ROOT, Refused

BRIDGE = Path(__file__).with_name("bridge.js")


class Bridge:
    """One long-lived node process; requests are answered in order."""

    def __init__(self) -> None:
        self.process: subprocess.Popen[str] | None = None
        self.lock = threading.Lock()
        self.ids = itertools.count(1)

    def _start(self) -> subprocess.Popen[str]:
        node = shutil.which("node")
        if node is None:
            raise Refused("node is not installed, and this view is derived by the browser's model under node")
        return subprocess.Popen(
            [node, str(BRIDGE)],
            cwd=ROOT,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            encoding="utf-8",
            bufsize=1,
        )

    def call(self, adapter: str, fn: str, *args: Any) -> Any:
        with self.lock:
            if self.process is None or self.process.poll() is not None:
                self.process = self._start()
            ident = next(self.ids)
            request = json.dumps({"id": ident, "adapter": adapter, "fn": fn, "args": list(args)})
            assert self.process.stdin and self.process.stdout
            try:
                self.process.stdin.write(request + "\n")
                self.process.stdin.flush()
                reply = self.process.stdout.readline()
            except (BrokenPipeError, OSError) as error:
                self.process = None
                raise Refused(f"the model bridge stopped: {error}") from error
            if not reply:
                self.process = None
                raise Refused(f"the model bridge stopped while answering {adapter} {fn}")
            answer = json.loads(reply)
            if answer.get("id") != ident:
                self.process.kill()
                self.process = None
                raise Refused("the model bridge answered out of turn")
            if not answer.get("ok"):
                raise Refused(answer.get("error") or f"{adapter} {fn} failed")
            return answer.get("value")

    def close(self) -> None:
        if self.process is not None and self.process.poll() is None:
            self.process.kill()
        self.process = None


BRIDGE_PROCESS = Bridge()


def call(adapter: str, fn: str, *args: Any) -> Any:
    return BRIDGE_PROCESS.call(adapter, fn, *args)
