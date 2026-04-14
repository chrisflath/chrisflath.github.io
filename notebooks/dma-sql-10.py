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
    app_title="DMA Session 10: Explorative Datenanalyse — Übungen",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 10: Explorative Datenanalyse (EDA) — Übungen

        Theorie und geführte Beispiele → **10-eda-guide.py**

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
                  37, 29, 48, 32, 52, 36, 30, 42, 35, 280],
        "gehalt": [52000, 58000, 75000, 48000, 62000, 71000, 65000, 45000, 88000, 55000,
                   53000, 47000, 72000, 59000, 66000, 73000, 51000, 82000, 56000, 63000,
                   44000, 92000, 52000, 68000, 60000, 46000, 54000, 78000, 50000, 64000,
                   74000, 48000, 61000, 85000, 53000, 69000, 43000, 57000, 80000, 65000,
                   58000, 49000, 70000, 45000, 89000, 62000, 51000, 76000, 54000, 67000,
                   47000, 59000, 81000, 52000, 63000, 77000, 44000, 68000, 55000, 86000,
                   50000, 73000, 46000, 61000, 83000, 53000, 66000, 79000, 51000, 71000,
                   57000, 48000, 75000, 52000, 91000, 64000, 49000, 80000, 60000, 69000,
                   45000, 84000, 54000, 67000, 42000, 72000, 50000, 78000, 56000, 65000,
                   62000, 47000, 82000, 53000, 88000, 59000, 49000, 74000, 58000, 450000],
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

    return gehaltsdaten, mo, pl, px


