import marimo

__generated_with = "0.14.10"
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


@app.cell(hide_code=True)
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    - In welchen Ländern verdienen Data Scientists am meisten, in welchen am wenigsten?

    Achten Sie darauf aussagekräftige Antworten zu geben.
    """
    )
    return


@app.cell
def _(ds_salaries, engine, mo):
    _df = mo.sql(
        f"""
        SELECT
            company_location,
            ROUND(AVG(salary_in_usd)) AS average_salary,
            COUNT(*) AS numberOfOffers
        FROM
            ds_salaries
        GROUP BY
            company_location
        HAVING
            numberOfOffers >= 5
        ORDER BY
            average_salary desc
        LIMIT
            10
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""- In welchen Ländern arbeiten besonders viele Mitarbeiter im Homeoffice? In welchen besonders wenige?""")
    return


@app.cell
def _(ds_salaries, engine, mo):
    _df = mo.sql(
        f"""
        SELECT
            company_location,
            AVG(remote_ratio) AS avg_remote,
            COUNT(*) AS numberOfOffers
        FROM
            ds_salaries
        GROUP BY
            company_location
        HAVING
            numberOfOffers >= 5
        ORDER BY
            avg_remote desc
        LIMIT
            10
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Der bereitgestellte Datensatz enthält Meldungen aus mehreren Jahren.

    - Wie haben sich die gemeldeten Gehälter im Bereich Data Science in den letzten Jahren entwickelt?
    """
    )
    return


@app.cell
def _(ds_salaries, engine, mo):
    _df = mo.sql(
        f"""
        SELECT
            company_location,
            work_year,
            ROUND(AVG(salary_in_usd)) AS average_salary
        FROM
            ds_salaries
        WHERE
            company_location IN ('US', 'DE', 'GB')
        GROUP BY
            work_year,
            company_location
        ORDER BY
            company_location,
            work_year
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## GPU Preise""")
    return


@app.cell
def _(GPU, engine, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM GPU
        """,
        engine=engine
    )
    return


@app.cell
def _(Prices, engine, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM Prices
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Offensichtlich unterliegen die Grafikkartenpreise teils großen Schwankungen.

    - Berechnen Sie für jede gelistete Grafikkarte die 5-Number-Summary, um die Preisschwankungen zu aggregieren.
    """
    )
    return


@app.cell
def _(engine, mo):
    _df = mo.sql(
        f"""
        SELECT  GPU_ID, MIN(Price), AVG(Price), MAX(Price) FROM `Prices`
        GROUP BY GPU_ID
        """,
        engine=engine
    )
    return


