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
app = marimo.App(width="medium", app_title="DMA Session 11: Explorative Datenanalyse")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Vorlesung 11: Explorative Datenanalyse (EDA)

        **Kursfahrplan:** I: SQL-Grundlagen (S1–4) · II: Datenmodellierung (S5–8) · III: Fortgeschrittenes SQL (S9–10) · **▸ IV: Datenanalyse (S11–14)**

        In den Sessions 1–10 haben wir gelernt, Daten zu speichern, zu modellieren und abzufragen. Jetzt beginnt Teil IV: Wir nutzen SQL als **Analysewerkzeug** — angefangen mit der systematischen Erkundung von Daten.

        **Lernziele:**
        - EDA systematisch durchführen und dokumentieren
        - Univariate Analyse: Verteilungen, Ausreißer erkennen
        - Bivariate Analyse: Korrelationen, Gruppenvergleiche
        - SQL für EDA: Aggregationen, CASE WHEN, Binning
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
    # Gehaltsdaten für EDA-Übungen
    gehaltsdaten = pl.DataFrame({
        "mitarbeiter_id": list(range(1, 101)),
        "name": [f"Mitarbeiter_{i}" for i in range(1, 101)],
        "abteilung": (["IT"] * 25 + ["HR"] * 20 + ["Vertrieb"] * 30 + ["Finanzen"] * 15 + ["Marketing"] * 10),
        "alter": [28, 32, 45, 29, 35, 41, 38, 27, 52, 33,
                  31, 29, 44, 36, 39, 42, 30, 48, 34, 37,
                  26, 55, 31, 40, 35, 28, 33, 46, 30, 38,
                  43, 29, 36, 50, 32, 41, 27, 34, 47, 39,
                  35, 30, 42, 28, 53, 37, 31, 44, 33, 40,
                  29, 36, 48, 32, 38, 45, 27, 41, 34, 51,
                  30, 43, 28, 37, 49, 33, 39, 46, 31, 42,
                  35, 29, 44, 32, 54, 38, 30, 47, 36, 41,
                  28, 50, 33, 40, 26, 43, 31, 45, 34, 39,
                  37, 29, 48, 32, 52, 36, 30, 42, 35, 280],  # Outlier: 280 statt 28
        "gehalt": [52000, 58000, 75000, 48000, 62000, 71000, 65000, 45000, 88000, 55000,
                   53000, 47000, 72000, 59000, 66000, 73000, 51000, 82000, 56000, 63000,
                   44000, 92000, 52000, 68000, 60000, 46000, 54000, 78000, 50000, 64000,
                   74000, 48000, 61000, 85000, 53000, 69000, 43000, 57000, 80000, 65000,
                   58000, 49000, 70000, 45000, 89000, 62000, 51000, 76000, 54000, 67000,
                   47000, 59000, 81000, 52000, 63000, 77000, 44000, 68000, 55000, 86000,
                   50000, 73000, 46000, 61000, 83000, 53000, 66000, 79000, 51000, 71000,
                   57000, 48000, 75000, 52000, 91000, 64000, 49000, 80000, 60000, 69000,
                   45000, 84000, 54000, 67000, 42000, 72000, 50000, 78000, 56000, 65000,
                   62000, 47000, 82000, 53000, 88000, 59000, 49000, 74000, 58000, 450000],  # Outlier: CEO
        "erfahrung_jahre": [3, 7, 20, 4, 10, 16, 13, 2, 27, 8,
                           6, 4, 19, 11, 14, 17, 5, 23, 9, 12,
                           1, 30, 6, 15, 10, 3, 8, 21, 5, 13,
                           18, 4, 11, 25, 7, 16, 2, 9, 22, 14,
                           10, 5, 17, 3, 28, 12, 6, 19, 8, 15,
                           4, 11, 23, 7, 13, 20, 2, 16, 9, 26,
                           5, 18, 3, 12, 24, 8, 14, 21, 6, 17,
                           10, 4, 19, 7, 29, 13, 5, 22, 11, 16,
                           3, 25, 8, 15, 1, 18, 6, 20, 9, 14,
                           12, 4, 23, 7, 27, 11, 5, 19, 10, 35],
        "geschlecht": (["M", "W"] * 50),
        "standort": (["München"] * 40 + ["Berlin"] * 35 + ["Hamburg"] * 25),
    })

    # Einige NULL-Werte einfügen
    gehaltsdaten = gehaltsdaten.with_columns([
        pl.when(pl.col("mitarbeiter_id").is_in([15, 42, 73, 88]))
        .then(None)
        .otherwise(pl.col("erfahrung_jahre"))
        .alias("erfahrung_jahre")
    ])

    daten_beschreibung = "Fiktive Gehaltsdaten (100 Mitarbeiter, inkl. Ausreißer und Missing Values)"
    return daten_beschreibung, gehaltsdaten


