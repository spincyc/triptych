"""Conserve exact negative fingerprints independently of English availability."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import tomllib
import unittest


REPOSITORY = Path(__file__).resolve().parents[2]


def load_tool():
    loader = importlib.machinery.SourceFileLoader(
        "test_public_alpha_quarantine_tool", str(REPOSITORY / "tools/public-alpha")
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def synthetic_record(marker, mass="fixture"):
    return {
        "mass": mass, "form_id": "main", "proper": "fixture", "cycle": "all",
        "occurrence": 1, "lang": "en", "extent": "body",
        "quarantined_text_sha256": [hashlib.sha256(marker.encode()).hexdigest()],
        "source_provenance": {"rejected_detectors": ["synthetic-test-source"]},
    }


def active_record(row):
    return {key: value for key, value in row.items() if key != "source_provenance"} | row["source_provenance"]


def write_test_inventory(tool, root, baseline, active, receipts=()):
    """Write project-created test metadata using the production registry shape."""
    def scalar(value):
        if isinstance(value, dict):
            return "{ " + ", ".join(f"{key} = {scalar(item)}" for key, item in value.items()) + " }"
        return json.dumps(value, ensure_ascii=False)

    lines = []
    if not active:
        lines.append("untranslated = []")
    for row in active:
        lines.append("[[untranslated]]")
        lines.extend(f"{key} = {scalar(value)}" for key, value in row.items())
    lines.extend([
        "[english_quarantine]", "schema = 1",
        f'baseline_commit = "{tool.POSTCONCILIAR_QUARANTINE_BASELINE_COMMIT}"',
        "baseline_inventory_sha256 = "
        f'"{tool.POSTCONCILIAR_QUARANTINE_BASELINE_INVENTORY_SHA256}"',
    ])
    for row in baseline:
        lines.append("[[english_quarantine.baseline]]")
        lines.extend(f"{key} = {scalar(value)}" for key, value in row.items())
    for row in receipts:
        lines.append("[[english_quarantine.admission_receipts]]")
        lines.extend(f"{key} = {scalar(value)}" for key, value in row.items())
    path = root / tool.POSTCONCILIAR_TRANSLATIONS_RELATIVE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def install_test_quarantine(tool, root, marker):
    """Give unrelated public-alpha tests an explicit synthetic baseline."""
    baseline = [synthetic_record(marker)]
    tool.POSTCONCILIAR_QUARANTINE_BASELINE_TARGETS = 1
    tool.POSTCONCILIAR_QUARANTINE_BASELINE_ROWS = 1
    tool.POSTCONCILIAR_QUARANTINE_BASELINE_SHA256 = hashlib.sha256(
        canonical(baseline).encode()
    ).hexdigest()
    return write_test_inventory(tool, root, baseline, [active_record(baseline[0])])


class PublicAlphaQuarantineTest(unittest.TestCase):
    def setUp(self):
        scratch = REPOSITORY / ".scratch/pc-quarantine-conservation-20261029/tests"
        scratch.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.tool = load_tool()
        self.tool.ROOT = self.root
        self.markers = ["PROJECT-CREATED QUARANTINE BASELINE " + str(index) for index in range(2)]
        self.baseline = [synthetic_record(marker, f"fixture-{index}")
                         for index, marker in enumerate(self.markers)]
        duplicate = deepcopy(self.baseline[0])
        duplicate["mass"] = "fixture-duplicate"
        self.baseline.append(duplicate)
        self.active = [active_record(self.baseline[0])]
        self.receipts = []
        self.tool.POSTCONCILIAR_QUARANTINE_BASELINE_TARGETS = 3
        self.tool.POSTCONCILIAR_QUARANTINE_BASELINE_ROWS = 2
        self.tool.POSTCONCILIAR_QUARANTINE_BASELINE_SHA256 = hashlib.sha256(
            canonical(sorted(self.baseline, key=canonical)).encode()
        ).hexdigest()
        self.write()

    def write(self):
        return write_test_inventory(self.tool, self.root, self.baseline, self.active, self.receipts)

    def receipt(self, rows, name="fixture-admission.json"):
        relative = self.tool.POSTCONCILIAR_ADMISSION_RECEIPTS_RELATIVE / name
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        # Admission files can preserve the same old row in two views.
        path.write_text(json.dumps({"superseded_unavailable_dictionaries": rows,
                                    "targets": [{"old": row} for row in rows]}) + "\n")
        self.receipts.append({"path": relative.as_posix(),
                              "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
        return path

    def test_baseline_survives_admission_of_every_active_target(self):
        self.active = []
        self.write()
        self.assertEqual(self.tool.postconciliar_quarantined_text_hashes(),
                         {hashlib.sha256(marker.encode()).hexdigest() for marker in self.markers})

    def test_active_and_admitted_additional_hashes_are_all_scanned(self):
        active_marker = "PROJECT-CREATED ACTIVE EXTRA QUARANTINE"
        admitted_marker = "PROJECT-CREATED ADMITTED EXTRA QUARANTINE"
        self.active.append(active_record(synthetic_record(active_marker, "extra-active")))
        self.receipt([active_record(synthetic_record(admitted_marker, "extra-admitted"))])
        self.write()
        expected = {hashlib.sha256(marker.encode()).hexdigest()
                    for marker in [*self.markers, active_marker, admitted_marker]}
        self.assertEqual(self.tool.postconciliar_quarantined_text_hashes(), expected)
        path = self.root / "src/web/data/structure/new-family/fixture.json"
        path.parent.mkdir(parents=True)
        for marker in [*self.markers, active_marker, admitted_marker]:
            with self.subTest(marker=marker):
                path.write_text(json.dumps({"unlabelled": marker}))
                with self.assertRaisesRegex(self.tool.ReleaseError, "quarantined English body") as caught:
                    self.tool.validate_liturgical_public_data(path)
                self.assertNotIn(marker, str(caught.exception))

    def test_missing_or_substituted_baseline_fails_even_at_same_count(self):
        original = deepcopy(self.baseline)
        for mutation in ("missing", "hash", "target", "source", "body"):
            with self.subTest(mutation=mutation):
                self.baseline = deepcopy(original)
                if mutation == "missing":
                    self.baseline.pop()
                elif mutation == "hash":
                    self.baseline[0]["quarantined_text_sha256"] = ["f" * 64]
                elif mutation == "target":
                    self.baseline[0]["mass"] = "substituted-target"
                elif mutation == "source":
                    self.baseline[0]["source_provenance"]["rejected_detectors"] = ["substituted-source"]
                else:
                    self.baseline[0]["text"] = "PROJECT-CREATED DISALLOWED BODY FIELD"
                self.write()
                with self.assertRaises(self.tool.ReleaseError):
                    self.tool.postconciliar_quarantined_text_hashes()

    def test_missing_registry_fails_closed(self):
        self.write().write_text("untranslated = []\n")
        with self.assertRaisesRegex(self.tool.ReleaseError, "active baseline registry"):
            self.tool.postconciliar_quarantined_text_hashes()

    def test_active_or_receipt_source_ambiguity_fails_closed(self):
        for route in ("active", "receipt"):
            with self.subTest(route=route):
                wrong = active_record(deepcopy(self.baseline[0]))
                wrong["rejected_detectors"] = ["different-source"]
                self.active = [wrong] if route == "active" else []
                self.receipts = []
                if route == "receipt":
                    self.receipt([wrong])
                self.write()
                with self.assertRaisesRegex(self.tool.ReleaseError, "source or hashes changed"):
                    self.tool.postconciliar_quarantined_text_hashes()

    def test_malformed_additional_negative_records_fail_closed(self):
        original = active_record(synthetic_record("PROJECT-CREATED EXTRA NEGATIVE", "extra"))
        for mutation in ("language", "extent", "hash", "duplicate", "source", "body"):
            with self.subTest(mutation=mutation):
                extra = deepcopy(original)
                if mutation == "language":
                    extra["lang"] = "la"
                elif mutation == "extent":
                    extra["extent"] = "incipit"
                elif mutation == "hash":
                    extra["quarantined_text_sha256"] = ["malformed"]
                elif mutation == "duplicate":
                    extra["quarantined_text_sha256"] *= 2
                elif mutation == "source":
                    extra.pop("rejected_detectors")
                    extra["rights"] = "permission"
                else:
                    extra["text"] = "PROJECT-CREATED DISALLOWED BODY"
                self.active = [extra]
                self.write()
                with self.assertRaises(self.tool.ReleaseError):
                    self.tool.postconciliar_quarantined_text_hashes()

    def test_receipt_removal_omission_or_tamper_invalidates_cached_guard(self):
        row = active_record(synthetic_record("PROJECT-CREATED RECEIPT ONLY HASH", "receipt-only"))
        path = self.receipt([row])
        original = path.read_bytes()
        self.write()
        self.tool.postconciliar_quarantined_text_hashes()
        prior = path.stat()
        path.write_bytes(original.replace(b"receipt-only", b"receipt-fake"))
        os.utime(path, ns=(prior.st_atime_ns, prior.st_mtime_ns))
        with self.assertRaisesRegex(self.tool.ReleaseError, "receipt hash changed"):
            self.tool.postconciliar_quarantined_text_hashes()
        path.write_bytes(original)
        self.tool.postconciliar_quarantined_text_hashes()
        path.unlink()
        with self.assertRaisesRegex(self.tool.ReleaseError, "receipt inventory changed"):
            self.tool.postconciliar_quarantined_text_hashes()
        path.write_bytes(original)
        self.receipts = []
        self.write()
        with self.assertRaisesRegex(self.tool.ReleaseError, "receipt inventory changed"):
            self.tool.postconciliar_quarantined_text_hashes()

    def test_inventory_tamper_with_restored_mtime_invalidates_cache(self):
        path = self.write()
        self.tool.postconciliar_quarantined_text_hashes()
        before = path.stat()
        path.write_text(path.read_text().replace("synthetic-test-source", "different-test-source"))
        os.utime(path, ns=(before.st_atime_ns, before.st_mtime_ns))
        with self.assertRaisesRegex(self.tool.ReleaseError, "baseline records changed"):
            self.tool.postconciliar_quarantined_text_hashes()

    def test_real_registry_retains_all_baseline_and_admission_hashes(self):
        tool = load_tool()
        document = tomllib.loads((REPOSITORY / tool.POSTCONCILIAR_TRANSLATIONS_RELATIVE).read_text())
        registry = document["english_quarantine"]
        baseline = registry["baseline"]
        expected = {digest for row in baseline for digest in row["quarantined_text_sha256"]}
        self.assertEqual(len(baseline), 174)
        self.assertEqual(len(expected), 172)
        for row in document["untranslated"]:
            expected.update(row.get("quarantined_text_sha256", []))
        def visit(value):
            if isinstance(value, dict):
                expected.update(value.get("quarantined_text_sha256", []))
                for child in value.values():
                    visit(child)
            elif isinstance(value, list):
                for child in value:
                    visit(child)
        for receipt in registry["admission_receipts"]:
            visit(json.loads((REPOSITORY / receipt["path"]).read_bytes()))
        self.assertEqual(tool.postconciliar_quarantined_text_hashes(), expected)


if __name__ == "__main__":
    unittest.main()
