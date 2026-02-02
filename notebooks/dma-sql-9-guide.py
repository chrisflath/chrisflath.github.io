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
    app_title="DMA Session 9: Subqueries, Views & Transaktionen — Guide",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    import polars as pl

    try:
        csv_path = mo.notebook_location() / "public" / "bundesliga.csv"
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

    return bundesliga, konten, pl, pokal_halbfinale


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 9: Subqueries, Views & Transaktionen — Guide

        **Kursfahrplan:** I: SQL-Grundlagen (S1–4) · II: Datenmodellierung (S5–7) · **▸ III: Fortgeschrittenes SQL (S8–9)** · IV: Datenanalyse (S10–13)

        ### Lernziele

        Nach dieser Session können Sie:

        - **Scalar/Column/Table Subqueries** unterscheiden und anwenden
        - **CTEs** (Common Table Expressions) für lesbare Abfragen nutzen
        - **Views** als wiederverwendbare virtuelle Tabellen erstellen
        - **ACID-Eigenschaften** von Transaktionen erklären

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 1: Subqueries — Abfragen in Abfragen

        Eine **Subquery** ist eine SELECT-Anweisung innerhalb einer anderen Abfrage.
        Je nach Rückgabe unterscheiden wir drei Typen:

        | Typ | Rückgabe | Einsatz | Beispiel |
        |-----|----------|---------|----------|
        | **Scalar** | 1 Wert | SELECT, WHERE | `WHERE Punkte > (SELECT AVG(Punkte) ...)` |
        | **Column** | 1 Spalte, n Zeilen | WHERE ... IN | `WHERE Mannschaft IN (SELECT team ...)` |
        | **Table** | Tabelle | FROM | `FROM (SELECT ...) AS t` |

        **Wichtig:** Die innere Abfrage wird zuerst ausgewertet, dann die äußere.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 9.1: Scalar Subquery — Differenz zum Durchschnitt

    Eine Scalar Subquery liefert **genau einen Wert** und kann überall dort stehen, wo ein einzelner Wert erwartet wird:
    """)
    return


@app.cell(hide_code=True)
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT
            Mannschaft,
            Punkte,
            ROUND((SELECT AVG(Punkte) FROM bundesliga), 1) AS Liga_Schnitt,
            ROUND(Punkte - (SELECT AVG(Punkte) FROM bundesliga), 1) AS Differenz
        FROM bundesliga
        ORDER BY Punkte DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Die Subquery `(SELECT AVG(Punkte) FROM bundesliga)` wird einmal berechnet und dann für jede Zeile verwendet. So sehen Sie auf einen Blick, welche Teams über oder unter dem Durchschnitt liegen.

        ---

        ### Geführtes Beispiel 9.2: Column Subquery mit IN

        Eine Column Subquery liefert **eine Spalte mit mehreren Werten** — ideal für `IN`:
        """
    )
    return


@app.cell(hide_code=True)
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
        **Beobachtung:** Die innere Abfrage liefert die Liste der Pokalhalbfinalisten. Die äußere Abfrage filtert die Bundesliga-Tabelle auf genau diese Teams.

        ---

        ### Vorhersage 1: Scalar Subquery in WHERE
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    pred_subquery = mo.ui.radio(
        options={
            "ueber_avg": "Nur Teams über dem Durchschnitt",
            "genau_avg": "Teams genau am Durchschnitt",
            "alle": "Alle Teams",
            "fehler": "Einen Fehler",
        },
        label="**Vorhersage:** Was liefert `WHERE Punkte > (SELECT AVG(Punkte) FROM bundesliga)`?",
    )
    pred_subquery
    return (pred_subquery,)


