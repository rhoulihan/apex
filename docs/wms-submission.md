# WMS Submission Package — AI Help Desk Workshop

Everything below is copy-paste-ready for livelabs.oracle.com/wms (Oracle VPN).
After approval, record the **WMS ID** in `tasks/todo.md` — it goes in the PR title (mandatory).

## Workshop Title

```
Build an AI-Powered Help Desk with Oracle APEX: From Prompt to Agent
```

## Abstract

```
Build a complete AI-powered help desk application in 90 minutes with Oracle APEX — and
learn the governed-AI patterns that make it enterprise-ready. You will design the data
model with AI and review the SQL it proposes, generate the Horizon Help Desk application
from a natural-language prompt, add plain-English analytics with AI Interactive Reports,
and build a 26.1 AI Agent with declarative tools that answers from your tickets and
knowledge base — and resolves a ticket only after you approve. Optional labs add
AI-drafted replies and fully in-database semantic search with AI Vector Search and an
ONNX embedding model.

Every AI feature comes with its governance story: token quotas you set yourself, human
review of AI-generated SQL, natural language that maps to inspectable declarative
settings (APEX never executes AI-generated SQL), tool allow-lists, and user-approval
confirmations on write actions — plus a clear statement of what data is (and is not)
sent to the model by each feature.

No OCI tenancy and no local install required: just a browser and a free Oracle account.
Suitable for experienced APEX developers, Oracle Database professionals new to APEX, and
developers new to Oracle.
```

## Short description

```
Build a governed AI help desk in Oracle APEX 26.1 in 90 minutes — from a prompt-generated app to an AI Agent that answers from your data and acts only after you approve, free in the browser.
```

## Reason for the workshop / business justification

```
This workshop supports a strategic account initiative: Oracle is working to grow database share within
Southwest Airlines' (SWA) developer organization, and this hands-on lab is built to reach those
developers directly — demonstrating that Oracle Database + APEX + the new 26.1 AI features let them
build governed, production-ready AI applications faster than the alternatives, and making the case for
Oracle Database as their platform of choice.

It also fills a real gap in the LiveLabs catalog. APEX 26.1 is a major AI release — declarative AI
Agents with governed tools, AI Interactive Reports (natural-language querying), and an expanded
Generative AI provider set — yet no workshop takes a developer end-to-end from prompt to a governed AI
agent on the free green-button sandbox; the existing AI-APEX workshops are all tenancy-only, which
excludes the large developer-day audience that arrives with just a browser and a free Oracle account.
In 90 minutes this green-button-first path teaches the new 26.1 AI features and, just as importantly,
the governance patterns that make them safe to ship — human review of AI-generated SQL, tool
allow-lists, user-approval confirmations on write actions, self-set token quotas, and an explicit
statement of what data each feature sends to the model. It serves the full APEX developer persona —
experienced APEX developers adopting AI, Oracle Database professionals new to low-code, and developers
new to Oracle.
```

## Outline (labs)

```
Introduction (finished-app tour; the Prompt -> App -> Trustworthy App arc)
Get Started: log in to the LiveLabs Sandbox (5 min)
Sign up for an APEX Workspace: Autonomous AI Database (Always Free where available, else trial credits) + workspace (10 min)
Lab 1: Connect APEX to Generative AI - OCI GenAI or OpenAI, token quota, APEX Assistant test (10 min)
Lab 2: Design the Data Model with AI - review AI's SQL, run the vetted schema + seed (10 min)
Lab 3: Generate the App from a Prompt - blueprint review, run the Horizon Help Desk (10 min)
Lab 4: Ask Your Data Anything with AI Interactive Reports - NL filters/charts as removable chips (10 min)
Lab 5: Build the Help Desk AI Agent - Retrieve Data tools + write tool with Requires Confirmation, Show AI Assistant embed (25 min)
Lab 6 [OPTIONAL]: Draft Replies with AI - Generate Text with AI on the ticket form (10 min)
Lab 7 [OPTIONAL]: Semantic Knowledge-Base Search - in-database ONNX embedding + Oracle Vector Search (15 min)
Take It Home: export, governance recap, credential cleanup, learning trail (7 min)
```

## Prerequisites

```
A free Oracle.com account and a modern browser. No OCI tenancy, no local install;
familiarity with SQL helpful but not required.
```

## Tags (required)

| Field | Value |
|---|---|
| Level | Beginner |
| Role | Application Developer; Database Administrator |
| Focus Area | Low Code; AI/ML |
| Product | Oracle APEX; Oracle Autonomous AI Database |

## Other fields

