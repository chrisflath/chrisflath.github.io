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
    app_title="DMA Session 12: Zeitreihenanalyse — Guide",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _():
    import polars as pl
    return (pl,)


@app.cell(hide_code=True)
def _():
    import plotly.express as px
    return (px,)


@app.cell(hide_code=True)
def _(mo, pl):
    try:
        csv_path = mo.notebook_location() / "public" / "us_retail_sales.csv"
        retail_sales = pl.read_csv(str(csv_path))
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
    return daten_quelle, retail_sales


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 12: Zeitreihenanalyse — Guide

        **Kursfahrplan:** I: SQL-Grundlagen (S1–4) · II: Datenmodellierung (S5–7) · III: Fortgeschrittenes SQL (S8–9) · **▸ IV: Datenanalyse (S10–13)**

        ### Lernziele

        Nach dieser Session können Sie:

        - **Zeitreihendaten** analysieren und Trend, Saisonalität & Residuen erkennen
        - **Window Functions** (LAG, LEAD, RANK, ROW_NUMBER) anwenden
        - **Moving Averages** mit SQL berechnen (trailing & zentriert)
        - **Year-over-Year Vergleiche** durchführen und Saisonalität eliminieren

        **Datensatz:** U.S. Census Bureau — Monthly Retail Trade Survey (1992–2020)

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(daten_quelle, mo):
    mo.md(
        f"""
        **Datenquelle:** {daten_quelle}

        ## Phase 1: Daten erkunden

        ### Zeitreihen — Drei Komponenten

        Jede Zeitreihe lässt sich konzeptuell in drei Bestandteile zerlegen:

        | Komponente | Beschreibung | Beispiel |
        |------------|-------------|----------|
        | **Trend** | Langfristige Richtung | Wachsender Online-Handel |
        | **Saisonalität** | Wiederkehrendes Muster | Weihnachtsgeschäft im Dezember |
        | **Residuen** | Zufällige Schwankungen | Einmaleffekte, Rauschen |

        Unser Datensatz enthält monatliche Einzelhandelsumsätze für verschiedene Branchen in den USA.
        Schauen wir uns zuerst an, was wir haben.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 12.1: Datenüberblick
    """)
    return


@app.cell(hide_code=True)
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
    mo.md(
        r"""
        **Beobachtung:** Wir haben knapp 30 Jahre monatlicher Daten für viele verschiedene Branchen — ein reichhaltiger Datensatz für Zeitreihenanalysen.

        ---

        ### Geführtes Beispiel 12.2: Gesamtumsatz über die Zeit
        """
    )
    return


@app.cell(hide_code=True)
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


@app.cell(hide_code=True)
def _(px, total_sales):
    fig_total = px.line(
        total_sales,
        x="sales_month",
        y="sales",
        title="US Retail Sales — Gesamt (1992–2020)",
        labels={"sales_month": "Monat", "sales": "Umsatz (Mio. USD)"},
    )
    fig_total.update_layout(template="plotly_white")
    fig_total
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Deutlicher **Aufwärtstrend** mit starker **Saisonalität** — jedes Jahr ein Dezember-Peak (Weihnachtsgeschäft). Außerdem sichtbar: Einbruch 2008/09 (Finanzkrise) und 2020 (COVID-19).

        ---

        ### Vorhersage 1: Dezember-Spike
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    pred_dezember = mo.ui.radio(
        options={
            "Etwa 10–15 % über dem Jahresdurchschnitt": "10_15",
            "Etwa 20–30 % über dem Jahresdurchschnitt": "20_30",
            "Über 50 % — Weihnachten dominiert den Einzelhandel": "50_plus",
            "Kaum Unterschied — der Aufwärtstrend täuscht": "gleich",
        },
        label="**Vorhersage:** Betrachten Sie die Zeitreihe oben. Um wie viel Prozent schätzen Sie den typischen Dezember-Umsatz höher als den Jahresdurchschnitt?",
    )
    return (pred_dezember,)


