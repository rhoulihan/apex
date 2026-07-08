"""LiveLabs workshop validator for ai-helpdesk-agent. Stdlib only.

Usage: python3 tools/validate_workshop.py [--online] [--final]
Exit 0 = all checks pass; exit 1 = errors printed to stdout.
"""
import json
import re
import sys
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
