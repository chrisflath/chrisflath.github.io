# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "polars",
#     "duckdb",
#     "plotly",
# ]
# ///

import marimo

__generated_with = "0.10.14"
app = marimo.App(width="medium", app_title="DMA Session 13: Zeitreihenanalyse")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Vorlesung 13: Zeitreihenanalyse

        **Kursfahrplan:** I: SQL-Grundlagen (S1–4) · II: Datenmodellierung (S5–8) · III: Fortgeschrittenes SQL (S9–10) · **▸ IV: Datenanalyse (S11–14)**

        Session 11 hat Querschnittsdaten analysiert, Session 12 hat statistische Signifikanz getestet. Jetzt kommt die Zeitdimension dazu: Wie verändern sich Daten über die Zeit?

        **Lernziele:**
        - Zeitreihendaten analysieren und Trends/Saisonalität erkennen
        - Window Functions: LAG, LEAD, ROW_NUMBER, RANK
        - Moving Averages mit SQL berechnen
        - Year-over-Year Vergleiche durchführen

        **Datenquelle:** U.S. Census Bureau - Monthly Retail Trade Survey (1992-2020)
        """
    )
    return


@app.cell
def _():
    import marimo as mo
    import polars as pl
    import plotly.express as px
    return mo, pl, px


@app.cell(hide_code=True)
def _(mo, pl):
    # Retail Sales Daten laden
    try:
        csv_path = mo.notebook_location() / "public" / "us_retail_sales.csv"
        retail_sales = pl.read_csv(str(csv_path))

        # Datentypen anpassen
        retail_sales = retail_sales.with_columns([
            pl.col("sales_month").str.to_date("%Y-%m-%d"),
            pl.col("sales").cast(pl.Float64)
        ])
        daten_quelle = "U.S. Census Bureau - Monthly Retail Trade Survey (1992-2020)"
    except Exception:
        from datetime import date
        retail_sales = pl.DataFrame({
            "sales_month": [date(2019, m, 1) for m in range(1, 13)] + [date(2020, m, 1) for m in range(1, 13)],
            "kind_of_business": ["Jewelry stores"] * 12 + ["Book stores"] * 12,
            "sales": [2500.0, 2200.0, 2800.0, 2600.0, 2900.0, 3100.0,
                      2700.0, 2500.0, 2800.0, 3000.0, 3500.0, 5200.0,
                      1100.0, 1000.0, 1050.0, 1100.0, 1150.0, 900.0,
                      850.0, 1200.0, 1300.0, 1100.0, 1050.0, 1400.0],
        })
        daten_quelle = "Offline-Daten (Fallback)"
        mo.callout(mo.md("**Hinweis:** CSV konnte nicht geladen werden. Es werden Beispieldaten verwendet."), kind="warn")
    return daten_quelle, retail_sales


@app.cell(hide_code=True)
def _(daten_quelle, mo):
    mo.md(
        f"""
        **Datenquelle:** {daten_quelle}

        ---

        ## Phase 1: Daten erkunden

        Unser Datensatz enthält monatliche Einzelhandelsumsätze für verschiedene Branchen.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 13.1: Datenüberblick

        Wie viele Datensätze haben wir? Welche Branchen sind enthalten?
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    mo.sql(
        f"""
        SELECT
            COUNT(*) AS anzahl_datensaetze,
            COUNT(DISTINCT kind_of_business) AS anzahl_branchen,
            MIN(sales_month) AS erster_monat,
            MAX(sales_month) AS letzter_monat
        FROM retail_sales
        """
    )


