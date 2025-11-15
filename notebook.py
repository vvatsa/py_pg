import marimo

__generated_with = "0.17.8"
app = marimo.App(width="medium", layout_file="layouts/notebook.slides.json")


@app.cell
def _():
    import sqlalchemy

    DATABASE_URL = f"postgresql://postgres:@localhost:5432/postgres"
    engine = sqlalchemy.create_engine(DATABASE_URL)
    return (engine,)


@app.cell
def _():
    import marimo as mo
    from pathlib import Path
    return Path, mo


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

    _text = mo.md("""
    * Everything is hard until it isn't
    * Multicorn
      * C - Shared libraries providing interface between postgres and Python FDW
      * Python package - Base class for the FDW
    * Table storage as a function

    """)

    _diag = mo.mermaid("""
    block
    columns 1
      db["Data Tier \n Database/Storage"]
      blockArrowId4<["&nbsp;&nbsp;&nbsp;"]>(down)
      block:ID
        Row[("&nbsp;Row&nbsp;")]
        JSON[("&nbsp;json&nbsp;")]
        Fn[("&nbsp;Fn&nbsp;")]
      end
      space

      style Fn fill:#969,stroke:#333,stroke-width:4px

    """)

    _title = mo.md("""# Data Application Platform 
    ##Postgres + __Multicorn__ + Python ecosystem
    """)

    _body = mo.hstack([_text, _diag], )
    mo.vstack([_title, _body], align='center')
    return


@app.cell
def _(mo):
    mo.md("""
    # A most simple Demo
    """)
    return


@app.cell
def _(mo):
    from multicorn import ForeignDataWrapper

    class DummyFDW(ForeignDataWrapper):

        def __init__(self, options, columns):
            super().__init__(options, columns)
            self.columns = columns
            self.options = options
            self.num_rows = int(self.options.get('num_rows', 20))

        def execute(self, quals, columns):
            for index in range(self.num_rows):
                line = {}
                for col_name in self.columns:
                  line[col_name] = f"{col_name}_{index}"
                yield line
    mo.show_code()
    return (ForeignDataWrapper,)


@app.cell
def _(mo):
    mo.md("""
    <pre>
    CREATE EXTENSION multicorn;
    create SERVER dummy FOREIGN DATA WRAPPER multicorn options ( wrapper 'DummyFDW');
    CREATE FOREIGN TABLE test (
        test character varying,
        test2 character varying
        ) server dummy options(
            num_rows '100'
        );
    </pre>
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    select * from test;
    """)
    return


@app.cell
def _(engine, mo, test):
    _df = mo.sql(
        f"""
        select * from test;
        """,
        engine=engine
    )
    return


@app.cell
def _(mo):
    mo.md("""
    # select * from internet
    """)
    return


@app.cell
def _(ForeignDataWrapper, datetime, mo, nvdlib, timedelta):

    def get_recent_cves(days=2):
        # Get the current date and time
        now = datetime.now()
        days_ago = now - timedelta(days=days)

        cves = nvdlib.searchCVE(pubStartDate=days_ago, pubEndDate=now, cvssV3Severity='CRITICAL')
        return [(cve.id, _description(cve), _cvss_score(cve)) for cve in cves]


    class CVEData(ForeignDataWrapper):
        def __init__(self, options, columns):
            super().__init__(options, columns)

        def execute(self, quals, columns):
            cves = get_recent_cves()
            return cves
    mo.show_code()
    return


@app.cell
def _(mo):
    mo.md("""
    <pre>
    CREATE SERVER CVE_DATA FOREIGN DATA WRAPPER multicorn options ( wrapper 'CVEData');
    CREATE FOREIGN TABLE cve_data (
        cve_id character varying,
        description character varying,
        score character varying
    ) server CVE_DATA;
    </pre>
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    select * from cve_data
    """)
    return


@app.cell
def _(cve_data, engine, mo):
    _df = mo.sql(
        f"""
        select * from cve_data
        """,
        engine=engine
    )
    return


@app.cell
def _(mo):
    mo.md("""
    # select * from numpy
    """)
    return


