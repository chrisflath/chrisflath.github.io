import marimo

__generated_with = "0.14.9"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import sqlalchemy

    return mo, pd, sqlalchemy


@app.cell
def _(DATABASE_URL, requests, sqlalchemy):
    url = "https://chrisflath.github.io/notebooks/public/datats.db"

    # Download and save the file
    filename = "data.db"

    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"SQL DB setup successfull")
    else:
        print(f"Failed to download, status: {response.status_code}")
    
    engine = sqlalchemy.create_engine(DATABASE_URL)
    return (engine,)


@app.cell
def _(mo):
    mo.md(r"""#Zeitreihenanalyse""")
    return


@app.cell
def _(mo):
    mo.md(r"""##Einfache Trendanalyse""")
    return


@app.cell
def _(engine, mo, retail_sales):
    salesTS = mo.sql(
        f"""
        SELECT sales_month, sales
        FROM retail_sales
        WHERE kind_of_business = 'Retail and food services sales, total';
        """,
        engine=engine
    )
    return (salesTS,)


@app.cell
def _(pd, salesTS):
    salesTS["sales_month"] = pd.to_datetime(salesTS["sales_month"])
    salesTS.plot(x="sales_month", y="sales")
    return


@app.cell
def _(engine, mo, retail_sales):
    _df = mo.sql(
        f"""
        SELECT sales_month, sales
        FROM retail_sales
        WHERE kind_of_business = 'Retail and food services sales, total'
        ORDER BY sales_month DESC
        LIMIT 1;
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo, retail_sales):
    _df = mo.sql(
        f"""
        SELECT julianday(sales_month), sales
        FROM retail_sales
        WHERE kind_of_business = 'Retail and food services sales, total'
        ORDER BY sales_month
        LIMIT 1;
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo, retail_sales):
    _df = mo.sql(
        f"""
        SELECT julianday(sales_month), sales
        FROM retail_sales
        WHERE kind_of_business = 'Retail and food services sales, total'
        ORDER BY sales_month DESC
        LIMIT 1;
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo, retail_sales):
    _df = mo.sql(
        f"""
        SELECT * FROM (SELECT sales_month as first_month, sales as first_sales
        FROM retail_sales
        WHERE kind_of_business = 'Retail and food services sales, total'
        ORDER BY sales_month
        LIMIT 1),
        (SELECT sales_month as last_month, sales as last_sales
        FROM retail_sales
        WHERE kind_of_business = 'Retail and food services sales, total'
        ORDER BY sales_month DESC
        LIMIT 1);
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo):
    _df = mo.sql(
        f"""
        SELECT 
            last_month, last_sales, (last_sales - first_sales) * 1.0 / (julianday(last_month) - julianday(first_month)) AS slope
        FROM(
        SELECT * FROM (SELECT sales_month as first_month, sales as first_sales
        FROM retail_sales
        WHERE kind_of_business = 'Retail and food services sales, total'
        ORDER BY sales_month
        LIMIT 1),
        (SELECT sales_month as last_month, sales as last_sales
        FROM retail_sales
        WHERE kind_of_business = 'Retail and food services sales, total'
        ORDER BY sales_month DESC
        LIMIT 1))
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo):
    _df = mo.sql(
        f"""
        SELECT 
            '2028-01-01' as sales_month, last_sales + (slope * (julianday('2028-01-01') - julianday(last_month))) AS sales_forecast
        FROM
        (SELECT 
            last_month, last_sales, (last_sales - first_sales) * 1.0 / (julianday(last_month) - julianday(first_month)) AS slope
        FROM(
        SELECT * FROM (SELECT sales_month as first_month, sales as first_sales
        FROM retail_sales
        WHERE kind_of_business = 'Retail and food services sales, total'
        ORDER BY sales_month
        LIMIT 1),
        (SELECT sales_month as last_month, sales as last_sales
        FROM retail_sales
        WHERE kind_of_business = 'Retail and food services sales, total'
        ORDER BY sales_month DESC
        LIMIT 1)))
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo):
    forecastTS = mo.sql(
        f"""
        SELECT sales_month, sales
        FROM retail_sales
        WHERE kind_of_business = 'Retail and food services sales, total'

        UNION

        SELECT 
            '2028-01-01' as sales_month, last_sales + (slope * (julianday('2028-01-01') - julianday(last_month))) AS sales
        FROM
        (SELECT 
            last_month, last_sales, (last_sales - first_sales) * 1.0 / (julianday(last_month) - julianday(first_month)) AS slope
        FROM(
        SELECT * FROM (SELECT sales_month as first_month, sales as first_sales
        FROM retail_sales
        WHERE kind_of_business = 'Retail and food services sales, total'
        ORDER BY sales_month
        LIMIT 1),
        (SELECT sales_month as last_month, sales as last_sales
        FROM retail_sales
        WHERE kind_of_business = 'Retail and food services sales, total'
        ORDER BY sales_month DESC
        LIMIT 1)))
        """,
        engine=engine
    )
    return (forecastTS,)


