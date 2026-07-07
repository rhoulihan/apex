# LiveLabs APEX Workshop Landscape — Research Report (July 2026)

> Research agent report commissioned for the APEX + AI LiveLabs workshop spec.
> Method: full inventory of the cloned `oracle-livelabs/apex` repo (this repo, 66 workshop folders) + web research on LiveLabs mechanics and publishing. Research date: July 7, 2026.

Variant naming note: `sandbox` and the older `livelabs` folder name are both the **green button** variant; `tenancy` = brown button ("Run on Your Tenancy"); `freetier` = older brown-button convention; `desktop` = noVNC remote desktop; `ocw*`/`aiw25`/`tenancy-special` = event-specific manifests (Oracle CloudWorld, AI World, bootcamps).

## 1. Inventory: oracle-livelabs/apex

Boilerplate labs ("Introduction", "Get Started", "Need Help?") omitted from lab lists.

| Folder | Title | Variants | Labs (core) | AI? |
|---|---|---|---|---|
| ai-interactive-report-lab | Build an AI Interactive Report in Oracle APEX | tenancy | Create SCM app; Configure GenAI service; IR with natural language; column-level AI attributes; Search with AI; IR Chat Assistant; dictation (opt) | **Yes** |
| ai-vision-lab | Build AI-Powered Image Search into your Oracle APEX App | **sandbox**, tenancy, ocw24 | Configure OCI API keys; import Social Media app; integrate OCI Vision; run app; mobile features | **Yes** |
| ai-world-hol-apex | Build Intelligent APEX Apps with OCI Gen AI and Your Oracle Data | freetier | Deploy ADB + workspace; configure GenAI; APEX app + AI chatbot; extend with Llama/Grok models | **Yes** |
| apex-integration | (template title placeholder) | desktop, freetier, **livelabs** | Provision instance; setup env; load data; query data | No |
| apex-native-map-regions | Plotting EV Charging Points with APEX Native Map Regions | **sandbox**, ocw23-sandbox | Init LiveLab env; change password/start ORDS; DB objects; create workspace; native map regions | No |
| apex-professional-consolidated | Oracle APEX Hands-On Labs Guide | tenancy | Consolidated pointer to HOL series | No |
| apex-professional-hol1…hol22 (21 folders) | APEX Professional certification HOL series | tenancy only | 1–10 labs each (SQL Workshop, Create App, Reports, Grids, Dynamic Actions, Forms, Security, PWA, Workflows, …) | No |
| apex-workflows | Simplify Business Process Management Using APEX Workflows | tenancy | 11 workflow labs | No |
| approvals-component | Build an Expense Tracker Application | tenancy | Expense tracker; task definition; email template; manage tasks | No |
| atp-apex-oda | Extend your application with advanced chat-bots | freetier, freetier2 | ADB; workspace + REST API; Oracle Digital Assistant; custom component; DA skill | Adjacent (ODA, pre-GenAI) |
| book-club-lab | Build a Book Club Application | freetier, ocw-/ocw23-livelabs+freetier | 10 labs: REST data source, search/details pages, library, ratings & reviews | No |
| bootcamp_crm | Build an AI-Powered CRM App with Oracle APEX | tenancy, tenancy-special | Configure GenAI service; **data model via AI**; **build app via AI**; AI chatbot; external data; custom auth/authz | **Yes** |
| build-low-code-apps | Modernize and Extend Legacy Apps in the Oracle Cloud | freetier, **livelabs** | Microservices, Kubernetes, APEX CI/CD | No |
| crm-apexlang | Build and Enhance a CRM App Through Spec-Driven Development with AI and APEXlang | tenancy | CRM schema; generate metadata from spec; deploy/customize; GenAI service; APEXlang skills | **Yes** (July 2026, newest) |
| crm-app | Build a CRM Application using Oracle APEX | tenancy | Quick SQL; forms; faceted search; heat map; workflow; dashboard | No |
| custom-auth-apex | Implement custom authentication in APEX | **sandbox**, tenancy, desktop | Custom auth scheme; self-service accounts | No |
| developer-live | Advanced Low Code Development with Oracle Autonomous Database | freetier, **livelabs** | 11 labs: workspace, spreadsheet app, faceted search, data structures, regeneration | No |
| employee-onboarding | Employee Onboarding with Oracle APEX | **sandbox**, tenancy, desktop | 11 labs: workflows, task definitions, workflow pages | No |
| event-mangement *(sic)* | **Build an AI-Powered Event Management App in 60 Minutes with Oracle APEX** | tenancy, tenancy-special | Configure GenAI service; data model via AI; create app via AI; enhance UI with AI; **AI chat assistant**; generate text with AI; charts via AI (opt) | **Yes** |
| existing-tables | Creating an App based on Existing Tables | freetier, **livelabs** | Sample tables; create/regenerate app; improve dashboard | No |
| forms-to-apex family (4 folders) | Forms modernization/migration | tenancy or freetier+**livelabs** | Forms analysis, mapping, migration | No |
| image-semantic-search | Implementing Image and Text Semantic Search in Oracle APEX | **sandbox**, tenancy, aiw25 | Import app; load ONNX model; **vector providers**; text+image semantic search | **Yes** |
| intro-to-javascript | JavaScript for APEX Developers | freetier, **livelabs** | JS basics; JS in APEX; DOM/jQuery | No |
| ja-jp-* (5 folders) | Japanese translations | freetier + **livelabs** | mirror originals | No |
| low-code-development | Low Code Development with Oracle Autonomous Database | freetier, **livelabs** | Spreadsheet app; DB objects; modify app | No |
| manage-offensive-behavior | Manage Offensive Behavior Using AI Language, Speech, and Video | tenancy | OCI Data Science notebook; jobs; APEX analysis UI | **Yes** (OCI AI services) |
| mle-javascript | APEX + Server-Side JavaScript | **sandbox**, livelabs, freetier, freetier1 | Spreadsheet app; JS pseudo-code; MLE modules | No |
| movies-lab | Build a Movies Watchlist Application | freetier, ocw-/ocw23-* | 10 labs incl. optional **vector search page** | Partially |
| nyc-genai-lab | **Build an Innovative Q&A Interface Powered by Generative AI with Oracle APEX** | **sandbox**, tenancy | Create app; map region; **configure GenAI service (OCI GenAI / OpenAI)**; conversational inquiry via GenAI; generate email via GenAI; optional **RAG with AI Vector Search** | **Yes** |
| object-storage-workflow | APEX App to manage files in OCI Object Storage | freetier, ocw23-sandbox, ocw23-tenancy | Task definitions; REST data source; Object Storage | No |
| oci-document-understanding | Automate Invoice Handling using APEX and OCI Document Understanding | tenancy | OCI keys/bucket; Document Understanding; invoice tracker; approvals | **Yes** |
| oci-rag-agent | Enhance your Oracle APEX App with Document-Aware Generative AI Agents | tenancy | Knowledge base + **OCI GenAI Agent**; REST data source; chat UI | **Yes** |
| online-bookstore-app | Build your own Online Bookstore App with Oracle APEX | tenancy | 18 labs incl. AI-Assistant chat widget, AI Vision book search, vector search | Partially |
| proof-of-concept | **Smart Project Management App with AI-Assisted Development in Oracle APEX** (LiveLabs wid 633) | tenancy, tenancy-special | AI data model; create app via GenAI; regenerate; generate text via AI; **AI chat assistant**; **vector search page** | **Yes** |
| rag-apex-app | Analyze Document store with RAG on Oracle APEX | freetier | GenAI agents backend; upload/ingest agent; **RAG chatbot** in low-code APEX | **Yes** |
| remote-data-source | Building an App using a Remote Data Source | freetier, **livelabs** | Table; report; charts | No |
| rest-data-source | Building an App using REST Data Sources | freetier, **livelabs** | REST-enable objects; REST sources; pages; LOV | No |
| sample-workshop | (template) | sandbox, tenancy, desktop | Template labs incl. variables demo | No |
| scm-ai-agent | **Build an AI Procurement Agent in Oracle APEX** | tenancy, desktop | Import data model/app; configure GenAI; **build AI Agent with context tools**; supplier-eval + PO tools; run agent in app | **Yes** (July 2026) |
| shopping-cart | Build a Starter Online Shopping App with Oracle APEX! | freetier, **livelabs** | 11 labs incl. AI generative text/chat assistant + vector search | Partially |
| social-media-app | Build a Social Media App using Oracle APEX | **sandbox**, tenancy | Data model; developer tools; cards; actions; dynamic actions; map | No |
| spreadsheet | Converting your Spreadsheet into a Cloud App | freetier, **livelabs** | Spreadsheet app; faceted search; report/form; map + PWA | No |

