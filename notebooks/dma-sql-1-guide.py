# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "polars",
#     "plotly",
# ]
# ///

import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium", app_title="DMA Session 1: SQL-Grundlagen — Guide")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Session 1: SQL-Grundlagen — Guide

    **Kursfahrplan:** **▸ I: SQL-Grundlagen (S1–4)** · II: Datenmodellierung (S5–7) · III: Fortgeschrittenes SQL (S8–9) · IV: Datenanalyse (S10–13)

    ### Lernziele

    Nach dieser Session können Sie:

    - Daten mit `SELECT` abfragen und Spalten auswählen
    - Zeilen mit `WHERE` filtern (Vergleichsoperatoren, Text)
    - Bedingungen mit `AND`, `OR`, `NOT` kombinieren
    - `BETWEEN`, `IN`, `LIKE` einsetzen
    - Den richtigen Diagrammtyp (Balken vs. Linie) wählen

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Wie arbeiten wir?

    Wir nutzen **marimo** — ein interaktives Python-Notebook — zusammen mit **DuckDB**, einer eingebetteten SQL-Datenbank.

    - SQL-Abfragen werden direkt im Notebook ausgeführt
    - Ergebnisse erscheinen sofort als Tabelle
    - Theorie steht in diesem **Guide-Notebook**
    - Übungen machen Sie im **Übungs-Notebook** → `01-sql-grundlagen.py`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Daten laden
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    import polars as pl

    try:
        csv_path = mo.notebook_location() / "public" / "bundesliga.csv"
        bundesliga = pl.read_csv(str(csv_path))

        spieltage_path = mo.notebook_location() / "public" / "bundesliga_spieltage.csv"
        bundesliga_spieltage = pl.read_csv(str(spieltage_path))

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
        bundesliga_spieltage = pl.DataFrame({
            "Mannschaft": ["Bayern München"] * 5,
            "Spieltag": [1, 2, 3, 4, 5],
            "Punkte_Kumuliert": [3, 6, 9, 10, 13],
        })
        daten_quelle = "Offline-Daten (Fallback)"
        mo.callout(mo.md("**Hinweis:** CSV konnte nicht geladen werden. Es werden Beispieldaten verwendet."), kind="warn")

    return bundesliga, bundesliga_spieltage, daten_quelle


@app.cell(hide_code=True)
def _(daten_quelle, mo):
    mo.md(f"""
    **Datenquelle:** {daten_quelle}

    **Verfügbare Spalten:** Mannschaft, Spiele, Siege, Unentschieden, Niederlagen, Tore, Gegentore, Tordifferenz, Punkte

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Phase 1: Was sind Datenbanken?

    ### Die DIKW-Pyramide

    ```
         Weisheit        ← Erfahrung + Urteilsvermögen
        Wissen           ← Verknüpftes Verständnis
       Information       ← Daten mit Kontext & Bedeutung
      Daten              ← Rohe Fakten & Zahlen
    ```

    **Beispiel Bundesliga:**
    - **Daten:** `74` (eine Zahl ohne Kontext)
    - **Information:** Bayern München hat 74 Punkte
    - **Wissen:** 74 Punkte reichen für den Meistertitel
    - **Weisheit:** Investitionen in Kadertiefe zahlen sich langfristig aus

    ### Aufbau einer Tabelle

    | Konzept | Bedeutung | Beispiel |
    |---------|-----------|----------|
    | **Tabelle** | Sammlung zusammengehöriger Daten | `bundesliga` |
    | **Spalte** (Attribut) | Eine Eigenschaft | `Mannschaft`, `Punkte` |
    | **Zeile** (Datensatz) | Ein konkreter Eintrag | Bayern München, 74 Punkte |
    | **Wert** (Zelle) | Einzelner Datenpunkt | `74` |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SELECT — Daten abfragen

    Die grundlegende SQL-Syntax:

    ```sql
    SELECT spalte1, spalte2   -- Was wollen wir sehen?
    FROM tabelle               -- Woher kommen die Daten?
    ```

    - `SELECT *` → alle Spalten
    - `SELECT spalte1, spalte2` → nur bestimmte Spalten

    ---

    ### Geführtes Beispiel: Alle Daten anzeigen
    """)
    return