@app.cell
def _(GPU, engine, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM GPU WHERE ID = '2167257'
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    - Berechnen Sie die Preisänderung der einzelnen Grafikkarten im Vergleich zum ersten Listing.
    - Bestimmen Sie die Karten mit der größten und der kleinsten Trendkomponente.
    """
    )
    return


@app.cell
def _(Prices, engine, mo):
    temp = mo.sql(
        f"""
        SELECT
            DISTINCT(GPU_ID),
            FIRST_VALUE(Price) OVER (PARTITION BY GPU_ID ORDER BY Date) AS first_price,
            julianday(FIRST_VALUE(Date) OVER (PARTITION BY GPU_ID ORDER BY Date)) AS first_date,
            LAST_VALUE(Price) OVER (PARTITION BY GPU_ID ORDER BY Date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_price,
            julianday(LAST_VALUE(Date) OVER (PARTITION BY GPU_ID ORDER BY Date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)) AS last_date
        FROM
            Prices
        GROUP BY
            GPU_ID, Price -- Include all non-aggregated columns in GROUP BY
        ORDER BY
            GPU_ID, Date;
        """,
        engine=engine
    )
    return


@app.cell
def _(Prices, engine, mo):
    _df = mo.sql(
        f"""
        SELECT gpu_id, (last_price - first_price) / (last_date - first_date) as slope FROM
            (SELECT
            DISTINCT(GPU_ID),
            FIRST_VALUE(Price) OVER (PARTITION BY GPU_ID ORDER BY Date) AS first_price,
            julianday(FIRST_VALUE(Date) OVER (PARTITION BY GPU_ID ORDER BY Date)) AS first_date,
            LAST_VALUE(Price) OVER (PARTITION BY GPU_ID ORDER BY Date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_price,
            julianday(LAST_VALUE(Date) OVER (PARTITION BY GPU_ID ORDER BY Date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)) AS last_date
        FROM
            Prices
        GROUP BY
            GPU_ID, Price -- Include all non-aggregated columns in GROUP BY
        ORDER BY
            GPU_ID, Date)
        ORDER BY slope
        """,
        engine=engine
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Ihr Kollege behauptet, dass GPU-Preise saisonalen Schwankungen (Weihnachten, Ferienzeit) unterliegen.

    - Aggregieren Sie alle Karten mit dem RTX 3080 Ti Chip und bestimmen Sie die saisonalen Faktoren um diese These zu untersuchen. Denken Sie an die voherige Trendbereinigung!
    """
    )
    return


@app.cell
def _(GPU, engine, mo):
    _df = mo.sql(
        f"""
        SELECT Name, ID FROM GPU
        WHERE Name LIKE "%3090%"
        """,
        engine=engine
    )
    return


@app.cell
def _(Prices, engine, mo):
    _df = mo.sql(
        f"""
        SELECT
          strftime('%Y', Date)    AS sales_year,
          strftime('%m', Date)    AS sales_month,
          AVG(Price)              AS avgPrice,
          julianday(MIN(Date))    AS month_jd
        FROM Prices
        WHERE GPU_ID IN ('2364388','2366077','2366719')
        GROUP BY sales_year, sales_month
        """,
        engine=engine
    )
    return


@app.cell
def _(Prices, engine, mo):
    _df = mo.sql(
        f"""
        -- 1) Create a temp table holding your trend parameters
        CREATE TEMP TABLE temp_trend AS
        SELECT
          FIRST_VALUE(avgPrice) OVER w    AS first_price,
          LAST_VALUE (avgPrice) OVER w    AS last_price,
          FIRST_VALUE(month_jd)  OVER w   AS first_julianday,
          LAST_VALUE (month_jd)  OVER w   AS last_julianday,
          (
            LAST_VALUE (avgPrice) OVER w
            - FIRST_VALUE(avgPrice) OVER w
          )
          /
          (
            LAST_VALUE (month_jd)  OVER w
            - FIRST_VALUE(month_jd)  OVER w
          )                                AS slope
        FROM (
          SELECT
            strftime('%Y', Date)    AS sales_year,
            strftime('%m', Date)    AS sales_month,
            AVG(Price)              AS avgPrice,
            julianday(MIN(Date))    AS month_jd
          FROM Prices
          WHERE GPU_ID IN ('2364388','2366077','2366719')
          GROUP BY sales_year, sales_month
        )
        WINDOW w AS (
          ORDER BY sales_year, sales_month
          ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        )
        LIMIT 1;
        """,
        engine=engine
    )
    return (temp_trend,)


@app.cell
def _(engine, mo, temp_trend):
    _df = mo.sql(
        f"""
        SELECT slope FROM temp_trend;
        """,
        engine=engine
    )
    return


@app.cell
def _(Prices, engine, mo, temp_trend):
    _df = mo.sql(
        f"""
        CREATE TEMP TABLE seasonalMeans AS
        SELECT sales_month, AVG(detrended) AS seasonalMean from
        (SELECT *, avgPrice + detrend AS detrended FROM
        (SELECT *,     (julianday(sales_year ||  '-' ||  sales_month || '-01') - julianday('2020-09-01')) * (SELECT slope from temp_trend)   AS detrend FROM
        (SELECT
            strftime('%Y', Date)    AS sales_year,
            strftime('%m', Date)    AS sales_month,
            AVG(Price)              AS avgPrice
          FROM Prices
          WHERE GPU_ID IN ('2364388','2366077','2366719')
          GROUP BY sales_year, sales_month)
            )
        )
        GROUP BY sales_month
        """,
        engine=engine
    )
    return (seasonalMeans,)


@app.cell
def _(engine, mo, seasonalMeans):
    seasonalFactors = mo.sql(
        f"""
        SELECT sales_month, seasonalMean / (SELECT sum(seasonalMean) FROM seasonalMeans) AS seasonalFactors FROM seasonalMeans
        """,
        engine=engine
    )
    return (seasonalFactors,)


@app.cell
def _(seasonalFactors):
    seasonalFactors.plot(x="sales_month", y="seasonalFactors", drawstyle="steps-post")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
