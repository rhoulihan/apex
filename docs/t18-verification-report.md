# T18 Verification Run — Findings Report

**Date:** 2026-07-08
**Environment:** LiveLabs green-button sandbox (reservation 213888, tenancy `c4ustudent03`, region us-ashburn-1), borrowed via the "Build a Starter Online Shopping App using Oracle APEX" workshop (wid 848) because our own workshop isn't in the catalog yet. Driven end-to-end in an instrumented browser.
**Purpose:** Verify the AI Help Desk workshop against a real sandbox before WMS submission — especially the week-1 unknowns (GenAI-from-sandbox, our SQL against real 26ai, APEX version).

## TL;DR — 5 findings that reshape the go-live path

1. **Sandbox ADB runs APEX 24.2.17, not 26.1.** The 26.1-only labs (Lab 4 AI Interactive Reports, Lab 5 AI Agents+tools) can't run as written on today's green button. Confirmed at the API level too: `APEX_AI.SET_TOOL_RESULT`/`GENERATE`/`CHAT` procedures are absent in 24.2.
2. **GenAI is reachable from the sandbox compartment, but a compartment quota blocks all chat inference.** Test Connection got past auth, endpoint, region, and model — then returned `429: Compartment quota max-on-demand-chat-request-per-minute-count is exceeded`. Persistent across a 50-second retry → effectively a **zero quota**. This is almost certainly why the AI-APEX green buttons are currently disabled in the catalog.
3. **Our SQL is solid.** The full T6 database gate **passed** on the real 26ai database: schema loads 83/83/0, is idempotent, wins over a divergent precondition, and the resolve-ticket logic works. The `VECTOR` column compiled → 26ai vector support is live at the DB level even under APEX 24.2.
4. **Always Free ADB is quota-blocked in the sandbox compartment** (`adb-free-count=0`); had to use Transaction Processing on trial credits.
5. **Lab 7's ONNX path is blocked by student-tenancy privilege restrictions** — the ADMIN grants it needs don't actually land on the workspace schema.

**Every one of these is an environment/provisioning issue, not a workshop-content defect.** The content that *could* be exercised (setup, schema, resolve logic, GenAI config) all worked exactly as authored.

## What passed cleanly

- **Setup flow (Get Started + Sign up):** reservation → active in ~2 min; sandbox login + forced password reset; ADB create; APEX workspace `HELPDESK`/`DEMO`. Clean-path setup ≈ 15 min — matches the spec budget.
- **T6 database gate (our `helpdesk-schema.sql`, `resolve-ticket.sql`):**
  - Schema script: **83 statements, 83 successful, 0 errors.**
  - **Idempotent:** second run identical.
  - **Divergent-precondition:** created a wrong 2-column `tickets` table with a junk row, re-ran the script → canonical schema won (junk gone, ticket 42 restored to Open/Network, counts exact 50/20/8).
  - `REPLY` (Lab 6) and `EMBEDDING VECTOR` (Lab 7) columns present; the `VECTOR` type compiled.
  - resolve-ticket core (SELECT subject + UPDATE Resolved) produced the exact intended message for ticket 42.
- **GenAI service configuration (Lab 1):** the APEX 24.2 create form matches our Lab 1 field-for-field (Compartment ID, Region, Model ID, Used by App Builder, inline User/Key/Tenancy/Fingerprint credential). Providers in 24.2 = OCI GenAI / OpenAI / Cohere (the 26.1 additions Claude/Gemini/Mistral/Ollama are absent — consistent). Service saved successfully; only the *inference* is quota-blocked.

## The GenAI finding in detail (most important)

Configured `Helpdesk AI` (static id `helpdesk_ai`), region `us-chicago-1`, model `cohere.command-r-08-2024`, with a self-generated OCI API key (public key uploaded to OCI, private key pasted into APEX). **Test Connection:**

> `429: Compartment quota max-on-demand-chat-request-per-minute-count is exceeded, request is throttled for compartment: ocid1.compartment.oc1..aaaa…`

