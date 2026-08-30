# Open validation findings — confirmed but NOT yet written into the lab docs

**Last updated:** 2026-08-30 · **Source:** live validation run on Rick's own tenancy
(`crhsentllc`, ADB `HELPDESK`, Always Free, 26ai, APEX **26.1.4**, workspace `HELPDESK` / schema `WKSP_HELPDESK`)

Lab 1's seven fixes are already applied to `ai-helpdesk-agent/1-connect-genai/1-connect-genai.md`.
**Everything below is verified but still undocumented** — it is parked here so it is not lost.

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
