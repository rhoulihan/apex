# AI Help Desk Workshop Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (Rick directed: all development inline, strict TDD) to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the "Build an AI-Powered Help Desk with Oracle APEX: From Prompt to Agent" LiveLabs workshop (spec: `docs/specs/2026-07-07-apex-ai-workshop-spec.md`), validator-first.

**Architecture:** A stdlib-only Python validator (`tools/`) is built and self-tested BEFORE any content; every lab goes red (manifest entry + missing file) → green (authored content passes all checks). Workshop content lives in `ai-helpdesk-agent/` following the nyc-genai-lab/sample-workshop conventions, with three manifest variants (sandbox/tenancy/event) over single-source labs.

**Tech Stack:** Python 3 stdlib (validator + unittest), LiveLabs markdown conventions, Oracle SQL/PL-SQL (26ai), APEX 26.1 builder features.

## Global Constraints (from spec — verbatim where exact)

- Repo: work on branch `apex-ai-workshop-spec` of `/mnt/c/Users/rickh/GitHub/apex`. Final upstream PR contains ONLY `ai-helpdesk-agent/` (Task 20).
- Workshop folder: `ai-helpdesk-agent/`; app name "Horizon Help Desk"; help email `livelabs-help-apex_us@oracle.com`.
- Manifest order (validator-enforced): Introduction #1, Get Started #2, sign-up #3, "Need Help?" last.
- Sign-up include: `../../../common-261/1-sign-up-apex/sign-up-apex-sandbox.md` (`common-latest` has NO sandbox flavor — do not "upgrade" the path without checking the file exists).
- Time budget: non-OPTIONAL manifest entries ≤ 90 min/variant (hard), all entries ≤ 180 (warning). Include overrides: Get Started=5, Sign up=10 (config, not headers).
- Lab skeleton: `# Title → ## Introduction → Estimated Time → ### Objectives → ### Prerequisites → ## Task 1..N → ## Learn More → ## Acknowledgements`; `<copy>` on every fenced code block; alt text on every image; lowercase filenames.
- Banned strings in lab content: `cohere.command-r-16k`, `command-r-plus`, `ocid1.` (hardcoded OCIDs), `23ai`, `Guardrail` (UI label — real label is "User Approval" / "Requires Confirmation"), `TODO`, `TBD`.
- UI terminology: "User Approval → Requires Confirmation" (never "Guardrail" as a UI term); AI Agent / AI Tools (26.1 names).
- Region string in labs: `us-chicago-1`; model instruction is "pick the latest available chat model" — never a hardcoded model ID.
- Governance beats & data-egress callouts per lab as specified in spec §4 (each lab task below lists its own).
- Fixed seed facts every lab may rely on: ticket **42** = open VPN ticket; KB article **"VPN error 812"**; exactly 3 tables `TICKETS`, `KB_ARTICLES`, `TEAM_MEMBERS`.
- `<copy>` blocks use literal angle-bracket placeholders only for attendee-substituted values (e.g. `<your-compartment-ocid>`); these are exempt from the `ocid1.` ban.
- External gates (not repo tasks, tracked in `tasks/todo.md`): WMS submission/approval before content PR; week-1 sandbox GenAI verification; screenshots + Self QA need a real LiveLabs reservation.

---

### Task 1: Validator core — manifest loading + ordering check

**Files:**
- Create: `tools/validate_workshop.py`
- Create: `tools/test_validator.py`
- Create: `tools/validator_config.json`

**Interfaces:**
- Produces: `load_manifest(variant_dir: Path) -> dict` (raises `ValidationError` on parse failure); `check_manifest_order(manifest: dict, variant: str) -> list[str]` (returns error strings, empty = pass); `ValidationError(Exception)`. Config JSON schema: `{"include_times": {"<title substring>": minutes}, "core_budget": 90, "warn_budget": 180, "banned_strings": [...], "workshop_dir": "ai-helpdesk-agent"}`.

- [ ] **Step 1: Write the failing tests**

```python
# tools/test_validator.py
import json, tempfile, unittest
from pathlib import Path
import validate_workshop as vw

def make_variant(tmp, manifest):
    d = Path(tmp) / "workshops" / "sandbox"
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
            d = Path(t) / "workshops" / "sandbox"; d.mkdir(parents=True)
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
```

- [ ] **Step 2: Run tests, verify they fail**

Run: `cd /mnt/c/Users/rickh/GitHub/apex/tools && python3 test_validator.py -v`
Expected: `ModuleNotFoundError: No module named 'validate_workshop'` (or AttributeError once the file exists empty).

- [ ] **Step 3: Implement minimal validator core**

```python
# tools/validate_workshop.py
"""LiveLabs workshop validator for ai-helpdesk-agent. Stdlib only."""
import json, re, sys
from pathlib import Path

class ValidationError(Exception):
    pass

def load_manifest(variant_dir):
    p = Path(variant_dir) / "manifest.json"
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise ValidationError(f"{p}: cannot load manifest: {e}")

def check_manifest_order(manifest, variant):
    errs = []
    titles = [t.get("title", "") for t in manifest.get("tutorials", [])]
    if not titles:
        return [f"{variant}: manifest has no tutorials"]
    if not titles[0].startswith("Introduction"):
        errs.append(f"{variant}: Introduction must be first, got '{titles[0]}'")
    if len(titles) > 1 and not titles[1].startswith("Get Started"):
        errs.append(f"{variant}: Get Started must be second, got '{titles[1]}'")
    if variant == "sandbox" and len(titles) > 2 and "Sign up" not in titles[2]:
        errs.append(f"{variant}: sign-up lab must be third, got '{titles[2]}'")
    if not titles[-1].startswith("Need Help"):
        errs.append(f"{variant}: 'Need Help?' must be last, got '{titles[-1]}'")
    return errs
```

- [ ] **Step 4: Run tests, verify pass**

Run: `cd /mnt/c/Users/rickh/GitHub/apex/tools && python3 test_validator.py -v`
Expected: `OK` (5 tests).

- [ ] **Step 5: Seed the config file**

```json
{
  "workshop_dir": "ai-helpdesk-agent",
  "variants": ["sandbox", "tenancy", "event"],
  "core_budget": 90,
  "warn_budget": 180,
  "include_times": {
    "Get Started": 5,
    "Sign up for an APEX Workspace": 10,
    "Need Help?": 0,
    "Introduction": 0
  },
  "banned_strings": ["cohere.command-r-16k", "command-r-plus", "ocid1.", "23ai", "Guardrail", "TODO", "TBD"]
}
```

