import marimo

__generated_with = "0.13.0"
app = marimo.App(
    width="medium",
    app_title="DMA Session 1: SQL-Grundlagen",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 1: SQL-Grundlagen

        Willkommen zur ersten Hands-on-Session! In diesem Notebook lernen Sie:

        - Daten mit `SELECT` abfragen
        - Spalten auswählen
        - Zeilen mit `WHERE` filtern
        - Bedingungen mit `AND`, `OR`, `NOT` kombinieren

        **Aufgabentypen:**
        - 🟢 **Geführt**: Beispiel zum Nachvollziehen
        - 🟡 **Scaffolded**: Teillösung zum Ergänzen
        - 🔵 **Selbstständig**: Eigene Lösung schreiben
        - 🔴 **Debugging**: Fehler finden und beheben
        - 🟣 **Vorhersage**: Was wird das Ergebnis sein?

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Daten laden: Bundesliga-Tabelle

        Wir arbeiten mit aktuellen Bundesliga-Daten.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    import polars as pl

    # Works both locally and in WASM/browser mode
    csv_path = mo.notebook_location() / "public" / "bundesliga.csv"
    bundesliga = pl.read_csv(str(csv_path))

    # Also load spieltage data for temporal analysis
    spieltage_path = mo.notebook_location() / "public" / "bundesliga_spieltage.csv"
    bundesliga_spieltage = pl.read_csv(str(spieltage_path))

    daten_quelle = "Beispieldaten Bundesliga Saison 2024/25"
    return bundesliga, bundesliga_spieltage, daten_quelle, pl


@app.cell(hide_code=True)
def _(daten_quelle, mo):
    mo.md(
        f"""
        **Datenquelle:** {daten_quelle}

        **Verfügbare Spalten:** Mannschaft, Spiele, Siege, Unentschieden, Niederlagen, ToreGeschossen, ToreKassiert, Tordifferenz, Punkte

        ---

        ## Phase 2: Erste SELECT-Abfragen (25 Minuten)

        ### 🟢 Aufgabe 2.1: Alle Daten anzeigen (geführt)

        Die einfachste Abfrage zeigt alle Spalten und Zeilen mit `SELECT *`:
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT *
        FROM bundesliga
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 2.2: Bestimmte Spalten auswählen (geführt)

        Zeigen Sie nur Mannschaft und Punkte:
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte
        FROM bundesliga
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟡 Aufgabe 2.3: Drei Spalten auswählen (scaffolded)

        Ergänze den folgenden Befehl, um Mannschaft, Siege und Niederlagen anzuzeigen:
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Ergänze die fehlende Spalte
    _df = mo.sql(
        f"""
        SELECT ???
        FROM bundesliga
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟣 Aufgabe 2.4: Vorhersage

        **Bevor Sie die Abfrage ausführen:** Wie viele Zeilen wird das Ergebnis haben?

        ```sql
        SELECT Mannschaft, Tordifferenz
        FROM bundesliga
        ```

        *Überlegen Sie zuerst, dann führen Sie aus:*
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Tordifferenz
        FROM bundesliga
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Antwort:** 18 Zeilen (alle Teams der Bundesliga), da kein WHERE-Filter verwendet wird.

        ---

        ### 🔵 Aufgabe 2.5: Selbstständig - Torstatistik

        Schreiben Sie eine Abfrage, die zeigt:
        - Mannschaft
        - ToreGeschossen
        - ToreKassiert
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Ihre Lösung hier:
    _df = mo.sql(
        f"""
        SELECT Mannschaft, ToreGeschossen, ToreKassiert
        FROM bundesliga
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 2.6: Selbstständig - Spielstatistik

        Zeigen Sie für jedes Team:
        - Mannschaft
        - Spiele
        - Siege
        - Unentschieden
        - Niederlagen
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Ihre Lösung hier:
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Spiele, Siege, Unentschieden, Niederlagen
        FROM bundesliga
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 2.7: Debugging - Finden Sie den Fehler!

        Diese Abfrage hat einen Syntaxfehler. Finden und beheben Sie ihn:

        ```sql
        SELECT Mannschaft Punkte
        FROM bundesliga
        ```
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Korrigieren Sie die Abfrage (Hinweis: Es fehlt etwas zwischen den Spaltennamen)
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte
        FROM bundesliga
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 2.8: Debugging - Spaltenname

        Diese Abfrage hat einen Fehler. Was stimmt nicht?

        ```sql
        SELECT Manschaft, Punkte
        FROM bundesliga
        ```
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Korrigieren Sie den Spaltennamen
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte
        FROM bundesliga
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 4: Filtern mit WHERE (25 Minuten)

        Mit `WHERE` können wir Zeilen filtern, die bestimmte Bedingungen erfüllen.

        ### 🟢 Aufgabe 4.1: Teams mit vielen Punkten (geführt)

        Zeigen Sie alle Teams mit mehr als 30 Punkten:
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte
        FROM bundesliga
        WHERE Punkte > 30
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 4.2: Teams mit negativer Tordifferenz (geführt)
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Tordifferenz
        FROM bundesliga
        WHERE Tordifferenz < 0
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 4.3: Exakter Vergleich (geführt)

        Finden Sie Teams mit genau 19 Spielen:
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Spiele
        FROM bundesliga
        WHERE Spiele = 19
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟣 Aufgabe 4.4: Vorhersage

        **Bevor Sie ausführen:** Wie viele Teams haben mindestens 10 Siege?

        Schätzen Sie, dann prüfen Sie:
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Siege
        FROM bundesliga
        WHERE Siege >= 10
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 4.5: Selbstständig - Wenig Niederlagen

        Finden Sie alle Teams mit weniger als 5 Niederlagen.
        Zeigen Sie Mannschaft und Niederlagen.
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Ihre Lösung:
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Niederlagen
        FROM bundesliga
        WHERE Niederlagen < 5
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 4.6: Selbstständig - Tore

        Finden Sie alle Teams, die mehr als 35 Tore geschossen haben.
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Ihre Lösung:
    _df = mo.sql(
        f"""
        SELECT Mannschaft, ToreGeschossen
        FROM bundesliga
        WHERE ToreGeschossen > 35
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 4.7: Debugging - Textvergleich

        Diese Abfrage soll Bayern München finden, aber funktioniert nicht:

        ```sql
        SELECT *
        FROM bundesliga
        WHERE Mannschaft = Bayern München
        ```

        Was fehlt?
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Korrigieren Sie die Abfrage (Hinweis: Text braucht Anführungszeichen)
    _df = mo.sql(
        f"""
        SELECT *
        FROM bundesliga
        WHERE Mannschaft = 'Bayern München'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 4.8: Debugging - Operator

        Diese Abfrage soll Teams mit mindestens 25 Punkten finden.
        Der Operator ist falsch. Korrigieren Sie ihn:

        ```sql
        SELECT Mannschaft, Punkte
        FROM bundesliga
        WHERE Punkte > 25
        ```

        (Hinweis: "mindestens" bedeutet "größer oder gleich")
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Korrigieren Sie den Operator
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte
        FROM bundesliga
        WHERE Punkte >= 25
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 6: Komplexe Abfragen mit AND, OR, NOT (40 Minuten)

        Jetzt kombinieren wir mehrere Bedingungen!

        ### 🟢 Aufgabe 6.1: AND - Beide Bedingungen (geführt)

        Teams mit vielen Siegen UND wenig Niederlagen:
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Siege, Niederlagen
        FROM bundesliga
        WHERE Siege > 8 AND Niederlagen < 5
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 6.2: OR - Mindestens eine Bedingung (geführt)

        Teams mit vielen Punkten ODER guter Tordifferenz:
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte, Tordifferenz
        FROM bundesliga
        WHERE Punkte > 35 OR Tordifferenz > 15
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 6.3: NOT - Ausschließen (geführt)

        Alle Teams außer Bayern München:
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte
        FROM bundesliga
        WHERE NOT Mannschaft = 'Bayern München'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 6.4: BETWEEN - Wertebereich (geführt)

        Teams mit 20 bis 30 Punkten (inklusiv):
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte
        FROM bundesliga
        WHERE Punkte BETWEEN 20 AND 30
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 6.5: IN - Werteliste (geführt)

        Nur bestimmte Teams anzeigen:
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte
        FROM bundesliga
        WHERE Mannschaft IN ('Bayern München', 'Borussia Dortmund', 'RB Leipzig')
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 Aufgabe 6.6: LIKE - Mustersuche (geführt)

        Teams, deren Name mit 'B' beginnt:
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft
        FROM bundesliga
        WHERE Mannschaft LIKE 'B%'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟣 Aufgabe 6.7: Vorhersage - AND vs OR

        **Welche Abfrage liefert MEHR Ergebnisse?**

        A) `WHERE Punkte > 30 AND Siege > 10`
        B) `WHERE Punkte > 30 OR Siege > 10`

        Überlegen Sie zuerst, dann testen Sie beide:
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Abfrage A: AND
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte, Siege
        FROM bundesliga
        WHERE Punkte > 30 AND Siege > 10
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Abfrage B: OR
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte, Siege
        FROM bundesliga
        WHERE Punkte > 30 OR Siege > 10
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Erklärung:** OR liefert mehr Ergebnisse, weil nur EINE Bedingung erfüllt sein muss. AND ist restriktiver.

        ---

        ### 🔵 Aufgabe 6.8: Selbstständig - Kombinierte Bedingung

        Finden Sie Teams, die:
        - Mehr als 30 Tore geschossen haben UND
        - Weniger als 25 Tore kassiert haben

        Zeigen Sie Mannschaft, ToreGeschossen, ToreKassiert.
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Ihre Lösung:
    _df = mo.sql(
        f"""
        SELECT Mannschaft, ToreGeschossen, ToreKassiert
        FROM bundesliga
        WHERE ToreGeschossen > 30 AND ToreKassiert < 25
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 6.9: Selbstständig - Abstiegskandidaten

        Finden Sie potenzielle Abstiegskandidaten:
        - Weniger als 20 Punkte ODER
        - Mehr als 10 Niederlagen

        Zeigen Sie Mannschaft, Punkte, Niederlagen.
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Ihre Lösung:
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte, Niederlagen
        FROM bundesliga
        WHERE Punkte < 20 OR Niederlagen > 10
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 Aufgabe 6.10: Selbstständig - LIKE

        Finden Sie alle Teams mit "Borussia" im Namen.

        (Hinweis: Verwenden Sie `%` vor und nach dem Suchbegriff)
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Ihre Lösung:
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte
        FROM bundesliga
        WHERE Mannschaft LIKE '%Borussia%'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 6.11: Debugging - Klammern

        Diese Abfrage soll Teams finden, die ENTWEDER viele Punkte (>35) ODER viele Tore (>40) haben, UND dabei weniger als 5 Niederlagen haben.

        Die Abfrage ist syntaktisch korrekt, liefert aber falsche Ergebnisse. Warum?

        ```sql
        SELECT Mannschaft, Punkte, ToreGeschossen, Niederlagen
        FROM bundesliga
        WHERE Punkte > 35 OR ToreGeschossen > 40 AND Niederlagen < 5
        ```
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Korrigieren Sie mit Klammern
    # (Hinweis: AND bindet stärker als OR!)
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte, ToreGeschossen, Niederlagen
        FROM bundesliga
        WHERE (Punkte > 35 OR ToreGeschossen > 40) AND Niederlagen < 5
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔴 Aufgabe 6.12: Debugging - LIKE

        Diese Abfrage soll alle Teams finden, die "FC" im Namen haben.
        Sie findet aber nicht alle. Was ist das Problem?

        ```sql
        SELECT Mannschaft
        FROM bundesliga
        WHERE Mannschaft LIKE 'FC%'
        ```
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Korrigieren Sie das LIKE-Muster
    # (Hinweis: "FC" kann auch mitten im Namen stehen)
    _df = mo.sql(
        f"""
        SELECT Mannschaft
        FROM bundesliga
        WHERE Mannschaft LIKE '%FC%'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Freie Exploration (verbleibende Zeit)

        Jetzt sind Sie dran! Beantworten Sie diese Fragen mit SQL:

        ### Frage 1: Effizienz
        Welche Teams haben mehr Siege als Niederlagen? (Hinweis: Spalten können verglichen werden!)
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Ihre Abfrage:
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Siege, Niederlagen
        FROM bundesliga
        WHERE Siege > Niederlagen
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Frage 2: Tormaschinen
        Welche Teams haben mehr als doppelt so viele Tore geschossen wie kassiert?
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Ihre Abfrage:
    _df = mo.sql(
        f"""
        SELECT Mannschaft, ToreGeschossen, ToreKassiert
        FROM bundesliga
        WHERE ToreGeschossen > 2 * ToreKassiert
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Frage 3: Mittelmäßig
        Welche Teams sind im Mittelfeld? (Zwischen 20 und 35 Punkte, nicht "Bayern" oder "Kiel" im Namen)
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Ihre Abfrage:
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte
        FROM bundesliga
        WHERE Punkte BETWEEN 20 AND 35
          AND Mannschaft NOT LIKE '%Bayern%'
          AND Mannschaft NOT LIKE '%Kiel%'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Frage 4: Eigene Frage
        Formulieren Sie eine eigene Frage und beantworten Sie sie mit SQL!
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Ihre eigene Frage und Abfrage:
    _df = mo.sql(
        f"""
        SELECT *
        FROM bundesliga
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 7: Erste Visualisierungen 📊

        **Der Workflow:**
        ```
        Datenbank → SQL → Abfrageergebnis → plotly → Grafik
        ```

        SQL liefert Daten – Diagramme machen Muster sichtbar!
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Zwei Datenstrukturen

        | Typ | Beschreibung | Chart |
        |-----|--------------|-------|
        | **Querschnitt** | 18 Teams, 1 Zeitpunkt | Balkendiagramm |
        | **Zeitreihe** | 1 Team, 34 Spieltage | Liniendiagramm |

        Wir haben beide: `bundesliga` (Endstand) und `bundesliga_spieltage` (Verlauf)
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 7.1 Geführt: Balkendiagramm (Querschnitt)

        Welche Teams haben die meisten Punkte?
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    import plotly.express as px

    # SQL liefert die Daten
    top_teams = mo.sql(
        f"""
        SELECT Mannschaft, Punkte
        FROM bundesliga
        WHERE Punkte > 50
        """
    )
    return px, top_teams


@app.cell
def _(px, top_teams):
    # Visualisierung: Balkendiagramm
    fig_bar = px.bar(
        top_teams.to_pandas(),
        x="Mannschaft",
        y="Punkte",
        title="Top Teams nach Punkten",
        color="Punkte",
        color_continuous_scale="Blues"
    )
    fig_bar
    return (fig_bar,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🟢 7.2 Geführt: Liniendiagramm (Zeitreihe)

        Wie entwickelte sich Bayern über die Saison?
        """
    )
    return


@app.cell
def _(bundesliga_spieltage, mo, px):
    # SQL: Ein Team über alle Spieltage
    bayern_verlauf = mo.sql(
        f"""
        SELECT Spieltag, Punkte_Kumuliert
        FROM bundesliga_spieltage
        WHERE Mannschaft = 'Bayern München'
        """
    )

    # Visualisierung: Liniendiagramm
    fig_line = px.line(
        bayern_verlauf.to_pandas(),
        x="Spieltag",
        y="Punkte_Kumuliert",
        title="Bayern München: Punkteverlauf",
        markers=True
    )
    fig_line
    return bayern_verlauf, fig_line


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### 🔵 7.3 Selbstständig: Eigene Visualisierung

        Erstelle ein Diagramm deiner Wahl:
        - Balkendiagramm: Welche Teams kassieren die meisten Gegentore? (`WHERE ToreKassiert > 60`)
        - Liniendiagramm: Wie entwickelte sich Dortmund über die Saison?
        """
    )
    return


@app.cell
def _(bundesliga, bundesliga_spieltage, mo, px):
    # Deine Lösung hier:
    meine_daten = mo.sql(
        f"""
        SELECT Mannschaft, ToreKassiert
        FROM bundesliga
        WHERE ToreKassiert > 60
        """
    )

    fig_own = px.bar(meine_daten.to_pandas(), x="Mannschaft", y="ToreKassiert")
    fig_own
    return fig_own, meine_daten


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Zusammenfassung

        | Konzept | Syntax | Beispiel |
        |---------|--------|----------|
        | Alle Spalten | `SELECT *` | `SELECT * FROM tabelle` |
        | Bestimmte Spalten | `SELECT spalte1, spalte2` | `SELECT Mannschaft, Punkte` |
        | Filtern | `WHERE bedingung` | `WHERE Punkte > 30` |
        | Und-Verknüpfung | `AND` | `WHERE Siege > 10 AND Niederlagen < 5` |
        | Oder-Verknüpfung | `OR` | `WHERE Punkte > 30 OR Tordifferenz > 10` |
        | Negation | `NOT` | `WHERE NOT Mannschaft = 'Bayern'` |
        | Wertebereich | `BETWEEN` | `WHERE Punkte BETWEEN 20 AND 30` |
        | Werteliste | `IN` | `WHERE Mannschaft IN ('A', 'B', 'C')` |
        | Mustersuche | `LIKE` | `WHERE Mannschaft LIKE 'B%'` |

        ### Visualisierung
        | Charttyp | Funktion | Verwendung |
        |----------|----------|------------|
        | Balkendiagramm | `px.bar()` | Querschnitt (Kategorien vergleichen) |
        | Liniendiagramm | `px.line()` | Zeitreihe (Entwicklung zeigen) |

        ### Häufige Fehler vermeiden:
        - ✅ Komma zwischen Spalten: `SELECT a, b`
        - ✅ Text in Anführungszeichen: `WHERE name = 'Text'`
        - ✅ Klammern bei komplexen Bedingungen: `WHERE (a OR b) AND c`
        - ✅ Richtige Operatoren: `>=` für "mindestens", `<=` für "höchstens"

        **Nächste Session:** Sortieren, DISTINCT, NULL-Werte, mehr Visualisierung
        """
    )
    return


if __name__ == "__main__":
    app.run()
