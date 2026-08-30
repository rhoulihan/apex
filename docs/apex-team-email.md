# Draft email to the APEX / LiveLabs team

**To:** [LiveLabs sandbox/infra owner] · **Cc:** [APEX PM] · livelabs-help-apex_us@oracle.com
**Subject:** LiveLabs green-button GenAI is quota-blocked (429) — request to raise the compartment chat limit

---

Hi [name],

Two quick updates on the new green-button workshop I'm building — **"Build an AI-Powered Help Desk with Oracle APEX: From Prompt to Agent."** I re-verified it end-to-end on a fresh LiveLabs green-button sandbox today (2026-07-28), and it's down to a single provisioning blocker.

**1. APEX 26.1 on ADB — resolved, thank you.** The sandbox ADB now provisions **APEX 26.1.1** (it was 24.2.17 three weeks ago). My two 26.1-only labs — AI Interactive Reports and AI Agents + tools — are unblocked, and the 26.1 declarative-agent data model is present. One small heads-up for anyone writing green-button labs: the ADB create form's **database-version dropdown still defaults to `19c`** (until the Sep 15 2026 default flip), so lab text has to tell readers to pick **26ai** explicitly or they silently get a 19c database.

**2. GenAI on-demand chat is still quota-blocked at zero — this is the blocker.** Configuring the Generative AI service in APEX works — auth, region (I tested `uk-london-1`), and model all validate — but **Test Connection returns:**

> `HTTP-429: Compartment quota max-on-demand-chat-request-per-minute-count is exceeded, request is throttled for compartment: ocid1.compartment.oc1..aaaa…`

This is the same error I hit on 2026-07-08, now **reproduced on a brand-new sandbox, different region, different tenancy, on the very first request** from a freshly created compartment — so the per-minute quota is effectively **0**. Importantly:
- The API key **authenticated** (a bad key returns 401, not 429), and the model/region **resolved** (else 404). It's purely the GenAI service quota.
- **API-key creation on the sandbox user is unrestricted** — so this is *not* an IAM ask; it's specifically the OCI Generative AI service limit.

**The ask:** raise `max-on-demand-chat-request-per-minute-count` (and the embedding equivalent) above zero on the LiveLabs green-button compartments. Without it, **no LiveLabs workshop can use OCI Generative AI on the green button at all** — this hits more than mine (e.g. the shopping-cart workshop's own GenAI lab hits the same wall), and it's almost certainly why the dedicated AI-APEX green buttons are currently disabled in the catalog.

I have a full write-up with the verbatim errors, the compartment OCID, screenshots, and timings — happy to send it over or open the sandbox Jira with it attached. Mostly I want to get the right compartment quota in place so the AI labs actually run at our developer days.

Thanks,
Rick

---

*Notes for Rick before sending:*
- *Evidence: `agentBridge/screenshots/009-test-result.png` (the 429), plus `docs/t18-verification-report.md` and the concrete asks in `docs/wms-submission.md`.*
- *Recipients: the LiveLabs sandbox/infra owner is the primary now (it's a provisioning/quota ask, not an APEX-feature question). Cc the APEX PM for awareness.*
- *If they want it as a ticket: the sandbox Jira summary format is `[Sandbox] WMS ID: <id> LL ID: <id> …` — but the quota raise can likely be actioned directly.*
