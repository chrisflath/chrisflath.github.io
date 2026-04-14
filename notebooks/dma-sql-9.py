# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "polars",
#     "plotly",
# ]
# ///

import marimo

__generated_with = "0.13.0"
app = marimo.App(
    width="medium",
    app_title="DMA Session 9: Subqueries, Views & Transaktionen — Übungen",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 9: Subqueries, Views & Transaktionen — Übungen

        Theorie und geführte Beispiele → **09-subqueries-views-transaktionen-guide.py**

        **Aufgabentypen:**

        - 🟡 **Scaffolded**: Teillösung zum Ergänzen
        - 🔵 **Selbstständig**: Eigene Lösung schreiben
        - 🔴 **Debugging**: Fehler finden und beheben
        - ⭐ **Exploration**: Offene Herausforderungen

        > **Hinweis:** 🟡-Aufgaben enthalten `???` als Platzhalter. Die Zelle zeigt einen SQL-Fehler, bis Sie die `???` durch die richtige Lösung ersetzen — das ist Absicht!
        """
    )
    return


@app.cell
def _(mo):
    import polars as pl
    import plotly.express as px

    try:
        import pathlib
        csv_path = pathlib.Path(__file__).parent / "public" / "bundesliga.csv"
        bundesliga = pl.read_csv(str(csv_path))
    except Exception:
        bundesliga = pl.DataFrame({
            "Mannschaft": [
                "Bayern München", "Bayer Leverkusen", "VfB Stuttgart",
                "Borussia Dortmund", "RB Leipzig", "Eintracht Frankfurt",
                "SC Freiburg", "TSG Hoffenheim", "Werder Bremen", "VfL Wolfsburg",
                "1. FC Union Berlin", "FC Augsburg", "Borussia M'gladbach",
                "1. FSV Mainz 05", "1. FC Heidenheim", "VfL Bochum",
                "FC St. Pauli", "Holstein Kiel",
            ],
            "Spiele": [34] * 18,
            "Siege": [25, 22, 18, 17, 16, 14, 13, 13, 10, 9, 9, 8, 8, 7, 7, 5, 5, 4],
            "Unentschieden": [4, 6, 5, 6, 7, 8, 6, 5, 8, 9, 7, 7, 5, 8, 6, 7, 5, 4],
            "Niederlagen": [5, 6, 11, 11, 11, 12, 15, 16, 16, 16, 18, 19, 21, 19, 21, 22, 24, 26],
            "Tore": [85, 72, 60, 62, 56, 48, 42, 50, 38, 40, 30, 28, 36, 32, 36, 24, 20, 24],
            "Gegentore": [32, 30, 45, 42, 40, 42, 52, 55, 48, 50, 50, 58, 62, 48, 62, 65, 52, 72],
            "Tordifferenz": [53, 42, 15, 20, 16, 6, -10, -5, -10, -10, -20, -30, -26, -16, -26, -41, -32, -48],
            "Punkte": [79, 72, 59, 57, 55, 50, 45, 44, 38, 36, 34, 31, 29, 29, 27, 22, 20, 16],
        })

    pokal_halbfinale = pl.DataFrame({
        "team": ["Bayern München", "Bayer Leverkusen", "VfB Stuttgart", "RB Leipzig"]
    })

    konten = pl.DataFrame({
        "konto_id": ["A", "B", "C"],
        "inhaber": ["Alice", "Bob", "Charlie"],
        "saldo": [1000.0, 500.0, 750.0],
    })

    return bundesliga, konten, pl, pokal_halbfinale, px


# -----------------------------------------------------------------------
# Phase 2: Subqueries
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 2: Subqueries
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 2.1: Scalar Subquery — Punkte vs. Durchschnitt

        Zeigen Sie alle Teams mit ihren Punkten und der **Differenz zum Liga-Durchschnitt**.
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT
            Mannschaft,
            Punkte,
            (SELECT AVG(Punkte) FROM bundesliga) AS Liga_Durchschnitt,
            Punkte - (SELECT AVG(Punkte) FROM bundesliga) AS Differenz
        FROM bundesliga
        ORDER BY Punkte DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 2.2: Column Subquery mit IN — Teams im Pokal

        Zeigen Sie nur die Teams, die im **Pokal-Halbfinale** stehen.
        """
    )
    return