@app.cell(hide_code=True)
def _(mo, pred_subquery):
    if pred_subquery.value == "ueber_avg":
        mo.output.replace(
            mo.md(
                "✅ **Richtig!** Die Scalar Subquery berechnet den Durchschnitt (einen einzigen Wert). "
                "Der `>`-Operator vergleicht dann jeden Punkte-Wert mit diesem Durchschnitt. "
                "Nur Zeilen, deren Punkte **strikt größer** sind, bleiben im Ergebnis."
            )
        )
    elif pred_subquery.value == "genau_avg":
        mo.output.replace(
            mo.md(
                "❌ Nicht ganz. Der Operator `>` schließt den Durchschnittswert selbst aus — "
                "nur Teams **über** dem Durchschnitt werden zurückgegeben. "
                "Für 'genau am Durchschnitt' bräuchten Sie `=`, für 'ab Durchschnitt' `>=`."
            )
        )
    elif pred_subquery.value == "alle":
        mo.output.replace(
            mo.md(
                "❌ Nicht alle Teams. Die WHERE-Klausel filtert: Nur Teams mit Punkten "
                "**über** dem Durchschnitt bleiben. Teams mit unterdurchschnittlichen Punkten "
                "werden ausgeschlossen."
            )
        )
    elif pred_subquery.value == "fehler":
        mo.output.replace(
            mo.md(
                "❌ Kein Fehler. Eine Scalar Subquery in WHERE ist gültiges SQL. "
                "Die innere Abfrage liefert genau einen Wert (den Durchschnitt), "
                "der dann als Vergleichswert für jede Zeile dient."
            )
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Probieren Sie selbst: Subqueries

    Experimentieren Sie! Probieren Sie:
    - Andere Aggregatfunktionen in der Subquery: `MAX(Punkte)`, `MIN(Tore)`
    - `NOT IN` statt `IN` — welche Teams sind *nicht* im Pokal-Halbfinale?
    - Eine Table Subquery: `FROM (SELECT ... WHERE ...) AS top`
    """)
    return


@app.cell
def _(bundesliga, mo, pokal_halbfinale):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte
        FROM bundesliga
        WHERE Mannschaft NOT IN (
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
        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 2.x**

        ---

        ## Phase 3: Common Table Expressions (CTEs)

        CTEs machen komplexe Abfragen **lesbar** durch benannte Zwischenergebnisse.
        Statt verschachtelte Subqueries zu schreiben, definieren Sie Zwischenschritte mit `WITH`:

        ```sql
        WITH cte_name AS (
            SELECT ...
        )
        SELECT ...
        FROM cte_name
        ```

        **Vorteile gegenüber Subqueries:**
        - Bessere Lesbarkeit durch sprechende Namen
        - Wiederverwendbarkeit innerhalb der Abfrage
        - Einfacheres Debugging (Zwischenergebnis einzeln prüfbar)
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 9.4: CTE für Durchschnitt

    Berechnen Sie Liga-Durchschnitte einmal und verwenden Sie sie mehrfach:
    """)
    return


