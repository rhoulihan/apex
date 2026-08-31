# Workshop Spec — "Build an AI-Powered Help Desk with Oracle APEX: From Prompt to Agent"

**Status:** **Approved by Rick 2026-07-08** — lab authoring may begin (inline, strict TDD per §7)<br>
**Date:** 2026-07-07 · rev 2 post adversarial review (27 findings) · rev 3 2026-07-08 delivery decisions (§10)<br>
**Author:** Claude (research: 3 agent reports in `docs/research/`, LiveLabs conventions report)
**Target repo:** `oracle-livelabs/apex` (this repo; develop on a fork branch, PR with WMS ID)<br>
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
| Stretch steps so experts never idle | Every core lab (1–5) ends with an optional "Go further" task; two optional labs at the end |
| One governance beat per AI feature | Token quotas you set yourself (Lab 1); "you review AI's SQL before running it" (Lab 2); "APEX never executes AI-generated SQL" (Lab 4); tool allow-list + user-approval confirmation on the write tool (Lab 5) |
| Data-egress callout per AI feature | Each AI lab states what does and does not leave the database (details in §4; summary in the Introduction) |
| Define AI terms, assume DB terms | Glossary beats: *token* (Lab 1), *RAG* + *agent/tool* (Lab 5), *embedding* (Lab 7); free use of *schema, workspace, PL/SQL* |
| Close with their actual learning trail | LiveLabs, APEX Office Hours, Insum Instant Tips, Cloud Nueva, apex.world — not "see GitHub" |

## 3. Workshop concept

- **Title (proposed):** *Build an AI-Powered Help Desk with Oracle APEX: From Prompt to Agent*
  Alternates: *From Prompt to Agent: Ship an AI Help Desk in 90 Minutes with Oracle APEX*; *Build and Govern an AI Agent App with Oracle APEX*.
- **Folder:** `ai-helpdesk-agent/`
- **App domain: IT Help Desk** ("Horizon Help Desk"). Rationale: universally understood by all three persona segments; enterprise-flavored (respects professional identity); a knowledge base is a *natural* RAG corpus; "resolve this ticket" is a natural governed agent action; and no existing workshop uses it (schools, events, CRM, procurement, bookstore, movies, expenses are taken).
- **Schema (3 tables, deterministic):** `TICKETS` (id, subject, description, status, priority, category, created_on, assigned_to), `KB_ARTICLES` (id, title, content, category, updated_on), `TEAM_MEMBERS` (id, name, role, email). Curated seed data ships in `files/`: ~50 tickets across statuses/categories and ~20 knowledge-base articles with concrete, memorable fixes (VPN error 812, printer spooler, MFA reset…) so every attendee's AI answers match the lab text.
- **Learning objectives** (WMS "Objectives"): after this workshop you can
  1. Connect APEX to a Generative AI provider, enable the APEX Assistant, and set token quotas on the service.
  2. Use AI to design a data model and generate a working application from a natural-language prompt.
  3. Add natural-language analytics to a report with AI Interactive Reports.
  4. Build a governed AI Agent with declarative tools (read data, act with user-approval confirmation) and embed it in your app.
  5. Explain how APEX keeps AI governed — human review of generated SQL, no AI-executed SQL, tool allow-lists, user-approval confirmations on write tools, token quotas — and what data is (and is not) sent to the model by each feature.
- **WMS prerequisites** (required submission field): a free Oracle.com account and a modern browser. No OCI tenancy, no local install; familiarity with SQL helpful but not required.
- **Narrative arc:** *Prompt → App → Trustworthy App.* Act 1: AI builds it with you. Act 2: AI works inside it, on your data. Act 3 (the through-line): you are the reviewer, the agent is governed — "AI as amplifier."
- **WMS tags:** Level: Beginner (Intermediate-friendly) · Role: Application Developer / DBA · Focus Area: Low Code, AI · Product: Oracle APEX, Autonomous AI Database.

## 4. Lab-by-lab breakdown (90-minute budget)

