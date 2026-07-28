import hashlib
import importlib.machinery
import importlib.util
import struct
import sys
import tempfile
import unittest
import zlib
from pathlib import Path
from unittest import mock

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

    def test_legacy_manifest_does_not_run_page_ground_edge_audit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            asset = root / "figure.png"
            asset.write_bytes(png(width=4, height=4))
            digest = hashlib.sha256(asset.read_bytes()).hexdigest()
            manifest = root / "artwork.toml"
            manifest.write_text(
                f"""[[asset]]
id = "legacy"
path = "figure.png"
sha256 = "{digest}"
width = 4
height = 4
depth = 8
mode = "grayscale"
""",
                encoding="utf-8",
            )
            with mock.patch.object(
                ARTWORK, "audit_page_ground_perimeter"
            ) as perimeter_audit:
                self.assertEqual(ARTWORK.validate_manifest(manifest), [])
                perimeter_audit.assert_not_called()

    def test_page_ground_treatment_accepts_clean_white_perimeter(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            asset = root / "figure.png"
            asset.write_bytes(png(width=8, height=8))
            digest = hashlib.sha256(asset.read_bytes()).hexdigest()
            manifest = root / "artwork.toml"
            manifest.write_text(
                f"""[[asset]]
id = "blended"
path = "figure.png"
sha256 = "{digest}"
width = 8
height = 8
depth = 8
mode = "grayscale"
boundary_treatment = "page-ground"
""",
                encoding="utf-8",
            )
            self.assertEqual(ARTWORK.validate_manifest(manifest), [])

    def test_manifest_accepts_grayscale_alpha_with_transparent_treatment(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            asset = root / "figure.png"
            asset.write_bytes(png(width=8, height=8, color_type=4))
            digest = hashlib.sha256(asset.read_bytes()).hexdigest()
            manifest = root / "artwork.toml"
            manifest.write_text(
                f"""[[asset]]
id = "transparent"
path = "figure.png"
sha256 = "{digest}"
width = 8
height = 8
depth = 8
mode = "grayscale-alpha"
boundary_treatment = "transparent"
""",
                encoding="utf-8",
            )
            self.assertEqual(ARTWORK.validate_manifest(manifest), [])

    def test_manifest_rejects_alpha_without_transparent_treatment(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            asset = root / "figure.png"
            asset.write_bytes(png(width=8, height=8, color_type=4))
            digest = hashlib.sha256(asset.read_bytes()).hexdigest()
            manifest = root / "artwork.toml"
            manifest.write_text(
                f"""[[asset]]
id = "unmarked-alpha"
path = "figure.png"
sha256 = "{digest}"
width = 8
height = 8
depth = 8
mode = "grayscale-alpha"
""",
                encoding="utf-8",
            )
            errors = "\n".join(ARTWORK.validate_manifest(manifest))
            self.assertIn(
                "alpha/transparency requires boundary_treatment='transparent'",
                errors,
            )

    def test_manifest_rejects_transparent_treatment_without_alpha(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            asset = root / "figure.png"
            asset.write_bytes(png(width=8, height=8))
            digest = hashlib.sha256(asset.read_bytes()).hexdigest()
            manifest = root / "artwork.toml"
            manifest.write_text(
                f"""[[asset]]
id = "false-transparent"
path = "figure.png"
sha256 = "{digest}"
width = 8
height = 8
depth = 8
mode = "grayscale"
boundary_treatment = "transparent"
""",
                encoding="utf-8",
            )
            errors = "\n".join(ARTWORK.validate_manifest(manifest))
            self.assertIn(
                "transparent boundary_treatment requires alpha/transparency",
                errors,
            )

    def test_page_ground_treatment_rejects_dark_perimeter(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            asset = root / "figure.png"
            # Rebuild the tiny fixture with a black outer scanline.
            rows = b"\0" + bytes(8)
            rows += b"".join(b"\0" + bytes([255]) * 8 for _ in range(7))
            ihdr = struct.pack(">IIBBBBB", 8, 8, 8, 0, 0, 0, 0)
            image = (
                ARTWORK.PNG_SIGNATURE
                + chunk(b"IHDR", ihdr)
                + chunk(b"IDAT", zlib.compress(rows))
                + chunk(b"IEND", b"")
            )
            asset.write_bytes(image)
            digest = hashlib.sha256(asset.read_bytes()).hexdigest()
            manifest = root / "artwork.toml"
            manifest.write_text(
                f"""[[asset]]
id = "boxed"
path = "figure.png"
sha256 = "{digest}"
width = 8
height = 8
depth = 8
mode = "grayscale"
boundary_treatment = "page-ground"
""",
                encoding="utf-8",
            )
            errors = "\n".join(ARTWORK.validate_manifest(manifest))
            self.assertIn("materially dark edge pixel", errors)
            self.assertIn("below the near-white threshold", errors)

    def test_manifest_rejects_unknown_boundary_treatment(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            asset = root / "figure.png"
            asset.write_bytes(png(width=4, height=4))
            digest = hashlib.sha256(asset.read_bytes()).hexdigest()
            manifest = root / "artwork.toml"
            manifest.write_text(
                f"""[[asset]]
id = "unknown"
path = "figure.png"
sha256 = "{digest}"
width = 4
height = 4
depth = 8
mode = "grayscale"
boundary_treatment = "drop-shadow"
""",
                encoding="utf-8",
            )
            errors = "\n".join(ARTWORK.validate_manifest(manifest))
            self.assertIn("boundary_treatment must be one of", errors)

    def test_framed_boundary_requires_rationale(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            asset = root / "figure.png"
            asset.write_bytes(png(width=4, height=4))
            digest = hashlib.sha256(asset.read_bytes()).hexdigest()
            manifest = root / "artwork.toml"
            manifest.write_text(
                f"""[[asset]]
id = "framed"
path = "figure.png"
sha256 = "{digest}"
width = 4
height = 4
depth = 8
mode = "grayscale"
boundary_treatment = "intentional-frame"
""",
                encoding="utf-8",
            )
            errors = "\n".join(ARTWORK.validate_manifest(manifest))
            self.assertIn("requires a nonempty boundary_treatment_rationale", errors)

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

    def test_dictionary_manifest_validates_nested_technical_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            research = root / "research"
            asset = root / "shared" / "artwork" / "figure.png"
            research.mkdir()
            asset.parent.mkdir(parents=True)
            asset.write_bytes(png(width=600, height=900))
            digest = hashlib.sha256(asset.read_bytes()).hexdigest()
            manifest = research / "artwork-manifest.toml"
            manifest.write_text(
                f"""[[asset_files]]
id = "file-test"
path = "shared/artwork/figure.png"
state = "held"
audit_record = "research/test.md"
technical = {{ width_px = 600, height_px = 900, bit_depth = 8, color_mode = "grayscale", bytes = {asset.stat().st_size}, sha256 = "{digest}" }}
""",
                encoding="utf-8",
            )
            self.assertEqual(ARTWORK.validate_manifest(manifest), [])

    def test_dictionary_page_ground_treatment_runs_perimeter_audit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            research = root / "research"
            asset = root / "shared" / "artwork" / "figure.png"
            research.mkdir()
            asset.parent.mkdir(parents=True)
            asset.write_bytes(png(width=8, height=8))
            digest = hashlib.sha256(asset.read_bytes()).hexdigest()
            manifest = research / "artwork-manifest.toml"
            manifest.write_text(
                f"""[[asset_files]]
id = "file-test"
path = "shared/artwork/figure.png"
state = "held"
boundary_treatment = "page-ground"
audit_record = "research/test.md"
technical = {{ width_px = 8, height_px = 8, bit_depth = 8, color_mode = "grayscale", bytes = {asset.stat().st_size}, sha256 = "{digest}" }}
""",
                encoding="utf-8",
            )
            with mock.patch.object(
                ARTWORK, "audit_page_ground_perimeter", return_value=[]
            ) as perimeter_audit:
                self.assertEqual(ARTWORK.validate_manifest(manifest), [])
                perimeter_audit.assert_called_once()

    def test_dictionary_manifest_accepts_declared_grayscale_alpha(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            research = root / "research"
            asset = root / "shared" / "artwork" / "figure.png"
            research.mkdir()
            asset.parent.mkdir(parents=True)
            asset.write_bytes(png(width=8, height=8, color_type=4))
            digest = hashlib.sha256(asset.read_bytes()).hexdigest()
            manifest = research / "artwork-manifest.toml"
            manifest.write_text(
                f"""[[asset_files]]
id = "file-transparent"
path = "shared/artwork/figure.png"
state = "held"
boundary_treatment = "transparent"
audit_record = "research/test.md"
technical = {{ width_px = 8, height_px = 8, bit_depth = 8, color_mode = "grayscale-alpha", bytes = {asset.stat().st_size}, sha256 = "{digest}" }}
""",
                encoding="utf-8",
            )
            self.assertEqual(ARTWORK.validate_manifest(manifest), [])

    def test_dictionary_manifest_rejects_alpha_without_transparent_treatment(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            research = root / "research"
            asset = root / "shared" / "artwork" / "figure.png"
            research.mkdir()
            asset.parent.mkdir(parents=True)
            asset.write_bytes(png(width=8, height=8, color_type=4))
            digest = hashlib.sha256(asset.read_bytes()).hexdigest()
            manifest = research / "artwork-manifest.toml"
            manifest.write_text(
                f"""[[asset_files]]
id = "file-unmarked-alpha"
path = "shared/artwork/figure.png"
state = "held"
audit_record = "research/test.md"
technical = {{ width_px = 8, height_px = 8, bit_depth = 8, color_mode = "grayscale-alpha", bytes = {asset.stat().st_size}, sha256 = "{digest}" }}
""",
                encoding="utf-8",
            )
            errors = "\n".join(ARTWORK.validate_manifest(manifest))
            self.assertIn(
                "alpha/transparency requires boundary_treatment='transparent'",
                errors,
            )

    def test_dictionary_manifest_rejects_transparent_treatment_without_alpha(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            research = root / "research"
            asset = root / "shared" / "artwork" / "figure.png"
            research.mkdir()
            asset.parent.mkdir(parents=True)
            asset.write_bytes(png(width=8, height=8))
            digest = hashlib.sha256(asset.read_bytes()).hexdigest()
            manifest = research / "artwork-manifest.toml"
            manifest.write_text(
                f"""[[asset_files]]
id = "file-false-transparent"
path = "shared/artwork/figure.png"
state = "held"
boundary_treatment = "transparent"
audit_record = "research/test.md"
technical = {{ width_px = 8, height_px = 8, bit_depth = 8, color_mode = "grayscale", bytes = {asset.stat().st_size}, sha256 = "{digest}" }}
""",
                encoding="utf-8",
            )
            errors = "\n".join(ARTWORK.validate_manifest(manifest))
            self.assertIn(
                "transparent boundary_treatment requires alpha/transparency",
                errors,
            )

    @mock.patch.object(ARTWORK.shutil, "which", return_value="/usr/bin/pdfimages")
    @mock.patch.object(ARTWORK.subprocess, "run")
    def test_pdf_audit_separates_failure_from_review_trigger(self, run, _which):
        run.return_value = mock.Mock(
            returncode=0,
            stdout="""page num type width height color comp bpc enc interp object ID x-ppi y-ppi size ratio
1 0 image 1000 1000 gray 1 8 image no 5 0 299 299 1K 1%
2 1 image 1000 1000 gray 1 8 image no 6 0 451 451 1K 1%
""",
            stderr="",
        )
        failures, triggers = ARTWORK.audit_pdf(Path("proof.pdf"))
        self.assertIn("below 300", failures[0])
        self.assertIn("450 review trigger", triggers[0])


if __name__ == "__main__":
    unittest.main()
