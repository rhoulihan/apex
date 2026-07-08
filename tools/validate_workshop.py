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
    """sandbox: Introduction, Get Started, sign-up, ..., Need Help? last.
    tenancy/event (nyc-genai-lab pattern): Introduction, sign-up, ..., Need Help? last."""
    errs = []
    titles = [t.get("title", "") for t in manifest.get("tutorials", [])]
    if not titles:
        return [f"{variant}: manifest has no tutorials"]
    if not titles[0].startswith("Introduction"):
        errs.append(f"{variant}: Introduction must be first, got '{titles[0]}'")
    if variant == "sandbox":
        if len(titles) > 1 and not titles[1].startswith("Get Started"):
            errs.append(f"{variant}: Get Started must be second, got '{titles[1]}'")
        if len(titles) > 2 and "Sign up" not in titles[2]:
            errs.append(f"{variant}: sign-up lab must be third, got '{titles[2]}'")
    else:
        if len(titles) > 1 and not ("Sign" in titles[1] or "Provision" in titles[1]):
            errs.append(f"{variant}: Sign Up/Provision lab must be second, got '{titles[1]}'")
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
    if md_path.name == "introduction.md":
        # official LiveLabs gate (validate-livelabs-markdown.sh) requires this exact phrase
        if "Estimated Workshop Time:" not in text:
            errs.append(f"{md_path.name}: missing 'Estimated Workshop Time:' line")
    elif "Estimated Time" not in text and "Estimated Lab Time" not in text:
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
            continue  # missing files are reported by check_paths_resolve
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
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--online", action="store_true", help="HEAD-check https includes")
    ap.add_argument("--final", action="store_true", help="pre-PR gate: fail on placeholder screenshots")
    args = ap.parse_args(argv)
    root = Path(__file__).resolve().parent.parent
    config = json.loads((Path(__file__).resolve().parent / "validator_config.json").read_text())
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
            errs.append(str(e))
            continue
        errs += check_manifest_order(m, variant)
        errs += check_paths_resolve(m, vd, online=args.online)
        errs += check_time_budget(m, variant, vd, config)
        for t in m.get("tutorials", []):
            fn = t.get("filename", "")
            # only labs local to this workshop get structure/bans checks
            # (common-* includes start ../../../ and are not ours to lint)
            if not fn.startswith("http") and fn.startswith("../../") and not fn.startswith("../../../"):
                p = (vd / fn).resolve()
                if p.exists():
                    errs += check_lab_structure(p)
                    errs += check_banned_strings(p, config)
                    if args.final:
                        imgdir = p.parent / "images"
                        for img in imgdir.glob("*.png") if imgdir.exists() else []:
                            if b"PLACEHOLDER-SCREENSHOT" in img.read_bytes():
                                errs.append(f"--final: placeholder screenshot remains: {img.relative_to(root)}")
    seen = set()
    for e in errs:
        if e not in seen:
            seen.add(e)
            print("FAIL:", e)
    print(f"{len(seen)} error(s)")
    return 1 if seen else 0


if __name__ == "__main__":
    sys.exit(main())
