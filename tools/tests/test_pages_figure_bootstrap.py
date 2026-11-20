"""The optional Pages bootstrap admits exact bytes and falls back on a miss."""
from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from io import BytesIO
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SPEC = spec_from_file_location("pages_figure_bootstrap", ROOT / ".github/scripts/bootstrap-web-figures.py")
bootstrap = module_from_spec(SPEC)
SPEC.loader.exec_module(bootstrap)


class PagesFigureBootstrapTests(unittest.TestCase):
    def test_only_exact_bounded_bytes_are_saved(self):
        svg = b"<svg>published</svg>"
        figure = "a" * 64
        expected = {"bytes": len(svg), "sha256": bootstrap.figures._sha(svg)}
        for status, returned, accepted in [(200, svg, True), (200, svg + b"x", False),
                                           (200, svg.upper(), False), (200, svg[:4], False),
                                           (404, svg, False), (302, svg, False)]:
            with (self.subTest(status=status, returned=returned),
                  tempfile.TemporaryDirectory() as temporary,
                  patch.object(bootstrap, "HTTPSConnection") as connection):
                response = BytesIO(returned)
                response.status = status
                connection.return_value.getresponse.return_value = response
                directory = Path(temporary)
                self.assertEqual(bootstrap.fetch(figure, expected, directory), accepted)
                path = directory / f"{figure}.svg"
                self.assertEqual(path.read_bytes() if path.exists() else None, svg if accepted else None)
                connection.assert_called_once_with("mystago.gy", timeout=3)

    def test_unavailable_delivery_leaves_the_compiler_a_miss(self):
        with (tempfile.TemporaryDirectory() as temporary,
              patch.object(bootstrap, "HTTPSConnection") as connection):
            connection.return_value.request.side_effect = TimeoutError()
            self.assertFalse(bootstrap.fetch("b" * 64, {"bytes": 42}, Path(temporary)))
            self.assertEqual(list(Path(temporary).iterdir()), [])