@app.cell(hide_code=True)
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
            ROUND(s.avg_punkte, 1) AS Liga_Schnitt_Punkte,
            ROUND(b.Punkte - s.avg_punkte, 1) AS Punkte_Diff,
            b.Tore,
            ROUND(s.avg_tore, 1) AS Liga_Schnitt_Tore,
            ROUND(b.Tore - s.avg_tore, 1) AS Tore_Diff
        FROM bundesliga b, statistiken s
        ORDER BY b.Punkte DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Der CTE `statistiken` wird einmal definiert und dann im JOIN verwendet. Ohne CTE müssten Sie die AVG-Subquery zweimal schreiben — einmal für Punkte, einmal für Tore.

        ---

        ### Geführtes Beispiel 9.5: Mehrere CTEs verketten

        CTEs können aufeinander aufbauen — jeder nutzt die vorherigen:
        """
    )
    return


@app.cell(hide_code=True)
def _(bundesliga, mo):
    siegquote_data = mo.sql(
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
    return (siegquote_data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Zuerst filtert `top_teams` die starken Teams, dann berechnet `mit_quote` die Siegquote. Jeder CTE hat einen klaren Zweck — das macht die Abfrage selbstdokumentierend.

        ---

        ### Vorhersage 2: Hauptvorteil von CTEs
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    pred_cte = mo.ui.radio(
        options={
            "lesbarkeit": "Bessere Lesbarkeit und Struktur",
            "schneller": "Schnellere Ausführung",
            "mehr_daten": "Können mehr Daten verarbeiten",
            "persistent": "Werden dauerhaft gespeichert",
        },
        label="**Vorhersage:** Was ist der Hauptvorteil von CTEs gegenüber verschachtelten Subqueries?",
    )
    pred_cte
    return (pred_cte,)


@app.cell(hide_code=True)
def _(mo, pred_cte):
    if pred_cte.value == "lesbarkeit":
        mo.output.replace(
            mo.md(
                "✅ **Richtig!** Der Hauptvorteil von CTEs ist die **bessere Lesbarkeit**. "
                "Statt tief verschachtelter Subqueries schreiben Sie benannte Zwischenschritte, "
                "die sich wie ein Rezept von oben nach unten lesen lassen."
            )
        )
    elif pred_cte.value == "schneller":
        mo.output.replace(
            mo.md(
                "❌ CTEs sind in der Regel **nicht schneller** als äquivalente Subqueries. "
                "Die Datenbank optimiert beide oft zum gleichen Ausführungsplan. "
                "Der Hauptvorteil ist die **bessere Lesbarkeit** und Wartbarkeit."
            )
        )
    elif pred_cte.value == "mehr_daten":
        mo.output.replace(
            mo.md(
                "❌ CTEs können nicht mehr Daten verarbeiten als Subqueries — "
                "sie sind nur eine andere Schreibweise. Der Hauptvorteil ist die "
                "**bessere Lesbarkeit**: benannte Zwischenschritte statt tiefer Verschachtelung."
            )
        )
    elif pred_cte.value == "persistent":
        mo.output.replace(
            mo.md(
                "❌ CTEs werden **nicht** dauerhaft gespeichert — sie existieren nur innerhalb "
                "einer einzigen Abfrage. Für dauerhafte Speicherung brauchen Sie **Views**. "
                "Der Hauptvorteil von CTEs ist die **bessere Lesbarkeit**."
            )
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 4.x**

        ---

        ## Phase 5: Views & Transaktionen

        ### Views — Wiederverwendbare virtuelle Tabellen

        Ein **View** ist eine gespeicherte Abfrage, die sich wie eine Tabelle verwenden lässt:

        ```sql
        CREATE OR REPLACE VIEW view_name AS
        SELECT ...
        FROM tabelle
        WHERE ...
        ```

        **Vorteile:**
        - Wiederverwendbar (im Gegensatz zu CTEs)
        - Vereinfacht komplexe Abfragen
        - Kann Zugriffsrechte steuern (bestimmte Spalten verbergen)
        - Wird bei jeder Abfrage **neu berechnet** (kein Snapshot!)
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel 9.6: View für Team-Statistiken

    Erstellen Sie einen View mit berechneten Kennzahlen:
    """)
    return


@app.cell(hide_code=True)
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