Timing model: LiveLabs Sandbox Lite — attendee logs into an assigned compartment and creates ADB + workspace themselves (the pattern of the four APEX sandbox workshops that provision their own ADB: nyc-genai-lab, ai-vision-lab, image-semantic-search, social-media-app; a pre-provisioned full sandbox is a possible upgrade, §5). Reservation set to 90 min in WMS; attendees can extend to 180 (manual, one click, ~1-hour increments — not automatic). **Core slot time = 87 min** (15 setup + 65 hands-on labs + 7 Take It Home); optional labs add 25 for fast attendees (110 max, inside the extendable reservation).

Manifest order follows the AI-workshop pattern in this repo (nyc-genai-lab, ai-vision-lab, image-semantic-search, social-media-app): **Introduction first, Get Started second, sign-up third** — validator-enforced (§7). (The sample-workshop template orders Get Started before Introduction; the AI workshops we model on do the reverse. We consciously pick the AI-workshop pattern; flip only if the LiveLabs council objects.)

| # | Lab | Time | Cumulative |
|---|---|---|---|
| — | Introduction (read now; revisit during ADB provisioning) | 0 | 0 |
| — | Get Started: sandbox login (CDN common lab) | 5 | 5 |
| — | Sign up for an APEX Workspace (common include: create Always Free ADB + workspace) | 10 | 15 |
| 1 | Connect APEX to Generative AI | 10 | 25 |
| 2 | Design the Data Model with AI | 10 | 35 |
| 3 | Generate the App from a Prompt | 10 | 45 |
| 4 | Ask Your Data Anything: AI Interactive Reports | 10 | 55 |
| 5 | Build the Help Desk AI Agent | 25 | 80 |
| 6 | OPTIONAL: Draft Replies with AI | 10 | (90) |
| 7 | OPTIONAL: Semantic Knowledge-Base Search with AI Vector Search | 15 | (105) |
| — | Take It Home: export your app + learning trail | 5 | **85 (core) – 110 (all optionals)** |

Optionals overflow the 90-min slot by design — the full path with both optionals plus Take It Home is 112 min, comfortably within the 180-min extended reservation. Both are marked OPTIONAL in the manifest title (established pattern: nyc-genai-lab Lab 7), and **each opens by instructing the attendee to extend the reservation first** (one click while it is still active). The §7 validator's budget check excludes OPTIONAL labs for exactly this reason.

**Live-event pacing:** while ADB provisions (~2–5 min), the instructor demos the finished app — this plants the wow before minute 10 and absorbs the provisioning wait. In self-paced mode the Introduction's finished-app tour fills the same gap.

### Introduction (0 min — read up front; revisit while ADB provisions)
Required content (this lab has acceptance criteria like any other):
1. About-this-workshop paragraph built from the §1 positioning sentence and the *Prompt → App → Trustworthy App* arc.
2. The explicit **"AI as amplifier, not replacement"** framing (§2): one sentence, plus "you review and approve what AI produces at every step."
3. **Finished-app tour** — 2–3 annotated screenshots or a short animated capture in `introduction/images/` — the self-paced substitute for the live instructor demo (medium decided at dev time).
4. One-paragraph data-egress summary: NL2IR sends schema/report metadata only; the agent's Retrieve Data tools and Generate Text send query results/ticket text as model context; vector search sends KB article text to the embed model; nothing else leaves the database.
5. Workshop-level Objectives (the five §3 objectives verbatim), Prerequisites (browser + free Oracle account), total Estimated Time (90 min), and the Lab/Title/Duration overview table (repo convention).

### Get Started + Sign up for an APEX Workspace (common includes, 15 min)
Manifest entries only — no authored content: CDN `cloud-login/cloud-login-livelabs2.md`, then `common-261/1-sign-up-apex/sign-up-apex-sandbox.md` (attendee creates Always Free ADB — APEX preinstalled — and a `DEMO` workspace). **Path ground truth (verified 2026-07-07): `common-latest` has no sandbox flavor of the sign-up lab** (it holds only `1-sign-up-apex.md` and `create-adb-livelabs.md`); the sandbox flavor exists in `common-242` (pinned by nyc-genai-lab, image-semantic-search, social-media-app) and `common-261` — use `common-261` as the newest resolvable pin, and at dev time check whether a newer `common-*` has added it before pinning. The include's own Estimated Time header says 5 min; we budget 10 (provisioning wait) — the validator's time source for includes is a config override, not the header (§7). The sign-up lab's provisioning-wait step should say: "while the database provisions, skim the Introduction (or watch the instructor demo at a live event)."

