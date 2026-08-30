# Lab 3: Generate the App from a Prompt

## Introduction

Your data is in place. Now describe the application you want — and review the blueprint AI proposes before a single page is created. Ten minutes from now you'll be logged into a real web app with authentication and a URL.

Estimated Time: 10 minutes

### Objectives

In this lab, you will:

* Generate an application blueprint from a natural-language prompt
* Verify the blueprint has the pages later labs depend on
* Create, run, and tour the Horizon Help Desk

### Prerequisites

This lab assumes you have:

* Completed Lab 2 (the three tables exist with seed data)

## Task 1: Describe the App

1. Navigate to **App Builder > Create**, then choose **Create App Using Generative AI**.

    ![App Builder Create App with AI option](images/create-app-with-ai.png " ")

2. Paste this prompt and send it:

    ```
    <copy>Create an application named Horizon Help Desk using my existing TICKETS, KB_ARTICLES
    and TEAM_MEMBERS tables. Build exactly these three pages, in this order:
    1. Dashboard - make this the home page. Include a chart of ticket counts by STATUS and a
    chart of ticket counts by CATEGORY.
    2. Tickets - an Interactive Report on the TICKETS table, with an editable form to edit a
    single ticket.
    3. Knowledge Base - a report on the KB_ARTICLES table.
    Use TEAM_MEMBERS only as a lookup for a ticket's assigned team member. Do not create any
    additional pages.</copy>
    ```

    > **Why this prompt is so specific.** Generated apps vary between runs, but Labs 4, 5 and 6 build on
    this one. Naming the pages, pinning the Dashboard as the home page, and asking for an **Interactive
    Report** by name are what make the rest of the workshop work first time. The full contract is in
    *Task 2*.

    > **Note the wording of item 2.** The report and its edit form are asked for as **one page entry**, not
    two. Listing them separately makes the wizard build *two* report-and-form pairs, leaving you with two
    pages both named Tickets — and Lab 4 then can't tell you which one to open.

3. AI responds with an application **blueprint** — a proposed set of pages. Read it, then click **Create Application** *in the chat*.

    > **That button does not create anything yet.** It hands off to the Create Application wizard, which is where the blueprint becomes editable — page names, page types, charts, features and authentication. The chat summary lists pages only; the wizard is where you can actually inspect and change them. Task 2 happens there.

    ![AI-proposed application blueprint](images/app-blueprint.png " ")

## Task 2: Review the Blueprint — Pin the Pages Later Labs Need

This is the highest-leverage review in the workshop. Everything below is **free to change now** in the
blueprint editor, and fiddly to change after the app exists.

1. Check the blueprint against all five requirements:

    | # | Check | Needed by |
    |---|---|---|
    | 1 | **Dashboard** is listed **first** — it must become page 1 | Lab 5 |
    | 2 | Dashboard has a **tickets by status** chart and a **tickets by category** chart — click its **Edit** and step through the *Chart 1* / *Chart 2* tabs to confirm | the Lab 3 tour |
    | 3 | A page named **Tickets** whose type is **Interactive Report** | **Lab 4** |
    | 4 | The Tickets entry also produces an **editable form** on TICKETS | **Lab 6** |
    | 5 | A page named **Knowledge Base** reporting on KB_ARTICLES | the tour |
    | 6 | There is only **one** page named Tickets | Lab 4 tells you to open "the Tickets page" |

    > **Check 3 is the one that bites.** Lab 4's AI features exist **only** on Interactive Report regions. If the blueprint chose Faceted Search, Cards, or a plain Classic Report for Tickets, change the page type here — ten seconds, declarative. Left wrong, Lab 4 has no AI settings to turn on.

    > **Check 1 matters for a smaller reason.** Lab 5 puts the agent button on **Page 1**, described there as the Dashboard. If your Dashboard ends up as a different page number, Lab 5 still works — just apply its Task 5 steps to whichever page holds the Breadcrumb Bar.

2. Adjust anything else you like (this is the review habit from Lab 2, applied to app design), then click **Create Application**.

## Task 3: Run It

1. When the builder finishes, click **Run Application** and sign in with your workspace credentials.

    > **"Your session has ended" later on?** Expected, not a failure. APEX expires an idle session after
    > an hour, and this workshop runs about 90 minutes, so you will probably be asked to sign in again
    > once — most likely around Lab 5. Sign in again and carry on; nothing you built is lost.

    ![Horizon Help Desk running: dashboard with charts](images/app-running.png " ")

2. Take that in: **a real web application — authentication, a URL you could send to a colleague, responsive UI — from one reviewed prompt.** In most stacks that was your whole afternoon.

    > **Dashboard charts empty, with an `ORA-20987` error?** Known issue in APEX 26.1.4, not something you
    > did. Verbatim: `ORA-20987: APEX - Column "ID" specified for attribute "" has not been found in data
    > source!` The Create App wizard builds each chart series from the whole `TICKETS` table *and* applies a
    > `Count` aggregation, so after grouping, the `ID` column it still refers to no longer exists.
    >
    > **Sixty-second fix, per chart:** in **Page Designer** open page 1, select the chart region's
    > **Series 1**, and under **Source** set **Type** to **SQL Query**. Replace the query with:
    >
    > `select status as label, count(*) as value from tickets group by status order by 1`
    >
    > (use `category` in place of `status` for the second chart). Then set **Column Mapping** — **Label** to `LABEL` and
    > **Value** to `VALUE` — and click **Save**. Reload the app and both charts render.
    >
    > Worth doing even though nothing later depends on these charts: it is a tidy example of reading an
    > Oracle error, finding the real cause, and fixing it declaratively.

## Task 4: A Two-Minute Tour (Vocabulary for the Rest of the Day)

1. Back in the builder, open the app and note what was generated:

    * **Pages** — Dashboard, Tickets, Ticket form, Knowledge Base: each item in your prompt became one
    * **Regions** — the charts and reports inside each page; Lab 4 adds AI to the Tickets report region
    * **Navigation menu** — wired automatically

    ![App page list in the builder](images/app-pages.png " ")

> **Your app looks slightly different from the screenshots?** That's the point of generative AI — blueprints vary. You only need (a) a Tickets **Interactive Report** page and (b) a Knowledge Base report page to continue. Missing one? **Create Page**, describe it in natural language, done in 60 seconds — Lab 4 opens with exactly that recovery step.

## Go Further (optional)

Try **Create Page with natural language** — new in APEX 26.1, so even longtime APEX developers may not have seen it:

```
<copy>Create a bar chart page named Team Workload showing the number of open tickets per team member.</copy>
```

Then inspect the generated page in the builder: what region type did it pick, and what SQL is behind it?

You may now **proceed to the next lab**.

## Learn More

* [Create App with AI](https://apex.oracle.com/en/platform/features/)

## Acknowledgements

* **Author** - Rick Houlihan
* **Last Updated By/Date** - Rick Houlihan, August 2026
