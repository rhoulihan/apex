# Workshop Spec — "Build an AI-Powered Help Desk with Oracle APEX: From Prompt to Agent"

**Status:** Draft for Rick's review — no lab authoring until approved
**Date:** 2026-07-07
**Author:** Claude (research: 3 agent reports in `docs/research/`, LiveLabs conventions report)
**Target repo:** `oracle-livelabs/apex` (this repo; develop on a fork branch, PR with WMS ID)
**Delivery:** Oracle LiveLabs, green button (LiveLabs Sandbox) primary + tenancy (brown button) variant

---

## 1. Context and goal

Rick needs a hands-on live lab for developer days: ~90 minutes, runnable by both new and existing APEX developers, focused on APEX + AI, delivered on the LiveLabs Sandbox so attendees need **nothing but a browser and a free Oracle account**.

**The catalog gap this fills** (see `docs/research/2026-07-07-livelabs-apex-landscape.md`): the `oracle-livelabs/apex` repo has 15 AI-related workshops, but only 3 ship a green-button variant, and all 3 are feature-integration labs on prebuilt apps. Every end-to-end "build an app with AI" workshop (event-mangement, bootcamp_crm, proof-of-concept, scm-ai-agent, crm-apexlang) is tenancy-only. **Nobody owns "AI-assisted app build + runtime AI agent, end-to-end, on the green button."** The 26.1 marquee features — AI Agents with declarative tools, and AI Interactive Reports — are unclaimed on the sandbox entirely.

**Positioning sentence** (for WMS abstract and the developer-day agenda):
> Build a complete AI-powered help desk application in 90 minutes with Oracle APEX — design the data model with AI, generate the app from a prompt, ask your data questions in plain English, and ship a governed AI agent that acts on your tickets. No tenancy, no install: just a browser.

## 2. Who this is for (persona summary)

Full report: `docs/research/2026-07-07-apex-developer-persona.md`. The load-bearing facts:

- The APEX developer is a **database person, not a web person**: Forms/PL-SQL veterans, DBAs upskilling, consultants. Expert SQL; weak-to-absent JavaScript; no npm/terminal culture. Pace to the "Oracle DB pro who has never used APEX" and give experts stretch steps.
- **AI sentiment is pragmatic optimism with identity anxiety.** Oracle's own framing ("the OG Vibe Coding Platform you can trust") co-opts the displacement narrative. The workshop must land "AI as amplifier, not replacement" — explicitly, in the intro and in the design (the attendee reviews and approves what AI produces at every step).
- Zero-install expectations; a 15-minute signup kills a 90-minute session.

Design rules derived from the persona (enforced throughout section 4):

| Rule | Consequence in this workshop |
|---|---|
| Anchor in SQL, never JS | Zero JavaScript typed by attendees; all code blocks are SQL/PL-SQL or prompts |
| ~70/30 clicks-to-code | Declarative components carry the flow; code appears only where it flatters their strength |
| AI wow early, then make it *real* | App exists by ~minute 45 of the slot (~minute 30 of hands-on time); the back half grounds AI in their data with governance |
| Stretch steps so experts never idle | Every core lab ends with an optional "Go further" task; two optional labs at the end |
| One governance beat per AI feature | "You review AI's SQL before running it" (Lab 2), "APEX never executes AI-generated SQL" (Lab 4), guardrail approval on the agent's write tool (Lab 5) |
| Define AI terms, assume DB terms | Glossary beats for *embedding, RAG, agent, tool, token*; free use of *schema, workspace, PL/SQL* |
| Close with their actual learning trail | LiveLabs, APEX Office Hours, Insum Instant Tips, Cloud Nueva, apex.world — not "see GitHub" |

## 3. Workshop concept

- **Title (proposed):** *Build an AI-Powered Help Desk with Oracle APEX: From Prompt to Agent*
  Alternates: *From Prompt to Agent: Ship an AI Help Desk in 90 Minutes with Oracle APEX*; *Build and Govern an AI Agent App with Oracle APEX*.