@app.cell
def _(bundesliga, mo, pokal_halbfinale):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte, Tordifferenz
        FROM bundesliga
        WHERE Mannschaft IN (
            SELECT team FROM pokal_halbfinale
        )
        ORDER BY Punkte DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 2.3: Subquery mit AVG (Scaffolded)

        Finden Sie alle Teams mit **mehr Toren als der Liga-Durchschnitt**.
        Ergänzen Sie die fehlenden Teile (`???`):
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Tore
        FROM bundesliga
        WHERE Tore > (
            SELECT ???(???)
            FROM ???
        )
        ORDER BY Tore DESC
        -- Tipp: AVG(Tore) FROM bundesliga
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT Mannschaft, Tore
FROM bundesliga
WHERE Tore > (
    SELECT AVG(Tore)
    FROM bundesliga
)
ORDER BY Tore DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 2.4: Teams über dem Punktedurchschnitt (Selbstständig)

        Finden Sie alle Teams mit **mehr Punkten als der Liga-Durchschnitt**.

        *Hinweis: Nutzen Sie eine Scalar Subquery in der WHERE-Klausel.*
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Ihre Lösung hier:
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: WHERE Punkte > (SELECT AVG(Punkte) FROM bundesliga)
        -- Erwartete Spalten: Mannschaft, Punkte
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS Hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT Mannschaft, Punkte
FROM bundesliga
WHERE Punkte > (
    SELECT AVG(Punkte)
    FROM bundesliga
)
ORDER BY Punkte DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 2.5: Weniger Gegentore als der Durchschnitt (Selbstständig)

        Finden Sie alle Teams mit **weniger Gegentoren als der Liga-Durchschnitt**.

        *Hinweis: `WHERE Gegentore < (SELECT AVG(Gegentore) ...)`*
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Ihre Lösung hier:
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: WHERE Gegentore < (SELECT AVG(Gegentore) FROM bundesliga)
        -- Erwartete Spalten: Mannschaft, Gegentore
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS Hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT Mannschaft, Gegentore
FROM bundesliga
WHERE Gegentore < (
    SELECT AVG(Gegentore)
    FROM bundesliga
)
ORDER BY Gegentore ASC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 2.6: Debugging — Scalar Subquery liefert mehrere Zeilen

        Die folgende Abfrage hat einen Fehler. Finden und beheben Sie ihn!
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        -- 🔴 Diese Abfrage hat einen Fehler — finden und beheben Sie ihn!
        SELECT Mannschaft, Punkte
        FROM bundesliga
        WHERE Punkte = (
            SELECT Punkte FROM bundesliga WHERE Siege > 15
        )
        ORDER BY Punkte DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**Problem:** Die Subquery gibt **mehrere Zeilen** zurück (alle Teams mit > 15 Siegen),
aber der `=`-Operator erwartet genau **einen** Wert.

**Lösung:** Verwenden Sie `IN` statt `=`, oder schränken Sie die Subquery mit `LIMIT 1` ein:

