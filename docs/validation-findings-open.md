# Validation findings — status tracker

**Rule for this file: a finding is not done until it is IMPLEMENTED in the labs.**
Recording alone is not sufficient. Each entry below is marked ✅ IMPLEMENTED (with where), or
⬜ OPEN with what still blocks it.

**Last updated:** 2026-08-30 · **Source:** live validation run on Rick's own tenancy
(`crhsentllc`, ADB `HELPDESK`, Always Free, 26ai, APEX **26.1.4**, workspace `HELPDESK` / schema `WKSP_HELPDESK`)

## Status summary

| # | Finding | Status |
|---|---|---|
| 1 | APEX 26.1.4 vs 26.1.1 version drift | ✅ IMPLEMENTED — `introduction.md` "Before You Begin" |
| 2 | `WKSP_` schema prefix | ✅ IMPLEMENTED — `introduction.md` + Lab 7 Task 1 callout |
| 3 | "Always Free" refused on sandboxes | ✅ IMPLEMENTED — `sign-up-apex-sandbox.md` callout + 19c default warning |
| 4 | OCI region/model reference data | ✅ IMPLEMENTED — Lab 1 region + model guidance |
| 5 | Sandbox GenAI 429 quota | ✅ IMPLEMENTED — Lab 1 troubleshooting now distinguishes busy-service from zero-quota and routes to the OpenAI track |
| 6 | In-product governance disclaimer | ✅ IMPLEMENTED — quoted in Lab 2 governance beat #2 |
| 7 | T18 screenshots | 🟡 IN PROGRESS — 15/38 captured live on APEX 26.1.4. `openai-key.png` **dropped** (OpenAI track is a fallback; the step reads fine without it). The 4 OCI-console shots (`oci-profile`, `oci-add-api-key`, `oci-config-preview`, `oci-compartment-ocid`) are **deliberately deferred to the LiveLabs sandbox** so console chrome, compartment names and region pickers match what attendees see, per the spec's "never from Rick's tenancy" rule — not missing work. |
| 8 | ORA-20987 dashboard chart defect | ✅ IMPLEMENTED — Lab 3 Task 3 workaround + defect report drafted |
| 9 | Model must support tool calling | ✅ IMPLEMENTED — Labs 1/4/5 + guarded by `tools/test_model_guidance.py` |
| 10 | Labs 4 and 5 need **different** models; two distinct 429s | ✅ IMPLEMENTED — Lab 1 + Lab 5 tables, switch instructions, guarded by tests |
| 11 | Re-verify xAI for Lab 5 once service limits are raised | ⬜ OPEN — blocked on provisioning; steps written into `docs/wms-submission.md` step 3② + step 5 |
| 12 | **Lab 7 ONNX URL dead; Oracle ships only `.zip` now** | ✅ **RESOLVED for the tenancy track** — full download/unzip/bucket/PAR procedure written as Lab 7 Tasks 2–3 and **validated end to end**. Still requested as provisioning item 3③ so the sandbox track does not need a reader-owned bucket. |
| 13 | Seed data too thin for vector demos | ✅ IMPLEMENTED — 20 → 30 articles, targeted at coverage gaps; all three demo queries now measured correct |
| 14 | Lab 7 shipped a known-dead PAR as a runnable `<copy>` block; `Task 2a` broke task numbering | ✅ IMPLEMENTED — hosting is Task 2, loading is Task 3 using the reader's own PAR; tasks renumbered 1–7 |
| 15 | **PR scope: internal-only files would ship to the public Oracle repo** | ⬜ **OPEN — needs Rick's decision.** `docs/`, `tools/`, `tasks/` (20 files) are ours and do not exist upstream; `docs/wms-submission.md` carries the Southwest Airlines account justification |

Detail for each follows.

---

## 1. 🔴 APEX version drift: 26.1.4 here vs 26.1.1 on LiveLabs sandboxes

| Environment | APEX | Observed |
|---|---|---|
| LiveLabs green-button sandbox | `26.1.1` | 2026-07-28 |
| Fresh Always Free ADB (26ai), own tenancy | `26.1.4` | 2026-08-30 |

