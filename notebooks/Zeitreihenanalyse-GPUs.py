import marimo

__generated_with = "0.14.9"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import sqlalchemy
    import requests
    import matplotlib
    return mo, requests, sqlalchemy


@app.cell
def _(requests, sqlalchemy):
    url = "https://chrisflath.github.io/notebooks/public/datats.db"

    # Download and save the file
    filename = "datats.db"

    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"SQL DB setup successfull")
    else:
        print(f"Failed to download, status: {response.status_code}")

    DATABASE_URL = "sqlite:///datats.db"
    engine = sqlalchemy.create_engine(DATABASE_URL)
    return (engine,)


@app.cell
def _(mo):
    mo.md(r"""## Data Science Salaries""")
    return


@app.cell
def _(ds_salaries, engine, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM ds_salaries
        """,
        engine=engine
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    - In welchen Ländern verdienen Data Scientists am meisten, in welchen am wenigsten?

    Achten Sie darauf aussagekräftige Antworten zu geben.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""- In welchen Ländern arbeiten besonders viele Mitarbeiter im Homeoffice? In welchen besonders wenige?""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Der bereitgestellte Datensatz enthält Meldungen aus mehreren Jahren.

    - Wie haben sich die gemeldeten Gehälter im Bereich Data Science in den letzten Jahren entwickelt?

    """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""## GPU Preise""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Offensichtlich unterliegen die Grafikkartenpreise teils großen Schwankungen.

    - Berechnen Sie für jede gelistete Grafikkarte die 5-Number-Summary, um die Preisschwankungen zu aggregieren.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    - Berechnen Sie die Preisänderung der einzelnen Grafikkarten im Vergleich zum ersten Listing.
    - Bestimmen Sie die Karten mit der größten und der kleinsten Trendkomponente.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Ihr Kollege behauptet, dass GPU-Preise saisonalen Schwankungen (Weihnachten, Ferienzeit) unterliegen.

    - Aggregieren Sie alle Karten mit dem RTX 3080 Ti Chip und bestimmen Sie die saisonalen Faktoren um diese These zu untersuchen. Denken Sie an die voherige Trendbereinigung!

    """
    )
    return


if __name__ == "__main__":
    app.run()
