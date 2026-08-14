#!/usr/bin/env python3
"""Prove, or refuse to let anyone claim, a visual difference between captures.

    pair-audit.py <capture-dir> [...] [--json OUT] [--tolerance N]
                  [--no-pixels] [--recursive]

Finds every pair of files in the given directories whose names differ only by
a `before--` / `after--` prefix, computes both SHA-256 digests, and — for PNG
pairs — decodes both images and compares them pixel by pixel. Each pair is
classified as exactly one of three things:

  (a) BYTE-IDENTICAL              same SHA-256. There is NO visual difference.
                                  No document may describe this pair as
                                  showing a rendering change.
  (b) VISUALLY EQUIVALENT         digests differ and the only pixels that
                                  differ do so by no more than --tolerance in
                                  every channel: encoder or rasterizer noise,
                                  no state a reader could see. Also no
                                  rendering change.
  (c) PIXELS DIFFER               digests differ and N pixels differ beyond
                                  the tolerance, inside the bounding box
                                  printed with the row. The region is stated
                                  so a reviewer can check a written
                                  description against the picture.

Unpaired captures are listed separately and are not an error: a run that has
produced only the `after--` half has no pair to audit yet.

WHY THIS EXISTS. The independent review of the V5 Catena evidence package
found five of its ten before/after screenshot pairs to be byte-identical
while four separate documents described each as showing a visible rendering
change. The captures were of the wrong states and nothing in the package
could tell. This script is the instrument that would have caught it, so it
EXITS NON-ZERO when any pair is byte-identical or decodes to identical
pixels: a caller cannot pass this check and still claim a difference that
does not exist.

Exit status
    0   every pair differs in its pixels, or there are no pairs to audit
    1   at least one pair is byte-identical or decodes to identical pixels
    2   a usage, filesystem or decode error

Standard library only; no third-party dependency and no network. The pixel
pass is pure Python and therefore slow (seconds per megapixel); `--no-pixels`
reduces the run to digests alone, at the cost of collapsing (b) into (c).
"""

import argparse
import hashlib
import json
import os
import struct
import sys
import zlib

BEFORE = "before--"
AFTER = "after--"
CHUNK = 1 << 20
RASTER = (".png",)


def digest(path):
    """(sha256 hex, byte length) of one file, read in bounded chunks."""
    sha = hashlib.sha256()
    size = 0
    with open(path, "rb") as handle:
        while True:
            block = handle.read(CHUNK)
            if not block:
                break
            sha.update(block)
            size += len(block)
    return sha.hexdigest(), size


# ------------------------------------------------------------------ PNG
# A minimal decoder: 8-bit, non-interlaced, colour types 0/2/4/6 — which is
# every PNG Chromium's `Page.captureScreenshot` writes. Anything else raises,
# because a wrong answer here would be worse than no answer.

CHANNELS = {0: 1, 2: 3, 4: 2, 6: 4}


def decode_png(path):
    """(width, height, bytes-per-pixel, raw pixel bytes) of one PNG."""
    with open(path, "rb") as handle:
        data = handle.read()
    if data[:8] != b"\x89PNG\r\n\x1a\x0a":
        raise ValueError("%s: not a PNG" % path)
    at = 8
    parts = []
    header = None
    while at + 8 <= len(data):
        length = struct.unpack(">I", data[at:at + 4])[0]
        kind = data[at + 4:at + 8]
        body = data[at + 8:at + 8 + length]
        if kind == b"IHDR":
            header = struct.unpack(">IIBBBBB", body)
        elif kind == b"IDAT":
            parts.append(body)
        elif kind == b"IEND":
            break
        at += 12 + length
    if header is None:
        raise ValueError("%s: no IHDR" % path)
    width, height, depth, colour, _compression, _filter, interlace = header
    if depth != 8 or interlace != 0 or colour not in CHANNELS:
        raise ValueError("%s: unsupported PNG (depth %d, colour %d, interlace %d)"
                         % (path, depth, colour, interlace))
    step = CHANNELS[colour]
    stride = width * step
    raw = zlib.decompress(b"".join(parts))
    out = bytearray(height * stride)
    previous = bytearray(stride)
    at = 0
    for row in range(height):
        kind = raw[at]
        at += 1
        line = bytearray(raw[at:at + stride])
        at += stride
        if kind == 1:
            for x in range(step, stride):
                line[x] = (line[x] + line[x - step]) & 0xFF
        elif kind == 2:
            for x in range(stride):
                line[x] = (line[x] + previous[x]) & 0xFF
        elif kind == 3:
            for x in range(stride):
                left = line[x - step] if x >= step else 0
                line[x] = (line[x] + ((left + previous[x]) >> 1)) & 0xFF
        elif kind == 4:
            for x in range(stride):
                left = line[x - step] if x >= step else 0
                up = previous[x]
                corner = previous[x - step] if x >= step else 0
                guess = left + up - corner
                da, db, dc = abs(guess - left), abs(guess - up), abs(guess - corner)
                if da <= db and da <= dc:
                    near = left
                elif db <= dc:
                    near = up
                else:
                    near = corner
                line[x] = (line[x] + near) & 0xFF
        elif kind != 0:
            raise ValueError("%s: unknown row filter %d" % (path, kind))
        out[row * stride:(row + 1) * stride] = line
        previous = line
    return width, height, step, bytes(out)