# -----------------------------------------------------------------------
# Phase 1: Erste Dateninspektion
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 1: Erste Dateninspektion
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 1.1: Zeilenanzahl und Schema

        Wie viele Zeilen hat der Datensatz? Welche Spalten gibt es?
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        SELECT COUNT(*) AS anzahl_zeilen
        FROM gehaltsdaten
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT COUNT(*) AS anzahl_zeilen
FROM gehaltsdaten
```
**Ergebnis:** 100 Zeilen mit 8 Spalten (mitarbeiter_id, name, abteilung, alter, gehalt, erfahrung_jahre, geschlecht, standort).
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 1.2: Erste Zeilen ansehen

        Schauen Sie sich die ersten 10 Datensätze an.
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM gehaltsdaten LIMIT 10
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT * FROM gehaltsdaten LIMIT 10
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 1.3: Verteilung nach Abteilung (Scaffolded)

        Wie viele Mitarbeiter gibt es pro Abteilung? Ergänzen Sie die fehlenden Teile (`???`):
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        SELECT
            ???,
            COUNT(*) AS anzahl
        FROM gehaltsdaten
        GROUP BY ???
        ORDER BY anzahl DESC
        -- Tipp: abteilung
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    abteilung,
    COUNT(*) AS anzahl
FROM gehaltsdaten
GROUP BY abteilung
ORDER BY anzahl DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 1.4: Verteilung nach Standort (Selbstständig)

        Wie viele Mitarbeiter gibt es pro Standort? Zeigen Sie auch den prozentualen Anteil.

        *Hinweis: `COUNT(*) * 100.0 / (SELECT COUNT(*) FROM gehaltsdaten) AS prozent`*
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Erwartete Spalten: standort, anzahl, prozent
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    standort,
    COUNT(*) AS anzahl,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM gehaltsdaten), 1) AS prozent
FROM gehaltsdaten
GROUP BY standort
ORDER BY anzahl DESC
```
""")})
    return


# -----------------------------------------------------------------------
# Phase 2: Univariate Analyse
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 2: Univariate Analyse
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 2.1: Deskriptive Statistiken — Gehalt

        Berechnen Sie Mittelwert, Median, Min, Max und Standardabweichung für das Gehalt.
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    _df = mo.sql(
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
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    COUNT(*) AS n,
    ROUND(AVG(gehalt), 2) AS mittelwert,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY gehalt) AS median,
    MIN(gehalt) AS minimum,
    MAX(gehalt) AS maximum,
    ROUND(STDDEV(gehalt), 2) AS std_abweichung
FROM gehaltsdaten
```
**Beobachtung:** Mittelwert >> Median → rechtsschiefe Verteilung (Ausreißer nach oben).
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 2.2: Quartile und IQR (Scaffolded)

        Berechnen Sie Q1, Median, Q3 und den IQR. Ergänzen Sie `???`:
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        SELECT
            PERCENTILE_CONT(???) WITHIN GROUP (ORDER BY gehalt) AS q1,
            PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY gehalt) AS median,
            PERCENTILE_CONT(???) WITHIN GROUP (ORDER BY gehalt) AS q3,
            PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY gehalt)
                - PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY gehalt) AS iqr
        FROM gehaltsdaten
        -- Tipp: 0.25 und 0.75
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY gehalt) AS q1,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY gehalt) AS median,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY gehalt) AS q3,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY gehalt)
        - PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY gehalt) AS iqr
FROM gehaltsdaten
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 2.3: Deskriptive Statistiken — Alter (Selbstständig)

        Berechnen Sie die gleichen Statistiken wie in 2.1, aber für die Spalte `alter`.

        *Hinweis: Gleiche Struktur, nur `gehalt` → `alter`*
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Erwartete Spalten: n, mittelwert, median, minimum, maximum, std_abweichung
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    COUNT(*) AS n,
    ROUND(AVG(alter), 2) AS mittelwert,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY alter) AS median,
    MIN(alter) AS minimum,
    MAX(alter) AS maximum,
    ROUND(STDDEV(alter), 2) AS std_abweichung
FROM gehaltsdaten
```
**Beobachtung:** Max = 280! Offensichtlich ein Datenfehler. Der Mittelwert wird dadurch stark verzerrt.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 2.4: Statistiken pro Abteilung (Selbstständig)

        Berechnen Sie Mittelwert und Median des Gehalts **pro Abteilung** (ohne den CEO-Ausreißer).

        *Hinweis: `GROUP BY abteilung`, `WHERE gehalt < 200000`*
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Erwartete Spalten: abteilung, n, mittel_gehalt, median_gehalt
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    abteilung,
    COUNT(*) AS n,
    ROUND(AVG(gehalt), 0) AS mittel_gehalt,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY gehalt), 0) AS median_gehalt
FROM gehaltsdaten
WHERE gehalt < 200000
GROUP BY abteilung
ORDER BY mittel_gehalt DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 2.5: Debugging — Fehlende GROUP BY

        Die folgende Abfrage soll das Durchschnittsgehalt pro Standort berechnen. Sie hat einen Fehler!
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        -- 🔴 Diese Abfrage hat einen Fehler — finden und beheben Sie ihn!
        SELECT
            standort,
            COUNT(*) AS n,
            ROUND(AVG(gehalt), 0) AS mittel_gehalt
        FROM gehaltsdaten
        WHERE gehalt < 200000
        ORDER BY mittel_gehalt DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**Problem:** `GROUP BY standort` fehlt! Ohne GROUP BY kann `standort` nicht zusammen mit Aggregatfunktionen stehen.

**Lösung:**
```sql
SELECT
    standort,
    COUNT(*) AS n,
    ROUND(AVG(gehalt), 0) AS mittel_gehalt
FROM gehaltsdaten
WHERE gehalt < 200000
GROUP BY standort
ORDER BY mittel_gehalt DESC
```
""")})
    return


