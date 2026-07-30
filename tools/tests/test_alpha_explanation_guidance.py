from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


class ReaderFacingReleaseStateGuidanceTest(unittest.TestCase):
  def read(self, path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")

  def test_universal_policy_keeps_release_state_out_of_reader_editions(self):
    editorial = self.read("guidance/editorial.md")
    self.assertIn(
      "Internal release and distribution states such as `alpha`, `hold`, "
      "`review`,",
      editorial,
    )
    self.assertIn(
      "Production review uses the same reader-facing composition intended",
      editorial,
    )
    self.assertIn(
      "Safety warnings and legally necessary notices remain immediately "
      "visible",
      editorial,
    )

  def test_repository_policy_forbids_reader_facing_release_labels(self):
    repository = self.read("guidance/repository.md")
    self.assertIn(
      "These internal states are not rendered\nin a PDF, web edition, catalog",
      repository,
    )
    self.assertIn(
      "without explaining the release\nworkflow",
      repository,
    )

  def test_specialized_guidance_preserves_the_common_boundary(self):
    paths = (
      "guidance/liturgy/roman-1962-pictorial-dictionaries.md",
      "guidance/liturgy/roman-1962-server-training.md",
      "guidance/liturgy/postconciliar-illustrated-dictionary-handoff.md",
    )
    for path in paths:
      with self.subTest(path=path):
        text = self.read(path)
        self.assertIn("terminal", text)
        self.assertIn("internal release state", text.lower())
        self.assertIn("safety", text.lower())


if __name__ == "__main__":
  unittest.main()