Same feature set for this workshop (the 26.1 agent data model is present in both), but **screenshots taken
on one may not match the other**. Decide before T18 screenshot capture which version is canonical, and
say so in the workshop prerequisites. Ideally capture on whatever a green-button sandbox serves, since
that is what most readers get.

## 2. 🟠 `WKSP_` schema prefix — re-confirmed, still undocumented in Labs 2 and 7

Asking for schema `HELPDESK` yields **`WKSP_HELPDESK`** on Autonomous. Confirmed again on 26.1.4
(SQL Workshop schema selector reads `WKSP_HELPDESK`). Any lab SQL that schema-qualifies an object must
use the prefixed name. Labs 2 and 7 currently do not mention this.

## 3. 🟠 "Always Free" wording may now be too pessimistic

`WMS-SUBMISSION.md` and the outline were softened to *"Always Free where available, else trial credits"*
after Always Free was refused on both sandbox regions in July. On a **personal tenancy in its home
region** Always Free worked with no issue (this ADB is Always Free). The hedge is still correct for
green-button sandboxes; consider splitting the wording per workshop variant rather than hedging globally.

## 4. 🟡 OCI Generative AI region/model reality (reference data)

- Chat models offered in **us-phoenix-1** — none served on-demand, all returned
  `HTTP-404: Entity with key <model> not found`:
  `cohere.command-r-plus-08-2024`, `google.gemini-2.5-flash`, `google.gemini-2.5-flash-lite`,
  `google.gemini-2.5-pro`, `xai.grok-4.20-0309-non-reasoning`, `xai.grok-4.20-0309-reasoning`,
  `xai.grok-4.20-non-reasoning`, `xai.grok-4.20-reasoning`, `xai.grok-4.3`
- **us-chicago-1** with `cohere.command-a-03-2025` → `Connection Succeeded!`
- APEX's Region field quick-links (Chicago / Ashburn / Phoenix / Frankfurt / London) are **not** a
  guarantee of on-demand availability — Phoenix is listed but serves nothing on-demand. Worth a warning
  if we ever name regions beyond Chicago.

## 5. 🟡 The 429 quota question is answered for TENANCIES, still open for SANDBOXES

**No** `max-on-demand-chat-request-per-minute-count` throttle exists in `crhsentllc` — the OCI GenAI track
works end to end. This does **not** retire the LiveLabs provisioning ask: the green-button sandbox quota
(`SUMMARY.md` §2, evidence `screenshots/009-test-result.png`) has not been re-tested since 2026-07-28.
Two unused sandbox sessions exist (`LL219273`/c4u02, `LL227625`/c4ustudent03) — re-testing one of those is
the only way to validate the workshop *as students receive it*.

## 6. 🟡 In-product governance artifacts worth citing in the docs

Both support the workshop's governance narrative and are quotable:
- Generative AI service create form exposes **`Maximum AI Tokens`** (set to `500000` in Lab 1 Task 3).
- APEX Assistant panel displays, unprompted: *"Please note that AI-generated code may contain errors or
  security risks. Always review and validate all code before use."* — this is Oracle's own text backing
  the "human review of AI-generated SQL" claim, not just ours.

## 7. ⬜ T18 screenshots still 39 placeholders

Unchanged; keeps `--final` red. Lab 1 now has real screens available to capture
(region subscription, Add API key dialog, GenAI service form, terms dialog, Assistant result).

## 8. 🔴 APEX 26.1.4 defect — generated dashboard charts fail with ORA-20987

**Every reader will hit this**, on the first screen they see after generating the app in Lab 3.

Verbatim runtime error on the Dashboard:

```
Ajax call returned server error ORA-20987: APEX - Column "ID" specified for attribute ""
has not been found in data source! for Tickets by Category.
```

Both charts render **"No data to display"**.