# -----------------------------------------------------------------------
# Phase 3: Ausreißer erkennen
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 3: Ausreißer erkennen
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 3.1: Ausreißer — Gehalt (IQR-Regel)

        Finden Sie Gehalts-Ausreißer mit der IQR-Regel (Faktor 1.5).
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    _df = mo.sql(
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
        SELECT g.mitarbeiter_id, g.name, g.abteilung, g.gehalt,
               gr.untere_grenze, gr.obere_grenze
        FROM gehaltsdaten g, grenzen gr
        WHERE g.gehalt < gr.untere_grenze
           OR g.gehalt > gr.obere_grenze
        ORDER BY g.gehalt DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
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
SELECT g.mitarbeiter_id, g.name, g.abteilung, g.gehalt,
       gr.untere_grenze, gr.obere_grenze
FROM gehaltsdaten g, grenzen gr
WHERE g.gehalt < gr.untere_grenze
   OR g.gehalt > gr.obere_grenze
ORDER BY g.gehalt DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 3.2: Ausreißer — Alter (Scaffolded)

        Finden Sie Alters-Ausreißer mit der IQR-Regel. Ergänzen Sie `???`:
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        WITH quartile AS (
            SELECT
                PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY ???) AS q1,
                PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY ???) AS q3
            FROM gehaltsdaten
        ),
        grenzen AS (
            SELECT
                q1 - 1.5 * (q3 - q1) AS untere_grenze,
                q3 + 1.5 * (q3 - q1) AS obere_grenze
            FROM quartile
        )
        SELECT g.mitarbeiter_id, g.name, g.alter,
               gr.untere_grenze, gr.obere_grenze
        FROM gehaltsdaten g, grenzen gr
        WHERE g.??? < gr.untere_grenze
           OR g.??? > gr.obere_grenze
        ORDER BY g.alter DESC
        -- Tipp: Ersetzen Sie alle ??? durch 'alter'
        """
    )
    return


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
SELECT g.mitarbeiter_id, g.name, g.alter,
       gr.untere_grenze, gr.obere_grenze
FROM gehaltsdaten g, grenzen gr
WHERE g.alter < gr.untere_grenze
   OR g.alter > gr.obere_grenze
ORDER BY g.alter DESC
```
**Ergebnis:** Mitarbeiter_100 mit Alter 280 — ein offensichtlicher Datenfehler.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 3.3: Extreme Ausreißer (3× IQR) — Gehalt (Selbstständig)

        Finden Sie nur die **extremen** Ausreißer mit Faktor 3.0 statt 1.5.

        *Hinweis: Gleiche Struktur wie 3.1, aber `1.5` → `3.0`*
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Erwartete Spalten: mitarbeiter_id, name, gehalt, untere_grenze, obere_grenze
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
WITH quartile AS (
    SELECT
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY gehalt) AS q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY gehalt) AS q3
    FROM gehaltsdaten
),
grenzen AS (
    SELECT
        q1 - 3.0 * (q3 - q1) AS untere_grenze,
        q3 + 3.0 * (q3 - q1) AS obere_grenze
    FROM quartile
)
SELECT g.mitarbeiter_id, g.name, g.gehalt,
       gr.untere_grenze, gr.obere_grenze
FROM gehaltsdaten g, grenzen gr
WHERE g.gehalt < gr.untere_grenze
   OR g.gehalt > gr.obere_grenze
ORDER BY g.gehalt DESC
```
**Ergebnis:** Nur der CEO-Ausreißer (450.000 €) wird erkannt — die „milden" Ausreißer fallen weg.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 3.4: Debugging — Fehlende FROM in Subquery

        Die folgende Abfrage soll Ausreißer finden. Sie hat einen Fehler!
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        -- 🔴 Diese Abfrage hat einen Fehler — finden und beheben Sie ihn!
        WITH quartile AS (
            SELECT
                PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY gehalt) AS q1,
                PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY gehalt) AS q3
        ),
        grenzen AS (
            SELECT
                q1 - 1.5 * (q3 - q1) AS untere_grenze,
                q3 + 1.5 * (q3 - q1) AS obere_grenze
            FROM quartile
        )
        SELECT g.mitarbeiter_id, g.gehalt
        FROM gehaltsdaten g, grenzen gr
        WHERE g.gehalt > gr.obere_grenze
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**Problem:** Im ersten CTE `quartile` fehlt `FROM gehaltsdaten`! Ohne FROM weiß die Datenbank nicht, woher die Spalte `gehalt` kommen soll.

**Lösung:**
```sql
WITH quartile AS (
    SELECT
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY gehalt) AS q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY gehalt) AS q3
    FROM gehaltsdaten   -- ← das fehlte!
),
grenzen AS (
    SELECT
        q1 - 1.5 * (q3 - q1) AS untere_grenze,
        q3 + 1.5 * (q3 - q1) AS obere_grenze
    FROM quartile
)
SELECT g.mitarbeiter_id, g.gehalt
FROM gehaltsdaten g, grenzen gr
WHERE g.gehalt > gr.obere_grenze
```
""")})
    return


