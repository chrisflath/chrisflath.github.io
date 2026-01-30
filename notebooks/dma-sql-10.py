# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "polars",
#     "duckdb",
# ]
# ///

import marimo

__generated_with = "0.10.14"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Vorlesung 10: Subqueries, Views & Transaktionen

        **Lernziele:**
        - Komplexe Abfragen mit Subqueries strukturieren
        - CTEs (WITH) für lesbare Abfragen nutzen
        - Views als wiederverwendbare Abfragen erstellen
        - ACID-Eigenschaften und Transaktionen verstehen
        """
    )
    return


@app.cell
def _():
    import marimo as mo
    import polars as pl
    return mo, pl


@app.cell(hide_code=True)
def _(mo, pl):
    # Bundesliga-Daten laden
    csv_path = mo.notebook_location() / "public" / "bundesliga.csv"
    bundesliga = pl.read_csv(str(csv_path))

    # Zusätzliche Tabellen für Übungen erstellen
    # Pokal-Halbfinalisten (fiktiv)
    pokal_halbfinale = pl.DataFrame({
        "team": ["Bayern München", "Bayer Leverkusen", "VfB Stuttgart", "RB Leipzig"]
    })

    # Konten-Tabelle für Transaktions-Demo
    konten = pl.DataFrame({
        "konto_id": ["A", "B", "C"],
        "inhaber": ["Alice", "Bob", "Charlie"],
        "saldo": [1000.0, 500.0, 750.0]
    })

    daten_quelle = "Bundesliga Saison 2024/25"
    return bundesliga, daten_quelle, konten, pokal_halbfinale


@app.cell(hide_code=True)
def _(daten_quelle, mo):
    mo.md(
        f"""
        **Datenquelle:** {daten_quelle}

        **Verfügbare Tabellen:**
        - `bundesliga` – Aktuelle Tabelle (18 Teams)
        - `pokal_halbfinale` – Teams im DFB-Pokal Halbfinale
        - `konten` – Bankkonten für Transaktions-Übungen

        ---

        ## Phase 1: Subqueries – Grundlagen

        Eine **Subquery** ist eine Abfrage innerhalb einer anderen Abfrage.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Subquery-Typen

        | Typ | Rückgabe | Beispiel-Kontext |
        |-----|----------|------------------|
        | **Scalar** | 1 Wert | `SELECT spalte - (SELECT AVG(...))` |
        | **Column** | 1 Spalte | `WHERE spalte IN (SELECT ...)` |
        | **Table** | Tabelle | `FROM (SELECT ...) AS t` |
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 10.1: Scalar Subquery

        Zeige alle Teams mit ihren Punkten und der **Differenz zum Durchschnitt**.
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    mo.sql(
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 10.2: Column Subquery mit IN

        Zeige nur die Teams, die im **Pokal-Halbfinale** stehen.
        """
    )
    return


@app.cell
def _(bundesliga, mo, pokal_halbfinale):
    mo.sql(
        f"""
        SELECT Mannschaft, Punkte, Tordifferenz
        FROM bundesliga
        WHERE Mannschaft IN (
            SELECT team FROM pokal_halbfinale
        )
        ORDER BY Punkte DESC
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 10.3: Selbstständig – Teams über dem Durchschnitt

        Finde alle Teams mit **mehr Punkten als der Durchschnitt**.

        *Hinweis: Nutze eine Scalar Subquery in der WHERE-Klausel.*
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Deine Lösung hier:
    mo.sql(
        f"""
        SELECT Mannschaft, Punkte
        FROM bundesliga
        WHERE Punkte > (SELECT AVG(Punkte) FROM bundesliga)
        ORDER BY Punkte DESC
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 2: Common Table Expressions (CTEs)

        CTEs machen komplexe Abfragen **lesbar** durch benannte Zwischenergebnisse.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### CTE Syntax

        ```sql
        WITH cte_name AS (
            SELECT ...
        )
        SELECT ... FROM cte_name ...
        ```
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 10.4: CTE für Durchschnitt

        Berechne den Durchschnitt einmal und verwende ihn mehrfach.
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    mo.sql(
        f"""
        WITH statistiken AS (
            SELECT
                AVG(Punkte) AS avg_punkte,
                AVG(ToreGeschossen) AS avg_tore
            FROM bundesliga
        )
        SELECT
            b.Mannschaft,
            b.Punkte,
            ROUND(s.avg_punkte, 1) AS Liga_Schnitt,
            b.Punkte - s.avg_punkte AS Punkte_Diff,
            b.ToreGeschossen,
            ROUND(s.avg_tore, 1) AS Tore_Schnitt,
            b.ToreGeschossen - s.avg_tore AS Tore_Diff
        FROM bundesliga b, statistiken s
        ORDER BY b.Punkte DESC
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 10.5: Mehrere CTEs verketten

        1. Filtere Top-Teams (> 50 Punkte)
        2. Berechne Siegquote für diese Teams
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    mo.sql(
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 3: Views – Virtuelle Tabellen

        Ein **View** ist eine gespeicherte Abfrage, die sich wie eine Tabelle verhält.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 10.6: View erstellen

        Erstelle einen View für Team-Statistiken mit berechneten Spalten.
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    mo.sql(
        f"""
        CREATE OR REPLACE VIEW team_statistik AS
        SELECT
            Mannschaft,
            Punkte,
            Siege,
            Unentschieden,
            Niederlagen,
            ToreGeschossen,
            ToreKassiert,
            Tordifferenz,
            ROUND(CAST(Siege AS FLOAT) / Spiele * 100, 1) AS Siegquote,
            ROUND(CAST(ToreGeschossen AS FLOAT) / Spiele, 2) AS Tore_pro_Spiel
        FROM bundesliga
        """
    )


@app.cell
def _(mo):
    # View verwenden wie eine normale Tabelle
    mo.sql(
        f"""
        SELECT Mannschaft, Siegquote, Tore_pro_Spiel
        FROM team_statistik
        WHERE Siegquote > 50
        ORDER BY Siegquote DESC
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 10.7: Selbstständig – View für Kellerkinder

        Erstelle einen View `abstiegskandidaten` mit Teams auf den letzten 6 Plätzen.

        *Hinweis: Sortiere nach Punkten und nutze LIMIT.*
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Deine Lösung hier:
    mo.sql(
        f"""
        CREATE OR REPLACE VIEW abstiegskandidaten AS
        SELECT Mannschaft, Punkte, Tordifferenz
        FROM bundesliga
        ORDER BY Punkte ASC, Tordifferenz ASC
        LIMIT 6
        """
    )


@app.cell
def _(mo):
    # Prüfe deinen View
    mo.sql(
        f"""
        SELECT * FROM abstiegskandidaten
        """
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 4: Transaktionen

        Transaktionen garantieren **ACID-Eigenschaften** bei Datenänderungen.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### ACID-Eigenschaften

        | Eigenschaft | Bedeutung |
        |-------------|-----------|
        | **A**tomicity | Alles oder nichts |
        | **C**onsistency | Datenbank bleibt konsistent |
        | **I**solation | Parallele Transaktionen stören sich nicht |
        | **D**urability | Bestätigte Änderungen sind permanent |
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 10.8: Überweisung simulieren

        Simuliere eine Überweisung von Konto A nach Konto B.
        """
    )
    return


@app.cell
def _(konten, mo):
    # Ausgangszustand
    mo.sql(
        f"""
        SELECT * FROM konten
        """
    )


@app.cell
def _(mo):
    mo.md(
        r"""
        **Transaktion: 100€ von Alice (A) nach Bob (B)**

        In einer echten Datenbank würden wir schreiben:
        ```sql
        BEGIN TRANSACTION;

        UPDATE konten SET saldo = saldo - 100 WHERE konto_id = 'A';
        UPDATE konten SET saldo = saldo + 100 WHERE konto_id = 'B';

        COMMIT;
        ```

        **Wichtig:** Bei Fehler würde ROLLBACK alles rückgängig machen.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Concurrency-Probleme

        | Problem | Beschreibung |
        |---------|--------------|
        | **Lost Update** | Zwei Transaktionen überschreiben sich |
        | **Dirty Read** | Lesen von nicht-committeten Daten |
        | **Non-Repeatable Read** | Gleiche Abfrage, verschiedene Ergebnisse |
        | **Phantom Read** | Neue Zeilen erscheinen zwischen Abfragen |
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Zusammenfassung

        | Konzept | Wann nutzen? |
        |---------|--------------|
        | **Subquery** | Einfache einmalige Berechnungen |
        | **CTE (WITH)** | Komplexe Abfragen strukturieren |
        | **View** | Wiederverwendbare, persistente Abfragen |
        | **Transaktion** | Zusammengehörige Änderungen absichern |

        ### Entscheidungsbaum

        ```
        Einmalige Abfrage?
        ├── Ja → Komplex? → Ja: CTE / Nein: Subquery
        └── Nein → View
        ```
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Freie Exploration

        Probieren Sie eigene Abfragen:

        - Erstellen Sie einen View für "Titelkandidaten" (Top 4)
        - Nutzen Sie CTEs um Teams mit überdurchschnittlichen Heim- UND Auswärtsbilanzen zu finden
        - Experimentieren Sie mit korrelierten Subqueries
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Ihre eigene Abfrage hier:
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte
        FROM bundesliga
        LIMIT 5
        """
    )
    return


if __name__ == "__main__":
    app.run()
