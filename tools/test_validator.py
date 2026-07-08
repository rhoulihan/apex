"""Unit tests for validate_workshop.py. Run: python3 test_validator.py -v"""
import json
import tempfile
import unittest
from pathlib import Path

import validate_workshop as vw


def make_variant(tmp, manifest, variant="sandbox"):
    d = Path(tmp) / "workshops" / variant
    d.mkdir(parents=True)
    (d / "manifest.json").write_text(json.dumps(manifest))
    return d


GOOD = {
    "workshoptitle": "Build an AI-Powered Help Desk with Oracle APEX: From Prompt to Agent",
    "help": "livelabs-help-apex_us@oracle.com",
    "tutorials": [
        {"title": "Introduction", "filename": "../../introduction/introduction.md"},
        {"title": "Get Started", "filename": "https://livelabs.oracle.com/cdn/common/labs/cloud-login/cloud-login-livelabs2.md"},
        {"title": "Sign up for an APEX Workspace", "filename": "../../../common-261/1-sign-up-apex/sign-up-apex-sandbox.md"},
        {"title": "Lab 1: Connect APEX to Generative AI", "filename": "../../1-connect-genai/1-connect-genai.md"},
        {"title": "Need Help?", "filename": "https://livelabs.oracle.com/cdn/common/labs/need-help/need-help-livelabs.md"},
    ],
}


class TestManifest(unittest.TestCase):
    def test_load_manifest_ok(self):
        with tempfile.TemporaryDirectory() as t:
            d = make_variant(t, GOOD)
            m = vw.load_manifest(d)
            self.assertEqual(m["help"], "livelabs-help-apex_us@oracle.com")

    def test_load_manifest_bad_json_raises(self):
        with tempfile.TemporaryDirectory() as t:
            d = Path(t) / "workshops" / "sandbox"
            d.mkdir(parents=True)
            (d / "manifest.json").write_text("{nope")
            with self.assertRaises(vw.ValidationError):
                vw.load_manifest(d)

    def test_order_ok(self):
        self.assertEqual(vw.check_manifest_order(GOOD, "sandbox"), [])

    def test_order_intro_not_first(self):
        bad = dict(GOOD, tutorials=[GOOD["tutorials"][1], GOOD["tutorials"][0]] + GOOD["tutorials"][2:])
        errs = vw.check_manifest_order(bad, "sandbox")
        self.assertTrue(any("Introduction" in e for e in errs))

    def test_order_need_help_not_last(self):
        bad = dict(GOOD, tutorials=GOOD["tutorials"][:-1][::-1] + [GOOD["tutorials"][0]])
        errs = vw.check_manifest_order(bad, "sandbox")
        self.assertTrue(any("Need Help" in e for e in errs))


if __name__ == "__main__":
    unittest.main()