# -----------------------------------------------------------------------
# Phase 4: Fehlende Werte
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 4: Fehlende Werte
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 4.1: Fehlende Werte zählen

        Wie viele Erfahrungswerte fehlen?
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        SELECT
            COUNT(*) AS total,
            COUNT(erfahrung_jahre) AS vorhanden,
            COUNT(*) - COUNT(erfahrung_jahre) AS fehlend,
            ROUND((COUNT(*) - COUNT(erfahrung_jahre)) * 100.0 / COUNT(*), 1) AS prozent_fehlend
        FROM gehaltsdaten
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    COUNT(*) AS total,
    COUNT(erfahrung_jahre) AS vorhanden,
    COUNT(*) - COUNT(erfahrung_jahre) AS fehlend,
    ROUND((COUNT(*) - COUNT(erfahrung_jahre)) * 100.0 / COUNT(*), 1) AS prozent_fehlend
FROM gehaltsdaten
```
**Trick:** `COUNT(*)` zählt alle Zeilen, `COUNT(spalte)` zählt nur Nicht-NULL-Werte.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 4.2: NULL-Muster nach Abteilung (Scaffolded)

        Gibt es ein Muster — fehlen die Werte in bestimmten Abteilungen häufiger? Ergänzen Sie `???`:
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        SELECT
            abteilung,
            COUNT(*) AS total,
            COUNT(erfahrung_jahre) AS vorhanden,
            COUNT(*) - COUNT(???) AS fehlend
        FROM gehaltsdaten
        GROUP BY ???
        ORDER BY fehlend DESC
        -- Tipp: erfahrung_jahre, abteilung
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    abteilung,
    COUNT(*) AS total,
    COUNT(erfahrung_jahre) AS vorhanden,
    COUNT(*) - COUNT(erfahrung_jahre) AS fehlend
FROM gehaltsdaten
GROUP BY abteilung
ORDER BY fehlend DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 4.3: Zeilen mit fehlenden Werten anzeigen (Selbstständig)

        Zeigen Sie alle Mitarbeiter, bei denen `erfahrung_jahre` NULL ist.

        *Hinweis: `WHERE erfahrung_jahre IS NULL`*
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Erwartete Spalten: mitarbeiter_id, name, abteilung, erfahrung_jahre
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT mitarbeiter_id, name, abteilung, erfahrung_jahre
FROM gehaltsdaten
WHERE erfahrung_jahre IS NULL
```
""")})
    return


# -----------------------------------------------------------------------
# Phase 5: Bivariate Analyse
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 5: Bivariate Analyse
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 5.1: Korrelation

        Berechnen Sie die Korrelation zwischen Alter und Gehalt (ohne Ausreißer).
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        SELECT
            ROUND(CORR(alter, gehalt), 3) AS korrelation_alter_gehalt,
            ROUND(CORR(erfahrung_jahre, gehalt), 3) AS korrelation_erfahrung_gehalt
        FROM gehaltsdaten
        WHERE alter < 100
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    ROUND(CORR(alter, gehalt), 3) AS korrelation_alter_gehalt,
    ROUND(CORR(erfahrung_jahre, gehalt), 3) AS korrelation_erfahrung_gehalt
FROM gehaltsdaten
WHERE alter < 100
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 5.2: Gruppenvergleich nach Geschlecht (Scaffolded)

        Vergleichen Sie das Durchschnittsgehalt nach Geschlecht. Ergänzen Sie `???`:
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        SELECT
            ???,
            COUNT(*) AS n,
            ROUND(AVG(gehalt), 0) AS mittel_gehalt,
            ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY gehalt), 0) AS median_gehalt
        FROM gehaltsdaten
        WHERE gehalt < 200000
        GROUP BY ???
        ORDER BY mittel_gehalt DESC
        -- Tipp: geschlecht
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    geschlecht,
    COUNT(*) AS n,
    ROUND(AVG(gehalt), 0) AS mittel_gehalt,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY gehalt), 0) AS median_gehalt
FROM gehaltsdaten
WHERE gehalt < 200000
GROUP BY geschlecht
ORDER BY mittel_gehalt DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 5.3: Kreuztabelle Standort × Geschlecht (Selbstständig)

        Berechnen Sie das Durchschnittsgehalt nach **Standort und Geschlecht** (ohne Ausreißer).

        *Hinweis: `GROUP BY standort, geschlecht`*
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Erwartete Spalten: standort, geschlecht, anzahl, durchschnitt_gehalt
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    standort,
    geschlecht,
    COUNT(*) AS anzahl,
    ROUND(AVG(gehalt), 0) AS durchschnitt_gehalt
FROM gehaltsdaten
WHERE gehalt < 200000
GROUP BY standort, geschlecht
ORDER BY standort, geschlecht
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 5.4: Gehalt mit Abteilungsdurchschnitt vergleichen (Selbstständig)

        Zeigen Sie für jeden Mitarbeiter sein Gehalt neben dem Durchschnitt seiner Abteilung. Nutzen Sie eine **Window Function**.

        *Hinweis: `AVG(gehalt) OVER (PARTITION BY abteilung)`*
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Erwartete Spalten: name, abteilung, gehalt, abteilung_avg, differenz
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    name,
    abteilung,
    gehalt,
    ROUND(AVG(gehalt) OVER (PARTITION BY abteilung), 0) AS abteilung_avg,
    gehalt - ROUND(AVG(gehalt) OVER (PARTITION BY abteilung), 0) AS differenz
FROM gehaltsdaten
WHERE gehalt < 200000
ORDER BY abteilung, differenz DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 5.5: Debugging — Fehlende GROUP BY bei Window + GROUP BY Mix

        Die folgende Abfrage soll die Varianz des Gehalts pro Abteilung zeigen. Sie hat einen Fehler!
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        -- 🔴 Diese Abfrage hat einen Fehler — finden und beheben Sie ihn!
        SELECT
            abteilung,
            ROUND(AVG(gehalt), 0) AS mittel,
            ROUND(STDDEV(gehalt), 0) AS std,
            ROUND(STDDEV(gehalt) / AVG(gehalt) * 100, 1) AS variationskoeffizient
        FROM gehaltsdaten
        WHERE gehalt < 200000
        ORDER BY variationskoeffizient DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**Problem:** `GROUP BY abteilung` fehlt! Ohne GROUP BY kann `abteilung` nicht neben Aggregatfunktionen stehen.

**Lösung:**
```sql
SELECT
    abteilung,
    ROUND(AVG(gehalt), 0) AS mittel,
    ROUND(STDDEV(gehalt), 0) AS std,
    ROUND(STDDEV(gehalt) / AVG(gehalt) * 100, 1) AS variationskoeffizient
FROM gehaltsdaten
WHERE gehalt < 200000
GROUP BY abteilung       -- ← das fehlte!
ORDER BY variationskoeffizient DESC
```
""")})
    return