- [ ] **Step 6: Commit**

```bash
git -C /mnt/c/Users/rickh/GitHub/apex add tools/ && git -C /mnt/c/Users/rickh/GitHub/apex commit -m "tools: validator core - manifest load + ordering (TDD)"
```

---

### Task 2: Validator — path resolution across variants

**Files:**
- Modify: `tools/validate_workshop.py`
- Modify: `tools/test_validator.py`

**Interfaces:**
- Produces: `check_paths_resolve(manifest: dict, variant_dir: Path, online: bool = False) -> list[str]`. Relative `filename`s resolve against `variant_dir`; `https://` URLs are syntax-checked offline, HEAD-checked (urllib, 10 s timeout) when `online=True`.

- [ ] **Step 1: Write failing tests** — add to `tools/test_validator.py`:

```python
class TestPaths(unittest.TestCase):
    def test_missing_local_file_reported(self):
        with tempfile.TemporaryDirectory() as t:
            d = make_variant(t, GOOD)
            errs = vw.check_paths_resolve(GOOD, d, online=False)
            self.assertTrue(any("introduction.md" in e for e in errs))

    def test_existing_local_file_ok(self):
        with tempfile.TemporaryDirectory() as t:
            d = make_variant(t, GOOD)
            for rel in ("introduction/introduction.md", "1-connect-genai/1-connect-genai.md"):
                f = Path(t) / rel; f.parent.mkdir(parents=True, exist_ok=True); f.write_text("# x")
            c = Path(t).parent / "common-261/1-sign-up-apex/sign-up-apex-sandbox.md"
            c.parent.mkdir(parents=True, exist_ok=True); c.write_text("# x")
            self.assertEqual(vw.check_paths_resolve(GOOD, d, online=False), [])

    def test_bad_url_scheme_reported(self):
        bad = dict(GOOD); bad["tutorials"] = [dict(GOOD["tutorials"][0], filename="http://insecure")]
        with tempfile.TemporaryDirectory() as t:
            d = make_variant(t, bad)
            errs = vw.check_paths_resolve(bad, d, online=False)
            self.assertTrue(any("https" in e for e in errs))
```

- [ ] **Step 2: Run, verify the 3 new tests fail** (`AttributeError: check_paths_resolve`).

- [ ] **Step 3: Implement**

```python
def check_paths_resolve(manifest, variant_dir, online=False):
    errs, variant_dir = [], Path(variant_dir)
    for t in manifest.get("tutorials", []):
        fn = t.get("filename", "")
        if fn.startswith("https://"):
            if online:
                import urllib.request
                try:
                    req = urllib.request.Request(fn, method="HEAD")
                    urllib.request.urlopen(req, timeout=10)
                except Exception as e:
                    errs.append(f"{t.get('title')}: URL unreachable: {fn} ({e})")
        elif fn.startswith("http://"):
            errs.append(f"{t.get('title')}: must use https, got {fn}")
        else:
            if not (variant_dir / fn).resolve().exists():
                errs.append(f"{t.get('title')}: file not found: {fn}")
    return errs
```

- [ ] **Step 4: Run all tests, verify pass** (`OK`, 8 tests).

- [ ] **Step 5: Commit** — `git ... commit -m "tools: validator path resolution per variant"`

---

### Task 3: Validator — lab structural rules

**Files:**
- Modify: `tools/validate_workshop.py`
- Modify: `tools/test_validator.py`

**Interfaces:**
- Produces: `check_lab_structure(md_path: Path) -> list[str]` enforcing: exactly one H1; `Estimated Time` line; `### Objectives`; `## Acknowledgements`; every fenced code block contains `<copy>`; every image `![alt](path)` has non-empty alt AND the file exists relative to the lab folder (placeholder images allowed — flagged only by `--final`, Task 4).

- [ ] **Step 1: Write failing tests** — add:

```python
LAB_OK = """# Lab 1: Connect APEX to Generative AI
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
"""

class TestLabStructure(unittest.TestCase):
    def _write(self, t, body):
        lab = Path(t) / "1-connect-genai"; (lab / "images").mkdir(parents=True)
        (lab / "images/builder.png").write_bytes(b"\\x89PNG")
        p = lab / "1-connect-genai.md"; p.write_text(body); return p

    def test_good_lab_passes(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(vw.check_lab_structure(self._write(t, LAB_OK)), [])

    def test_copy_tag_required(self):
        with tempfile.TemporaryDirectory() as t:
            p = self._write(t, LAB_OK.replace("<copy>", "").replace("</copy>", ""))
            self.assertTrue(any("<copy>" in e for e in vw.check_lab_structure(p)))

    def test_missing_sections_reported(self):
        with tempfile.TemporaryDirectory() as t:
            p = self._write(t, "# T\\nhello\\n")
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
```

- [ ] **Step 2: Run, verify 5 new tests fail.**

- [ ] **Step 3: Implement**

```python
IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^) ]+)( \"[^\"]*\")?\)")
FENCE_RE = re.compile(r"```[a-z]*\n(.*?)```", re.S)

def check_lab_structure(md_path):
    md_path = Path(md_path)
    errs, text = [], md_path.read_text(encoding="utf-8")
    h1 = [l for l in text.splitlines() if l.startswith("# ")]
    if len(h1) != 1:
        errs.append(f"{md_path.name}: expected exactly one H1, found {len(h1)}")
    if "Estimated Time" not in text and "Estimated Lab Time" not in text:
        errs.append(f"{md_path.name}: missing 'Estimated Time' line")
    if "### Objectives" not in text:
        errs.append(f"{md_path.name}: missing '### Objectives'")
    if "## Acknowledgements" not in text:
        errs.append(f"{md_path.name}: missing '## Acknowledgements'")
    for block in FENCE_RE.findall(text):
        if "<copy>" not in block:
            errs.append(f"{md_path.name}: fenced code block without <copy>: {block.strip()[:40]!r}")
    for alt, src, _ in IMG_RE.findall(text):
        if not alt.strip():
            errs.append(f"{md_path.name}: image {src} missing alt text")
        if not src.startswith("http") and not (md_path.parent / src).exists():
            errs.append(f"{md_path.name}: image file not found: {src}")
    return errs
```

- [ ] **Step 4: Run all tests → OK (13). Step 5: Commit** `"tools: validator lab structural rules"`

---

### Task 4: Validator — time budget, banned strings, CLI, placeholder-image final gate

**Files:**
- Modify: `tools/validate_workshop.py`
- Modify: `tools/test_validator.py`