### Lab 1: Connect APEX to Generative AI (10 min)
- **Tasks:** (1) Generate an OCI API key pair for the sandbox user; collect **user, tenancy, and assigned-compartment OCIDs** — the compartment OCID is *not* in the API-key config file; in the sandbox it comes from the reservation's assigned-compartment details (per-step screenshot). (2) Create the Generative AI service in Workspace Utilities: OCI Generative AI, region `us-chicago-1`, current model (instruction says "pick the latest available chat model" — never a hardcoded deprecated ID), **"Used by App Builder" ON** (the classically missed toggle — screenshot + warning box). (3) *Governance beat #1 + glossary:* define **token** ("the unit LLMs read and bill by") and set the **Max AI Tokens** quota on the service you just created — you cap your own AI spend/usage declaratively. (4) Instant feedback: ask APEX Assistant a question from SQL Workshop to prove the wiring.
- **Provider fallback:** `type` conditional (nyc-genai-lab Lab 3 pattern): `OCIGenAI` (default) / `OpenAI` (bring-your-own key; event-provided key at instructor-led deliveries — logistics in §5) in the *same* lab file. Caution box on the OpenAI track: your prompts and any data the AI features send as context go to a third party — fine for this workshop's synthetic seed data; evaluate for your own apps.
- **Adapt, don't fork:** start from `common-261/2-configure-ai-keys` content; if it fits verbatim, include it directly from the manifest and this lab shrinks to a wrapper around tasks 3–4.
- **Go further (stretch):** ask the Assistant to *explain* a PL/SQL block (segment-a candy).

### Lab 2: Design the Data Model with AI (10 min)
- **Tasks:** (1) Open Create Data Model with AI; paste the provided prompt ("help desk for an IT team: tickets, knowledge-base articles, team members…"). (2) **Review** the SQL the AI proposes — the lab calls out what to check (keys, data types, naming). *Governance beat #2: you are the reviewer.* **Do not execute the wizard's proposed SQL** — close the wizard after review (callout explains why: the room stays in sync on the vetted version; the wizard's terminal action saves a script, so simply don't run it). (3) Run the **canonical DDL + seed data script** (copy block + `files/helpdesk-schema.sql`): framed as "run the reviewed, vetted version" — this both teaches the review habit and guarantees deterministic downstream labs (AI output varies per attendee; lab text and screenshots must not). Recovery note in the lab: "if you already ran the AI's script, the canonical script replaces those tables."
- **Script contract:** `helpdesk-schema.sql` is a **state-reset checkpoint**, not merely idempotent — it drops (with existence handling) and recreates all three tables, then seeds, so the canonical schema wins regardless of what an attendee did first. Tested accordingly (§7).
- **Go further:** ask APEX Assistant to write an analytic query (tickets by category, trend) and run it.