def compare_pixels(before, after, tolerance):
    """How the two rasters differ, separating noise from a real change.

    A pixel whose every channel differs by at most `tolerance` is counted as
    NOISE and kept out of the bounding box: an antialiasing byte is not a
    state a reader can see, and letting one pass as a difference would make
    this script useless in the direction it exists for.
    """
    bw, bh, bs, bp = decode_png(before)
    aw, ah, asz, ap = decode_png(after)
    if (bw, bh) != (aw, ah):
        return {"error": "different dimensions: %dx%d vs %dx%d" % (bw, bh, aw, ah)}
    if bs != asz:
        return {"error": "different channel counts: %d vs %d" % (bs, asz)}
    stride = bw * bs
    changed = 0
    noise = 0
    worst = 0
    x0, y0, x1, y1 = bw, bh, -1, -1
    for row in range(bh):
        base = row * stride
        if bp[base:base + stride] == ap[base:base + stride]:
            continue
        for column in range(bw):
            at = base + column * bs
            one, other = bp[at:at + bs], ap[at:at + bs]
            if one == other:
                continue
            delta = max(abs(one[i] - other[i]) for i in range(bs))
            if delta > worst:
                worst = delta
            if delta <= tolerance:
                noise += 1
                continue
            changed += 1
            if column < x0:
                x0 = column
            if column > x1:
                x1 = column
            if row < y0:
                y0 = row
            if row > y1:
                y1 = row
    box = None if changed == 0 else (x0, y0, x1, y1)
    return {"pixels": changed, "noise": noise, "worst": worst,
            "box": box, "total": bw * bh}


# ---------------------------------------------------------------- pairing

def collect(roots, recursive):
    """{directory: {stem: {'before': path, 'after': path}}} over the roots."""
    found = {}
    for root in roots:
        if not os.path.isdir(root):
            raise NotADirectoryError(root)
        walk = os.walk(root) if recursive else [(root, [], os.listdir(root))]
        for here, _dirs, names in walk:
            for name in sorted(names):
                path = os.path.join(here, name)
                if not os.path.isfile(path):
                    continue
                if name.startswith(BEFORE):
                    side, stem = "before", name[len(BEFORE):]
                elif name.startswith(AFTER):
                    side, stem = "after", name[len(AFTER):]
                else:
                    continue
                found.setdefault(here, {}).setdefault(stem, {})[side] = path
    return found


