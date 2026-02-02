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
    app_title="DMA Session 2: SQL für Datenexploration — Guide",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 2: SQL für Datenexploration — Guide

        **Kursfahrplan:** **▸ I: SQL-Grundlagen (S1–4)** · II: Datenmodellierung (S5–7) · III: Fortgeschrittenes SQL (S8–9) · IV: Datenanalyse (S10–13)

        ### Lernziele

        Nach dieser Session können Sie:

        - Ergebnisse **sortieren** mit `ORDER BY` (ASC/DESC)
        - Ergebnisse **begrenzen** mit `LIMIT` und **überspringen** mit `OFFSET`
        - **Eindeutige Werte** finden mit `DISTINCT`
        - **Mustersuche** vertiefen mit `LIKE`
        - Mit **NULL-Werten** umgehen (`IS NULL`, `COALESCE`)
        - **Streudiagramme** für Zusammenhänge nutzen

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Daten laden

        Wir arbeiten heute mit zwei Datensätzen:
        1. **Bundesliga-Tabelle** (wie letzte Woche)
        2. **Spieler-Daten** (mit fehlenden Werten für NULL-Übungen)
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    import polars as pl

    try:
        csv_path = mo.notebook_location() / "public" / "bundesliga.csv"
        bundesliga = pl.read_csv(str(csv_path))
        daten_quelle = "Beispieldaten Bundesliga Saison 2024/25"
    except Exception:
        bundesliga = pl.DataFrame({
            "Mannschaft": ["Bayern München", "Bayer Leverkusen", "VfB Stuttgart", "Borussia Dortmund", "RB Leipzig"],
            "Spiele": [34, 34, 34, 34, 34],
            "Siege": [23, 21, 17, 16, 15],
            "Unentschieden": [5, 7, 6, 7, 8],
            "Niederlagen": [6, 6, 11, 11, 11],
            "Tore": [82, 68, 58, 62, 55],
            "Gegentore": [32, 29, 44, 42, 38],
            "Tordifferenz": [50, 39, 14, 20, 17],
            "Punkte": [74, 70, 57, 55, 53],
        })
        daten_quelle = "Offline-Daten (Fallback)"
        mo.callout(mo.md("**Hinweis:** CSV konnte nicht geladen werden. Es werden Beispieldaten verwendet."), kind="warn")

    return bundesliga, daten_quelle, pl


@app.cell(hide_code=True)
def _(mo, pl):
    try:
        spieler_path = mo.notebook_location() / "public" / "spieler.csv"
        spieler = pl.read_csv(str(spieler_path))

        spieltage_path = mo.notebook_location() / "public" / "bundesliga_spieltage.csv"
        bundesliga_spieltage = pl.read_csv(str(spieltage_path))
    except Exception:
        spieler = pl.DataFrame({
            "Name": ["Müller", "Neuer", "Kimmich", "Wirtz", "Musiala"],
            "Vorname": ["Thomas", "Manuel", "Joshua", "Florian", "Jamal"],
            "Position": ["Sturm", "Tor", "Mittelfeld", "Mittelfeld", "Mittelfeld"],
            "Verein": ["Bayern München", "Bayern München", "Bayern München", "Bayer Leverkusen", None],
            "Tore": [8, 0, 3, 11, None],
            "Vorlagen": [4, 0, 8, 9, 7],
            "Alter": [35, 38, 29, 21, 21],
            "Länderspiele": [131, 118, 91, 28, 35],
            "Spitzname": [None, None, None, None, "Bambi"],
        })
        bundesliga_spieltage = pl.DataFrame({
            "Mannschaft": ["Bayern München"] * 5,
            "Spieltag": [1, 2, 3, 4, 5],
            "Punkte_Kumuliert": [3, 6, 9, 10, 13],
        })
        mo.callout(mo.md("**Hinweis:** CSVs konnten nicht geladen werden. Es werden Beispieldaten verwendet."), kind="warn")

    return bundesliga_spieltage, spieler