- **Folder:** `ai-helpdesk-agent/`
- **App domain: IT Help Desk** ("Horizon Help Desk"). Rationale: universally understood by all three persona segments; enterprise-flavored (respects professional identity); a knowledge base is a *natural* RAG corpus; "close this ticket" is a natural governed agent action; and no existing workshop uses it (schools, events, CRM, procurement, bookstore, movies, expenses are taken).
- **Schema (3 tables, deterministic):** `TICKETS` (id, subject, description, status, priority, category, created_on, assigned_to), `KB_ARTICLES` (id, title, content, category, updated_on), `TEAM_MEMBERS` (id, name, role, email). Curated seed data ships in `files/`: ~50 tickets across statuses/categories and ~20 knowledge-base articles with concrete, memorable fixes (VPN error 812, printer spooler, MFA reset…) so every attendee's AI answers match the lab text.
- **Learning objectives** (WMS "Objectives"): after this workshop you can
  1. Connect APEX to a Generative AI provider and enable the APEX Assistant.
  2. Use AI to design a data model and generate a working application from a natural-language prompt.
  3. Add natural-language analytics to a report with AI Interactive Reports.
  4. Build a governed AI Agent with declarative tools (read data, act with approval) and embed it in your app.
  5. Explain how APEX keeps AI governed: human review of generated SQL, no AI-executed SQL, tool allow-lists, guardrail approvals, token quotas.
- **Narrative arc:** *Prompt → App → Trustworthy App.* Act 1: AI builds it with you. Act 2: AI works inside it, on your data. Act 3 (the through-line): you are the reviewer, the agent is governed — "AI as amplifier."
- **WMS tags:** Level: Beginner (Intermediate-friendly) · Role: Application Developer / DBA · Focus Area: Low Code, AI · Product: Oracle APEX, Autonomous AI Database.

## 4. Lab-by-lab breakdown (90-minute budget)

Timing model: LiveLabs Sandbox Lite — attendee logs into an assigned compartment and creates ADB + workspace themselves (this is the pattern of every current APEX sandbox workshop; a pre-provisioned full sandbox is a possible upgrade, section 5). Reservation set to 90 min in WMS; attendees can self-extend to 180. Core hands-on = **75 min**; optionals +25 for fast attendees.

| # | Lab | Time | Cumulative |
|---|---|---|---|
| — | Get Started: sandbox login (CDN common lab) | 5 | 5 |
| — | Sign up for an APEX Workspace (common include: create Always Free ADB + workspace) | 10 | 15 |
| — | Introduction (read while ADB provisions) | 0 | 15 |
| 1 | Connect APEX to Generative AI | 10 | 25 |
| 2 | Design the Data Model with AI | 10 | 35 |
| 3 | Generate the App from a Prompt | 10 | 45 |
| 4 | Ask Your Data Anything: AI Interactive Reports | 10 | 55 |
| 5 | Build the Help Desk AI Agent | 20 | 75 |
| 6 | OPTIONAL: Draft Replies with AI | 10 | (85) |
| 7 | OPTIONAL: Semantic Knowledge-Base Search with AI Vector Search | 15 | (100)* |
| — | Take It Home: export your app + learning trail | 5 | 80–90 |

\* Optionals overflow the 90-min slot by design; the reservation self-extends and both labs are marked OPTIONAL in the manifest title (established pattern: nyc-genai-lab Lab 7).

**Live-event pacing:** while ADB provisions (~2–5 min), the instructor demos the finished app — this plants the wow before minute 10 and absorbs the provisioning wait. In self-paced mode the Introduction fills the same gap.

