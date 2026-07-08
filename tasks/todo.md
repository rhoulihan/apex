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