```sql
-- Variante 1: IN statt =
SELECT Mannschaft, Punkte
FROM bundesliga
WHERE Punkte IN (
    SELECT Punkte FROM bundesliga WHERE Siege > 15
)
ORDER BY Punkte DESC

-- Variante 2: LIMIT 1 (z.B. Maximum)
SELECT Mannschaft, Punkte
FROM bundesliga
WHERE Punkte = (
    SELECT MAX(Punkte) FROM bundesliga WHERE Siege > 15
)
```
""")})
    return


# -----------------------------------------------------------------------
# Phase 4: Common Table Expressions (CTEs)
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 4: Common Table Expressions (CTEs)
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 4.1: CTE für Durchschnitt

        Berechnen Sie den Durchschnitt **einmal** und verwenden Sie ihn mehrfach.
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        WITH statistiken AS (
            SELECT
                AVG(Punkte) AS avg_punkte,
                AVG(Tore) AS avg_tore
            FROM bundesliga
        )
        SELECT
            b.Mannschaft,
            b.Punkte,
            ROUND(s.avg_punkte, 1) AS Liga_Schnitt,
            b.Punkte - s.avg_punkte AS Punkte_Diff,
            b.Tore,
            ROUND(s.avg_tore, 1) AS Tore_Schnitt,
            b.Tore - s.avg_tore AS Tore_Diff
        FROM bundesliga b, statistiken s
        ORDER BY b.Punkte DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 4.2: Mehrere CTEs verketten

        1. Filtern Sie die Top-Teams (> 50 Punkte)
        2. Berechnen Sie die Siegquote für diese Teams
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        WITH
        top_teams AS (
            SELECT Mannschaft, Punkte, Siege, Spiele
            FROM bundesliga
            WHERE Punkte > 50
        ),
        mit_quote AS (
            SELECT
                Mannschaft,
                Punkte,
                Siege,
                Spiele,
                ROUND(CAST(Siege AS FLOAT) / Spiele * 100, 1) AS Siegquote
            FROM top_teams
        )
        SELECT * FROM mit_quote
        ORDER BY Siegquote DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 4.3: CTE mit CASE WHEN — Leistungsgruppen (Scaffolded)

        Teilen Sie die Teams in Leistungsgruppen ein und berechnen Sie Gruppenstatistiken.
        Ergänzen Sie die fehlenden Teile (`???`):
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        WITH leistung AS (
            SELECT
                Mannschaft, Punkte,
                CASE
                    WHEN Punkte >= 60 THEN ???
                    WHEN Punkte >= 40 THEN ???
                    ELSE ???
                END AS Gruppe
            FROM bundesliga
        )
        SELECT Gruppe, COUNT(*) AS Anzahl, ROUND(AVG(Punkte), 1) AS Schnitt_Punkte
        FROM leistung
        GROUP BY Gruppe
        ORDER BY Schnitt_Punkte DESC
        -- Tipp: 'Top', 'Mitte', 'Unten'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
WITH leistung AS (
    SELECT
        Mannschaft, Punkte,
        CASE
            WHEN Punkte >= 60 THEN 'Top'
            WHEN Punkte >= 40 THEN 'Mitte'
            ELSE 'Unten'
        END AS Gruppe
    FROM bundesliga
)
SELECT Gruppe, COUNT(*) AS Anzahl, ROUND(AVG(Punkte), 1) AS Schnitt_Punkte
FROM leistung
GROUP BY Gruppe
ORDER BY Schnitt_Punkte DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 4.4: Tordifferenz-Rangliste Top 5 per CTE (Selbstständig)

        Erstellen Sie eine CTE, die die **Top 5 Teams nach Tordifferenz** ermittelt,
        und geben Sie Mannschaft, Tordifferenz und Punkte aus.

        *Hinweis: `WITH top_td AS (SELECT ... ORDER BY Tordifferenz DESC LIMIT 5)`*
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Ihre Lösung hier:
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: WITH top_td AS (SELECT Mannschaft, Tordifferenz, Punkte FROM bundesliga ORDER BY Tordifferenz DESC LIMIT 5)
        -- dann: SELECT * FROM top_td
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS Hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
WITH top_td AS (
    SELECT Mannschaft, Tordifferenz, Punkte
    FROM bundesliga
    ORDER BY Tordifferenz DESC
    LIMIT 5
)
SELECT * FROM top_td
ORDER BY Tordifferenz DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 4.5: Debugging — CTE definiert, aber nicht verwendet

        Die folgende Abfrage definiert eine CTE, nutzt sie aber nicht. Finden Sie den Fehler!
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        -- 🔴 Diese Abfrage definiert eine CTE, nutzt sie aber nicht!
        WITH top_teams AS (
            SELECT Mannschaft, Punkte
            FROM bundesliga
            WHERE Punkte > 50
        )
        SELECT * FROM bundesliga
        ORDER BY Punkte DESC
        LIMIT 5
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**Problem:** Die CTE `top_teams` wird definiert, aber im `SELECT` wird direkt
aus `bundesliga` gelesen — die CTE wird ignoriert!

**Lösung:** Lesen Sie aus der CTE statt aus der Originaltabelle:

```sql
WITH top_teams AS (
    SELECT Mannschaft, Punkte
    FROM bundesliga
    WHERE Punkte > 50
)
SELECT * FROM top_teams
ORDER BY Punkte DESC
```
""")})
    return


