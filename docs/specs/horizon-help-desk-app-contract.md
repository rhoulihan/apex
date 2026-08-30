# Horizon Help Desk — generated app contract

**Purpose.** Lab 3 generates the application with AI, which means its output *varies between runs*.
Labs 4, 5 and 6 then build on that output. This document is the **contract**: the minimum the generated
app must satisfy for the rest of the workshop to work as written. Lab 3's prompt is written to produce it,
and Lab 3 Task 2 verifies it before anything is created.

If a change is made to Lab 3's prompt, or to any of Labs 4–6's page references, **update this file too**.

---

## Required by downstream labs

| # | Requirement | Required by | Why it breaks without it |
|---|---|---|---|
| C1 | **Page 1 is the Dashboard** | Lab 5 Task 5 | Lab 5 says "Open **Page 1** (the Dashboard)" and adds the `ASK_THE_ANALYST` button to its Breadcrumb Bar. If page 1 is something else, the instruction points at the wrong page. |
| C2 | Page 1 has a **Breadcrumb Bar** region containing a **Breadcrumb** | Lab 5 Task 5 | The button is created via right-click **Breadcrumb > Create Button Below**, Region **Breadcrumb**, Slot **Next**. |
| C3 | A page named **Tickets** containing an **Interactive Report** region on `TICKETS` | Lab 4 Tasks 2–3 | Natural Language Support / "Search with AI" exists **only** on Interactive Report regions. Faceted Search or Cards will not do. |
| C4 | An **editable form page on `TICKETS`**, reachable from the Tickets report | Lab 6 Tasks 1–2 | Lab 6 adds the Reply textarea and the `DRAFT_REPLY` button to this page. |
| C5 | A page named **Knowledge Base** with a report on `KB_ARTICLES` | Lab 3 Task 4 tour; referenced as context in Lab 5 | Keeps the tour and the agent's RAG story coherent. |
| C6 | Dashboard has a **tickets-by-status** chart and a **tickets-by-category** chart | Lab 3 Task 4 tour | These are what the tour points at, and what makes the dashboard worth showing. |
| C7 | App name is **Horizon Help Desk** | Throughout | Screenshots, prose and the Take It Home export all use this name. |

## Not required (deliberately unconstrained)

- Exact page numbers other than page 1 — Lab 6 references items like `&P6_DESCRIPTION.` **as examples only**
  and explicitly tells the reader their item names may differ.
- Theme, colours, navigation style, icons.
- Whether a `TEAM_MEMBERS` maintenance page exists. Harmless if generated; nothing depends on it.
- Any extra pages the blueprint adds.

## Data contract (established in Lab 2, verified 2026-08-30)

| Item | Value |
|---|---|
| `TICKETS` rows | 50 |
| `KB_ARTICLES` rows | 20 |
| `TEAM_MEMBERS` rows | 8 |
| Ticket **42** | `Open` / `Network` — used by Lab 5's agent demo |
| Ticket **27** | the new-laptop VPN ticket — used by Lab 6's Draft Reply demo |
| `KB_ARTICLES.EMBEDDING` | `VECTOR` column present, populated in Lab 7 |
| `TICKETS.REPLY` | present but empty — surfaced in Lab 6 |

## Recovery if the blueprint misses something

Every requirement above is recoverable in about a minute, and the labs say so:
- **Missing Tickets Interactive Report** → Lab 4 Task 2 has the 60-second **Create Page** recovery.
- **Wrong page type** → change it in the blueprint editor before clicking Create Application.
- **Page 1 is not the Dashboard** → regenerate, or adapt Lab 5 Task 5 to whichever page holds the Breadcrumb Bar.

This is why Lab 3 Task 2 exists: **verify the blueprint against C1–C7 before creating the app**, when
changing it is still free.