- No `401`/`NotAuthorized` → **the IAM policy allows GenAI and the credential is valid.**
- No `404` on the model → **the model id and region are valid and available.**
- The failure is purely a **compartment-level on-demand-chat quota**, hit on the very first request and still failing after a 50-second wait → the quota is at or near **zero** for LiveLabs student compartments.

**Implication:** the workshop's core AI mechanism is *viable* on the green button — the plumbing works — but it is gated entirely on the environment's GenAI capacity being provisioned. This must be the #1 line item in the WMS Sandbox Lite / full-sandbox Jira request.

### Root cause of the 429 — refined (which "guardrail" is it?)

The most likely cause is **the account tier of the sandbox tenancy, not a per-workshop provisioning toggle.** Evidence:
- The sandbox tenancy (`c4ustudent03`) is flagged **"Free Tier account"** on every OCI page.
- The error string `max-on-demand-chat-request-per-minute-count` is the literal name of an **OCI Generative AI service limit**, and OCI Free-Trial / Always-Free accounts default this on-demand-inference limit to **0 / near-0** until a service-limit increase is requested. The OCI Console → *Limits, quotas and usage* page even surfaces a **"Request a service limit increase"** action and notes "availability can be affected by quota policies set on this compartment and/or its parent compartments."
- The assigned compartment is per-reservation and isolated, and the first-ever request 429'd → not shared consumption, but a limit at/near zero.

So the throttle is best understood as **"free-tier GenAI is off by default,"** an OCI-account-level cost guardrail — directionally what one would expect for a free workshop, but tied to the *tenancy's account tier/service limit*, not to whether a particular workshop's sandbox pool has "GenAI enabled."

**Corroborating signal, with a caveat:** the shopping-cart workshop we borrowed *does* ship GenAI labs, and the dedicated AI-APEX green buttons (nyc-genai-lab, ai-vision-lab) are currently **disabled** — consistent with GenAI-on-sandbox being broadly constrained right now, which fits an account-tier/service-limit cause more than a per-workshop one.

**What we could NOT determine from inside one borrowed free-trial sandbox:** the exact limit value, and whether LiveLabs' *production* GenAI-workshop sandboxes run on an entitled/paid tenancy with the limit already raised. A LiveLabs admin can read both in ~30 seconds. So the sharpened ask is: **does our workshop's sandbox run on a tenancy/compartment where the OCI Generative AI on-demand chat service limit is > 0 (entitled tenancy, or limit-increase filed)** — not merely "please enable GenAI for this pool." This makes the OpenAI fallback + staggered-exercise design load-bearing regardless.

## Decisions this run tees up (for Rick + APEX team)

1. **26.1 timing** — when does APEX 26.1 reach ADB in the LiveLabs tenancies/regions? Until it does, Labs 4–5 need the 24.2 "AI Configurations" fallback (already documented in the spec) or the workshop waits.
2. **Sandbox provisioning asks** (all must be in the WMS/Jira request, or no AI lab runs on green button):
   - Raise `max-on-demand-chat-request-per-minute-count` (+ embedding equivalents) on the workshop compartments.
   - `adb-free-count ≥ 1` (or accept trial-credit ADBs).
   - `DBMS_CLOUD` execute + `CREATE MINING MODEL` grantable to workspace schemas (for Lab 7), or pre-provision the ONNX model.
3. **Launch shape** — given the above, a 24.2-compatible v1 (Labs 4–5 via AI Configurations) is buildable now *if* the quota is raised; the full 26.1 Agents/NL2IR version waits on the ADB rollout.

## Artifacts

- Screenshots (throwaway sandbox creds, redact before any external use): `scratchpad/t18-captures/` — includes `genai-429-error.png`, the reservation drawer, and grant results.
- Timings log: `scratchpad/t18-timings.txt`.
- All findings also logged inline in `tasks/todo.md` under the T18 headings.

*Note: the sandbox reservation auto-deletes at expiry; nothing to clean up. Credentials captured during the run were throwaway LiveLabs student-tenancy credentials for an isolated compartment.*
