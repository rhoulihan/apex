# Take It Home

## Introduction

Ninety minutes ago this was an empty workspace. Now it's a running help desk with an AI-designed schema, an app generated from a prompt, natural-language analytics, and a governed AI agent. This last stop makes sure you leave with all of it.

> **Your sandbox is deleted when the reservation ends — export now, not later.** Everything below takes five minutes.

Estimated Time: 5 minutes

### Objectives

In this lab, you will:

* Export your application and keep the workshop scripts
* Recap the five governance mechanisms you used
* Pick up the trail: where APEX developers actually keep learning

## Task 1: Export Your Application

1. In the builder, open **Horizon Help Desk**, then **Export/Import > Export**, and download the export file. It imports into any APEX 26.1 workspace — including a free one at apex.oracle.com.

    ![Application export page](images/app-export.png " ")

    > Exports are also how you version-control APEX today — and APEX 26.1's **APEXlang** (`.apx` application spec, readable by humans, diff tools, and LLMs alike) plus **SQLcl Projects** are the modern, source-control-native path. One search for "APEXlang" gets you started.

2. Keep the scripts — they rebuild the schema anywhere:

    * [helpdesk-schema.sql](../2-data-model-ai/files/helpdesk-schema.sql) — schema + seed (state-reset checkpoint)
    * [resolve-ticket.sql](../5-ai-agent/files/resolve-ticket.sql) — the agent's write tool
    * [embed-kb.sql](../7-vector-search/files/embed-kb.sql) — the one-statement embedding pipeline

3. Want to keep building for free? [apex.oracle.com](https://apex.oracle.com) gives you a permanent free workspace; [Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/) gives you two Always Free Autonomous Databases with APEX included.

## Task 2: What Made It Trustworthy — the Recap

You met five governance mechanisms today, one per AI feature:

1. **Token quotas** you set on the service yourself (Lab 1)
2. **Human review of AI-generated SQL** before anything runs (Lab 2)
3. **No AI-executed SQL** — natural language maps to declarative, inspectable settings (Lab 4)
4. **Tool allow-lists** — the agent can only call what you attached (Lab 5)
5. **User-approval confirmations on write tools** — the human clicks Resolve (Lab 5)

And in every lab, you knew **exactly what data was sent to the model** — from metadata-only (Lab 4) to scoped query results (Lab 5) to nothing at all (Lab 7, in-database). That's the difference between an AI demo and an AI feature you'd ship: *AI as amplifier, with you as the reviewer.*

## Task 3: Where APEX Developers Actually Keep Learning

* **[Oracle LiveLabs](https://livelabs.oracle.com)** — your next workshops, hands-on and free. Natural sequels to today: *Build an AI Procurement Agent in Oracle APEX* (deeper agent tooling) and *Spec-Driven Development with AI and APEXlang*.
* **[APEX Office Hours](https://apex.oracle.com/officehours)** — live sessions with the APEX product managers.
* **[Insum APEX Instant Tips](https://www.youtube.com/playlist?list=PLCAYBJ7ynpQQQrdwKFBZu8Kx9VTFt-pRP)** — weekly, short, practical.
* **[Cloud Nueva blog](https://blog.cloudnueva.com)** — hands-on APEX + AI engineering write-ups.
* **[apex.world](https://apex.world)** — community news, jobs, Slack.

Thanks for building with us — see you at the next developer day.

## Learn More

* [Oracle APEX and AI](https://www.oracle.com/apex/ai/)

## Acknowledgements

* **Author** - Rick Houlihan
* **Last Updated By/Date** - Rick Houlihan, July 2026
