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

## Task 1: Grant Model Privileges

1. Open **Database Actions** (SQL) as **ADMIN** — the password you set when creating the database — and run, replacing the schema name with your workspace schema (shown in the APEX SQL Workshop header).

    > **Your schema name is almost certainly `WKSP_` + your workspace name** — for example a workspace
    > called `HELPDESK` uses schema **`WKSP_HELPDESK`**. Autonomous Database adds that prefix when APEX
    > creates a new schema. Use the prefixed name here, exactly as SQL Workshop shows it.

    ```
    <copy>grant execute on dbms_cloud to <your-schema-name>;
    grant create mining model to <your-schema-name>;</copy>
    ```

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

    The model loads in under a minute. (If the download link has rotated, search the Oracle Machine Learning blog for the current *all_MiniLM_L12_v2* ONNX location — the rest of the lab is unchanged.)

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
* **Last Updated By/Date** - Rick Houlihan, July 2026