@app.cell(hide_code=True)
def _(mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Siegquote, Tore_pro_Spiel
        FROM team_statistik
        WHERE Siegquote > 40
        ORDER BY Siegquote DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Beobachtung:** Der View `team_statistik` berechnet Siegquote und Tore pro Spiel automatisch. Sie können ihn wie eine normale Tabelle abfragen — die Berechnung erfolgt bei jedem Zugriff.

        ---

        ### Transaktionen — ACID-Eigenschaften

        Transaktionen fassen zusammengehörige Änderungen zu einer **unteilbaren Einheit** zusammen:

        | Eigenschaft | Bedeutung | Beispiel |
        |-------------|-----------|----------|
        | **A**tomicity | Alles oder nichts | Überweisung: Abbuchung + Gutschrift |
        | **C**onsistency | Datenbank bleibt konsistent | Gesamtsumme aller Konten bleibt gleich |
        | **I**solation | Parallele Transaktionen stören sich nicht | Zwei gleichzeitige Überweisungen |
        | **D**urability | Bestätigte Änderungen sind permanent | Nach COMMIT auch bei Stromausfall sicher |
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Concurrency-Probleme

        Ohne Isolation können folgende Probleme auftreten:

        | Problem | Beschreibung | Konsequenz |
        |---------|--------------|------------|
        | **Lost Update** | Zwei Transaktionen überschreiben sich | Eine Änderung geht verloren |
        | **Dirty Read** | Lesen von nicht-committeten Daten | Entscheidung auf ungültiger Basis |
        | **Non-Repeatable Read** | Gleiche Abfrage, verschiedene Ergebnisse | Inkonsistente Analyse |
        | **Phantom Read** | Neue Zeilen erscheinen zwischen Abfragen | Unerwartete Ergebnisse |
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Transaktions-Demo: Überweisung

    Ausgangszustand der Konten:
    """)
    return


@app.cell(hide_code=True)
def _(konten, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM konten
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Transaktion: 200 EUR von Alice (A) nach Bob (B)**

        In einer echten Datenbank würden Sie schreiben:

        ```sql
        BEGIN TRANSACTION;

        UPDATE konten SET saldo = saldo - 200 WHERE konto_id = 'A';
        UPDATE konten SET saldo = saldo + 200 WHERE konto_id = 'B';

        COMMIT;
        ```

        **Wichtig:** Wenn zwischen den beiden UPDATEs ein Fehler auftritt, macht `ROLLBACK` **beide** Änderungen rückgängig. Alice verliert kein Geld, und Bob bekommt keins — statt dass nur die Hälfte ausgeführt wird.

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### ACID-Quiz
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    acid_quiz = mo.ui.radio(
        options={
            "atomic": "Alles oder nichts — entweder alle Operationen oder keine",
            "isolation": "Gleichzeitiger Zugriff ist möglich",
            "durability": "Daten werden dauerhaft gespeichert",
            "consistency": "Daten bleiben konsistent",
        },
        label="**Quiz:** Was garantiert die **Atomarität** (Atomicity) einer Transaktion?",
    )
    acid_quiz
    return (acid_quiz,)


@app.cell(hide_code=True)
def _(acid_quiz, mo):
    if acid_quiz.value == "atomic":
        mo.output.replace(
            mo.md(
                "✅ **Richtig!** Atomarität bedeutet: Eine Transaktion wird entweder "
                "**komplett** oder **gar nicht** ausgeführt. Wenn ein Schritt fehlschlägt, "
                "werden alle bisherigen Änderungen rückgängig gemacht (ROLLBACK)."
            )
        )
    elif acid_quiz.value == "isolation":
        mo.output.replace(
            mo.md(
                "❌ Das beschreibt **Isolation**, nicht Atomarität. "
                "Isolation sorgt dafür, dass parallele Transaktionen sich nicht gegenseitig stören. "
                "Atomarität bedeutet: **Alles oder nichts** — entweder alle Operationen oder keine."
            )
        )
    elif acid_quiz.value == "durability":
        mo.output.replace(
            mo.md(
                "❌ Das beschreibt **Durability** (Dauerhaftigkeit), nicht Atomarität. "
                "Durability garantiert, dass bestätigte Änderungen permanent sind. "
                "Atomarität bedeutet: **Alles oder nichts** — keine halb ausgeführten Transaktionen."
            )
        )
    elif acid_quiz.value == "consistency":
        mo.output.replace(
            mo.md(
                "❌ Das beschreibt **Consistency** (Konsistenz), nicht Atomarität. "
                "Konsistenz garantiert, dass Integritätsbedingungen eingehalten werden. "
                "Atomarität bedeutet: **Alles oder nichts** — die Transaktion ist unteilbar."
            )
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Vorhersage 3: Absturz während einer Transaktion
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    pred_acid = mo.ui.radio(
        options={
            "geld_weg": "Geld ist weg — Alice hat weniger, Bob nicht mehr",
            "rollback": "Automatisches Rollback — beide Konten wie vorher",
            "halb": "Halb ausgeführt — Abbuchung bleibt, Gutschrift fehlt",
            "retry": "Automatische Wiederholung der Transaktion",
        },
        label="**Vorhersage:** Der Server stürzt nach der Abbuchung bei Alice, aber vor der Gutschrift bei Bob ab. Was passiert?",
    )
    pred_acid
    return (pred_acid,)


@app.cell(hide_code=True)
def _(mo, pred_acid):
    if pred_acid.value == "rollback":
        mo.output.replace(
            mo.md(
                "✅ **Richtig!** Die ACID-Eigenschaft **Atomicity** garantiert: Wenn die Transaktion "
                "nicht vollständig abgeschlossen wurde (kein COMMIT), werden **alle** Änderungen "
                "rückgängig gemacht. Nach dem Neustart haben beide Konten ihren ursprünglichen Stand."
            )
        )
    elif pred_acid.value == "geld_weg":
        mo.output.replace(
            mo.md(
                "❌ Das wäre ein Albtraum-Szenario — aber genau davor schützt **Atomicity**! "
                "Ohne COMMIT wird die gesamte Transaktion zurückgerollt. "
                "Alice behält ihr Geld, Bobs Konto bleibt unverändert."
            )
        )
    elif pred_acid.value == "halb":
        mo.output.replace(
            mo.md(
                "❌ Genau das verhindert **Atomicity**: Es gibt keine halb ausgeführten Transaktionen. "
                "Entweder werden alle Operationen ausgeführt (COMMIT) oder keine (ROLLBACK). "
                "Nach dem Absturz wird automatisch zurückgerollt."
            )
        )
    elif pred_acid.value == "retry":
        mo.output.replace(
            mo.md(
                "❌ Die Datenbank wiederholt die Transaktion nicht automatisch. "
                "Stattdessen greift **Atomicity**: Die nicht abgeschlossene Transaktion wird "
                "zurückgerollt (ROLLBACK), und die Anwendung muss sie bei Bedarf erneut starten."
            )
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 6.x**

        ---

        ## Phase 7: Visualisierung — CTE-Ergebnisse darstellen
        """
    )
    return


