# Draft email to the APEX / LiveLabs team

**To:** [APEX PM / LiveLabs team]
**Subject:** APEX + AI LiveLabs workshop — two questions before I submit (26.1-on-ADB + GenAI sandbox limits)

---

Hi [name],

I'm putting together a new LiveLabs workshop — **"Build an AI-Powered Help Desk with Oracle APEX: From Prompt to Agent"** — a 90-minute, **green-button (Sandbox)** workshop that walks attendees from prompt-to-app through a governed AI Agent that acts on their data. It's aimed at a gap I couldn't find covered: an end-to-end *build-an-AI-app-on-the-green-button* experience, since today's AI-APEX workshops (event-mangement, scm-ai-agent, crm-apexlang, …) are all tenancy-only.

Before submitting to WMS, I ran the whole thing end-to-end on a real LiveLabs sandbox. The **content held up** — our schema and PL/SQL ran clean on 26ai and setup timed to budget — but I hit two environment blockers I'd like your read on:

**1. APEX 26.1 on ADB.** The sandbox ADB provisioned at **APEX 24.2.17** (and reports "up to date"). Two of my labs — AI Interactive Reports and AI Agents + Tools — are 26.1-only. When do you expect 26.1 to reach ADB Serverless in the LiveLabs sandbox tenancies/regions? If it's a way out, I'll ship a 24.2-compatible v1 (AI Configurations in place of Agents) and upgrade once ADB catches up.

**2. GenAI on-demand chat in the sandbox.** Configuring the Generative AI service worked — auth, region (us-chicago-1), and model all validated — but Test Connection returns:

> `429: Compartment quota max-on-demand-chat-request-per-minute-count is exceeded, request is throttled for compartment…`

The sandbox tenancy is a **Free Tier account**, so I suspect the OCI on-demand-chat service limit is 0 by default. Two questions:
- Do the production APEX GenAI green-button sandboxes run on a tenancy/compartment where that service limit is **raised** (or a limit increase is on file)? I want the workshop's sandbox to have chat capacity > 0 — otherwise no AI lab runs on the green button.
- Related: the **nyc-genai-lab** and **ai-vision-lab** green buttons are currently **disabled** in the catalog — is that the same GenAI-on-sandbox issue?

For the sandbox request itself, I'll be asking for: the **GenAI on-demand chat limit raised**, **adb-free-count ≥ 1** on the compartment, and **DBMS_CLOUD execute + CREATE MINING MODEL grantable** to workspace schemas (my optional vector-search lab loads an ONNX model in-database).

I have a full verification write-up — findings, timings, and exact errors — happy to send it over. Mostly I want to request the right sandbox configuration up front so the AI labs actually run at our developer days.

Thanks,
Rick

---

*Notes for Rick before sending:*
- *Fill in the recipient(s). Good candidates: the APEX PM who owns the AI features / the LiveLabs APEX content owner, plus livelabs-help-apex_us@oracle.com or the LiveLabs infra/sandbox owner on cc.*
- *Full evidence is in `docs/t18-verification-report.md`; the concrete sandbox asks are in `docs/wms-submission.md`.*
- *If you'd rather split it: question 1 (26.1-on-ADB) is really for the APEX PM team; question 2 (GenAI limits + disabled green buttons) is for the LiveLabs sandbox/infra owner. Sending one email cc'ing both is fine — they'll route it.*