@app.cell(hide_code=True)
def _(daten_quelle, mo):
    mo.md(
        f"""
        **Datenquelle Bundesliga:** {daten_quelle}

        **Datensätze:**
        - `bundesliga` – Finale Tabelle (18 Teams, 1 Zeitpunkt)
        - `bundesliga_spieltage` – Verlauf (18 Teams × 34 Spieltage)
        - `spieler` – Spielerdaten (mit NULL-Werten)

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Recap: Von Zeitreihe zu Querschnitt

        Die finale Tabelle ist nur ein **WHERE-Filter** auf den letzten Spieltag!
        """
    )
    return


@app.cell(hide_code=True)
def _(bundesliga_spieltage, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte_Kumuliert AS Punkte
        FROM bundesliga_spieltage
        WHERE Spieltag = (SELECT MAX(Spieltag) FROM bundesliga_spieltage)
        ORDER BY Punkte DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Erkenntnis:** Die "Tabelle" die wir letzte Woche verwendet haben, ist einfach der letzte Spieltag!

        ---

        ## Phase 2: Daten sortieren und begrenzen

        ### ORDER BY — Ergebnisse sortieren

        ```sql
        SELECT spalten
        FROM tabelle
        ORDER BY spalte ASC    -- aufsteigend (Standard)
        ORDER BY spalte DESC   -- absteigend
        ```

        - `ASC` = aufsteigend (ascending) — Standard, kann weggelassen werden
        - `DESC` = absteigend (descending) — muss explizit angegeben werden
        - Mehrere Sortierkriterien: `ORDER BY spalte1 DESC, spalte2 ASC`

        ### LIMIT und OFFSET — Paginierung

        ```sql
        SELECT spalten
        FROM tabelle
        ORDER BY spalte DESC
        LIMIT 5           -- nur die ersten 5 Zeilen
        LIMIT 5 OFFSET 5  -- 5 Zeilen, überspringe die ersten 5 (= Plätze 6-10)
        ```

        **Reihenfolge der Klauseln:**
        ```
        SELECT → FROM → WHERE → ORDER BY → LIMIT
        ```
        Diese Reihenfolge muss eingehalten werden!
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel: Sortierung
    """)
    return


@app.cell(hide_code=True)
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte
        FROM bundesliga
        ORDER BY Punkte DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel: Paginierung — Top 5
    """)
    return