@app.cell(hide_code=True)
def _(daten_beschreibung, mo):
    mo.md(
        f"""
        **Datensatz:** {daten_beschreibung}

        ---

        ## Phase 1: Erste Dateninspektion

        Bevor wir analysieren, müssen wir die Daten **kennenlernen**.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 11.1: Datenüberblick

        Wie viele Zeilen und Spalten haben unsere Daten? Welche Datentypen?
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    mo.sql(
        f"""
        SELECT
            COUNT(*) AS anzahl_zeilen
        FROM gehaltsdaten
        """
    )


@app.cell
def _(gehaltsdaten):
    # Spalteninfo mit Polars
    gehaltsdaten.schema
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 11.2: Erste Zeilen ansehen

        Schauen Sie sich die ersten Datensätze an, um ein Gefühl für die Daten zu bekommen.
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    mo.sql(
        f"""
        SELECT * FROM gehaltsdaten LIMIT 10
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 2: Univariate Analyse

        Jede Variable einzeln betrachten: Verteilung, Zentrum, Streuung.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 11.3: Deskriptive Statistiken für Gehalt

        Berechnen Sie Mittelwert, Median, Min, Max und Standardabweichung.
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    gehalt_stats = mo.sql(
        f"""
        SELECT
            COUNT(*) AS n,
            ROUND(AVG(gehalt), 2) AS mittelwert,
            PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY gehalt) AS median,
            MIN(gehalt) AS minimum,
            MAX(gehalt) AS maximum,
            ROUND(STDDEV(gehalt), 2) AS std_abweichung
        FROM gehaltsdaten
        """
    )
    return (gehalt_stats,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Der Mittelwert ist deutlich höher als der Median!
        Das deutet auf einen oder mehrere Ausreißer nach oben hin.

        ### Aufgabe 11.4: Quartile und IQR berechnen
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    quartile = mo.sql(
        f"""
        SELECT
            PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY gehalt) AS q1,
            PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY gehalt) AS median,
            PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY gehalt) AS q3,
            PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY gehalt)
                - PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY gehalt) AS iqr
        FROM gehaltsdaten
        """
    )
    return (quartile,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Visualisierung: Gehaltsverteilung
        """
    )
    return


@app.cell
def _(gehaltsdaten, px):
    fig_hist = px.histogram(
        gehaltsdaten,
        x="gehalt",
        nbins=30,
        title="Verteilung der Gehälter",
        labels={"gehalt": "Gehalt (EUR)", "count": "Anzahl"}
    )
    fig_hist.update_layout(showlegend=False)
    fig_hist


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Ein extremer Ausreißer ist deutlich sichtbar (CEO-Gehalt?).

        > **Vorhersage:** Der Datensatz enthält 100 Mitarbeiter. Wie viele Ausreißer erwarten Sie beim Gehalt, wenn wir die IQR-Regel (1,5 × IQR) anwenden? Und beim Alter?

        ---

        ## Phase 3: Ausreißer erkennen

        ### Aufgabe 11.5: Ausreißer mit IQR-Regel finden
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    ausreisser = mo.sql(
        f"""
        WITH quartile AS (
            SELECT
                PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY gehalt) AS q1,
                PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY gehalt) AS q3
            FROM gehaltsdaten
        ),
        grenzen AS (
            SELECT
                q1 - 1.5 * (q3 - q1) AS untere_grenze,
                q3 + 1.5 * (q3 - q1) AS obere_grenze
            FROM quartile
        )
        SELECT g.*, gr.untere_grenze, gr.obere_grenze
        FROM gehaltsdaten g, grenzen gr
        WHERE g.gehalt < gr.untere_grenze
           OR g.gehalt > gr.obere_grenze
        ORDER BY g.gehalt DESC
        """
    )
    return (ausreisser,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 11.6: Selbstständig - Ausreißer im Alter finden

        Finden Sie auch die Ausreißer in der Spalte `alter` mit der IQR-Regel.
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    # Ihre Lösung hier:
    alter_ausreisser = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: Gleiche CTE-Struktur wie bei Aufgabe 11.5 (Gehalt), aber für 'alter'
        -- 1. WITH quartile AS (SELECT Q1, Q3 FROM gehaltsdaten)
        -- 2. grenzen AS (SELECT q1 - 1.5*IQR, q3 + 1.5*IQR)
        -- 3. SELECT WHERE alter < untere_grenze OR alter > obere_grenze
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return (alter_ausreisser,)


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
WITH quartile AS (
    SELECT
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY alter) AS q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY alter) AS q3
    FROM gehaltsdaten
),
grenzen AS (
    SELECT
        q1 - 1.5 * (q3 - q1) AS untere_grenze,
        q3 + 1.5 * (q3 - q1) AS obere_grenze
    FROM quartile
)
SELECT g.*, gr.untere_grenze, gr.obere_grenze
FROM gehaltsdaten g, grenzen gr
WHERE g.alter < gr.untere_grenze
   OR g.alter > gr.obere_grenze
ORDER BY g.alter DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Ein Mitarbeiter hat Alter 280 - offensichtlich ein Datenfehler (vermutlich 28 gemeint).

        ---

        ## Phase 4: Missing Values analysieren

        ### Aufgabe 11.7: Fehlende Werte zählen
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    mo.sql(
        f"""
        SELECT
            COUNT(*) AS total,
            COUNT(erfahrung_jahre) AS vorhanden,
            COUNT(*) - COUNT(erfahrung_jahre) AS fehlend,
            ROUND((COUNT(*) - COUNT(erfahrung_jahre)) * 100.0 / COUNT(*), 1) AS prozent_fehlend
        FROM gehaltsdaten
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 5: Bivariate Analyse

        Zusammenhänge zwischen Variablen untersuchen.

        ### Aufgabe 11.8: Korrelation Alter-Gehalt
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    mo.sql(
        f"""
        SELECT
            ROUND(CORR(alter, gehalt), 3) AS korrelation_alter_gehalt,
            ROUND(CORR(erfahrung_jahre, gehalt), 3) AS korrelation_erfahrung_gehalt
        FROM gehaltsdaten
        WHERE alter < 100  -- Ausreißer ausschließen
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Visualisierung: Scatterplot Erfahrung vs. Gehalt
        """
    )
    return


@app.cell
def _(gehaltsdaten, px):
    # Daten ohne extreme Ausreißer für bessere Visualisierung
    clean_data = gehaltsdaten.filter(
        (gehaltsdaten["gehalt"] < 200000) & (gehaltsdaten["alter"] < 100)
    )

    fig_scatter = px.scatter(
        clean_data,
        x="erfahrung_jahre",
        y="gehalt",
        color="abteilung",
        title="Gehalt vs. Erfahrung (ohne extreme Ausreißer)",
        labels={"erfahrung_jahre": "Erfahrung (Jahre)", "gehalt": "Gehalt (EUR)"},
        trendline="ols"
    )
    fig_scatter
    return clean_data, fig_scatter


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 11.9: Gruppenvergleich nach Abteilung
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    abteilung_stats = mo.sql(
        f"""
        SELECT
            abteilung,
            COUNT(*) AS n,
            ROUND(AVG(gehalt), 0) AS mittel_gehalt,
            ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY gehalt), 0) AS median_gehalt,
            MIN(gehalt) AS min_gehalt,
            MAX(gehalt) AS max_gehalt
        FROM gehaltsdaten
        WHERE gehalt < 200000  -- Ausreißer ausschließen
        GROUP BY abteilung
        ORDER BY mittel_gehalt DESC
        """
    )
    return (abteilung_stats,)


@app.cell
def _(clean_data, px):
    fig_box = px.box(
        clean_data,
        x="abteilung",
        y="gehalt",
        title="Gehaltsverteilung nach Abteilung",
        labels={"abteilung": "Abteilung", "gehalt": "Gehalt (EUR)"}
    )
    fig_box


@app.cell(hide_code=True)
def _(mo):
    quiz_window = mo.ui.radio(
        options={
            "correct": "GROUP BY reduziert Zeilen (eine pro Gruppe), Window Functions behalten alle Zeilen",
            "reversed": "Window Functions reduzieren Zeilen, GROUP BY behält alle Zeilen",
            "speed": "GROUP BY ist schneller, Window Functions sind langsamer — sonst gleich",
            "syntax": "GROUP BY braucht SELECT, Window Functions brauchen nur OVER()",
        },
        label="**Quiz:** Was ist der Hauptunterschied zwischen GROUP BY und Window Functions?"
    )
    quiz_window
    return (quiz_window,)


@app.cell(hide_code=True)
def _(quiz_window, mo):
    if quiz_window.value == "correct":
        mo.output.replace(mo.md("Richtig! GROUP BY fasst viele Zeilen zu einer zusammen (z.B. eine Zeile pro Mannschaft). Window Functions berechnen Aggregate, aber **jede Originalzeile bleibt erhalten** — Sie bekommen die Aggregation *neben* den Originaldaten."))
    elif quiz_window.value:
        mo.output.replace(mo.md("Nicht ganz. Der entscheidende Unterschied: GROUP BY *komprimiert* Zeilen (viele → eine pro Gruppe). Window Functions mit OVER() berechnen dasselbe, aber **behalten alle Originalzeilen** bei."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 6: SQL für EDA - Binning

        ### Aufgabe 11.10: Gehaltsklassen erstellen
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    mo.sql(
        f"""
        SELECT
            CASE
                WHEN gehalt < 50000 THEN '1: unter 50k'
                WHEN gehalt < 65000 THEN '2: 50-65k'
                WHEN gehalt < 80000 THEN '3: 65-80k'
                WHEN gehalt < 100000 THEN '4: 80-100k'
                ELSE '5: über 100k'
            END AS gehaltsklasse,
            COUNT(*) AS anzahl,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM gehaltsdaten), 1) AS prozent
        FROM gehaltsdaten
        GROUP BY gehaltsklasse
        ORDER BY gehaltsklasse
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 11.11: Selbstständig - Altersgruppen analysieren

        Erstellen Sie Altersgruppen (unter 30, 30-40, 40-50, über 50) und
        berechnen Sie das Durchschnittsgehalt pro Gruppe.

        *Hinweis: Schließen Sie den Ausreißer (Alter > 100) aus.*
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    # Ihre Lösung hier:
    mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: CASE WHEN alter < 30 THEN '1: unter 30' ... END AS altersgruppe
        -- GROUP BY altersgruppe, dann AVG(gehalt) berechnen
        -- Ausreißer ausschließen: WHERE alter < 100 AND gehalt < 200000
        -- Erwartete Spalten: altersgruppe, anzahl, durchschnitt_gehalt
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    CASE
        WHEN alter < 30 THEN '1: unter 30'
        WHEN alter < 40 THEN '2: 30-40'
        WHEN alter < 50 THEN '3: 40-50'
        ELSE '4: über 50'
    END AS altersgruppe,
    COUNT(*) AS anzahl,
    ROUND(AVG(gehalt), 0) AS durchschnitt_gehalt
FROM gehaltsdaten
WHERE alter < 100 AND gehalt < 200000
GROUP BY altersgruppe
ORDER BY altersgruppe
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 7: Vollständige EDA - Zusammenfassung

        ### Aufgabe 11.12: EDA-Report erstellen

        Fassen Sie Ihre Erkenntnisse zusammen:
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **EDA-Erkenntnisse für den Gehaltsdatensatz:**

        1. **Datenqualität:**
           - 100 Datensätze, 8 Variablen
           - 4 fehlende Werte bei `erfahrung_jahre` (4%)
           - 2 Ausreißer identifiziert: CEO-Gehalt (450k), Alter-Fehler (280)

        2. **Univariate Analyse:**
           - Gehaltsverteilung ist rechtsschief (Mean > Median)
           - Typisches Gehalt: ca. 55-65k EUR (ohne Ausreißer)
           - Alter: 26-55 Jahre (ein Datenfehler bei 280)

        3. **Bivariate Analyse:**
           - Positive Korrelation zwischen Erfahrung und Gehalt
           - Gehaltsunterschiede zwischen Abteilungen
           - IT und Finanzen haben höchste Durchschnittsgehälter

        4. **Empfehlungen:**
           - Alter-Fehler (280) korrigieren zu 28
           - CEO-Gehalt separat behandeln oder ausschließen
           - Missing Values bei Erfahrung untersuchen (nur 4 Fälle)
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Datasaurus Dozen: Warum Visualisierung unverzichtbar ist

        **Anscombe's Quartet** (1973) zeigte: 4 Datensätze mit identischen Statistiken,
        aber völlig verschiedenen Mustern.

        Das **Datasaurus Dozen** (2017) treibt das auf die Spitze:
        **13 Datensätze** mit nahezu identischen Statistiken — darunter ein Dinosaurier!

        Alle 13 Datensätze haben:

        - Gleichen Mittelwert (x ≈ 54.3, y ≈ 47.8)
        - Gleiche Standardabweichung (x ≈ 16.8, y ≈ 26.9)
        - Gleiche Korrelation (r ≈ −0.06)
        """
    )
    return


@app.cell
def _(pl):
    # Datasaurus Dozen laden
    try:
        datasaurus = pl.read_csv(
            "https://raw.githubusercontent.com/jumpingrivers/datasauRus/main/inst/extdata/DatasaurusDozen-long.csv"
        )
        ds_quelle = "Live-Daten (GitHub)"
    except Exception:
        # Minimaler Fallback: leerer Hinweis
        datasaurus = pl.DataFrame({"dataset": ["?"], "x": [0.0], "y": [0.0]})
        ds_quelle = "Fehler beim Laden — bitte Internetverbindung prüfen"

    return datasaurus, ds_quelle


@app.cell
def _(datasaurus, mo):
    mo.sql(
        f"""
        SELECT
            dataset,
            ROUND(AVG(x), 2) AS mean_x,
            ROUND(AVG(y), 2) AS mean_y,
            ROUND(STDDEV(x), 2) AS std_x,
            ROUND(STDDEV(y), 2) AS std_y,
            ROUND(CORR(x, y), 3) AS korrelation,
            COUNT(*) AS n
        FROM datasaurus
        GROUP BY dataset
        ORDER BY dataset
        """
    )


@app.cell
def _(datasaurus, px):
    px.scatter(
        datasaurus,
        x="x",
        y="y",
        facet_col="dataset",
        facet_col_wrap=4,
        width=900,
        height=900,
        title="Datasaurus Dozen — Gleiche Statistiken, völlig verschiedene Muster",
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Freie Exploration

        Probieren Sie eigene Analysen:

        - Geschlechterverteilung nach Abteilung
        - Gehalt nach Standort vergleichen
        - Korrelationsmatrix erstellen
        - Weitere Visualisierungen
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    # Eigene Analyse hier:
    mo.sql(
        f"""
        SELECT
            standort,
            geschlecht,
            COUNT(*) AS anzahl,
            ROUND(AVG(gehalt), 0) AS durchschnitt_gehalt
        FROM gehaltsdaten
        WHERE gehalt < 200000
        GROUP BY standort, geschlecht
        ORDER BY standort, geschlecht
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Zusammenfassung

        | Konzept | Beschreibung | SQL |
        |---------|--------------|-----|
        | **Lagemaße** | Zentrum der Daten | `AVG()`, `PERCENTILE_CONT(0.5)` |
        | **Streuungsmaße** | Variabilität | `STDDEV()`, `MAX()-MIN()` |
        | **Ausreißer** | IQR-Regel | `Q1 - 1.5*IQR`, `Q3 + 1.5*IQR` |
        | **Korrelation** | Zusammenhang | `CORR(x, y)` |
        | **Binning** | Kategorisieren | `CASE WHEN ... THEN ...` |
        | **Missing Values** | Fehlende Werte | `COUNT(*) - COUNT(spalte)` |

        **Goldene Regel:** Immer visualisieren! (Anscombe's Quartet / Datasaurus Dozen)

        **Nächste Session:** Statistische Inferenz & A/B-Tests
        """
    )
    return


if __name__ == "__main__":
    app.run()