# -----------------------------------------------------------------------
# Phase 6: Views
# -----------------------------------------------------------------------


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 6: Views
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 6.1: View erstellen — team_statistik

        Erstellen Sie einen View mit berechneten Spalten (Siegquote, Tore pro Spiel).
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE VIEW team_statistik AS
        SELECT
            Mannschaft,
            Punkte,
            Siege,
            Unentschieden,
            Niederlagen,
            Tore,
            Gegentore,
            Tordifferenz,
            ROUND(CAST(Siege AS FLOAT) / Spiele * 100, 1) AS Siegquote,
            ROUND(CAST(Tore AS FLOAT) / Spiele, 2) AS Tore_pro_Spiel
        FROM bundesliga
        """
    )
    return


@app.cell
def _(mo):
    # View verwenden wie eine normale Tabelle
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Siegquote, Tore_pro_Spiel
        FROM team_statistik
        WHERE Siegquote > 50
        ORDER BY Siegquote DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 6.2: Titelkandidaten-View (Scaffolded)

        Erstellen Sie einen View `titelkandidaten` mit den **Top 4 Teams** nach Punkten.
        Ergänzen Sie die fehlenden Teile (`???`):
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE VIEW titelkandidaten AS
        SELECT Mannschaft, Punkte, Tordifferenz
        FROM bundesliga
        ORDER BY ??? DESC
        LIMIT ???
        -- Tipp: Punkte, 4
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
CREATE OR REPLACE VIEW titelkandidaten AS
SELECT Mannschaft, Punkte, Tordifferenz
FROM bundesliga
ORDER BY Punkte DESC
LIMIT 4
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 6.3: Abstiegskandidaten-View (Selbstständig)

        Erstellen Sie einen View `abstiegskandidaten` mit den Teams auf den **letzten 6 Plätzen**.

        *Hinweis: Sortieren Sie nach Punkten aufsteigend und nutzen Sie LIMIT.*
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Ihre Lösung hier:
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: CREATE OR REPLACE VIEW abstiegskandidaten AS
        --       SELECT Mannschaft, Punkte, Tordifferenz FROM bundesliga
        --       ORDER BY Punkte ASC LIMIT 6
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS Hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
CREATE OR REPLACE VIEW abstiegskandidaten AS
SELECT Mannschaft, Punkte, Tordifferenz
FROM bundesliga
ORDER BY Punkte ASC
LIMIT 6
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 6.4: View offensive_teams (Selbstständig)

        Erstellen Sie einen View `offensive_teams` mit allen Teams,
        die **mehr Tore geschossen als kassiert** haben.

        *Hinweis: `WHERE Tore > Gegentore`*
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Ihre Lösung hier:
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: CREATE OR REPLACE VIEW offensive_teams AS
        --       SELECT Mannschaft, Tore, Gegentore,
        --              ROUND(CAST(Tore AS FLOAT) / Spiele, 2) AS Tore_pro_Spiel,
        --              ROUND(CAST(Gegentore AS FLOAT) / Spiele, 2) AS Gegentore_pro_Spiel
        --       FROM bundesliga WHERE Tore > Gegentore
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS Hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
CREATE OR REPLACE VIEW offensive_teams AS
SELECT
    Mannschaft,
    Tore,
    Gegentore,
    ROUND(CAST(Tore AS FLOAT) / Spiele, 2) AS Tore_pro_Spiel,
    ROUND(CAST(Gegentore AS FLOAT) / Spiele, 2) AS Gegentore_pro_Spiel
FROM bundesliga
WHERE Tore > Gegentore
ORDER BY Tore DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 6.5: Debugging — Falscher Spaltenname

        Die folgende Abfrage hat einen Fehler. Finden und beheben Sie ihn!
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        -- 🔴 Diese Abfrage hat einen Fehler — finden und beheben Sie ihn!
        SELECT Name, Punkte
        FROM bundesliga
        ORDER BY Punkte DESC
        LIMIT 5
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**Problem:** Die Spalte heißt `Mannschaft`, nicht `Name`!

**Lösung:**
```sql
SELECT Mannschaft, Punkte
FROM bundesliga
ORDER BY Punkte DESC
LIMIT 5
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

        **Tipp:** Vergleichen Sie Ihre Lösungen mit Ihrem Nachbarn — es gibt oft mehrere Wege zum gleichen Ergebnis!
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐ Exploration 1: View für Teams mit Siegquote > 50 %

        Erstellen Sie einen View `starke_teams`, der alle Teams mit einer
        Siegquote über 50 % enthält.
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Ihre Lösung hier:
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS Hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
CREATE OR REPLACE VIEW starke_teams AS
SELECT
    Mannschaft,
    Siege,
    Spiele,
    ROUND(CAST(Siege AS FLOAT) / Spiele * 100, 1) AS Siegquote
FROM bundesliga
WHERE CAST(Siege AS FLOAT) / Spiele > 0.5
ORDER BY Siegquote DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐⭐ Exploration 2: Korrelierte Subquery — Nächstplatzierter Verein

        Finden Sie für jedes Team den **nächstplatzierten Verein** (das Team mit den
        nächstniedrigeren Punkten). Nutzen Sie eine korrelierte Subquery.

        *Hinweis: Für jede Zeile suchen Sie das Maximum der Punkte, die kleiner als
        die eigenen Punkte sind.*
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Ihre Lösung hier:
    _df = mo.sql(
        f"""
        -- Ihre Lösung hier
        -- Tipp: Korrelierte Subquery in SELECT
        SELECT 'Schreiben Sie Ihre Abfrage hier' AS Hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    b1.Mannschaft,
    b1.Punkte,
    (
        SELECT b2.Mannschaft
        FROM bundesliga b2
        WHERE b2.Punkte < b1.Punkte
        ORDER BY b2.Punkte DESC
        LIMIT 1
    ) AS Naechstplatzierter,
    (
        SELECT MAX(b2.Punkte)
        FROM bundesliga b2
        WHERE b2.Punkte < b1.Punkte
    ) AS Punkte_dahinter,
    b1.Punkte - (
        SELECT MAX(b2.Punkte)
        FROM bundesliga b2
        WHERE b2.Punkte < b1.Punkte
    ) AS Abstand
