"""One locked Markdown-to-HTML primitive for the site and publication audits.

Callers supply their owning repository root; page preparation and layout remain
with the site. Importing this module does not require Python Markdown.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version as distribution_version
from pathlib import Path
import re


class MarkdownRenderError(RuntimeError):
    """The site's selected Markdown renderer is unavailable or not locked."""


# Web editions are endnote-heavy and carry their own section anchors, so
# footnotes and heading attributes must become real markup rather than literal
# [^n] and {#id} text. Proper studies also retain their four-senses description
# lists, so definition terms and bodies must become semantic markup. `fenced_code`
# is here because a triple-backtick block is
# not a Markdown core construct: without the extension the backticks are read as
# an inline code span, so the block's lines run together inside a paragraph and
# its language word prints as prose. The site's `reject_unrendered_code_fences`
# refuses any page carrying that shape, so dropping an extension from this list
# fails the build rather than quietly changing what a reader sees.
MARKDOWN_EXTENSIONS = [
    "tables",
    "sane_lists",
    "def_list",
    "toc",
    "footnotes",
    "attr_list",
    "fenced_code",
]


def require_locked_markdown_dependency(root: Path) -> None:
    """Prove that rendering uses the exact dependency selected by the bound lock."""
    lock_path = root / "requirements-public-alpha.txt"
    requirements = [
        line.strip()
        for line in lock_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    markdown_pins = [
        match.group(1)
        for requirement in requirements
        if (match := re.fullmatch(r"Markdown==([^\s;]+)", requirement))
    ]
    if len(markdown_pins) != 1:
        raise MarkdownRenderError(
            "requirements-public-alpha.txt must contain exactly one exact Markdown pin"
        )
    try:
        installed = distribution_version("Markdown")
    except PackageNotFoundError as exc:
        raise MarkdownRenderError(
            "Python Markdown is required; install requirements-public-alpha.txt "
            "in an isolated environment"
        ) from exc
    if installed != markdown_pins[0]:
        raise MarkdownRenderError(
            "installed Python Markdown does not match the bound dependency lock: "
            f"expected {markdown_pins[0]}, found {installed}"
        )


def render_markdown(markdown_text: str, root: Path) -> str:
    """Render article HTML with the site's exact extensions and dependency pin."""
    try:
        import markdown
    except ImportError as exc:
        raise MarkdownRenderError(
            "Python Markdown is required; install requirements-public-alpha.txt in an isolated environment"
        ) from exc
    require_locked_markdown_dependency(root)
    return markdown.markdown(
        markdown_text,
        extensions=MARKDOWN_EXTENSIONS,
        extension_configs={"toc": {"toc_depth": "2-2"}},
        output_format="html5",
    )
