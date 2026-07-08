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

    def test_order_tenancy_no_get_started_ok(self):
        # nyc-genai-lab tenancy pattern: Introduction -> Sign Up -> labs -> Need Help
        tm = {"tutorials": [
            {"title": "Introduction", "filename": "../../introduction/introduction.md"},
            {"title": "Sign Up for an APEX Workspace", "filename": "../../../common-261/1-sign-up-apex/1-sign-up-apex.md"},
            {"title": "Lab 1: Connect APEX to Generative AI", "filename": "../../1-connect-genai/1-connect-genai.md"},
            {"title": "Need Help?", "filename": "https://livelabs.oracle.com/cdn/common/labs/need-help/need-help-livelabs.md"},
        ]}
        self.assertEqual(vw.check_manifest_order(tm, "tenancy"), [])

    def test_order_tenancy_missing_signup_reported(self):
        tm = {"tutorials": [
            {"title": "Introduction", "filename": "x"},
            {"title": "Lab 1: A", "filename": "y"},
            {"title": "Need Help?", "filename": "z"},
        ]}
        errs = vw.check_manifest_order(tm, "tenancy")
        self.assertTrue(any("Sign" in e for e in errs))


class TestPaths(unittest.TestCase):
    def test_missing_local_file_reported(self):
        with tempfile.TemporaryDirectory() as t:
            d = make_variant(t, GOOD)
            errs = vw.check_paths_resolve(GOOD, d, online=False)
            self.assertTrue(any("introduction.md" in e for e in errs))

    def test_existing_local_file_ok(self):
        # layout mirrors the real repo: <repo>/<workshop>/workshops/sandbox
        # so ../../../common-261/... resolves to <repo>/common-261/...
        with tempfile.TemporaryDirectory() as t:
            wk = Path(t) / "repo" / "wkshp"
            d = make_variant(wk, GOOD)
            for rel in ("introduction/introduction.md", "1-connect-genai/1-connect-genai.md"):
                f = wk / rel
                f.parent.mkdir(parents=True, exist_ok=True)
                f.write_text("# x")
            c = Path(t) / "repo" / "common-261/1-sign-up-apex/sign-up-apex-sandbox.md"
            c.parent.mkdir(parents=True, exist_ok=True)
            c.write_text("# x")
            self.assertEqual(vw.check_paths_resolve(GOOD, d, online=False), [])

    def test_bad_url_scheme_reported(self):
        bad = dict(GOOD)
        bad["tutorials"] = [dict(GOOD["tutorials"][0], filename="http://insecure")]
        with tempfile.TemporaryDirectory() as t:
            d = make_variant(t, bad)
            errs = vw.check_paths_resolve(bad, d, online=False)
            self.assertTrue(any("https" in e for e in errs))


LAB_OK = '''# Lab 1: Connect APEX to Generative AI
## Introduction
Estimated Time: 10 minutes
### Objectives
* Do a thing
## Task 1: Go
1. Click.
    ```sql
    <copy>select 1 from dual;</copy>
    ```
2. See ![The APEX builder](images/builder.png " ").
## Acknowledgements
* **Author** - Rick Houlihan
'''


