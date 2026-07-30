#!/usr/bin/env python3
"""Shared CLI launcher helpers for top-level repository tools."""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Callable

PROTOCOL_VERSION = 1

CommandHandler = Callable[[argparse.Namespace], object]
OutputRenderer = Callable[[object, argparse.Namespace], int]


def dump_json(payload: dict[str, object]) -> str:
    return json.dumps(
        {**payload, "v": PROTOCOL_VERSION},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def print_json(payload: dict[str, object], *, stream=sys.stdout) -> None:
    print(dump_json(payload), file=stream)


def fail(message: str, code: str, as_json: bool, status: int, prefix: str) -> int:
    if as_json:
        print_json(
            {
                "code": code,
                "error": message,
                "status": "error",
            },
            stream=sys.stderr,
        )
    else:
        print(f"{prefix}: {message}", file=sys.stderr)
    return status


def run_verb_cli(
    *,
    parser: argparse.ArgumentParser,
    handlers: dict[str, CommandHandler],
    renderer: OutputRenderer,
    prefix: str,
    argv: list[str] | None,
    default_verb: str | None = None,
    dependency_message: str | None = None,
    mapped_errors: dict[type[BaseException], tuple[str, int]] | None = None,
) -> int:
    arguments = parser.parse_args(argv)
    verb = getattr(arguments, "command", None) or default_verb
    if verb is None:
        parser.error("missing command")
    handler = handlers.get(verb)
    if handler is None:
        parser.error(f"unknown command: {verb}")

    as_json = bool(getattr(arguments, "json", False))
    try:
        payload = handler(arguments)
    except ModuleNotFoundError as error:
        message = str(error)
        if dependency_message:
            message = f"{message}; {dependency_message}"
        return fail(message, "dependency", as_json, 69, prefix)
    except Exception as error:
        if mapped_errors:
            for exc_type, (code, status) in mapped_errors.items():
                if isinstance(error, exc_type):
                    return fail(
                        str(error) or error.__class__.__name__,
                        code,
                        as_json,
                        status,
                        prefix,
                    )
        # An unmapped exception is a defect, not a data-validation failure.
        # The friendly one-line form makes the two indistinguishable, so keep
        # an escape hatch for diagnosing one.
        if os.environ.get("TPT_TRACEBACK"):
            raise
        return fail(
            str(error) or error.__class__.__name__,
            "internal",
            as_json,
            70,
            prefix,
        )
    return renderer(payload, arguments)