@app.cell(hide_code=True)
def _():
    import plotly.express as px
    return (px,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Siegquote der Top-Teams (via CTE)
    """)
    return


@app.cell(hide_code=True)
def _(bundesliga, mo, px):
    _top = mo.sql(
        f"""
        WITH mit_quote AS (
            SELECT
                Mannschaft,
                Punkte,
                ROUND(CAST(Siege AS FLOAT) / Spiele * 100, 1) AS Siegquote
            FROM bundesliga
            WHERE Punkte > 30
        )
        SELECT * FROM mit_quote ORDER BY Siegquote DESC
        """
    )

    fig_siegquote = px.bar(
        _top,
        x="Mannschaft",
        y="Siegquote",
        color="Punkte",
        title="Siegquote der Teams mit > 30 Punkten (berechnet via CTE)",
        labels={"Siegquote": "Siegquote (%)", "Mannschaft": ""},
        color_continuous_scale="Blues",
    )
    fig_siegquote
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Divergierendes Balkendiagramm: Differenz zum Liga-Durchschnitt
    """)
    return


@app.cell(hide_code=True)
def _(bundesliga, mo, px):
    _diff = mo.sql(
        f"""
        WITH liga_avg AS (
            SELECT AVG(Punkte) AS avg_punkte
            FROM bundesliga
        )
        SELECT
            b.Mannschaft,
            ROUND(b.Punkte - a.avg_punkte, 1) AS Differenz
        FROM bundesliga b, liga_avg a
        ORDER BY Differenz DESC
        """
    )

    fig_diverging = px.bar(
        _diff,
        x="Differenz",
        y="Mannschaft",
        orientation="h",
        title="Punkte-Differenz zum Liga-Durchschnitt",
        labels={"Differenz": "Differenz zum Ø (Punkte)", "Mannschaft": ""},
        color="Differenz",
        color_continuous_scale=["#d62728", "#f7f7f7", "#1f77b4"],
        color_continuous_midpoint=0,
    )
    fig_diverging.update_layout(yaxis=dict(autorange="reversed"))
    fig_diverging
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Viz-Choice: Abweichungen darstellen
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    viz_choice_9 = mo.ui.radio(
        options={
            "bar_diverging": "Divergierendes Balkendiagramm",
            "pie": "Kreisdiagramm",
            "line": "Liniendiagramm",
            "scatter": "Streudiagramm",
        },
        label="Sie wollen die Differenz jedes Teams zum Liga-Durchschnitt darstellen. Welcher Charttyp eignet sich am besten?",
    )
    viz_choice_9
    return (viz_choice_9,)