@app.cell(hide_code=True)
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte
        FROM bundesliga
        ORDER BY Punkte DESC
        LIMIT 5
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Probieren Sie selbst: Sortierung und Begrenzung

    Ändern Sie die Abfrage: Versuchen Sie `ASC` statt `DESC`, oder ändern Sie das `LIMIT`.
    Was passiert bei `LIMIT 3 OFFSET 5`?
    """)
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte
        FROM bundesliga
        ORDER BY Punkte DESC
        LIMIT 3
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Vorhersage 1
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    vorhersage_limit = mo.ui.radio(
        options={
            "5": "5 Zeilen",
            "18": "18 Zeilen (alle Teams)",
            "fehler": "Fehler",
        },
        label="Wie viele Zeilen liefert `SELECT Mannschaft, Punkte FROM bundesliga ORDER BY Punkte DESC LIMIT 5`?"
    )
    vorhersage_limit
    return (vorhersage_limit,)


@app.cell(hide_code=True)
def _(vorhersage_limit, mo):
    if vorhersage_limit.value == "5":
        mo.output.replace(mo.md("✅ **Richtig!** `LIMIT 5` begrenzt das Ergebnis auf maximal 5 Zeilen — unabhängig davon, wie viele Zeilen die Tabelle hat."))
    elif vorhersage_limit.value == "18":
        mo.output.replace(mo.md("❌ 18 Zeilen wären das Ergebnis **ohne** LIMIT. `LIMIT 5` begrenzt die Ausgabe auf maximal **5 Zeilen** — die ersten 5 nach der Sortierung."))
    elif vorhersage_limit.value == "fehler":
        mo.output.replace(mo.md("❌ Kein Fehler — die Abfrage ist syntaktisch korrekt. `LIMIT 5` begrenzt das Ergebnis auf maximal **5 Zeilen**. Es werden die Top-5 Teams nach Punkten angezeigt."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 2.x**

        ---

        ## Phase 4: DISTINCT und LIKE

        ### DISTINCT — Eindeutige Werte

        ```sql
        SELECT DISTINCT spalte
        FROM tabelle
        ```

        Entfernt doppelte Zeilen aus dem Ergebnis. Nützlich um herauszufinden, welche verschiedenen Werte eine Spalte enthält.

        **Wichtig:** `NULL` zählt als eigener "Wert" bei DISTINCT!

        ### LIKE — Wildcards im Detail

        | Muster | Bedeutung | Beispiel | Findet |
        |--------|-----------|----------|--------|
        | `'B%'` | Beginnt mit B | `LIKE 'B%'` | Bayern, Borussia |
        | `'%er'` | Endet mit er | `LIKE '%er'` | Müller, Neuer |
        | `'%FC%'` | Enthält FC | `LIKE '%FC%'` | 1. FC Union, FC Augsburg |
        | `'M___r'` | M + 3 Zeichen + r | `LIKE 'M___r'` | Mayer, Meier |
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Vorhersage 2
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    vorhersage_distinct = mo.ui.radio(
        options={
            "ohne_null": "NULL-Zeilen werden herausgefiltert — nur echte Vereine erscheinen",
            "mit_null": "NULL erscheint als eigene Zeile im Ergebnis",
            "fehler": "Es gibt einen Fehler, weil DISTINCT mit NULL nicht funktioniert",
        },
        label="Die Spieler-Tabelle enthält NULL-Werte in der Spalte `Verein`. Was passiert bei `SELECT DISTINCT Verein FROM spieler` mit den NULL-Einträgen?"
    )
    vorhersage_distinct
    return (vorhersage_distinct,)


@app.cell(hide_code=True)
def _(vorhersage_distinct, mo):
    if vorhersage_distinct.value == "mit_null":
        mo.output.replace(mo.md("✅ **Richtig!** DISTINCT behandelt NULL als eigenen 'Wert'. Im Ergebnis erscheint genau **eine** NULL-Zeile — egal wie viele Spieler keinen Verein haben. So können Sie fehlende Daten gezielt erkennen."))
    elif vorhersage_distinct.value == "ohne_null":
        mo.output.replace(mo.md("❌ Nicht ganz. DISTINCT filtert NULL **nicht** heraus. Stattdessen wird NULL als eigener 'Wert' behandelt und erscheint als **eigene Zeile** im Ergebnis. Um NULL-Werte auszuschließen, brauchen Sie explizit `WHERE spalte IS NOT NULL`."))
    elif vorhersage_distinct.value == "fehler":
        mo.output.replace(mo.md("❌ Nicht ganz. DISTINCT funktioniert problemlos mit NULL-Werten. NULL wird dabei als eigener 'Wert' behandelt und erscheint als **eigene Zeile** im Ergebnis — kein Fehler."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 4.x**

        ---

        ## Phase 6: NULL-Werte — Das Unbekannte

        ### Was ist NULL?

        NULL bedeutet **"unbekannt"** oder **"nicht vorhanden"** — es ist NICHT dasselbe wie 0, leer oder False!

        ### Dreiwertige Logik

        In den meisten Programmiersprachen gibt es nur TRUE und FALSE. SQL hat **drei** Wahrheitswerte:

        | Vergleich | Ergebnis |
        |-----------|----------|
        | `5 = 5` | TRUE |
        | `5 = 3` | FALSE |
        | `5 = NULL` | **NULL** (unbekannt!) |
        | `NULL = NULL` | **NULL** (nicht TRUE!) |

        ### IS NULL und IS NOT NULL

        ```sql
        -- ✅ Richtig:
        WHERE spalte IS NULL
        WHERE spalte IS NOT NULL

        -- ❌ Falsch (liefert nie Ergebnisse!):
        WHERE spalte = NULL
        ```

        ### COALESCE — NULL ersetzen

        ```sql
        COALESCE(wert, ersatz)
        -- Wenn wert NULL ist, verwende ersatz

        COALESCE(wert1, wert2, wert3)
        -- Erster nicht-NULL Wert wird verwendet
        ```

        ### NULL in Berechnungen

        Jede Berechnung mit NULL ergibt NULL:
        - `5 + NULL` → NULL
        - `NULL * 3` → NULL
        - `'Hallo' || NULL` → NULL
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Probieren Sie selbst: NULL-Werte erkunden

    Experimentieren Sie mit NULL in der Spieler-Tabelle. Ändern Sie die Abfrage!
    Probieren Sie: `IS NOT NULL`, `COALESCE(Verein, 'Unbekannt')`, `WHERE Tore IS NULL`
    """)
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT Name, Verein, Tore
        FROM spieler
        WHERE Verein IS NULL
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Vorhersage 3
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    vorhersage_null = mo.ui.radio(
        options={
            "null": "NULL",
            "5": "5",
            "0": "0",
            "fehler": "Fehler",
        },
        label="Was ergibt `5 + NULL` in SQL?"
    )
    vorhersage_null
    return (vorhersage_null,)


