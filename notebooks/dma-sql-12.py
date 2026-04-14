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

__generated_with = "0.13.0"
app = marimo.App(
    width="medium",
    app_title="DMA Session 12: Zeitreihenanalyse — Übungen",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 12: Zeitreihenanalyse — Übungen

        Theorie und geführte Beispiele → **12-zeitreihen-guide.py**

        **Aufgabentypen:**

        - 🟢 **Geführt**: Vollständige Lösung zum Nachvollziehen
        - 🟡 **Angepasst**: Teillösung zum Ergänzen (`???`)
        - 🔵 **Selbstständig**: Eigene Lösung schreiben
        - 🔴 **Debugging**: Fehler finden und beheben
        - ⭐ **Entdecken**: Offene Herausforderungen

        > **Hinweis:** 🟡-Aufgaben enthalten `???` als Platzhalter. Die Zelle zeigt einen SQL-Fehler, bis Sie die `???` durch die richtige Lösung ersetzen — das ist Absicht!
        """
    )
    return


@app.cell
def _(mo):
    import polars as pl
    import plotly.express as px

    try:
        csv_path = mo.notebook_location() / "public" / "us_retail_sales.csv"
        retail_sales = pl.read_csv(str(csv_path))
        retail_sales = retail_sales.with_columns([
            pl.col("sales_month").str.to_date("%Y-%m-%d"),
            pl.col("sales").cast(pl.Float64)
        ])
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
        mo.callout(mo.md("**Hinweis:** CSV konnte nicht geladen werden. Es werden Beispieldaten verwendet."), kind="warn")

    return mo, pl, px, retail_sales


# -----------------------------------------------------------------------
# Phase 1: Daten erkunden
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 1: Daten erkunden

        Unser Datensatz enthält monatliche Einzelhandelsumsätze verschiedener Branchen in den USA (1992-2020).

        Spalten: `sales_month` (Datum), `kind_of_business` (Branche), `sales` (Umsatz in Mio. USD)
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 12.1: Datenüberblick

        Wie viele Datensätze haben wir? Wie viele verschiedene Branchen? Welcher Zeitraum?
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    _df = mo.sql(
        f"""
        SELECT
            COUNT(*) AS anzahl_datensaetze,
            COUNT(DISTINCT kind_of_business) AS anzahl_branchen,
            MIN(sales_month) AS erster_monat,
            MAX(sales_month) AS letzter_monat
        FROM retail_sales
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    COUNT(*) AS anzahl_datensaetze,
    COUNT(DISTINCT kind_of_business) AS anzahl_branchen,
    MIN(sales_month) AS erster_monat,
    MAX(sales_month) AS letzter_monat
FROM retail_sales
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 12.2: Branchen auflisten

        Welche Branchen sind im Datensatz enthalten?
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    _df = mo.sql(
        f"""
        SELECT DISTINCT kind_of_business
        FROM retail_sales
        ORDER BY kind_of_business
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT DISTINCT kind_of_business
FROM retail_sales
ORDER BY kind_of_business
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 12.3: Gesamtumsatz einer Branche (Scaffolded)

        Berechnen Sie den Gesamtumsatz für Juweliergeschäfte. Ergänzen Sie `???`:
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    _df = mo.sql(
        f"""
        SELECT
            COUNT(*) AS anzahl_monate,
            ROUND(SUM(sales), 0) AS gesamt_umsatz,
            ROUND(AVG(sales), 0) AS durchschnitt_umsatz,
            ROUND(MIN(sales), 0) AS min_umsatz,
            ROUND(MAX(sales), 0) AS max_umsatz
        FROM retail_sales
        WHERE kind_of_business = ???
        -- Tipp: 'Jewelry stores'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    COUNT(*) AS anzahl_monate,
    ROUND(SUM(sales), 0) AS gesamt_umsatz,
    ROUND(AVG(sales), 0) AS durchschnitt_umsatz,
    ROUND(MIN(sales), 0) AS min_umsatz,
    ROUND(MAX(sales), 0) AS max_umsatz
FROM retail_sales
WHERE kind_of_business = 'Jewelry stores'
```
""")})
    return


# -----------------------------------------------------------------------
# Phase 2: Window Functions Syntax
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 2: Window Functions — Syntax

        Window Functions berechnen Werte über ein "Fenster" von Zeilen,
        **ohne** die Zeilen zu reduzieren (anders als GROUP BY).

        ```sql
        funktion() OVER (
            [PARTITION BY ...]
            [ORDER BY ...]
            [ROWS BETWEEN ... AND ...]
        )
        ```
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 12.4: Laufende Summe

        Berechnen Sie die kumulierte Summe der Umsätze für Buchläden.
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    _df = mo.sql(
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
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    sales_month,
    sales,
    SUM(sales) OVER (ORDER BY sales_month) AS cumulative_sales
FROM retail_sales
WHERE kind_of_business = 'Book stores'
ORDER BY sales_month
LIMIT 20
```
**Erklärung:** `SUM() OVER (ORDER BY ...)` berechnet die laufende Summe. Jede Zeile enthält die Summe aller bisherigen Werte.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 12.5: Ranking (Scaffolded)

        Welche Monate hatten die höchsten Umsätze bei Juwelieren? Ergänzen Sie `???`:
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    _df = mo.sql(
        f"""
        SELECT
            sales_month,
            sales,
            RANK() OVER (ORDER BY ???) AS rang
        FROM retail_sales
        WHERE kind_of_business = 'Jewelry stores'
        ORDER BY rang
        LIMIT 10
        -- Tipp: sales DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    sales_month,
    sales,
    RANK() OVER (ORDER BY sales DESC) AS rang
FROM retail_sales
WHERE kind_of_business = 'Jewelry stores'
ORDER BY rang
LIMIT 10
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 12.6: ROW_NUMBER vs. DENSE_RANK (Selbstständig)

        Vergleichen Sie `ROW_NUMBER()`, `RANK()` und `DENSE_RANK()` für Juweliergeschäfte,
        sortiert nach Umsatz absteigend. Was ist der Unterschied?

        *Hinweis: Alle drei Funktionen mit `OVER (ORDER BY sales DESC)`. Zeigen Sie die Top 15.*
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Erwartete Spalten: sales_month, sales, row_num, rang, dense_rang
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    sales_month,
    sales,
    ROW_NUMBER() OVER (ORDER BY sales DESC) AS row_num,
    RANK() OVER (ORDER BY sales DESC) AS rang,
    DENSE_RANK() OVER (ORDER BY sales DESC) AS dense_rang
FROM retail_sales
WHERE kind_of_business = 'Jewelry stores'
ORDER BY row_num
LIMIT 15
```
**Unterschied:** Bei gleichen Werten:
- `ROW_NUMBER`: fortlaufend (1, 2, 3, ...) — keine Duplikate
- `RANK`: gleicher Rang, dann Lücke (1, 1, 3, ...)
- `DENSE_RANK`: gleicher Rang, keine Lücke (1, 1, 2, ...)
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 12.7: Debugging — Fehlende Window-Spezifikation

        Die folgende Abfrage soll eine laufende Summe berechnen. Sie hat einen Fehler!
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    _df = mo.sql(
        f"""
        -- 🔴 Diese Abfrage hat einen Fehler — finden und beheben Sie ihn!
        SELECT
            sales_month,
            sales,
            SUM(sales) AS cumulative_sales
        FROM retail_sales
        WHERE kind_of_business = 'Book stores'
        ORDER BY sales_month
        LIMIT 20
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**Problem:** `SUM(sales)` ohne `OVER`-Klausel! Ohne OVER ist SUM eine Aggregatfunktion, die alle Zeilen zu einer zusammenfasst — es fehlt dann entweder GROUP BY oder die Window-Spezifikation.

**Lösung:**
```sql
SELECT
    sales_month,
    sales,
    SUM(sales) OVER (ORDER BY sales_month) AS cumulative_sales
FROM retail_sales
WHERE kind_of_business = 'Book stores'
ORDER BY sales_month
LIMIT 20
```
""")})
    return


# -----------------------------------------------------------------------
# Phase 3: LAG und LEAD
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 3: LAG und LEAD

        - `LAG(spalte, n)` greift auf den Wert **n Zeilen vorher** zu
        - `LEAD(spalte, n)` greift auf den Wert **n Zeilen danach** zu

        Damit können wir Veränderungen von Monat zu Monat berechnen.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 12.8: Monatliche Änderung — Juweliere

        Berechnen Sie die monatliche Umsatzänderung (absolut und prozentual) für Juweliergeschäfte.
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    _df = mo.sql(
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
        LIMIT 20
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
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
LIMIT 20
```
**Beobachtung:** Die erste Zeile hat NULL bei prev_month_sales — es gibt keinen Vorgänger!
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 12.9: Monatliche Änderung — Sportgeschäfte (Scaffolded)

        Berechnen Sie die monatliche prozentuale Änderung für Sportgeschäfte. Ergänzen Sie `???`:
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    _df = mo.sql(
        f"""
        SELECT
            sales_month,
            sales,
            LAG(sales, 1) OVER (ORDER BY ???) AS prev_month,
            ROUND((sales * 1.0 / LAG(sales, 1) OVER (ORDER BY ???) - 1) * 100, 1)
                AS pct_change
        FROM retail_sales
        WHERE kind_of_business = ???
        ORDER BY sales_month
        LIMIT 20
        -- Tipp: ORDER BY sales_month, WHERE 'Sporting goods stores'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    sales_month,
    sales,
    LAG(sales, 1) OVER (ORDER BY sales_month) AS prev_month,
    ROUND((sales * 1.0 / LAG(sales, 1) OVER (ORDER BY sales_month) - 1) * 100, 1)
        AS pct_change
FROM retail_sales
WHERE kind_of_business = 'Sporting goods stores'
ORDER BY sales_month
LIMIT 20
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 12.10: LEAD — Nächster Monat (Selbstständig)

        Zeigen Sie für Buchläden den Umsatz des **nächsten** Monats neben dem aktuellen.
        Berechnen Sie auch die erwartete Änderung.

        *Hinweis: `LEAD(sales, 1) OVER (ORDER BY sales_month)`*
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Erwartete Spalten: sales_month, sales, next_month_sales, expected_change
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    sales_month,
    sales,
    LEAD(sales, 1) OVER (ORDER BY sales_month) AS next_month_sales,
    LEAD(sales, 1) OVER (ORDER BY sales_month) - sales AS expected_change
FROM retail_sales
WHERE kind_of_business = 'Book stores'
ORDER BY sales_month
LIMIT 20
```
**Beobachtung:** Die letzte Zeile hat NULL bei next_month_sales — es gibt keinen Nachfolger!
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 12.11: Debugging — NULL in der ersten Zeile

        Die folgende Abfrage berechnet die prozentuale Änderung, aber die erste Zeile erzeugt einen NULL-Wert.
        Wie können wir das bereinigen?
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    _df = mo.sql(
        f"""
        -- 🔴 Diese Abfrage hat einen Fehler — finden und beheben Sie ihn!
        SELECT
            sales_month,
            sales,
            LAG(sales, 1) OVER (ORDER BY sales_month) AS prev_month,
            ROUND((sales * 1.0 / LAG(sales, 1) OVER (ORDER BY sales_month) - 1) * 100, 1)
                AS pct_change
        FROM retail_sales
        WHERE kind_of_business = 'Jewelry stores'
        ORDER BY sales_month
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**Problem:** Die erste Zeile hat keinen Vorgänger, daher ist `LAG()` NULL und die Division ergibt NULL. Das ist zwar kein Fehler im SQL, aber oft unerwünscht.

**Lösung 1: NULL-Zeilen ausfiltern (bevorzugt)**
```sql
WITH mit_lag AS (
    SELECT
        sales_month,
        sales,
        LAG(sales, 1) OVER (ORDER BY sales_month) AS prev_month
    FROM retail_sales
    WHERE kind_of_business = 'Jewelry stores'
)
SELECT
    sales_month,
    sales,
    prev_month,
    ROUND((sales * 1.0 / prev_month - 1) * 100, 1) AS pct_change
FROM mit_lag
WHERE prev_month IS NOT NULL
ORDER BY sales_month
```

**Lösung 2: COALESCE als Fallback**
```sql
SELECT
    sales_month,
    sales,
    COALESCE(LAG(sales, 1) OVER (ORDER BY sales_month), sales) AS prev_month,
    ROUND((sales * 1.0 / COALESCE(LAG(sales, 1) OVER (ORDER BY sales_month), sales) - 1) * 100, 1)
        AS pct_change
FROM retail_sales
WHERE kind_of_business = 'Jewelry stores'
ORDER BY sales_month
```
""")})
    return


# -----------------------------------------------------------------------
# Phase 4: Moving Averages
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 4: Moving Averages

        Gleitende Durchschnitte glätten kurzfristige Schwankungen und machen den **Trend** sichtbar.

        ```sql
        AVG(sales) OVER (
            ORDER BY sales_month
            ROWS BETWEEN n PRECEDING AND CURRENT ROW  -- trailing
        )
        ```
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 12.12: 12-Monats Moving Average (trailing)

        Berechnen Sie einen 12-Monats gleitenden Durchschnitt für den Gesamtumsatz.
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
    fig_ma = px.line(
        ma_12,
        x="sales_month",
        y=["sales", "ma_12"],
        title="Retail Sales mit 12-Monats Moving Average",
        labels={"sales_month": "Monat", "value": "Umsatz (Mio. USD)", "variable": "Serie"}
    )
    fig_ma


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
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
```
**Erklärung:** `ROWS BETWEEN 11 PRECEDING AND CURRENT ROW` = 12 Monate (11 vorherige + aktueller). Der MA glättet die Saisonalität!
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 12.13: 3-Monats zentrierter Moving Average (Scaffolded)

        Berechnen Sie einen **zentrierten** 3-Monats Moving Average für Buchläden. Ergänzen Sie `???`:
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    _df = mo.sql(
        f"""
        SELECT
            sales_month,
            sales,
            ROUND(AVG(sales) OVER (
                ORDER BY sales_month
                ROWS BETWEEN ??? PRECEDING AND ??? FOLLOWING
            ), 0) AS ma_3_centered
        FROM retail_sales
        WHERE kind_of_business = 'Book stores'
        ORDER BY sales_month
        LIMIT 20
        -- Tipp: 1 PRECEDING und 1 FOLLOWING
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    sales_month,
    sales,
    ROUND(AVG(sales) OVER (
        ORDER BY sales_month
        ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
    ), 0) AS ma_3_centered
FROM retail_sales
WHERE kind_of_business = 'Book stores'
ORDER BY sales_month
LIMIT 20
```
**Zentriert** bedeutet: gleich viele Monate vor und nach dem aktuellen Datum.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 12.14: 6-Monats Moving Average (Selbstständig)

        Berechnen Sie einen 6-Monats trailing Moving Average für Sportgeschäfte.

        *Hinweis: `ROWS BETWEEN 5 PRECEDING AND CURRENT ROW` für 6 Monate*
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Erwartete Spalten: sales_month, sales, ma_6
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    sales_month,
    sales,
    ROUND(AVG(sales) OVER (
        ORDER BY sales_month
        ROWS BETWEEN 5 PRECEDING AND CURRENT ROW
    ), 0) AS ma_6
FROM retail_sales
WHERE kind_of_business = 'Sporting goods stores'
ORDER BY sales_month
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 12.15: Debugging — Falscher Window Frame

        Die folgende Abfrage soll einen 3-Monats trailing Moving Average berechnen. Sie hat einen Fehler!
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    _df = mo.sql(
        f"""
        -- 🔴 Diese Abfrage hat einen Fehler — finden und beheben Sie ihn!
        SELECT
            sales_month,
            sales,
            ROUND(AVG(sales) OVER (
                ORDER BY sales_month
                ROWS 2 PRECEDING
            ), 0) AS ma_3
        FROM retail_sales
        WHERE kind_of_business = 'Book stores'
        ORDER BY sales_month
        LIMIT 20
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**Problem:** `ROWS 2 PRECEDING` ist keine gültige Syntax! Es fehlt das Schlüsselwort `BETWEEN`.

**Lösung:**
```sql
SELECT
    sales_month,
    sales,
    ROUND(AVG(sales) OVER (
        ORDER BY sales_month
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 0) AS ma_3
FROM retail_sales
WHERE kind_of_business = 'Book stores'
ORDER BY sales_month
LIMIT 20
```
**Merke:** Die korrekte Syntax ist immer `ROWS BETWEEN ... AND ...`.
""")})
    return


# -----------------------------------------------------------------------
# Phase 5: Year-over-Year Vergleiche
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 5: Year-over-Year Vergleiche

        YoY-Vergleiche eliminieren Saisonalität, indem sie jeden Monat mit dem
        **gleichen Monat des Vorjahres** vergleichen. Dafür nutzen wir `LAG(sales, 12)`.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 12.16: YoY-Wachstum — Juweliere

        Berechnen Sie das Year-over-Year Wachstum mit LAG(12) für Juweliergeschäfte.
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
        title="Year-over-Year Wachstum — Juweliere (%)",
        labels={"sales_month": "Monat", "yoy_growth": "YoY Wachstum (%)"}
    )
    fig_yoy.add_hline(y=0, line_dash="dash", line_color="gray")
    fig_yoy


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    sales_month,
    sales,
    LAG(sales, 12) OVER (ORDER BY sales_month) AS sales_last_year,
    ROUND((sales * 1.0 / LAG(sales, 12) OVER (ORDER BY sales_month) - 1) * 100, 1)
        AS yoy_growth
FROM retail_sales
WHERE kind_of_business = 'Jewelry stores'
ORDER BY sales_month
```
**Warum LAG(12)?** Bei monatlichen Daten ist LAG(12) = gleicher Monat im Vorjahr. So eliminieren wir saisonale Effekte.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 12.17: YoY-Wachstum jährlich (Scaffolded)

        Berechnen Sie das jährliche YoY-Wachstum: Erst Jahresdaten aggregieren, dann vergleichen. Ergänzen Sie `???`:
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    _df = mo.sql(
        f"""
        WITH yearly AS (
            SELECT
                EXTRACT(YEAR FROM sales_month) AS year,
                ROUND(SUM(sales), 0) AS annual_sales
            FROM retail_sales
            WHERE kind_of_business = 'Jewelry stores'
            GROUP BY ???
        )
        SELECT
            year,
            annual_sales,
            LAG(annual_sales, 1) OVER (ORDER BY ???) AS prev_year,
            ROUND((annual_sales * 1.0 / LAG(annual_sales, 1) OVER (ORDER BY ???) - 1) * 100, 1)
                AS yoy_growth
        FROM yearly
        ORDER BY year
        -- Tipp: GROUP BY EXTRACT(YEAR FROM sales_month), ORDER BY year
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
WITH yearly AS (
    SELECT
        EXTRACT(YEAR FROM sales_month) AS year,
        ROUND(SUM(sales), 0) AS annual_sales
    FROM retail_sales
    WHERE kind_of_business = 'Jewelry stores'
    GROUP BY EXTRACT(YEAR FROM sales_month)
)
SELECT
    year,
    annual_sales,
    LAG(annual_sales, 1) OVER (ORDER BY year) AS prev_year,
    ROUND((annual_sales * 1.0 / LAG(annual_sales, 1) OVER (ORDER BY year) - 1) * 100, 1)
        AS yoy_growth
FROM yearly
ORDER BY year
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 12.18: COVID-Effekt — Buchläden 2020 (Selbstständig)

        Berechnen Sie das monatliche YoY-Wachstum für Buchläden im Jahr 2020.
        Können Sie den COVID-Effekt erkennen?

        *Hinweis: Erst YoY mit LAG(12) berechnen, dann auf 2020 filtern*
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Erwartete Spalten: sales_month, sales, sales_last_year, yoy_growth
        -- Filter: nur 2020
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
WITH mit_yoy AS (
    SELECT
        sales_month,
        sales,
        LAG(sales, 12) OVER (ORDER BY sales_month) AS sales_last_year,
        ROUND((sales * 1.0 / LAG(sales, 12) OVER (ORDER BY sales_month) - 1) * 100, 1)
            AS yoy_growth
    FROM retail_sales
    WHERE kind_of_business = 'Book stores'
)
SELECT *
FROM mit_yoy
WHERE EXTRACT(YEAR FROM sales_month) = 2020
ORDER BY sales_month
```
**Beobachtung:** Ab März/April 2020 starker Einbruch durch Lockdowns!
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 12.19: Anteil am Gesamtumsatz pro Monat (Selbstständig)

        Berechnen Sie für jeden Monat den Anteil von "Jewelry stores" am Gesamtumsatz aller Branchen.

        *Hinweis: `SUM(sales) OVER (PARTITION BY sales_month)` für den Gesamtumsatz pro Monat*
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Erwartete Spalten: sales_month, sales, total_sales, pct_of_total
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    sales_month,
    kind_of_business,
    sales,
    SUM(sales) OVER (PARTITION BY sales_month) AS total_sales,
    ROUND(sales * 100.0 / SUM(sales) OVER (PARTITION BY sales_month), 2) AS pct_of_total
FROM retail_sales
WHERE kind_of_business = 'Jewelry stores'
ORDER BY sales_month
```
**PARTITION BY sales_month** berechnet den Gesamtumsatz separat für jeden Monat.
""")})
    return


# -----------------------------------------------------------------------
# Phase 6: Praktische Analyse
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 6: Praktische Analyse

        Jetzt kombinieren wir die gelernten Techniken für echte Geschäftsanalysen.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 12.20: Herren- vs. Damenbekleidung — Verhältnis

        Wie hat sich das Umsatzverhältnis zwischen Damen- und Herrenbekleidung über die Jahre entwickelt?
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
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
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
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 12.21: Saisonale Muster für 3 Branchen (Scaffolded)

        Welche Monate sind für verschiedene Branchen am stärksten? Ergänzen Sie `???`:
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    _df = mo.sql(
        f"""
        SELECT
            EXTRACT(??? FROM sales_month) AS month_num,
            kind_of_business,
            ROUND(AVG(sales), 0) AS avg_sales
        FROM retail_sales
        WHERE kind_of_business IN ('Jewelry stores', 'Sporting goods stores', ???)
        GROUP BY EXTRACT(??? FROM sales_month), kind_of_business
        ORDER BY kind_of_business, month_num
        -- Tipp: EXTRACT(MONTH FROM ...), dritte Branche z.B. 'Book stores'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    EXTRACT(MONTH FROM sales_month) AS month_num,
    kind_of_business,
    ROUND(AVG(sales), 0) AS avg_sales
FROM retail_sales
WHERE kind_of_business IN ('Jewelry stores', 'Sporting goods stores', 'Book stores')
GROUP BY EXTRACT(MONTH FROM sales_month), kind_of_business
ORDER BY kind_of_business, month_num
```
**Beobachtung:** Juweliere haben ihren Peak im Dezember (Weihnachten), Sportgeschäfte eher im Frühjahr/Sommer.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 12.22: Volatilität — Welche Branche schwankt am meisten? (Selbstständig)

        Berechnen Sie die Standardabweichung der YoY-Wachstumsraten pro Branche.
        Die Branche mit der höchsten STDDEV ist die volatilste.

        *Hinweis: Erst YoY berechnen (LAG(12) mit PARTITION BY kind_of_business), dann STDDEV pro Branche*
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Erwartete Spalten: kind_of_business, avg_yoy, stddev_yoy
        -- Sortiert nach stddev_yoy DESC
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    kind_of_business,
    ROUND(AVG(yoy_growth), 1) AS avg_yoy,
    ROUND(STDDEV(yoy_growth), 1) AS stddev_yoy
FROM (
    SELECT
        kind_of_business,
        sales_month,
        (sales * 1.0 / LAG(sales, 12) OVER (
            PARTITION BY kind_of_business ORDER BY sales_month
        ) - 1) * 100 AS yoy_growth
    FROM retail_sales
    WHERE kind_of_business NOT LIKE '%total%'
)
WHERE yoy_growth IS NOT NULL
GROUP BY kind_of_business
ORDER BY stddev_yoy DESC
LIMIT 10
```
""")})
    return


# -----------------------------------------------------------------------
# Phase 7 (Bonus): Indexierung
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 7 (Bonus): Indexierung

        Indexierung normalisiert alle Werte relativ zu einem Basiswert (z.B. erster Monat = 100).
        So können wir Branchen mit **unterschiedlichen Umsatzniveaus** direkt vergleichen.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 12.23: FIRST_VALUE — Indexierung zum Basisjahr

        Zeigen Sie alle Werte relativ zum ersten Wert (Januar 1992 = 100).
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    _df = mo.sql(
        f"""
        SELECT
            sales_month,
            sales,
            FIRST_VALUE(sales) OVER (ORDER BY sales_month) AS base_sales,
            ROUND(sales * 100.0 / FIRST_VALUE(sales) OVER (ORDER BY sales_month), 1)
                AS index_value
        FROM retail_sales
        WHERE kind_of_business = 'Women''s clothing stores'
        ORDER BY sales_month
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    sales_month,
    sales,
    FIRST_VALUE(sales) OVER (ORDER BY sales_month) AS base_sales,
    ROUND(sales * 100.0 / FIRST_VALUE(sales) OVER (ORDER BY sales_month), 1)
        AS index_value
FROM retail_sales
WHERE kind_of_business = 'Women''s clothing stores'
ORDER BY sales_month
```
**Interpretation:** Ein Index von 120 bedeutet: 20% mehr als der Basiswert.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 12.24: Zwei Branchen indexiert vergleichen (Selbstständig)

        Vergleichen Sie Juweliere und Buchläden mit Indexierung (Basis = erster Monat jeder Branche = 100).

        *Hinweis: `FIRST_VALUE(sales) OVER (PARTITION BY kind_of_business ORDER BY sales_month)`*
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Erwartete Spalten: sales_month, kind_of_business, sales, index_value
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    sales_month,
    kind_of_business,
    sales,
    ROUND(sales * 100.0 / FIRST_VALUE(sales) OVER (
        PARTITION BY kind_of_business ORDER BY sales_month
    ), 1) AS index_value
FROM retail_sales
WHERE kind_of_business IN ('Jewelry stores', 'Book stores')
ORDER BY sales_month, kind_of_business
```
**Durch PARTITION BY** bekommt jede Branche ihren eigenen Basiswert (= erster Monat jeder Branche).
""")})
    return


# -----------------------------------------------------------------------
# Exploration
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Exploration

        Offene Herausforderungen für Fortgeschrittene.

        **Tipp:** Vergleichen Sie Ihre Analysen mit Ihrem Nachbarn — bei Zeitreihen gibt es oft mehrere spannende Perspektiven!
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐ Exploration 1: Volatilste Branchen

        Finden Sie die 5 volatilsten Branchen (höchste STDDEV der monatlichen YoY-Wachstumsraten).
        Visualisieren Sie deren YoY-Verlauf.

        *Hinweis: Wie Aufgabe 12.22, aber mit Visualisierung der Top-5*
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    kind_of_business,
    ROUND(AVG(yoy_growth), 1) AS avg_yoy,
    ROUND(STDDEV(yoy_growth), 1) AS stddev_yoy
FROM (
    SELECT
        kind_of_business,
        sales_month,
        (sales * 1.0 / LAG(sales, 12) OVER (
            PARTITION BY kind_of_business ORDER BY sales_month
        ) - 1) * 100 AS yoy_growth
    FROM retail_sales
    WHERE kind_of_business NOT LIKE '%total%'
      AND kind_of_business NOT LIKE '%and%'
)
WHERE yoy_growth IS NOT NULL
GROUP BY kind_of_business
ORDER BY stddev_yoy DESC
LIMIT 5
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐⭐ Exploration 2: Finanzkrise 2008 — Vorher vs. Nachher

        Vergleichen Sie den durchschnittlichen Umsatz **vor** (2005-2007) und **nach** (2009-2011) der Finanzkrise
        für verschiedene Branchen. Welche Branchen waren am stärksten betroffen?

        *Hinweis: CASE WHEN + EXTRACT(YEAR FROM ...) für die Perioden*
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    kind_of_business,
    ROUND(AVG(CASE WHEN EXTRACT(YEAR FROM sales_month) BETWEEN 2005 AND 2007
              THEN sales END), 0) AS avg_pre_crisis,
    ROUND(AVG(CASE WHEN EXTRACT(YEAR FROM sales_month) BETWEEN 2009 AND 2011
              THEN sales END), 0) AS avg_post_crisis,
    ROUND(
        (AVG(CASE WHEN EXTRACT(YEAR FROM sales_month) BETWEEN 2009 AND 2011 THEN sales END)
         - AVG(CASE WHEN EXTRACT(YEAR FROM sales_month) BETWEEN 2005 AND 2007 THEN sales END))
        * 100.0
        / AVG(CASE WHEN EXTRACT(YEAR FROM sales_month) BETWEEN 2005 AND 2007 THEN sales END),
    1) AS change_pct
FROM retail_sales
WHERE kind_of_business NOT LIKE '%total%'
  AND EXTRACT(YEAR FROM sales_month) BETWEEN 2005 AND 2011
GROUP BY kind_of_business
HAVING AVG(CASE WHEN EXTRACT(YEAR FROM sales_month) BETWEEN 2005 AND 2007 THEN sales END) IS NOT NULL
ORDER BY change_pct ASC
LIMIT 10
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐⭐⭐ Exploration 3: Mini-Dashboard — Eine Branche komplett analysieren

        Erstellen Sie eine Gesamtanalyse für eine Branche Ihrer Wahl:
        1. **Trend:** 12-Monats Moving Average
        2. **Saisonalität:** Durchschnittsumsatz pro Monat
        3. **YoY-Wachstum:** Monatlich mit LAG(12)
        4. **Volatilität:** STDDEV des YoY-Wachstums

        *Hinweis: Nutzen Sie CTEs, um die verschiedenen Perspektiven zu kombinieren*
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
**Beispiel für "Jewelry stores":**

**1. Trend (12-Monats MA):**
```sql
SELECT sales_month, sales,
       ROUND(AVG(sales) OVER (ORDER BY sales_month
           ROWS BETWEEN 11 PRECEDING AND CURRENT ROW), 0) AS ma_12
FROM retail_sales
WHERE kind_of_business = 'Jewelry stores'
ORDER BY sales_month
```

**2. Saisonalität:**
```sql
SELECT EXTRACT(MONTH FROM sales_month) AS monat,
       ROUND(AVG(sales), 0) AS avg_sales
FROM retail_sales
WHERE kind_of_business = 'Jewelry stores'
GROUP BY EXTRACT(MONTH FROM sales_month)
ORDER BY monat
```

**3. YoY-Wachstum:**
```sql
SELECT sales_month, sales,
       ROUND((sales * 1.0 / LAG(sales, 12) OVER (ORDER BY sales_month) - 1) * 100, 1) AS yoy
FROM retail_sales
WHERE kind_of_business = 'Jewelry stores'
ORDER BY sales_month
```

**4. Volatilität:**
```sql
SELECT ROUND(STDDEV(yoy_growth), 1) AS volatilitaet
FROM (
    SELECT (sales * 1.0 / LAG(sales, 12) OVER (ORDER BY sales_month) - 1) * 100 AS yoy_growth
    FROM retail_sales
    WHERE kind_of_business = 'Jewelry stores'
) WHERE yoy_growth IS NOT NULL
```
""")})
    return


# -----------------------------------------------------------------------
# Zusammenfassung
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Zusammenfassung

        | Konzept | Aufgaben | Wann nutzen? |
        |---------|----------|--------------|
        | **Daten erkunden** | 12.1 – 12.3 | Immer zuerst: COUNT, DISTINCT, MIN/MAX |
        | **Window Functions** | 12.4 – 12.7 | SUM/RANK/ROW_NUMBER ohne GROUP BY |
        | **LAG / LEAD** | 12.8 – 12.11 | Monatliche Veränderungen berechnen |
        | **Moving Averages** | 12.12 – 12.15 | Trend glätten mit ROWS BETWEEN |
        | **Year-over-Year** | 12.16 – 12.19 | Saisonalität eliminieren mit LAG(12) |
        | **Praktische Analyse** | 12.20 – 12.22 | Branchenvergleiche, Saisonalität, Volatilität |
        | **Indexierung (Bonus)** | 12.23 – 12.24 | Branchen normalisiert vergleichen |

        **Nächste Session:** Textanalyse mit SQL-String-Funktionen
        """
    )
    return


if __name__ == "__main__":
    app.run()
