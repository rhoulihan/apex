# APEX + AI LiveLabs Workshop — Task Tracker

Spec: `docs/specs/2026-07-07-apex-ai-workshop-spec.md` (rev 3, APPROVED 2026-07-08)
Plan: `docs/plans/2026-07-08-ai-helpdesk-agent-workshop.md`

## Phase 1 — Research
- [x] All research complete (see docs/research/)

## Phase 2 — Spec
- [x] Spec written, adversarially reviewed (rev 2), delivery decisions applied (rev 3)

## Phase 3 — Review gate
- [x] Rick reviews spec — APPROVED 2026-07-08 (large groups; both optionals; Help Desk domain; Rick = WMS submitter + QA owner)

## Phase 4 — Development (inline, strict TDD; plan tasks)
- [x] T1 Validator core — manifest load + ordering (21 unit tests total by T17)
- [x] T2 Validator — path resolution
- [x] T3 Validator — lab structural rules
- [x] T4 Validator — budget/bans/CLI (workshop went red as designed)
- [x] T5 Scaffold manifests (sandbox/tenancy/event) + index stubs + placeholder tool
- [x] T6 SQL artifacts (schema/seed/resolve-ticket) + 7-test text contract — manual ADB gate PENDING (below)
- [x] T7 Introduction lab
- [x] T8 Lab 1 connect-genai (type-conditional OCI/OpenAI, token quota beat)
- [x] T9 Lab 2 data-model-ai (review-then-run checkpoint)
- [x] T10 Lab 3 generate-app (blueprint pins Tickets IR)
- [x] T11 Lab 4 ai-interactive-report (+ app-level AI Attributes link — spec gap found & fixed)
- [x] T12 Lab 5 ai-agent (mirrors scm-ai-agent mechanics: trigger action, param grid, set_tool_result)
- [x] T13 Lab 6 generate-text (reply column moved into canonical schema)
- [x] T14 Lab 7 vector-search (in-database ONNX — track-independent, pure-SQL embedding)
- [x] T15 Take It Home — validator 0 errors all variants, --online green
- [x] T16 Event runbook (docs/event-runbook.md)
- [x] T17 Repo lint gates — official validate-livelabs-markdown.sh PASSES (caught 'Estimated Workshop Time:' rule → encoded in validator); markdownlint is advisory-only in CI
- [ ] T18 Screenshot pass (EXTERNAL: real sandbox reservation) → replace placeholders, export app zip, `--final --online` green, record timings
- [ ] T19 Self QA + WMS submission (EXTERNAL: Rick, Oracle VPN)
- [ ] T20 Clean PR branch (ai-helpdesk-agent/ only, `-s` signoff, WMS ID in PR title)

### External gates / verifications to record
- [ ] Week-1 sandbox check: OCI GenAI reachable from LiveLabs compartment; APEX version >= 26.1; Lab 7 ONNX link + grants work in sandbox
- [ ] T6 manual ADB gate: run helpdesk-schema.sql twice (state-reset), divergent-precondition test, resolve-ticket block with :TICKET_ID=42
- [ ] T18 actual lab timings vs budget (core must stay <= 90)
- [ ] Verify Lab 6 'Generate Text with AI' dynamic action config fields against the 26.1 builder during the real run (Message/Result Item names)

### T18 run log (2026-07-08)
- Reservation: "Build a Starter Online Shopping App using Oracle APEX!" (wid 848, green button), submitted 09:18 US/Central, Sandbox Lite-style (login -> create ADB + workspace in assigned compartment)
- CATALOG INTEL: nyc-genai-lab (wid 3947) and ai-vision-lab (wid 3811) currently have their green buttons DISABLED in the catalog (button present in DOM, display:none + disabled) — only 3 APEX workshops have active sandboxes today (spreadsheet, shopping-cart, movies-lab; none AI). Strengthens our gap claim AND raises the question for WMS/Jira: why were the AI-APEX sandboxes pulled? Ask LiveLabs team; GenAI-from-sandbox verification below is therefore even more load-bearing.
- T18 FINDING (quota): shopping-cart sandbox compartment has quota adb-free-count=0 -> "Always Free" ADB creation FAILS with quota error; regular (trial-credit) ADB required. ACTION: WMS Sandbox Lite request must ask for adb-free-count >= 1, AND our Get Started/sign-up guidance needs a fallback note ("if Always Free is blocked by quota, uncheck it - the sandbox trial credits cover the database"). Also: ADB create form now has a dedicated APEX workload type - consider pinning it in the sign-up lab dev-time check.
- T18 FINDING (CRITICAL, week-1 verification result): fresh sandbox ADB (26ai database, Ashburn, provisioned 2026-07-08) runs **APEX 24.2.17**, footer says "System is up-to-date" — APEX 26.1 has NOT rolled out to ADB in this tenancy/region despite GA in May. Labs 4 (NL2IR) and 5 (AI Agents + tools) are 26.1-only and cannot run as written today. Spec's documented fallback applies (24.2 "AI Configurations" chat instead of Agent+tools). Decision needed: launch as 24.2-compatible v1 vs wait for ADB 26.1 rollout.
- T18 timings so far: reservation submit->Active ~2 min; login+pw reset ~3 min; ADB create (clean path) ~2 min form + ~2 min provisioning; workspace create ~2 min. Setup labs total ~15 min clean = matches budget.

### T18 VERIFICATION RESULTS (2026-07-08, real 26ai ADB + APEX 24.2.17)
- [x] Setup labs (Get Started + sign-up): full flow works; APEX 24.2.17 not 26.1 (see finding above). Compartment quota blocks Always Free + APEX-workload ADB -> use Transaction Processing on trial credits (WMS Sandbox Lite must request adb quotas).
- [x] **T6 DB GATE — FULLY PASSED**: helpdesk-schema.sql = 83 statements / 83 successful / 0 errors. Run TWICE (idempotent). Divergent-precondition (wrong 2-col tickets + junk row 999) -> canonical schema WINS (junk gone, ticket 42 Open/Network restored, 50/20/8 counts exact). REPLY + EMBEDDING columns present. **VECTOR type compiled OK -> 26ai DB confirmed even under APEX 24.2.**
- [x] resolve-ticket core logic (SELECT subject + UPDATE Resolved) works; message exact. apex_ai.set_tool_result is 26.1-only (APEX_AI pkg exists in 24.2 but SET_TOOL_RESULT/GENERATE/CHAT procs not exposed -> Lab 5 agent tools confirmed 26.1-gated at API level too).
- [ ] Lab 1 GenAI-from-sandbox: IN PROGRESS

