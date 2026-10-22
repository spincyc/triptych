"""Ask the browser's own scripts, under node, for what they alone derive."""
from __future__ import annotations

import itertools
import json
import selectors
import shutil
import subprocess
import threading
from pathlib import Path
from typing import Any

from .repo import ROOT, Refused

BRIDGE = Path(__file__).with_name("bridge.js")
# Long enough for the largest structure a model first parses (a missal's
# propers, some 17 MB); a reply later than this is a hung bridge, not a slow one.
PATIENCE = 120.0


class Bridge:
    """One long-lived node process; requests are answered in order."""

    def __init__(self) -> None:
        self.process: subprocess.Popen[str] | None = None
        self.lock = threading.Lock()
        self.ids = itertools.count(1)
        self.waiting = 0  # calls under way, which a snapshot waits out

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
            self.waiting += 1
            try:
                self.process.stdin.write(request + "\n")
                self.process.stdin.flush()
                reply = self._reply()
            except (BrokenPipeError, OSError) as error:
                self._drop()
                raise Refused(f"the model bridge stopped: {error}") from error
            finally:
                self.waiting -= 1
            if reply is None:
                self._drop()
                raise Refused(f"the model bridge did not answer {adapter} {fn} within {PATIENCE:.0f} s")
            if not reply:
                self._drop()
                raise Refused(f"the model bridge stopped while answering {adapter} {fn}")
            try:
                answer = json.loads(reply)
            except ValueError as error:
                # A line that is not the protocol: nothing after it can be trusted.
                self._drop()
                raise Refused(f"the model bridge answered {adapter} {fn} with something not JSON") from error
            if answer.get("id") != ident:
                self._drop()
                raise Refused("the model bridge answered out of turn")
            if not answer.get("ok"):
                raise Refused(answer.get("error") or f"{adapter} {fn} failed")
            return answer.get("value")

    def _reply(self) -> str | None:
        """One line from the bridge, or None if none arrives in time."""
        assert self.process and self.process.stdout
        with selectors.DefaultSelector() as watch:
            watch.register(self.process.stdout, selectors.EVENT_READ)
            if not watch.select(timeout=PATIENCE):
                return None
        return self.process.stdout.readline()

    def _drop(self) -> None:
        if self.process is not None and self.process.poll() is None:
            self.process.kill()
        self.process = None

    def close(self) -> None:
        if self.process is not None and self.process.poll() is None:
            self.process.kill()
        self.process = None


BRIDGE_PROCESS = Bridge()


def call(adapter: str, fn: str, *args: Any) -> Any:
    return BRIDGE_PROCESS.call(adapter, fn, *args)