### Get Started + Sign up for an APEX Workspace (common includes, 15 min)
Manifest entries only — no authored content: CDN `cloud-login/cloud-login-livelabs2.md`, then `common-latest/1-sign-up-apex/sign-up-apex-sandbox.md` (attendee creates Always Free ADB — APEX preinstalled — and a `DEMO` workspace). Verify at dev time whether `common-latest` vs `common-261` is the maintainers' current preference and that the include paths resolve (nyc-genai-lab's sandbox manifest has a stale local path — the exact bug our validator must catch).

### Lab 1: Connect APEX to Generative AI (10 min)
- **Tasks:** (1) Generate an OCI API key pair for the sandbox user; collect user/tenancy OCIDs. (2) Create the Generative AI service in Workspace Utilities: OCI Generative AI, region `us-chicago-1`, current model (instruction says "pick the latest available chat model" — never a hardcoded deprecated ID), **"Used by App Builder" ON** (the classically missed toggle — screenshot + warning box). (3) Instant feedback: ask APEX Assistant a question from SQL Workshop to prove the wiring.
- **Provider fallback:** `type` conditional (nyc-genai-lab Lab 3 pattern): `OCIGenAI` (default) / `OpenAI` (bring-your-own key) in the *same* lab file.
- **Adapt, don't fork:** start from `common-261/2-configure-ai-keys` content; if it fits verbatim, include it directly from the manifest and this lab shrinks to a wrapper.
- **Go further (stretch):** ask the Assistant to *explain* a PL/SQL block (segment-a candy).

### Lab 2: Design the Data Model with AI (10 min)
- **Tasks:** (1) Open Create Data Model with AI; paste the provided prompt ("help desk for an IT team: tickets, knowledge-base articles, team members…"). (2) **Review** the SQL the AI proposes — the lab calls out what to check (keys, data types, naming). *Governance beat #1: you are the reviewer.* (3) Run the **canonical DDL + seed data script** (copy block + `files/helpdesk-schema.sql`): framed as "run the reviewed, vetted version so the whole room stays in sync" — this both teaches the review habit and guarantees deterministic downstream labs (AI output varies per attendee; lab text and screenshots must not).
- **Go further:** ask APEX Assistant to write an analytic query (tickets by category, trend) and run it.

### Lab 3: Generate the App from a Prompt (10 min)
- **Tasks:** (1) Create App with AI over the existing tables, provided prompt. (2) **Blueprint checklist** before clicking Create: must include Dashboard, Tickets (report + form), Knowledge Base; add any missing page declaratively in the blueprint editor — this bounds AI variance. (3) Create, run, log in: **a real web app with auth at a real URL — the act-one payoff.** (4) 2-minute guided tour mapping what got generated to APEX concepts (pages, regions — vocabulary for the rest of the labs).
- **Fallback box:** "Your generated app may differ — that's the point of generative AI. As long as you have X and Y, continue; here's how to add either in 60 seconds."

### Lab 4: Ask Your Data Anything — AI Interactive Reports (10 min)
- **Tasks:** (1) Enable AI on the Tickets interactive report (26.1 NL2IR). (2) Prompt it: "show open tickets by priority as a chart", "group by category, oldest first" → watch filters/charts land as **removable declarative chips**. (3) *Governance beat #2*, in a callout: APEX never executes AI-generated SQL — the AI maps intent onto the same declarative IR settings you could click by hand; chips are inspectable and reversible.
- **Go further:** column-level AI attributes (per `ai-interactive-report-lab`).