@app.cell(hide_code=True)
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT *
        FROM bundesliga
        LIMIT 5
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel: Bestimmte Spalten auswählen
    """)
    return


@app.cell(hide_code=True)
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
    mo.md(r"""
    ### Probieren Sie selbst: Spaltenauswahl

    Ändern Sie die Abfrage unten — wählen Sie andere Spalten aus! Welche Spalten gibt es?

    `Mannschaft, Spiele, Siege, Unentschieden, Niederlagen, Tore, Gegentore, Tordifferenz, Punkte`
    """)
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Siege, Niederlagen
        FROM bundesliga
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    **Jetzt zum Übungs-Notebook → Aufgaben 2.x**

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Phase 3: Filtern mit WHERE

    Mit `WHERE` können wir Zeilen filtern, die bestimmte Bedingungen erfüllen:

    ```sql
    SELECT spalte1, spalte2
    FROM tabelle
    WHERE bedingung
    ```

    ### Vergleichsoperatoren

    | Operator | Bedeutung | Beispiel |
    |----------|-----------|----------|
    | `=` | gleich | `WHERE Punkte = 30` |
    | `<>` oder `!=` | ungleich | `WHERE Mannschaft <> 'Bayern München'` |
    | `>` | größer | `WHERE Punkte > 30` |
    | `<` | kleiner | `WHERE Tordifferenz < 0` |
    | `>=` | größer oder gleich | `WHERE Siege >= 10` |
    | `<=` | kleiner oder gleich | `WHERE Niederlagen <= 5` |

    ### Textvergleiche

    Text muss immer in **einfache Anführungszeichen** gesetzt werden:

    ```sql
    WHERE Mannschaft = 'Bayern München'   -- ✅ richtig
    WHERE Mannschaft = Bayern München     -- ❌ Fehler!
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel: Filtern nach Punkten
    """)
    return


@app.cell(hide_code=True)
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
    mo.md(r"""
    ### Probieren Sie selbst: Filter ändern

    Experimentieren Sie mit der WHERE-Bedingung! Versuchen Sie:
    - Andere Vergleichsoperatoren: `<`, `>=`, `<=`, `<>`
    - Andere Spalten: `Siege`, `Tore`, `Tordifferenz`
    """)
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte, Tore
        FROM bundesliga
        WHERE Tore > 50
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Häufige Fehler beim Filtern

    | Fehler | Problem | Korrektur |
    |--------|---------|-----------|
    | `WHERE Mannschaft = Bayern` | Text ohne Anführungszeichen | `WHERE Mannschaft = 'Bayern München'` |
    | `WHERE Punkte > 25` statt `>= 25` | "mindestens" = größer **oder gleich** | `WHERE Punkte >= 25` |
    | `SELECT Mannschaft Punkte` | Fehlendes Komma | `SELECT Mannschaft, Punkte` |
    | `SELECT Manschaft` | Tippfehler im Spaltennamen | `SELECT Mannschaft` |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Vorhersage 1
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    vorhersage_select = mo.ui.radio(
        options={
            "1": "Nur 1 Zeile",
            "alle": "Alle Zeilen der Tabelle",
            "kommt_drauf_an": "Kommt auf die ausgewählten Spalten an",
        },
        label="Wie viele Zeilen liefert `SELECT Mannschaft, Tordifferenz FROM bundesliga` (ohne WHERE)?"
    )
    vorhersage_select
    return (vorhersage_select,)


