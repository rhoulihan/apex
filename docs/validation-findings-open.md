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
| 7 | T18 screenshots (39 placeholders) | ⬜ OPEN — needs real capture; cannot be written, only taken |
| 8 | ORA-20987 dashboard chart defect | ✅ IMPLEMENTED — Lab 3 Task 3 workaround + defect report drafted |
| 9 | Model must support tool calling | ✅ IMPLEMENTED — Labs 1/4/5 + guarded by `tools/test_model_guidance.py` |

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
