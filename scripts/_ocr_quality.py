#!/usr/bin/env python3
"""Measure whether a retrieved text layer is Latin prose or OCR wreckage.

The Genesis survey has to distinguish three states that a catalogue cannot:
a work with no digitisation at all, a work digitised only as page images, and a
work whose text layer exists and is unusable. The third is the dangerous one,
because a `_djvu.txt` file downloads successfully, has the right size, and is
in the right language — and `guidance/catena.md` measured Migne PL 34's at
roughly one corrupted word in eight.

The measure is deliberately crude and stated rather than tuned: the share of
whitespace tokens that are common Latin function words. Running Latin prose sits
near or above ten per cent; the blackletter incunabula OCR this survey met sits
near zero, because almost nothing it emits is a word at all. It answers "is this
prose" and never "is this correct", so a text that passes here is still a
finding aid until it is collated.

    python3 scripts/_ocr_quality.py FILE...
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Function words, not content words: a content word list would score a
# Genesis commentary higher than an Isaiah one for reasons of subject.
LATIN = {
    "et", "in", "quod", "est", "non", "qui", "ad", "cum", "ex", "per", "sed",
    "autem", "enim", "quae", "quam", "sunt", "hoc", "esse", "ut", "de", "a",
    "ab", "id", "eius", "sicut", "vel", "quia", "atque", "nam", "ita", "si",
    "quo", "quibus", "etiam", "tamen", "ergo", "iam", "nec", "aut", "vero",
    "ipse", "haec", "hic", "eo", "ea", "eum", "post", "ante", "super", "sub",
}
ENGLISH = {
    "the", "and", "of", "to", "in", "that", "is", "it", "for", "as", "was",
    "with", "be", "by", "not", "this", "which", "but", "from", "they", "he",
    "are", "his", "on", "or", "an", "we", "all", "have", "who", "their",
}
GREEK = {
    "καὶ", "τοῦ", "τὸ", "τῶν", "τὴν", "δὲ", "ἐν", "τῆς", "τὸν", "γὰρ", "οὐ",
    "τῷ", "μὲν", "εἰς", "ὁ", "ἡ", "τά", "πρὸς", "ἀλλὰ", "ἐπὶ", "κατὰ", "ὡς",
}

_TOKEN = re.compile(r"[^\W\d_]+", re.UNICODE)


def measure(text: str) -> dict[str, object]:
    tokens = [token.lower() for token in _TOKEN.findall(text)]
    total = len(tokens)
    if not total:
        return {"tokens": 0, "latin": 0.0, "english": 0.0, "greek": 0.0, "verdict": "empty"}
    scores = {
        "latin": sum(token in LATIN for token in tokens) / total,
        "english": sum(token in ENGLISH for token in tokens) / total,
        "greek": sum(token in GREEK for token in tokens) / total,
    }
    best = max(scores, key=lambda key: scores[key])
    share = scores[best]
    if share >= 0.10:
        verdict = f"prose-{best}"
    elif share >= 0.04:
        verdict = f"degraded-{best}"
    else:
        verdict = "not-prose"
    return {
        "tokens": total,
        **{key: round(value, 4) for key, value in scores.items()},
        "verdict": verdict,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+")
    arguments = parser.parse_args(argv)
    for name in arguments.files:
        path = Path(name)
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as error:
            print(f"{name}\tunreadable\t{error}", file=sys.stderr)
            continue
        result = measure(text)
        print(
            f"{path.name}\t{len(text):>9} bytes\t{result['tokens']:>8} tokens\t"
            f"la={result['latin']}\ten={result['english']}\tel={result['greek']}\t"
            f"{result['verdict']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