**Interfaces:**
- Produces: `check_time_budget(manifest, variant, labs_root: Path, config) -> list[str]` (time source: config `include_times` by title-substring match first, else the lab's `Estimated Time: N minutes` header; titles containing `OPTIONAL` excluded from ≤`core_budget` hard check, included in ≤`warn_budget` warning); `check_banned_strings(md_path, config) -> list[str]` (skips content inside `<copy>` blocks for the `ocid1.` pattern only); CLI `python3 tools/validate_workshop.py [--online] [--final]` — iterates config variants (missing variant dir = error), aggregates all checks over every local lab in each manifest, prints errors, exit 1 on any. `--final` additionally fails on images whose bytes match the Task 6 placeholder marker (`b"PLACEHOLDER-SCREENSHOT"` embedded in the PNG) and on warning-level budget breaches.

- [ ] **Step 1: Write failing tests** — add (abridged to the behaviors that matter):

```python
class TestBudgetAndBans(unittest.TestCase):
    def test_core_budget_excludes_optional(self):
        m = {"tutorials": [
            {"title": "Introduction", "filename": "x"},
            {"title": "Lab 1: A", "filename": "l1"}, {"title": "Lab 6 OPTIONAL: B", "filename": "l6"},
        ]}
        cfg = {"include_times": {"Introduction": 0}, "core_budget": 90, "warn_budget": 180}
        with tempfile.TemporaryDirectory() as t:
            for name, mins in (("l1", 85), ("l6", 60)):
                p = Path(t) / name; p.mkdir(); (p / f"{name}.md").write_text(f"# L\\nEstimated Time: {mins} minutes\\n")
            m["tutorials"][1]["filename"] = f"../../l1/l1.md"; m["tutorials"][2]["filename"] = f"../../l6/l6.md"
            vd = Path(t) / "workshops/sandbox"; vd.mkdir(parents=True)
            errs = vw.check_time_budget(m, "sandbox", vd, cfg)
            self.assertEqual([e for e in errs if "hard" in e], [])          # 85 <= 90
            self.assertTrue(any("warn" in e for e in errs) is False)        # 145 <= 180

    def test_core_budget_hard_fail(self):
        # same shape with l1=95 → hard error
        ...

    def test_banned_string_found(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "x.md"; p.write_text("uses cohere.command-r-16k model")
            errs = vw.check_banned_strings(p, {"banned_strings": ["cohere.command-r-16k"]})
            self.assertTrue(errs)

    def test_ocid_in_copy_block_allowed(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "x.md"; p.write_text('```\\n<copy>ocid1.<your-compartment-ocid></copy>\\n```')
            self.assertEqual(vw.check_banned_strings(p, {"banned_strings": ["ocid1."]}), [])
```

(Write `test_core_budget_hard_fail` fully in the file — same fixture with `l1`=95 and assert one error containing `"hard"`.)

- [ ] **Step 2: Run, verify new tests fail.**

- [ ] **Step 3: Implement** `check_time_budget`, `check_banned_strings`, `main()`:

```python
TIME_RE = re.compile(r"Estimated (?:Lab )?Time:\s*(\d+)\s*min", re.I)

def lab_minutes(entry, variant_dir, config):
    for key, mins in config.get("include_times", {}).items():
        if key in entry.get("title", ""):
            return mins
    fn = entry.get("filename", "")
    if fn.startswith("http"):
        return 0
    m = TIME_RE.search((Path(variant_dir) / fn).resolve().read_text(encoding="utf-8"))
    return int(m.group(1)) if m else 0

def check_time_budget(manifest, variant, variant_dir, config):
    errs, core, total = [], 0, 0
    for t in manifest.get("tutorials", []):
        try:
            mins = lab_minutes(t, variant_dir, config)
        except OSError:
            continue  # missing files reported by check_paths_resolve
        total += mins
        if "OPTIONAL" not in t.get("title", "").upper():
            core += mins
    if core > config["core_budget"]:
        errs.append(f"{variant}: hard budget exceeded: core {core} > {config['core_budget']} min")
    if total > config["warn_budget"]:
        errs.append(f"{variant}: warn budget exceeded: total {total} > {config['warn_budget']} min")
    return errs

COPY_RE = re.compile(r"<copy>.*?</copy>", re.S)

def check_banned_strings(md_path, config):
    text = Path(md_path).read_text(encoding="utf-8")
    errs = []
    for s in config.get("banned_strings", []):
        hay = COPY_RE.sub("", text) if s == "ocid1." else text
        if s in hay:
            errs.append(f"{Path(md_path).name}: banned string present: {s!r}")
    return errs

def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--online", action="store_true")
    ap.add_argument("--final", action="store_true")
    args = ap.parse_args(argv)
    root = Path(__file__).resolve().parent.parent
    config = json.loads((Path(__file__).parent / "validator_config.json").read_text())
    wdir = root / config["workshop_dir"]
    errs = []
    for variant in config["variants"]:
        vd = wdir / "workshops" / variant
        if not vd.exists():
            errs.append(f"variant missing: workshops/{variant}")
            continue
        try:
            m = load_manifest(vd)
        except ValidationError as e:
            errs.append(str(e)); continue
        errs += check_manifest_order(m, variant)
        errs += check_paths_resolve(m, vd, online=args.online)
        errs += check_time_budget(m, variant, vd, config)
        for t in m.get("tutorials", []):
            fn = t.get("filename", "")
            if not fn.startswith("http") and fn.startswith("../../") and not fn.startswith("../../../"):
                p = (vd / fn).resolve()
                if p.exists():
                    errs += check_lab_structure(p)
                    errs += check_banned_strings(p, config)
                    if args.final:
                        for img in (p.parent / "images").glob("*.png") if (p.parent / "images").exists() else []:
                            if b"PLACEHOLDER-SCREENSHOT" in img.read_bytes():
                                errs.append(f"--final: placeholder screenshot remains: {img}")
    for e in errs:
        print("FAIL:", e)
    print(f"{len(errs)} error(s)")
    return 1 if errs else 0

if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run all tests → OK. Step 5:** Run `python3 tools/validate_workshop.py`; Expected: `FAIL: variant missing: workshops/sandbox` ×3, exit 1 — **this is the red state the whole workshop now drives to green.**

- [ ] **Step 6: Commit** `"tools: validator budget/bans/CLI - workshop now red"`

---

### Task 5: Workshop scaffolding — manifests, index.html, placeholder images

**Files:**
- Create: `ai-helpdesk-agent/workshops/{sandbox,tenancy,event}/manifest.json` and `index.html`
- Create: `tools/make_placeholder.py`

**Interfaces:**
- Consumes: validator CLI (Task 4). Produces: the three manifests every later task adds no entries to (entries are complete NOW; only lab files are missing → red), and `python3 tools/make_placeholder.py <lab>/images/<name>.png "caption"` which writes a 400×250 gray PNG containing the marker bytes `PLACEHOLDER-SCREENSHOT`.

- [ ] **Step 1: Copy `index.html` verbatim from the exemplar** (it is a framework stub): `cp nyc-genai-lab/workshops/sandbox/index.html ai-helpdesk-agent/workshops/sandbox/index.html` (repeat for tenancy, event).

- [ ] **Step 2: Author the sandbox manifest** — `ai-helpdesk-agent/workshops/sandbox/manifest.json`:

```json
{
  "workshoptitle": "Build an AI-Powered Help Desk with Oracle APEX: From Prompt to Agent",
  "help": "livelabs-help-apex_us@oracle.com",
  "tutorials": [
    { "title": "Introduction", "description": "What you will build and why: prompt to app to trustworthy app", "filename": "../../introduction/introduction.md" },
    { "title": "Get Started", "description": "Log in to your LiveLabs Sandbox environment", "filename": "https://livelabs.oracle.com/cdn/common/labs/cloud-login/cloud-login-livelabs2.md" },
    { "title": "Sign up for an APEX Workspace", "description": "Create an Always Free Autonomous Database and an APEX workspace", "filename": "../../../common-261/1-sign-up-apex/sign-up-apex-sandbox.md" },
    { "title": "Lab 1: Connect APEX to Generative AI", "description": "Configure a Generative AI service, set token quotas, and test the APEX Assistant", "filename": "../../1-connect-genai/1-connect-genai.md", "type": { "OCIGenAI": "OCIGenAI", "OpenAI": "OpenAI" } },
    { "title": "Lab 2: Design the Data Model with AI", "description": "Generate a data model with AI, review it, and run the vetted script", "filename": "../../2-data-model-ai/2-data-model-ai.md" },
    { "title": "Lab 3: Generate the App from a Prompt", "description": "Create the Horizon Help Desk app with AI and take the tour", "filename": "../../3-generate-app/3-generate-app.md" },
    { "title": "Lab 4: Ask Your Data Anything with AI Interactive Reports", "description": "Natural-language filters, charts, and governance", "filename": "../../4-ai-interactive-report/4-ai-interactive-report.md" },
    { "title": "Lab 5: Build the Help Desk AI Agent", "description": "AI Agent with Retrieve Data tools and an approved write action", "filename": "../../5-ai-agent/5-ai-agent.md" },
    { "title": "Lab 6 [OPTIONAL]: Draft Replies with AI", "description": "Generate Text with AI on the ticket form", "filename": "../../6-generate-text/6-generate-text.md" },
    { "title": "Lab 7 [OPTIONAL]: Semantic Knowledge-Base Search with AI Vector Search", "description": "Vector Provider, embeddings, and a semantic search page", "filename": "../../7-vector-search/7-vector-search.md" },
    { "title": "Take It Home", "description": "Export your app, keep the scripts, and find your next workshop", "filename": "../../8-take-it-home/8-take-it-home.md" },
    { "title": "Need Help?", "description": "Solutions to Common Problems and Directions for Receiving Live Help", "filename": "https://livelabs.oracle.com/cdn/common/labs/need-help/need-help-livelabs.md" }
  ]
}
```

- [ ] **Step 3: Author tenancy + event manifests.** Tenancy = same tutorials with: Get Started → `https://livelabs.oracle.com/cdn/common/labs/cloud-login/pre-register-free-tier-account.md`; sign-up entry title "Provision an Autonomous Database and APEX Workspace" → `../../../common-261/1-sign-up-apex/1-sign-up-apex.md`; Need Help? → `.../need-help/need-help-freetier.md`. Event = copy of tenancy (event re-cuts adjust per event later). **Verify both include paths exist on disk first** (`ls ../common-261/1-sign-up-apex/`); if `1-sign-up-apex.md` is absent, use the exact tenancy include used by `nyc-genai-lab/workshops/tenancy/manifest.json` (open it and copy verbatim).

- [ ] **Step 4: Write `tools/make_placeholder.py`**

```python
"""Write a gray placeholder PNG (with marker bytes) + caption text file."""
import struct, sys, zlib
from pathlib import Path

def png(w=400, h=250, rgb=(220, 222, 226)):
    def chunk(typ, data):
        c = typ + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c))
    raw = b"".join(b"\x00" + bytes(rgb) * w for _ in range(h))
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + chunk(b"tEXt", b"Comment\x00PLACEHOLDER-SCREENSHOT")
            + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))

if __name__ == "__main__":
    out, caption = Path(sys.argv[1]), sys.argv[2]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(png())
    out.with_suffix(".caption.txt").write_text(caption + "\n")
    print("placeholder:", out)
```

- [ ] **Step 5: Run validator** — Expected now: no "variant missing"; instead `file not found` for all 9 local labs, exit 1. Run `python3 tools/test_validator.py` → still OK.

- [ ] **Step 6: Commit** `"workshop: scaffold manifests + index stubs (all labs red)"`

---

### Task 6: SQL artifacts — schema, seed, resolve-ticket

**Files:**
- Create: `ai-helpdesk-agent/2-data-model-ai/files/helpdesk-schema.sql`
- Create: `ai-helpdesk-agent/5-ai-agent/files/resolve-ticket.sql`
- Create: `tools/test_sql_contract.py`

**Interfaces:**
- Produces: schema contract every lab relies on — tables `TICKETS(id, subject, description, status, priority, category, created_on, assigned_to)`, `KB_ARTICLES(id, title, content, category, updated_on)`, `TEAM_MEMBERS(id, name, role, email)`; ids `GENERATED BY DEFAULT ON NULL AS IDENTITY (START WITH 1000)`; seed = 50 tickets (fixed ids 1–50; **ticket 42: status 'Open', category 'Network', subject 'Cannot connect to VPN - error 812 when working from home'**), 20 KB articles (fixed ids 1–20; **article 7 title 'Fixing VPN Error 812: remote access policy mismatch'** with a concrete 3-step fix in content), 8 team members. Statuses: Open/In Progress/Resolved/Closed; priorities: Low/Medium/High/Critical; categories: Network/Hardware/Software/Access/Email.

- [ ] **Step 1: Write the contract test** (`tools/test_sql_contract.py`, pure text checks — DB execution is Step 4's manual gate):

```python
import re, unittest
from pathlib import Path
SQL = (Path(__file__).parent.parent / "ai-helpdesk-agent/2-data-model-ai/files/helpdesk-schema.sql").read_text()

class TestSchemaScript(unittest.TestCase):
    def test_drop_and_recreate_semantics(self):
        for t in ("TICKETS", "KB_ARTICLES", "TEAM_MEMBERS"):
            self.assertIn(f"drop table {t.lower()}", SQL.lower())
            self.assertIn(f"create table {t.lower()}", SQL.lower())

    def test_fixed_rows_present(self):
        self.assertRegex(SQL, r"insert into tickets[^;]*42[^;]*error 812", msg="ticket 42 VPN row")
        self.assertRegex(SQL, r"insert into kb_articles[^;]*VPN Error 812")

    def test_seed_counts(self):
        self.assertEqual(len(re.findall(r"insert into tickets", SQL, re.I)), 50)
        self.assertEqual(len(re.findall(r"insert into kb_articles", SQL, re.I)), 20)
        self.assertEqual(len(re.findall(r"insert into team_members", SQL, re.I)), 8)

    def test_identity_start_1000(self):
        self.assertIn("identity (start with 1000", SQL.lower())

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run → fails (file missing). Step 3: Author `helpdesk-schema.sql`.** Header comment states the contract ("state-reset checkpoint — drops and recreates; safe to re-run"). Shape:

```sql
-- Horizon Help Desk canonical schema + seed. State-reset checkpoint:
-- drops and recreates all three tables; safe to re-run at any point.
begin
  for t in (select table_name from user_tables
            where table_name in ('TICKETS','KB_ARTICLES','TEAM_MEMBERS')) loop
    execute immediate 'drop table ' || t.table_name || ' cascade constraints purge';
  end loop;
end;
/
create table team_members (
  id    number generated by default on null as identity (start with 1000) primary key,
  name  varchar2(100) not null,
  role  varchar2(50)  not null,
  email varchar2(255) not null
);
create table tickets (
  id          number generated by default on null as identity (start with 1000) primary key,
  subject     varchar2(200) not null,
  description varchar2(4000),
  status      varchar2(20) default 'Open' not null
              constraint tickets_status_ck check (status in ('Open','In Progress','Resolved','Closed')),
  priority    varchar2(10) default 'Medium' not null
              constraint tickets_priority_ck check (priority in ('Low','Medium','High','Critical')),
  category    varchar2(20) not null
              constraint tickets_category_ck check (category in ('Network','Hardware','Software','Access','Email')),
  created_on  date default sysdate not null,
  assigned_to number references team_members(id)
);
create table kb_articles (
  id         number generated by default on null as identity (start with 1000) primary key,
  title      varchar2(200) not null,
  content    varchar2(4000) not null,
  category   varchar2(20) not null,
  updated_on date default sysdate not null
);
-- seed: 8 team members (ids 1-8), 20 KB articles (ids 1-20), 50 tickets (ids 1-50)
insert into team_members (id, name, role, email) values (1, 'Ava Chen', 'Support Lead', 'ava.chen@example.com');
-- ... (7 more)
insert into kb_articles (id, title, content, category, updated_on) values (7,
 'Fixing VPN Error 812: remote access policy mismatch',
 'Error 812 means the RAS/VPN server rejected the connection because of an authentication policy mismatch. Fix: 1) Open the VPN client and select Settings > Security. 2) Change authentication from MS-CHAP v1 to MS-CHAP v2. 3) Reconnect. If the error persists, reset the user''s dial-in policy in the admin console.',
 'Network', date '2026-05-14');
-- ... (19 more articles: printer spooler, MFA reset, email quota, disk cleanup, wifi cert, ...)
insert into tickets (id, subject, description, status, priority, category, created_on, assigned_to) values (42,
 'Cannot connect to VPN - error 812 when working from home',
 'User reports VPN fails with error 812 every time they connect from their home network. Started after the password reset on Monday.',
 'Open', 'High', 'Network', date '2026-07-01', 3);
-- ... (49 more tickets across statuses/priorities/categories; ~40% Open/In Progress)
commit;
```

Author every INSERT explicitly (deterministic literals, varied realistic content; keep each description 1–3 sentences; 3–4 more tickets mention VPN so the agent's "open tickets about it" query returns a handful). Content rules: no real names/domains (`example.com`), no product names beyond generic ones.

- [ ] **Step 4: Text contract green** — `python3 tools/test_sql_contract.py -v` → OK.

- [ ] **Step 5: Author `resolve-ticket.sql`** (the Lab 5 tool body, also a copy block there):

```sql
-- AI Tool: Execute Server-side Code -- resolve_ticket
-- Bind :ticket_id is supplied by the agent from conversation context.
declare
  l_subject tickets.subject%type;
begin
  select subject into l_subject from tickets where id = :ticket_id;
  update tickets set status = 'Resolved' where id = :ticket_id;
  apex_ai.set_tool_result(
    p_result => 'Ticket ' || :ticket_id || ' ("' || l_subject || '") is now Resolved.');
exception
  when no_data_found then
    apex_ai.set_tool_result(p_result => 'No ticket with id ' || :ticket_id || ' exists.');
end;
```

(Exact bind/parameter mechanics verified against the builder in the DB gate below — the scm-ai-agent lab is the reference if the signature differs.)

- [ ] **Step 6 (manual DB gate — record results in `tasks/todo.md`):** on Rick's 26ai ADB via SQL Workshop: (a) run `helpdesk-schema.sql` twice → second run succeeds, `select count(*) from tickets` = 50, ticket 42 Open; (b) divergent-precondition: create a dummy `tickets` table with 2 columns, run script → canonical schema wins; (c) run `resolve-ticket.sql` body with `:ticket_id := 42` (temporarily replacing `apex_ai.set_tool_result` with `dbms_output.put_line` — `apex_ai` needs an APEX session) → ticket 42 Resolved; re-run schema script to reset.

- [ ] **Step 7: Commit** `"workshop: canonical schema + seed + resolve-ticket tool (SQL contract tested)"`

---

### Task 7: Introduction lab

**Files:**
- Create: `ai-helpdesk-agent/introduction/introduction.md` + `images/` (3 placeholders)

**Interfaces:**
- Consumes: spec §4 "Introduction" contract (5 required elements). Produces: the workshop's framing language other labs echo ("Prompt → App → Trustworthy App", "AI as amplifier").

- [ ] **Step 1: Red** — `python3 tools/validate_workshop.py` currently lists `introduction.md: file not found`. Confirm.
- [ ] **Step 2: Author the lab.** Structure (all five spec elements, in this order):

```markdown
# Introduction

## About this Workshop
[Positioning paragraph from spec §1 verbatim-adapted + the three-act arc:
Act 1 AI builds it with you; Act 2 AI works inside it on your data;
Act 3 you are the reviewer — AI as amplifier, not replacement. One sentence:
"At every step you review and approve what AI produces."]

![The finished Horizon Help Desk dashboard](images/finished-dashboard.png " ")
![Chatting with the help desk AI agent](images/finished-agent-chat.png " ")
![Semantic knowledge-base search](images/finished-vector-search.png " ")

### What Data Leaves Your Database?
[4-sentence egress summary per spec: NL2IR = schema/report metadata only;
agent Retrieve Data tools + Generate Text = query results/ticket text as context;
vector search = KB article text to the embed model; nothing else.]

### Workshop Overview
| Lab | Title | Duration |
[table matching the sandbox manifest rows and §4 times]

Estimated Time: 90 minutes

### Objectives
[the 5 spec §3 objectives verbatim]

### Prerequisites
* A free Oracle.com account and a modern browser — no OCI tenancy, no local install
* Familiarity with SQL helpful but not required

## Learn More
* [Oracle APEX AI](https://www.oracle.com/apex/ai/)

## Acknowledgements
* **Author** - Rick Houlihan
* **Last Updated By/Date** - Rick Houlihan, July 2026
```

- [ ] **Step 3: Generate the 3 placeholder images** with `tools/make_placeholder.py` (captions describe the exact final screenshot to capture).
- [ ] **Step 4: Green check** — validator: introduction errors gone (8 labs still red). **Step 5: Commit** `"workshop: introduction lab"`

---

### Task 8: Lab 1 — Connect APEX to Generative AI

**Files:**
- Create: `ai-helpdesk-agent/1-connect-genai/1-connect-genai.md` + `images/` placeholders

**Interfaces:**
- Consumes: `common-261/2-configure-ai-keys/2-configure-ai-keys.md` (open it FIRST; mirror its step order and `if type="..."` conditional syntax exactly). Produces: a configured Generative AI service with Static ID `HELPDESK_AI` that Labs 2–7 name verbatim; the workshop's OpenAI/OCIGenAI `type` conditional pattern.

- [ ] **Step 1: Red confirmed.** **Step 2: Author.** Task list (10 min budget):
  - Task 1 (type=OCIGenAI): generate OCI API key pair; collect user OCID, tenancy OCID, **and assigned-compartment OCID** ("the compartment OCID is not in the API-key config file — copy it from your reservation's assigned-compartment details"); per-step placeholder screenshots.
  - Task 2 (type=OCIGenAI): Workspace Utilities → Generative AI Services → Create: OCI Generative AI, region `us-chicago-1`, "pick the latest available chat model from the list", **Used by App Builder ON** (warning box: "the classically missed toggle"), Static ID `HELPDESK_AI`.
  - Task 2-alt (type=OpenAI): same service with an OpenAI key; caution box verbatim from spec: prompts and context go to a third party — fine for this workshop's synthetic data; evaluate for your own apps. Note: at instructor-led events the key is provided on-screen; self-paced users bring their own.
  - Task 3 (both types): **governance beat #1** callout — define *token* ("the unit LLMs read and bill by — every AI call in this workshop spends them") and set **Max AI Tokens** on the service ("you cap your own AI usage declaratively").
  - Task 4 (both types): instant feedback — SQL Workshop → SQL Commands → APEX Assistant: ask "Write a query counting tickets by status" (works even before our tables exist? tables don't exist until Lab 2 — use "Write a query that shows today's date in three formats" instead; zero schema dependency).
  - Go further: paste the `resolve-ticket.sql` block and ask the Assistant to explain it.
- [ ] **Step 3: copy blocks** — every OCID/key value uses `<copy>` with `<angle-bracket>` placeholders. **Step 4: validator green for lab 1; tests still OK. Step 5: Commit** `"workshop: lab 1 connect genai (type-conditional)"`

---

### Task 9: Lab 2 — Design the Data Model with AI

**Files:**
- Create: `ai-helpdesk-agent/2-data-model-ai/2-data-model-ai.md` + `images/` placeholders (files/ exists from Task 6)

**Interfaces:**
- Consumes: `files/helpdesk-schema.sql` (Task 6), service `HELPDESK_AI` (Task 8). Produces: the three seeded tables every later lab queries.

- [ ] **Steps 1–5 (red → author → green → commit).** Task list (10 min):
  - Task 1: SQL Workshop → Utilities → Create Data Model Using AI; paste prompt:
    ```
    <copy>Create a data model for an IT help desk: support tickets with subject, description,
    status, priority, category, created date and an assigned team member; knowledge base
    articles with title, content and category; and a small team members table.</copy>
    ```
  - Task 2: **review** the proposed SQL — checklist callout (primary keys? sensible types? FK from tickets to team members? naming?). *Governance beat #2: "You are the reviewer — this is the habit that makes AI-assisted development trustworthy."* Then: **"Do not run the wizard's script — close the wizard"** (info box: the wizard's final step saves a script; we run the vetted room-sync version instead). Recovery note: "Already ran it? No problem — the next step replaces those tables."
  - Task 3: run `helpdesk-schema.sql` (full copy block inline + `files/` download link); verify: `select count(*) from tickets;` → 50, and Object Browser shows 3 tables.
  - Go further: ask the APEX Assistant for "open ticket count by category, ordered by count descending" and run it.

---

### Task 10: Lab 3 — Generate the App from a Prompt

**Files:**
- Create: `ai-helpdesk-agent/3-generate-app/3-generate-app.md` + `images/` placeholders

**Interfaces:**
- Consumes: seeded tables (Task 9). Produces: app "Horizon Help Desk" with pages later labs open by name: **Dashboard**, **Tickets** (Interactive Report + form), **Knowledge Base** (report).

- [ ] **Steps 1–5.** Task list (10 min):
  - Task 1: App Builder → Create App with AI (or Create Application → Generate with AI — match the 26.1 builder wording during screenshot pass); prompt:
    ```
    <copy>Create an application named Horizon Help Desk over my existing TICKETS, KB_ARTICLES
    and TEAM_MEMBERS tables with: a dashboard with charts of tickets by status and category;
    an interactive report on tickets with a form to edit a ticket; and a report on knowledge
    base articles.</copy>
    ```
  - Task 2: **blueprint checklist** before Create — must show Dashboard; Tickets page with **page type Interactive Report** ("Lab 4's AI features only exist on Interactive Report regions — if the blueprint chose Faceted Search or Cards for Tickets, change it here or add an Interactive Report page"); Knowledge Base report; add anything missing declaratively in the blueprint editor.
  - Task 3: Create → Run → log in. Payoff callout: "That's a real web application — authentication, URL, responsive UI — from one reviewed prompt."
  - Task 4: two-minute tour mapping generated artifacts to APEX concepts (page, region, navigation menu) — vocabulary for Labs 4–6.
  - Fallback box (verbatim requirement from spec): "Your generated app may differ — that's the point of generative AI. You need (a) a Tickets Interactive Report page and (b) a Knowledge Base report page; here's how to add either in 60 seconds with Create Page."
  - Go further: **Create Page with natural language** — "a chart page showing open tickets per team member" — then inspect what got generated.

---

### Task 11: Lab 4 — AI Interactive Reports

**Files:**
- Create: `ai-helpdesk-agent/4-ai-interactive-report/4-ai-interactive-report.md` + `images/` placeholders

**Interfaces:**
- Consumes: Tickets Interactive Report page (Task 10). Produces: nothing downstream — self-contained.

- [ ] **Steps 1–5.** Task list (10 min):
  - Task 1 (recovery, 60 s): "No Interactive Report on Tickets? Create Page → describe in natural language: `an interactive report on the TICKETS table` → Create."
  - Task 2: enable AI on the IR (26.1 NL2IR attribute — exact builder path confirmed against `ai-interactive-report-lab/` content during authoring; open that lab file and mirror its steps).
  - Task 3: prompts to try (copy blocks): `show open tickets by priority as a chart`; `group by category, oldest first`; watch each land as **removable chips**.
  - Task 4: *governance beat #3* callout: "APEX never executes AI-generated SQL — the AI maps your intent onto the same declarative report settings you could click by hand. Chips are inspectable and reversible." **Egress callout:** "NL2IR sends your prompt and the report's metadata — not your rows."
  - Go further: column-level AI attributes (mirror `ai-interactive-report-lab` lab 4).

---

### Task 12: Lab 5 — Build the Help Desk AI Agent (marquee, 25 min)

**Files:**
- Create: `ai-helpdesk-agent/5-ai-agent/5-ai-agent.md` + `images/` placeholders (files/ from Task 6)

**Interfaces:**
- Consumes: tables (Task 9), app (Task 10), service `HELPDESK_AI` (Task 8), `files/resolve-ticket.sql` (Task 6). Produces: the workshop's payoff conversation (scripted below — keep the exact three utterances; ticket 42 and article 7 are the fixed seed facts it depends on).

- [ ] **Steps 1–5.** Task list — **open `scm-ai-agent/3-*` and `4-*` labs first and mirror their builder step wording exactly**; our six tasks:
  - Task 1: Shared Components → AI Agents → Create: name `Help Desk Analyst`; system prompt copy block:
    ```
    <copy>You are the Horizon Help Desk analyst assistant. Answer using only the tools
    available to you. When asked about problems, first check the knowledge base for a
    documented fix, then check for related tickets. Be concise. Never invent ticket
    numbers or article titles.</copy>
    ```
    welcome message: `Hi! Ask me about tickets or known fixes — e.g. "any KB fix for VPN error 812?"`.
    Glossary callouts: *agent* (an LLM that can call the tools you attach — and only those) and *tool*.
  - Task 2: AI Tool → Retrieve Data over tickets. SQL source:
    ```
    <copy>select id, subject, status, priority, category, created_on from tickets</copy>
    ```
    *RAG defined in one sentence:* "Retrieval-Augmented Generation: the model's answers are grounded in rows retrieved from your tables, not in its training data."
  - Task 3: second Retrieve Data tool over `kb_articles` (id, title, content, category).
  - Task 4: AI Tool → Execute Server-side Code `resolve_ticket`, code from `files/resolve-ticket.sql` (full copy block); under **User Approval** toggle **Requires Confirmation** ON; Confirmation Title `Confirm Ticket Resolution`, Message `Mark ticket &TICKET_ID. as Resolved?`. Terminology note for authors (HTML comment in the md): conceptually "guardrails," but UI labels only.
  - Task 5: in the app: Tickets page → Dynamic Action **Show AI Assistant** (floating), select the `Help Desk Analyst` agent (mirror scm-ai-agent's embed lab for exact 26.1 wiring).
  - Task 6: the payoff conversation (numbered, verbatim):
    1. `A user reports VPN error 812 - is there a KB fix?` → agent cites article 7's 3-step fix.
    2. `Are there open tickets about it?` → agent lists ticket 42 (+ the other seeded VPN tickets).
    3. `Resolve ticket 42` → **confirmation dialog appears** → Approve → agent confirms; refresh the report: ticket 42 Resolved.
    *Governance beat #4* callout: "The agent can only use the tools you attached, and the write required your approval." **Egress callout:** "The Retrieve Data tools' query results ARE sent to the model as context — you scope what each tool's SQL can see. Contrast Lab 4, which sends metadata only."
  - Live-event note (blockquote): instructor may drive Tasks 5–6 from the podium if the room is behind at minute 60.
  - Go further: add a create-ticket tool; ask the agent something outside its tools ("what's the weather?") and observe the refusal.

---

### Task 13: Lab 6 (OPTIONAL) — Draft Replies with AI

**Files:**
- Create: `ai-helpdesk-agent/6-generate-text/6-generate-text.md` + `images/` placeholders

- [ ] **Steps 1–5.** Requirements: opens with **"Extend your reservation first (one click, while it is still active)"** info box; Generate Text with AI dynamic action on the ticket form's reply/notes item — source = ticket description (+ instruct pattern "draft a courteous reply that walks the user through the documented fix"), editable before save ("AI drafts, human sends"); egress callout (ticket text goes as context); Estimated Time: 10 minutes; marked OPTIONAL in manifest only (title there already has it).

---

### Task 14: Lab 7 (OPTIONAL) — Semantic KB Search

**Files:**
- Create: `ai-helpdesk-agent/7-vector-search/7-vector-search.md` + `images/` placeholders + `files/embed-kb.sql`

**Interfaces:**
- Consumes: KB_ARTICLES (Task 9); Vector Provider mechanics per spec §4 Lab 7 (**decision gate: ONNX in-database is the default plan** — works on both provider tracks; revisit only if week-1 sandbox verification shows `DBMS_VECTOR.LOAD_ONNX_MODEL` unavailable, then fall back to type-conditional OCI/OpenAI providers).

- [ ] **Steps 1–5.** Requirements: reservation-extension box first; Task 1 load ONNX embedding model (mirror `image-semantic-search` lab's exact model-load steps — open it first); Task 2 `files/embed-kb.sql` (full copy block): add `embedding VECTOR` column to `kb_articles`, populate via the ONNX model, note "run from SQL Workshop — APEX session required if you use apex_ai"; Task 3 Workspace Utilities → Vector Providers → create Database ONNX Model provider; Task 4 Search Configuration, Search Type **Oracle Vector Search**, select the provider; Task 5 Create Page → Search page; the wow query (copy block): `laptop won't connect from hotel wifi` → finds the VPN article with zero keyword overlap; *embedding* glossary callout; Estimated Time: 15 minutes.

---

### Task 15: Take It Home lab

**Files:**
- Create: `ai-helpdesk-agent/8-take-it-home/8-take-it-home.md` + `images/` placeholder

- [ ] **Steps 1–5.** Required content: export the app (App Builder → Export; one paragraph noting APEXlang/SQLcl as the source-control-friendly export); download links for the three SQL files; **warning box: the sandbox is deleted at reservation end — export now**; "run this again free" (apex.oracle.com + Always Free); governance recap paragraph naming all five mechanisms (objective 5 closure); learning trail links (LiveLabs catalog, APEX Office Hours, Insum APEX Instant Tips, Cloud Nueva, apex.world); "your next workshop" pointers (scm-ai-agent, crm-apexlang); Estimated Time: 5 minutes.
- [ ] **Validator full green check:** `python3 tools/validate_workshop.py` → `0 error(s)`, exit 0 (without `--final`; placeholders remain by design until Task 18). Also run `--online` once to verify the three CDN URLs.

---

### Task 16: Event runbook

**Files:**
- Create: `docs/event-runbook.md`

- [ ] **Step 1: Author** per spec §6: sections = Event-tenancy sizing (ADB count or shared pre-provisioned instances + per-attendee workspaces — bootcamp pattern); OCI GenAI limits pre-negotiation / compartment-or-region sharding for hundreds of concurrent users; Event Code timeline (request ≥1 week out; active day-before to day-after); OpenAI relief-valve key (spend cap, on-screen distribution, immediate revocation); day-of contingencies (Lab 5 podium rule; 429 guidance); teardown checklist. Each section: checklist form with owner column (Rick/event team).
- [ ] **Step 2: Commit** `"docs: large-event delivery runbook"`

---

### Task 17: Repo lint gates

- [ ] **Step 1:** locate the repo's lint tooling: `ls /mnt/c/Users/rickh/GitHub/apex/.github/workflows/` and check for `lintchecker`/`md-validator` configs (also look at what CI ran on recent PRs: `git -C /mnt/c/Users/rickh/GitHub/apex log --oneline -5 upstream/main` and the PR checks of a recent merged PR via `gh pr list -R oracle-livelabs/apex --state merged --limit 3`).
- [ ] **Step 2:** run whatever is runnable locally against `ai-helpdesk-agent/` only; fix findings; re-run validator + unit tests (all green).
- [ ] **Step 3: Commit** `"workshop: pass repo lint gates"`

---

### Task 18: Screenshot pass (EXTERNAL GATE — real sandbox reservation)

- [ ] **Step 1:** From a real LiveLabs sandbox reservation (also satisfies the spec's week-1 GenAI verification if not yet done): execute the whole workshop following the labs verbatim; capture every placeholder's `.caption.txt` shot (one browser window size; one theme mode — match `common-261/2-configure-ai-keys` dark-mode convention if that include ships verbatim; **no unredacted OCIDs/tenancy names/key material**).
- [ ] **Step 2:** replace placeholders (same filenames), delete `.caption.txt` files, export the finished app → `ai-helpdesk-agent/ai-helpdesk-agent.zip` (nyc-genai-lab pattern) and link it from Take It Home.
- [ ] **Step 3:** `python3 tools/validate_workshop.py --final --online` → 0 errors. Record actual lab timings vs §4 budget in `tasks/todo.md`; adjust Estimated Time headers if reality disagrees (validator re-run must stay ≤ 90 core).
- [ ] **Step 4: Commit** `"workshop: real screenshots + finished app export (final gate green)"`

---

### Task 19: Self QA + WMS (Rick, EXTERNAL)

- [ ] Timed click-through on a fresh reservation by someone who didn't write the labs (or Rick cold); log issues as validator rules where checkable; fix and re-run `--final --online`.
- [ ] Rick: WMS submission flow (abstract/prerequisites/tags from spec §3; Workshop Time 90; Sandbox Lite checkbox; full-sandbox Jira in parallel; Publish entry).

---

### Task 20: Clean PR branch

- [ ] **Step 1:** `git -C /mnt/c/Users/rickh/GitHub/apex fetch upstream && git -C /mnt/c/Users/rickh/GitHub/apex checkout -b ai-helpdesk-agent-pr upstream/main` — wait: `upstream` may not be configured; if `git remote -v` lacks it, `git remote add upstream https://github.com/oracle-livelabs/apex.git` first.
- [ ] **Step 2:** `git checkout apex-ai-workshop-spec -- ai-helpdesk-agent/` → commit ONLY the workshop folder: `git add ai-helpdesk-agent && git commit -s -m "WMS <ID>: Add Build an AI-Powered Help Desk with Oracle APEX workshop"` (OCA sign-off `-s`; WMS ID in title — PR is rejected without it).
- [ ] **Step 3:** push to Rick's fork, open PR to `oracle-livelabs/apex:main` with WMS ID in the PR title (Rick approves the gh commands).

---

## Self-Review (done at plan time)

- **Spec coverage:** §4 labs → Tasks 7–15; §5 tracks → manifests (Task 5) + runbook (Task 16); §6 structure/screenshots → Tasks 5/18; §7 TDD harness → Tasks 1–4 precede all content, SQL gates in Task 6; §8 process → Tasks 19–20 (external gates flagged). Gap check: none found; spec's "quiz lab" was never adopted (spec §4 omits it deliberately).
- **Placeholder scan:** the only deferred artifacts are screenshots and the app zip — physically impossible before a live run; both are explicit external-gate tasks with a validator `--final` backstop, not TBDs.
- **Type consistency:** service Static ID `HELPDESK_AI` (Tasks 8/12/14); table/column names identical across Tasks 6/9/10/12/14; ticket 42/article 7 facts identical in Tasks 6 and 12; placeholder marker bytes identical in Tasks 4 and 5.