@app.cell
def _(ForeignDataWrapper, INFO, log_to_postgres, mo, np):
    class NpNormal(ForeignDataWrapper):
        def __init__(self, options, columns):
            super().__init__(options, columns)
            self.mean = int(options.get('mean', 0))
            self.std = int(options.get('std', 1))
            self.size = int(options.get('size', 100))

        def _quals_to_dict(self, quals):
            return {qual.field_name: int(qual.value) for qual in quals if qual.operator == '='}

        def execute(self, quals, columns):
            _quals_dict = self._quals_to_dict(quals)
            mean = _quals_dict.get('mean', self.mean)
            std = _quals_dict.get('std', self.std)
            size = _quals_dict.get('size', self.size)
            log_to_postgres(f"Executing NpNormal with mean={mean}, std={std}, size={size}", level=INFO)
            for idx, smpl in enumerate(np.random.normal(loc=mean, scale=std, size=size)):
                yield idx, smpl, mean, std, size
    mo.show_code()
    return


@app.cell
def _(mo):
    mo.md("""
    <pre>
    CREATE SERVER NP_NORMAL FOREIGN DATA WRAPPER multicorn options ( wrapper 'NpNormal');
    CREATE FOREIGN TABLE np_normal (
        idx integer,
        sample numeric,
        mean integer,
        std integer,
        size integer
    ) server NP_NORMAL options(
        mean '0',
        std '1',
        size '100'
    );
    </pre>
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    select * from np_normal where size = '1000' and mean=2;
    """)
    return


@app.cell
def _(engine, mo, np_normal):
    _df = mo.sql(
        f"""
        select * from np_normal where size = '1000' and mean=2;
        """,
        engine=engine
    )
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
def _(mo):
    mo.md("""
    # Multicorn

    ## SQL operations supported by Multicorn

    * def execute(self, quals, columns, sortkeys=None, limit=None, offset=None):
    * def insert(self, values):
    * def update(self, oldvalues, newvalues):
    * def delete(self, oldvalues):


    ## Tables are just functions, we can create FDW in a few lines of python.
    """)
    return


@app.cell
def _(Path, mo):
    _img = mo.image(Path("public/kent-brockman-insect-overlords.gif"), rounded=True, width=400, height=300)
    mo.md(f"""
    # I for one welcome our robot overlords

    {_img}

    """)
    return


@app.cell
def _(mo):
    mo.md("""
    # PGVector
    ## Open-source vector similarity search for Postgres

    ## Distance search

    *    <-> - L2 distance
    *    <#> - (negative) inner product
    *    <=> - cosine distance
    *    <+> - L1 distance
    *    <~> - Hamming distance (binary vectors)
    *    <%> - Jaccard distance (binary vectors)

    # Plus all of the other great features of Postgres
    """)
    return


@app.cell
def _(mo):
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
    mo.show_code()
    return llm, vectorstore


@app.cell
def _(mo, vectorstore):
    # Load data into vector db
    for f_name in ["cheuk.txt", "luca.txt"]:
        with open(f_name, 'r') as fd:
            _data = fd.read()
        vectorstore.add_texts(texts=[_data])
    mo.show_code()
    return


@app.cell
def _(llm, mo, vectorstore):
    retriever = vectorstore.as_retriever()

    retrieved_documents = retriever.invoke("Python Talks")

    ai_resp = llm.invoke(f"""
    FROM: {retrieved_documents}

    What is in the document
    """)
    print(ai_resp)
    mo.show_code()
    return


@app.cell
def _(mo):
    mo.md(r"""
    The document contains two talks:

    **Talk 1: "Story About the Python GIL - its Existence and the Lack Thereof"**

    * Title: Cheuk Ting Ho
    * Summary: A talk about the Global Interpreter Lock (GIL) in Python, including:
    + Concurrency in Python
    + Multi-threading under the hood
    + The role of the GIL in Python processes
    + Differences between free-threaded Python 3.13 and regular Python with the GIL
    + Benchmarking and comparing performance benefits

    **Talk 2: "Build a Tiny Language Model from Scratch"**

    * Title: Luca Gilli
    * Summary: A hands-on workshop on building a Tiny Language Model (TLM) using Andrej Karpathy's LLM.c repository. The workshop covers:
    + Curation of a dataset for small-scale training
    + Designing and configuring a lightweight GPT architecture
    + Training and evaluating the model in resource-constrained environments

    Both talks are aimed at Python developers with a basic understanding of software development, and no prior knowledge of concurrency or language models is required.
    """)
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
def _(mo):
    mo.md("""
    # And other crazy things.... Postgres in your browser
    # PGlite
    ## WASM build of Postgres
    * Persistence in your browser
    * extentions support
     * PGVector...
    """)
    return


@app.cell
def _():




    return


if __name__ == "__main__":
    app.run()