### Lab 3: Generate the App from a Prompt (10 min)
- **Tasks:** (1) Create App with AI over the existing tables, provided prompt. (2) **Blueprint checklist** before clicking Create: must include Dashboard, **Tickets as an Interactive Report** (+ form), Knowledge Base — verify the Tickets page *type* is Interactive Report in the blueprint editor, since Lab 4's NL2IR exists only on Interactive Report regions; add or retype any missing page declaratively. (3) Create, run, log in: **a real web app with auth at a real URL — the act-one payoff.** (4) 2-minute guided tour mapping what got generated to APEX concepts (pages, regions — vocabulary for the rest of the labs).
- **Fallback box (concrete):** "Your generated app may differ — that's the point of generative AI. You need (a) a Tickets Interactive Report page and (b) a Knowledge Base report page; here's how to add either in 60 seconds with Create Page."
- **Go further (stretch):** use **Create Page with natural language** (26.1-new — even segment (a) hasn't seen it) to add a page the blueprint didn't include, e.g. a team-workload chart over TEAM_MEMBERS, then inspect what got generated.

### Lab 4: Ask Your Data Anything — AI Interactive Reports (10 min)
- **Tasks:** (1) Open the Tickets Interactive Report. *(Recovery step, 60 s, mirroring `ai-interactive-report-lab`: no IR on Tickets? Create Page → describe it in natural language: "an interactive report on the TICKETS table.")* (2) Enable AI on the IR (26.1 NL2IR). (3) Prompt it: "show open tickets by priority as a chart", "group by category, oldest first" → watch filters/charts land as **removable declarative chips**. (4) *Governance beat #3*, in a callout: APEX never executes AI-generated SQL — the AI maps intent onto the same declarative IR settings you could click by hand; chips are inspectable and reversible. **Data egress:** NL2IR sends schema/report metadata and your prompt — not your rows.
- **Go further:** column-level AI attributes (per `ai-interactive-report-lab`); second/third NL prompts.

### Lab 5: Build the Help Desk AI Agent (25 min — the marquee)
Budget evidence: `scm-ai-agent` (Oracle's own 26.1 agent workshop, prebuilt app) spends ~15 min on "agent + two tools" and ~4–5 min per additional tool/task; six tasks at that cadence is 25 min, not 20.
- **Tasks:** (1) Create an **AI Agent** (26.1 shared component; note it evolved from 24.2 "AI Configurations"): system prompt = help-desk analyst persona; welcome message. (2) Attach **AI Tool: Retrieve Data** over tickets (SQL source) — *define RAG in one callout sentence here, and define agent/tool as you go.* (3) Attach a second Retrieve Data tool over KB articles (the payoff conversation depends on it). (4) Attach **AI Tool: Execute Server-side Code** — `resolve_ticket(p_ticket_id)` (provided ~10-line PL/SQL ending with `apex_ai.set_tool_result` so the agent learns the outcome) — and under **User Approval** toggle **Requires Confirmation** ON, with a Confirmation Title/Message ("Resolve ticket &TICKET_ID.?"); the user sees Approve/Cancel, and Cancel skips the tool. (Conceptually these are "guardrails," but lab text and screenshots must use the real builder labels — User Approval → Requires Confirmation — not the blog term.) (5) Add the **Show AI Assistant** dynamic action to the app (floating chat). (6) The payoff conversation, scripted in the lab: *"A user reports VPN error 812 — any KB fix?"* (agent retrieves the article) → *"Are there open tickets about it?"* (agent queries tickets) → *"Resolve ticket 42"* → **confirmation prompt appears** → approve → row updated. *Governance beat #4: the agent can only use tools you attached, and writes require your approval.* **Data egress callout:** the Retrieve Data tools' query results ARE sent to the model as context — governance here means you scope the SQL each tool can run (plus OCI GenAI's on-demand no-retention posture); contrast with Lab 4's metadata-only NL2IR.
- **Live-event contingency:** if the room is behind at minute 60, the instructor drives tasks 5–6 from the podium while attendees follow — governance beat #4 and Take It Home are never cut.
- **Go further:** add a third tool (create ticket), tune the system prompt, ask the agent something outside its tools and observe the refusal.

### Lab 6 (OPTIONAL, extend reservation first): Draft Replies with AI (10 min)
- Generate Text with AI dynamic action on the ticket form: draft a customer-facing reply from the ticket description (+ relevant KB article as context), editable before save — the "AI drafts, human sends" pattern attendees can lift straight into their own apps. (Egress: the ticket text is sent as context — same callout pattern as Lab 5.)

### Lab 7 (OPTIONAL, extend reservation first): Semantic Knowledge-Base Search with AI Vector Search (15 min)
- **Mechanism (corrected to the repo's canonical Search Configuration pattern — nyc-genai-lab Lab 7):** (1) Create an APEX **Vector Provider** in Workspace Utilities. (2) `files/embed-kb.sql` adds a `VECTOR` column and embeds the 20 KB articles via `apex_ai.get_vector_embeddings(p_value => …, p_service_static_id => '<provider_static_id>')` — note `apex_ai` needs an APEX session context, so the script runs from SQL Workshop (or wraps `apex_session.create_session` when tested via SQLcl — §7). (3) Create a **Search Configuration**, Search Type **Oracle Vector Search**, selecting the same Vector Provider (it embeds the user's query at runtime); build the search page. (4) The wow: "laptop won't connect from hotel wifi" finds the VPN article with zero keyword overlap. Defines *embedding* in one callout.
- **Cross-track dependency (hard requirement):** an OCI-GenAI-type Vector Provider reuses Lab 1's OCI web credential — attendees on Lab 1's **OpenAI track have no OCI key**. Whichever approach ships must work on both provider tracks. Options, decided at dev time: **(a) preferred — in-database ONNX embedding** (`DBMS_VECTOR.LOAD_ONNX_MODEL` + provider type "Database ONNX Model", the nyc-genai-lab precedent: no external credential, works on both tracks, immune to GenAI throttling); (b) make Lab 7 `type`-conditional like Lab 1; (c) ship pre-computed vectors in the seed data and keep live embedding as a stretch step.
- Clearly marked OPTIONAL; nothing downstream depends on it. This is the segment-(a) magnet and the 26ai tie-in.

### Take It Home (7 min)
- Export the app (and note APEXlang/SQLcl as the modern export for source control — one paragraph, no exercise); download links for all scripts; **the sandbox is wiped at reservation end** (warning box); "run this again free": apex.oracle.com + Always Free; one-paragraph recap tying the five governance mechanisms together (objective 5); learning trail (LiveLabs catalog, APEX Office Hours, Insum Instant Tips, Cloud Nueva, apex.world); pointers to the tenancy-only sequels (scm-ai-agent, crm-apexlang) as "your next workshop."

## 5. Environment design

**Primary: LiveLabs Sandbox Lite** (green button). Auto-created in 1 business day via WMS checkbox; attendee gets an isolated compartment in a LiveLabs-owned tenancy; creates own ADB + workspace (15 min, common includes). No infra-team dependency — this is the ship-now path, matching the four current APEX sandbox workshops that use the shared sign-up-apex-sandbox lab.

**Upgrade path (parallel, non-blocking): full LiveLabs Sandbox** via Jira from the WMS Sandbox Environment tab — pre-provisioned ADB + workspace would claw back ~10 minutes and move the first wow before minute 20 (persona ideal). **Precedent exists in this repo:** `apex-native-map-regions`' sandbox variant runs on a full pre-provisioned LiveLabs environment (pre-created resources; attendees still create the workspace) — cite it in the Jira request, noting our ask goes one step further (pre-built ADB + workspace). A pre-provisioned environment also lets the LiveLabs team pre-stage the Max AI Tokens quota centrally. The workshop must not depend on this landing.

**The critical unknown to burn down first: OCI GenAI availability from LiveLabs sandbox compartments.** Evidence says yes (nyc-genai-lab's green-button variant configures OCI GenAI in-sandbox), but this gets verified **in week 1 of development** with a real sandbox reservation, before any lab content is written. Documented fallback either way: the OpenAI `type` path.

**OpenAI fallback logistics (it is load-bearing in three places — Lab 1 type path, GenAI-blocked risk, 429 relief valve):** at instructor-led events, use a per-event OpenAI key with a hard spend cap, distributed via the Event Code page or on-screen at the venue (never baked into lab content), revoked immediately after the event. Self-paced catalog users on the OpenAI track bring their own key (stated plainly in Lab 1); the "nothing but a free Oracle account" promise holds on the default OCI GenAI track.

**Variants shipped:** `workshops/sandbox/` (green, Track A primary), `workshops/tenancy/` (brown — **first-class, not a twin**: it is the Track B large-event backbone and gets equal Self-QA; swaps the setup includes for freetier login/provision labs and `need-help-freetier.md`), and `workshops/event/` re-cuts per developer day (established `tenancy-special`/`aiw25` pattern; first one authored alongside launch so the Track B path is rehearsed, not improvised). Single-source lab content; variance only in manifests and `type` conditionals — **every include path must resolve in every variant** (validator-enforced).

**Concurrency plan for developer days (DECIDED 2026-07-08 — plan for large groups):** most events are ≤30 seats, but **some will be hundreds**. Two first-class delivery tracks, both shipped and QA'd from day one:

- **Track A — green button (≤30 seats, and all self-paced use):** sandbox as-is; attendees start reservations at t-0 (provisioning is minutes).
- **Track B — large events (hundreds of seats):** **Event Code** in WMS (2-day review) pointing at an event manifest, backed by the **tenancy variant on an event-provided tenancy** — the established bootcamp pattern (`tenancy-special` in bootcamp_crm / event-mangement). Capacity = tenancy limits, so the pre-event runbook (§6) must cover, per event: (1) event-tenancy service limits — ADB instance count for N attendees (or pre-provisioned shared instances with per-attendee workspaces, the bootcamp approach); (2) **OCI GenAI throughput at hundreds of concurrent users** — pre-negotiate limits for the event tenancy or shard attendees across compartments/regions; at this scale the 429 mitigations below are load-bearing, not defensive; (3) the per-event OpenAI relief-valve key (logistics above); (4) event-code issuance timing (request ≥1 week out; code active from 1 day before to 1 day after). Sandbox-capacity pre-negotiation with the LiveLabs team remains a fallback for mid-size events (research cites livelabs-help-db_us@oracle.com; **confirm the current alias in WMS before the request** — one review verdict disputed it).

**Throttling defense (any variant):** OCI GenAI on-demand inference is dynamically throttled per tenancy — 30–50 people in one tenancy can see 429s. Mitigations designed in: **attendee-set Max AI Tokens on the GenAI service (Lab 1 step 3)** — per-workspace caps on Sandbox Lite are necessarily attendee-side, since each attendee is their own instance admin; labs alternate clicky tasks with AI calls (natural staggering); the scripted agent conversation is 3 calls, not 20; troubleshooting box in every AI lab ("if you get a rate-limit error, wait 30s and retry"); OpenAI fallback path as pressure relief.

## 6. Repo deliverables (target structure)

```
ai-helpdesk-agent/
├── introduction/introduction.md          # content contract in §4; + images/ (finished-app tour)
├── 1-connect-genai/1-connect-genai.md    # type-conditional OCIGenAI/OpenAI (or common-261 include + wrapper)
├── 2-data-model-ai/2-data-model-ai.md    # + files/helpdesk-schema.sql (drop-and-recreate + seed: state-reset checkpoint)
├── 3-generate-app/3-generate-app.md
├── 4-ai-interactive-report/4-ai-interactive-report.md
├── 5-ai-agent/5-ai-agent.md              # + files/resolve-ticket.sql (ends with apex_ai.set_tool_result)
├── 6-generate-text/6-generate-text.md    # OPTIONAL
├── 7-vector-search/7-vector-search.md    # OPTIONAL + files/embed-kb.sql (Vector Provider pattern, §4)
├── 8-take-it-home/8-take-it-home.md      # + finished app export zip
└── workshops/
    ├── sandbox/{index.html,manifest.json}   # Track A (green button)
    ├── tenancy/{index.html,manifest.json}   # Track B backbone (brown button) — equal QA priority
    └── event/{index.html,manifest.json}     # first event re-cut, authored alongside launch
```

**Additional deliverable — large-event runbook** (`docs/event-runbook.md`, kept with the spec, not shipped in the workshop PR): per-event checklist for hundreds-scale delivery — event-tenancy sizing (ADB count or shared pre-provisioned instances + workspaces), OCI GenAI limit pre-negotiation / compartment-or-region sharding, Event Code request timeline, OpenAI relief-valve key issuance + revocation, day-of instructor contingencies (Lab 5 podium-drive rule), and post-event teardown.

Conventions (from `sample-workshop` + repo lint, validator-enforced): lowercase filenames; one folder per lab with `images/` (+ `files/`); lab skeleton `# Title → ## Introduction → Estimated Time → ### Objectives → ### Prerequisites → ## Task 1..N → ## Learn More → ## Acknowledgements`; `<copy>` on every code block; alt text on every image; image sizes within the repo's `enforce-image-size` workflow limits; manifest lab titles `Lab N: <imperative>`; "Need Help?" CDN include last; help email `livelabs-help-apex_us@oracle.com` (manifest `help` field).

**Screenshot standards:** all screenshots captured inside a **real LiveLabs sandbox reservation** (fold into the §5 week-1 verification or the §7 Self-QA reservation) so console chrome, compartment names, and region pickers match what attendees see — never from Rick's tenancy. Pick one APEX theme mode for every new capture, deciding together with the `common-261/2-configure-ai-keys` include question (that lab's screenshots are Dark Mode / APEX 26.1 — match it if included verbatim), and state the mode in the Introduction. Redaction: never capture the private-key download or key contents; blur tenancy names, OCIDs, and key fingerprints in every image. Consistent browser window size within the image-size limits.

## 7. Development methodology — inline, strict TDD

All development happens inline (no delegated authoring). TDD for a content deliverable means **executable checks exist before the content they check**, and the cycle is red → green → refactor:

1. **Harness first.** Build `tools/validate_workshop.py` (stdlib-only) + a pytest suite covering the validator itself, before any lab is written. Checks: manifest parses and conforms (title, help email, **exact ordering: Introduction #1, Get Started #2, sign-up #3, "Need Help?" last** — per the consciously chosen AI-workshop pattern, §4); **every `filename` resolves** — local, `common-*`, and CDN URLs (HTTP 200) — in **every** variant; per-lab structural rules (single H1, Estimated Time, Objectives, Acknowledgements, `<copy>` on fenced code, images exist + alt text); **time-budget check: sum of non-OPTIONAL manifest entries ≤ 90 min per variant** (entries whose title contains "OPTIONAL" are excluded from the hard check but counted in a warning-level total that must stay ≤ 180, the extension cap); time source is the Estimated Time header for locally authored labs and **per-variant config overrides for CDN/common includes** (headers we cannot edit; seeded from the §4 table — reconcile the sign-up row's 10 min budget vs the include's declared 5 at dev time); **banned-strings list** (deprecated model IDs, hardcoded OCIDs, "23ai" where "26ai" is meant, "Guardrail" as a UI label, TODO/TBD).
2. **Red-green per lab.** Add the manifest entry + any lab-specific validator expectations first (validator fails: file missing) → author the lab until the run is green. No lab is "done" with a red validator.
3. **SQL is code.** `helpdesk-schema.sql`, `resolve-ticket.sql`, `embed-kb.sql` are executed against a real 26ai ADB (Rick's tenancy) before being referenced by any lab. Tests: run-twice (state-reset semantics — second run reproduces the canonical state); **divergent-precondition** (execute a sample AI-wizard output first, then the canonical script; assert the canonical schema and seed win — e.g., ticket 42 exists with expected columns); `embed-kb.sql` runs in an APEX session context (SQL Workshop, or `apex_session.create_session` under SQLcl).
4. **Repo gates.** The repo's own `lintchecker`/`md-validator` and image-size workflow must pass locally before the PR.
5. **The test that matters.** Self QA = full click-through on a **real LiveLabs sandbox reservation**, timed, before WMS Self-QA-Complete — including the image-redaction check (no unredacted OCIDs/tenancy identifiers/key material in any screenshot; the validator scans markdown only and cannot see images). Week-of-event check: model IDs still valid, GenAI region catalog unchanged, common includes unchanged.

## 8. Process runway (LiveLabs publishing)

| Step | Owner | Latency |
|---|---|---|
| WMS submission (abstract, prerequisites, tags §3; outline §4) — **before content development** | Rick (Oracle-internal VPN) | council 2–3 business days |
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
| OCI GenAI blocked/limited in LiveLabs sandbox compartments | Low (nyc-genai-lab proves the pattern) but **must verify week 1** | OpenAI `type` path (event key logistics §5); instructor-tenancy demo as last resort |
| Hundreds-seat events exceed sandbox capacity | **Certain for some events (decided)** | Track B is first-class: Event Code + tenancy variant on event tenancy, rehearsed via the event runbook (§6) |
| 429 throttling on shared-tenancy GenAI | Medium at 30 seats; **high at hundreds** | Attendee-set Max AI Tokens (Lab 1), staggered lab design, retry guidance, OpenAI relief valve; Track B: pre-negotiated GenAI limits / compartment-or-region sharding (§5) |
| Model ID deprecation between QA and event | High over months | "Pick latest chat model" instruction, banned-ID validator check, week-of-event verification, quarterly QA |
| AI output variance breaks lab continuity | Certain (it's generative) | State-reset canonical script (Lab 2), blueprint checklist pinning the Tickets IR page type (Lab 3), Lab 4 NL recovery step, "your app may differ" fallback boxes, deterministic seed data |
| Lab 7 embed path breaks for OpenAI-track attendees | Certain on that track, if OCI-only | Track-independence is a hard requirement: ONNX in-database preferred / type-conditional / pre-computed vectors (§4 Lab 7) |
| OCI API-key dance stalls the room (~10 error-prone min) | Medium | Dedicated Lab 1 with per-step screenshots (incl. compartment OCID) + instant Assistant test; full-sandbox upgrade could pre-stage it |
| Sandbox APEX version < 26.1 (agents/NL2IR labs break) | Low (rollout complete ~June 2026) | Verify in week-1 sandbox check; 24.2 fallback = "AI Configuration" chat instead of Agent+tools (degraded, documented) |
| Setup eats 15 min before first wow | Certain on Sandbox Lite | Instructor demo during provisioning; Introduction finished-app tour (self-paced); full-sandbox Jira upgrade path |
| Stale include paths across variants (nyc-genai-lab bug; we nearly shipped one — see rev-2 changelog) | Medium | Validator resolves every path in every variant, CI-style |
| Quarterly QA lapse → catalog removal | Medium over a year | Named owner + calendar from day one (open Q3) |

## 10. Decisions (answered by Rick, 2026-07-08)

1. **Seat count:** plan for large groups — most events ≤30, **some in the hundreds** → dual-track delivery (§5): green button for ≤30/self-paced, Event Code + tenancy variant on event tenancy for hundreds; tenancy variant and event runbook are first-class deliverables.
2. **WMS access:** submitted under Rick's Oracle identity.
3. **Quarterly QA owner:** Rick.
4. **Scope:** keep both optional labs (6: Generate Text, 7: Vector Search).
5. **App domain:** Help Desk approved — "perfect choice for this audience."

## 11. Source documents

- `docs/research/2026-07-07-apex-developer-persona.md` — persona, segments, design rules
- `docs/research/2026-07-07-apex-ai-platform.md` — 26.1 feature set, sandbox feasibility per feature, gotchas
- `docs/research/2026-07-07-livelabs-apex-landscape.md` — catalog inventory, gap analysis, exemplar structures, sandbox mechanics, publishing process (note: its recommendation #3 named a `common-latest` sandbox include that does not exist — corrected here and flagged in that file)
- Rick's prior workshop (`rag-agents-oracle-ai-db` in `~/GitHub/developer`) and `sample-workshop` — structural conventions
- Repo ground truth consulted during review: `nyc-genai-lab/7-vector-search`, `scm-ai-agent/3-…/4-…` (agent + tools timings, User Approval settings), `common-261/`, `apex-native-map-regions`

### Rev-2 changelog (adversarial review, 2026-07-07)

27 verified findings applied; highlights: Lab 5 rebudgeted 20→25 min (scm-ai-agent evidence) with live-event contingency; Lab 7 mechanism corrected to APEX Vector Provider + `apex_ai.get_vector_embeddings` + Search Configuration, with cross-track (OpenAI) dependency made a hard requirement; sign-up include corrected from nonexistent `common-latest/...sign-up-apex-sandbox.md` to `common-261`; manifest ordering fixed to the AI-workshop pattern and validator-enforced; "Guardrail" replaced with the real User Approval → Requires Confirmation setting (+ `apex_ai.set_tool_result` in the tool); data-egress governance beat added workshop-wide; Lab 3 blueprint now pins the Tickets Interactive Report page type with a Lab 4 recovery step; canonical script upgraded from "idempotent" to drop-and-recreate state-reset with divergent-precondition test; token/Max-AI-Tokens got a teaching home (Lab 1) matching objective 5; timing arithmetic corrected (core 85, full path 110, manual reservation extension); Introduction and screenshot standards given explicit acceptance criteria; capacity-email alias hedged (conflicting verifier verdicts) — confirm in WMS.