@app.cell(hide_code=True)
def _(mo, viz_choice_9):
    if viz_choice_9.value == "bar_diverging":
        mo.output.replace(
            mo.md(
                "✅ **Richtig!** Ein **divergierendes Balkendiagramm** ist ideal für Abweichungen "
                "von einem Referenzwert. Die Nulllinie markiert den Durchschnitt, positive Balken "
                "zeigen überdurchschnittliche Teams, negative unterdurchschnittliche. "
                "Die Farbe verstärkt den Effekt visuell."
            )
        )
    elif viz_choice_9.value == "pie":
        mo.output.replace(
            mo.md(
                "❌ Ein Kreisdiagramm zeigt Anteile am Ganzen (z.B. 'Bayern hat X% aller Punkte'). "
                "Für **Abweichungen** mit positiven und negativen Werten ist es ungeeignet. "
                "Ein **divergierendes Balkendiagramm** zeigt Über- und Unterdurchschnitt direkt."
            )
        )
    elif viz_choice_9.value == "line":
        mo.output.replace(
            mo.md(
                "❌ Ein Liniendiagramm suggeriert eine zeitliche Entwicklung oder Verbindung "
                "zwischen den Datenpunkten. Teams haben keine natürliche Reihenfolge. "
                "Ein **divergierendes Balkendiagramm** eignet sich besser für kategorische Abweichungen."
            )
        )
    elif viz_choice_9.value == "scatter":
        mo.output.replace(
            mo.md(
                "❌ Ein Streudiagramm zeigt den Zusammenhang zwischen zwei numerischen Variablen. "
                "Hier haben wir Kategorien (Teams) und einen Wert (Differenz). "
                "Ein **divergierendes Balkendiagramm** stellt positive und negative Abweichungen am klarsten dar."
            )
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Selbsttest
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    selbsttest_9 = mo.ui.radio(
        options={
            "cte_temp": "CTE existiert nur innerhalb einer Abfrage, View ist dauerhaft gespeichert",
            "gleich": "Kein Unterschied — beides sind Aliase für Abfragen",
            "view_schneller": "Views sind schneller als CTEs",
        },
        label="Was ist der Unterschied zwischen einer CTE und einem View?",
    )
    selbsttest_9
    return (selbsttest_9,)


@app.cell(hide_code=True)
def _(mo, selbsttest_9):
    if selbsttest_9.value == "cte_temp":
        mo.output.replace(
            mo.md(
                "✅ **Richtig!** Eine CTE existiert nur innerhalb der **einen** Abfrage, in der sie "
                "definiert wird. Ein View wird dauerhaft in der Datenbank gespeichert und kann "
                "von **beliebig vielen** Abfragen wie eine Tabelle verwendet werden. "
                "Merkhilfe: CTE = temporärer Notizzettel, View = gespeichertes Rezept."
            )
        )
    elif selbsttest_9.value == "gleich":
        mo.output.replace(
            mo.md(
                "❌ Es gibt einen wichtigen Unterschied: Eine CTE existiert nur **innerhalb einer Abfrage** "
                "und verschwindet danach. Ein View wird **dauerhaft gespeichert** und kann wie eine Tabelle "
                "von verschiedenen Abfragen genutzt werden."
            )
        )
    elif selbsttest_9.value == "view_schneller":
        mo.output.replace(
            mo.md(
                "❌ Views sind nicht grundsätzlich schneller als CTEs — beide werden bei jeder "
                "Abfrage neu berechnet. Der wahre Unterschied: CTEs sind **temporär** (eine Abfrage), "
                "Views sind **dauerhaft** (in der Datenbank gespeichert)."
            )
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Zusammenfassung

        | Konzept | Beschreibung | Wann nutzen? |
        |---------|--------------|--------------|
        | **Subquery** | Abfrage in Abfrage | Einfache einmalige Berechnungen (AVG, MAX in WHERE) |
        | **CTE (WITH)** | Benannte Zwischenergebnisse | Komplexe Abfragen lesbar strukturieren |
        | **View** | Gespeicherte virtuelle Tabelle | Wiederverwendbare Abfragen für mehrere Nutzer |
        | **Transaktion** | Zusammengehörige Änderungen | Datenintegrität bei Änderungen sichern (ACID) |

        ### Entscheidungsbaum

        ```
        Brauche ich das Ergebnis öfter?
        ├── Nein (einmalig) → Ist die Abfrage komplex?
        │   ├── Ja → CTE (WITH ... AS)
        │   └── Nein → Subquery
        └── Ja (wiederholt) → View (CREATE VIEW)
        ```

        ### ACID auf einen Blick

        | A | C | I | D |
        |---|---|---|---|
        | Alles oder nichts | Konsistenzregeln einhalten | Parallele Transaktionen isoliert | Bestätigte Änderungen permanent |

        ### Ausblick Session 10: Datenanalyse

        Ab nächster Woche starten wir Block IV — Explorative Datenanalyse mit SQL und Python.
        """
    )
    return


if __name__ == "__main__":
    app.run()
