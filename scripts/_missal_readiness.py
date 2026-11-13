"""Compose daily-reader readiness from validated, text-free owning reports.

Availability, target fidelity and complete execution are different questions.
This report never counts an alternative witness as another target, treats an
unselected legitimate choice as a missing prayer, or promotes a source body
(which may end in a printed cue) to a complete spoken execution.
"""
from __future__ import annotations

from copy import deepcopy

from _missal_coverage import validate_summary

SCHEMA = "triptych-daily-missal-readiness/v1"
CALENDARS = ("roman-1962", "postconciliar")
LANGUAGES = ("en", "la")
# Six consecutive liturgical years cover the joint cycles, not merely the two
# marginal sets {A,B,C} and {I,II}. They do not exhaust Gregorian occurrences.
CYCLE_YEARS = (
    (2026, "A", "II"), (2027, "B", "I"), (2028, "C", "II"),
    (2029, "A", "I"), (2030, "B", "II"), (2031, "C", "I"),
)


def unresolved(reason: str, **details: object) -> dict:
    return {"state": "unresolved", "reason": reason, **details}


def language_inventory(summary: dict, scope: str) -> list[dict]:
    """Keep the owner's identity denominator and all relationship qualifications."""
    validate_summary(summary)
    if summary["scope"] != scope:
        raise ValueError(f"readiness expected {scope} coverage")
    result = []
    for lang in LANGUAGES:
        source = next((row for row in summary["languages"] if row["lang"] == lang), None)
        if source is None:
            raise ValueError(f"readiness {scope} coverage omits {lang}")
        missing = source["targets"] - source["available_targets"]
        result.append({
            "lang": lang,
            "state": "incomplete" if missing else "available-within-represented-scope",
            "targets": source["targets"],
            "available_targets": source["available_targets"],
            "unavailable_targets": missing,
            "occurrences": source["occurrences"],
            "available_occurrences": source["available"],
            "availability_occurrences": deepcopy(source["availability"]),
            "exact_target_targets": source["exact_target_targets"],
            "relationship_occurrences": deepcopy(source["relationships"]),
            "collation_occurrences": deepcopy(source["collations"]),
            "witnesses": deepcopy(source["witnesses"]),
            "scripture_targets": source["scripture_targets"],
            "scripture_occurrences": source["scripture_occurrences"],
        })
    return result


def build_readiness(completeness: dict) -> dict:
    """Compose an acceptance report without loading or owning another corpus.

    The caller first validates the three owning reports through complete-missal's
    ordinary composition. Unreported dimensions stay aggregate unknowns: in
    particular, no conclusion-free text receives a fabricated execution gap.
    """
    if completeness.get("schema") != "triptych-complete-missal-completeness/v1":
        raise ValueError("readiness requires the validated complete-missal report")
    if completeness.get("check", {}).get("valid") is not True:
        raise ValueError("readiness requires valid owning reports")
    coverage = {row["calendar"]: row for row in completeness.get("coverage", [])}
    families = {row["calendar"]: row for row in completeness.get("families", [])}
    results = []
    for calendar in CALENDARS:
        if calendar not in families:
            raise ValueError(f"readiness report omits {calendar}")
        if calendar not in coverage:
            results.append({"calendar": calendar, "status": "unresolved",
                            "source_inventory": unresolved("typed-coverage-not-reported")})
            continue
        typed = coverage[calendar]
        proper = language_inventory(typed["propers"], "calendar")
        ordinary = language_inventory(typed["ordinary"], "ordinary")
        expected = typed["propers"].get("expected_inventory") or {}
        unknown = families[calendar]["textual"]["unknown_slots"]
        missing = any(row["unavailable_targets"] for row in proper + ordinary)
        unrepresented = deepcopy(expected.get("not_represented") or [])
        results.append({
            "calendar": calendar,
            "status": "incomplete" if missing or unrepresented else "unresolved",
            "source_inventory": {
                "denominator": "represented-units",
                "propers": proper,
                "ordinary": ordinary,
                "ordinary_extent": "all represented elements, including headings and rubrics; not a spoken-prayer count",
            },
            "expected_universe": {
                "state": expected.get("whole_inventory_state", "unresolved"),
                "target_states": deepcopy(expected.get("target_states") or {}),
                "not_represented": unrepresented,
                "boundaries": deepcopy(expected.get("boundaries") or []),
                "review_ref": expected.get("review_ref"),
            },
            "english_policy": {
                "study_translations": "source-admitted-study-translations-with-visible-qualification",
                "approved_liturgical_translation_required": False,
                "fidelity_review": unresolved("owning-summaries-do-not-report-per-target-review-status"),
            },
            "execution_extent": unresolved(
                "owning-summaries-do-not-measure-complete-source-controlled-execution",
                per_target_classification="not-reported; conclusion-free texts are not presumed incomplete",
            ),
            "choice_space": unresolved(
                "all-permitted-contexts-and-choices-not-enumerated",
                caller_choice_required_is_a_source_gap=False,
                unresolved_common_selections=deepcopy(unknown.get("unresolved_common_set_selections") or []),
            ),
            "scripture_execution": unresolved("Bible-delegation-is-not-an-exact-Missal-body-or-a-runtime-resolution-proof"),
        })
    return {
        "schema": SCHEMA,
        "status": "incomplete" if any(row["status"] == "incomplete" for row in results) else "unresolved",
        "ready": bool(results) and all(row["status"] == "ready" for row in results),
        "calendars": results,
        "scope": {
            "source": "validated complete-missal composition of mass-propers, mass-ordinary and calendar-days",
            "pre_1955_included": False,
            "runtime_executed": False,
            "required_postconciliar_cycle_years": [
                {"ending": year, "sunday": sunday, "weekday": weekday}
                for year, sunday, weekday in CYCLE_YEARS
            ],
            "gregorian_model_span": {"first": 2020, "last": 2120, "executed": False},
            "uncovered_by_cycle_years": [
                "all Gregorian weekday, leap-day and Easter interactions",
                "all territorial, dedication-location and local calendar contexts",
                "every permitted Mass, form, commemoration, source path, Ordinary option and oration choice",
                "native browser rendering, both languages, source qualifications and complete execution",
            ],
            "readiness_limit": "Available source records alone cannot establish a complete daily Mass. No current owning summary proves all execution and choice dimensions.",
        },
    }


def render_text(report: dict) -> None:
    print(f"daily missal readiness: {report['status']}")
    for family in report["calendars"]:
        print(f"{family['calendar']}: {family['status']}")
        inventory = family["source_inventory"]
        for scope in ("propers", "ordinary"):
            for row in inventory.get(scope, []):
                print(f"  {scope} {row['lang']}: {row['available_targets']}/{row['targets']} represented targets available; "
                      f"{row['exact_target_targets']} exact-target")
        print("  complete execution, reviewed English fidelity and all-choice coverage: unresolved")
    print("Required Sunday/weekday cycle combinations: A/II, B/I, C/II, A/I, B/II, C/I")
    print("Runtime checks were not run by this source-readiness report.")
