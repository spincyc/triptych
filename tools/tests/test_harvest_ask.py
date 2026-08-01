"""`harvest ask` — the one verb in this repository that calls a model.

Nothing here reaches a model. The call itself is one function, `_ask_model`,
and every test below either replaces it or exercises a path that never gets to
it, because a test that needed the network to pass would stop being run.

What is worth asserting is not that the model answers well — it cannot be — but
the three things around the answer that are this tool's own work: that a dry run
spends nothing and still says what it would ask, that what `ask` writes is
exactly what `record` reads, and that the model a run is stamped with is read
out of the answer rather than assumed from the request.
"""

from __future__ import annotations

import argparse
import importlib.machinery
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load_harvest():
    loader = importlib.machinery.SourceFileLoader("harvest_tool", str(ROOT / "tools" / "harvest"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


harvest = load_harvest()


def arguments(**overrides) -> argparse.Namespace:
    defaults = dict(
        corpus=None, passage=["Psalms 24", "Luke 21"], runs=2, limit=0, top=5,
        by_chapter=False, out="unset", model="opus", jobs=1, budget=0.0,
        record=False, dry_run=False,
    )
    return argparse.Namespace(**{**defaults, **overrides})


class DryRunTests(unittest.TestCase):
    """A dry run is the answer to "what will this cost me", so it cannot cost."""

    def test_a_dry_run_never_reaches_the_call(self) -> None:
        def refuse(*args, **kwargs):
            raise AssertionError("a dry run asked the model")

        original, harvest._ask_model = harvest._ask_model, refuse
        try:
            payload = harvest.run_ask(arguments(dry_run=True))
        finally:
            harvest._ask_model = original
        self.assertEqual(payload["status"], "dry-run")

    def test_a_dry_run_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as scratch:
            out = Path(scratch) / "runs"
            harvest.run_ask(arguments(dry_run=True, out=str(out)))
            self.assertFalse(out.exists(), "a dry run created its output directory")

    def test_a_dry_run_reports_the_scale_it_would_run_at(self) -> None:
        payload = harvest.run_ask(arguments(dry_run=True, runs=3))
        self.assertEqual(payload["passages"], 2)
        self.assertEqual(payload["runs"], 3)
        self.assertEqual(payload["queries"], 6, "one query a passage a run")

    def test_a_dry_run_shows_the_prompt_rather_than_describing_it(self) -> None:
        """Paraphrase would let the shown prompt and the sent one diverge."""
        payload = harvest.run_ask(arguments(dry_run=True))
        self.assertEqual(payload["prompt"], harvest._ask_prompt("Psalms 24", 5))

    def test_the_prompt_carries_what_record_will_enforce(self) -> None:
        """A prompt that omitted the cutoff or the roles would spend queries on
        answers `record` then refuses."""
        prompt = harvest._ask_prompt("Psalms 24", 5)
        self.assertIn(str(harvest.CUTOFF_YEAR), prompt)
        for role in harvest.ROLES:
            self.assertIn(role, prompt)
        self.assertIn(harvest.NUMBERING_NOTE, prompt)

    def test_the_schema_and_the_validator_agree_on_the_roles(self) -> None:
        """Both are derived from ROLES; neither restates it."""
        schema = harvest._ask_schema()
        item = schema["properties"]["works"]["items"]
        self.assertEqual(item["properties"]["role"]["enum"], list(harvest.ROLES))
        self.assertEqual(sorted(item["required"]), ["author", "death_year", "role", "title"])
        # And the schema is what the CLI will actually be handed.
        json.dumps(schema)

    def test_the_schema_refuses_every_blank_that_record_refuses(self) -> None:
        """The docstring's promise, asserted against `_check_work` itself.

        `_ask_schema` says it is "derived from what `record` will accept", and
        for the roles it is. For the string fields it was not: a bare
        `{"type": "string"}` admits `""` while `_check_work` refuses it, so an
        answer could validate at ask time and be refused at record time. The
        whole-canon audit of 2026-08-01 hit exactly that — one empty title on
        Sirach cost the recording of all seventy-two books in that run.
        """
        item = harvest._ask_schema()["properties"]["works"]["items"]
        blank = {"author": "", "title": "", "role": "church-father", "death_year": 400}
        refused: list[str] = []
        harvest._check_work(blank, "where", refused)
        for field in ("author", "title"):
            with self.subTest(field=field):
                self.assertTrue(
                    any(f"{field} is required" in problem for problem in refused),
                    "record refuses a blank here",
                )
                self.assertEqual(
                    item["properties"][field].get("minLength"),
                    1,
                    "so the ask schema must refuse it too",
                )


class ModelIdentityTests(unittest.TestCase):
    """The stamp comes from the answer or the run stops. Never from the request."""

    def assistant(self, model: str) -> dict:
        return {"type": "assistant", "message": {"model": model, "content": []}}

    def test_the_model_is_read_from_the_assistant_messages(self) -> None:
        served = harvest._answered_by(
            [self.assistant("claude-opus-5"), self.assistant("claude-opus-5"),
             {"type": "result", "subtype": "success"}]
        )
        self.assertEqual(served, "claude-opus-5")

    def test_a_helper_model_in_the_usage_tally_does_not_become_the_stamp(self) -> None:
        """The real failure this guards. An opus query bills a helper model, so
        `modelUsage` names two and cannot say which wrote the answer; the
        assistant messages name one."""
        events = [
            self.assistant("claude-opus-5"),
            {
                "type": "result", "subtype": "success",
                "modelUsage": {
                    "claude-haiku-4-5-20251001": {"outputTokens": 40},
                    "claude-opus-5": {"outputTokens": 900},
                },
            },
        ]
        self.assertEqual(harvest._answered_by(events), "claude-opus-5")

    def test_an_answer_naming_no_model_stops_the_run(self) -> None:
        with self.assertRaises(ValueError):
            harvest._answered_by([{"type": "result", "subtype": "success"}])

    def test_two_models_writing_one_answer_stops_the_run(self) -> None:
        with self.assertRaises(ValueError) as raised:
            harvest._answered_by([self.assistant("claude-opus-5"),
                                  self.assistant("claude-opus-4-8")])
        self.assertIn("one model that produced it", str(raised.exception))

    def test_a_run_is_stamped_with_the_answer_not_the_request(self) -> None:
        """--model is a request. `opus` is an alias and resolves to whatever is
        current, so the alias must never reach the ledger."""
        with tempfile.TemporaryDirectory() as scratch:
            payload = self.ask_with_stub(scratch, answered_by="claude-opus-5")
        self.assertEqual(payload["model"], "claude-opus-5")
        self.assertNotIn("opus'", str(payload["results"]))
        self.assertIn("claude-opus-5", payload["results"][0])

    def test_answers_from_two_models_within_a_run_are_refused(self) -> None:
        served = iter(["claude-opus-5", "claude-opus-4-8"])

        def stub(prompt, *, model, budget=0.0):
            return [], next(served)

        with tempfile.TemporaryDirectory() as scratch:
            with self.assertRaises(ValueError) as raised:
                self.ask_with_stub(scratch, stub=stub, runs=1)
        self.assertIn("a run records one model", str(raised.exception))

    def ask_with_stub(self, scratch, *, answered_by="claude-opus-5", stub=None, runs=1):
        works = [
            {"author": "Augustine of Hippo", "title": "Enarrationes in Psalmos",
             "role": "church-father", "death_year": 430,
             "aliases": ["Expositions on the Psalms"]},
        ]
        stub = stub or (lambda prompt, *, model, budget=0.0: (works, answered_by))
        original, harvest._ask_model = harvest._ask_model, stub
        try:
            return harvest.run_ask(
                arguments(out=str(Path(scratch) / "runs"), runs=runs)
            )
        finally:
            harvest._ask_model = original


class HandsToRecordTests(unittest.TestCase):
    """What `ask` writes is what `record` reads — not a second format."""

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.out = Path(self.scratch.name) / "runs"
        self.works = [
            {"author": "Augustine of Hippo", "title": "Enarrationes in Psalmos",
             "role": "church-father", "death_year": 430},
            {"author": "Cassiodorus", "title": "Expositio Psalmorum",
             "role": "ecclesiastical-writer", "death_year": 585},
        ]

    def ask(self, **overrides):
        def stub(prompt, *, model, budget=0.0):
            return list(self.works), "claude-opus-5"

        original, harvest._ask_model = harvest._ask_model, stub
        try:
            return harvest.run_ask(arguments(out=str(self.out), runs=2, **overrides))
        finally:
            harvest._ask_model = original

    def test_one_results_file_a_run(self) -> None:
        payload = self.ask()
        self.assertEqual(len(payload["results"]), 2)
        self.assertEqual(len({Path(p).name for p in payload["results"]}), 2)

    def test_record_ingests_what_ask_wrote_unedited(self) -> None:
        """The contract in one assertion: no reshaping between the two verbs."""
        payload = self.ask()
        ledger = Path(self.scratch.name) / "ledger.yaml"
        outcomes = [
            harvest.run_record(
                argparse.Namespace(
                    results=results, model=payload["model"],
                    audited_on=payload["audited_on"], ledger=str(ledger),
                    allow_shrink=False,
                )
            )
            for results in payload["results"]
        ]
        self.assertEqual(outcomes[0]["status"], "recorded")
        recorded = harvest._ledger_runs(harvest._load(ledger))
        self.assertEqual(recorded[0]["model"], "claude-opus-5")
        self.assertEqual(sorted(recorded[0]["passages"]), ["Luke 21", "Psalms 24"])

    def test_two_runs_that_said_the_same_thing_are_one_run_and_ask_says_so(self) -> None:
        """The ledger keys a run by what it said, so identical runs collapse —
        correct, and the same guard that makes re-recording a file a no-op. But
        confidence is appearances over runs, so an operator who thinks two runs
        of corroboration landed where one did has a wrong number, not a missing
        one. The stub here answers identically every time; a model would not."""
        ledger = Path(self.scratch.name) / "ledger.yaml"
        payload = self.ask(record=True, ledger=str(ledger))
        self.assertEqual(payload["runs"], 2)
        self.assertEqual(payload["identical_runs"], 1)
        self.assertEqual(len(harvest._ledger_runs(harvest._load(ledger))), 1)

    def test_the_reported_record_command_is_the_one_that_works(self) -> None:
        payload = self.ask()
        for command, results in zip(payload["record_with"], payload["results"]):
            self.assertIn(f"--results {results}", command)
            self.assertIn(f"--model {payload['model']}", command)
            self.assertIn(f"--audited-on {payload['audited_on']}", command)

    def test_record_is_left_to_record_unless_asked_for(self) -> None:
        ledger = Path(self.scratch.name) / "untouched.yaml"
        self.ask(ledger=str(ledger))
        self.assertFalse(ledger.exists(), "ask wrote the ledger without --record")

    def test_with_record_the_ledger_is_stamped_from_the_answer(self) -> None:
        ledger = Path(self.scratch.name) / "ledger.yaml"
        payload = self.ask(record=True, ledger=str(ledger))
        recorded = harvest._ledger_runs(harvest._load(ledger))
        self.assertEqual([r["model"] for r in recorded], ["claude-opus-5"])
        self.assertEqual([r["audited_on"] for r in recorded], [payload["audited_on"]])
        self.assertEqual(set(payload["recorded"]), {r["run_id"] for r in recorded})

    def test_a_passage_that_fails_is_dropped_rather_than_failing_the_run(self) -> None:
        """A run is a set of passages; the answered ones are evidence either way."""
        def stub(prompt, *, model, budget=0.0):
            if "Luke 21" in prompt:
                raise ValueError("no answer")
            return list(self.works), "claude-opus-5"

        original, harvest._ask_model = harvest._ask_model, stub
        try:
            payload = harvest.run_ask(arguments(out=str(self.out), runs=1))
        finally:
            harvest._ask_model = original
        self.assertEqual(payload["failures"], 1)
        recorded = harvest._load(Path(payload["results"][0]))
        self.assertEqual(sorted(recorded["passages"]), ["Psalms 24"])

    def test_a_run_that_answers_nothing_is_not_written(self) -> None:
        def stub(prompt, *, model, budget=0.0):
            raise ValueError("no answer")

        original, harvest._ask_model = harvest._ask_model, stub
        try:
            with self.assertRaises(ValueError):
                harvest.run_ask(arguments(out=str(self.out), runs=1))
        finally:
            harvest._ask_model = original
        self.assertEqual(list(self.out.glob("*.yaml")) if self.out.exists() else [], [])


class WorklistTests(unittest.TestCase):
    """What to ask about comes from `plan`, so the two cannot disagree."""

    def test_explicit_passages_are_taken_in_order_and_deduplicated(self) -> None:
        chosen = harvest._ask_worklist(arguments(passage=["Psalms 24", "Psalms 24", "Luke 21"]))
        self.assertEqual(chosen, ["Psalms 24", "Luke 21"])

    def test_a_corpus_worklist_is_what_plan_reports_as_pending(self) -> None:
        with tempfile.TemporaryDirectory() as scratch:
            corpus = Path(scratch) / "corpus.yaml"
            corpus.write_text(
                "passages:\n- passage: 'Isaiah 63:16-64:7'\n- passage: 'Psalms 24:1-24:3'\n",
                encoding="utf-8",
            )
            ledger = Path(scratch) / "ledger.yaml"
            shared = dict(corpus=str(corpus), runs=3, limit=0, ledger=str(ledger))
            planned = harvest.run_plan(argparse.Namespace(by_chapter=True, **shared))
            asked = harvest._ask_worklist(
                arguments(passage=[], by_chapter=True, **shared)
            )
        self.assertEqual(asked, [entry["passage"] for entry in planned["passages"]])
        self.assertIn("Isaiah 64", asked, "a two-chapter reference is two loci")

    def test_asking_with_neither_a_corpus_nor_a_passage_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            harvest._ask_worklist(arguments(passage=[], corpus=None))


if __name__ == "__main__":
    unittest.main()