**Root cause (confirmed, not inferred).** The Create App wizard builds each chart series as
`Source Type = Table / View` on `TICKETS` with `Value Aggregation = Count` and **no Value column**.
Switching the source type to `SQL Query` reveals the query APEX generates for it:

```sql
select ID, SUBJECT, DESCRIPTION, STATUS, PRIORITY, CATEGORY, CREATED_ON, ASSIGNED_TO, REPLY
from TICKETS
```

It projects **every column, including `ID`**, and then aggregates. After the implied `group by`,
`ID` is not in the result set, so the reference to it cannot resolve. The offending attribute is
reported as `""` (blank) and is **not exposed anywhere in the Page Designer property editor** —
neither on the series nor the region. Re-saving the page does **not** clear it.

**Workaround — ~60 seconds per chart, verified working 2026-08-30:**

1. Page Designer > page 1 > chart region > **Series 1**.
2. Source: set **Type** = `SQL Query`.
3. Replace the query with an explicit aggregate:

   ```sql
   select status as label, count(*) as value from tickets group by status order by 1
   ```

   (and `category` for the second chart)
4. Column Mapping: **Label** = `LABEL`, **Value** = `VALUE`. `Value Aggregation` disappears — correct.
5. **Save**, then reload the running app.

Result: both charts render correctly (`Closed / In Progress / Open / Resolved`, and
`Access / Email / Hardware / Network / Software`).

**Decision needed before publishing:**
- (a) Document the workaround in Lab 3 as a known 26.1.4 issue, or
- (b) Have Lab 3's prompt ask for charts defined by SQL query rather than table+aggregate, or
- (c) Report to the APEX team and hope it is fixed before the workshop ships.

Recommend (a) + (c): a reader cannot be left staring at a broken dashboard at the exact moment the
lab says *"Take that in: a real web application."* Note this is **not blocking for Labs 4–6** — none of
them depend on the dashboard charts — so it is a polish/credibility issue, not a functional gate.

## 9. 🔴 CRITICAL — AI Interactive Reports only work with SOME OCI GenAI models

**Tested 2026-08-30 on APEX 26.1.4, same report, same prompt** (`show open tickets by priority as a chart`),
OCI Generative AI in `us-chicago-1`, changing only the Model ID:

| Model | Result |
|---|---|
| `cohere.command-a-03-2025` — **APEX's own pre-filled default** | ❌ `HTTP-400 {"error_type":"INVALID_TOOL_GENERATION","message":"your request resulted in an invalid tool generation. Try updating the messages or tool definitions"}` |
| `google.gemini-2.5-pro` | ❌ `HTTP-400 {"error":{"code":400,"message":"Invalid JSON payload received. Unknown name \"$schema\" at 'tools[0].function_declarations[0].parameters': Cannot find field.` |
| **`xai.grok-4.3`** | ✅ **WORKS** — chips `Chart` + `Status in 'Open, In Progress'`, bar chart by priority |

Note **all three pass `Test Connection`** — that only exercises a plain chat completion, not tool calling.
So a reader can configure Lab 1 perfectly, see "Connection Succeeded!", and still have Lab 4 fail.

**Analysis.** AI Interactive Reports translate the prompt into declarative report settings via
**tool/function calling**. APEX 26.1.4 emits tool definitions containing a **`$schema`** key. Google's
function-declaration API rejects unknown fields outright; Cohere accepts the call but cannot generate a
valid tool invocation against it. Only the xAI models (OpenAI-compatible tool schema, tolerant of extra
keys) worked. This looks like an APEX defect — the `$schema` key should not be emitted — with a
model-compatibility matrix as the practical consequence.

**Impact on the workshop — this is not cosmetic:**
- Lab 1 currently says *"Model ID: pick the latest available chat model from the list"*. Two of the three
  obvious picks, **including the one APEX pre-fills for you**, break Lab 4 completely.
- The errors name tool generation and JSON payloads. Nothing points at the model. A reader will assume
  they misconfigured the report and will not recover.
- **Lab 5 (AI Agents with declarative tools) almost certainly has the same dependency** — agents are
  tool-calling by definition. Untested as of this writing; test before shipping.

