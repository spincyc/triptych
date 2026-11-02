"""The optional print workflow selects one identity and verifies its delivery."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

import yaml

from tools.tests.test_pages_publication_selection import DeploymentFixture, ROOT


class ManualPrintWorkflowTests(DeploymentFixture, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.workflow = yaml.safe_load((ROOT / ".github/workflows/print-document.yml").read_text())
        self.steps = {step["name"]: step for step in self.workflow["jobs"]["print"]["steps"]}
        self.env.update(DOCUMENT="publication:gpt/study", PRINT_EDITION="main",
                        PRINT_OUT=".scratch/print-document-ci", PRINT_IMAGE=self.pages()["env"]["TEXLIVE_IMAGE"],
                        GITHUB_OUTPUT=str(self.root / "toolchain-output"),
                        DEPLOYMENT_TEST_SCRIPTS=str(ROOT / "scripts"))
        self.write(".github/workflows/pages.yml", (ROOT / ".github/workflows/pages.yml").read_text())
        self.write("src/gpt/study/generation-metadata.tex", "% source metadata fixture\n")
        self.write("tools/tpt", "import sys\nraise SystemExit(0 if '--phase' in sys.argv else 99)\n")
        # The real print selector and dependency query run; the owning metadata
        # and compiler are boundary doubles, as in the Make graph tests.
        self.write("tools/check-generation-metadata", "import sys\n"
                   "assert sys.argv[1:] == ['--provider', 'gpt', '--document', 'study']\n")
        self.write("bin/python", f"#!{sys.executable}\n" + r'''
import json
import os
from pathlib import Path
import sys

args = sys.argv[1:]
if args == ["-"]:
    os.execv(sys.executable, [sys.executable, "-"])
if args[:3] != ["tools/tpt", "print-document", "check"]:
    raise SystemExit("unexpected manual print command: " + repr(args))
sys.path.insert(0, os.environ["DEPLOYMENT_TEST_SCRIPTS"])
import _print_document as printing
try:
    root = Path(os.environ["DEPLOYMENT_TEST_ROOT"])
    selected = printing.select(args[args.index("--document") + 1], args[args.index("--edition") + 1], root=root)
    result = printing.check(selected, root=root)
    print(json.dumps({"status": "valid", "document": printing.public_recipe(result)}))
except (ValueError, OSError) as error:
    raise SystemExit(str(error))
''').chmod(0o755)
        self.write("bin/git", "#!/bin/sh\n[ \"$*\" = 'diff --exit-code' ] || exit 99\n").chmod(0o755)
        self.write("bin/docker", f"#!{sys.executable}\n" + r'''
import hashlib
import json
import os
from pathlib import Path
import sys

args = sys.argv[1:]
root = Path(os.environ["DEPLOYMENT_TEST_ROOT"])
with open(root / "docker.jsonl", "a") as log:
    log.write(json.dumps(args) + "\n")
assert args[0] == "run", "the fixture never pulls a container or contacts a registry"
assert args[args.index("--network") + 1] == "none"
command = args[args.index("python"):]
assert command[:4] == ["python", "tools/tpt", "print-document", "build"]
assert command.count("--document") == command.count("--edition") == 1
document = command[command.index("--document") + 1]
destination = root / os.environ["PRINT_OUT"]
selection = json.loads((destination / "selection.json").read_text())
assert document == selection["document"]["id"]
assert command[command.index("--edition") + 1] == os.environ["PRINT_EDITION"]
assert command[command.index("--out") + 1] == os.environ["PRINT_OUT"]
pdf = destination / "study--fixture.pdf"
pdf.write_bytes(b"%PDF-1.4\nselected fixture\n")
receipt = {"status": "built", "output_format": "pdf", "document": selection["document"],
           "path_base": "receipt-directory", "output": pdf.name,
           "receipt": "study--fixture.print.json", "bytes": pdf.stat().st_size,
           "output_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest()}
(destination / "study--fixture.print.json").write_text(json.dumps(receipt))
''').chmod(0o755)

    def step(self, name, *, env=None):
        return self.shell(self.steps[name]["run"], env=env)

    def validate_and_build(self):
        for name in ("Validate the single document selection", "Read the shared immutable toolchain", "Build the selected PDF"):
            result = self.step(name)
            self.assertEqual(result.returncode, 0, name + ": " + result.stdout + result.stderr)

    def test_manual_workflow_is_dispatch_only_and_has_no_deployment_authority(self):
        # PyYAML's YAML 1.1 loader treats the Actions key `on` as True.
        triggers = self.workflow.get("on", self.workflow.get(True))
        self.assertEqual(set(triggers), {"workflow_dispatch"})
        self.assertEqual(self.workflow["permissions"], {"contents": "read", "packages": "read"})
        self.assertEqual(set(self.workflow["jobs"]), {"print"})
        self.assertNotIn("permissions", self.workflow["jobs"]["print"])
        for step in self.steps.values():
            self.assertNotIn("${{ inputs.", step.get("run", ""))
            self.assertNotIn("pages", step.get("uses", ""))
        env = self.workflow["jobs"]["print"]["env"]
        self.assertEqual(env["DOCUMENT"], "${{ inputs.document }}")
        self.assertEqual(env["PRINT_EDITION"], "${{ inputs.edition }}")

    def test_manual_shell_builds_only_the_validated_document_and_attests_one_pdf(self):
        source = self.root / "src/gpt/study/main.tex"
        before = source.read_bytes()
        self.validate_and_build()
        result = self.step("Confirm one PDF and its receipt")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        calls = [json.loads(line) for line in (self.root / "docker.jsonl").read_text().splitlines()]
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].count("publication:gpt/study"), 1)
        self.assertEqual(source.read_bytes(), before)
        self.assertFalse((self.root / "pdf").exists())
        self.assertFalse((self.root / "release").exists())
        self.assertFalse((self.root / "build/public-alpha").exists())
        upload = self.steps["Upload the generated print copy"]["with"]
        self.assertEqual(set(upload["path"].splitlines()),
                         {".scratch/print-document-ci/*.pdf", ".scratch/print-document-ci/*.print.json"})
        self.assertEqual(upload["if-no-files-found"], "error")

    def test_invalid_multiple_and_shell_input_never_reach_container(self):
        for document in ("publication:gpt/../study", "publication:gpt/missing",
                         "publication:gpt/study publication:gpt/held",
                         "publication:gpt/study;touch .scratch/injected",
                         "publication:gpt/study$(touch .scratch/injected)"):
            with self.subTest(document=document):
                result = self.step("Validate the single document selection", env={**self.env, "DOCUMENT": document})
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((self.root / ".scratch/injected").exists())
                self.assertFalse((self.root / "docker.jsonl").exists())

    def test_receipt_gate_rejects_tampering_and_nonportable_paths(self):
        self.validate_and_build()
        destination = self.root / self.env["PRINT_OUT"]
        pdf = next(destination.glob("*.pdf"))
        receipt = next(destination.glob("*.print.json"))
        original_pdf, original_receipt = pdf.read_bytes(), receipt.read_text()
        mutations = (
            "extra-pdf", "extra-receipt", "different-selection", "changed-bytes",
            "missing-receipt", "missing-path-base", "wrong-path-base",
            "absolute-output", "traversal-output", "wrong-receipt-basename",
            "absolute-receipt", "traversal-receipt", "symlink-output", "symlink-receipt",
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                pdf.unlink(missing_ok=True)
                receipt.unlink(missing_ok=True)
                pdf.write_bytes(original_pdf)
                receipt.write_text(original_receipt)
                extra = destination / "extra.pdf"
                extra.unlink(missing_ok=True)
                extra_receipt = destination / "extra.print.json"
                extra_receipt.unlink(missing_ok=True)
                if mutation == "extra-pdf":
                    extra.write_bytes(original_pdf)
                elif mutation == "extra-receipt":
                    extra_receipt.write_text(original_receipt)
                elif mutation == "different-selection":
                    data = json.loads(original_receipt)
                    data["document"]["id"] = "publication:gpt/held"
                    receipt.write_text(json.dumps(data))
                elif mutation == "changed-bytes":
                    pdf.write_bytes(b"changed output")
                elif mutation == "missing-receipt":
                    receipt.unlink()
                elif mutation.startswith("symlink-"):
                    path, payload = (pdf, original_pdf) if mutation == "symlink-output" else (receipt, original_receipt.encode())
                    actual = destination.parent / ("external-" + path.name)
                    actual.write_bytes(payload)
                    path.unlink()
                    path.symlink_to(actual)
                else:
                    data = json.loads(original_receipt)
                    if mutation == "missing-path-base":
                        del data["path_base"]
                    else:
                        field, value = {
                            "wrong-path-base": ("path_base", "repository"),
                            "absolute-output": ("output", str(pdf.resolve())),
                            "traversal-output": ("output", "../print-document-ci/" + pdf.name),
                            "wrong-receipt-basename": ("receipt", "another.print.json"),
                            "absolute-receipt": ("receipt", str(receipt.resolve())),
                            "traversal-receipt": ("receipt", "../print-document-ci/" + receipt.name),
                        }[mutation]
                        data[field] = value
                    receipt.write_text(json.dumps(data))
                result = self.step("Confirm one PDF and its receipt")
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
