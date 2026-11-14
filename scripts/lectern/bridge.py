"""Ask the browser's own scripts, under node, for what they alone derive."""
from __future__ import annotations

import atexit
import itertools
from contextvars import Context
import json
import os
import selectors
import shutil
import subprocess
import sys
import threading
from pathlib import Path
from typing import Any

from _corpus_index import CorpusIndexError as ProductError
from .data import indexed_products

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
        self._products: dict[subprocess.Popen[str], tuple[Any, Any]] = {}
        self._readers: dict[subprocess.Popen[str], Any] = {}
        self._data_pipes: dict[subprocess.Popen[str], int] = {}
        self._checked: Any = None

    def adopt(self, index: Any) -> None:
        """Open the next reading session on an index startup has just checked.

        Only that next session uses it; a restarted bridge checks afresh.
        """
        with self._state:
            self._checked = index

    def _start(self) -> subprocess.Popen[str]:
        node = shutil.which("node")
        if node is None:
            raise Refused("node is not installed, and this view is derived by the browser's model under node")
        # Requests and shutdown can run in different reader workers. Enter and
        # leave the product context in this same explicit Context so its tokens
        # and cache lock belong to the child's whole lifetime, across threads.
        # A fresh context must not borrow an outer operation's snapshot: that
        # operation could finish while this interactive child is still alive.
        context = Context()
        # Callers hold self._state here.
        checked, self._checked = self._checked, None
        try:
            manager = indexed_products(ROOT, checked)
            products = context.run(manager.__enter__)
        except (ProductError, OSError) as error:
            raise Refused(f"indexed reading data is unavailable: {error}") from error
        # Temporary snapshots can install their own exit cleanup. Re-register
        # after every acquisition so this verification and child teardown run
        # first, including after a bridge restart.
        atexit.unregister(self.close)
        atexit.register(self.close)
        read_fd, write_fd = os.pipe()
        try:
            process = subprocess.Popen(
                [node, str(BRIDGE), "--indexed", str(read_fd)],
                cwd=ROOT,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                encoding="utf-8",
                bufsize=1,
                pass_fds=(read_fd,),
            )
        except BaseException:
            os.close(write_fd)
            try:
                context.run(manager.__exit__, *sys.exc_info())
            finally:
                atexit.unregister(self.close)
            raise
        finally:
            os.close(read_fd)
        self._products[process] = (context, manager)
        self._readers[process] = products
        self._data_pipes[process] = write_fd
        return process

    def call(self, adapter: str, fn: str, *args: Any, cancelled=None) -> Any:
        with self._state:
            generation = self._generation
            if self._closing:
                raise Refused("the model bridge is closing")
        with self.lock:
            if cancelled is not None and cancelled():
                raise Refused("the reading request was superseded")
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
                if not isinstance(answer, dict):
                    raise ValueError("the bridge response is not an object")
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
        """Answer selected-data requests until the browser model returns."""
        stream = process.stdout
        assert stream
        with selectors.DefaultSelector() as watch:
            watch.register(stream, selectors.EVENT_READ)
            while True:
                if not watch.select(timeout=PATIENCE):
                    return None
                line = stream.readline()
                if not line:
                    return line
                try:
                    message = json.loads(line)
                except ValueError:
                    return line
                if not isinstance(message, dict) or message.get("reader_data") is not True:
                    return line
                try:
                    reader = self._readers[process]
                    context, _ = self._products[process]
                    body = context.run(reader.read, message.get("path"))
                    response = {"ok": True, "text": None if body is None else body.decode("utf-8")}
                except Exception as error:
                    response = {"ok": False, "error": str(error)}
                payload = (json.dumps(response, ensure_ascii=False) + "\n").encode("utf-8")
                descriptor = self._data_pipes[process]
                while payload:
                    count = os.write(descriptor, payload)
                    payload = payload[count:]

    def read_product(self, relative: str) -> bytes | None:
        """Read a selected publication through the same owned source snapshot."""
        with self.lock:
            with self._state:
                if self._closing:
                    raise Refused("the model bridge is closing")
                if self.process is None or self.process.poll() is not None:
                    self._dispose(self.process)
                    self.process = self._start()
                process = self.process
            reader = self._readers[process]
            context, _ = self._products[process]
            try:
                return context.run(reader.read, relative)
            except (ProductError, OSError, ValueError) as error:
                raise Refused(f"indexed reading data is unavailable: {error}") from error

    def _dispose(self, process: subprocess.Popen[str] | None) -> None:
        if process is None:
            return
        if process.poll() is None:
            process.kill()
        process.wait(timeout=5)
        for stream in (process.stdin, process.stdout):
            if stream is not None:
                stream.close()
        # Release only after termination is confirmed. A failed teardown keeps
        # the process and snapshot owned, so a later close can finish it.
        lifetime = self._products.pop(process, None)
        self._readers.pop(process, None)
        descriptor = self._data_pipes.pop(process, None)
        if descriptor is not None:
            os.close(descriptor)
        try:
            if lifetime is not None:
                context, manager = lifetime
                try:
                    context.run(manager.__exit__, None, None, None)
                except (ProductError, OSError) as error:
                    raise Refused(f"published browser data changed during reading: {error}") from error
        finally:
            if not self._products:
                atexit.unregister(self.close)

    def _drop(self, process: subprocess.Popen[str] | None) -> None:
        # The serial caller (or close after that caller exits) owns the pipes.
        try:
            self._dispose(process)
        finally:
            if process is None or process.poll() is not None:
                with self._state:
                    if self.process is process:
                        self.process = None

    def close(self) -> None:
        # Kill without taking the request lock: its owner may be in select.
        # Do not close its streams until it has returned from that read.
        with self._state:
            self._closing = True
            self._generation += 1
            self._checked = None
            generation = self._generation
            process = self.process
            reader = self._readers.get(process)
            if reader is not None and hasattr(reader, "cancel"):
                reader.cancel()
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
    worker = None
    try:
        from textual.worker import get_current_worker, NoActiveWorker
        try:
            worker = get_current_worker()
        except NoActiveWorker:
            pass
    except ImportError:
        pass
    return BRIDGE_PROCESS.call(adapter, fn, *args,
                               cancelled=(lambda: worker.is_cancelled) if worker else None)
