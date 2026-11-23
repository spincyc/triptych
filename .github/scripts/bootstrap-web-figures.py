"""Try the deployed SVGs on an empty Pages cache; the compiler rechecks every hit."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from http.client import HTTPException, HTTPSConnection
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import _web_edition_figures as figures  # noqa: E402


def fetch(figure: str, expected: dict, directory: Path) -> bool:
    if not figures._ID.fullmatch(figure):
        raise ValueError("invalid figure ID in Pages digest record")
    # This fixed origin is the public Pages site. No credentials or redirects.
    connection = HTTPSConnection("mystago.gy", timeout=3)
    try:
        connection.request("GET", f"/web-figures/{figure}.svg", headers={"Accept-Encoding": "identity"})
        with connection.getresponse() as response:
            if response.status != 200:
                return False
            data = response.read(expected["bytes"] + 1)
    except (OSError, HTTPException):
        return False
    finally:
        connection.close()
    if len(data) != expected["bytes"] or figures._sha(data) != expected["sha256"]:
        return False
    with (directory / f"{figure}.svg").open("xb") as target:
        target.write(data)
    return True


def main(directory: Path) -> None:
    proof = figures._pages_proof(ROOT, "docker:" + os.environ["TEXLIVE_IMAGE"])
    if not proof:
        return
    # A partial GitHub cache is already usable. Never write through a restored
    # directory or mix new downloads into an existing one.
    try:
        directory.mkdir(parents=True)
    except FileExistsError:
        return
    with ThreadPoolExecutor(max_workers=6) as pool:
        downloads = [pool.submit(fetch, figure, row, directory) for figure, row in proof["figures"].items()]
        print(f"Fetched {sum(job.result() for job in downloads)} verified figure candidates from Pages.")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