@app.cell(hide_code=True)
def _(vorhersage_select, mo):
    if vorhersage_select.value == "alle":
        mo.output.replace(mo.md("✅ **Richtig!** Ohne `WHERE`-Filter werden **alle Zeilen** der Tabelle zurückgegeben. `SELECT` wählt nur die **Spalten** aus, nicht die Zeilen."))
    elif vorhersage_select.value == "1":
        mo.output.replace(mo.md("❌ Nicht ganz. `SELECT` wählt nur die **Spalten** aus, nicht die Zeilen. Ohne `WHERE`-Filter werden **alle Zeilen** der Tabelle zurückgegeben — egal wie viele Spalten Sie auswählen."))
    elif vorhersage_select.value == "kommt_drauf_an":
        mo.output.replace(mo.md("❌ Nicht ganz. Die Spaltenauswahl hat keinen Einfluss auf die Zeilenanzahl. Ohne `WHERE` werden **immer alle Zeilen** der Tabelle zurückgegeben. `SELECT` wählt Spalten, `WHERE` filtert Zeilen."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    **Jetzt zum Übungs-Notebook → Aufgaben 4.x**

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Phase 5: Logische Operatoren — AND, OR, NOT

    ### Bedingungen kombinieren

    | Operator | Bedeutung | Ergebnis |
    |----------|-----------|----------|
    | `AND` | Beide Bedingungen müssen gelten | Weniger Ergebnisse (restriktiver) |
    | `OR` | Mindestens eine Bedingung muss gelten | Mehr Ergebnisse (erweitert) |
    | `NOT` | Bedingung umkehren | Gegenteil |

    ### Wahrheitstabellen

    **AND** — beide müssen wahr sein:

    | A | B | A AND B |
    |---|---|---------|
    | ✅ | ✅ | ✅ |
    | ✅ | ❌ | ❌ |
    | ❌ | ✅ | ❌ |
    | ❌ | ❌ | ❌ |

    **OR** — mindestens eines muss wahr sein:

    | A | B | A OR B |
    |---|---|--------|
    | ✅ | ✅ | ✅ |
    | ✅ | ❌ | ✅ |
    | ❌ | ✅ | ✅ |
    | ❌ | ❌ | ❌ |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Spezialoperatoren

    | Operator | Syntax | Beispiel |
    |----------|--------|----------|
    | `BETWEEN` | `WHERE spalte BETWEEN a AND b` | `WHERE Punkte BETWEEN 20 AND 30` |
    | `IN` | `WHERE spalte IN (wert1, wert2)` | `WHERE Mannschaft IN ('Bayern', 'Dortmund')` |
    | `LIKE` | `WHERE spalte LIKE 'Muster'` | `WHERE Mannschaft LIKE 'B%'` |

    **LIKE-Wildcards:**
    - `%` — beliebig viele Zeichen: `'B%'` findet "Bayern", "Borussia"
    - `_` — genau ein Zeichen: `'_FC'` findet "1FC"

    ### Operatorvorrang

    `AND` bindet stärker als `OR` — wie Multiplikation vor Addition!

    ```sql
    -- ACHTUNG: AND wird zuerst ausgewertet!
    WHERE A OR B AND C      -- bedeutet: A OR (B AND C)

    -- Mit Klammern explizit machen:
    WHERE (A OR B) AND C    -- erst OR, dann AND
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Vorhersage 2
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    vorhersage_and_or = mo.ui.radio(
        options={
            "and": "AND liefert mehr Ergebnisse",
            "or": "OR liefert mehr Ergebnisse",
            "gleich": "Beide liefern gleich viele Ergebnisse",
        },
        label="Welcher Operator liefert in der Regel mehr Ergebnisse: AND oder OR?"
    )
    vorhersage_and_or
    return (vorhersage_and_or,)


@app.cell(hide_code=True)
def _(vorhersage_and_or, mo):
    if vorhersage_and_or.value == "or":
        mo.output.replace(mo.md("✅ **Richtig!** `OR` liefert mehr Ergebnisse, weil nur **eine** der Bedingungen erfüllt sein muss. `AND` ist restriktiver — **beide** Bedingungen müssen gelten."))
    elif vorhersage_and_or.value == "and":
        mo.output.replace(mo.md("❌ Nicht ganz. `AND` ist **restriktiver** — **beide** Bedingungen müssen gleichzeitig gelten. Das schließt mehr Zeilen aus. `OR` dagegen braucht nur **eine** wahre Bedingung und liefert daher mehr Ergebnisse."))
    elif vorhersage_and_or.value == "gleich":
        mo.output.replace(mo.md("❌ Nicht ganz. `AND` und `OR` liefern unterschiedlich viele Ergebnisse: `OR` erweitert die Ergebnismenge (mindestens eine Bedingung reicht), `AND` schränkt sie ein (beide müssen gelten). Daher liefert `OR` in der Regel **mehr** Ergebnisse."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Quiz: Operatorvorrang
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    quiz_operator = mo.ui.radio(
        options={
            "and_or": "AND hat Vorrang vor OR (wie Multiplikation vor Addition)",
            "or_and": "OR hat Vorrang vor AND",
            "gleich": "Beide haben den gleichen Vorrang (links nach rechts)",
            "klammern": "Es gibt keinen festen Vorrang, man muss immer Klammern setzen"
        },
        label="**Quiz:** Welche Aussage zu AND und OR in SQL ist korrekt?"
    )
    quiz_operator
    return (quiz_operator,)


@app.cell(hide_code=True)
def _(quiz_operator, mo):
    if quiz_operator.value == "and_or":
        mo.output.replace(mo.md("✅ **Richtig!** AND bindet stärker als OR, genau wie `*` vor `+` in der Mathematik. Deshalb sind Klammern bei OR wichtig: `WHERE (A OR B) AND C` ist etwas anderes als `WHERE A OR B AND C`."))
    elif quiz_operator.value == "or_and":
        mo.output.replace(mo.md("❌ Genau umgekehrt! **AND** bindet stärker als OR — wie Multiplikation (`×`) vor Addition (`+`). Eselsbrücke: **A**ND = **A**nmultiplizieren."))
    elif quiz_operator.value == "gleich":
        mo.output.replace(mo.md("❌ Nicht ganz. AND und OR haben **unterschiedlichen** Vorrang: AND bindet stärker (wie `×` vor `+` in der Mathematik). Deshalb ist `A OR B AND C` dasselbe wie `A OR (B AND C)`."))
    elif quiz_operator.value == "klammern":
        mo.output.replace(mo.md("❌ Es gibt einen festen Vorrang: **AND** bindet stärker als OR. Klammern sind also nicht zwingend nötig, machen den Code aber lesbarer. Ohne Klammern gilt: `A OR B AND C` = `A OR (B AND C)`."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    **Jetzt zum Übungs-Notebook → Aufgaben 6.x**

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Phase 7: Erste Visualisierungen

    ### Der Workflow

    ```
    Datenbank → SQL-Abfrage → Ergebnistabelle → plotly → Diagramm
    ```

    SQL liefert die Daten — Diagramme machen Muster sichtbar!

    ### Zwei Datenstrukturen — Zwei Diagrammtypen

    | Datenstruktur | Beschreibung | Diagrammtyp |
    |---------------|-------------|-------------|
    | **Querschnitt** | Viele Einheiten, ein Zeitpunkt (18 Teams, Endstand) | **Balkendiagramm** |
    | **Zeitreihe** | Eine Einheit, viele Zeitpunkte (Bayern, 34 Spieltage) | **Liniendiagramm** |

    Wir haben beide Datenstrukturen:
    - `bundesliga` → Querschnitt (Endstand der Saison)
    - `bundesliga_spieltage` → Zeitreihe (Verlauf über Spieltage)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel: Balkendiagramm (Querschnitt)

    Welche Teams haben die meisten Punkte?
    """)
    return


@app.cell(hide_code=True)
def _():
    import plotly.express as px
    return (px,)


@app.cell(hide_code=True)
def _(bundesliga, mo, px):
    top_teams = mo.sql(
        f"""
        SELECT Mannschaft, Punkte
        FROM bundesliga
        WHERE Punkte > 50
        """
    )

    fig_bar = px.bar(
        top_teams,
        x="Mannschaft",
        y="Punkte",
        title="Top Teams nach Punkten",
        color="Punkte",
        color_continuous_scale="Blues"
    )
    fig_bar
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel: Liniendiagramm (Zeitreihe)

    Wie entwickelte sich Bayern über die Saison?
    """)
    return


@app.cell(hide_code=True)
def _(bundesliga_spieltage, mo, px):
    bayern_verlauf = mo.sql(
        f"""
        SELECT Spieltag, Punkte_Kumuliert
        FROM bundesliga_spieltage
        WHERE Mannschaft = 'Bayern München'
        """
    )

    fig_line = px.line(
        bayern_verlauf,
        x="Spieltag",
        y="Punkte_Kumuliert",
        title="Bayern München: Punkteverlauf",
        markers=True
    )
    fig_line
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Viz-Choice: Den richtigen Diagrammtyp wählen
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    viz_choice = mo.ui.radio(
        options={
            "bar": "Balkendiagramm",
            "line": "Liniendiagramm",
            "scatter": "Streudiagramm",
            "histogram": "Histogramm",
        },
        label="Sie wollen zeigen, wie sich Bayerns Punkte über die Saison entwickeln. Welcher Diagrammtyp passt am besten?"
    )
    viz_choice
    return (viz_choice,)


@app.cell(hide_code=True)
def _(viz_choice, mo):
    if viz_choice.value == "line":
        mo.output.replace(mo.md("✅ **Richtig!** Ein **Liniendiagramm** ist ideal für **Zeitreihen** — es zeigt die Entwicklung eines Werts über die Zeit. Die x-Achse ist der Spieltag, die y-Achse die kumulierten Punkte."))
    elif viz_choice.value == "bar":
        mo.output.replace(mo.md("❌ Nicht ganz. Ein Balkendiagramm eignet sich für **Querschnittsdaten** (Kategorien vergleichen), z.B. alle 18 Teams im Vergleich. Für eine **Zeitreihe** (Entwicklung über die Saison) passt ein **Liniendiagramm** besser."))
    elif viz_choice.value == "scatter":
        mo.output.replace(mo.md("❌ Nicht ganz. Ein Streudiagramm zeigt den **Zusammenhang** zwischen zwei Variablen (z.B. Tore vs. Punkte). Für eine **Zeitreihe** (Entwicklung über die Saison) passt ein **Liniendiagramm** besser."))
    elif viz_choice.value == "histogram":
        mo.output.replace(mo.md("❌ Nicht ganz. Ein Histogramm zeigt die **Verteilung** einer einzelnen Variable (z.B. wie viele Teams haben 20-30 Punkte). Für eine **Zeitreihe** (Entwicklung über die Saison) passt ein **Liniendiagramm** besser."))
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
    selbsttest = mo.ui.radio(
        options={
            "where": "Mit WHERE",
            "select": "Mit SELECT",
            "from": "Gar nicht — SQL zeigt immer alle Zeilen",
        },
        label="Wie begrenzen Sie in SQL die **Zeilen** einer Abfrage?"
    )
    selbsttest
    return (selbsttest,)


@app.cell(hide_code=True)
def _(selbsttest, mo):
    if selbsttest.value == "where":
        mo.output.replace(mo.md("✅ **Richtig!** `WHERE` filtert Zeilen nach einer Bedingung. `SELECT` wählt hingegen nur die **Spalten** aus."))
    elif selbsttest.value == "select":
        mo.output.replace(mo.md("❌ `SELECT` wählt **Spalten** aus, nicht Zeilen. Um Zeilen zu filtern, verwenden Sie `WHERE` mit einer Bedingung."))
    elif selbsttest.value == "from":
        mo.output.replace(mo.md("❌ SQL kann Zeilen filtern — dafür gibt es `WHERE`. Ohne `WHERE` werden zwar alle Zeilen angezeigt, aber mit `WHERE bedingung` bekommen Sie nur die passenden Zeilen."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Zusammenfassung

    ### SQL-Grundlagen

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

    | Datenstruktur | Charttyp | Funktion |
    |---------------|----------|----------|
    | Querschnitt (Kategorien) | Balkendiagramm | `px.bar()` |
    | Zeitreihe (Entwicklung) | Liniendiagramm | `px.line()` |

    ### Häufige Fehler vermeiden

    - Komma zwischen Spalten: `SELECT a, b` (nicht `SELECT a b`)
    - Text in Anführungszeichen: `WHERE name = 'Text'`
    - Klammern bei komplexen Bedingungen: `WHERE (a OR b) AND c`
    - Richtige Operatoren: `>=` für "mindestens", `<=` für "höchstens"

    ### Ausblick Session 2

    Nächste Woche: Sortieren mit `ORDER BY`, eindeutige Werte mit `DISTINCT`, `NULL`-Werte und mehr Visualisierung!
    """)
    return


if __name__ == "__main__":
    app.run()
