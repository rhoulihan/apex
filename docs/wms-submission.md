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

## Outline (labs)

```
Introduction (finished-app tour; the Prompt -> App -> Trustworthy App arc)
Get Started: log in to the LiveLabs Sandbox (5 min)
Sign up for an APEX Workspace: Always Free ADB + workspace (10 min)
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
| Brown-button URL (after PR merges) | `https://oracle-livelabs.github.io/apex/ai-helpdesk-agent/workshops/tenancy/` |
| Green-button URL (after PR merges) | `https://oracle-livelabs.github.io/apex/ai-helpdesk-agent/workshops/sandbox/` |

## Submission steps (in order)

1. VPN → livelabs.oracle.com/wms → **Submit a Workshop**. Paste title, abstract, outline, prerequisites, tags from above. Submit. (Council reviews in 2–3 business days.)
2. When status = **Approved**: on the workshop's **Sandbox Environment** tab, tick the **Sandbox Lite** checkbox (auto-created ~1 business day). This is our ship-now green-button path.
3. Same tab, in parallel (optional upgrade, non-blocking): open the **Jira for a Full Sandbox** — summary format `[Sandbox] WMS ID: <id> LL ID: <id> Build an AI-Powered Help Desk with Oracle APEX`. Ask for: pre-provisioned ADB (26ai, APEX 26.1) + pre-created APEX workspace per attendee; cite `apex-native-map-regions` as the existing full-sandbox APEX precedent.

   **CRITICAL provisioning asks (from the T18 verification run — see `docs/t18-verification-report.md`). Without these, NO AI lab runs on the green button:**
   - **Raise the compartment GenAI quota** `max-on-demand-chat-request-per-minute-count` (and embedding equivalents) on the workshop compartments. T18 proved GenAI auth/endpoint/model all work from a sandbox compartment, but this quota is at/near **zero** on student compartments → all chat inference 429s. This is the #1 blocker and almost certainly why the existing AI-APEX green buttons are disabled.
   - **APEX 26.1 on the ADB** — sandbox ADBs are still on APEX 24.2.17; Labs 4 (AI Interactive Reports) and 5 (AI Agents + tools) are 26.1-only. Ask when 26.1 reaches ADB in the LiveLabs tenancies, or plan a 24.2 "AI Configurations" fallback for those two labs.
   - **`adb-free-count ≥ 1`** on the compartment (Always Free ADB creation currently quota-blocked → had to use trial credits).
   - **Lab 7:** `DBMS_CLOUD` execute + `CREATE MINING MODEL` grantable to workspace schemas (or pre-load the ONNX model). T18 showed these ADMIN grants don't land in the student tenancy.
4. Reply here with the **WMS ID** → I cut the clean PR branch (T20) with the ID in the title.
5. Once you have any sandbox reservation (yours via the green-buttoned nyc-genai-lab in the same tenancy, or ours once Sandbox Lite exists): that's our T18 screenshot/timing run and the week-1 GenAI verification.

## What does NOT block on WMS

The workshop content is done and validator-green. WMS approval gates the PR/publishing,
not development. The screenshot run (T18) needs a sandbox reservation, not WMS.
