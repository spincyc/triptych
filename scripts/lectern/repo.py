"""The checkout root, refusal type, and shared reader cache."""
from __future__ import annotations

import threading
from collections import OrderedDict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]


class Refused(Exception):
    """A request the data or a tool declined, with the reason it gave."""


class _Cache:
    """A small thread-safe LRU, so a reader paging back and forth pays once."""

    def __init__(self, size: int) -> None:
        self.size = size
        self.items: OrderedDict[object, Any] = OrderedDict()
        self.lock = threading.Lock()

    def get(self, key: object) -> Any:
        with self.lock:
            if key in self.items:
                self.items.move_to_end(key)
                return self.items[key]
        return None

    def put(self, key: object, value: Any) -> Any:
        with self.lock:
            self.items[key] = value
            self.items.move_to_end(key)
            while len(self.items) > self.size:
                self.items.popitem(last=False)
        return value
