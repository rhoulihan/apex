"""Guards the model-compatibility finding from 2026-08-30.

APEX 26.1.4 emits tool definitions containing a `$schema` key. Labs 4 and 5 are
driven by tool calling, and most OCI GenAI models cannot handle it:

    cohere.command-a-03-2025  (APEX's pre-filled default)  -> INVALID_TOOL_GENERATION
    google.gemini-2.5-pro                                  -> rejects "$schema"
    xai.grok-4.3                                           -> works

`Test Connection` passes for all three, so nothing catches this before Lab 4
fails. These tests keep the warning in the labs.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "ai-helpdesk-agent"
LAB1 = ROOT / "1-connect-genai" / "1-connect-genai.md"
LAB4 = ROOT / "4-ai-interactive-report" / "4-ai-interactive-report.md"
LAB5 = ROOT / "5-ai-agent" / "5-ai-agent.md"

GOOD_MODEL = "xai.grok-4.3"
BAD_DEFAULT = "cohere.command-a-03-2025"


def read(p):
    return p.read_text(encoding="utf-8")


class TestLab1ModelGuidance(unittest.TestCase):
    def setUp(self):
        self.txt = read(LAB1)

    def test_names_a_known_good_model(self):
        self.assertIn(GOOD_MODEL, self.txt,
                      "Lab 1 must name a verified tool-calling model, not leave the choice open")

    def test_warns_about_the_prefilled_default(self):
        self.assertIn(BAD_DEFAULT, self.txt,
                      "Lab 1 must warn that APEX's pre-filled model breaks Labs 4 and 5")

    def test_does_not_tell_reader_to_freely_pick_a_model(self):
        # The original wording sent readers to pick any model, which breaks Lab 4.
        self.assertNotRegex(
            self.txt,
            r"Model ID:\s*\*\*pick the latest available chat model from the list\*\*",
            "Lab 1 must not tell the reader to pick any model - most fail tool calling",
        )

    def test_states_test_connection_does_not_prove_tool_calling(self):
        self.assertRegex(
            self.txt,
            r"Test Connection.{0,120}(does NOT prove|never exercises)",
            "Lab 1 must state that a passing Test Connection does not prove Labs 4/5 work",
        )

    def test_troubleshooting_covers_the_tool_calling_errors(self):
        for token in ("INVALID_TOOL_GENERATION", "$schema"):
            self.assertIn(token, self.txt,
                          f"Lab 1 troubleshooting must mention {token}")


class TestDownstreamLabsDeclareTheDependency(unittest.TestCase):
    def test_lab4_prerequisite_names_the_model(self):
        self.assertIn(GOOD_MODEL, read(LAB4),
                      "Lab 4 must state the tool-calling model requirement")

    def test_lab4_troubleshoots_tool_calling_failure(self):
        self.assertIn("INVALID_TOOL_GENERATION", read(LAB4),
                      "Lab 4 must tell the reader a tool-calling error means the wrong Model ID")

    def test_lab5_prerequisite_names_the_model(self):
        self.assertIn(GOOD_MODEL, read(LAB5),
                      "Lab 5 (AI Agents) is tool calling by definition and must state the requirement")


if __name__ == "__main__":
    unittest.main()
