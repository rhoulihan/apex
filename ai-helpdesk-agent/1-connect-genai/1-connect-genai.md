# Lab 1: Connect APEX to Generative AI

## Introduction

Every AI feature in this workshop — the APEX Assistant, app generation, AI Interactive Reports, and the help desk agent — talks to a Generative AI service that you configure once, at the workspace level. In this lab you create that service and prove it works.

You can use **OCI Generative AI** (default for this workshop) or **OpenAI** (bring your own API key). Use the selector at the top of this page to switch instructions.

Estimated Time: 10 minutes

### Objectives

In this lab, you will:

* Create an API key for your AI provider
* Configure a Generative AI service in your APEX workspace
* Set a token quota on the service
* Test the wiring with the APEX Assistant

### Prerequisites

This lab assumes you have:

* An APEX workspace (previous lab) with your Autonomous Database up and running

<if type="OCIGenAI">

## Task 1: Generate API Keys using the OCI Console

OCI API keys are a public/private key pair used to authenticate REST calls to OCI services — including OCI Generative AI.

1. In the OCI Console, click **Profile** at the top-right corner and select your username.

    ![Profile menu in the OCI Console](images/oci-profile.png " ")

2. Switch to the **Tokens and keys** tab and click **Add API key**.

    ![Tokens and keys tab with Add API key button](images/oci-add-api-key.png " ")

3. Select **Generate API Key Pair**, then click **Download Private Key**. A *.pem* file is saved to your device — you paste its contents into APEX in the next task.

    > **Keep the private key private.** Never share the .pem file or upload it anywhere; anyone holding it can call OCI services as you.

4. Click **Add**. The **Configuration File Preview** appears — copy the whole snippet into a scratch note. It contains your **user OCID**, **tenancy OCID**, and **key fingerprint**, all needed in the next task.

    ![Configuration file preview dialog](images/oci-config-preview.png " ")

5. You also need your **assigned compartment's OCID** — this one is *not* in the configuration file. In the LiveLabs Sandbox, open your reservation details to find your assigned compartment, or in the OCI Console navigate to **Identity & Security > Compartments** and copy the OCID shown next to your compartment.

    ![Compartments page showing the compartment OCID](images/oci-compartment-ocid.png " ")

## Task 2: Configure the Generative AI Service in APEX

1. In APEX, from the workspace home page navigate to **App Builder > Workspace Utilities > Generative AI**, and click **Create**.

    ![Workspace Utilities Generative AI page](images/genai-create.png " ")

2. Enter/select the following:

    * AI Provider: **OCI Generative AI Service**
    * Name: **Helpdesk AI**
    * Static ID: **helpdesk\_ai** — Labs 5 and 7 refer to the service by this exact ID
    * Compartment ID: your assigned compartment OCID from Task 1, step 5
    * Region: **us-chicago-1** (OCI Generative AI runs in a limited set of regions; APEX calls it over REST, so your database can live anywhere)
    * Model ID: **pick the latest available chat model from the list** — pre-trained models are deprecated regularly, so this lab never names one
    * Used by App Builder: toggle **ON**

    > **Don't skip the toggle.** "Used by App Builder" is what lights up the APEX Assistant in the builder — it's the most commonly missed step in this lab.

3. For Credential, select **Create New** and enter, from your Task 1 scratch note:

    * **OCI User ID** (the user OCID)
    * **OCI Private Key** (paste the full contents of the downloaded .pem file)
    * **OCI Tenancy ID** (the tenancy OCID)
    * **OCI Public Key Fingerprint**

4. Click **Test Connection**. When it succeeds, click **Create**.

    ![Generative AI service configuration with successful test](images/genai-service-created.png " ")

    > **If Test Connection fails:** re-check the region spelling (`us-chicago-1`, exactly) and that all four credential fields came from the same API key. At a live event, a rate-limit error just means the room is busy — wait 30 seconds and retry.

</if>

<if type="OpenAI">

## Task 1: Get an OpenAI API Key

1. Sign in at the OpenAI platform site, open **API keys**, and create a new secret key. Copy it immediately — it is shown only once.

    ![OpenAI API keys page](images/openai-key.png " ")

    > **Where your data goes on this track.** With OpenAI as the provider, your prompts — and any data the AI features send as context (query results, ticket text) — go to a third party. That's fine for this workshop's synthetic seed data; evaluate it deliberately for your own applications.

    > At an instructor-led event, use the event-provided key shown on screen instead of creating your own. Self-paced? You need your own (paid) OpenAI key on this track — or switch this page to the OCI Generative AI instructions.

## Task 2: Configure the Generative AI Service in APEX

1. In APEX, from the workspace home page navigate to **App Builder > Workspace Utilities > Generative AI**, and click **Create**.

    ![Workspace Utilities Generative AI page](images/genai-create.png " ")

2. Enter/select the following:

    * AI Provider: **OpenAI**
    * Name: **Helpdesk AI**
    * Static ID: **helpdesk\_ai** — Labs 5 and 7 refer to the service by this exact ID
    * Model ID: **pick the latest available chat model from the list**
    * Used by App Builder: toggle **ON**
    * Credential: **Create New**, and paste your API key

    > **Don't skip the toggle.** "Used by App Builder" is what lights up the APEX Assistant in the builder — it's the most commonly missed step in this lab.

3. Click **Test Connection**. When it succeeds, click **Create**.

    ![Generative AI service configuration with successful test](images/genai-service-created.png " ")

</if>

## Task 3: Set a Token Quota on the Service

> **Glossary — token:** the unit LLMs read and bill by (a short word is roughly one token). Every AI call in this workshop spends tokens.

1. Edit the **Helpdesk AI** service you just created and set **Maximum AI Tokens** to **500000**, then save.

    ![Maximum AI Tokens setting on the Generative AI service](images/max-ai-tokens.png " ")

2. **Governance beat #1 — you cap your own AI usage declaratively.** This quota is the first of five governance mechanisms you'll meet today; the others appear in Labs 2, 4, and 5. No code, no proxy — a workspace setting.

## Task 4: Prove the Wiring with the APEX Assistant

1. Navigate to **SQL Workshop > SQL Commands** and click the **APEX Assistant** button in the toolbar.

2. Ask it:

    ```
    <copy>Write a query that shows today's date in three different formats.</copy>
    ```

3. The Assistant streams back a query — click **Insert** and run it. If you get SQL and a result, everything downstream of this lab will work.

    ![APEX Assistant generating a query in SQL Commands](images/assistant-test.png " ")

## Go Further (optional)

Paste this block into SQL Commands, select it, and ask the APEX Assistant to *explain* it — you'll meet this exact code again in Lab 5 as your AI agent's write tool:

```
<copy>declare
  l_subject tickets.subject%type;
begin
  select subject into l_subject from tickets where id = :TICKET_ID;
  update tickets set status = 'Resolved' where id = :TICKET_ID;
  apex_ai.set_tool_result(
    p_result => 'Ticket ' || :TICKET_ID || ' ("' || l_subject || '") is now Resolved.');
end;</copy>
```

You may now **proceed to the next lab**.

## Learn More

* [Managing Generative AI Services](https://docs.oracle.com/en/database/oracle/apex/26.1/htmdb/managing-generative-ai-services.html)
* [OCI Generative AI regions and models](https://docs.oracle.com/en-us/iaas/Content/generative-ai/overview.htm)

## Acknowledgements

* **Author** - Rick Houlihan
* **Last Updated By/Date** - Rick Houlihan, July 2026