### T18 HEADLINE FINDING — GenAI-from-sandbox (Lab 1 verification)
Configured OCI GenAI service in APEX (Helpdesk AI, static id helpdesk_ai, us-chicago-1, model cohere.command-r-08-2024, self-generated API key). **Test Connection result: GenAI IS REACHABLE — auth OK, endpoint OK, model accepted (no 401/404)** — BUT returned:
`429: Compartment quota max-on-demand-chat-request-per-minute-count is exceeded, request is throttled for compartment`
INTERPRETATION: The plumbing works end-to-end from a LiveLabs student compartment (huge — validates the workshop's core AI mechanism on sandbox). BUT these compartments carry a per-minute on-demand-chat quota that is at or near ZERO — almost certainly WHY the AI-APEX green buttons (nyc-genai-lab, ai-vision-lab) are currently disabled in the catalog.
ACTIONS:
1. WMS Sandbox Lite / full-sandbox Jira MUST explicitly request the quota `max-on-demand-chat-request-per-minute-count` (and embed/generate equivalents) be raised for the workshop's compartments. This is now the #1 gating dependency — without it, NO AI lab runs on green button.
2. Spec 429 risk is CONFIRMED and is COMPARTMENT-level (worse than the tenancy-level we assumed) — OpenAI fallback + staggering are load-bearing, not optional.
3. Screenshot saved: scratchpad/t18-captures/genai-429-error.png

### T18 Lab 7 (in-database ONNX) finding
Lab 7 semantic search is INDEPENDENT of the GenAI chat quota (pure in-DB), so it was the best candidate to run on sandbox today. Result: DEMO schema lacks EXECUTE on DBMS_CLOUD + CREATE MINING MODEL (our Lab 7 Task 1 grants). Ran the grants as ADMIN in Database Actions ("Grant succeeded" x2) BUT verification shows DEMO still has DIRECT_PRIV=0, MINING_PRIV=0 -> the student sandbox tenancy restricts these ADMIN grants (they don't actually land). So ONNX model load (DBMS_VECTOR.LOAD_ONNX_MODEL via DBMS_CLOUD.GET_OBJECT) is BLOCKED on this sandbox. Same root cause class as the GenAI quota: LiveLabs student tenancy needs proper privilege/quota provisioning. WMS/Jira must request: DBMS_CLOUD execute + CREATE MINING MODEL grantable to workspace schemas (or pre-provisioned). CONFIRMED separately: 26ai VECTOR column type compiles fine (schema HAS_VEC=1), so only the model-load privilege is the blocker, not vector support.

### T18 teardown (2026-07-08)
- Reservation 213888 TERMINATED ("Keep in History") — workshop environment destroyed: HELPDESKDB ADB, HELPDESK/DEMO APEX workspace, self-generated OCI API key, and all compartment resources released back to the shared sandbox pool. Reservation record kept for reference.
- No persistent artifacts: workshop content + all findings are committed to git; throwaway sandbox credentials existed only in the session scratchpad (ephemeral).

### 2026-07-27 — resuming to validate full 26.1 lab; dev-env network fix
- Blocker found & being fixed: NordVPN Threat Protection (NDivert WFP driver) SNI-blocked livelabs/apex for non-browser clients on Rick's host (false-positive reputation-DB block, ~1 week old). Not WSL, not router, not DNS — proven from 6 angles. Rick disabling nordsec-threatprotection-service + nordvpn-service (StartupType Disabled) + reboot.
- ON RESUME (after reboot): verify `curl https://livelabs.oracle.com/ords/r/dbpm/livelabs/home` = 200, then reserve green-button sandbox → 26ai ADB + workspace → CHECK APEX VERSION (26.1?) → GenAI Test Connection (re-check 429 compartment chat quota) → run Lab 4 (NL2IR) + Lab 5 (AI Agent) end-to-end.

### 2026-07-28 — ✅ APEX 26.1 CONFIRMED (re-validation via agentBridge mac-agent)
- **Network root cause (final):** NOT the host — livelabs is behind **Akamai Bot Manager**; automated/CDP browsers get RST, only a genuine human browser works (bare curl → reset; curl + full Chrome headers → 302). NordVPN/Malwarebytes/NDivert all exonerated by clean-boot test. WSL drives via **agentBridge** repo (github.com/rhoulihan/agentBridge) → mac-agent w/ Claude-in-Chrome drives Rick's real Windows Chrome.
- **✅ APEX VERSION = `26.1.1`** (4-way verified: admin footer, DOM, `select version_no from apex_release`, "System up-to-date"). Was 24.2.17 on 2026-07-08. **Labs 4 & 5 unblocked.** Stack: APEX 26.1.1 / ORDS 26.2.1 / DB Oracle AI 26ai 23.26.3.1.0.
- Sandbox: res 218906, tenancy `c4u02`, **region UK South London uk-london-1** (per-reservation region — was Phoenix day before). ADB `HELPDESK` = 26ai / Transaction Processing / paid-trial (Always Free **blocked in London**: home-region rule; distinct from Phoenix adb-free-count=0).
- **Workshop-doc fixes surfaced this run:** (a) ADB create form **defaults to 19c → must select 26ai** (default flips 26ai on Sep 15 2026 per console banner); (b) ADB list **403 Forbidden** until compartment filter set to `LLxxxx-COMPARTMENT` (nested under Livelabs, not top-level); (c) green button is **one-click** — no reservation dialog / start-time / duration / terms (our doc describes a dialog that doesn't exist); (d) sandbox creds are behind **"View Login Info"** in the workshop runner, not a Get-Started step; (e) the borrowed ADB already had **1 workspace + 4 apps** pre-installed (848 content) — check collision before installing ours.
- **STILL OPEN:** GenAI **429 compartment chat-quota** re-test (req 007 in flight; tenancy-level, not fixed by 26.1) → then Lab 4 (NL2IR) + Lab 5 (AI Agent + ticket-42).

### 2026-08-28 — LOCAL 26ai CONTAINER VALIDATION (SQL layer fully green)
Rig: Podman `oracle-ai-dev` = **Oracle AI Database 26ai Free 23.26.3.0.0** (sandbox ADB was 23.26.3.1.0 — same major line).
SQLcl 26.2 + `plugin_dev` user + saved connection `dev` in the plugin's isolated store; SQLcl MCP arm wired.

- [x] **T6 DB GATE — PASSES on 26ai, matches the 2026-07-08 ADB result exactly.**
  - `helpdesk-schema.sql` run **twice**, 0 errors both times (idempotent); 0 invalid objects.
  - Counts exact: **TICKETS=50 / KB_ARTICLES=20 / TEAM_MEMBERS=8**.
  - Ticket 42 = `Open / Network / "Cannot connect to VPN - error 812 when working from home"`.
  - `EMBEDDING` column is type **VECTOR** on `KB_ARTICLES` → 26ai confirmed.
  - `resolve-ticket.sql` **core logic** verified (select subject → `UPDATE status='Resolved'`), rolled back.
    NOTE: the `apex_ai.set_tool_result` call is APEX-only and is NOT exercised here — still needs an APEX run.
- [x] **Lab 7 ONNX — UNBLOCKED AND VALIDATED (was hard-blocked on the LiveLabs sandbox).**
  - Model loaded via `DBMS_VECTOR.LOAD_ONNX_MODEL` from a local directory object — `ASSERT:embedding_model:PASS`.
  - Loaded a second copy under the workshop's exact name **`MINILM_L12`** so lab SQL runs verbatim.
  - **`embed-kb.sql` run verbatim → `20 rows updated`, `EMBEDDED=20`.**
  - Semantic search proven: query *"I cannot connect to the VPN from home"* →
    1. `Installing and updating the VPN client` (0.386)
    2. `Fixing VPN Error 812: remote access policy mismatch` (0.481)  ← the correct article for ticket 42
    3. `Wi-Fi shows connected but no intranet` (0.653)
  - ⚠️ **Workshop-doc gap:** Lab 7 Task 2 loads the model via `DBMS_CLOUD.GET_OBJECT`, which is an **ADB-only**
    package — that exact SQL cannot run on a local/non-ADB database. A local path needs a directory object +
    `LOAD_ONNX_MODEL` instead. Fine for the ADB-targeted variants; must be conditionalised if a local variant ships.

### Still to validate (needs a real APEX 26.1)
- [ ] Labs 1, 3, 4, 5, 6 — APEX Builder UI (Create-App-from-prompt, NL2IR, AI Agent + tools, Generate Text)
- [ ] `apex_ai.set_tool_result` inside a real Lab 5 agent tool
- [ ] T18 screenshots (39 placeholders remain; `--final` gate red until replaced)

### Environment gotchas found this run
- oracle-ai-dev plugin: optional `tns_admin` interpolates to an **empty string** in `.mcp.json` when unset →
  MCP `connect` fails with **ORA-17869**. Fix: set `pluginConfigs["oracle-ai-dev@oracle-ai-dev-marketplace"].tns_admin`
  to a real directory. (Set in `~/.claude/settings.json`; needs a Claude restart.)
- Homebrew JDK is keg-only, so the MCP child sees only macOS's `/usr/bin/java` stub → SQLcl won't start.
  Fix: `sudo ln -sfn /opt/homebrew/opt/openjdk/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk.jdk`.
- The plugin's ONNX configurator names the model `ALL_MINILM_L12_V2`; the workshop expects `MINILM_L12`.

### 2026-08-28 (evening) — PAUSED: OCI-side issues. Resume in the morning.

**Stop reason:** OCI was having problems. The first `HELPDESK` ADB create wedged at exactly **18%** for ~25 min
(work request `In progress`, only two log lines both stamped at start, **zero errors**) — consistent with an
OCI-side fault rather than anything wrong with our config.

**State left behind (tenancy `crhsentllc`, region `us-phoenix-1`):**
- `HELPDESK` — **Terminating** (Rick authorised terminate + retry Always Free). May be gone by morning.
- `WMAustin` — **Available**, untouched. ⚠️ Rick's existing JSON DB — never terminate it.
- Always Free allows **2 ADBs**; `WMAustin` holds one slot, so a recreate needs the old one fully released.

**To recreate `HELPDESK`** (Create Autonomous AI Database):
- Display name + Database name: `HELPDESK`
- Compartment: **`crhsentllc (root)`** — NOT `wavemax-prod`
- Workload: Transaction Processing · Always Free: **ON**
- ⚠️ **Database version: `26ai`** — the form defaults to `19c`
- Network access: default (Secure access from everywhere)
- **Rick sets the ADMIN password** and clicks Create.

**⭐ Key result banked today — the tenancy GenAI quota:**
| Scope | `max-on-demand-chat-request-per-minute-count` |
|---|---|
| LiveLabs green-button compartment | effectively **0** (429 on first request) |
| **`crhsentllc` root, us-phoenix-1** | **500** (embed: 1,000) |

So **no OpenAI key is needed** — Labs 1/4/5/6 can be validated on the workshop's documented **OCI GenAI**
track. Caveat: a *service limit* of 500 does not rule out a compartment **quota policy** narrowing it; the
real proof is Lab 1 `Test Connection`. Also reframes the LiveLabs ask: 500/min looks like stock default, so
their compartments are provisioned far *below* default, not merely conservatively.

**Next session, in order:**
1. Recreate `HELPDESK` (config above) → wait for Available.
2. Confirm APEX is **26.1.x** (Tool configuration tab shows NO versions — use Database actions / APEX admin footer).
3. Create the APEX workspace (Rick sets the workspace password; schema will auto-prefix to `WKSP_*`).
4. **Lab 1 → Test Connection on OCI GenAI** — the real quota proof.
5. Then Labs 4 & 5 (never yet run end-to-end), Lab 6, and T18 screenshots (39 placeholders keep `--final` red).

**Also outstanding (non-blocking):** WMS `12192` still has both GitHub URL fields empty. Verified live today:
dev URL returns **200** (all 3 variants); prod URL 404s, which is expected until the T20 PR merges.

## 2026-08-30 — ADB up in crhsentllc; Lab 1 walkthrough on APEX 26.1.4

**Environment (Rick's own tenancy, NOT a LiveLabs sandbox):**

| | |
|---|---|
| ADB | `HELPDESK` · Available · **26ai** · Transaction Processing · Always Free |
| Compartment | `crhsentllc (root)` · region `us-phoenix-1` |
| OCID | `ocid1.autonomousdatabase.oc1.phx.<redacted>` (in Rick's OCI console) |
| APEX | **26.1.4** (DOM-confirmed from admin footer) — note: LiveLabs sandbox was **26.1.1** |
| Workspace | `HELPDESK` · admin `helpadmin` · 0 apps / 0 tables at start |
| APEX URL | `https://<adb-host>.adb.us-phoenix-1.oraclecloudapps.com/ords/apex` (redacted; from Tool configuration tab) |

**Confirmed still true on 26.1.4:**
- 8 AI providers, unchanged list: OCI_GENAI, OPENAI, COHERE, GEMINI, CLAUDE, MISTRAL, OLLAMA, GENERIC_OPENAI.
- OCI GenAI requires the **full API key** (OCI User ID + Private Key + Tenancy ID + Fingerprint), all mandatory.
  Credential dropdown offers only `- Create New -`. **No resource-principal option even on an ADB in your own
  tenancy** — so this is a property of APEX, not of LiveLabs sandboxes.
- Base URL defaults to **us-chicago-1**; Model ID defaults to `cohere.command-a-03-2025`.
- Documented nav path `App Builder > Workspace Utilities > Generative AI` is still correct.
- The ADB credential gateway fronts `/ords/apex` and **accepts an APEX workspace user** (`helpadmin`),
  not just a database user. Second confirmation; the July prediction that it would reject one was wrong.

**NEW workshop-text findings (Lab 1):**

1. **Model ID "list" does not exist.** Lab 1 Task 2 says *"Model ID: pick the latest available chat model
   from the list"*. `P9801_OCI_MODEL_ID` is `INPUT type=text` with no datalist — a free-text field
   pre-filled with `cohere.command-a-03-2025`. Reword: the reader must TYPE an exact model ID, and needs
   a pointer to where the current list of model IDs is published.

2. **OCI Console menu drift.** Lab 1 Task 1 step 1 says *"click Profile ... and select your username"*.
   The Profile menu has no username entry; the item is **`User settings`**, which lands on My profile →
   **Tokens and keys** tab (tab name in the lab is correct).

3. **Root-compartment shortcut is undocumented.** Task 1 step 5 sends the reader to Identity & Security >
   Compartments for the compartment OCID. When running in a personal tenancy's ROOT compartment, the
   compartment OCID IS the tenancy OCID already present in the Configuration File Preview. Worth a note
   for the tenancy variant of the workshop.

4. **⚠️ Region vs quota mismatch — needs resolving.** Lab 1 pins Region `us-chicago-1`. Our measured
   500/min chat quota for `crhsentllc` was read in **us-phoenix-1**. OCI service limits are per-region,
   so Chicago headroom is unverified. Testing Chicago first as the lab is written; fall back to Phoenix
   if it 429s and document whichever is required.

**NOT a finding (checked and retracted):** `Used by App Builder` defaulting OFF *is* already documented,
with a callout naming it "the most commonly missed step in this lab." No change needed.

**State at pause:** Generative AI create form staged with Name `Helpdesk AI`, Static ID `helpdesk_ai`,
Region `us-chicago-1`, Max AI Tokens `500000`, Used by App Builder ON. Blocked on Rick supplying the OCI
API key + compartment OCID (agent does not handle key material). Next action after that: **Test Connection**.

### Lab 1 OCI GenAI — root cause found (2026-08-30, tenancy track)

**Test Connection results, in order, all verbatim:**

1. Region `us-chicago-1` (as Lab 1 specifies), model `cohere.command-a-03-2025` (APEX default):
   `ORA-20955: Authentication error or forbidden access (HTTP-401) for URL
   https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/20231130/actions/chat.
   Please check the configuration of Generative AI Service helpdesk_ai.`
2. Region `us-phoenix-1`, same model: `Bad Gateway` (transient), then
   `HTTP-404: 404: Entity with key cohere.command-a-03-2025 not found`
3. Region `us-phoenix-1`, model `cohere.command-r-plus-08-2024` (taken from the Phoenix console model list):
   `HTTP-404: 404: Entity with key cohere.command-r-plus-08-2024 not found`
4. OCI Console GenAI Chat playground, Phoenix, same model: generic `Error` toast.

**ROOT CAUSE — the tenancy is subscribed to ONE region.** Verbatim from the OCI region menu:
`You're subscribed to only one region. Subscribe to additional regions to ensure availability if a
regional outage occurs.` Region Management confirms `US Midwest (Chicago) / us-chicago-1 / Not subscribed`.

- Chicago 401 = not subscribed to that region.
- Phoenix 404 on EVERY model = Phoenix does not serve these models on-demand; the console's model list is
  catalog metadata, not proof of regional on-demand availability. Endpoint column is `—` for all 9 models.

**KEY POSITIVE FINDING:** the Phoenix 404 proves the request AUTHENTICATED and reached the GenAI service —
the API key works and there is **NO 429 / compartment-quota throttle** in `crhsentllc`. That is the wall
that made every LiveLabs green-button sandbox unusable, and it is absent here.

**⚠️ NEW HIGH-PRIORITY WORKSHOP FINDING (tenancy variant):**
Lab 1 pins Region `us-chicago-1` but never tells the reader their tenancy must be SUBSCRIBED to a
GenAI region. An unsubscribed reader gets an opaque HTTP-401, and Lab 1's troubleshooting note
(*"re-check the region spelling (us-chicago-1, exactly)"*) actively misdirects them toward a typo they
do not have. The tenancy track needs an explicit pre-step: Profile > Regions > Manage regions >
subscribe to a GenAI region. Note region subscriptions appear to be permanent (add-only).

Chat models offered in us-phoenix-1 (for reference; none served on-demand):
cohere.command-r-plus-08-2024, google.gemini-2.5-flash / -flash-lite / -pro,
xai.grok-4.20-0309-non-reasoning / -reasoning, xai.grok-4.20-non-reasoning / -reasoning, xai.grok-4.3

**Also confirmed:** APEX `Model ID` is free text with NO list (26.1.4), so Lab 1's "pick from the list"
wording is wrong, and the reader has no in-product way to discover valid IDs — they must go to the OCI
Console GenAI playground model picker. Worth documenting explicitly.

**Next:** Rick subscribing to us-chicago-1; then set Region back to us-chicago-1 + Model
cohere.command-a-03-2025 and re-run Test Connection (Lab 1 exactly as written).

### ⭐ Lab 1 PASSED on the OCI GenAI track (2026-08-30)

**`Connection Succeeded!`** — then `Create` → `Changes applied.` Service is live in the workspace:

| Name | Static ID | Provider | Base URL | Model | Used by App Builder |
|---|---|---|---|---|---|
| Helpdesk AI | `helpdesk_ai` | OCI Generative AI Service | `https://inference.generativeai.us-chicago-1.oci.oraclecloud.com` | `cohere.command-a-03-2025` | Yes |

Max AI Tokens `500000` (Lab 1 Task 3). Compartment = tenancy root OCID.

**THE HEADLINE — the July blocker is resolved on a real tenancy.** There is NO 429
`max-on-demand-chat-request-per-minute-count` throttle in `crhsentllc`. The OCI GenAI path documented in
Lab 1 works exactly as written, with the region caveat below. **No OpenAI key is required** to run this
workshop on a tenancy with a subscribed GenAI region. (The green-button sandbox quota question is still
open and unchanged — that remains a LiveLabs provisioning ask.)

**Sequence that got there, for the record:**
Chicago 401 (not subscribed) → Phoenix 404 on every model (region serves none on-demand; this 404 is what
PROVED the key authenticates) → Rick subscribed `us-chicago-1` → still 401 for ~5 min (identity
replication lag) → succeeded on the next 5-minute retry with Lab 1's documented values restored.

**Confirmed Lab 1 doc fixes needed (tenancy track), in priority order:**
1. **Add a region-subscription pre-step.** Lab 1 pins `us-chicago-1` but never says the tenancy must be
   subscribed to it. Symptom is an opaque HTTP-401, and the existing troubleshooting note
   (*"re-check the region spelling"*) misdirects. Add: Profile > Regions > Manage regions > subscribe.
   Note subscriptions appear to be permanent (add-only).
2. **Add "wait a few minutes after subscribing."** A freshly subscribed region returns 401 until IAM
   identity replication completes (~5 min observed). Without this note a reader will assume bad credentials
   and start regenerating API keys.
3. **Fix "pick the latest available chat model from the list."** APEX's Model ID is free text with NO list.
   Point readers at OCI Console > Generative AI > Chat playground > model picker, and warn that model
   availability is REGION-SPECIFIC (`cohere.command-a-03-2025` exists in Chicago, not Phoenix).
4. **Fix "click Profile and select your username"** → the menu item is `User settings`.
5. **Note the Add button is disabled until Download private key is clicked** in the Add API key dialog.
6. **Root-compartment shortcut:** in a personal tenancy's root compartment, Compartment ID = the tenancy
   OCID already in the Configuration File Preview; no trip to Identity & Security > Compartments needed.

**Next:** Lab 1 Task 4 — SQL Workshop > SQL Commands > APEX Assistant, ask for a query showing today's
date in three formats, Insert and run.

### ⭐ Lab 2 PASSED — no doc changes required (2026-08-30)

Ran all three tasks as written on APEX 26.1.4 / ADB 26ai, workspace HELPDESK, schema `WKSP_HELPDESK`.

| Task | Result |
|---|---|
| 1 — Describe the data model to AI | ✅ `SQL Workshop > Utilities > Create Data Model Using AI` path is correct. Lab's verbatim prompt produced a full 3-table Oracle SQL model in **~50 s**. |
| 2 — Review, do not run | ✅ `Create SQL Script` button confirmed present in the wizard, so the lab's claim that the final step *saves* rather than runs is **accurate**. Closed without running. |
| 3 — Canonical schema + seed | ✅ Uploaded 25,834 bytes / **83 statements**, ran to Status `Complete`. |

**Verification query result — every assertion exact:**

| TICKETS | KB_ARTICLES | TEAM_MEMBERS | ticket 42 | VECTOR col on KB_ARTICLES |
|---|---|---|---|---|
| 50 | 20 | 8 | `Open/Network` | 1 |

Matches the local Podman 26ai container run (T6 gate) exactly — **the schema behaves identically on ADB 26ai
and on 26ai Free**, which retires the risk that the container validation wasn't representative.

**Observations (recorded, no doc change made):**
- The AI's proposal diverged from canonical in ways that make Task 2's review beat land well: `it_`-prefixed
  table names, unrequested audit columns (`created_by`, `updated_on`, `row_version`), `varchar2(255)` for
  nearly everything, and a lowercase status CHECK (`'open','in progress','resolved','closed'`) vs the
  canonical `Open`. Deliberately NOT hard-coded into the lab — AI output varies per run, so promising
  specifics would age badly. Useful as instructor talking points.
- `Create Data Model Using AI` is the LAST tile on the Utilities page and needs scrolling at 1512px width.
  Minor; not worth a doc change unless a screenshot makes it look top-of-page.
- The AI terms dialog did NOT reappear — confirms the "once per workspace" wording added to Lab 1.

**Agent tooling limit (not a workshop issue):** the Upload Script file input lives in an iframe that the
accessibility tree cannot reach, so `file_upload` has no element ref and the agent cannot attach the file.
Rick performed the Choose File step. Any future automated run of Lab 2 Task 3 needs the same hand-off, or
should use `SQL Scripts > Create` and paste the script instead.

**Next:** Lab 3 — Generate the App from a Prompt.

### ⭐ Lab 3 — prompt rewritten from a written contract, then validated (2026-08-30)

**New artifact: `docs/specs/horizon-help-desk-app-contract.md`** — C1–C7, the minimum the generated app
must satisfy for Labs 4–6. Lab 3's prompt is derived from it and Lab 3 Task 2 verifies against it.

**Contract derived from what Labs 4–6 actually reference:**
- Lab 4 → a page named **Tickets** with an **Interactive Report** region (AI features exist ONLY on IR).
- Lab 5 → **Page 1 must be the Dashboard**, with a Breadcrumb Bar (the `ASK_THE_ANALYST` button goes there).
- Lab 6 → an editable **ticket form** page; ticket **27** (seeded).

**Two runs — the first one failed the contract, and that is the finding.**

*Run 1 (4-page prompt: Dashboard / Tickets / Ticket / Knowledge Base)* → app 101 came out with
**SIX pages including TWO both named "Tickets"** (pages 2 and 4) and two ticket forms (3 and 5).
Listing the report and its form as separate numbered pages makes the wizard build **two report+form
pairs**. Lab 4 says "open the Tickets page" — a reader would face two. App 101 deleted (Rick approved).

*Run 2 (corrected 3-page prompt, report+form as ONE entry)* → app **102**, clean:

| Page | Name | Alias | Type |
|---|---|---|---|
| 1 | Dashboard | home | Home |
| 2 | Tickets | tickets | Interactive Report |
| 3 | Ticket | ticket | DML Form |
| 4 | Knowledge Base | knowledge-base | Report |

**Lab 3 doc changes applied:**
1. **Prompt rewritten** — 3 page entries, report+form as one, Dashboard pinned as home page,
   "Interactive Report" named explicitly, "do not create any additional pages".
2. **Nav label fixed** — `App Builder > Create` then **`Create App Using Generative AI`**. The old text
   said "Create App with AI (labelled *Generate with AI* on some screens)"; neither string exists in 26.1.4.
3. **Two-stage blueprint explained** — `Create Application` in the chat does NOT create anything; it opens
   the Create Application wizard, which is the editable blueprint. The chat lists pages only.
4. **Task 2 rewritten** as a 6-row checklist keyed to the contract, incl. "there is only ONE page named
   Tickets", and how to verify the charts (Dashboard > Edit > Chart 1 / Chart 2 tabs).
5. Added a callout explaining WHY item 2 of the prompt pairs report+form.

**⚠️ Key behavioural finding — the AI renames pages even when the prompt names them explicitly.**
Run 2's first blueprint returned `Help Desk Overview` and `Manage Tickets` instead of `Dashboard` and
`Tickets`. A one-line conversational correction ("must be named exactly ...") fixed it. **This is why
Task 2's name checks are mandatory, not optional** — a prescriptive prompt reduces variance but does not
eliminate it.

**Verified in the wizard before creating (C6):** Dashboard > Edit exposes Chart 1 `Tickets by Status`
(Bar, TICKETS, label STATUS, Count) and Chart 2 `Tickets by Category` (Pie, TICKETS, label CATEGORY,
Count). Region-level detail is visible ONLY in the wizard — the chat blueprint summary never shows it.

**App settings:** ID **102**, schema `WKSP_HELPDESK`, Authentication `Oracle APEX Accounts`,
Appearance `Iris, Side Menu`, features `Install Progressive Web App` + `Push Notifications`
(added by the AI unprompted; harmless, not pages).

**Next:** Lab 3 Task 3 — Run Application and sign in; then Task 4 tour; then Lab 4.

### Lab 5 — Tasks 1-4 complete (2026-08-30), agent + 3 tools built

**Agent `Help Desk Analyst`** (static ID `help-desk-analyst`) in app 102, Service `Helpdesk AI`
(`xai.grok-4.3`), system prompt + welcome message per the lab. Tools:

| Tool | Type | Execution Point |
|---|---|---|
| `get_tickets` | Retrieve Data | On Demand |
| `get_kb_articles` | Retrieve Data | On Demand |
| `resolve_ticket` | Execute Server-side Code | On Demand (forced) |

`resolve_ticket` has parameter `TICKET_ID` / NUMBER / Required, the canonical PL/SQL block, and
User Approval: Confirmation Title `Confirm Ticket Resolution`, Message `Mark ticket &TICKET_ID. as
Resolved?`, Approve `Resolve`, Cancel `Cancel`.

**Lab 5 observations to implement:**

1. **`Execution Point` is READ-ONLY for `Execute Server-side Code`** — it is forced to `On Demand`.
   Lab 5 Task 4 lists it as something you select. Reword to "note that Execution Point is fixed at
   On Demand for this type".
2. **`Requires Confirmation` already defaults ON** for Execute Server-side Code tools. Lab says
   "Toggle **On**". Reword to "confirm it is On (it defaults on for this tool type)". Worth calling out
   as a *good* Oracle default that supports the governance story.
3. **The Tools section does not exist until the agent is created.** Create the agent first, then reopen
   it to add tools — which is the order the lab already uses, but the lab should say why.
4. **Parameters use an editable grid** — a single click only selects the row; you must **double-click** a
   cell to type in it. Non-obvious and cost time here.
5. **The PL/SQL editor auto-indents as you type**, so retyping the block by hand produces cascading
   indentation. Harmless in PL/SQL, but the lab should tell readers to **paste** (or use the linked
   `resolve-ticket.sql`), not retype.
6. Page title is **`Generative AI Agents`**, not "AI Agents"; the tool form's security banner is worth
   quoting for governance: *"On Demand tools are called by the AI Service. Validate all inputs and return
   only necessary data, excluding untrusted data that could enable prompt injection."*

**Next:** Task 5 (embed via ASK_THE_ANALYST button on page 1) and Task 6 (the payoff conversation).

### ⭐ Lab 5 PASSED end to end (2026-08-30) — the agent resolved ticket 42

Full payoff conversation on `cohere.command-a-03-2025`:

1. Quick-action chip → agent called `get_kb_articles` → *"Yes, there is a KB fix for VPN Error 812...
   remote access policy mismatch... changing the authentication method in the VPN client."*
2. *"Are there open tickets about it?"* → `get_tickets` → **Ticket 27** and **Ticket 42**, the exact two
   the lab predicts (27 is Lab 6's Draft Reply ticket).
3. *"Resolve ticket 42"* → **`Confirm Ticket Resolution` / "Mark ticket 42 as Resolved?" / Cancel + Resolve**
   → approved → green toast **`Ticket 42 resolved.`** → agent: *"Ticket 42 has been resolved."*
4. **Database verified**: `select id, status from tickets where id in (27,42)` →
   `27 = Open`, `42 = Resolved`. The write was real and correctly scoped.

`&TICKET_ID.` substitution worked in the confirmation message. `apex_ai.set_tool_result`'s
`p_notification_message` produced the success toast exactly as the lab describes.

**Doc fixes IMPLEMENTED in Lab 5:** different-model warning + comparison table; Execution Point is
read-only for Execute Server-side Code; Requires Confirmation defaults ON (reframed as Oracle's own
governance default); Parameters grid needs a double-click; paste the PL/SQL rather than retyping
(editor auto-indents); the Breadcrumb Bar region is named after the app on page 1, not "Breadcrumb";
Tools tab only exists after the agent is created.

**Not drift after all:** Quick Actions really are labelled `Message 1` / `Message 2` — an earlier note
to the contrary was from a truncated filter view and is withdrawn.

**Next:** Lab 6 (Draft Replies with AI, uses ticket 27) and Lab 7 (Vector Search — already proven on the
local container; needs ONNX model load on ADB).

### ⭐ Lab 6 PASSED (2026-08-30) — AI drafted a reply on ticket 27

Ticket 27 ("VPN error 812 on my new laptop", Open/Medium/Network/Marcus Webb) opened as a drawer from the
Tickets report; **Draft Reply with AI** produced, into the Reply textarea:

> *"Thanks for reaching out. Error 812 typically indicates an issue with the VPN authentication process.
> Here's how you can troubleshoot this on your new laptop: 1. **Check VPN Credentials**: Ensure you're
> using the correct username, password, and any required authentication details..."*

Model in use: `cohere.command-a-03-2025` (left from Lab 5). **Generate Text With AI is a plain completion,
not tool calling, so it works on any of the models tested** — unlike Labs 4 and 5.

**Doc fixes IMPLEMENTED in Lab 6:**

1. **`Create Dynamic Action` → `Create Trigger Action`.** For a *button*, the context menu offers Trigger
   Action; there is no "Create Dynamic Action" entry. (Lab 5 already had this right — the two labs
   disagreed with each other.)
2. **The action is spelled `Generate Text With AI`** (capital W).
3. **🔴 The biggest one — `Message` / `Result Item` do not exist.** The real UI is
   **`Input Value` → Type `Item` → Item** and **`Use Response` → Type `Item` → Item**. They are item
   *pickers*: you supply `P3_DESCRIPTION`, **not** `&P3_DESCRIPTION.`. The old wording would send a reader
   hunting for a text field that isn't there, and typing substitution syntax that isn't accepted.
4. **Task 1 reframed** — the generated form already has a Reply item (because `REPLY` shipped in the Lab 2
   schema), so Synchronize Columns is the fallback, not the main path. Also names the page: with the Lab 3
   prompt the ticket form is page 3 `Ticket`, rendered as a drawer.

**Item naming note:** the lab's `&P6_*` examples are now `P3_*` and the text says the prefix depends on
which page the form landed on, which is honest and stays true if the generator numbers pages differently.

**Next: Lab 7** — Vector Search. Already proven on the local Podman 26ai container (ONNX load,
20/20 embedded, correct semantic hit). On ADB it needs `DBMS_CLOUD` + `create mining model` grants as
ADMIN, then the ONNX model load.

### 🔴 Lab 7 BLOCKED (2026-08-30) — Oracle changed how it ships the ONNX model

**Task 1 (grants): validated, with a real gotcha.** Confirmed necessary — as `WKSP_HELPDESK` the ONNX load
fails `PLS-00201: identifier 'DBMS_CLOUD' must be declared`. Also found that in Database Actions the green
▶ runs only the statement under the cursor: the first attempt granted `CREATE MINING MODEL` but not
`DBMS_CLOUD`, and the resulting failure looks identical to not having run the grants at all. Lab now tells
readers to use **Run Script / F5**.

**Task 2 (load the model): cannot work as written.**
- Lab's URI → `ORA-20401: Authorization failed for URI` (PAR expired, bucket moved).
- Oracle's current page (via the stable docs lookup) publishes **only `_augmented.zip`** for every model.
  No bare `.onnx` exists any more. Confirmed by fetching the page and by a direct DB attempt at a bare
  `.onnx` name in the new bucket (also ORA-20401).
- Downloaded and inspected the zip: HTTP 200, 122,537,890 bytes, containing
  `all_MiniLM_L12_v2.onnx` at **133,322,334 bytes (~127 MB)**, dated 2025-10-30.
- The database cannot unzip; `DBMS_VECTOR` has **no cloud loader** (only LOAD_ONNX_MODEL, DROP_ONNX_MODEL,
  INMEMORY_ONNX_MODEL); and the ADB has **no pre-loaded model** (`all_mining_models` is empty).

**IMPLEMENTED in Lab 7:** a prominent KNOWN ISSUE callout with the verbatim error, the stable docs-lookup
link for finding the current model, the download/unzip/host procedure, and "never hard-code a PAR".
Prerequisites now state that ADMIN access and a way to host a ~127 MB file are required.

**NEEDS A DECISION (see docs/validation-findings-open.md #12):** host the model ourselves in a
LiveLabs-owned bucket (most reliable for readers), require a reader-owned bucket, try APEX Static Workspace
Files (127 MB may exceed the upload limit — untested), or re-scope the lab away from in-database embedding
(which would cost the "nothing left the database" governance point).

**Tasks 3-5 remain unvalidated on ADB** — they are blocked behind Task 2. Note the SQL itself is already
proven on the local Podman 26ai container (ONNX loaded as MINILM_L12, 20/20 embedded, correct semantic
hit), so what is unproven is specifically the ADB model-sourcing path plus the Vector Provider and Search
Configuration UI.

### ⭐⭐ Lab 7 PASSED end to end on ADB via a tenancy-owned bucket (2026-08-31)

The last unvalidated part of the workshop. Full chain proven on APEX 26.1.4 / ADB 26ai:

| Step | Evidence |
|---|---|
| Grants (Task 1) | `DBMS_CLOUD` + `CREATE MINING MODEL` to `WKSP_HELPDESK` |
| Bucket | `workshop-models`, namespace `ax2feb9jcdu9`, `crhsentllc (root)`, Phoenix, **Private** |
| Upload | `all_MiniLM_L12_v2.onnx`, **127.15 MiB** |
| PAR | **Object**-scoped, **Permit object reads** only (least privilege) |
| Load (Task 2) | `Statement processed. **11.51 seconds**` |
| Model registered | `MINILM_L12` / `ONNX` / `EMBEDDING` in `user_mining_models` |
| Embed (Task 3) | `**20 row(s) updated**` in 2.55 s; `EMBEDDED = 20` |
| Vector Provider (Task 4) | `KB MiniLM` / `kb_minilm` / Database ONNX Model / `MINILM_L12` |
| Search Config (Task 4) | `Oracle AI Vector Search` on `KB_ARTICLES`, EMBEDDING/TITLE/CONTENT |
| Search page (Task 5) | page 5 `Ask the Knowledge Base` |
| **Semantic search** | `email box is jammed` → **`Mailbox is full: fixing email quota issues`** first. Zero keyword overlap. |

**Measured relevance (cosine distance, 20-article corpus):**

| Query | Top hit | Distance | Verdict |
|---|---|---|---|
| `email box is jammed` | Mailbox is full: fixing email quota issues | .4674 | ✅ ideal demo |
| `laptop won't connect from hotel wifi` | Wi-Fi shows connected but no intranet | .5711 | ⚠️ **not** the VPN 812 article the lab promises |
| `screen keeps blinking` | Triage steps for a slow laptop | .6982 | ❌ weak — no display article existed |
| `vpn error 812` | Fixing VPN Error 812 | .2553 | ✅ but keyword overlap, so a poor "meaning" demo |

**Lab 7 doc fixes to implement:**
1. 🔴 **The headline expected result is wrong.** `laptop won't connect from hotel wifi` does not return the
   VPN 812 article. Fixed at the data layer instead of by rewording — see seed expansion below.
2. `screen keeps blinking` had no matching article. Also fixed by seed expansion.
3. **Vector Providers is directly under Workspace Utilities** — there is no "All Workspace Utilities" step.
4. Search type is **`Oracle AI Vector Search`**, not "Oracle Vector Search".
5. **Search Page lives under the `Component` tab** of Create a Page; the dialog now opens on a
   `Generative AI` tab.
6. **Static ID auto-fills from Name.** Typing appends to it — we produced `kb-minilmkb_minilm` before
   noticing. Tell readers to clear the field first.
7. ONNX Model Owner defaults to **`- Current Parsing Schema -`**, simpler than naming the schema.
8. **Bearer-credential warning** (Rick): a PAR URL is a credential — anyone holding it can read the object
   until it expires. Use Object scope + reads only, never share it, and note the console's own warning
   that the URL is shown once.
9. **Teardown step** (Rick): delete the PAR and the bucket object when finished.

### Seed data expanded 20 → 30 KB articles (2026-08-31)

Targeted, not bulk. Chosen to close real coverage gaps AND make the documented demo queries land:

`Monitor flickers or goes black intermittently` (fixes `screen keeps blinking`) ·
`Connecting on public or hotel Wi-Fi (captive portals)` (**makes the lab's own hotel-wifi query correct**) ·
`Setting up work email on a personal phone` · `Account locked after too many sign-in attempts` ·
`Printer produces blank, faded, or streaked pages` · `Files are not syncing to cloud storage` ·
`Bluetooth headset will not connect for calls` · `Laptop runs hot and the fan never stops` ·
`Browser blocks a download or warns the site is not secure` · `Requesting a paid software license`

**Why 30 and not 100:** Lab 5's `get_kb_articles` tool sends `id, title, content, category` for every row
to the agent as context on every turn. A large corpus inflates every agent call and eventually breaks it.
30 keeps the agent payload modest while giving vector search enough coverage to be convincing.

**Ripples to re-verify:** `20` is asserted in Lab 2 Task 3, Lab 7 Task 3, the app contract, and
`tools/test_sql_contract.py`. All must move to 30, then re-run schema + re-embed + re-measure.

### Rebuild checks queued from the 2026-08-30 capture pass

- [ ] **Search Configuration label case.** Lab 7 tells the reader to enter `KB Semantic Search`; the stored
      Label reads `Kb Semantic Search`. Unresolved whether APEX title-cases the field or the original run
      typed it that way. On the rebuild, type `KB Semantic Search` exactly and observe what is stored — if
      APEX normalises it, say so in the lab so the reader is not thrown when picking the configuration in
      the Create Page dialog (Lab 7 Task 6 refers to it by the un-normalised name).
- [ ] **`object-browser-tables.png`** must be captured *before* Lab 7 runs, so it shows only the three
      seeded tables and not the four `DM$P*MINILM_L12` model tables.

### Teardown for the clean-room rebuild (2026-08-31)

Rick approved a content reset (workspace and ADB kept). Executed and verified:

| Step | Result |
|---|---|
| App 102 `Horizon Help Desk` | deleted — "Application 102 deleted." |
| Search Configuration `Kb Semantic Search` | went with the app (app-scoped, not workspace-scoped) |
| Vector Provider `kb_minilm` | deleted |
| Generative AI service `helpdesk_ai` | deleted — "No AI Services configured in this workspace." |
| `MINILM_L12` ONNX model + `TICKETS`/`KB_ARTICLES`/`TEAM_MEMBERS` | dropped via one PL/SQL block; `user_objects` returns **no data found** for all four names and the `DM$` tables |
| OCI bucket PAR + `.onnx` object | **done** — Rick deleted the bucket; OCI's Delete-bucket panel cascades, and it listed Pre-authenticated requests(1) and Objects(1), confirming both were still live. Buckets list in `crhsentllc (root)` / Phoenix now reads "No items to display". |

Captured `genai-create.png` from the resulting empty state (success banner dismissed first, so the
image shows what a Lab 1 reader actually sees).

**Two behaviours worth knowing, both observed here:**

1. **Deleting a Generative AI service does NOT delete its Web Credential.** `Credentials for helpdesk ai`
   (`credentials-for-helpdesk-ai`, OCI Native Authentication) survived. Good news for the rebuild — Lab 1
   can select the existing credential rather than re-pasting the private key. It also means a reader who
   "removes" the service still has OCI key material stored in the workspace.
2. **Deleting an APEX application leaves its push-notification credential behind.** Both
   `App 101 Push Notifications Credentials` and `App 102 Push Notifications Credentials` are still
   present, app 101 having been deleted long ago. Harmless, but it is real debris a tidy teardown misses.

3. **CORRECTION to (1): a surviving Web Credential cannot be reused for a new Generative AI service.**
   On the Create form the **Credential** list offers only `- Create New -`, even after an explicit
   `apex.item(...).refresh()`, and even though `Credentials for helpdesk ai` (OCI Native Authentication)
   still exists at workspace level. So deleting a GenAI service *does* strand its credential: the key
   material stays in the workspace but is not offered back to you, and rebuilding means pasting the
   private key again. This matches the original 2026-07-28 finding that the dropdown offers only
   "- Create New -" with no resource-principal option.

**Teardown verified on both sides.** Database: `user_objects` returns no rows for `TICKETS`, `KB_ARTICLES`, `TEAM_MEMBERS`, `MINILM_L12` or the `DM$` tables. OCI: no buckets remain in the root compartment. The workspace keeps `Credentials for helpdesk ai`, so Lab 1 can reuse it rather than
re-pasting the private key.

> **Console note:** the Object Storage deep link `…/buckets/<ns>/<bucket>/objects?region=…` rendered
> as an empty skeleton with stray numeric tabs. Navigating from **Storage > Buckets** worked. Lab 7
> already tells readers to go via the console menu, so no lab change is needed — but do not "helpfully"
> replace that with a deep link.

### Rebuild — Lab 1 re-run (2026-08-31), clean workspace

Walked as written on APEX 26.1.4. Confirmed live, matching the lab text:

- Create form defaults: Model ID `cohere.command-a-03-2025`, Base URL Chicago, **Used by App Builder OFF**.
  All three are exactly what Lab 1 warns about.
- Provider list is the documented 8 (OCI GenAI / OpenAI / Cohere / Gemini / Claude / Mistral / Ollama /
  Generic).
- `Test Connection` **succeeded on `xai.grok-4.3`** — no per-model 429 at this time, so Lab 4 should run.
- `Maximum AI Tokens` is under **Advanced** (item `P9801_AI_MAX_TOKENS`), as now documented.
- Turning on **Used by App Builder** is what puts the **APEX Assistant** button in the SQL Commands
  toolbar — the lab's "most commonly missed step" claim holds.
- The Assistant answered the lab's prompt and the inserted query ran: `31-AUG-2026`, `2026-08-31`,
  `31/08/2026`.

**Two new defects found and fixed in Lab 1:**
- Static ID **auto-fills with a hyphen** (`helpdesk-ai`) from the Name, but the lab requires
  `helpdesk_ai` and the field locks after Create.
- `Default for New Apps` is **ON by default**, so "toggle ON" was wrong; it now says "leave it ON".

**Not re-verifiable this run:** Task 4's third-party AI terms dialog did not appear. Acceptance is once
per workspace and we deliberately kept the workspace, so this is expected — *not* evidence the step is
wrong. It needs a genuinely new workspace to re-confirm.