@app.cell(hide_code=True)
def _(mo, pred_dezember):
    if pred_dezember.value == "20_30":
        _result = (
            mo.md(
                "✅ **Richtig!** Der Dezember liegt typischerweise ca. **20–25 %** über dem Jahresdurchschnitt. "
                "Das Weihnachtsgeschäft ist ein starker saisonaler Treiber, aber der Effekt variiert "
                "je nach Branche — Juweliere haben einen noch extremeren Dezember-Peak."
            )
        )
    elif pred_dezember.value == "10_15":
        _result = (
            mo.md(
                "❌ Etwas zu niedrig geschätzt. Der Dezember liegt typischerweise **20–25 %** über dem "
                "Jahresdurchschnitt. 10–15 % wäre für manche Branchen realistisch, aber der "
                "Gesamteinzelhandel hat einen stärkeren Weihnachtseffekt."
            )
        )
    elif pred_dezember.value == "50_plus":
        _result = (
            mo.md(
                "❌ Etwas zu hoch geschätzt. Für den **Gesamteinzelhandel** liegt der Dezember ca. "
                "20–25 % über dem Jahresdurchschnitt. Einzelne Branchen wie Juweliere können 50 %+ "
                "erreichen, aber aggregiert gleichen sich die Unterschiede etwas aus."
            )
        )
    elif pred_dezember.value == "gleich":
        _result = (
            mo.md(
                "❌ Der Dezember-Spike ist real und kein Artefakt des Trends! "
                "Selbst wenn man den Trend herausrechnet, liegt der Dezember typischerweise "
                "**20–25 %** über dem Jahresdurchschnitt. Das Weihnachtsgeschäft ist ein "
                "dominanter saisonaler Effekt."
            )
        )
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([pred_dezember, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 1.x**

        ---

        ## Phase 2: Window Functions — Syntax

        Window Functions berechnen Werte über ein „Fenster" von Zeilen, **ohne die Zeilenzahl zu reduzieren** (anders als GROUP BY).

        ```sql
        funktion() OVER (
            [PARTITION BY spalte]    -- optional: Gruppen bilden
            ORDER BY spalte          -- Reihenfolge im Fenster
            [ROWS BETWEEN ...]       -- optional: Fensterrahmen
        )
        ```

        | Funktion | Typ | Rückgabe |
        |----------|-----|----------|
        | `SUM() OVER(...)` | Aggregat | Laufende/kumulative Summe |
        | `AVG() OVER(...)` | Aggregat | Gleitender Durchschnitt |
        | `ROW_NUMBER()` | Ranking | Fortlaufende Nummer (keine Gleichstände) |
        | `RANK()` | Ranking | Rang mit Lücken bei Gleichstand |
        | `DENSE_RANK()` | Ranking | Rang ohne Lücken bei Gleichstand |
        | `LAG(col, n)` | Versatz | Wert n Zeilen **zurück** |
        | `LEAD(col, n)` | Versatz | Wert n Zeilen **voraus** |
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 12.3: Laufende Summe (Cumulative Sum)

    `SUM() OVER (ORDER BY ...)` berechnet eine kumulierte Summe — jede Zeile enthält die Summe aller bisherigen Werte:
    """)
    return


@app.cell(hide_code=True)
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
    mo.md(
        r"""
        **Beobachtung:** Die Spalte `cumulative_sales` wächst monoton — jeder Wert ist die Summe aller bisherigen Monatsumsätze. Beachten Sie: Die Originalzeilen bleiben erhalten (anders als bei GROUP BY).

        ---

        ### Geführtes Beispiel 12.4: Ranking — Top-Monate bei Juwelieren

        `RANK() OVER (ORDER BY sales DESC)` vergibt Ränge basierend auf den Umsatzwerten:
        """
    )
    return


@app.cell(hide_code=True)
def _(mo, retail_sales):
    _df = mo.sql(
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
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Die Top-10-Monate für Juweliere sind fast ausschließlich Dezember-Monate — ein eindrucksvoller Beweis für die Saisonalität.

        ---

        ### Vorhersage 2: ROW_NUMBER vs. RANK vs. DENSE_RANK
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    pred_ranking = mo.ui.radio(
        options={
            "ROW_NUMBER: 1, 2, 3 — RANK: 1, 2, 2 — DENSE_RANK: 1, 2, 2": "row_number",
            "ROW_NUMBER: 1, 2, 3 — RANK: 1, 2, 2, 4 — DENSE_RANK: 1, 2, 2, 3": "correct",
            "Alle drei geben 1, 2, 2, 3 zurück": "alle_gleich",
            "RANK gibt einen Fehler bei Gleichständen": "rank_error",
        },
        label="**Vorhersage:** Vier Zeilen, Werte: 100, 90, 90, 80. Welche Ränge vergeben ROW_NUMBER, RANK und DENSE_RANK?",
    )
    return (pred_ranking,)


@app.cell(hide_code=True)
def _(mo, pred_ranking):
    if pred_ranking.value == "correct":
        _result = (
            mo.md(
                "✅ **Richtig!** Bei Gleichstand (90, 90):\n\n"
                "- **ROW_NUMBER** vergibt immer eindeutige Nummern: 1, 2, 3, 4 (Reihenfolge bei Gleichstand ist zufällig)\n"
                "- **RANK** gibt beiden 90ern Rang 2, springt dann zu 4 (Rang 3 wird übersprungen)\n"
                "- **DENSE_RANK** gibt beiden 90ern Rang 2, macht dann mit 3 weiter (keine Lücke)"
            )
        )
    elif pred_ranking.value == "row_number":
        _result = (
            mo.md(
                "❌ Fast richtig, aber unvollständig! RANK gibt bei Gleichstand (90, 90) beiden Rang 2 "
                "und springt dann zu **4** (nicht 3). DENSE_RANK hingegen macht lückenlos weiter: "
                "2, 2, **3**. Und ROW_NUMBER hat immer 4 verschiedene Werte: 1, 2, 3, 4."
            )
        )
    elif pred_ranking.value == "alle_gleich":
        _result = (
            mo.md(
                "❌ Die drei Funktionen unterscheiden sich genau bei Gleichständen:\n\n"
                "- ROW_NUMBER → 1, 2, 3, 4 (immer eindeutig)\n"
                "- RANK → 1, 2, 2, **4** (Lücke nach Gleichstand)\n"
                "- DENSE_RANK → 1, 2, 2, **3** (keine Lücke)"
            )
        )
    elif pred_ranking.value == "rank_error":
        _result = (
            mo.md(
                "❌ RANK gibt keinen Fehler bei Gleichständen — das ist sogar sein Kernfeature! "
                "RANK vergibt beiden 90ern Rang 2 und springt zu 4. "
                "DENSE_RANK macht es ähnlich, aber ohne Lücke (2, 2, 3)."
            )
        )
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([pred_ranking, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 2.x**

        ---

        ## Phase 3: LAG und LEAD

        **LAG** greift auf den Wert einer **vorherigen** Zeile zu, **LEAD** auf den einer **nachfolgenden**.
        So können wir Veränderungen von Monat zu Monat direkt berechnen.

        ```sql
        LAG(spalte, n)  OVER (ORDER BY ...)  -- n Zeilen zurück (Standard: 1)
        LEAD(spalte, n) OVER (ORDER BY ...)  -- n Zeilen voraus (Standard: 1)
        ```
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 12.5: Monatliche Änderung mit LAG

    Berechnen Sie die absolute und prozentuale Änderung gegenüber dem Vormonat:
    """)
    return


@app.cell(hide_code=True)
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** LAG(sales, 1) holt den Umsatz des Vormonats. Die erste Zeile hat `NULL`, weil es keinen Vorgänger gibt. Die prozentuale Änderung zeigt extreme Sprünge — besonders im November→Dezember (Weihnachtsgeschäft).

        ### Visualisierung: Monatliche Änderung (grün/rot)
        """
    )
    return


@app.cell(hide_code=True)
def _(monthly_change, px):
    _mc = monthly_change.drop_nulls()
    fig_change = px.bar(
        _mc,
        x="sales_month",
        y="pct_change",
        title="Monatliche Umsatzänderung — Juweliere (%)",
        labels={"sales_month": "Monat", "pct_change": "Änderung (%)"},
    )
    fig_change.update_traces(
        marker_color=[
            "green" if x > 0 else "red"
            for x in _mc.get_column("pct_change")
        ]
    )
    fig_change.update_layout(template="plotly_white")
    fig_change
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Das Muster ist markant: Jedes Jahr ein starker Anstieg zum Dezember (grün) und dann ein drastischer Einbruch im Januar (rot). Das ist typisch für stark saisonale Branchen.

        ---

        ### Vorhersage 3: LAG vs. LEAD — Richtung
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    pred_lag_lead = mo.ui.radio(
        options={
            "LAG schaut zurück (Vormonat), LEAD schaut voraus (nächster Monat)": "correct",
            "LAG schaut voraus, LEAD schaut zurück": "umgekehrt",
            "Beide liefern dasselbe Ergebnis, nur die Syntax unterscheidet sich": "gleich",
            "LAG verwendet negative Offsets, LEAD positive": "offset",
        },
        label="**Vorhersage:** Was ist der Unterschied zwischen LAG(sales, 1) und LEAD(sales, 1)?",
    )
    return (pred_lag_lead,)


@app.cell(hide_code=True)
def _(mo, pred_lag_lead):
    if pred_lag_lead.value == "correct":
        _result = (
            mo.md(
                "✅ **Richtig!** LAG greift auf **vorherige** Zeilen zu (zeitlich zurück), "
                "LEAD auf **nachfolgende** (zeitlich voraus). "
                "Merkhilfe: **LAG** = rückwärts (engl. 'lag behind'), **LEAD** = vorwärts (engl. 'lead ahead'). "
                "Tipp: `LAG(col, 1)` = `LEAD(col, -1)` — aber die negative Syntax ist unüblich."
            )
        )
    elif pred_lag_lead.value == "umgekehrt":
        _result = (
            mo.md(
                "❌ Genau umgekehrt! **LAG** schaut **zurück** (engl. 'lag behind' = hinterherhinken), "
                "**LEAD** schaut **voraus** (engl. 'lead ahead' = vorausgehen). "
                "LAG(sales, 1) holt den Vormonats-Umsatz, LEAD(sales, 1) den nächsten Monat."
            )
        )
    elif pred_lag_lead.value == "gleich":
        _result = (
            mo.md(
                "❌ Sie liefern unterschiedliche Ergebnisse! LAG(sales, 1) gibt den Wert der **vorherigen** Zeile, "
                "LEAD(sales, 1) den der **nächsten** Zeile. "
                "LAG hat NULL in der ersten Zeile, LEAD hat NULL in der letzten."
            )
        )
    elif pred_lag_lead.value == "offset":
        _result = (
            mo.md(
                "❌ Beide verwenden **positive** Offsets. LAG(col, 1) = 1 Zeile zurück, "
                "LEAD(col, 1) = 1 Zeile voraus. Der Unterschied liegt in der **Richtung**, "
                "nicht im Vorzeichen des Offsets."
            )
        )
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([pred_lag_lead, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 3.x**

        ---

        ## Phase 4: Moving Averages

        **Gleitende Durchschnitte** glätten kurzfristige Schwankungen und machen den Trend sichtbar.

        | Variante | Fenster | Formel | Anwendung |
        |----------|---------|--------|-----------|
        | **Trailing** | Vergangene n Werte | `ROWS BETWEEN n-1 PRECEDING AND CURRENT ROW` | Real-Time Dashboards |
        | **Zentriert** | n/2 vor + n/2 nach | `ROWS BETWEEN k PRECEDING AND k FOLLOWING` | Retrospektive Analyse |

        Für Monatsdaten: **12-Monats-MA** eliminiert Saisonalität vollständig.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 12.6: 12-Monats Trailing Moving Average
    """)
    return