| Field | Value |
|---|---|
| Workshop Time (publishing entry) | 90 minutes |
| Author / Owner | Rick Houlihan |
| Quarterly QA owner | Rick Houlihan |
| **Development URL — green (sandbox)** ✅ LIVE | `https://rhoulihan.github.io/apex/ai-helpdesk-agent/workshops/sandbox/index.html` |
| **Development URL — brown (tenancy)** ✅ LIVE | `https://rhoulihan.github.io/apex/ai-helpdesk-agent/workshops/tenancy/index.html` |
| Development URL — event ✅ LIVE | `https://rhoulihan.github.io/apex/ai-helpdesk-agent/workshops/event/index.html` |
| Production URL — green (sandbox), after PR merges | `https://oracle-livelabs.github.io/apex/ai-helpdesk-agent/workshops/sandbox/index.html` |
| Production URL — brown (tenancy), after PR merges | `https://oracle-livelabs.github.io/apex/ai-helpdesk-agent/workshops/tenancy/index.html` |

*Dev hosting: fork `rhoulihan/apex`, branch `helpdesk-workshop-dev` (workshop-only), GitHub Pages built 2026-08-27. Screenshots are still placeholders until the T18 capture pass.*

## Environment status (2026-07-28 re-verification)

Verified end-to-end on a real green-button sandbox (see `docs/t18-verification-report.md` and the
`~/GitHub/agentBridge` run, responses 006 & 009):

| Item | Status |
|---|---|
| **APEX 26.1 on the sandbox ADB** | ✅ **Resolved** — provisions **APEX 26.1.1** (was 24.2.17 on 2026-07-08). Labs 4 & 5 unblocked; 26.1 AI-Agent data model present. |
| **OCI GenAI compartment chat quota** | ⚠️ **Zero by default → 429**, but **the Oracle LiveLabs team has confirmed they can raise `max-on-demand-chat-request-per-minute-count` on request** once the workshop's sandbox exists. So this is a **standard provisioning line-item**, not a blocker — it just has to be requested for our compartments (step 3 below). |
| **Lab 7 ONNX model hosting** | 🔴 **Lab 7 cannot run without this.** Oracle now publishes its embedding models **only as `_augmented.zip`**, and the database cannot unzip. Lab 7 needs a **LiveLabs-hosted, unzipped `all_MiniLM_L12_v2.onnx` (~127 MB)** reachable over HTTPS. This is a *hosting* request, not a service-limit one (step 3③). |
| **OCI GenAI per-model service limit** | ⚠️ **A second, separate limit** — tenancy/region scoped and applied **per model**, not per compartment. Raising the compartment quota does nothing for it. Verified 2026-08-30: `xai.grok-4.3` returned `HTTP-429: The requested model is throttled because the OCI Generative AI service limit for this model has been reached` after only two Lab 4 prompts, and had not recovered 70 s later. Must be requested **by model name** (step 3② below). |
| **Always Free ADB** | Unreliable on green-button (varies by region assignment) → workshop uses **trial-credit** ADB, not Always Free. |
| **Lab 7 ONNX grants** | `DBMS_CLOUD` execute + `CREATE MINING MODEL` need to be grantable to the workspace schema (or the model pre-loaded); not re-tested 2026-07-28. |

## Step-by-step submission guide