def main(argv):
    parser = argparse.ArgumentParser(
        description="Classify before--/after-- capture pairs, and fail on any "
                    "pair that shows no rendering change.")
    parser.add_argument("directory", nargs="+", help="directory of captures")
    parser.add_argument("--recursive", action="store_true",
                        help="descend into subdirectories (pairs match within "
                             "one directory)")
    parser.add_argument("--tolerance", type=int, default=1,
                        help="a pixel differing by at most this in every "
                             "channel is noise, not a difference (default 1)")
    parser.add_argument("--no-pixels", action="store_true",
                        help="digests only; do not decode rasters")
    parser.add_argument("--json", dest="json_out", metavar="OUT",
                        help="also write the classification as JSON, so a "
                             "caller's index can carry the verdict rather "
                             "than a hand-written claim")
    parser.add_argument("--quiet-unpaired", action="store_true",
                        help="do not list captures with no partner")
    args = parser.parse_args(argv)

    try:
        found = collect(args.directory, args.recursive)
    except OSError as error:
        print("pair-audit: %s" % error, file=sys.stderr)
        return 2

    pairs = []
    unpaired = []
    for here in sorted(found):
        for stem in sorted(found[here]):
            sides = found[here][stem]
            if "before" in sides and "after" in sides:
                pairs.append((stem, sides["before"], sides["after"]))
            else:
                side = "before" if "before" in sides else "after"
                unpaired.append((side, sides[side]))

    rows = []
    for stem, before, after in pairs:
        try:
            before_sha, before_size = digest(before)
            after_sha, after_size = digest(after)
        except OSError as error:
            print("pair-audit: %s" % error, file=sys.stderr)
            return 2
        row = {"stem": stem, "before": before, "after": after,
               "before_sha": before_sha, "after_sha": after_sha,
               "before_size": before_size, "after_size": after_size,
               "raster": stem.lower().endswith(RASTER), "pixels": None}
        if before_sha == after_sha:
            row["verdict"] = "a. BYTE-IDENTICAL — NO VISUAL DIFFERENCE"
            row["fatal"] = True
        elif not row["raster"]:
            row["verdict"] = "c. DIFFERING (not a raster; digests only)"
            row["fatal"] = False
        elif args.no_pixels:
            row["verdict"] = "c. DIFFERING DIGESTS (pixel pass not run)"
            row["fatal"] = False
        else:
            try:
                row["pixels"] = compare_pixels(before, after, args.tolerance)
            except (ValueError, OSError, zlib.error) as error:
                print("pair-audit: %s" % error, file=sys.stderr)
                return 2
            if "error" in row["pixels"]:
                row["verdict"] = "c. PIXELS DIFFER (%s)" % row["pixels"]["error"]
                row["fatal"] = False
            elif row["pixels"]["pixels"] == 0:
                row["verdict"] = ("b. BYTE-DIFFERENT BUT VISUALLY EQUIVALENT — "
                                  "NO VISUAL DIFFERENCE")
                row["fatal"] = True
            else:
                row["verdict"] = "c. PIXELS DIFFER"
                row["fatal"] = False
        rows.append(row)

    print("PAIR AUDIT — SHA-256, and pixels, over every before--/after-- pair")
    print("=" * 78)
    if not rows:
        print("no pairs to audit (%d unpaired capture(s) present)" % len(unpaired))
    for row in rows:
        print("")
        print(row["stem"])
        print("  verdict : %s" % row["verdict"])
        print("  before  : %9d bytes  %s" % (row["before_size"], row["before_sha"]))
        print("  after   : %9d bytes  %s" % (row["after_size"], row["after_sha"]))
        seen = row["pixels"]
        if seen and "pixels" in seen and seen["pixels"]:
            x0, y0, x1, y1 = seen["box"]
            print("  pixels  : %d of %d differ (%.4f%%); %d noise pixel(s) "
                  "ignored; worst channel delta %d"
                  % (seen["pixels"], seen["total"],
                     100.0 * seen["pixels"] / seen["total"],
                     seen.get("noise", 0), seen.get("worst", 0)))
            print("  region  : x %d..%d, y %d..%d  (%d x %d box)"
                  % (x0, x1, y0, y1, x1 - x0 + 1, y1 - y0 + 1))
            print("  NAME IT : a description of this pair must name what changed "
                  "inside that box.")
        elif seen and "pixels" in seen:
            print("  pixels  : 0 of %d differ beyond the tolerance "
                  "(%d noise pixel(s), worst channel delta %d)"
                  % (seen["total"], seen.get("noise", 0), seen.get("worst", 0)))
        if row["fatal"]:
            print("  NOTE    : the two captures show the same picture. No document "
                  "may describe")
            print("            this pair as showing a rendering change.")

    if unpaired and not args.quiet_unpaired:
        print("")
        print("-" * 78)
        print("UNPAIRED CAPTURES (%d) — no partner to compare against yet:"
              % len(unpaired))
        for side, path in sorted(unpaired, key=lambda one: one[1]):
            print("  %-6s %s" % (side, os.path.basename(path)))

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as handle:
            json.dump({
                "tool": "pair-audit.py",
                "tolerance": args.tolerance,
                "classes": {
                    "a": "BYTE-IDENTICAL — no visual difference; no document "
                         "may describe this pair as showing a rendering change",
                    "b": "BYTE-DIFFERENT BUT VISUALLY EQUIVALENT — only "
                         "sub-tolerance pixels differ; also no rendering change",
                    "c": "PIXELS DIFFER — a real change, inside the stated box; "
                         "a description must name what changed there"},
                "pairs": [{
                    "stem": one["stem"],
                    "verdict": one["verdict"],
                    "class": one["verdict"][0],
                    "showsNoRenderingChange": one["fatal"],
                    "before": {"path": one["before"], "bytes": one["before_size"],
                               "sha256": one["before_sha"]},
                    "after": {"path": one["after"], "bytes": one["after_size"],
                              "sha256": one["after_sha"]},
                    "pixels": one["pixels"]} for one in rows],
                "unpaired": [{"side": side, "path": path}
                             for side, path in sorted(unpaired, key=lambda one: one[1])]
            }, handle, indent=2, ensure_ascii=False)
            handle.write("\n")

    fatal = [row["stem"] for row in rows if row["fatal"]]
    print("")
    print("=" * 78)
    print("pairs audited          : %d" % len(rows))
    print("a. byte-identical      : %d"
          % len([one for one in rows if one["verdict"].startswith("a.")]))
    print("b. visually equivalent : %d"
          % len([one for one in rows if one["verdict"].startswith("b.")]))
    print("c. pixels differ       : %d"
          % len([one for one in rows if one["verdict"].startswith("c.")]))
    print("unpaired captures      : %d" % len(unpaired))

    if fatal:
        print("")
        print("FAIL: %d pair(s) show no rendering change: %s"
              % (len(fatal), ", ".join(fatal)))
        print("Either the captures are of the wrong states, or the difference "
              "they were")
        print("offered to show is not in the raster and the capture should not "
              "be shipped.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