**Non-workshop support folders:** `common-242/`, `common-261/`, `common-latest/`, `apex-professional-common/` (shared, version-pinned labs: "Sign up for an APEX Workspace" incl. a `sign-up-apex-sandbox.md` sandbox flavor, "Configure AI keys", "APEX basics terminology"); `apex-242/` (empty); `cicd-workflow/` (non-standard layout, manifest under `workshop/freetier/`).

## 2. Gap Analysis

### AI-focused APEX workshops that already exist

In this repo: **15 AI-related workshops** (see table). In the live catalog: [Document-Aware GenAI Agents, wid 4190](https://livelabs.oracle.com/ords/r/dbpm/livelabs/view-workshop?wid=4190), [Smart Project Management App with AI-Assisted Development, wid 633](https://livelabs.oracle.com/ords/r/dbpm/livelabs/view-workshop?wid=633), [Q&A Interface Powered by GenAI (nyc-genai-lab)](https://oracle-livelabs.github.io/apex/nyc-genai-lab/workshops/tenancy/index.html), [AI Vision image search](https://oracle-livelabs.github.io/apex/ai-vision-lab/workshops/tenancy/index.html), plus the [Build an AI-Powered Event Management App in 60 Minutes blog/LiveLab](https://blogs.oracle.com/apex/build-an-ai-powered-event-management-app-in-60-minutes-with-oracle-apex).

### The decisive pattern: AI content and the green button barely overlap

- **Only 3 AI workshops have a sandbox (green-button) variant**: `nyc-genai-lab`, `ai-vision-lab`, `image-semantic-search` — and all three are *feature-integration* labs (Q&A widget, OCI Vision, ONNX vector search) grafted onto an imported/pre-built app.
- **Every "build an app with AI-assisted development" workshop is brown-button only** (`tenancy`/`freetier`): event-mangement (60-min AI Assistant end-to-end build), bootcamp_crm, proof-of-concept, ai-interactive-report-lab, scm-ai-agent (AI Agent + tools, updated July 2026), crm-apexlang (spec-driven AI dev, July 2026), ai-world-hol-apex, oci-rag-agent, rag-apex-app, oci-document-understanding.
- The tenancy-only AI workshops require the attendee to bring an OCI account with GenAI access or a paid/free-tier tenancy — the #1 friction point for live events and cold audiences.

### Closest existing workshop to "build an AI-powered APEX app in 90 minutes"

**`event-mangement` — "Build an AI-Powered Event Management App in 60 Minutes with Oracle APEX"** (updated May 2026). It covers the full modern arc: configure a Generative AI service in APEX → create data model with AI → generate the app with AI → enhance UI with AI → build an AI chat assistant → AI text generation → optional AI-generated charts. **But it has no sandbox variant** — tenancy and tenancy-special (bootcamp) only. `nyc-genai-lab` (updated July 6, 2026) is the closest *sandbox* workshop (~60 min core) but is a GenAI *feature* lab (chat widget + email generation on a schools app), not an AI-assisted app build, and doesn't touch the APEX AI Assistant, agents, or Select AI.

### The gap our workshop fills

A **90-minute, green-button, zero-prerequisite** workshop that delivers the full "APEX + AI" story end-to-end: AI-assisted app creation (AI Assistant / Create App with AI) **plus** runtime AI features (chat assistant / RAG / vector search / AI agent) in one sitting — the pitch none of the 15 existing AI workshops delivers on the sandbox. Newest differentiators unclaimed on the green button: APEX AI Agents with tools (scm-ai-agent is tenancy-only) and 26ai-native vector search. Avoid duplicating: OCI Vision (ai-vision-lab), ONNX semantic search (image-semantic-search), Q&A chat widget on a prebuilt app (nyc-genai-lab), OCI GenAI Agents service (oci-rag-agent), Document Understanding.

## 3. Structural Exemplars

### Primary: `nyc-genai-lab` (sandbox + tenancy, AI, updated 2026-07-06)

```
nyc-genai-lab/
├── 0-intro/            0-intro.md, files/, images/
├── 1-create-app/       1-create-app.md, files/, images/
├── 2-schools-on-map/   ...
├── 4-using-genai/      ...
├── 5-apply-to-school/  ...
├── 6-run-app/          ...
├── 7-vector-search/    ...
├── 8-appendix/  8-quiz/
├── nyc-genai-lab.zip           ← downloadable finished app
└── workshops/
    ├── sandbox/   index.html + manifest.json   ← green button
    └── tenancy/   index.html + manifest.json   ← brown button
```

Pattern: one folder per lab (`n-name/n-name.md` + `images/` + optional `files/`), lab content shared across variants, and **one manifest per variant** re-sequencing the same labs with variant-specific setup labs. `index.html` is a stub that renders the manifest via the LiveLabs JS framework.

`workshops/sandbox/manifest.json` (verbatim, at `nyc-genai-lab/workshops/sandbox/manifest.json`):

```json
{
  "workshoptitle": "Build an Innovative Q&A Interface Powered by Generative AI with Oracle APEX",
  "help": "livelabs-help-apex_us@oracle.com",
	"tutorials": [
    {
      "title": "Introduction",
      "filename": "../../0-intro/0-intro.md"
    },
    {
      "title": "Get Started",
      "description": "Prerequisites for LiveLabs (Oracle-owned tenancies). The title of the lab and the Contents Menu title (the title above) match for Prerequisite lab. This lab is always first.",
      "filename": "https://livelabs.oracle.com/cdn/common/labs/cloud-login/cloud-login-livelabs2.md"
   },
   {
    "title": "Sign up for an APEX Workspace",
    "filename": "../../../common-242/1-sign-up-apex/sign-up-apex-sandbox.md"
  },
  {
    "title": "Lab 1: Create an APEX App",
    "filename": "../../1-create-app/1-create-app.md"
  },
  {
    "title": "Lab 2: Visualize Schools on a Map",
    "filename": "../../2-schools-on-map/2-schools-on-map.md"
  },
  {
    "title": "Lab 3: Configure a Generative AI Service in APEX",
    "filename": "../../3-configure-oci/3-configure-oci.md",
    "type": {
      "OCIGenAI" : "OCIGenAI",
      "OpenAI" : "OpenAI"
      }
  },
  {
    "title": "Lab 4: Build a Conversational Inquiry using Generative AI",
    "filename": "../../4-using-genai/4-using-genai.md"
  },
  {
    "title": "Lab 5: Generate Email to Apply to a School using Gen AI",
    "filename": "../../5-apply-to-school/5-apply-to-school.md"
  },
  {
    "title": "Lab 6: Run the Application",
    "filename": "../../6-run-app/6-run-app.md"
  },
  {
    "title": "Lab 7 [OPTIONAL]: Implement RAG using AI Vector Search",
    "filename": "../../7-vector-search/7-vector-search.md"
  },
  {
    "title": "Lab Appendix: Download Instructions",
    "filename": "../../8-appendix/8-appendix.md"
  },
    {
      "title": "Need Help?",
      "description": "Solutions to Common Problems and Directions for Receiving Live Help",
      "filename":"https://livelabs.oracle.com/cdn/common/labs/need-help/need-help-livelabs.md"
    }
  ]
}
```

Key mechanics:
- **Common includes, three tiers**: (1) CDN-hosted platform labs by absolute URL — `cloud-login-livelabs2.md` (sandbox login lab, always first in sandbox variants) and `need-help-livelabs.md`; (2) repo-shared, version-pinned lab folders — `common-242/`, `common-261/`, `common-latest/` (e.g. sandbox variant uses `common-242/1-sign-up-apex/sign-up-apex-sandbox.md`, tenancy variant uses `common-261/1-sign-up-apex/1-sign-up-apex.md` + `common-261/4-apex-basics/`); (3) local labs by relative path.
- **Conditional content via `type`**: Lab 3 declares `"type": {"OCIGenAI": ..., "OpenAI": ...}` — the markdown uses `if type="OCIGenAI"` blocks so one lab serves both AI providers. Same mechanism distinguishes freetier vs livelabs content in single-source workshops.
- **Estimated times**: intro declares 60 min total; per-lab: create-app 5, map 10, GenAI inquiry 20, email 15, run 5, optional RAG +15.
- Bug worth avoiding: the sandbox manifest references `../../3-configure-oci/3-configure-oci.md`, which doesn't exist in the repo (the tenancy variant correctly points at `common-261/2-configure-ai-keys/`); stale include paths across variants are a real hazard.
- **`variables.json`** is *not* used by nyc-genai-lab; in this repo only `sample-workshop`, `employee-onboarding`, and `manage-offensive-behavior` use it (`"variables": ["../../variables/variables.json"]` at manifest top, referenced in markdown as `[](var:name)`). Useful for version strings (e.g. "26ai") you'll bump repo-wide.

### Secondary: `event-mangement` (content model) and `sample-workshop` (canonical skeleton)

`event-mangement` is the 60-minute AI-Assistant app build: 7 labs of ~5–10 min each (total declared 60 min), `tenancy-special` variant showing how a bootcamp/event re-cut of the same labs is just another manifest. `sample-workshop` is the LiveLabs-maintained template with all three variants (sandbox/tenancy/desktop) plus the variables and tables demo labs — start any new workshop by copying it, per the [author guide](https://oracle-livelabs.github.io/common/sample-livelabs-templates/create-labs/labs/workshops/livelabs/index.html).

## 4. LiveLabs Sandbox (Green Button) Mechanics

**Reservation flow** ([request-reservation sprint](https://livelabs.oracle.com/cdn/sprints/livelabs/request-reservation/index.html); source in [oracle-livelabs/sprints](https://github.com/oracle-livelabs/sprints)):
- Requires only a free Oracle.com account (SSO) — no OCI tenancy. User picks timezone, "Start Workshop Now" or a scheduled date/time, consents to emails, submits. Status: Pending → Provisioning → Active → "Launch Workshop".
- In most sandbox workshops **setup is automated and resources are pre-provisioned** (e.g., an Autonomous Database instance) so users start at the product task.
- User receives: tenancy name, username, one-time password (forced reset on first login), and an **assigned compartment** inside a LiveLabs-owned tenancy ([cloud-login common lab](https://livelabs.oracle.com/cdn/common/labs/cloud-login/cloud-login-livelabs2.md)).
- **At reservation end the environment and everything in it is deleted.** Duration is set per-workshop (the "Workshop Time" the author supplies at publishing); users can extend an active reservation **up to 2× the original allotted time** ([extend-reservation sprint](https://livelabs.oracle.com/cdn/sprints/livelabs/extend-reservation/index.html)), in ~1-hour increments ([Oracle Japan tutorial](https://oracle-japan.github.io/ocitutorials/adb/adb103-livelabs/)).

**Two sandbox types an author can request** (from `create-labs` Lab 6, Task 3 — [publish lab](https://oracle-livelabs.github.io/common/sample-livelabs-templates/create-labs/labs/workshops/livelabs/index.html?lab=6-labs-publish)):
1. **Sandbox Lite** — auto-created within **1 business day**, checkbox in WMS. Creates **no resources**; gives each user an isolated compartment in a LiveLabs tenancy where they create everything themselves. This is what current APEX sandbox workshops effectively use: the shared `sign-up-apex-sandbox.md` lab has the attendee create an ADB (APEX pre-integrated) in the assigned compartment and then create workspace/users themselves.
2. **Full LiveLabs Sandbox** — pre-provisioned stack. Requested via a **Jira ticket** opened from the WMS Sandbox Environment tab (summary format `[Sandbox] WMS ID: … LL ID: … Title`), questionnaire describing the resources; the LiveLabs team builds the demo environment, the author tests it, then the team moves it to production and enables the green button. This is how you'd get "ADB already running + APEX workspace pre-created" at launch.

**What the author supplies in WMS**: mandatory **Run on LiveLabs Sandbox URL** = `https://oracle-livelabs.github.io/[repo]/[workshop-folder]/workshops/sandbox/`, a sandbox-specific `manifest.json`/`index.html`, and sandbox-conditional lab content where instructions differ (or `type`-conditional blocks in shared markdown).

**APEX-specific reality check**: none of the APEX sandbox workshops assume a pre-created APEX workspace; they all budget ~10 min for "log into sandbox tenancy → create Always Free ADB in your compartment → create workspace DEMO/DEMO". A full-sandbox Jira request could eliminate that, but adds a dependency on the LiveLabs infra team and OCI GenAI availability inside LiveLabs tenancies (each request is reviewed; "not all OCI services are available in a sandbox environment").

## 5. Publishing Process (WMS + GitHub)

From the LiveLabs authoring workshop (`oracle-livelabs/common/sample-livelabs-templates/create-labs`, updated Jan 2026; rendered at [oracle-livelabs.github.io](https://oracle-livelabs.github.io/common/sample-livelabs-templates/create-labs/labs/workshops/livelabs/index.html)):

1. **Submit in WMS first** (Oracle-internal, VPN: livelabs.oracle.com/wms). Abstract, outline, prerequisites, tags (Level, Role, Focus Area, Product required). The **Workshop Council reviews within 2–3 business days**. Don't start building until Approved.
2. **Statuses**: Submitted → Approved → In Development → Self QA → Self QA Complete (stakeholders verify within 2 business days) → Completed → Published. Published workshops require **Quarterly QA every 90 days** (auto-flagged at day 60; not completed by day 90 → pulled from production, purged from catalog after 30 more days).
3. **Development**: fork the `oracle-livelabs/apex` repo, copy `sample-workshop`, lowercase filenames, imperative lab titles, images in `images/` with alt text, `<copy>` tags on code blocks, Acknowledgements section per lab (lint-enforced — repo has `lintchecker`/`md-validator`; PRs get automated checks).
4. **Publish**: PR to `oracle-livelabs/apex:main` with **WMS ID in the PR title** (PRs without it are not approved; reviewed within 1 business day; OCA sign-off per [CONTRIBUTING.md](https://github.com/oracle-livelabs/apex/blob/main/CONTRIBUTING.md)) **plus** a WMS Publishing entry: Publish Type (**Public / Event / Private / Disabled**), Workshop Time (drives reservation length), brown-button URL, optional video embed. Live within ~1 business day of approval.
5. **Green button**: request via the Sandbox Environment tab (Sandbox Lite checkbox, or Jira for full sandbox) — can be added after the workshop is already in production.

## 6. Live Events & Concurrency

From the LiveLabs FAQ (`create-labs/labs/livelabs-faq/livelabs-faq.md`):

- **Event Codes**: fully customizable, hidden-from-catalog workshop bundles for a target audience; requested in WMS ("Request an Event Code"), reviewed within 2 business days, created within 1 business day. Set start date 1 day before and end date 1 day after the event for timezone slack. Attendees need an oracle.com account (SSO) to redeem. You can build an event-specific manifest (custom lab subset, event name) and point the event code at it — exactly the `ocw23-*`/`aiw25`/`tenancy-special` variant pattern in the apex repo.
- **Capacity — the critical number**: for green-button/sandbox delivery, **~30 concurrent users** is the stated quota ("limited by our collection of tenancies and what else is running"). If the event organizer provides their own tenancy (brown button/event tenancy), capacity is limited only by that tenancy's resources. Plan a >30-seat event either as brown-button-on-event-tenancy, or coordinate capacity with the LiveLabs team in advance.
- Green-button usage is individually tracked (workshop id + email); brown-button only counts page views.

## 7. Recommendations for Our Workshop

1. **Positioning**: "Build an AI-powered APEX app in 90 minutes, nothing but a browser and a free Oracle account." Own the intersection nobody holds: AI-assisted *app building* (AI Assistant / Create App with AI) + runtime AI (chat assistant or AI agent + 26ai vector search) **on the green button**. Explicitly differentiate from wid 633 (Smart PM app — tenancy only), event-mangement (60-min, tenancy only), and nyc-genai-lab (sandbox, but feature-integration only).
2. **Structure**: clone `sample-workshop`, model content on `event-mangement`/`nyc-genai-lab`. Ship `workshops/sandbox/` first, `workshops/tenancy/` as the brown-button twin (needed anyway for the WMS publishing entry), and plan an `event/`-style manifest variant for conferences. One folder per lab, 6–7 core labs of 10–15 min (90 total), one clearly-marked OPTIONAL stretch lab, downloadable finished app zip in the Appendix, quiz lab optional.
3. **Reuse the commons**: first two manifest entries = CDN `cloud-login-livelabs2.md` + the sign-up sandbox lab (or a Jira-provisioned pre-built ADB to claw back 10 minutes); last entry = CDN `need-help-livelabs.md`. **[ERRATUM 2026-07-07: this report originally named `common-latest/1-sign-up-apex/sign-up-apex-sandbox.md`, which does not exist — `common-latest` has no sandbox flavor. The file exists only in `common-242/` (per §on common includes above) and `common-261/`. Use `common-261/1-sign-up-apex/sign-up-apex-sandbox.md`.]** Use `type` conditionals for OCI GenAI vs OpenAI provider choice (nyc-genai-lab Lab 3 pattern) rather than duplicate labs; verify every cross-variant include path resolves (nyc-genai-lab's sandbox manifest has a stale one).
4. **Sandbox strategy**: start with **Sandbox Lite** (1-day turnaround, no infra dependency) and budget Lab 0 at ≤10 min for ADB + workspace creation; in parallel, open the Jira for a full sandbox with pre-provisioned ADB/APEX workspace and confirm **OCI GenAI availability in the LiveLabs tenancies** — that's the single biggest technical risk; nyc-genai-lab hedges with an OpenAI path (bring-your-own key), which we should keep as fallback.
5. **Timing discipline**: set WMS Workshop Time to 90 min knowing users can self-extend to 2× (180 min) — comfortable for slow attendees; everything is wiped at reservation end, so the Appendix must include export/download-your-app instructions (standard pattern in the AI workshops).
6. **Process runway**: submit to WMS before writing content (council 2–3 days), and expect end-to-end ~2–4 weeks: development → Self QA → stakeholder QA (2 days) → PR with WMS ID (1 day) → publish (1 day) → green button enablement. Commit to Quarterly QA every 90 days or the workshop gets pulled.
7. **Events >30 people**: green button caps at ~30 concurrent reservations — for larger live events, request an Event Code with a brown-button path on an event-provided tenancy, or pre-negotiate sandbox capacity with livelabs-help-db_us@oracle.com.

**Sources**: [LiveLabs authoring workshop (create-labs)](https://oracle-livelabs.github.io/common/sample-livelabs-templates/create-labs/labs/workshops/livelabs/index.html) · [oracle-livelabs/common](https://github.com/oracle-livelabs/common) · [oracle-livelabs/apex](https://github.com/oracle-livelabs/apex) · [request-reservation sprint](https://livelabs.oracle.com/cdn/sprints/livelabs/request-reservation/index.html) · [extend-reservation sprint](https://livelabs.oracle.com/cdn/sprints/livelabs/extend-reservation/index.html) · [cloud-login common lab](https://livelabs.oracle.com/cdn/common/labs/cloud-login/cloud-login-livelabs2.md) · [Oracle Japan LiveLabs tutorial](https://oracle-japan.github.io/ocitutorials/adb/adb103-livelabs/) · [wid 4190](https://livelabs.oracle.com/ords/r/dbpm/livelabs/view-workshop?wid=4190) · [wid 633](https://livelabs.oracle.com/ords/r/dbpm/livelabs/view-workshop?wid=633) · [Event Management app blog](https://blogs.oracle.com/apex/build-an-ai-powered-event-management-app-in-60-minutes-with-oracle-apex) · [nyc-genai-lab live](https://oracle-livelabs.github.io/apex/nyc-genai-lab/workshops/tenancy/index.html) · [Oracle APEX AI page](https://www.oracle.com/apex/ai/)
