"""Reading a typed reference ("Gen 1", "1 Cor 13", "John 3") against a canon."""
from __future__ import annotations

import re


def parse(text: str, books: list[dict]) -> tuple[dict, int] | None:
    """The book and chapter a reader typed, or None when it names neither.

    Matched against the canon's own tokens and names only; nothing here knows a
    book that the published canon does not list.
    """
    match = re.fullmatch(r"\s*(.+?)\s*(\d+)?\s*", text or "")
    if not match:
        return None
    name, chapter = match.group(1), int(match.group(2) or 1)
    fold = re.sub(r"[\s.]+", " ", name).strip().lower()
    squeezed = fold.replace(" ", "")

    def keys(book: dict) -> tuple[str, str]:
        return book["token"].lower(), book["name"].lower()

    tiers = (
        lambda token, title: squeezed in (token, title.replace(" ", "")),
        lambda token, title: fold == title,
        lambda token, title: title.startswith(fold) or title.replace(" ", "").startswith(squeezed),
        lambda token, title: token.startswith(squeezed),
    )
    for test in tiers:
        found = [book for book in books if test(*keys(book))]
        if len(found) == 1 or (found and test is tiers[0]):
            book = found[0]
            # The chapter is passed on as typed: an out-of-range one is refused by
            # the page's own address check, never quietly moved to the nearest.
            return book, chapter
    return None
