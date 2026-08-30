# Oracle APEX + AI — Platform Research Report (July 2026)

> Research agent report commissioned for the APEX + AI LiveLabs workshop spec.
> Method: web research against oracle.com, docs.oracle.com, Oracle blogs, community blogs. URLs cited per claim.

## 1. Release timeline and AI features

**Current release: APEX 26.1** (GA May 14, 2026). There was **no 25.1/25.2** — Oracle skipped the 25.x line entirely and jumped from 24.2 to 26.1 to align with the "Oracle AI Database 26ai" branding ([dgielis.com](https://dgielis.com/oracle-apex-251-and-beyond), [blogs.oracle.com/apex/announcing-oracle-apex-261](https://blogs.oracle.com/apex/announcing-oracle-apex-261), [26.1 release notes](https://docs.oracle.com/en/database/oracle/apex/26.1/htmrn/new-features.html)). Support covers current + two prior releases, so 24.1/24.2/26.1 are all supported ([release notes index](https://apex.oracle.com/en/learn/documentation/release-notes/)).

### APEX 24.1 (June 2024) — foundation layer
- **APEX Assistant** in the builder: NL→SQL generation, code suggestions, "explain code," one-click debug correction ([Oracle press release](https://www.prnewswire.com/news-releases/oracle-apex-ai-assistant-enables-natural-language-based-development-of-enterprise-applications-302173588.html), [blog](https://blogs.oracle.com/apex/coding-with-the-ai-powered-apex-assistant-on-oracle-apex)).
- **Create Application from natural language**: prompt → AI-generated app blueprint; uses the APEX Dictionary Cache to pick relevant tables and propose pages ([whats-new-241](https://apex.oracle.com/en/platform/features/whats-new-241/)).
- **Generative AI Service configurations** (Workspace Utilities → Generative AI): native providers were **OCI Generative AI, OpenAI, Cohere**; credentials stored as Web Credentials; per-service "Used by App Builder" toggle and Static ID for API use ([docs 24.1](https://docs.oracle.com/en/database/oracle/apex/24.1/htmdb/managing-generative-ai-services.html)).
- **AI Dynamic Actions**: "Show AI Assistant" chat widget in end-user apps.
- **APEX_AI PL/SQL API** (`APEX_AI.CHAT`, etc.) ([apex.oracle.com/en/platform/ai/](https://apex.oracle.com/en/platform/ai/)).

### APEX 24.2 (Dec 2024) — AI in the app + RAG
- **AI Configurations** shared component: system prompt, welcome message, and **RAG Sources** (SQL query / PL/SQL function / static text) that ground chat responses in your data — declarative RAG ([announcement](https://blogs.oracle.com/apex/announcing-oracle-apex-242), [MaxAPEX RAG guide](https://www.maxapex.com/blogs/rag-in-oracle-apex-24-2/)).
- **"Generate Text with AI" Dynamic Action** — AI text generation into form items ([blog](https://blogs.oracle.com/apex/whats-new-in-apex-242-dynamic-action-generate-text-with-ai)).
- **AI Vector Search in Search Configurations** — declarative semantic search component on 23ai vector columns ([blog](https://blogs.oracle.com/apex/nextgen-data-search-integrating-ai-vector-search-into-search-configurations), [oracle.com AI Vector Search in APEX](https://www.oracle.com/artificial-intelligence/ai-vector-search-in-apex/)).
- **AI-driven data modeling**: NL → SQL data model + sample data ([blog](https://blogs.oracle.com/apex/blog-create-data-model-using-ai)).

### APEX 26.1 (May 2026) — the agentic release
Per the [26.1 release notes](https://docs.oracle.com/en/database/oracle/apex/26.1/htmrn/new-features.html) and [26.1 announcement](https://blogs.oracle.com/apex/announcing-oracle-apex-261):
- **AI Agents + AI Tools**: AI Configurations renamed **AI Agents**; agents call declarative **AI Tools** (Retrieve Data, Execute Server-side Code, Execute Client-side Code, custom plug-ins), with **Guardrails** requiring user approval for sensitive tools. LLM can only call tools attached to the agent; execution stays inside the app's security boundary ([AI Agents blog](https://blogs.oracle.com/apex/ai-agents-in-oracle-apex), [CRM agent example](https://blogs.oracle.com/apex/build-a-crm-ai-agent-with-oracle-apex)).
- **AI Interactive Reports (NL2IR)**: natural-language filters/breaks/charts/pivots on IRs; AI never executes generated SQL — it maps intent to declarative IR settings shown as removable chips ([blog](https://blogs.oracle.com/apex/introducing-apex-ai-interactive-reports)).
- **New AI providers**: **Anthropic Claude, Google Gemini, Mistral AI, Ollama**, plus "Generic (OpenAI API-compatible)" — joining OCI GenAI, OpenAI, Cohere ([release notes](https://docs.oracle.com/en/database/oracle/apex/26.1/htmrn/new-features.html); provider list confirmed in the [current LiveLabs config lab](https://raw.githubusercontent.com/oracle-livelabs/apex/main/common-261/2-configure-ai-keys/2-configure-ai-keys.md)).
- **APEX_AI upgrades**: `APEX_AI.GENERATE` with file/image attachments, structured JSON output with JSON Schema, `SET_TOOL_RESULT` for tool callbacks; **Generate Text with AI page process**; Max AI Tokens quotas at instance/workspace/service level.
- **APEXlang**: open, human-readable `.apx` application spec — source-control-, diff-, and LLM-friendly; supported in SQL Developer for VS Code and SQLcl, positioned for AI-agent-driven app authoring (Claude/Codex plugins) ([JMJ Cloud first impressions](https://jmjcloud.com/blog/apex-26-1-apexlang-claude-code/)); **Blueprints for spec-driven development** (markdown blueprint → app); **Create Page using natural language**.
- Also: workflow **Generate Text with AI activity**, parallel workflow branches, Data Reporter, "Describe Tables" (LLM-friendly schema descriptions via `APEX_DB_DICTIONARY`).

### RAG / database-side AI
- **Select AI** (`DBMS_CLOUD_AI`) on Autonomous AI Database: NL2SQL, chat, RAG, and **Select AI Agents**; APEX is the canonical front end ([reference architecture](https://docs.oracle.com/en/solutions/select-ai-apex-framework/index.html), [Select AI page](https://www.oracle.com/autonomous-database/select-ai/)). 26ai adds RAG + vector-search-dependent features not in 19c ([Select AI by release](https://blogs.oracle.com/machinelearning/select-ai-by-release-a-quick-guide-to-26ai-and-19c-capabilities)).
- **Autonomous AI Database MCP Server** (announced ~Oracle AI World, Oct 2025): lets Claude Desktop / OCI agents invoke Select AI Agent tools ([blog](https://blogs.oracle.com/machinelearning/announcing-the-oracle-autonomous-ai-database-mcp-server)).
- **OCI Generative AI Agents service** integration with APEX for hosted RAG ([blog](https://blogs.oracle.com/apex/integrating-oci-generative-ai-agents-with-oracle-apex-apps-for-ragpowered-conversational-experience)).

## 2. What each feature needs in a lab

**Everything AI in APEX needs a configured Generative AI Service + credential.** For OCI GenAI: attendee generates an **OCI API key pair** in the console, then supplies user OCID / tenancy OCID / private key / **compartment OCID** / region / model ID in the APEX config ([current LiveLabs lab](https://raw.githubusercontent.com/oracle-livelabs/apex/main/common-261/2-configure-ai-keys/2-configure-ai-keys.md)). OpenAI/Cohere/Claude need only an API key in a Web Credential ([docs 24.2](https://docs.oracle.com/en/database/oracle/apex/24.2/htmdb/managing-generative-ai-services.html)).

- **OCI GenAI regions** (on-demand): Chicago, Ashburn, Phoenix, Frankfurt, London, Osaka, Hyderabad, São Paulo, Riyadh, Dubai, Abu Dhabi — **not all models in all regions**; Chicago has the fullest catalog. APEX calls it via REST, so the ADB can live in any region and target `us-chicago-1` ([regions doc](https://docs.oracle.com/en-us/iaas/Content/generative-ai/regions.htm), [models by region](https://docs.oracle.com/en-us/iaas/Content/generative-ai/model-endpoint-regions.htm)).
- **LiveLabs Sandbox works**: Oracle's own "Build an Innovative Q&A Interface Powered by Generative AI with Oracle APEX" ships a **green-button sandbox variant** whose flow is exactly: create app → configure OCI GenAI (Chicago) or OpenAI → Show AI Assistant chatbot with AI Agent/RAG tools → Generate Text DA → optional Vector Search RAG lab ([sandbox manifest](https://github.com/oracle-livelabs/apex/tree/main/nyc-genai-lab/workshops), [workshop](https://oracle-livelabs.github.io/apex/nyc-genai-lab/workshops/tenancy/index.html)). So the Oracle-owned sandbox tenancy already carries the IAM policy allowing GenAI inference. There is also an **"ai-world-hol-apex"** and an **"ai-interactive-report-lab"** (26.1-based) in the repo to crib from.
- **Select AI / resource principal**: needs `DBMS_CLOUD_ADMIN.ENABLE_PRINCIPAL_AUTH` + a tenancy dynamic-group/policy for GenAI — fine on the sandbox if pre-provisioned, awkward for attendees to set up themselves ([Select AI profile docs](https://docs.oracle.com/en-us/iaas/autonomous-database-serverless/doc/select-ai-manage-profiles.html)).
- **Vector search**: needs 23ai/26ai ADB + an embedding model (OCI GenAI Cohere embed via credential, or an in-database ONNX model — ONNX avoids any external call).

## 3. What Autonomous Database ships with

APEX is **preinstalled on every Autonomous AI Database Serverless** instance (and APEX Service). New APEX releases roll out to all 50+ regions starting at GA, completing in 2–5 weeks, with a 45-day (extendable to 90) customer-controlled upgrade window — so by July 2026 sandbox ADBs are on **26.1** ([cloud updates](https://apex.oracle.com/en/platform/apex-oracle-cloud/cloud-updates/), [ADB docs](https://docs.oracle.com/en/cloud/paas/autonomous-database/serverless/adbsb/apex-apply-defer-updates.html)). ADB Serverless is now "Autonomous AI Database" on **26ai** (rebranded from 23ai at AI World, Oct 2025), with AI Vector Search and Select AI included at no extra charge ([26ai announcement](https://blogs.oracle.com/database/oracle-announces-oracle-ai-database-26ai), [oracle.com news](https://www.oracle.com/news/announcement/ai-world-database-26ai-powers-the-ai-for-data-revolution-2025-10-14/)). Always Free ADB includes two instances and supports Select AI/vector search (LLM credential still required).

## 4. Current Oracle messaging

- Tagline: **"APEX + AI = Awesome"** ([oracle.com/apex/ai/](https://www.oracle.com/apex/ai/)); 26.1 framed as "enterprise low-code built for the AI era."
- Pillars: AI-assisted development (Assistant, NL create app/page), AI inside apps (agents, tools, NL2IR, chat), and **governed/trusted AI** — "APEX does not execute AI-generated SQL," guardrails, tool allow-lists ([AI IR blog](https://blogs.oracle.com/apex/introducing-apex-ai-interactive-reports), [AI Agents blog](https://blogs.oracle.com/apex/ai-agents-in-oracle-apex)).
- Flagship demos: CRM AI Agent, AI Interactive Reports, APEXlang + Claude Code/Codex spec-driven development, "AI-powered event app in 60 minutes" ([CRM agent](https://blogs.oracle.com/apex/build-a-crm-ai-agent-with-oracle-apex), [event app](https://blogs.oracle.com/apex/build-an-ai-powered-event-management-app-in-60-minutes-with-oracle-apex)).

## 5. Gotchas for a 50-person live run

1. **Model deprecation churn**: APEX's historical default `cohere.command-r-16k` is deprecated/retired; hardcoded model IDs 404. Oracle's own lab now says "pre-trained models are frequently deprecated — check the docs" ([Cohere R+ retired](https://docs.oracle.com/en-us/iaas/Content/generative-ai/cohere-command-r-plus.htm), [LiveLabs lab text](https://raw.githubusercontent.com/oracle-livelabs/apex/main/common-261/2-configure-ai-keys/2-configure-ai-keys.md)). Verify the model ID the week of the event.
2. **Dynamic throttling on on-demand inference**: OCI GenAI adjusts tenancy-level rate limits by demand — 50 people hammering one shared tenancy compartment can hit 429s ([limits](https://docs.oracle.com/en-us/iaas/Content/generative-ai/limits.htm), [modes](https://docs.oracle.com/en-us/iaas/Content/generative-ai/modes.htm)). Mitigate with 26.1 Max AI Tokens caps and staggered exercises.
3. **Region mismatch**: sandbox ADB region ≠ GenAI region is fine (REST), but attendees must type `us-chicago-1` exactly; wrong region → cryptic 404s.
4. **API-key friction**: the OCI key-pair + 3 OCIDs dance is the single most error-prone 10 minutes; budget for it or pre-stage.
5. **APEX Assistant needs "Used by App Builder" ON** at the workspace service — a frequently missed toggle ([docs](https://docs.oracle.com/en/database/oracle/apex/24.2/htmdb/managing-generative-ai-services.html)).

## Implications for a 90-min sandbox workshop

**Safe bets** (proven in Oracle's own green-button labs, all in-sandbox):
- Configure OCI GenAI service (Chicago) with attendee-generated API key — mirror `common-261/2-configure-ai-keys`.
- APEX Assistant SQL generation + NL "Create Application/Page" (needs only the service config).
- **Show AI Assistant** chat + **AI Agent with a Retrieve Data tool** (declarative RAG over lab schema) — the 26.1 marquee moment.
- **Generate Text with AI** dynamic action/page process in a form.
- **AI Interactive Reports (NL2IR)** — new, demo-friendly, zero extra setup once the service exists.

**Risky** (avoid or make optional):
- Select AI / resource principal setup (tenancy IAM work; policy may not exist in sandbox) — show as instructor demo or pre-provision.
- Vector search RAG with OCI embedding models (extra credential + embedding pipeline; fine as an optional lab like Oracle's, or use a pre-loaded ONNX model/pre-computed vectors).
- MCP server / APEXlang-with-Claude-Code (needs local tooling on attendee laptops).
- Anything pinned to a specific model ID without a "pick any current model" instruction.

**Fallbacks**: offer OpenAI-key path as alternate provider track (Oracle's lab does exactly this via a lab-type switch); pre-create the Gen AI service in a staged workspace export; keep one instructor tenancy with a dedicated compartment in case sandbox GenAI policy hiccups; pre-compute vector embeddings in the lab schema so the RAG lab needs no embedding calls.
