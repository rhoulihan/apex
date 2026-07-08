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

1. Navigate to **App Builder** and choose **Create App with AI** (labelled *Generate with AI* on some screens).

    ![App Builder Create App with AI option](images/create-app-with-ai.png " ")

2. Paste this prompt and send it:

    ```
    <copy>Create an application named Horizon Help Desk over my existing TICKETS, KB_ARTICLES
    and TEAM_MEMBERS tables with: a dashboard with charts of tickets by status and category;
    an interactive report on tickets with a form to edit a ticket; and a report on knowledge
    base articles.</copy>
    ```

3. AI responds with an application **blueprint** — a proposed set of pages you can edit before anything is built.

    ![AI-proposed application blueprint](images/app-blueprint.png " ")

## Task 2: Review the Blueprint — Pin the Pages Later Labs Need

1. Before clicking Create, verify the blueprint includes all three of:

    * **Dashboard**
    * **Tickets** — and the page type must be **Interactive Report** (with a form to edit a ticket)
    * **Knowledge Base** report

    > **Why the page type matters:** Lab 4's AI features exist only on Interactive Report regions. If the blueprint chose Faceted Search or Cards for Tickets, change the page type here in the blueprint editor — or add an extra Interactive Report page on TICKETS. Declarative, ten seconds.

2. Adjust anything else you like (this is the review habit from Lab 2, applied to app design), then click **Create Application**.

## Task 3: Run It

1. When the builder finishes, click **Run Application** and sign in with your workspace credentials.

    ![Horizon Help Desk running: dashboard with charts](images/app-running.png " ")

2. Take that in: **a real web application — authentication, a URL you could send to a colleague, responsive UI — from one reviewed prompt.** In most stacks that was your whole afternoon.

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
* **Last Updated By/Date** - Rick Houlihan, July 2026
