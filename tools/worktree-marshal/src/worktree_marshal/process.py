"""Dependency-injected child-process supervision and status normalization."""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol


class ChildProcess(Protocol):
    def poll(self) -> int | None: ...

    def send_signal(self, signum: int) -> None: ...

    def terminate(self) -> None: ...

    def wait(self, timeout: float | None = None) -> int: ...


def wait_for_child(
    process: ChildProcess,
    *,
    forwarded_signals: Callable[[], tuple[int, int]],
    get_signal_handler: Callable[[int], object],
    set_signal_handler: Callable[[int, object], object],
    interrupt_signal: Callable[[], int],
    keyboard_interrupt: Callable[[], type[BaseException]],
    process_lookup_error: Callable[[], type[BaseException]],
    timeout_expired: Callable[[], type[BaseException]],
) -> int:
    """Wait for one child while preserving the launcher's signal semantics."""

    forwarded_handlers: dict[int, object] = {}

    def forward(signum: int, _frame: object) -> None:
        if process.poll() is None:
            try:
                process.send_signal(signum)
            except process_lookup_error():
                pass

    for signum in forwarded_signals():
        forwarded_handlers[signum] = get_signal_handler(signum)
        set_signal_handler(signum, forward)
    try:
        try:
            return process.wait()
        except keyboard_interrupt():
            if process.poll() is None:
                try:
                    process.send_signal(interrupt_signal())
                except process_lookup_error():
                    pass
            try:
                return process.wait(timeout=10)
            except timeout_expired():
                process.terminate()
                return process.wait()
    finally:
        for signum, handler in forwarded_handlers.items():
            set_signal_handler(signum, handler)


def normalized_exit_status(
    returncode: int,
    *,
    absolute: Callable[[int], int] = abs,
) -> int:
    if returncode < 0:
        return 128 + absolute(returncode)
    return returncode