@app.cell
def _(mo, retail_sales):
    mo.sql(
        f"""
        SELECT DISTINCT kind_of_business
        FROM retail_sales
        ORDER BY kind_of_business
        LIMIT 15
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 13.2: Erste Visualisierung

        Wie entwickelt sich der Gesamtumsatz über die Zeit?
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    total_sales = mo.sql(
        f"""
        SELECT sales_month, sales
        FROM retail_sales
        WHERE kind_of_business = 'Retail and food services sales, total'
        ORDER BY sales_month
        """
    )
    return (total_sales,)


@app.cell
def _(px, total_sales):
    fig_total = px.line(
        total_sales,
        x="sales_month",
        y="sales",
        title="US Retail Sales - Gesamt (1992-2020)",
        labels={"sales_month": "Monat", "sales": "Umsatz (Mio. USD)"}
    )
    fig_total


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Deutlicher Aufwärtstrend mit starker Saisonalität (Weihnachtsgeschäft).

        > **Vorhersage:** Betrachten Sie die Zeitreihe oben. Um wie viel Prozent schätzen Sie den typischen Dezember-Umsatz höher als den Jahresdurchschnitt? Und was passiert im Jahr 2020?

        ---

        ## Phase 2: Window Functions - Syntax

        Window Functions berechnen Werte über ein "Fenster" von Zeilen,
        **ohne** die Zeilen zu reduzieren (anders als GROUP BY).
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 13.3: Laufende Summe

        Berechnen Sie die kumulierte Summe der Umsätze für Buchläden.
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    mo.sql(
        f"""
        SELECT
            sales_month,
            sales,
            SUM(sales) OVER (ORDER BY sales_month) AS cumulative_sales
        FROM retail_sales
        WHERE kind_of_business = 'Book stores'
        ORDER BY sales_month
        LIMIT 20
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 13.4: Ranking

        Welche Monate hatten die höchsten Umsätze bei Juwelieren?
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    mo.sql(
        f"""
        SELECT
            sales_month,
            sales,
            RANK() OVER (ORDER BY sales DESC) AS rang
        FROM retail_sales
        WHERE kind_of_business = 'Jewelry stores'
        ORDER BY rang
        LIMIT 10
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 3: LAG und LEAD

        Mit LAG greifen wir auf den Wert einer **vorherigen** Zeile zu,
        mit LEAD auf den Wert einer **nachfolgenden** Zeile.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 13.5: Monatliche Änderung

        Berechnen Sie die monatliche Änderung der Umsätze für Juweliergeschäfte.
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    monthly_change = mo.sql(
        f"""
        SELECT
            sales_month,
            sales,
            LAG(sales, 1) OVER (ORDER BY sales_month) AS prev_month_sales,
            sales - LAG(sales, 1) OVER (ORDER BY sales_month) AS abs_change,
            ROUND((sales * 1.0 / LAG(sales, 1) OVER (ORDER BY sales_month) - 1) * 100, 1)
                AS pct_change
        FROM retail_sales
        WHERE kind_of_business = 'Jewelry stores'
        ORDER BY sales_month
        """
    )
    return (monthly_change,)


@app.cell
def _(monthly_change, px):
    fig_change = px.bar(
        monthly_change.drop_nulls(),
        x="sales_month",
        y="pct_change",
        title="Monatliche Umsatzänderung - Juweliere (%)",
        labels={"sales_month": "Monat", "pct_change": "Änderung (%)"}
    )
    fig_change.update_traces(marker_color=["green" if x > 0 else "red" for x in monthly_change.drop_nulls().get_column("pct_change")])
    fig_change


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 13.6: Selbstständig - Sportgeschäfte analysieren

        Berechnen Sie die monatliche prozentuale Änderung für "Sporting goods stores".
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    # Ihre Lösung hier:
    mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: Verwenden Sie LAG(sales, 1) OVER (ORDER BY sales_month)
        -- Filter: WHERE kind_of_business = 'Sporting goods stores'
        -- Erwartete Spalten: sales_month, sales, prev_month, pct_change
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 4: Moving Averages

        Gleitende Durchschnitte glätten kurzfristige Schwankungen und machen den Trend sichtbar.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 13.7: 12-Monats Moving Average

        Berechnen Sie einen 12-Monats gleitenden Durchschnitt (trailing).
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    ma_12 = mo.sql(
        f"""
        SELECT
            sales_month,
            sales,
            ROUND(AVG(sales) OVER (
                ORDER BY sales_month
                ROWS BETWEEN 11 PRECEDING AND CURRENT ROW
            ), 0) AS ma_12
        FROM retail_sales
        WHERE kind_of_business = 'Retail and food services sales, total'
        ORDER BY sales_month
        """
    )
    return (ma_12,)


@app.cell
def _(ma_12, px):
    ma_df = ma_12
    fig_ma = px.line(
        ma_df,
        x="sales_month",
        y=["sales", "ma_12"],
        title="Retail Sales mit 12-Monats Moving Average",
        labels={"sales_month": "Monat", "value": "Umsatz (Mio. USD)", "variable": "Serie"}
    )
    fig_ma


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 13.8: Selbstständig - 3-Monats MA

        Berechnen Sie einen zentrierten 3-Monats Moving Average für Buchläden.

        *Hinweis: ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING*
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    # Ihre Lösung hier:
    mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: AVG(sales) OVER (ORDER BY sales_month ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING)
        -- Filter: WHERE kind_of_business = 'Book stores'
        -- Erwartete Spalten: sales_month, sales, ma_3_centered
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 5: Year-over-Year Vergleiche

        YoY-Vergleiche eliminieren Saisonalität, indem sie jeden Monat mit dem
        **gleichen Monat des Vorjahres** vergleichen.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 13.9: YoY-Wachstum

        Berechnen Sie das Year-over-Year Wachstum mit LAG(12).
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    yoy = mo.sql(
        f"""
        SELECT
            sales_month,
            sales,
            LAG(sales, 12) OVER (ORDER BY sales_month) AS sales_last_year,
            ROUND((sales * 1.0 / LAG(sales, 12) OVER (ORDER BY sales_month) - 1) * 100, 1)
                AS yoy_growth
        FROM retail_sales
        WHERE kind_of_business = 'Jewelry stores'
        ORDER BY sales_month
        """
    )
    return (yoy,)


@app.cell
def _(px, yoy):
    yoy_df = yoy.drop_nulls()
    fig_yoy = px.line(
        yoy_df,
        x="sales_month",
        y="yoy_growth",
        title="Year-over-Year Wachstum - Juweliere (%)",
        labels={"sales_month": "Monat", "yoy_growth": "YoY Wachstum (%)"}
    )
    fig_yoy.add_hline(y=0, line_dash="dash", line_color="gray")
    fig_yoy


@app.cell(hide_code=True)
def _(mo):
    quiz_lag = mo.ui.radio(
        options={
            "correct": "LAG(12) vergleicht mit dem gleichen Monat im Vorjahr — das eliminiert Saisonalität",
            "same": "LAG(12) und LAG(1) geben das gleiche Ergebnis, LAG(12) ist nur schneller",
            "avg": "LAG(12) berechnet einen 12-Monats-Durchschnitt, LAG(1) einen 1-Monats-Durchschnitt",
            "usage": "LAG kann nur mit Zeitreihen verwendet werden, nicht mit normalem GROUP BY",
        },
        label="**Quiz:** Oktober-Umsatz ist sehr hoch. Ist das ungewöhnlich, oder ist Oktober immer stark? Welche LAG-Verschiebung hilft?"
    )
    quiz_lag
    return (quiz_lag,)


@app.cell(hide_code=True)
def _(quiz_lag, mo):
    if quiz_lag.value == "correct":
        mo.output.replace(mo.md("Richtig! LAG(12) vergleicht Oktober 2020 mit Oktober 2019 — so sehen wir, ob der Wert *für diesen Monat* ungewöhnlich ist. LAG(1) würde nur mit September vergleichen, was bei saisonalen Daten irreführend wäre."))
    elif quiz_lag.value:
        mo.output.replace(mo.md("Nicht ganz. LAG(n) greift auf den Wert *n Zeilen vorher* zu — bei monatlichen Daten bedeutet LAG(12) den *gleichen Monat im Vorjahr*. So eliminieren wir saisonale Effekte."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 13.10: Indexierung zum Basisjahr

        Zeigen Sie alle Werte relativ zum ersten Wert (Januar 1992 = 0%).
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    indexed = mo.sql(
        f"""
        SELECT
            sales_month,
            sales,
            FIRST_VALUE(sales) OVER (ORDER BY sales_month) AS base_sales,
            ROUND((sales * 1.0 / FIRST_VALUE(sales) OVER (ORDER BY sales_month) - 1) * 100, 1)
                AS pct_from_base
        FROM retail_sales
        WHERE kind_of_business = 'Women''s clothing stores'
        ORDER BY sales_month
        """
    )
    return (indexed,)


@app.cell
def _(indexed, px):
    fig_indexed = px.line(
        indexed,
        x="sales_month",
        y="pct_from_base",
        title="Indexierte Verkaufszahlen - Damenbekleidung (Basis: Jan 1992)",
        labels={"sales_month": "Monat", "pct_from_base": "Änderung vs. Basis (%)"}
    )
    fig_indexed.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Basiswert")
    fig_indexed


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 6: Praktische Zeitreihenanalyse

        ### Aufgabe 13.11: Branchenvergleich - Herren vs. Damen Bekleidung
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    men_vs_women = mo.sql(
        f"""
        SELECT
            EXTRACT(YEAR FROM sales_month) AS year,
            SUM(CASE WHEN kind_of_business = 'Women''s clothing stores' THEN sales END) AS womens_sales,
            SUM(CASE WHEN kind_of_business = 'Men''s clothing stores' THEN sales END) AS mens_sales,
            ROUND(SUM(CASE WHEN kind_of_business = 'Women''s clothing stores' THEN sales END) * 1.0 /
                  SUM(CASE WHEN kind_of_business = 'Men''s clothing stores' THEN sales END), 2)
                AS womens_to_mens_ratio
        FROM retail_sales
        WHERE kind_of_business IN ('Women''s clothing stores', 'Men''s clothing stores')
        GROUP BY EXTRACT(YEAR FROM sales_month)
        ORDER BY year
        """
    )
    return (men_vs_women,)


@app.cell
def _(men_vs_women, px):
    fig_ratio = px.line(
        men_vs_women,
        x="year",
        y="womens_to_mens_ratio",
        title="Verhältnis Damen- zu Herrenbekleidung (jährlich)",
        labels={"year": "Jahr", "womens_to_mens_ratio": "Verhältnis"}
    )
    fig_ratio


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 13.12: Saisonale Muster erkennen

        Welche Monate sind am stärksten für verschiedene Branchen?
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    seasonal_pattern = mo.sql(
        f"""
        SELECT
            EXTRACT(MONTH FROM sales_month) AS month_num,
            kind_of_business,
            ROUND(AVG(sales), 0) AS avg_sales
        FROM retail_sales
        WHERE kind_of_business IN ('Jewelry stores', 'Sporting goods stores', 'Book stores')
        GROUP BY EXTRACT(MONTH FROM sales_month), kind_of_business
        ORDER BY kind_of_business, month_num
        """
    )
    return (seasonal_pattern,)


@app.cell
def _(px, seasonal_pattern):
    fig_seasonal = px.line(
        seasonal_pattern,
        x="month_num",
        y="avg_sales",
        color="kind_of_business",
        title="Saisonale Muster nach Branche (Durchschnitt 1992-2020)",
        labels={"month_num": "Monat", "avg_sales": "Ø Umsatz (Mio. USD)", "kind_of_business": "Branche"}
    )
    fig_seasonal


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 13.13: Selbstständig - COVID-Effekt

        Vergleichen Sie das YoY-Wachstum für 2020 mit den Vorjahren für "Book stores".
        Sehen Sie den COVID-Effekt?
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    # Ihre Lösung hier:
    mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: GROUP BY Jahr, dann LAG(..., 1) OVER (ORDER BY year) für Vorjahresvergleich
        -- Filter: WHERE kind_of_business = 'Book stores'
        -- Erwartete Spalten: year, annual_sales, prev_year, yoy_growth
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 13.14: Selbstständig - Anteil am Gesamtumsatz

        Berechnen Sie für jeden Monat den Anteil von "Jewelry stores" am Gesamtumsatz.

        *Hinweis: Verwenden Sie SUM() OVER (PARTITION BY sales_month)*
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    # Ihre Lösung hier:
    mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: SUM(sales) OVER (PARTITION BY sales_month) für den Gesamtumsatz pro Monat
        -- Dann: sales * 100.0 / SUM(sales) OVER (...) für den Anteil
        -- Erwartete Spalten: sales_month, kind_of_business, sales, total_sales, pct_of_total
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Freie Exploration

        Probieren Sie eigene Zeitreihenanalysen:

        - Vergleichen Sie verschiedene Branchen mit Indexierung
        - Finden Sie die volatilsten Branchen (höchste Standardabweichung der YoY-Wachstumsraten)
        - Analysieren Sie Trends vor und nach der Finanzkrise 2008
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    # Eigene Analyse hier:
    mo.sql(
        f"""
        SELECT
            kind_of_business,
            ROUND(AVG(yoy_growth), 1) AS avg_yoy_growth,
            ROUND(STDDEV(yoy_growth), 1) AS stddev_yoy_growth
        FROM (
            SELECT
                kind_of_business,
                sales_month,
                (sales * 1.0 / LAG(sales, 12) OVER (PARTITION BY kind_of_business ORDER BY sales_month) - 1) * 100
                    AS yoy_growth
            FROM retail_sales
            WHERE kind_of_business NOT LIKE '%total%'
        )
        WHERE yoy_growth IS NOT NULL
        GROUP BY kind_of_business
        ORDER BY stddev_yoy_growth DESC
        LIMIT 10
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Zusammenfassung

        | Konzept | Syntax | Anwendung |
        |---------|--------|-----------|
        | **LAG** | `LAG(col, n) OVER (ORDER BY ...)` | Vorheriger Wert |
        | **LEAD** | `LEAD(col, n) OVER (ORDER BY ...)` | Nächster Wert |
        | **Moving Avg** | `AVG() OVER (ROWS BETWEEN ...)` | Trend glätten |
        | **YoY** | `LAG(col, 12) OVER (...)` | Saisonalität eliminieren |
        | **Indexierung** | `FIRST_VALUE() OVER (...)` | Normalisieren |
        | **Ranking** | `RANK() OVER (ORDER BY ...)` | Top-N finden |

        **Nächste Session:** Textanalyse mit SQL String-Funktionen
        """
    )
    return


if __name__ == "__main__":
    app.run()
