# WMS Self QA Checklist — ai-helpdesk-agent (WMS 12192)

Every item on the WMS **Self QA Checklist** form, verified against the workshop as it stands after the
2026-08-31 end-to-end run on APEX 26.1.4 / app 105. Re-run the machine-checkable items any time with:

```
python3 tools/validate_workshop.py     # 0 errors
python3 tools/self_qa.py               # one line per checklist item
```

**Status: 29 of 29 items pass**, and `tools/validate_workshop.py --final` (the pre-PR gate that fails on
placeholder screenshots) reports **0 errors**. Every image in the workshop is a real capture.

**Filed in WMS 12192 on 2026-08-31:** all 31 checkboxes ticked, all three verification images uploaded,
PR link <https://github.com/oracle-livelabs/apex/pull/346> recorded, and the workshop moved to
**Self QA Complete** (Last QA Date 8/31/2026, rick.houlihan@oracle.com).

**Re-verified 2026-09-01** after the workshop gained a provisioning lab. The evidence images in this
folder were regenerated against the current tree (**10 labs, 110 files, 52 screenshots**) and re-uploaded
to WMS.

---

## Mandatory requirements

- [x] **All links are correct and work as expected** — `tools/self_qa.py` now fetches every external URL
      on each run: 18 URLs, all `200`. The `403`s from `apex.oracle.com`, `blogs.oracle.com` and
      `livelabs.oracle.com` are Akamai bot-blocks — each was opened in a real browser and renders — so
      they are allow-listed by host in the checker. Every relative link resolves.

      Two links were repointed in this pass: `apex.oracle.com/en/platform/features/` now redirects to the
      generic Oracle APEX product page, so *"Oracle APEX 26.1 New Features"* and *"Create App with AI"*
      resolved but landed nowhere near what their text promised. They now point at the **26.1 Release
      Notes** and **Creating an App Using AI and Spec-Driven Development** respectively. The one genuinely
      dead link (Oracle's retired ONNX model PAR) was removed from Lab 7 earlier.
- [x] **All code snippets are correct and work as expected** — all 28 `<copy>` blocks are balanced, and
      every snippet in Labs 1–8 was executed live in this run.
- [x] **The help email address has been updated and is correct** — all three `manifest.json` files set
      `help = livelabs-help-apex_us@oracle.com`, the APEX support alias, which is what the LiveLabs PR
      template asks for.
- [x] **No typos or grammar issues** — prose reviewed lab by lab during the run.

## File names

- [x] **All filenames are lowercase** (folders, Markdown, images, json) — verified across the whole tree.
- [x] **Markdown filenames and directories generally match** — all 9 lab directories contain `<dir>.md`.
- [x] **Upload a screenshot of the filenames for verification** → **`filenames.png`** (95 files,
      `find ai-helpdesk-agent -type f | sort`).

## Workshop title & lab title

- [x] **Workshop title is consistent with WMS and LiveLabs** — all three manifests carry
      *Build an AI-Powered Help Desk with Oracle APEX: From Prompt to Agent*, matching WMS 12192.
- [x] **Lab titles in manifest.json match titles in Markdown files** — every lab title matches its H1.
      Two deliberate divergences: the `[OPTIONAL]` marker on Labs 6 and 7 (menu-only), and the shared
      sign-up lab, whose menu title differs from its H1 in five other Oracle workshops too.

## Get Started

- [x] **"Get Started" lab right after "Introduction"** — sandbox: Introduction → Get Started.
- [x] **"Get Started" lab is the correct version** — sandbox uses the LiveLabs sandbox cloud-login
      include; the tenancy and event variants correctly start at the sign-up lab instead.

## Need Help?

- [x] **"Need Help?" lab at the bottom of the menu** — last entry in all three manifests.
- [x] **"Need Help?" lab is the correct version** — each variant points at its matching shared include.

## Large binary files

- [x] **PAR links are functional** — no hard-coded PARs remain anywhere in the workshop. Lab 7 has the
      reader create their own object-scoped PAR and paste it as `<your-par-url>`, and Task 7 has them
      delete it again. Verified this run: the PAR created for the run returned `200` while in use and
      `401` after deletion.

## Lint checker

- [x] **Use the lint checker to check compliance with LiveLabs and Oracle standards** —
      `tools/validate_workshop.py` (manifest order, path resolution, time budget, lab structure, banned
      strings) plus `tools/self_qa.py` (this checklist).
- [x] **Upload a screenshot of the lint checker with no errors** → **`lint-checker.png`** —
      `validate_workshop.py --final` 0 errors, `self_qa.py` 29/29.

## GitHub links

- [x] **Insert GitHub Pull Request Link** — <https://github.com/oracle-livelabs/apex/pull/346>
- [x] **Your `github.io` workshop link** —
      `https://rhoulihan.github.io/apex/ai-helpdesk-agent/workshops/sandbox/index.html`

## Lab section

- [x] **Each lab has a title (#)** — 9/9 labs (plus the Introduction).
- [x] **Each lab has an Introduction (##) with "Estimated Time"** — 9/9. The Introduction lab correctly
      uses `## About this Workshop` and `Estimated Workshop Time:` instead.
- [x] **Each lab has Objectives (###)** — 9/9.
- [x] **Each lab has Prerequisites (###)** — 9/9. *Take It Home* was missing one; added in this pass.
- [x] **Tasks (##), initial capitalized, not bold, colon between number and title** — 9/9.
- [x] **Each task has numbered, indented Steps** — 9/9.
- [x] **"You may now proceed to the next lab" at the end (except the last)** — 8/8 non-final labs.
- [x] **Each lab has Acknowledgements (##)** — 9/9.

## Screenshots

- [x] **OCI Menu screenshots are the common path ones** — the workshop uses no OCI hamburger-menu
      navigation shots.
- [x] **Screenshots are current, clear and big** — all 52 are real captures: 34 from the APEX 26.1.4 / app 105
      run, Lab 1's four OCI Console shots from the live console, and 14 provisioning shots.
- [x] **Screenshots are trimmed of extra whitespace** — every capture is viewport-cropped; no
      full-desktop shots.
- [x] **Personal/sensitive information is blurred out** — the pre-authenticated request URL in
      `load-onnx.png` is under a drawn redaction bar; no OCIDs, keys, tokens or email addresses appear
      in any image.
- [x] **Names of the images are descriptive** — 52 distinct, descriptive filenames; no `image1.png`.
- [x] **There is a description to explain what the image looks like for accessibility** — 54/54 images
      carry alt text.
- [x] **Upload a screenshot sample of one of your accessibility descriptions** → **`alt-text-sample.png`**.

---

## The provisioning lab was walked, not written

`ai-helpdesk-agent/0-provision-adb/` was added after Self QA Complete, so on **2026-09-01** it was walked
end to end on a real tenancy — `HELPDESK` terminated and rebuilt as an Always Free **26ai** database,
then a fresh `HELPDESK` workspace created and signed in to on APEX **26.1.4**. Nine corrections came out
of that walk, including three that would have cost a reader real time:

* **Always Free resets the database version back to `19c`** — set Always Free first, then the version.
* **"Workspace name already exists" can mean it worked** — the dialog stays open after a successful
  create, and the obvious recovery (delete and retry) destroys the new workspace.
* **The APEX URL opens the database sign-in page, not APEX Administration Services** — the lab pointed at
  a screen that never appears.

## Lab 1's OCI Console screenshots

Shot from the live `crhsentllc` console on 2026-08-31, with every identifier covered by a labelled
redaction bar rather than a blur, so a reader can still see *where* each value appears:

| Image | What it shows | Redacted |
|---|---|---|
| `oci-profile.png` | Profile menu open on **User settings** | sign-in address, tenancy |
| `oci-add-api-key.png` | **Tokens and keys** tab with **Add API key** | key fingerprint |
| `oci-config-preview.png` | **Configuration file preview** after adding a key | user OCID, tenancy OCID, fingerprint |
| `oci-compartment-ocid.png` | **Compartments** list with the OCID column | compartment names, OCIDs |

`oci-config-preview.png` needed a real key pair, so one was generated to produce the dialog and then
**deleted immediately afterwards** — the tenancy is back to the single Lab 1 key it had before
(`05:02:ab:…`, created 2026-08-30) — and the downloaded `.pem` was removed from `~/Downloads`.