class TestLabStructure(unittest.TestCase):
    def _write(self, t, body):
        lab = Path(t) / "1-connect-genai"
        (lab / "images").mkdir(parents=True)
        (lab / "images/builder.png").write_bytes(b"\x89PNG")
        p = lab / "1-connect-genai.md"
        p.write_text(body)
        return p

    def test_good_lab_passes(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(vw.check_lab_structure(self._write(t, LAB_OK)), [])

    def test_copy_tag_required(self):
        with tempfile.TemporaryDirectory() as t:
            p = self._write(t, LAB_OK.replace("<copy>", "").replace("</copy>", ""))
            self.assertTrue(any("<copy>" in e for e in vw.check_lab_structure(p)))

    def test_missing_sections_reported(self):
        with tempfile.TemporaryDirectory() as t:
            p = self._write(t, "# T\nhello\n")
            errs = vw.check_lab_structure(p)
            for needle in ("Estimated Time", "Objectives", "Acknowledgements"):
                self.assertTrue(any(needle in e for e in errs), needle)

    def test_empty_alt_text_reported(self):
        with tempfile.TemporaryDirectory() as t:
            p = self._write(t, LAB_OK.replace("![The APEX builder]", "![]"))
            self.assertTrue(any("alt text" in e for e in vw.check_lab_structure(p)))

    def test_missing_image_file_reported(self):
        with tempfile.TemporaryDirectory() as t:
            p = self._write(t, LAB_OK.replace("builder.png", "gone.png"))
            self.assertTrue(any("gone.png" in e for e in vw.check_lab_structure(p)))

    def test_introduction_requires_workshop_time(self):
        # official LiveLabs gate: introduction.md must say 'Estimated Workshop Time:'
        intro = LAB_OK.replace("# Lab 1: Connect APEX to Generative AI", "# Introduction")
        with tempfile.TemporaryDirectory() as t:
            lab = Path(t) / "introduction"
            (lab / "images").mkdir(parents=True)
            (lab / "images/builder.png").write_bytes(b"\x89PNG")
            p = lab / "introduction.md"
            p.write_text(intro)
            errs = vw.check_lab_structure(p)
            self.assertTrue(any("Estimated Workshop Time" in e for e in errs))
            p.write_text(intro.replace("Estimated Time: 10 minutes", "Estimated Workshop Time: 90 minutes"))
            self.assertEqual(vw.check_lab_structure(p), [])


def budget_fixture(t, l1_minutes):
    m = {"tutorials": [
        {"title": "Introduction", "filename": "../../intro/intro.md"},
        {"title": "Lab 1: A", "filename": "../../l1/l1.md"},
        {"title": "Lab 6 [OPTIONAL]: B", "filename": "../../l6/l6.md"},
    ]}
    for name, mins in (("intro", 0), ("l1", l1_minutes), ("l6", 60)):
        p = Path(t) / name
        p.mkdir()
        (p / f"{name}.md").write_text(f"# L\nEstimated Time: {mins} minutes\n")
    vd = Path(t) / "workshops" / "sandbox"
    vd.mkdir(parents=True)
    return m, vd


CFG = {"include_times": {"Introduction": 0}, "core_budget": 90, "warn_budget": 180}


class TestBudgetAndBans(unittest.TestCase):
    def test_core_budget_excludes_optional(self):
        with tempfile.TemporaryDirectory() as t:
            m, vd = budget_fixture(t, 85)
            errs = vw.check_time_budget(m, "sandbox", vd, CFG)
            self.assertEqual(errs, [])  # core 85 <= 90; total 145 <= 180

    def test_core_budget_hard_fail(self):
        with tempfile.TemporaryDirectory() as t:
            m, vd = budget_fixture(t, 95)
            errs = vw.check_time_budget(m, "sandbox", vd, CFG)
            self.assertTrue(any("hard" in e for e in errs))

    def test_warn_budget_fail(self):
        with tempfile.TemporaryDirectory() as t:
            m, vd = budget_fixture(t, 85)
            cfg = dict(CFG, warn_budget=100)
            errs = vw.check_time_budget(m, "sandbox", vd, cfg)
            self.assertTrue(any("warn" in e for e in errs))

    def test_banned_string_found(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "x.md"
            p.write_text("uses cohere.command-r-16k model")
            errs = vw.check_banned_strings(p, {"banned_strings": ["cohere.command-r-16k"]})
            self.assertTrue(errs)

    def test_ocid_in_copy_block_allowed(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "x.md"
            p.write_text('```\n<copy>ocid1.<your-compartment-ocid></copy>\n```')
            self.assertEqual(vw.check_banned_strings(p, {"banned_strings": ["ocid1."]}), [])

    def test_ocid_outside_copy_block_banned(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "x.md"
            p.write_text("my compartment is ocid1.compartment.oc1..aaa")
            self.assertTrue(vw.check_banned_strings(p, {"banned_strings": ["ocid1."]}))


if __name__ == "__main__":
    unittest.main()