1. **Submit the workshop.** Connect **Oracle VPN** → `livelabs.oracle.com/wms` → **Submit a Workshop**. Paste **Title, Abstract, Outline, Prerequisites, Tags** from the sections above. Submit. *(Council reviews in ~2–3 business days.)*
2. **On `Approved` → create the green-button sandbox.** On the workshop's **Sandbox Environment** tab, tick the **Sandbox Lite** checkbox (auto-created in ~1 business day). This is the ship-now green-button path. *(Optional, non-blocking upgrade: open the **Full Sandbox Jira** — summary `[Sandbox] WMS ID: <id> LL ID: <id> Build an AI-Powered Help Desk with Oracle APEX` — for a pre-provisioned 26ai/APEX-26.1 ADB + pre-created workspace per attendee; cite `apex-native-map-regions` as the existing full-sandbox APEX precedent.)*
3. **Request the provisioning items for our compartments** (in the Sandbox Lite request and/or the Jira). These are the environment settings the AI labs need:
   - **③ Host the Lab 7 embedding model.** Publish an **unzipped** `all_MiniLM_L12_v2.onnx` in a
     LiveLabs-owned Object Storage bucket and give us a **long-lived** URL (public object or a PAR with a
     far-future expiry). Source: Oracle's *Machine Learning AI models* page, reached via the stable lookup
     `https://docs.oracle.com/pls/topic/lookup?ctx=en/database/oracle/oracle-database/26/vecse&id=oml_ai_models_object_storage`
     → download `all_MiniLM_L12_v2_augmented.zip` (~117 MB) → unzip → host the ~127 MB `.onnx`.
     **It must be the bare `.onnx`, not the zip** — `DBMS_VECTOR.LOAD_ONNX_MODEL` takes the model blob, the
     database has no unzip, and 26ai has no cloud loader to delegate to.
     *Why we are asking rather than self-hosting:* the workshop's previous hard-coded PAR expired and broke
     Lab 7 silently (`ORA-20401`). A LiveLabs-owned, long-lived URL is the only version of this that does
     not rot. **Whoever owns it should re-verify the link each quarterly QA.**
     *If LiveLabs will not host it:* Lab 7 becomes tenancy-only — each reader must create their own bucket
     and PAR — and the sandbox variant should drop Lab 7 or mark it as requiring an OCI bucket.
   - **② Raise the per-model GenAI service limits — by model name.** Separate from ①. The workshop
     currently needs an **xAI** model for Lab 4 (AI Interactive Reports) and **`cohere.command-a-03-2025`**
     for Lab 5 (AI Agents); no single model passes both labs on APEX 26.1.4. Size for **agents, not
     chat** — one agent turn is several tool-calling round trips, so Lab 5 consumes far more requests per
     student than Lab 4; a 30-seat room needs real headroom.
     **⚠️ Open question for the LiveLabs team:** can third-party model limits (xAI, Google, Meta) be
     raised at all, or only Oracle's own Cohere partner capacity? If xAI cannot be raised, Lab 4 needs
     either Oracle to fix the tool-definition `$schema` defect or the OpenAI track promoted to primary.
   - **① Raise the OCI GenAI chat quota** — set `max-on-demand-chat-request-per-minute-count` (and the embedding equivalent) **above zero** on the workshop compartments. The team confirmed this is doable on request. Without it, GenAI chat returns `HTTP-429: Compartment quota max-on-demand-chat-request-per-minute-count is exceeded` on the first request (verified 2026-07-08 Phoenix `c4ustudent03` and 2026-07-28 London `c4u02`; evidence `agentBridge/screenshots/009-test-result.png`). Note it is a **quota** ask, **not** IAM — API-key creation on the sandbox user is already unrestricted. Same limit affects every GenAI LiveLabs on green button.
   - **② Trial-credit ADB** — either grant Always-Free capacity in the assigned region, or confirm attendees create a **Transaction Processing** ADB on trial credits (the workshop already assumes this).
   - **③ Lab 7 (optional lab) grants** — `DBMS_CLOUD` execute + `CREATE MINING MODEL` grantable to the workspace schema, or pre-load the ONNX model.
4. **Record the WMS ID.** Put it in `tasks/todo.md`, then it goes in the **PR title** (mandatory). Reply with the WMS ID → the clean PR branch (T20) gets cut with the ID in the title.
5. **Screenshot / timing run + quota confirmation.** Once any sandbox reservation exists (Sandbox Lite, or a borrowed green-button in the same tenancy), do the screenshot/timing pass and confirm **GenAI Test Connection now succeeds** (i.e. the quota raise landed).

   > **⬜ MUST DO in production sandbox testing — re-verify the xAI model once limits are raised.**
   > `xai.grok-4.3` is the only model verified to drive **Lab 4**, but on Rick's tenancy it hit a
   > per-model service limit before **Lab 5**'s agent could answer even once. So its agent behaviour is
   > **unverified**. Once ② lands, re-run **both** Lab 4 (`show open tickets by priority as a chart`)
   > **and** the full Lab 5 conversation on the xAI model.
   > - If xAI drives both, the workshop can standardise on **one** model and the Lab 4 ↔ Lab 5 switch
   >   instruction can be deleted from Labs 1 and 5.
   > - If it still throttles, keep the two-model guidance and treat the switch as permanent.
   >
   > Note that **`Test Connection` succeeding proves nothing here** — it is a plain chat call and never
   > exercises tool calling. Only running the labs settles it.

   > **⬜ Also verify Lab 7 once ③ lands.** Point Task 3's `object_uri` at the hosted `.onnx` and run
   > Tasks 2–5 end to end: model loads as `MINILM_L12`, `embed-kb.sql` reports **20**, the Vector Provider
   > and Search Configuration save, and `laptop won't connect from hotel wifi` returns the VPN 812 article.
   > None of Tasks 2–5 has been validated on Autonomous Database yet — only on a local 26ai container.

> **Workshop-content note (not a WMS field):** the ADB-create **DB-version dropdown defaults to `19c`** (options: 26ai / 19c) until Oracle flips the default on **Sep 15 2026** — the sign-up lab must tell readers to pick **26ai** explicitly, or every 26ai-dependent lab silently fails.

## What does NOT block on WMS

The workshop content is done and validator-green. WMS approval gates the PR/publishing,
not development. The screenshot run (T18) needs a sandbox reservation, not WMS.