@app.cell
def _(forecastTS, pd):
    forecastTS["sales_month"] = pd.to_datetime(forecastTS["sales_month"])
    forecastTS.plot(x="sales_month", y="sales")
    return


@app.cell
def _(mo):
    mo.md(r"""## Aggregierte Trends""")
    return


@app.cell
def _(engine, mo, retail_sales):
    yearlySales = mo.sql(
        f"""
        SELECT strftime('%Y',sales_month) as sales_year,
        sum(sales) as sales
        FROM retail_sales
        WHERE kind_of_business = 'Retail and food services sales, total'
        GROUP BY sales_year
        ORDER BY sales_year;
        """,
        engine=engine
    )
    return (yearlySales,)


@app.cell
def _(pd, yearlySales):
    yearlySales["sales_year"] = pd.to_datetime(yearlySales["sales_year"])
    yearlySales.plot(x="sales_year", y="sales")
    return


@app.cell
def _(mo):
    mo.md(r"""## Gruppierte Trends""")
    return


@app.cell
def _(engine, mo, retail_sales):
    groupedTS = mo.sql(
        f"""
        SELECT strftime('%Y',sales_month) as sales_year,
        kind_of_business,
        sum(sales) as sales
        FROM retail_sales
        WHERE kind_of_business in ('Book stores','Sporting goods stores','Hobby, toy, and game stores')
        GROUP BY sales_year, kind_of_business
        ORDER BY sales_year, kind_of_business;
        """,
        engine=engine
    )
    return (groupedTS,)


@app.cell
def _(groupedTS):
    _wide = groupedTS.pivot(
        index='sales_year',
        columns='kind_of_business',
        values='sales'
    )
    _wide.plot()
    return


@app.cell
def _(engine, mo, retail_sales):
    menVSwomen = mo.sql(
        f"""
        SELECT strftime('%Y',sales_month) as sales_year,
        kind_of_business,
        sum(sales) as sales
        FROM retail_sales
        WHERE kind_of_business in ('Men''s clothing stores','Women''s clothing stores')
        GROUP BY sales_year, kind_of_business;
        """,
        engine=engine
    )
    return (menVSwomen,)


@app.cell
def _(menVSwomen):
    _wide = menVSwomen.pivot(
        index='sales_year',
        columns='kind_of_business',
        values='sales'
    )
    _wide.plot()
    return


