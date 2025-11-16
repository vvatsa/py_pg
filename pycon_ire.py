import marimo

__generated_with = "0.17.8"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo, slider):
    mo.md(f"""
    # Hello PyCon Ireland

    {"🐍"*slider.value}
    """)
    return


@app.cell
def _(mo):
    slider = mo.ui.slider(start=1, stop=100, debounce=True)
    slider

    return (slider,)


@app.cell
def _(mo):
    mo.md("""
    # Diagrams
    """)
    return


@app.cell
def _():
    doc = """
    graph TD
        A[PyCon Ireland] --> B(Talk)
        B --> C{see lighting talk list}
        D[Do Lighting Talk]
        C --> E[Drink Beer]
        E --> D
        D --> F[Go to Social]
    
    """
    return (doc,)


@app.cell
def _(doc, mo):
    mo.mermaid(doc)
    return


@app.cell
def _(mo):
    mo.md("""
    # SQL & Dataframes
    """)
    return


@app.cell
def _():
    import sqlalchemy
    engine = sqlalchemy.create_engine("postgresql+psycopg://postgres@localhost/postgres")
    return (engine,)


@app.cell
def _(cve_data, engine, mo):
    _df = mo.sql(
        f"""
        SELECT * from cve_data
        """,
        engine=engine
    )
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
