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
        self._state = threading.Lock()
        self._generation = 0
        self._closing = False
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
        with self._state:
            generation = self._generation
            if self._closing:
                raise Refused("the model bridge is closing")
        with self.lock:
            with self._state:
                if self._closing or generation != self._generation:
                    raise Refused("the model bridge closed before this request could start")
                if self.process is None or self.process.poll() is not None:
                    self._dispose(self.process)
                    self.process = self._start()
                process = self.process
            ident = next(self.ids)
            request = json.dumps({"id": ident, "adapter": adapter, "fn": fn, "args": list(args)})
            assert process.stdin and process.stdout
            self.waiting += 1
            try:
                process.stdin.write(request + "\n")
                process.stdin.flush()
                reply = self._reply(process)
            except (BrokenPipeError, OSError) as error:
                self._drop(process)
                raise Refused(f"the model bridge stopped: {error}") from error
            finally:
                self.waiting -= 1
            if reply is None:
                self._drop(process)
                raise Refused(f"the model bridge did not answer {adapter} {fn} within {PATIENCE:.0f} s")
            if not reply:
                self._drop(process)
                raise Refused(f"the model bridge stopped while answering {adapter} {fn}")
            try:
                answer = json.loads(reply)
            except ValueError as error:
                # A line that is not the protocol: nothing after it can be trusted.
                self._drop(process)
                raise Refused(f"the model bridge answered {adapter} {fn} with something not JSON") from error
            if answer.get("id") != ident:
                self._drop(process)
                raise Refused("the model bridge answered out of turn")
            if not answer.get("ok"):
                raise Refused(answer.get("error") or f"{adapter} {fn} failed")
            return answer.get("value")

    def _reply(self, process: subprocess.Popen[str]) -> str | None:
        """One line from the bridge, or None if none arrives in time."""
        stream = process.stdout
        assert stream
        with selectors.DefaultSelector() as watch:
            watch.register(stream, selectors.EVENT_READ)
            if not watch.select(timeout=PATIENCE):
                return None
        return stream.readline()

    @staticmethod
    def _dispose(process: subprocess.Popen[str] | None) -> None:
        if process is None:
            return
        if process.poll() is None:
            process.kill()
        process.wait(timeout=5)
        for stream in (process.stdin, process.stdout):
            if stream is not None:
                stream.close()

    def _drop(self, process: subprocess.Popen[str] | None) -> None:
        # The serial caller (or close after that caller exits) owns the pipes.
        with self._state:
            if self.process is process:
                self.process = None
        self._dispose(process)

    def close(self) -> None:
        # Kill without taking the request lock: its owner may be in select.
        # Do not close its streams until it has returned from that read.
        with self._state:
            self._closing = True
            self._generation += 1
            generation = self._generation
            process = self.process
            if process is not None and process.poll() is None:
                process.kill()
        with self.lock:
            try:
                self._drop(process)
            finally:
                with self._state:
                    if generation == self._generation:
                        self._closing = False


BRIDGE_PROCESS = Bridge()


def call(adapter: str, fn: str, *args: Any) -> Any:
    return BRIDGE_PROCESS.call(adapter, fn, *args)