### Lab 5: Build the Help Desk AI Agent (20 min — the marquee)
- **Tasks:** (1) Create an **AI Agent** (26.1 shared component; note it evolved from 24.2 "AI Configurations"): system prompt = help-desk analyst persona; welcome message. (2) Attach **AI Tool: Retrieve Data** over tickets (SQL source) — *define RAG in one callout sentence here.* (3) Attach a second Retrieve Data tool over KB articles. (4) Attach **AI Tool: Execute Server-side Code** — `resolve_ticket(p_ticket_id)` (provided ~10-line PL/SQL) — with **Guardrail: require user approval**. (5) Add the **Show AI Assistant** dynamic action to the app (floating chat). (6) The payoff conversation, scripted in the lab: *"A user reports VPN error 812 — any KB fix?"* (agent retrieves the article) → *"Are there open tickets about it?"* (agent queries tickets) → *"Resolve ticket 42"* → **approval prompt appears** → confirm → row updated. *Governance beat #3: the agent can only use tools you attached, and writes require your approval.*
- **Go further:** add a third tool (create ticket), tune the system prompt, ask the agent something outside its tools and observe the refusal.

### Lab 6 (OPTIONAL): Draft Replies with AI (10 min)
- Generate Text with AI dynamic action on the ticket form: draft a customer-facing reply from the ticket description (+ relevant KB article as context), editable before save — the "AI drafts, human sends" pattern attendees can lift straight into their own apps.

