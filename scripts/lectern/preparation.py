"""Run the canonical offline preflight without blocking the loading screen."""
from __future__ import annotations

import asyncio
import os
from pathlib import Path
import signal
import sys


async def _run(command: list[str]) -> tuple[int, str]:
    # Producers inherit this group. Cancelling a first build must stop those
    # children as well as the Python preflight that holds the cache lock.
    launch = asyncio.create_task(asyncio.create_subprocess_exec(
        *command, stdin=asyncio.subprocess.DEVNULL,
        stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.PIPE,
        start_new_session=os.name == "posix",
    ))
    process = None
    drain = None
    completed = False
    try:
        # Shield creation so cancellation cannot lose a newly spawned process.
        process = await asyncio.shield(launch)
        drain = asyncio.create_task(process.communicate())
        _, stderr = await asyncio.shield(drain)
        completed = True
        return process.returncode, stderr.decode("utf-8", errors="replace").strip()
    finally:
        if not completed:
            process = process or await launch
            drain = drain or asyncio.create_task(process.communicate())

            def stop(force: bool = False) -> None:
                try:
                    if os.name == "posix":
                        os.killpg(process.pid, signal.SIGKILL if force else signal.SIGTERM)
                    elif process.returncode is None:
                        process.kill() if force else process.terminate()
                except ProcessLookupError:
                    pass

            stop()
            try:
                await asyncio.wait_for(asyncio.shield(drain), timeout=1)
            except asyncio.TimeoutError:
                pass
            finally:
                stop(force=True)
            await drain


async def prepare_products() -> None:
    from .repo import Refused

    status, detail = await _run([sys.executable, "-I", "-B", str(Path(__file__).resolve())])
    if status:
        raise Refused(detail or f"browser data preparation exited {status}")


def _main() -> int:
    # Keep verification, cache construction and error wording owned by the CLI's
    # existing preflight; snapshots invoke that same function synchronously.
    import runpy

    tool = runpy.run_path(str(Path(__file__).resolve().parents[2] / "tools/lectern"))
    try:
        tool["_prepare_products"](announce=False)
    except tool["ReaderRefused"] as error:
        print(error, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