@app.cell
def _(engine, mo, retail_sales):
    _df = mo.sql(
        f"""
        SELECT strftime('%Y',sales_month) as sales_year,
        sum(case when kind_of_business = 'Women''s clothing stores' then sales end) as womens_sales,
        sum(case when kind_of_business = 'Men''s clothing stores' then sales end) as mens_sales
        FROM retail_sales
        WHERE kind_of_business in ('Men''s clothing stores','Women''s clothing stores')
        GROUP BY sales_year
        ORDER BY sales_year;
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo, retail_sales):
    menVSwomen2 = mo.sql(
        f"""
        SELECT sales_year, womens_sales - mens_sales as womens_minus_mens,
        1.0 * womens_sales / mens_sales as womens_times_of_mens, (1.0 * womens_sales / mens_sales - 1) * 100 as womens_pct_of_mens
        FROM(
        SELECT strftime('%Y',sales_month) as sales_year,
        sum(case when kind_of_business = 'Women''s clothing stores' then sales end) as womens_sales,
        sum(case when kind_of_business = 'Men''s clothing stores' then sales end) as mens_sales
        FROM retail_sales
        WHERE kind_of_business in ('Men''s clothing stores','Women''s clothing stores')
        GROUP BY sales_year)
        ORDER BY sales_year;
        """,
        engine=engine
    )
    return (menVSwomen2,)


@app.cell
def _(menVSwomen2, pd):
    menVSwomen2["sales_year"] = pd.to_datetime(menVSwomen2["sales_year"])
    menVSwomen2.plot(x="sales_year", y="womens_minus_mens", title="Differenz")
    return


@app.cell
def _(menVSwomen2):
    menVSwomen2.plot(x="sales_year", y="womens_pct_of_mens", title="Verhältnis")
    return


@app.cell
def _(engine, mo, retail_sales):
    pctShareTotal = mo.sql(
        f"""
        SELECT 	sales_month, kind_of_business,	sales,
        SUM(sales) OVER (PARTITION BY sales_month) AS total_sales,
        ROUND(sales * 100.0 / SUM(sales) OVER (PARTITION BY sales_month), 1) AS pct_total
        FROM retail_sales
        WHERE kind_of_business in ('Men''s clothing stores','Women''s clothing stores')
        ORDER BY sales_month;
        """,
        engine=engine
    )
    return (pctShareTotal,)


@app.cell
def _(pctShareTotal):
    _wide = pctShareTotal.pivot(
        index='sales_month',
        columns='kind_of_business',
        values='pct_total'
    )
    _wide.plot()
    return


@app.cell
def _(mo):
    mo.md(r"""## Indexierung""")
    return


@app.cell
def _(engine, mo, retail_sales):
    indexiertWomen = mo.sql(
        f"""
        SELECT sales_year,
        kind_of_business,	sales,
        first_value(sales) over (order by sales_year) as index_sales,
        ROUND((1.0 * sales / first_value(sales) OVER (partition by kind_of_business order by sales_year) - 1) * 100,1) as pct_from_index
        FROM
        (SELECT strftime('%Y',sales_month) as sales_year,
        kind_of_business,
        sum(sales) as sales
        FROM retail_sales
        WHERE kind_of_business = 'Women''s clothing stores'
        GROUP BY sales_year);
        """,
        engine=engine
    )
    return (indexiertWomen,)


@app.cell
def _(indexiertWomen):
    indexiertWomen.plot(y="pct_from_index", x="sales_year", title="Indexierte Verkaufszahlen von Frauenbekleidung")
    return


@app.cell
def _(mo):
    mo.md(r"""##Saisonalität""")
    return


@app.cell
def _(engine, mo):
    _df = mo.sql(
        f"""
        DROP TABLE IF EXISTS detrended_sales;
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo):
    _df = mo.sql(
        f"""
        DROP TABLE IF EXISTS monthly_avg;
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo):
    _df = mo.sql(
        f"""
        DROP TABLE IF EXISTS seasonal_factors;
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo, retail_sales):
    _df = mo.sql(
        f"""
        CREATE TABLE detrended_sales AS
        SELECT 
            strftime('%m', sales_month) AS month,
            sales_month,
            sales,
            sales - ((last_sales - first_sales) * 1.0 / (julianday(last_month) - julianday(first_month)) * 
            (julianday(sales_month) - julianday(first_month))) AS detrended_sales
        FROM 
            retail_sales,
            (SELECT 
                (SELECT sales_month
                 FROM retail_sales
                 WHERE kind_of_business = 'Retail and food services sales, total'
                 ORDER BY sales_month
                 LIMIT 1) AS first_month,
                (SELECT sales
                 FROM retail_sales
                 WHERE kind_of_business = 'Retail and food services sales, total'
                 ORDER BY sales_month
                 LIMIT 1) AS first_sales,
                (SELECT sales_month
                 FROM retail_sales
                 WHERE kind_of_business = 'Retail and food services sales, total'
                 ORDER BY sales_month DESC
                 LIMIT 1) AS last_month,
                (SELECT sales
                 FROM retail_sales
                 WHERE kind_of_business = 'Retail and food services sales, total'
                 ORDER BY sales_month DESC
                 LIMIT 1) AS last_sales
            ) AS bounds
        WHERE 
            kind_of_business = 'Retail and food services sales, total'
        ORDER BY 
            sales_month;
        """,
        engine=engine
    )
    return (detrended_sales,)


@app.cell
def _(detrended_sales, engine, mo):
    detrendedSales = mo.sql(
        f"""
        select * from detrended_sales;
        """,
        engine=engine
    )
    return (detrendedSales,)


@app.cell
def _(detrendedSales):
    detrendedSales.plot(x="sales_month", title="Detrended Sales")
    return


@app.cell
def _(detrended_sales, engine, mo):
    _df = mo.sql(
        f"""
        -- Create a temporary table for monthly averages
        CREATE TABLE monthly_avg AS
        SELECT 
            month,
            AVG(detrended_sales) AS avg_detrended_sales
        FROM 
            detrended_sales
        GROUP BY 
            month
        ORDER BY 
            month;
        """,
        engine=engine
    )
    return (monthly_avg,)


@app.cell
def _(engine, mo, monthly_avg):
    _df = mo.sql(
        f"""
        select * from monthly_avg;
        """,
        engine=engine
    )
    return


@app.cell
def _(detrended_sales, engine, mo, monthly_avg):
    _df = mo.sql(
        f"""
        -- Calculate the multiplicative seasonal components
        CREATE TABLE seasonal_factors AS
        SELECT 
            month,
            avg_detrended_sales,
            avg_detrended_sales / (SELECT AVG(detrended_sales) FROM detrended_sales) AS Factor,
            avg_detrended_sales - (SELECT AVG(detrended_sales) FROM detrended_sales) AS Delta
        FROM 
            monthly_avg
        GROUP BY
            month;
        """,
        engine=engine
    )
    return (seasonal_factors,)


@app.cell
def _(engine, mo, seasonal_factors):
    seasonalFactors = mo.sql(
        f"""
        SELECT * FROM seasonal_factors;
        """,
        engine=engine
    )
    return (seasonalFactors,)


@app.cell
def _(seasonalFactors):
    seasonalFactors.plot(x="month", y="Factor", title="Multiplikative saisonale Faktoren")
    return


@app.cell
def _(detrended_sales, engine, mo, seasonal_factors):
    _df = mo.sql(
        f"""
        -- Calculate the overall average of detrended sales (stored in a subquery)
        SELECT 
            d.sales_month,
            d.detrended_sales,
            d.detrended_sales / Factor as multi,
            d.detrended_sales - Delta as additive
        FROM 
            detrended_sales d
        JOIN 
            seasonal_factors m
        ON 
            strftime('%m', d.sales_month) = m.month
        ORDER BY 
            d.sales_month;
        """,
        engine=engine
    )
    return


@app.cell
def _(detrended_sales, engine, mo, seasonal_factors):
    deseasonalined = mo.sql(
        f"""
        SELECT 
            d.sales_month,
            d.detrended_sales,
            d.detrended_sales / Factor as multi,
            d.detrended_sales - Delta as additive
        FROM 
            detrended_sales d
        JOIN 
            seasonal_factors m
        ON 
            strftime('%m', d.sales_month) = m.month
        ORDER BY 
            d.sales_month;
        """,
        engine=engine
    )
    return (deseasonalined,)


@app.cell
def _(deseasonalined):
    deseasonalined.plot(x="sales_month", y="multi", title="Multiplikative Deseasonalierung")
    return


@app.cell
def _(deseasonalined):
    deseasonalined.plot(x="sales_month", y="additive", title="Additive Deseasonalierung")
    return


@app.cell
def _(mo):
    mo.md(r"""##Monatsvergleiche""")
    return


@app.cell
def _(engine, mo, retail_sales):
    monthTOmonth = mo.sql(
        f"""
        -- Vormonat
        SELECT 
        kind_of_business,
        sales_month,
        sales,
        lag(sales_month) over (partition by kind_of_business order by sales_month) as prev_month,
        lag(sales) over (partition by kind_of_business order by sales_month) as prev_month_sales,
        (1.0 * sales / lag(sales) over (partition by kind_of_business order by sales_month) - 1) * 100 as pct_growth_from_previous
        FROM retail_sales
        WHERE kind_of_business = 'Jewelry stores'
        """,
        engine=engine
    )
    return (monthTOmonth,)


@app.cell
def _(monthTOmonth):
    monthTOmonth.plot(
        x="sales_month",
        y="pct_growth_from_previous",
        title="Monatliche Wachstumsrate im Vergleich zum Vormonat"
    )
    return


@app.cell
def _(engine, mo, retail_sales):
    yearToYear = mo.sql(
        f"""
        SELECT 
        kind_of_business,
        sales_month,
        sales,
        lag(sales_month, 12) over (partition by kind_of_business order by sales_month) as prev_month,
        lag(sales , 12) over (partition by kind_of_business order by sales_month) as prev_month_sales,
        (1.0 * sales / lag(sales , 12) over (partition by kind_of_business order by sales_month) - 1) * 100 as pct_growth_from_previous
        FROM retail_sales
        WHERE kind_of_business = 'Jewelry stores'
        """,
        engine=engine
    )
    return (yearToYear,)


@app.cell
def _(yearToYear):
    yearToYear.plot(
        x="sales_month",
        y="pct_growth_from_previous",
        title="Jährliche Wachstumsrate im Vergleich zum Vorjahr"
    )
    return


@app.cell
def _(engine, mo, retail_sales):
    monthlySalesByYear = mo.sql(
        f"""
        SELECT 
        strftime('%m', sales_month) AS month_number,
        MAX(CASE WHEN strftime('%Y', sales_month) = '1992' THEN sales END) AS sales_1992,
        MAX(CASE WHEN strftime('%Y', sales_month) = '1993' THEN sales END) AS sales_1993,
        MAX(CASE WHEN strftime('%Y', sales_month) = '1994' THEN sales END) AS sales_1994
        FROM 
        retail_sales
        WHERE 
        kind_of_business = 'Jewelry stores' 
        AND sales_month BETWEEN '1992-01-01' AND '1994-12-31'
        GROUP BY 
        month_number
        ORDER BY 
        month_number;
        """,
        engine=engine
    )
    return (monthlySalesByYear,)


@app.cell
def _(monthlySalesByYear):
    monthlySalesByYear.plot()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