FROM bundesliga b1
ORDER BY b1.Punkte DESC
```

**Erklärung:** Die Subquery ist *korreliert*, weil sie sich auf `b1.Punkte` aus der
äußeren Abfrage bezieht. Für jede Zeile wird die Subquery erneut ausgewertet.
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐⭐⭐ Exploration 3: Lost-Update-Problem simulieren

        Die Tabelle `konten` enthält drei Bankkonten. Stellen Sie sich vor, zwei
        Transaktionen laufen **gleichzeitig** ab:

        - **Transaktion 1:** Überweise 100 € von Alice (A) nach Bob (B)
        - **Transaktion 2:** Überweise 50 € von Alice (A) nach Charlie (C)

        Ohne Isolation kann ein **Lost Update** auftreten. Beschreiben Sie das Problem
        konzeptionell und zeigen Sie den Ausgangszustand der Konten.
        """
    )
    return


@app.cell
def _(konten, mo):
    # Ausgangszustand anzeigen
    _df = mo.sql(
        f"""
        -- Ausgangszustand der Konten
        SELECT * FROM konten
        """
    )
    return


@app.cell
def _(mo):
    # Ihre Analyse hier:
    _df = mo.sql(
        f"""
        -- Versuchen Sie, den Ablauf konzeptionell nachzuvollziehen:
        -- T1 liest Saldo A = 1000
        -- T2 liest Saldo A = 1000
        -- T1 schreibt Saldo A = 1000 - 100 = 900
        -- T2 schreibt Saldo A = 1000 - 50  = 950  ← überschreibt T1!
        -- Ergebnis: Alice hat 950 statt korrekter 850
        SELECT 'Schreiben Sie Ihre Analyse hier' AS Hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## 🎓 Übungsklausur: Transaktions-Serialisierbarkeit

        In der Klausur werden Sie häufiger auf Aufgaben zur Serialisierbarkeit treffen. Hier ist ein typisches Beispiel aus einer vergangenen Klausur.

        Gegeben sei folgende Historie von drei Transaktionen ($T_1, T_2, T_3$).

        | Schritt | $T_1$ | $T_2$ | $T_3$ |
        |---|---|---|---|
        | 1 | | `read(x)` | |
        | 2 | | `write(x)` | |
        | 3 | `read(y)` | | |
        | 4 | | `read(y)` | |
        | 5 | | | `write(y)` |
        | 6 | `write(y)` | | |
        | 7 | | | `read(y)` |

        **Aufgabe:**
        1. Zeichnen Sie (mental oder auf Papier) den Präzedenzgraphen.
        2. Bestimmen Sie, ob die Historie **konfliktserialisierbar** ist.
        3. Identifizieren Sie ggf. den Konfliktzyklus.
        """
    )
    return


@app.cell
def _(mo):
    # Tragen Sie Ihre Analyse hier ein
    mo.md(
        """
        **Ihre Antwort:**

        - Konflikte:
          - ...
        - Präzedenzgraph Kanten:
          - ...
        - Zyklus vorhanden?
        - Serialisierbar?
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Lösung": mo.md("""
**Konfliktanalyse:**
Wir suchen nach Konfliktpaaren (R-W, W-R, W-W) auf demselben Objekt zwischen verschiedenen Transaktionen:

1. **Konflikt auf y:**
   - Schritt 4: $T_2$ `read(y)`
   - Schritt 5: $T_3$ `write(y)`
   - **Kante:** $T_2 \to T_3$

2. **Konflikt auf y:**
   - Schritt 3: $T_1$ `read(y)`
   - Schritt 5: $T_3$ `write(y)`
   - **Kante:** $T_1 \to T_3$

3. **Konflikt auf y:**
   - Schritt 5: $T_3$ `write(y)`
   - Schritt 6: $T_1$ `write(y)`
   - **Kante:** $T_3 \to T_1$

**Präzedenzgraph:**
- $T_2 \to T_3$
- $T_1 \to T_3$
- $T_3 \to T_1$

**Ergebnis:**
- Wir haben einen Zyklus: $T_1 \to T_3 \to T_1$.
- Die Historie ist **NICHT konfliktserialisierbar**.
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

        ## ⭐ Analyse-Aufgabe: Teams über dem Liga-Durchschnitt

        Diese Aufgabe kombiniert mehrere Konzepte aus dieser Session:
        - CTEs für strukturierte Berechnungen
        - Aggregation (AVG, Vergleiche)
        - Subqueries für dynamische Schwellenwerte

        **Geschäftsfrage:** Welche Teams performen besser als der Liga-Durchschnitt — und wie weit?

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ⭐ Analyse: Teams über Durchschnitt mit Abweichung

        **Aufgabe:** Erstellen Sie eine Analyse, die zeigt:
        1. Alle Teams mit mehr Punkten als der Liga-Durchschnitt
        2. Den Liga-Durchschnitt als Referenzwert
        3. Die Abweichung vom Durchschnitt (absolut und prozentual)
        4. Eine Klassifizierung: "Deutlich über" (>20%), "Über" (>0%), oder "Im Durchschnitt"

        Nutzen Sie CTEs, um die Berechnung zu strukturieren.
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # ⭐ Analyse-Aufgabe: Ihre Lösung
    _df = mo.sql(
        f"""
        -- Schreiben Sie Ihre Analyse-Abfrage hier
        -- Ziel: Teams über dem Durchschnitt mit Klassifizierung
        SELECT 'Ihre Lösung hier' AS hinweis
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
WITH liga_stats AS (
    SELECT
        AVG(Punkte) AS avg_punkte,
        AVG(Tore) AS avg_tore,
        AVG(Tordifferenz) AS avg_td
    FROM bundesliga
),
teams_bewertet AS (
    SELECT
        b.Mannschaft,
        b.Punkte,
        ROUND(l.avg_punkte, 1) AS Liga_Schnitt,
        b.Punkte - l.avg_punkte AS Abweichung_Absolut,
        ROUND((b.Punkte - l.avg_punkte) / l.avg_punkte * 100, 1) AS Abweichung_Prozent,
        CASE
            WHEN (b.Punkte - l.avg_punkte) / l.avg_punkte > 0.20 THEN 'Deutlich über Durchschnitt'
            WHEN b.Punkte > l.avg_punkte THEN 'Über Durchschnitt'
            ELSE 'Im Durchschnitt oder darunter'
        END AS Klassifizierung
    FROM bundesliga b, liga_stats l
)
SELECT *
FROM teams_bewertet
WHERE Abweichung_Absolut > 0
ORDER BY Abweichung_Prozent DESC
```