# -----------------------------------------------------------------------
# Phase 6: Binning
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 6: Binning mit CASE WHEN
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 6.1: Gehaltsklassen erstellen

        Teilen Sie die Gehälter in Klassen ein.
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    _df = mo.sql(
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
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
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
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 6.2: Altersgruppen (Scaffolded)

        Erstellen Sie Altersgruppen und berechnen Sie das Durchschnittsgehalt pro Gruppe. Ergänzen Sie `???`:
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        SELECT
            CASE
                WHEN alter < 30 THEN ???
                WHEN alter < 40 THEN ???
                WHEN alter < 50 THEN ???
                ELSE ???
            END AS altersgruppe,
            COUNT(*) AS anzahl,
            ROUND(AVG(gehalt), 0) AS durchschnitt_gehalt
        FROM gehaltsdaten
        WHERE alter < 100 AND gehalt < 200000
        GROUP BY altersgruppe
        ORDER BY altersgruppe
        -- Tipp: '1: unter 30', '2: 30-40', '3: 40-50', '4: über 50'
        """
    )
    return


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
        ### 🔵 Aufgabe 6.3: Erfahrungsgruppen (Selbstständig)

        Erstellen Sie Erfahrungsgruppen (Junior: <5 Jahre, Mid: 5-15, Senior: 15-25, Expert: >25)
        und berechnen Sie Durchschnittsgehalt und Anzahl pro Gruppe.

        *Hinweis: Schließen Sie NULL-Werte aus (`WHERE erfahrung_jahre IS NOT NULL`)*
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Erwartete Spalten: erfahrungsgruppe, anzahl, durchschnitt_gehalt
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    CASE
        WHEN erfahrung_jahre < 5 THEN '1: Junior (<5)'
        WHEN erfahrung_jahre < 15 THEN '2: Mid (5-15)'
        WHEN erfahrung_jahre < 25 THEN '3: Senior (15-25)'
        ELSE '4: Expert (>25)'
    END AS erfahrungsgruppe,
    COUNT(*) AS anzahl,
    ROUND(AVG(gehalt), 0) AS durchschnitt_gehalt
FROM gehaltsdaten
WHERE erfahrung_jahre IS NOT NULL AND gehalt < 200000
GROUP BY erfahrungsgruppe
ORDER BY erfahrungsgruppe
```
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

        **Tipp:** Vergleichen Sie Ihre Analysen mit Ihrem Nachbarn — verschiedene EDA-Perspektiven ergänzen sich!
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐ Exploration 1: Gender Pay Gap Analyse

        Gibt es einen Gehaltsunterschied zwischen Geschlechtern? Unterscheidet sich der Gap nach Abteilung oder Standort?

        *Hinweis: `GROUP BY abteilung, geschlecht` + `AVG(gehalt)`, dann vergleichen*
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
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
    abteilung,
    ROUND(AVG(CASE WHEN geschlecht = 'M' THEN gehalt END), 0) AS avg_gehalt_m,
    ROUND(AVG(CASE WHEN geschlecht = 'W' THEN gehalt END), 0) AS avg_gehalt_w,
    ROUND(AVG(CASE WHEN geschlecht = 'M' THEN gehalt END)
        - AVG(CASE WHEN geschlecht = 'W' THEN gehalt END), 0) AS gap_absolut,
    ROUND((AVG(CASE WHEN geschlecht = 'M' THEN gehalt END)
         - AVG(CASE WHEN geschlecht = 'W' THEN gehalt END))
         * 100.0
         / AVG(CASE WHEN geschlecht = 'M' THEN gehalt END), 1) AS gap_prozent
FROM gehaltsdaten
WHERE gehalt < 200000
GROUP BY abteilung
ORDER BY gap_prozent DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐⭐ Exploration 2: Varianz nach Abteilung — Welche Abteilung streut am meisten?

        Berechnen Sie den **Variationskoeffizienten** (STDDEV/AVG × 100) für jede Abteilung.
        Welche Abteilung hat die homogensten Gehälter?
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
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
    abteilung,
    COUNT(*) AS n,
    ROUND(AVG(gehalt), 0) AS mittel,
    ROUND(STDDEV(gehalt), 0) AS std,
    ROUND(STDDEV(gehalt) / AVG(gehalt) * 100, 1) AS variationskoeffizient
FROM gehaltsdaten
WHERE gehalt < 200000
GROUP BY abteilung
ORDER BY variationskoeffizient ASC
```
Die Abteilung mit dem niedrigsten Variationskoeffizienten hat die homogensten Gehälter.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐⭐⭐ Exploration 3: Vollständiger EDA-Report

        Erstellen Sie einen EDA-Report: Finden Sie Gehälter, die mehr als 2 Standardabweichungen vom Durchschnitt **ihrer Abteilung** abweichen. Sind es immer die gleichen Abteilungen?

        *Hinweis: `AVG() + STDDEV()` als Window Function mit `PARTITION BY abteilung`*
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
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
WITH mit_stats AS (
    SELECT
        name,
        abteilung,
        gehalt,
        AVG(gehalt) OVER (PARTITION BY abteilung) AS abt_avg,
        STDDEV(gehalt) OVER (PARTITION BY abteilung) AS abt_std
    FROM gehaltsdaten
    WHERE gehalt < 200000 AND alter < 100
)
SELECT
    name,
    abteilung,
    gehalt,
    ROUND(abt_avg, 0) AS abt_durchschnitt,
    ROUND((gehalt - abt_avg) / abt_std, 2) AS z_score
FROM mit_stats
WHERE ABS((gehalt - abt_avg) / abt_std) > 2
ORDER BY ABS((gehalt - abt_avg) / abt_std) DESC
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

        ## ⭐ Analyse-Aufgabe: Team Performance-Profile

        Diese Aufgabe kombiniert mehrere EDA-Konzepte aus dieser Session:
        - Deskriptive Statistik (Mittelwert, Median, Standardabweichung)
        - Ausreißererkennung (IQR-Methode)
        - Binning (Kategorisierung)
        - Bivariate Analyse (Gruppenvergleiche)

        **Geschäftsfrage:** Wie lassen sich die Mitarbeiter-Gehälter nach Abteilung charakterisieren und vergleichen?

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐ Analyse: Vollständiges Abteilungs-Profil

        **Aufgabe:** Erstellen Sie ein vollständiges Profil für jede Abteilung:
        1. Grundstatistiken (n, Mittelwert, Median, Standardabweichung)
        2. Variationskoeffizient als Maß für die Homogenität
        3. Anteil der Ausreißer (per IQR-Methode)
        4. Klassifizierung: "Homogen" (VK < 20%), "Mittel" (20-30%), "Heterogen" (> 30%)

        Nutzen Sie CTEs, um die Analyse zu strukturieren.
        """
    )
    return