**Required doc changes:**
1. Lab 1 must **name a known-good model** (`xai.grok-4.3` verified) rather than telling readers to choose.
   Keep the "models get deprecated" caveat, but give a working default and a fallback list.
2. Add to Lab 1 troubleshooting: `INVALID_TOOL_GENERATION` or `Unknown name "$schema"` means **the model
   does not work with APEX's tool calling — change the Model ID**, not the report configuration.
3. State explicitly that **`Test Connection` succeeding does not prove Labs 4 and 5 will work**, because
   it does not exercise tool calling.

**Still to determine:** whether any Cohere or Meta model in Chicago works, and whether the OpenAI track
(Lab 1's alternative) is affected — OpenAI tolerates extra schema keys, so it is likely fine, which would
make the OpenAI track *more* reliable than the OCI track for Labs 4-5. That inverts the workshop's
current framing of OCI as primary and OpenAI as fallback.

## 10. 🔴 Labs 4 and 5 need DIFFERENT models — no single OCI model passes both

Corrects and supersedes finding #9's implication that `xai.grok-4.3` is the answer for the whole workshop.
Verified 2026-08-30 on APEX 26.1.4, OCI GenAI `us-chicago-1`:

| Model | Lab 4 — AI Interactive Report | Lab 5 — AI Agent (On Demand tools) |
|---|---|---|
| `cohere.command-a-03-2025` (APEX default) | ❌ `INVALID_TOOL_GENERATION` | ✅ **works** — and is what APEX itself recommends |
| `xai.grok-4.3` | ✅ works | ⚠️ **unverified** — hit a per-model service limit before answering |
| `google.gemini-2.5-pro` | ❌ rejects `$schema` | untested |
| older Cohere models | untested | ❌ `ORA-20950: ... does not support On Demand tools. Oracle recommends upgrading to at least "cohere.command-a-03-2025"` |

**The two features are not equivalent.** AI Interactive Reports and AI Agents both use tool calling, but
they emit different tool definitions, and APEX validates agent tools itself (ORA-20950 is APEX's own
error, not a passthrough). A model can support one and not the other.

**Two distinct 429s — do not conflate them:**

1. `Compartment quota max-on-demand-chat-request-per-minute-count is exceeded` — the LiveLabs
   green-button blocker from July. Compartment-scoped. Already a provisioning line-item.
2. `The requested model is throttled because the OCI Generative AI service limit for this model has been
   reached. Request a service limit increase for Generative AI in OCI, then retry.` — **per-model**,
   tenancy/region-scoped. Hit on `xai.grok-4.3` after only two Lab 4 prompts, and it did **not** clear
   after 70 s, so it is a limit, not a burst.

**Consequence for the sandbox/green-button provisioning ask — it must cover BOTH, and name models:**
- compartment quota raised above zero, AND
- per-model service limits for **each** model the workshop uses (currently one xAI model for Lab 4 and
  `cohere.command-a-03-2025` for Lab 5).
- Size for **agents, not chat**: one agent turn is several tool-calling round trips, so Lab 5 consumes far
  more requests per student than Lab 4. A 30-seat room needs real headroom.
- **Open risk:** third-party model capacity (xAI, Google, Meta) may be harder for LiveLabs to raise than
  Cohere, which is Oracle's own partner capacity. If xAI limits cannot be raised, Lab 4 needs either the
  `$schema` defect fixed or the OpenAI track.

**IMPLEMENTED:** Lab 1 names the Lab 4 model, explains the per-model service limit and points at the Lab 5
switch; Lab 5 carries the comparison table and the switch instruction; `tools/test_model_guidance.py`
(39 tests) fails the build if any of it is removed.

## 11. ⬜ OPEN — re-verify the xAI model for Lab 5 once service limits are raised

**Why it is open:** `xai.grok-4.3` is the only model verified to drive **Lab 4**, but it hit a per-model
service limit before **Lab 5**'s agent produced a single answer. Its agent behaviour is therefore
**unverified, not failed** — we never saw it succeed or fail on merit.

**Do this during production/sandbox provisioning testing, after the per-model limits land:**

1. Set Model ID to the xAI model and run **Lab 4**: `show open tickets by priority as a chart`.
2. Without changing the model, run the **whole Lab 5 conversation** — KB question, related tickets,
   `Resolve ticket 42`, approve, and confirm in the database that ticket 42 flipped to `Resolved`.
3. Record how many agent turns complete before any `HTTP-429 ... service limit for this model` appears.

**Outcomes:**
- **xAI drives both** → standardise on one model; delete the Lab 4 ↔ Lab 5 switch from Labs 1 and 5 and
  drop the comparison table to a single line. Simpler workshop.
- **xAI still throttles** → keep the two-model guidance as permanent, and make sure the provisioning ask
  covers `cohere.command-a-03-2025` at agent-scale volume.

**`Test Connection` cannot answer this** — it is a plain chat call and never exercises tool calling.
Only running the labs settles it.

**Tracked in the provisioning ask:** `docs/wms-submission.md`, step 3② and step 5.

## 12. 🔴 BLOCKING — Lab 7's ONNX model URL is dead, and Oracle no longer publishes a bare `.onnx`

**Verified 2026-08-30 on ADB 26ai.** Lab 7 Task 2 (as originally written) cannot work.

**What happens now.** With `DBMS_CLOUD` granted (Task 1 done), the lab's `LOAD_ONNX_MODEL` call returns:

```
ORA-20401: Authorization failed for URI - https://adwc4pm.objectstorage.us-ashburn-1.oci.customer-oci.com
/p/VBRD9P8ZFWkKvnfhrWxkpPe8K03-JIoM5h_8EJyJcpE80c108fuUjg7R5L5O7mMZ/n/adwc4pm/b/OML-Resources/o/all_MiniLM_L12_v2.onnx
ORA-06512: at "C##CLOUD$SERVICE.DBMS_CLOUD$PDBCS_260821_1_0", line 2291
```

The pre-authenticated request in the lab has expired **and** the bucket changed.

**What Oracle publishes today** (resolved via the stable docs lookup
`docs.oracle.com/pls/topic/lookup?ctx=en/database/oracle/oracle-database/26/vecse&id=oml_ai_models_object_storage`,
which redirects to the current *Oracle Machine Learning AI models* page):

- Bucket is now **`OML-ai-models`**, not `OML-Resources`.
- **Every model is published only as `<name>_augmented.zip`. There is no bare `.onnx` for any model** —
  confirmed for all_MiniLM_L12_v2, multilingual_e5_base, multilingual_e5_small, and both CLIP models.
- Downloading `all_MiniLM_L12_v2_augmented.zip` succeeds (HTTP 200, 122,537,890 bytes) and contains
  **`all_MiniLM_L12_v2.onnx` at 133,322,334 bytes (~127 MB)**, plus a LICENSE and README, dated 2025-10-30.
- Pointing `DBMS_CLOUD.GET_OBJECT` at a bare `.onnx` name in the new bucket also fails with ORA-20401 —
  the PAR is scoped to the zip.

**Why this is not a one-line URL swap:**
- `LOAD_ONNX_MODEL` needs the ONNX **blob** (or a file in a directory). The database cannot unzip.
- **`DBMS_VECTOR` in 26ai has no cloud loader** — `all_procedures` shows only `LOAD_ONNX_MODEL`,
  `DROP_ONNX_MODEL`, `INMEMORY_ONNX_MODEL`. There is no `LOAD_ONNX_MODEL_CLOUD` to delegate to.
- The ADB ships **no pre-loaded embedding model**: `select * from all_mining_models` returns no rows.

**Options — needs a decision, each changes the lab's shape:**

1. **Reader-owned Object Storage.** Download the zip, unzip locally, upload the 127 MB `.onnx` to a bucket
   in their own compartment, create a PAR, and use that URI. Works on ADB and is Oracle's documented
   pattern, but adds a bucket + PAR to an *optional* lab and assumes console rights.
2. **Upload into APEX.** Put the `.onnx` in Static Workspace Files and load it from the APEX file view as a
   BLOB. Keeps everything inside APEX, but **127 MB may exceed the instance upload limit** — untested.
3. **Drop the in-database embedding.** Re-scope Lab 7 to use a Vector Provider backed by a remote
   embedding service rather than a local ONNX model. Loses the "nothing left the database" governance
   point, which is the lab's whole thesis.
4. **Ship the model ourselves** in a LiveLabs-owned bucket with a long-lived PAR, and reference that.
   Most reliable for readers; needs a hosting decision and periodic re-verification.

**DECIDED — pursuing option 4.** A LiveLabs-hosted, unzipped `.onnx` with a long-lived URL is now
**provisioning item 3③** in `docs/wms-submission.md`, with option 1 (reader-owned bucket) as the documented
fallback if LiveLabs declines, in which case Lab 7 becomes tenancy-only. Whatever is chosen, **the lab must stop hard-coding a PAR** — PARs
expire. Reference the stable docs lookup URL and tell readers to get the current link from there.

**Note:** Lab 7 already requires ADMIN database access for the Task 1 grants, so it is not a pure
green-button lab today either. Worth deciding whether it stays optional or becomes tenancy-only.

---

## 14. Lab 7 offered a dead PAR as the default path — IMPLEMENTED

Found by the WMS self-QA pass (2026-08-30), checklist item **LARGE BINARY FILES — "PAR links functional"**.

Lab 7 Task 2 opened with a `<copy>` block whose `object_uri` was Oracle's retired model PAR, and placed
the "this no longer works" warning *after* it. Readers copy first and read second, so the documented
failure was the default path. Independently reconfirmed:

```
$ curl https://adwc4pm.objectstorage.us-ashburn-1.oci.customer-oci.com/p/.../all_MiniLM_L12_v2.onnx
{"code":"NotAuthenticated","message":"PAR does not exist"}
```

Object Storage is not behind Oracle's Akamai WAF, so unlike the `403`s on `apex.oracle.com` and
`blogs.oracle.com` (which are bot-blocks, not broken links) this `401` is a genuine dead link.

Secondary defect: the working procedure was numbered **`Task 2a`**, which breaks LiveLabs' sequential
task numbering.

**Implemented:** hosting became **Task 2**, loading became **Task 3** and now takes the reader's own
`<your-par-url>`; the retired-URL explanation survives as a note rather than runnable code; tasks
renumbered gap-free **1–7**; cross-references updated in the Prerequisites, the `PLS-00201` note, and in
`docs/`. Validator 0 errors, 39/39 tests pass.

## 15. PR scope — internal files would ship to the public repo — OPEN

The PR target is the **public** `oracle-livelabs/apex` repo. Confirmed against the root import commit
`49a6a5e` (a 14,351-file squashed upstream import): upstream has **no `docs/`, `tools/`, or `tasks/`** at
root. All 20 such files in our diff are ours, and they are internal working material:

* `docs/wms-submission.md` — contains the **Southwest Airlines (SWA) strategic-account justification**
* `docs/validation-findings-open.md`, `tasks/todo.md` — name Rick's live tenancy `crhsentllc`
* `docs/apex-team-email.md`, `docs/apex-defect-report-ora-20987.md` — unsent internal drafts
* `docs/plans/`, `docs/research/`, `docs/specs/`, `tools/` — build-time material, not workshop content

**Recommended:** the upstream PR should carry only `ai-helpdesk-agent/**` plus the one shared fix to
`common-261/1-sign-up-apex/sign-up-apex-sandbox.md`; everything else stays on the fork.

**Also note:** that `common-261` file is **shared** — `ai-vision-lab`'s sandbox manifest includes it too.
The edit is a correct bug fix (sandboxes refuse Always Free) and benefits both, but the PR description
must call out the cross-workshop change so reviewers are not surprised.
