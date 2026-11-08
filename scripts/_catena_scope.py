"""Catholic author eligibility for active Catena texts and acquisition leads.

Ecclesial facts belong to _standing's cited registry. This module applies the
Catena policy to them; an unregistered name is unreviewed, never Catholic by
default. Source-library preservation and historical research are unaffected.
"""
from __future__ import annotations

import re
import tomllib
from pathlib import Path
from typing import Any

import _standing

ROOT = Path(__file__).resolve().parents[1]
POLICY = "triptych-catena-catholic-scope/v1"
INPUTS = (_standing.REGISTRY_RELATIVE.as_posix(),)
# A consumer policy exception, not a second ecclesial classification. The cited
# canonical row preserves the maintainer's settlement AND contrary evidence.
RECEIVED_EXCEPTIONS = {
    "theophylact-of-ohrid": "guidance/liturgy/liturgical-commentators-plan-2026-09-22.md#maintainer-decisions-2026-09-22",
}


def validate(root: Path = ROOT) -> list[str]:
    """The cited standing registry must be valid before eligibility is trusted."""
    return _standing.validate(Path(root))


def _decision(status: str, reason: str, person: dict | None = None) -> dict[str, Any]:
    person = person or {}
    return {
        "policy": POLICY,
        "status": status,
        "eligible": status == "eligible",
        "person_id": person.get("id"),
        "standing": person.get("standing"),
        "reason": reason,
        "basis_sources": list(person.get("basis_sources") or []),
    }


class Scope:
    """One immutable-in-use policy snapshot per build/query, without global caching.

    Optional works is the already-loaded source library's id -> data mapping.
    Work decisions follow the intellectual work, never its edition translator,
    editor, artifact controller or constituent_of delivery container.
    """

    def __init__(self, root: Path = ROOT, works: dict | None = None) -> None:
        self.root = Path(root)
        self.errors = validate(self.root)
        # _standing.Registry deliberately tolerates missing files, but malformed
        # row fields need not be safe to index. Never index rejected facts.
        self.registry = None if self.errors else _standing.Registry(self.root)
        self.works = works
        self._work_cache: dict[str, dict | None] = {}

    def author_decision(self, name: str) -> dict[str, Any]:
        if self.errors:
            return _decision("unreviewed", "Author-standing registry is invalid: " + "; ".join(self.errors))
        person = self.registry.for_name(name)
        if person is None:
            return _decision("unreviewed", "No reviewed author identity in the author-standing registry.")
        if person.get("standing") == "non-catholic":
            return _decision("excluded", "Author is recorded outside Catholic communion.", person)
        if (person.get("id") in RECEIVED_EXCEPTIONS
                and person.get("standing") == "ecclesiastical-writer"):
            result = _decision("eligible", "Explicit received-author exception: the maintainer's 2026-09-23 Theophylact settlement, preserved with its contrary evidence in the canonical standing record.", person)
            result["policy_exception"] = RECEIVED_EXCEPTIONS[person["id"]]
            return result
        if _standing.fold(person.get("confession")) != "catholic":
            return _decision("unreviewed", "Registry does not establish Catholic communion for this author; a work-specific historical review is required.", person)
        return _decision("eligible", "Author's cited standing record establishes Catholic communion or received patristic standing.", person)

    def allowed_author(self, name: str) -> bool:
        return self.author_decision(name)["eligible"]

    def _work(self, work_id: str) -> dict | None:
        if self.works is not None:
            return self.works.get(work_id)
        if work_id not in self._work_cache:
            # IDs usually match paths, but paths are not source identities.
            # On a miss consult the records, never infer an author from the id.
            if not re.fullmatch(r"work\.[a-z0-9-]+\.[a-z0-9.-]+", work_id):
                return None
            path = self.root / "src/sources/works" / Path(*work_id.split(".")[1:]) / "work.toml"
            work = tomllib.loads(path.read_text(encoding="utf-8")) if path.is_file() else None
            if work is None or work.get("id") != work_id:
                self.works = {
                    row["id"]: row
                    for candidate in sorted((self.root / "src/sources/works").glob("*/*/work.toml"))
                    if (row := tomllib.loads(candidate.read_text(encoding="utf-8"))).get("id")
                }
                return self.works.get(work_id)
            self._work_cache[work_id] = work
        return self._work_cache[work_id]

    def work_decision(self, work_id: str) -> dict[str, Any]:
        if self.errors:
            return self.author_decision("")
        work = self._work(str(work_id))
        if work is None:
            return _decision("unreviewed", "No intellectual work record establishes the commentary author.")
        kind = str(work.get("work_type") or "")
        responsible = str(work.get("responsible") or "")
        if "anthology" in kind or kind == "patristic-collection" or re.search(r"\beditor\b", responsible, re.I):
            return _decision("unreviewed", "Container/editor identity does not establish its constituent commentary author; use the constituent work.")
        result = self.author_decision(responsible)
        namespace_person = self.registry.for_work(work_id)
        # A known namespace cannot launder a different author into eligibility.
        if namespace_person and namespace_person.get("id") != result["person_id"]:
            if namespace_person.get("standing") == "non-catholic":
                return _decision("excluded", "Work namespace belongs to an author recorded outside Catholic communion.", namespace_person)
            if result["status"] != "excluded":
                return _decision("unreviewed", "Responsible name and registered work namespace do not resolve to the same reviewed author.")
        return result

    def allowed_work(self, work_id: str) -> bool:
        return self.work_decision(work_id)["eligible"]

    def lead_decision(self, lead: dict) -> dict[str, Any]:
        """A canonical work identity and the harvested author must agree."""
        author = self.author_decision(str(lead.get("author") or ""))
        if not lead.get("work_id"):
            return author
        work = self.work_decision(str(lead["work_id"]))
        if work["status"] == "excluded":
            return work
        if author["status"] == "excluded":
            return author
        if author["eligible"] and work["eligible"] and author["person_id"] == work["person_id"]:
            return work
        return _decision("unreviewed", "Lead author and canonical intellectual work do not establish the same eligible author.")


def author_decision(name: str, root: Path = ROOT) -> dict[str, Any]:
    return Scope(root).author_decision(name)


def allowed_author(name: str, root: Path = ROOT) -> bool:
    return Scope(root).allowed_author(name)


def work_decision(work_id: str, root: Path = ROOT) -> dict[str, Any]:
    return Scope(root).work_decision(work_id)


def allowed_work(work_id: str, root: Path = ROOT) -> bool:
    return Scope(root).allowed_work(work_id)
