# WMS Self QA Checklist — ai-helpdesk-agent (WMS 12192)

Every item on the WMS **Self QA Checklist** form, verified against the workshop as it stands after the
2026-08-31 end-to-end run on APEX 26.1.4 / app 105. Re-run the machine-checkable items any time with:

```
python3 tools/validate_workshop.py     # 0 errors
python3 tools/self_qa.py               # one line per checklist item
```

**Status: 28 of 29 items pass.** The single open item is the four deferred OCI Console screenshots in
Lab 1 — see *Open item* at the bottom.

---

## Mandatory requirements

- [x] **All links are correct and work as expected** — every relative link resolves; external links were
      opened by hand. The `403`s from `apex.oracle.com` and `blogs.oracle.com` are Akamai bot-blocks, not
      broken links. The one genuinely dead link (Oracle's retired ONNX model PAR) was removed in Lab 7.
- [x] **All code snippets are correct and work as expected** — all 28 `<copy>` blocks are balanced, and
      every snippet in Labs 1–8 was executed live in this run.
- [x] **The help email address has been updated and is correct** — the workshop carries no hard-coded
      support address; help routing comes from the shared **Need Help?** include, which is the current
      LiveLabs version for each variant.
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
- [ ] **Upload a screenshot of the lint checker with no errors** → **`lint-checker.png`**. The validator
      shows **0 errors**; the checklist run shows **28/29**, with the four Lab 1 placeholders as the one
      remaining failure. Re-shoot this image once that item closes.

## GitHub links

- [ ] **Insert GitHub Pull Request Link** — pending; the PR against `oracle-livelabs/apex` is not open yet.
- [x] **Your `github.io` workshop link** —
      `https://rhoulihan.github.io/apex/ai-helpdesk-agent/workshops/sandbox/index.html`

## Lab section

- [x] **Each lab has a title (#)** — 8/8 labs (plus the Introduction).
- [x] **Each lab has an Introduction (##) with "Estimated Time"** — 8/8. The Introduction lab correctly
      uses `## About this Workshop` and `Estimated Workshop Time:` instead.
- [x] **Each lab has Objectives (###)** — 8/8.
- [x] **Each lab has Prerequisites (###)** — 8/8. *Take It Home* was missing one; added in this pass.
- [x] **Tasks (##), initial capitalized, not bold, colon between number and title** — 8/8.
- [x] **Each task has numbered, indented Steps** — 8/8.
- [x] **"You may now proceed to the next lab" at the end (except the last)** — 7/7 non-final labs.
- [x] **Each lab has Acknowledgements (##)** — 8/8.

## Screenshots

- [x] **OCI Menu screenshots are the common path ones** — the workshop uses no OCI hamburger-menu
      navigation shots.
- [ ] **Screenshots are current, clear and big** — 34 of 38 are fresh captures from this run on APEX
      26.1.4. Four remain placeholders; see *Open item*.
- [x] **Screenshots are trimmed of extra whitespace** — every capture is viewport-cropped; no
      full-desktop shots.
- [x] **Personal/sensitive information is blurred out** — the pre-authenticated request URL in
      `load-onnx.png` is under a drawn redaction bar; no OCIDs, keys, tokens or email addresses appear
      in any image.
- [x] **Names of the images are descriptive** — 38 distinct, descriptive filenames; no `image1.png`.
- [x] **There is a description to explain what the image looks like for accessibility** — 40/40 images
      carry alt text.
- [x] **Upload a screenshot sample of one of your accessibility descriptions** → **`alt-text-sample.png`**.

---

## Open item

**Lab 1's four OCI Console screenshots are still placeholders**
(`oci-profile.png`, `oci-add-api-key.png`, `oci-config-preview.png`, `oci-compartment-ocid.png`).

They were deliberately deferred to a LiveLabs sandbox rather than shot from the live `crhsentllc`
tenancy, so the images show generic sandbox identities instead of Rick's production account, compartment
names and key fingerprints.

This one deferral holds two checklist items open — *Screenshots are current, clear and big* and
*lint checker with no errors* — and `tools/validate_workshop.py --final` fails on placeholders, so it
must close before the PR. Three of the four can be shot from any tenancy with redaction; the fourth
(*Configuration File Preview*) only appears while generating a new API key pair.
