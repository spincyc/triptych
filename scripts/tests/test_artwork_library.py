import hashlib
import importlib.machinery
import importlib.util
import struct
import sys
import tempfile
import unittest
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "artwork-library"
LOADER = importlib.machinery.SourceFileLoader("artwork_library", str(SCRIPT))
SPEC = importlib.util.spec_from_loader("artwork_library", LOADER)
ARTWORK = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules["artwork_library"] = ARTWORK
SPEC.loader.exec_module(ARTWORK)


def chunk(kind: bytes, payload: bytes) -> bytes:
    checksum = zlib.crc32(kind + payload) & 0xFFFFFFFF
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", checksum)


def png(width=3, height=2, color_type=0, depth=8, profile=False) -> bytes:
    channels = {0: 1, 2: 3, 4: 2, 6: 4}[color_type]
    rows = b"".join(b"\0" + bytes([255]) * width * channels for _ in range(height))
    ihdr = struct.pack(">IIBBBBB", width, height, depth, color_type, 0, 0, 0)
    extra = chunk(b"sRGB", b"\0") if profile else b""
    return (
        ARTWORK.PNG_SIGNATURE
        + chunk(b"IHDR", ihdr)
        + extra
        + chunk(b"IDAT", zlib.compress(rows))
        + chunk(b"IEND", b"")
    )


class ArtworkLibraryTests(unittest.TestCase):
    def test_inspects_stripped_grayscale_png(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "figure.png"
            path.write_bytes(png())
            info = ARTWORK.inspect_png(path)
            self.assertEqual((info.width, info.height, info.depth), (3, 2, 8))
            self.assertEqual(info.mode, "grayscale")
            self.assertFalse(info.has_alpha)
            self.assertFalse(info.has_color_profile)

    def test_manifest_accepts_matching_asset(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            asset = root / "artwork" / "figure.png"
            asset.parent.mkdir()
            asset.write_bytes(png(width=900, height=500))
            digest = hashlib.sha256(asset.read_bytes()).hexdigest()
            manifest = root / "artwork.toml"
            manifest.write_text(
                f"""[[asset]]
id = "RPD-FIG-test-0001-iso"
path = "artwork/figure.png"
sha256 = "{digest}"
width = 900
height = 500
depth = 8
mode = "grayscale"
largest_placement_inches = 3.0
""",
                encoding="utf-8",
            )
            self.assertEqual(ARTWORK.validate_manifest(manifest), [])

    def test_manifest_rejects_hash_rgb_profile_and_low_dpi(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            asset = root / "figure.png"
            asset.write_bytes(png(width=30, color_type=2, profile=True))
            manifest = root / "artwork.toml"
            manifest.write_text(
                """[[asset]]
id = "RPD-FIG-test-0001-iso"
path = "figure.png"
sha256 = "wrong"
width = 30
height = 2
depth = 8
mode = "grayscale"
largest_placement_inches = 1.0
""",
                encoding="utf-8",
            )
            errors = "\n".join(ARTWORK.validate_manifest(manifest))
            self.assertIn("manifest sha256", errors)
            self.assertIn("color type 0", errors)
            self.assertIn("color profile", errors)
            self.assertIn("below 300", errors)

    def test_manifest_rejects_duplicate_ids_and_escaping_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "artwork.toml"
            entry = """[[asset]]
id = "RPD-FIG-test-0001-iso"
path = "../figure.png"
sha256 = "none"
width = 1
height = 1
depth = 8
mode = "grayscale"
"""
            manifest.write_text(entry + entry, encoding="utf-8")
            errors = "\n".join(ARTWORK.validate_manifest(manifest))
            self.assertIn("duplicate artwork ID", errors)
            self.assertIn("path must remain", errors)


if __name__ == "__main__":
    unittest.main()