### Lab 7 (OPTIONAL): Semantic Knowledge-Base Search with AI Vector Search (15 min)
- Provided script adds a `VECTOR` column, creates the `DBMS_VECTOR` credential (reusing Lab 1's key), embeds the 20 KB articles via OCI GenAI embed model; then a declarative **Search Configuration (AI Vector Search)** + search page: "laptop won't connect from hotel wifi" finds the VPN article with zero keyword overlap. Defines *embedding* in one callout. This is the segment-(a) magnet and the 26ai tie-in.
- Clearly marked OPTIONAL; nothing downstream depends on it. (ONNX in-database embedding is the no-external-call alternative — decide at dev time after testing both in the sandbox.)

### Take It Home (5 min)
- Export the app (and note APEXlang/SQLcl as the modern export for source control — one paragraph, no exercise); download links for all scripts; **the sandbox is wiped at reservation end** (warning box); "run this again free": apex.oracle.com + Always Free; learning trail (LiveLabs catalog, APEX Office Hours, Insum Instant Tips, Cloud Nueva, apex.world); pointers to the tenancy-only sequels (scm-ai-agent, crm-apexlang) as "your next workshop."

## 5. Environment design

**Primary: LiveLabs Sandbox Lite** (green button). Auto-created in 1 business day via WMS checkbox; attendee gets an isolated compartment in a LiveLabs-owned tenancy; creates own ADB + workspace (15 min, common includes). No infra-team dependency — this is the ship-now path, and it matches every existing APEX sandbox workshop.

**Upgrade path (parallel, non-blocking): full LiveLabs Sandbox** via Jira from the WMS Sandbox Environment tab — pre-provisioned ADB + workspace would claw back ~10 minutes and move the first wow before minute 20 (persona ideal). Pursue it, but the workshop must not depend on it.

**The critical unknown to burn down first: OCI GenAI availability from LiveLabs sandbox compartments.** Evidence says yes (nyc-genai-lab's green-button variant configures OCI GenAI in-sandbox), but this gets verified **in week 1 of development** with a real sandbox reservation, before any lab content is written. Documented fallback either way: the OpenAI `type` path with an event-provided key.

**Variants shipped:** `workshops/sandbox/` (green, primary), `workshops/tenancy/` (brown twin — required for the WMS publishing entry; swaps the two setup includes for freetier login/provision labs and `need-help-freetier.md`), and later `workshops/event/` re-cuts per developer day (established `tenancy-special`/`aiw25` pattern). Single-source lab content; variance only in manifests and `type` conditionals — **every include path must resolve in every variant** (validator-enforced).

**Concurrency plan for developer days:** green button caps at **~30 concurrent reservations**.
- ≤30 seats: green button as-is (have attendees start reservations at t-0; provisioning is minutes).
- >30 seats: request an **Event Code** in WMS (2-day review) pointing at the event manifest, backed by the **tenancy variant on an event-provided tenancy** (capacity = tenancy limits), and/or pre-negotiate sandbox capacity via livelabs-help-apex_us@oracle.com. Decision input needed from Rick: expected seat count (open question #1).

**Throttling defense (any variant):** OCI GenAI on-demand inference is dynamically throttled per tenancy — 30–50 people in one tenancy can see 429s. Mitigations designed in: 26.1 **Max AI Tokens** quotas at workspace level; labs alternate clicky tasks with AI calls (natural staggering); the scripted agent conversation is 3 calls, not 20; troubleshooting box in every AI lab ("if you get a rate-limit error, wait 30s and retry"); OpenAI fallback path as pressure relief.

## 6. Repo deliverables (target structure)

```
ai-helpdesk-agent/
├── introduction/introduction.md          # + images/
├── 1-connect-genai/1-connect-genai.md    # type-conditional OCIGenAI/OpenAI (or common-261 include)
├── 2-data-model-ai/2-data-model-ai.md    # + files/helpdesk-schema.sql (DDL + seed, idempotent)
├── 3-generate-app/3-generate-app.md
├── 4-ai-interactive-report/4-ai-interactive-report.md
├── 5-ai-agent/5-ai-agent.md              # + files/resolve-ticket.sql
├── 6-generate-text/6-generate-text.md    # OPTIONAL
├── 7-vector-search/7-vector-search.md    # OPTIONAL + files/embed-kb.sql
├── 8-take-it-home/8-take-it-home.md      # + finished app export zip
└── workshops/
    ├── sandbox/{index.html,manifest.json}
    └── tenancy/{index.html,manifest.json}
```

Conventions (from `sample-workshop` + repo lint, validator-enforced): lowercase filenames; one folder per lab with `images/` (+ `files/`); lab skeleton `# Title → ## Introduction → Estimated Time → ### Objectives → ### Prerequisites → ## Task 1..N → ## Learn More → ## Acknowledgements`; `<copy>` on every code block; alt text on every image; image sizes within the repo's `enforce-image-size` workflow limits; manifest lab titles `Lab N: <imperative>`; "Need Help?" CDN include last; help email `livelabs-help-apex_us@oracle.com`.

## 7. Development methodology — inline, strict TDD

All development happens inline (no delegated authoring). TDD for a content deliverable means **executable checks exist before the content they check**, and the cycle is red → green → refactor:

1. **Harness first.** Build `tools/validate_workshop.py` (stdlib-only) + a pytest suite covering the validator itself, before any lab is written. Checks: manifest parses and conforms (title, help email, "Need Help?" last, Get Started first in sandbox variant); **every `filename` resolves** — local, `common-*`, and CDN URLs (HTTP 200) — in **every** variant; per-lab structural rules (single H1, Estimated Time, Objectives, Acknowledgements, `<copy>` on fenced code, images exist + alt text); lab time sum ≤ budget per variant; **banned-strings list** (deprecated model IDs, hardcoded OCIDs, "23ai" where "26ai" is meant, TODO/TBD).
2. **Red-green per lab.** Add the manifest entry + any lab-specific validator expectations first (validator fails: file missing) → author the lab until the run is green. No lab is "done" with a red validator.
3. **SQL is code.** `helpdesk-schema.sql`, `resolve-ticket.sql`, `embed-kb.sql` are executed against a real 26ai ADB (Rick's tenancy) before being referenced by any lab — including the **run-twice idempotence test** (attendees re-run scripts when confused).
4. **Repo gates.** The repo's own `lintchecker`/`md-validator` and image-size workflow must pass locally before the PR.
5. **The test that matters.** Self QA = full click-through on a **real LiveLabs sandbox reservation**, timed, before WMS Self-QA-Complete. Week-of-event check: model IDs still valid, GenAI region catalog unchanged, common includes unchanged.

## 8. Process runway (LiveLabs publishing)

| Step | Owner | Latency |
|---|---|---|
| WMS submission (abstract §3, outline §4, tags) — **before content development** | Rick (Oracle-internal VPN) | council 2–3 business days |
| Sandbox Lite checkbox + (parallel) full-sandbox Jira + GenAI-in-sandbox verification | Rick / dev | 1 day + verify in week 1 |
| Lab development, TDD (§7) | inline, this project | ~1–2 weeks |
| Self QA on real sandbox → stakeholder QA | dev → stakeholders | +2 business days |
| PR to `oracle-livelabs/apex:main`, **WMS ID in PR title**, OCA signoff | Rick | ~1 business day review |
| Publishing entry (Workshop Time = 90 min, URLs) → live | Rick | ~1 business day |
| Event Code per developer day (if >30 seats or hidden bundle wanted) | Rick | 2 + 1 business days |
| **Quarterly QA every 90 days or the workshop is pulled** | assign owner now | recurring |

End-to-end: **~2–4 weeks** — schedule the first developer day accordingly.

## 9. Risks and mitigations

| Risk | Likelihood | Mitigation |
|---|---|---|
| OCI GenAI blocked/limited in LiveLabs sandbox compartments | Low (nyc-genai-lab proves the pattern) but **must verify week 1** | OpenAI `type` path with event-provided key; instructor-tenancy demo as last resort |
| >30 attendees vs sandbox concurrency cap | Depends on event size (open Q1) | Event Code + tenancy variant on event tenancy; pre-negotiate capacity |
| 429 throttling on shared-tenancy GenAI | Medium at 30 seats | Max AI Tokens quotas, staggered lab design, retry guidance, OpenAI relief valve |
| Model ID deprecation between QA and event | High over months | "Pick latest chat model" instruction, banned-ID validator check, week-of-event verification, quarterly QA |
| AI output variance breaks lab continuity | Certain (it's generative) | Canonical DDL checkpoint (Lab 2), blueprint checklist (Lab 3), "your app may differ" fallback boxes, deterministic seed data |
| OCI API-key dance stalls the room (~10 error-prone min) | Medium | Dedicated Lab 1 with per-step screenshots + instant Assistant test; full-sandbox upgrade could pre-stage it |
| Sandbox APEX version < 26.1 (agents/NL2IR labs break) | Low (rollout complete ~June 2026) | Verify in week-1 sandbox check; 24.2 fallback = "AI Configuration" chat instead of Agent+tools (degraded, documented) |
| Setup eats 15 min before first wow | Certain on Sandbox Lite | Instructor demo during provisioning; full-sandbox Jira upgrade path |
| Stale include paths across variants (nyc-genai-lab bug) | Medium | Validator resolves every path in every variant, CI-style |
| Quarterly QA lapse → catalog removal | Medium over a year | Named owner + calendar from day one (open Q3) |

## 10. Open questions for Rick

1. **Seat count per developer day?** Determines green-button-only vs Event Code + event tenancy track (§5).
2. **WMS access:** you submit under your Oracle identity — any co-authors/stakeholders to list?
3. **Quarterly QA owner** — you, or a teammate?
4. **Scope check:** keep both optional labs (6: Generate Text, 7: Vector Search), or cut one? Recommendation: keep both — they're the fast-lane for experts and neither blocks the core.
5. **App domain sign-off:** Help Desk (recommended) vs alternates (field-service dispatch, HR case tracker)?

## 11. Source documents

- `docs/research/2026-07-07-apex-developer-persona.md` — persona, segments, design rules
- `docs/research/2026-07-07-apex-ai-platform.md` — 26.1 feature set, sandbox feasibility per feature, gotchas
- `docs/research/2026-07-07-livelabs-apex-landscape.md` — catalog inventory, gap analysis, exemplar structures, sandbox mechanics, publishing process
- Rick's prior workshop (`rag-agents-oracle-ai-db` in `~/GitHub/developer`) and `sample-workshop` — structural conventions