@app.cell(hide_code=True)
def _(mo, retail_sales):
    ma_data = mo.sql(
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
    return (ma_data,)


@app.cell(hide_code=True)
def _(ma_data, px):
    fig_ma = px.line(
        ma_data,
        x="sales_month",
        y=["sales", "ma_12"],
        title="Retail Sales mit 12-Monats Moving Average",
        labels={"sales_month": "Monat", "value": "Umsatz (Mio. USD)", "variable": "Serie"},
    )
    fig_ma.update_layout(template="plotly_white")
    fig_ma
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Die orange MA-Linie glättet die Saisonalität vollständig und zeigt den reinen **Trend**. Deutlich sichtbar: stetiges Wachstum, Einbruch 2008/09 und erneut 2020.

        ---

        ### Vorhersage 4: Fensterrahmen — Wie viele Zeilen?
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    pred_window = mo.ui.radio(
        options={
            "12 Zeilen — 11 vorherige + aktuelle Zeile = 12": "correct",
            "11 Zeilen — nur die 11 vorherigen": "11",
            "13 Zeilen — 11 vorherige + aktuelle + 1 nachfolgende": "13",
            "Variabel — die Anzahl hängt von der Position ab": "variabel",
        },
        label="**Vorhersage:** `ROWS BETWEEN 11 PRECEDING AND CURRENT ROW` — wie viele Zeilen umfasst dieses Fenster?",
    )
    return (pred_window,)


@app.cell(hide_code=True)
def _(mo, pred_window):
    if pred_window.value == "correct":
        _result = (
            mo.md(
                "✅ **Richtig!** `11 PRECEDING AND CURRENT ROW` umfasst die aktuelle Zeile plus "
                "die 11 davor = **12 Zeilen** insgesamt. Für einen 12-Monats-Durchschnitt brauchen wir "
                "genau das: den aktuellen Monat und die 11 vorherigen. "
                "Häufiger Fehler: `ROWS BETWEEN 12 PRECEDING AND CURRENT ROW` wäre ein 13-Monats-Fenster!"
            )
        )
    elif pred_window.value == "11":
        _result = (
            mo.md(
                "❌ Fast! `ROWS BETWEEN 11 PRECEDING AND CURRENT ROW` schließt die **aktuelle Zeile** "
                "mit ein. Also: 11 vorherige + 1 aktuelle = **12 Zeilen**. "
                "Der Fensterrahmen definiert immer eine Spanne *inklusive* der Grenzen."
            )
        )
    elif pred_window.value == "13":
        _result = (
            mo.md(
                "❌ `CURRENT ROW` ist die Obergrenze, es wird keine Zeile danach einbezogen. "
                "11 vorherige + aktuelle = **12 Zeilen**. Für 13 Zeilen müssten Sie "
                "`ROWS BETWEEN 11 PRECEDING AND 1 FOLLOWING` schreiben."
            )
        )
    elif pred_window.value == "variabel":
        _result = (
            mo.md(
                "❌ Nach den ersten 11 Zeilen ist das Fenster immer **12 Zeilen** groß. "
                "Nur am Anfang der Zeitreihe (die ersten 11 Monate) enthält das Fenster weniger Zeilen, "
                "weil es noch nicht genug Vorgänger gibt. Danach ist es konstant 12."
            )
        )
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([pred_window, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Probieren Sie selbst: Moving Averages

    Experimentieren Sie! Probieren Sie:
    - Einen **3-Monats zentrierten** MA: `ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING`
    - Einen **6-Monats trailing** MA: `ROWS BETWEEN 5 PRECEDING AND CURRENT ROW`
    - Verschiedene Branchen: `'Book stores'`, `'Sporting goods stores'`
    """)
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
                ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
            ), 0) AS ma_3_centered
        FROM retail_sales
        WHERE kind_of_business = 'Book stores'
        ORDER BY sales_month
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 4.x**

        ---

        ## Phase 5: Year-over-Year Vergleiche

        **Problem:** Monatliche Änderungen (LAG(1)) werden von Saisonalität dominiert — ein Rückgang von Dezember auf Januar ist normal, kein Warnsignal.

        **Lösung:** Vergleichen Sie jeden Monat mit dem **gleichen Monat des Vorjahres** → `LAG(sales, 12)`.

        Das eliminiert Saisonalität vollständig und zeigt nur noch den **echten Trend**.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 12.7: YoY-Wachstum mit LAG(12)
    """)
    return


@app.cell(hide_code=True)
def _(mo, retail_sales):
    yoy_data = mo.sql(
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
    return (yoy_data,)


@app.cell(hide_code=True)
def _(px, yoy_data):
    _yoy_clean = yoy_data.drop_nulls()
    fig_yoy = px.line(
        _yoy_clean,
        x="sales_month",
        y="yoy_growth",
        title="Year-over-Year Wachstum — Juweliere (%)",
        labels={"sales_month": "Monat", "yoy_growth": "YoY Wachstum (%)"},
    )
    fig_yoy.add_hline(y=0, line_dash="dash", line_color="gray")
    fig_yoy.update_layout(template="plotly_white")
    fig_yoy
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Die YoY-Linie schwankt um 0 % — saisonale Effekte sind eliminiert. Deutlich sichtbar: der Einbruch 2008/09 (Finanzkrise) und 2020 (COVID-19). Im Normalbetrieb bewegt sich das Wachstum meist im Bereich -5 % bis +10 %.

        ---

        ### Vorhersage 5: LAG(12) vs. LAG(1) bei Saisonalität
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    pred_yoy = mo.ui.radio(
        options={
            "LAG(12) vergleicht mit dem gleichen Monat im Vorjahr — eliminiert Saisonalität": "correct",
            "LAG(1) ist besser, weil es aktuellere Vergleichswerte nutzt": "lag1_besser",
            "Beide eliminieren Saisonalität, LAG(12) ist nur langsamer": "gleich",
            "Weder LAG(1) noch LAG(12) helfen bei Saisonalität — man braucht PARTITION BY": "keins",
        },
        label="**Vorhersage:** Warum ist LAG(12) besser als LAG(1) für die Analyse saisonaler Zeitreihen?",
    )
    return (pred_yoy,)


@app.cell(hide_code=True)
def _(mo, pred_yoy):
    if pred_yoy.value == "correct":
        _result = (
            mo.md(
                "✅ **Richtig!** LAG(12) vergleicht **Dezember 2019 mit Dezember 2018** — "
                "beide haben den gleichen saisonalen Effekt, der sich herausdividiert. "
                "LAG(1) würde Dezember mit November vergleichen — und der Anstieg ist nur "
                "saisonale Routine, kein echtes Wachstum."
            )
        )
    elif pred_yoy.value == "lag1_besser":
        _result = (
            mo.md(
                "❌ LAG(1) ist **schlechter** für saisonale Daten! Der Vergleich Dezember → November "
                "zeigt immer einen Anstieg (Weihnachtsgeschäft), Januar → Dezember immer einen Rückgang. "
                "LAG(12) vergleicht **gleiche Monate** und eliminiert so die Saisonalität."
            )
        )
    elif pred_yoy.value == "gleich":
        _result = (
            mo.md(
                "❌ LAG(1) eliminiert Saisonalität **nicht** — es vergleicht aufeinanderfolgende Monate, "
                "die naturgemäß unterschiedliche saisonale Niveaus haben. "
                "Nur LAG(12) vergleicht den **gleichen Monat** im Vorjahr und neutralisiert so "
                "saisonale Effekte."
            )
        )
    elif pred_yoy.value == "keins":
        _result = (
            mo.md(
                "❌ LAG(12) eliminiert Saisonalität sehr effektiv! Es vergleicht jeden Monat mit "
                "dem **gleichen Monat des Vorjahres** — der saisonale Effekt ist in beiden Werten gleich "
                "und kürzt sich heraus. PARTITION BY ist hier nicht nötig."
            )
        )
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([pred_yoy, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 5.x**

        ---

        ## Phase 6: Praktische Anwendung
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 12.8: Branchenvergleich — Herren- vs. Damenbekleidung
    """)
    return


@app.cell(hide_code=True)
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


@app.cell(hide_code=True)
def _(men_vs_women, px):
    fig_ratio = px.line(
        men_vs_women,
        x="year",
        y="womens_to_mens_ratio",
        title="Verhältnis Damen- zu Herrenbekleidung (jährlich)",
        labels={"year": "Jahr", "womens_to_mens_ratio": "Verhältnis (Damen / Herren)"},
    )
    fig_ratio.update_layout(template="plotly_white")
    fig_ratio
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Das Verhältnis Damen-/Herrenbekleidung hat sich über die Jahre stark verändert — die Schere hat sich geschlossen. Ein Beispiel dafür, wie Zeitreihenanalyse langfristige Marktverschiebungen sichtbar macht.

        ---

        ### Geführtes Beispiel 12.9: Saisonale Muster — 3 Branchen im Vergleich
        """
    )
    return


@app.cell(hide_code=True)
def _(mo, retail_sales):
    seasonal_data = mo.sql(
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
    return (seasonal_data,)


@app.cell(hide_code=True)
def _(px, seasonal_data):
    fig_seasonal = px.line(
        seasonal_data,
        x="month_num",
        y="avg_sales",
        color="kind_of_business",
        title="Saisonale Muster nach Branche (Durchschnitt 1992–2020)",
        labels={"month_num": "Monat", "avg_sales": "Ø Umsatz (Mio. USD)", "kind_of_business": "Branche"},
    )
    fig_seasonal.update_layout(template="plotly_white")
    fig_seasonal
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Jede Branche hat ein eigenes saisonales Profil:

        - **Juweliere:** Extremer Dezember-Peak (Weihnachten, Verlobungen)
        - **Sportgeschäfte:** Frühlings-Peak (Outdoorsaison)
        - **Buchläden:** Moderatere Saisonalität, leichter Anstieg zu Schuljahresbeginn

        ---

        ### Probieren Sie selbst: Praktische Anwendung

        Experimentieren Sie mit eigenen Analysen! Ideen:
        - YoY-Wachstum für 2020 — welche Branchen profitieren von COVID?
        - Anteil am Gesamtumsatz über die Zeit: `SUM() OVER (PARTITION BY sales_month)`
        - Volatilste Branchen: `STDDEV(yoy_growth)` pro Branche
        """
    )
    return


@app.cell
def _(mo, retail_sales):
    _df = mo.sql(
        f"""
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
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 7 (Bonus): Indexierung

        **Indexierung** normalisiert alle Werte relativ zu einem Basiswert (z.B. Januar 1992 = 100 %).
        Das ermöglicht den Vergleich von Branchen mit unterschiedlichen Umsatzniveaus.

        ```sql
        FIRST_VALUE(sales) OVER (ORDER BY sales_month)  -- Basiswert
        sales * 100.0 / FIRST_VALUE(sales) OVER (...)   -- Index
        ```
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 12.10: Indexierung zum Basisjahr
    """)
    return


@app.cell(hide_code=True)
def _(mo, retail_sales):
    indexed_data = mo.sql(
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
    return (indexed_data,)


@app.cell(hide_code=True)
def _(indexed_data, px):
    fig_indexed = px.line(
        indexed_data,
        x="sales_month",
        y="pct_from_base",
        title="Indexierte Verkaufszahlen — Damenbekleidung (Basis: Jan 1992)",
        labels={"sales_month": "Monat", "pct_from_base": "Änderung vs. Basis (%)"},
    )
    fig_indexed.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Basiswert")
    fig_indexed.update_layout(template="plotly_white")
    fig_indexed
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Die Indexierung macht langfristige Entwicklungen vergleichbar. Man sieht sofort, ob und wann eine Branche über oder unter ihrem Ausgangsniveau lag.

        ---

        ## Selbsttest
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    selbsttest_1 = mo.ui.radio(
        options={
            "Weil LAG(12) jeden Monat mit dem gleichen Monat im Vorjahr vergleicht — der saisonale Effekt kürzt sich heraus": "correct",
            "Weil LAG(12) einen 12-Monats-Durchschnitt berechnet": "avg",
            "Weil LAG(12) die Zeitreihe um 12 Monate verschiebt und so Schwankungen ausgleicht": "offset",
        },
        label="Warum eliminiert LAG(12) die Saisonalität?",
    )
    return (selbsttest_1,)


@app.cell(hide_code=True)
def _(mo, selbsttest_1):
    if selbsttest_1.value == "correct":
        _result = (
            mo.md(
                "✅ **Richtig!** LAG(12) vergleicht z.B. Dezember 2019 mit Dezember 2018. "
                "Beide Monate haben denselben saisonalen Effekt (Weihnachtsgeschäft), "
                "der sich bei der Differenzbildung herauskürzt. Übrig bleibt nur das **echte Wachstum**."
            )
        )
    elif selbsttest_1.value == "avg":
        _result = (
            mo.md(
                "❌ LAG(12) berechnet keinen Durchschnitt — das wäre `AVG() OVER (ROWS BETWEEN 11 PRECEDING AND CURRENT ROW)`. "
                "LAG(12) greift auf den Wert **genau 12 Zeilen zurück** zu (= gleicher Monat im Vorjahr). "
                "So vergleicht es z.B. Dezember mit Dezember."
            )
        )
    elif selbsttest_1.value == "offset":
        _result = (
            mo.md(
                "❌ LAG(12) verschiebt die Zeitreihe nicht — es holt den Wert 12 Zeilen zurück als "
                "Vergleichswert. Der Mechanismus: Dezember 2019 wird mit Dezember 2018 verglichen. "
                "Da beide den gleichen saisonalen Effekt haben, kürzt er sich heraus."
            )
        )
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([selbsttest_1, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    selbsttest_2 = mo.ui.radio(
        options={
            "Trailing für Echtzeitentscheidungen (nur vergangene Daten), zentriert für retrospektive Analyse (genauere Glättung)": "correct",
            "Trailing ist immer besser — er verwendet mehr Daten": "trailing_always",
            "Zentriert ist immer besser — er ist symmetrisch und daher genauer": "centered_always",
        },
        label="Trailing vs. zentrierter Moving Average — wann welchen verwenden?",
    )
    return (selbsttest_2,)


@app.cell(hide_code=True)
def _(mo, selbsttest_2):
    if selbsttest_2.value == "correct":
        _result = (
            mo.md(
                "✅ **Richtig!** Der **Trailing MA** verwendet nur vergangene Daten und ist daher "
                "für Echtzeit-Dashboards geeignet — er 'weiß' nichts über die Zukunft. "
                "Der **zentrierte MA** bezieht Werte vor und nach dem aktuellen Punkt ein und "
                "ist symmetrisch, was eine genauere Trendschätzung ergibt — aber er funktioniert "
                "nur retrospektiv, weil die zukünftigen Werte bereits bekannt sein müssen."
            )
        )
    elif selbsttest_2.value:
        _result = (
            mo.md(
                "Nicht ganz. Keiner ist immer besser. **Trailing MA** ist für Echtzeit geeignet (nur "
                "vergangene Daten nötig), **zentrierter MA** für retrospektive Analyse (symmetrisch, genauerer Trend). "
                "Die Wahl hängt vom Anwendungsfall ab."
            )
        )
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([selbsttest_2, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    selbsttest_3 = mo.ui.radio(
        options={
            "ROWS zählt physische Zeilen, RANGE gruppiert gleiche Werte — bei eindeutigen Zeitstempeln ist das Ergebnis identisch": "correct",
            "Es gibt keinen Unterschied — beides sind Synonyme": "gleich",
            "ROWS ist schneller, RANGE genauer": "rows_faster",
        },
        label="Was ist der Unterschied zwischen ROWS und RANGE in Window-Frame-Spezifikationen?",
    )
    return (selbsttest_3,)


@app.cell(hide_code=True)
def _(mo, selbsttest_3):
    if selbsttest_3.value == "correct":
        _result = (
            mo.md(
                "✅ **Richtig!** `ROWS` zählt die **physischen Zeilen** (z.B. genau 11 Zeilen zurück). "
                "`RANGE` gruppiert alle Zeilen mit dem **gleichen ORDER BY-Wert** zusammen. "
                "Bei eindeutigen Zeitstempeln (wie monatliche Daten pro Branche) sind die Ergebnisse "
                "identisch. Bei Duplikaten im ORDER BY kann `RANGE` mehr Zeilen einschließen als erwartet."
            )
        )
    elif selbsttest_3.value:
        _result = (
            mo.md(
                "Nicht ganz. `ROWS` zählt physische Zeilen, `RANGE` gruppiert gleiche ORDER BY-Werte. "
                "Bei eindeutigen Werten sind sie identisch; bei Duplikaten kann `RANGE` "
                "unerwartete Ergebnisse liefern. Für Zeitreihenanalyse empfiehlt sich meist `ROWS`."
            )
        )
    else:
        _result = mo.callout(mo.md("Bitte wählen."), kind="info")
    mo.vstack([selbsttest_3, _result])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Zusammenfassung

        | Konzept | SQL-Befehl | Beispiel |
        |---------|-----------|----------|
        | **LAG** | `LAG(col, n) OVER (ORDER BY ...)` | Vorheriger Wert: Monatsänderung |
        | **LEAD** | `LEAD(col, n) OVER (ORDER BY ...)` | Nächster Wert: Vorausschau |
        | **Moving Average** | `AVG() OVER (ROWS BETWEEN ...)` | Trend glätten: 12-Monats-MA |
        | **YoY-Vergleich** | `LAG(col, 12) OVER (ORDER BY ...)` | Saisonalität eliminieren |
        | **Ranking** | `RANK() OVER (ORDER BY ... DESC)` | Top-N Monate finden |
        | **Indexierung** | `FIRST_VALUE() OVER (ORDER BY ...)` | Normalisierung zum Basiswert |

        ### Entscheidungsbaum

        ```
        Was möchte ich analysieren?
        ├── Veränderung zum Vormonat → LAG(col, 1)
        ├── Veränderung zum Vorjahr → LAG(col, 12)
        ├── Trend sichtbar machen → AVG() OVER (ROWS BETWEEN ...)
        ├── Branchen vergleichen → FIRST_VALUE() (Indexierung)
        └── Top-N finden → RANK() / ROW_NUMBER()
        ```

        ### Fensterrahmen auf einen Blick

        | Angabe | Zeilen | Anwendung |
        |--------|--------|-----------|
        | `ROWS BETWEEN 11 PRECEDING AND CURRENT ROW` | 12 (trailing) | 12-Monats-MA |
        | `ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING` | 3 (zentriert) | 3-Monats-MA |
        | `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` | Alle bis jetzt | Kumulative Summe |

        ### Ausblick Session 13: Textanalyse

        Nächste Woche kommt die Textdimension: SQL-String-Funktionen, Pattern Matching und reguläre Ausdrücke.
        """
    )
    return


if __name__ == "__main__":
    app.run()
