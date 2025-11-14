import marimo

__generated_with = "0.17.8"
app = marimo.App(width="medium", layout_file="layouts/notebook.slides.json")


@app.cell
def _(mo):
    mo.md(f"""
    # An ode to Postgres


    ## PyCon Ireland 2025
    ## Vishal Vatsa
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Agenda

    * $whoami
    * Postgres - History
    * Classical / Document DB
    * FDW Extentsions
    * Multicorn
    * PGVector
    * Usecase Demos
        * API Wrapper
        * Data Lakes
        * Data Science Libraries
        * AI
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # $ whoami

    ## Vishal Vatsa
    * Software Engineeer, 20+ as a Python dev
    * Built
      * HPC
      * API
      * Distributed systems
      * Frameworks
      * Abused Postgres
      * Application Security and Audit Systems
      * (ab)Using Gen AI
    """)
    return


@app.cell
def _(Path, mo):
    _img = mo.image(Path("public/stonebraker.jpg"), rounded=True, width=400, height=300)
    mo.md(f"""
    # Postgres - History

    ## Michale Stonebraker (yes, that’s his real name)

    {_img}

    * Started the modern relational database movement
    * Co-Created INGRES 
    * Co-Created Postgres (POST-in-GRES)
    * 2014 ACM Turing Award 
    """)
    return


@app.cell
def _(mo):
    _title = mo.md("# Postgres - History") 
    _diag = mo.mermaid("""
    flowchart LR

        ingres(Ingres _QUEL_)
        postgres(Postgres _POSTQUEL_)
        postgres95(PostgreSQL _SQL_)

        ingres -- (80s) --> postgres
        postgres -- (mid 90s) --> postgres95

    """)

    mo.vstack([_title, _diag])
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Postgres - History

    ## Milestones
    * 0 - 5 - DARPA funded
    * 6.0 (1996) - 1st PostgreSQL release, MVCC
    * 7.x - FK, WAL, Outer Joins, SQL FN
    * 8.x - Full txt search, xml type, CTE
    * 9+ - JSONB, FDW
    * 12+ - Pluggable storage
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Postgres - Derived

    * Amazon Aurora & RDS
    * Parcel/AWS Redshift
    * Greenplum
    * TimescaleDB
    """)
    return


@app.cell
def _(mo):
    _diag = mo.mermaid("""
    erDiagram
        users ||--o{ posts : creates

        users {
            int id PK
            string username
            string email
        }

        posts {
            int id PK
            int user_id FK
            string title
            text content
        }
    """)

    _sql = mo.md("""
    <pre>
        SELECT 
            u.username,
            p.title AS post_title
        FROM 
            users u
        INNER JOIN 
            posts p ON u.id = p.user_id
         ORDER BY 
            u.username, p.title
    <pre>
    """)

    _title = mo.md("""
    # Basic Relational Table
    """)

    _body = mo.hstack([_diag, _sql])

    mo.vstack(items=[_title, _body], align='center')
    return


@app.cell
def _(mo):
    _diag = mo.mermaid("""
    erDiagram
        users {
            int id PK
            string username
            string email
            jsonb posts
        }
    """)

    _sql = mo.md("""
    <pre>
    SELECT 
        u.username,
        post->>'title' AS post_title
    FROM 
        users u,
        JSONB_ARRAY_ELEMENTS(u.posts) AS post
    ORDER BY 
        u.username, post->>'title';

    </pre>
    """)
    _body = mo.hstack(items=[_diag, _sql])
    _title = mo.md("""
    # JSON + SQL
    """)

    mo.vstack(items=[_title, _body], align='center')
    return


@app.cell
def _(mo):
    _diag = mo.mermaid("""
    erDiagram
        locations {
            int id PK
            string name
            geometry location
            string category
        }
    """)
    _sql = mo.md("""
    <pre>

    -- Find all locations within 5km of a point (Times Square)
    SELECT 
        name,
        category,
        ST_Distance(
            location::geography,
            ST_SetSRID(ST_MakePoint(-73.9855, 40.7580), 4326)::geography
        ) / 1000 AS distance_km
    FROM 
        locations
    WHERE 
        ST_DWithin(
            location::geography,
            ST_SetSRID(ST_MakePoint(-73.9855, 40.7580), 4326)::geography,
            5000  -- 5000 meters = 5km
        )
    ORDER BY 
        distance_km;

    </pre>
    """)
    _title = mo.md("# PostGIS ")
    _body = mo.hstack([_diag, _sql])
    mo.vstack([_title, _body], align='center')
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Foreign Data Wrapper

    * Std: SQL/MED (Mangement of External Data)
    * Full Read/Write support from v9.3 (2013)
    * But you have to write C 😩 or 😀
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Data Application Platform
    ## Postgres + __Multicorn__ + Python ecosystem

    Everything is hard until it isn't

    * Multicorn
      * C - Shared libraries providing interface between postgres and Python FDW
      * Python package - Base class for the FDW
    * Table storage as a function
    """)
    return


@app.cell
def _(engine, mo):
    _df = mo.sql(
        f"""
        SELECT
            *
        FROM
            "information_schema"."foreign_servers"
        """,
        engine=engine
    )
    return


@app.cell
def _():
    import sqlalchemy

    DATABASE_URL = f"postgresql://postgres:@localhost:5432/postgres"
    engine = sqlalchemy.create_engine(DATABASE_URL)
    return (engine,)


@app.cell
def _(engine, mo, np_normal):
    _df = mo.sql(
        f"""
        Select
            *
        from
            np_normal where mean=5 and size=1000;
        """,
        engine=engine
    )
    return


@app.cell
def _():
    import marimo as mo
    from pathlib import Path
    return Path, mo


@app.cell
def _():
    from langchain_ollama import OllamaEmbeddings, OllamaLLM
    from langchain_postgres import PGVector
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    embeddings = OllamaEmbeddings(
        model="llama3:8b",
    )

    llm = OllamaLLM(model="llama3:8b")

    vectorstore = PGVector(
        embeddings=embeddings,
        connection="postgresql+psycopg://postgres@localhost:5432/postgres", 
        collection_name="py_con_irl"
    )
    return llm, vectorstore


@app.cell
def _(vectorstore):
    for f_name in ["cheuk.txt", "luca.txt"]:
        with open(f_name, 'r') as fd:
            _data = fd.read()
        vectorstore.add_texts(texts=[_data])
    return


@app.cell
def _(llm, vectorstore):
    # Use the vectorstore as a retriever
    retriever = vectorstore.as_retriever()

    # Retrieve the most similar text
    retrieved_documents = retriever.invoke("cheuk ")
    ai_resp = llm.invoke(f"""
    FROM: {retrieved_documents[0]}

    What is in the document
    """)
    print(ai_resp)
    return retrieved_documents, retriever


@app.cell
def _(retrieved_documents):
    retrieved_documents
    return


@app.cell
def _(retriever):
    retriever.invoke("cheuk")
    return


@app.cell
def _(engine, langchain_pg_embedding, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM "langchain_pg_embedding" LIMIT 100
        """,
        engine=engine
    )
    return


@app.cell
def _():




    return


if __name__ == "__main__":
    app.run()