@app.cell
def _(gehaltsdaten, mo):
    # ⭐ Analyse-Aufgabe: Ihre Lösung
    _df = mo.sql(
        f"""
        -- Schreiben Sie Ihre Analyse-Abfrage hier
        -- Ziel: Vollständiges Abteilungs-Profil mit Klassifizierung
        SELECT 'Ihre Lösung hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
WITH abt_stats AS (
    SELECT
        abteilung,
        COUNT(*) AS n,
        ROUND(AVG(gehalt), 0) AS mittelwert,
        ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY gehalt), 0) AS median,
        ROUND(STDDEV(gehalt), 0) AS std,
        ROUND(STDDEV(gehalt) / AVG(gehalt) * 100, 1) AS variationskoeffizient,
        ROUND(PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY gehalt), 0) AS q1,
        ROUND(PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY gehalt), 0) AS q3
    FROM gehaltsdaten
    WHERE gehalt < 200000
    GROUP BY abteilung
),
klassifiziert AS (
    SELECT
        *,
        CASE
            WHEN variationskoeffizient < 20 THEN 'Homogen'
            WHEN variationskoeffizient < 30 THEN 'Mittel'
            ELSE 'Heterogen'
        END AS homogenitaet,
        q3 - q1 AS iqr
    FROM abt_stats
)
SELECT
    abteilung,
    n,
    mittelwert,
    median,
    std,
    variationskoeffizient || '%' AS vk,
    homogenitaet,
    ROUND(q1 - 1.5 * iqr, 0) AS ausreisser_grenze_unten,
    ROUND(q3 + 1.5 * iqr, 0) AS ausreisser_grenze_oben
FROM klassifiziert
ORDER BY variationskoeffizient
```

**Analyse-Erkenntnisse:**
- Zwei CTEs strukturieren die Analyse: erst Grundstatistiken, dann Klassifizierung
- Der Variationskoeffizient normalisiert die Streuung für den Vergleich
- Die Homogenitäts-Klassifizierung erleichtert die Interpretation
- IQR-Grenzen ermöglichen Ausreißer-Erkennung pro Abteilung

**Business Value:** Diese Analyse hilft bei:
- Identifikation von Abteilungen mit ungleichmäßiger Gehaltsstruktur
- Benchmarking zwischen Abteilungen
- Erkennung potenzieller Fairness-Probleme
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Zusammenfassung

        | Konzept | Aufgaben | Wann nutzen? |
        |---------|----------|--------------|
        | **Dateninspektion** | 1.1 – 1.4 | Immer zuerst: COUNT, Schema, LIMIT |
        | **Univariate Analyse** | 2.1 – 2.5 | Jede Variable einzeln beschreiben |
        | **Ausreißer (IQR)** | 3.1 – 3.4 | Extreme Werte und Datenfehler finden |
        | **Fehlende Werte** | 4.1 – 4.3 | NULL-Muster erkennen |
        | **Bivariate Analyse** | 5.1 – 5.5 | Zusammenhänge untersuchen |
        | **Binning** | 6.1 – 6.3 | Kategorien aus numerischen Werten |

        **Nächste Session:** Statistische Inferenz & A/B-Tests
        """
    )
    return


if __name__ == "__main__":
    app.run()