@app.cell(hide_code=True)
def _(vorhersage_null, mo):
    if vorhersage_null.value == "null":
        mo.output.replace(mo.md("✅ **Richtig!** Jede Berechnung mit NULL ergibt NULL. NULL bedeutet 'unbekannt' — und 5 + unbekannt = unbekannt. Deshalb ist `COALESCE` so wichtig: `COALESCE(spalte, 0)` ersetzt NULL durch 0 vor der Berechnung."))
    elif vorhersage_null.value == "5":
        mo.output.replace(mo.md("❌ Nicht ganz. SQL ignoriert NULL **nicht** und nimmt auch nicht einfach den bekannten Wert. NULL bedeutet 'unbekannt', und 5 + unbekannt = **unbekannt (NULL)**. Verwenden Sie `COALESCE(spalte, 0)` um NULL vorher durch 0 zu ersetzen."))
    elif vorhersage_null.value == "0":
        mo.output.replace(mo.md("❌ Nicht ganz. NULL ist **nicht** dasselbe wie 0! NULL bedeutet 'unbekannt'. Da der zweite Operand unbekannt ist, ist auch das Ergebnis **unbekannt (NULL)**. Um NULL als 0 zu behandeln: `COALESCE(spalte, 0)`."))
    elif vorhersage_null.value == "fehler":
        mo.output.replace(mo.md("❌ Kein Fehler — SQL führt die Berechnung aus, gibt aber **NULL** zurück. NULL bedeutet 'unbekannt', und jede Berechnung mit einem unbekannten Wert ergibt NULL."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Quiz: NULL = NULL
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    quiz_null = mo.ui.radio(
        options={
            "null": "NULL (unbekannt)",
            "true": "TRUE",
            "false": "FALSE",
            "error": "Ein Fehler tritt auf"
        },
        label="**Quiz:** Was ergibt der Vergleich `NULL = NULL` in SQL?"
    )
    quiz_null
    return (quiz_null,)


@app.cell(hide_code=True)
def _(quiz_null, mo):
    if quiz_null.value == "null":
        mo.output.replace(mo.md("✅ **Richtig!** `NULL = NULL` ergibt NULL (nicht TRUE!), weil NULL 'unbekannt' bedeutet. Zwei unbekannte Werte sind nicht zwingend gleich — deshalb brauchen wir `IS NULL` statt `= NULL`."))
    elif quiz_null.value == "true":
        mo.output.replace(mo.md("❌ Intuitiv denkt man: 'Gleich ist gleich!' Aber NULL bedeutet 'unbekannt'. Zwei **unbekannte** Werte sind nicht automatisch gleich — deshalb ergibt `NULL = NULL` nicht TRUE, sondern **NULL**. Verwenden Sie `IS NULL` statt `= NULL`."))
    elif quiz_null.value == "false":
        mo.output.replace(mo.md("❌ Nah dran — aber nicht FALSE. `NULL = NULL` ergibt **NULL** (nicht FALSE). In SQL gibt es drei Wahrheitswerte: TRUE, FALSE und NULL. Jeder Vergleich mit NULL ergibt NULL."))
    elif quiz_null.value == "error":
        mo.output.replace(mo.md("❌ Kein Fehler — SQL führt den Vergleich aus. Aber das Ergebnis ist **NULL** (nicht TRUE oder FALSE). NULL bedeutet 'unbekannt', und ob zwei unbekannte Werte gleich sind, ist ebenfalls unbekannt."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 6.x**

        ---

        ## Phase 7: Visualisierung — Zusammenhänge erkennen

        ### Streudiagramm (Scatter Plot)

        Ein Streudiagramm zeigt den **Zusammenhang** zwischen zwei numerischen Variablen:
        - x-Achse: eine Variable (z.B. Tore)
        - y-Achse: andere Variable (z.B. Punkte)
        - Jeder Punkt = ein Datensatz

        ```python
        px.scatter(daten, x="Variable1", y="Variable2",
                   hover_name="Label", trendline="ols")
        ```
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel: Tore vs. Punkte
    """)
    return


@app.cell(hide_code=True)
def _():
    import plotly.express as px
    return (px,)


@app.cell(hide_code=True)
def _(bundesliga, mo, px):
    alle_teams = mo.sql(
        f"""
        SELECT Mannschaft, Tore, Punkte
        FROM bundesliga
        """
    )

    fig_scatter = px.scatter(
        alle_teams,
        x="Tore",
        y="Punkte",
        hover_name="Mannschaft",
        title="Tore vs. Punkte",
        trendline="ols"
    )
    fig_scatter
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel: Streudiagramm mit Farbdimension

    Eine dritte Variable als Farbe kodieren:
    """)
    return


@app.cell(hide_code=True)
def _(bundesliga, mo, px):
    offensiv_defensiv = mo.sql(
        f"""
        SELECT Mannschaft, Tore, Gegentore, Tordifferenz
        FROM bundesliga
        """
    )

    fig_color = px.scatter(
        offensiv_defensiv,
        x="Tore",
        y="Gegentore",
        color="Tordifferenz",
        hover_name="Mannschaft",
        title="Offensiv- vs. Defensivstärke (Farbe = Tordifferenz)"
    )
    fig_color
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Viz-Choice: Den richtigen Charttyp wählen
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    viz_choice_2 = mo.ui.radio(
        options={
            "bar": "Balkendiagramm",
            "line": "Liniendiagramm",
            "scatter": "Streudiagramm",
            "histogram": "Histogramm",
        },
        label="Sie wollen den Zusammenhang zwischen Tore und Punkten zeigen. Welcher Charttyp passt am besten?"
    )
    viz_choice_2
    return (viz_choice_2,)


@app.cell(hide_code=True)
def _(viz_choice_2, mo):
    if viz_choice_2.value == "scatter":
        mo.output.replace(mo.md("✅ **Richtig!** Ein **Streudiagramm** ist ideal, um den **Zusammenhang** zwischen zwei numerischen Variablen zu zeigen. Jedes Team ist ein Punkt, und man sieht sofort, ob ein Muster (Korrelation) existiert."))
    elif viz_choice_2.value == "bar":
        mo.output.replace(mo.md("❌ Nicht ganz. Ein Balkendiagramm eignet sich zum **Vergleichen** von Kategorien (z.B. Punkte pro Team). Für den **Zusammenhang** zwischen zwei numerischen Variablen ist ein **Streudiagramm** besser."))
    elif viz_choice_2.value == "line":
        mo.output.replace(mo.md("❌ Nicht ganz. Ein Liniendiagramm zeigt **Entwicklungen über die Zeit**. Für den **Zusammenhang** zwischen zwei numerischen Variablen (ohne Zeitbezug) ist ein **Streudiagramm** besser."))
    elif viz_choice_2.value == "histogram":
        mo.output.replace(mo.md("❌ Nicht ganz. Ein Histogramm zeigt die **Verteilung** einer einzelnen Variable. Für den **Zusammenhang** zwischen zwei Variablen ist ein **Streudiagramm** besser."))
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
    selbsttest_2 = mo.ui.radio(
        options={
            "where_null": "WHERE Verein = NULL",
            "is_null": "WHERE Verein IS NULL",
            "coalesce": "WHERE COALESCE(Verein) = NULL",
        },
        label="Welche Abfrage findet Spieler ohne Verein korrekt?"
    )
    selbsttest_2
    return (selbsttest_2,)


@app.cell(hide_code=True)
def _(selbsttest_2, mo):
    if selbsttest_2.value == "is_null":
        mo.output.replace(mo.md("✅ **Richtig!** `IS NULL` ist der einzig korrekte Weg, auf NULL zu prüfen. `= NULL` ergibt immer NULL (nie TRUE), daher findet es keine Zeilen."))
    elif selbsttest_2.value == "where_null":
        mo.output.replace(mo.md("❌ `= NULL` funktioniert nicht! Der Vergleich ergibt immer NULL (nie TRUE). Verwenden Sie stattdessen `IS NULL`."))
    elif selbsttest_2.value == "coalesce":
        mo.output.replace(mo.md("❌ `COALESCE` ersetzt NULL durch einen Standardwert — es prüft nicht auf NULL. Und `COALESCE(Verein)` ohne Ersatzwert ist sinnlos. Verwenden Sie `IS NULL` zum Prüfen."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Zusammenfassung

        ### SQL-Konzepte

        | Konzept | Syntax | Beispiel |
        |---------|--------|----------|
        | Aufsteigend sortieren | `ORDER BY spalte ASC` | `ORDER BY Punkte ASC` |
        | Absteigend sortieren | `ORDER BY spalte DESC` | `ORDER BY Punkte DESC` |
        | Begrenzen | `LIMIT n` | `LIMIT 5` |
        | Überspringen | `LIMIT n OFFSET m` | `LIMIT 5 OFFSET 5` |
        | Eindeutige Werte | `SELECT DISTINCT` | `SELECT DISTINCT Position` |
        | Muster (beginnt mit) | `LIKE 'X%'` | `WHERE Name LIKE 'M%'` |
        | Muster (enthält) | `LIKE '%X%'` | `WHERE Name LIKE '%er%'` |
        | NULL prüfen | `IS NULL` / `IS NOT NULL` | `WHERE Tore IS NULL` |
        | NULL ersetzen | `COALESCE(wert, ersatz)` | `COALESCE(Tore, 0)` |

        ### Visualisierung mit Plotly

        | Chart-Typ | Funktion | Verwendung |
        |-----------|----------|------------|
        | Balkendiagramm | `px.bar()` | Kategorien vergleichen |
        | Streudiagramm | `px.scatter()` | Zusammenhänge zeigen |
        | Farbe als Dimension | `color=` | Dritte Variable kodieren |

        ### Häufige Fehler vermeiden

        - `IS NULL` statt `= NULL`
        - Reihenfolge: SELECT → FROM → WHERE → ORDER BY → LIMIT
        - Bei Berechnungen: COALESCE verwenden, um NULL zu ersetzen
        - ASC ist Standard, DESC muss explizit angegeben werden

        ### Ausblick Session 3

        Nächste Woche: Aggregation & Gruppierung — COUNT, SUM, AVG, GROUP BY, HAVING
        """
    )
    return


if __name__ == "__main__":
    app.run()
