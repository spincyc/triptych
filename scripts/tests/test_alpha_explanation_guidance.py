from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


class AlphaExplanationGuidanceTest(unittest.TestCase):
  def read(self, path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")

  def test_universal_policy_places_explanation_in_terminal_appendix(self):
    editorial = self.read("guidance/editorial.md")
    self.assertIn(
      "A work's alpha explanation—including what alpha means, present scope,",
      editorial,
    )
    self.assertIn(
      "The first page may carry a terse\nstatus-only footer such as `Alpha`",
      editorial,
    )
    self.assertIn(
      "Safety warnings and legally necessary notices remain immediately "
      "visible",
      editorial,
    )

  def test_repository_policy_does_not_require_first_page_exposition(self):
    repository = self.read("guidance/repository.md")
    self.assertIn(
      "explains its alpha\nstate, actual scope, completion limits, review "
      "state",
      repository,
    )
    self.assertIn(
      "first page may carry a terse status-only `Alpha` footer",
      repository,
    )
    self.assertNotIn(
      "states its actual present scope on the first page",
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
        self.assertIn("status-only", text)
        self.assertIn("`Alpha` footer", text)
        self.assertIn("safety", text.lower())


if __name__ == "__main__":
  unittest.main()
