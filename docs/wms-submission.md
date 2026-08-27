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
Take It Home: export, governance recap, learning trail (5 min)
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
| **Always Free ADB** | Unreliable on green-button (varies by region assignment) → workshop uses **trial-credit** ADB, not Always Free. |
| **Lab 7 ONNX grants** | `DBMS_CLOUD` execute + `CREATE MINING MODEL` need to be grantable to the workspace schema (or the model pre-loaded); not re-tested 2026-07-28. |

## Step-by-step submission guide

1. **Submit the workshop.** Connect **Oracle VPN** → `livelabs.oracle.com/wms` → **Submit a Workshop**. Paste **Title, Abstract, Outline, Prerequisites, Tags** from the sections above. Submit. *(Council reviews in ~2–3 business days.)*
2. **On `Approved` → create the green-button sandbox.** On the workshop's **Sandbox Environment** tab, tick the **Sandbox Lite** checkbox (auto-created in ~1 business day). This is the ship-now green-button path. *(Optional, non-blocking upgrade: open the **Full Sandbox Jira** — summary `[Sandbox] WMS ID: <id> LL ID: <id> Build an AI-Powered Help Desk with Oracle APEX` — for a pre-provisioned 26ai/APEX-26.1 ADB + pre-created workspace per attendee; cite `apex-native-map-regions` as the existing full-sandbox APEX precedent.)*
3. **Request the provisioning items for our compartments** (in the Sandbox Lite request and/or the Jira). These are the environment settings the AI labs need:
   - **① Raise the OCI GenAI chat quota** — set `max-on-demand-chat-request-per-minute-count` (and the embedding equivalent) **above zero** on the workshop compartments. The team confirmed this is doable on request. Without it, GenAI chat returns `HTTP-429: Compartment quota max-on-demand-chat-request-per-minute-count is exceeded` on the first request (verified 2026-07-08 Phoenix `c4ustudent03` and 2026-07-28 London `c4u02`; evidence `agentBridge/screenshots/009-test-result.png`). Note it is a **quota** ask, **not** IAM — API-key creation on the sandbox user is already unrestricted. Same limit affects every GenAI LiveLabs on green button.
   - **② Trial-credit ADB** — either grant Always-Free capacity in the assigned region, or confirm attendees create a **Transaction Processing** ADB on trial credits (the workshop already assumes this).
   - **③ Lab 7 (optional lab) grants** — `DBMS_CLOUD` execute + `CREATE MINING MODEL` grantable to the workspace schema, or pre-load the ONNX model.
4. **Record the WMS ID.** Put it in `tasks/todo.md`, then it goes in the **PR title** (mandatory). Reply with the WMS ID → the clean PR branch (T20) gets cut with the ID in the title.
5. **Screenshot / timing run + quota confirmation.** Once any sandbox reservation exists (Sandbox Lite, or a borrowed green-button in the same tenancy), do the screenshot/timing pass and confirm **GenAI Test Connection now succeeds** (i.e. the quota raise landed).

> **Workshop-content note (not a WMS field):** the ADB-create **DB-version dropdown defaults to `19c`** (options: 26ai / 19c) until Oracle flips the default on **Sep 15 2026** — the sign-up lab must tell readers to pick **26ai** explicitly, or every 26ai-dependent lab silently fails.

## What does NOT block on WMS

The workshop content is done and validator-green. WMS approval gates the PR/publishing,
not development. The screenshot run (T18) needs a sandbox reservation, not WMS.