**Analyse-Erkenntnisse:**
- Zwei CTEs strukturieren die Berechnung: erst Liga-Statistiken, dann Team-Bewertung
- Die prozentuale Abweichung normalisiert den Vergleich
- CASE WHEN klassifiziert in verständliche Kategorien
- Diese Struktur ist leicht erweiterbar (z.B. für Tore, Tordifferenz)

**Business Value:** Diese Analyse hilft bei:
- Identifikation von Überperformern
- Benchmarking gegen Liga-Durchschnitt
- Reporting für Stakeholder
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Zusammenfassung

        | Konzept | Wann nutzen? | Aufgaben |
        |---------|--------------|----------|
        | **Subquery** | Einfache einmalige Berechnungen | 2.1 – 2.6 |
        | **CTE (WITH)** | Komplexe Abfragen strukturieren | 4.1 – 4.5 |
        | **View** | Wiederverwendbare, persistente Abfragen | 6.1 – 6.5 |
        | **Transaktion** | Zusammengehörige Änderungen absichern | Exploration 3 |

        ### Entscheidungsbaum

        ```
        Einmalige Abfrage?
        ├── Ja → Komplex? → Ja: CTE / Nein: Subquery
        └── Nein → View
        ```

        **Nächste Session:** Explorative Datenanalyse (EDA)
        """
    )
    return


if __name__ == "__main__":
    app.run()
