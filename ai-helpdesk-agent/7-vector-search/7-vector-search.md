# Lab 7: Semantic Knowledge-Base Search with AI Vector Search

## Introduction

Keyword search finds articles that share words with the query. Semantic search finds articles that share *meaning*: in this optional lab, "laptop won't connect from hotel wifi" will find your VPN article even though they share almost no words. You'll do it entirely **in-database** — an ONNX embedding model loaded into Oracle AI Database, plain SQL to embed the articles, and a declarative APEX Search Configuration on top. No external AI calls, no extra credentials, and it works identically on the OCI GenAI and OpenAI tracks from Lab 1.

> **Before you start:** if you haven't already, extend your LiveLabs reservation now — one click on your reservation page while it is still active.

> **Glossary — embedding:** a list of numbers (a vector) representing a text's meaning; texts with similar meaning get nearby vectors, which is what makes "hotel wifi" land next to "VPN".

Estimated Time: 15 minutes

### Objectives

In this lab, you will:

* Load a text-embedding ONNX model into your database
* Embed the 20 knowledge-base articles with one SQL statement
* Create a Vector Provider and a declarative Search Configuration
* Build a search page and watch meaning beat keywords

### Prerequisites

This lab assumes you have:

* Completed Lab 2 (the `KB_ARTICLES` table exists; its `embedding` column shipped with the schema)
* **`ADMIN` access to the database** — Task 1's grants cannot be run as your workspace user
* **A way to host a ~127 MB file the database can read** — see the known issue in Task 2. Oracle now
  publishes its ONNX models only as zip archives, so you need an Object Storage bucket (or another
  URL the database can fetch a bare `.onnx` from)

## Task 1: Grant Model Privileges

1. Open **Database Actions** (SQL) as **ADMIN** — the password you set when creating the database — and run, replacing the schema name with your workspace schema (shown in the APEX SQL Workshop header).

    > **Your schema name is almost certainly `WKSP_` + your workspace name** — for example a workspace
    > called `HELPDESK` uses schema **`WKSP_HELPDESK`**. Autonomous Database adds that prefix when APEX
    > creates a new schema. Use the prefixed name here, exactly as SQL Workshop shows it.

    ```
    <copy>grant execute on dbms_cloud to <your-schema-name>;
    grant create mining model to <your-schema-name>;</copy>
    ```

    > **Run both statements.** In Database Actions the green ▶ button is *Run Statement* and executes only
    > the one under your cursor — use **Run Script** (or press F5) so both grants run. If you miss the
    > `dbms_cloud` grant, Task 2 fails with `PLS-00201: identifier 'DBMS_CLOUD' must be declared`, which
    > gives no hint that a grant is the cause.

    ![Database Actions SQL as ADMIN running the grants](images/admin-grants.png " ")

## Task 2: Load the Embedding Model

1. Back in APEX, in **SQL Workshop > SQL Commands**, load Oracle's all-MiniLM-L12-v2 text embedding model straight from Oracle's public model bucket:

    ```
    <copy>begin
      dbms_vector.load_onnx_model(
        model_name => 'minilm_l12',
        model_data => dbms_cloud.get_object(
                        credential_name => null,
                        object_uri      => 'https://adwc4pm.objectstorage.us-ashburn-1.oci.customer-oci.com/p/VBRD9P8ZFWkKvnfhrWxkpPe8K03-JIoM5h_8EJyJcpE80c108fuUjg7R5L5O7mMZ/n/adwc4pm/b/OML-Resources/o/all_MiniLM_L12_v2.onnx'),
        metadata   => json('{"function":"embedding","embeddingOutput":"embedding","input":{"input":["data"]}}')
      );
    end;</copy>
    ```

    > **🔴 KNOWN ISSUE — this URL no longer works (verified 2026-08-30).** It returns
    > `ORA-20401: Authorization failed for URI`. The pre-authenticated link has expired *and* Oracle has
    > moved the models to a new bucket where **only `_augmented.zip` archives are published — there is no
    > bare `.onnx` for any model**. Because the database cannot unzip, and `DBMS_VECTOR` in 26ai offers no
    > cloud loader, this step cannot be fixed by swapping the URL.
    >
    > **To get the current model:** open
    > `https://docs.oracle.com/pls/topic/lookup?ctx=en/database/oracle/oracle-database/26/vecse&id=oml_ai_models_object_storage`
    > — a stable link that redirects to Oracle's current *Machine Learning AI models* page — and download
    > `all_MiniLM_L12_v2_augmented.zip` (~117 MB). Unzip it to get `all_MiniLM_L12_v2.onnx` (~127 MB), then
    > make that file reachable from the database: upload it to an Object Storage bucket in your own
    > compartment, create a pre-authenticated request for it, and use that URI as the `object_uri` above.
    >
    > **Never hard-code a PAR in your own work either** — they expire. That is exactly what broke here.

    ![LOAD_ONNX_MODEL run in SQL Commands](images/load-onnx.png " ")

## Task 3: Embed the Knowledge Base — One SQL Statement

1. Run [embed-kb.sql](files/embed-kb.sql):

    ```
    <copy>update kb_articles
       set embedding = vector_embedding(minilm_l12 using title || ' ' || content as data);

    commit;

    select count(*) as embedded from kb_articles where embedding is not null;</copy>
    ```

    Expected result: **20**. That's the entire embedding pipeline — one SQL function, running next to your data. Nothing left the database.

## Task 4: Create the Vector Provider and Search Configuration

1. Navigate to **App Builder > Workspace Utilities > All Workspace Utilities > Vector Providers**, click **Create**, and enter/select:

    * Provider Type: **Database ONNX Model**
    * Name: **KB MiniLM** — Static ID: **kb\_minilm**
    * ONNX Model Owner: *your schema* — ONNX Model Name: **MINILM\_L12**

    ![Vector Provider configuration](images/vector-provider.png " ")

2. In your app's **Shared Components**, under **Navigation and Search**, select **Search Configurations**, click **Create**, and enter/select:

    * Name: **KB Semantic Search**
    * Search Type: **Oracle Vector Search**
    * Vector Provider: **KB MiniLM** (it embeds the user's query at runtime)
    * Source: table **KB\_ARTICLES**, vector column **EMBEDDING**
    * Title Column: **TITLE** — Description Column: **CONTENT**

    ![Search Configuration with Oracle Vector Search type](images/search-config.png " ")

## Task 5: Build the Search Page and Beat Keywords

1. **Create Page > Search Page**, name it **Ask the Knowledge Base**, and include the **KB Semantic Search** configuration.

2. Run the page and search:

    ```
    <copy>laptop won't connect from hotel wifi</copy>
    ```

    The VPN error 812 article comes back on top — **zero keyword overlap, pure meaning**. Try a few more: `email box is jammed`, `screen keeps blinking`.

    ![Semantic search results for the hotel wifi query](images/semantic-results.png " ")

## Go Further (optional)

* Compare with a plain **Standard** search configuration on the same table — run the hotel-wifi query in both and note the difference.
* Ask the APEX Assistant to write a SQL query using `vector_distance()` to find the 3 nearest articles to a phrase — review it, then run it (the Lab 2 habit, one last time).

You may now **proceed to the next lab**.

## Learn More

* [AI Vector Search in Oracle APEX](https://www.oracle.com/artificial-intelligence/ai-vector-search-in-apex/)

## Acknowledgements

* **Author** - Rick Houlihan
* **Last Updated By/Date** - Rick Houlihan, August 2026
