# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "polars",
#     "pandas",
#     "plotly",
# ]
# ///

import marimo

__generated_with = "0.13.0"
app = marimo.App(
    width="medium",
    app_title="DMA Session 3: Aggregation & Gruppierung — Guide",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 3: Aggregation & Gruppierung — Guide

        **Kursfahrplan:** **▸ I: SQL-Grundlagen (S1–4)** · II: Datenmodellierung (S5–7) · III: Fortgeschrittenes SQL (S8–9) · IV: Datenanalyse (S10–13)

        ### Lernziele

        Nach dieser Session können Sie:

        - **Aggregatfunktionen** anwenden: COUNT, SUM, AVG, MIN, MAX
        - Daten mit **GROUP BY** gruppieren
        - Gruppen mit **HAVING** filtern
        - Den Unterschied zwischen **WHERE** und **HAVING** erklären
        - Die SQL-**Ausführungsreihenfolge** beschreiben

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Daten laden

        Wir arbeiten heute mit:
        1. **Bundesliga-Tabelle** (bekannt aus den letzten Sessions)
        2. **Spieler-Daten** (erweitert mit mehr Spielern)
        """
    )
    return


@app.cell(hide_code=True)
def _():
    import polars as pl

    spieler = pl.DataFrame({
        "Name": ["Müller", "Neuer", "Kimmich", "Sané", "Musiala", "Gündogan",
                 "Havertz", "Wirtz", "Füllkrug", "Schlotterbeck", "Rüdiger", "Tah",
                 "Gnabry", "Goretzka", "ter Stegen", "Baumann"],
        "Vorname": ["Thomas", "Manuel", "Joshua", "Leroy", "Jamal", "İlkay",
                    "Kai", "Florian", "Niclas", "Nico", "Antonio", "Jonathan",
                    "Serge", "Leon", "Marc-André", "Oliver"],
        "Position": ["Sturm", "Tor", "Mittelfeld", "Sturm", "Mittelfeld", "Mittelfeld",
                     "Sturm", "Mittelfeld", "Sturm", "Abwehr", "Abwehr", "Abwehr",
                     "Sturm", "Mittelfeld", "Tor", "Tor"],
        "Verein": ["Bayern München", "Bayern München", "Bayern München", "Bayern München",
                   "Bayern München", "FC Barcelona", "Arsenal", "Bayer Leverkusen",
                   "West Ham", "Borussia Dortmund", "Real Madrid", "Bayer Leverkusen",
                   "Bayern München", "Bayern München", "FC Barcelona", "TSG Hoffenheim"],
        "Tore": [8, 0, 3, 5, 12, 4, 9, 11, 6, 1, 2, 0, 7, 2, 0, 0],
        "Vorlagen": [4, 0, 8, 3, 7, 2, 5, 9, 2, 0, 1, 0, 4, 3, 0, 0],
        "Alter": [35, 38, 29, 28, 21, 33, 25, 21, 31, 24, 31, 28, 28, 29, 32, 34],
        "Länderspiele": [131, 118, 91, 67, 35, 82, 47, 28, 20, 12, 70, 32, 42, 57, 40, 5]
    })
    return (spieler,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 2: Aggregatfunktionen

        Aggregatfunktionen berechnen **einen** Wert aus **vielen** Zeilen:

        | Funktion | Beschreibung | Beispiel |
        |----------|-------------|----------|
        | `COUNT(*)` | Zählt alle Zeilen | Wie viele Teams? |
        | `COUNT(spalte)` | Zählt nicht-NULL Werte | Wie viele mit Toren? |
        | `SUM(spalte)` | Summiert Werte | Gesamttore |
        | `AVG(spalte)` | Berechnet Durchschnitt | Durchschnittsalter |
        | `MIN(spalte)` | Kleinster Wert | Jüngstes Alter |
        | `MAX(spalte)` | Größter Wert | Meiste Tore |

        ```sql
        SELECT COUNT(*) AS Anzahl, AVG(Punkte) AS Durchschnitt
        FROM bundesliga
        ```
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel: COUNT
    """)
    return


@app.cell(hide_code=True)
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT COUNT(*) AS Anzahl_Spieler
        FROM spieler
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel: SUM und AVG
    """)
    return


@app.cell(hide_code=True)
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT
            SUM(Tore) AS Gesamttore,
            AVG(Tore) AS Durchschnitt_Tore,
            MIN("Alter") AS Jüngster,
            MAX("Alter") AS Ältester
        FROM spieler
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Probieren Sie selbst: Aggregatfunktionen

    Ändern Sie die Abfrage! Probieren Sie:
    - `COUNT(DISTINCT Position)` — Wie viele verschiedene Positionen gibt es?
    - `SUM(Vorlagen)` — Wie viele Vorlagen insgesamt?
    - `AVG("Alter")` — Durchschnittsalter? (Anführungszeichen um `Alter` weil es ein reserviertes Wort ist)
    """)
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT
            COUNT(*) AS Anzahl,
            SUM(Vorlagen) AS Gesamt_Vorlagen,
            AVG("Alter") AS Durchschnittsalter
        FROM spieler
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

        ## Phase 4: GROUP BY — Daten gruppieren

        ### Wie GROUP BY Daten "faltet"

        Ohne GROUP BY:
        ```
        Müller    | Sturm      | 8 Tore
        Neuer     | Tor        | 0 Tore
        Kimmich   | Mittelfeld | 3 Tore
        Sané      | Sturm      | 5 Tore
        Musiala   | Mittelfeld | 12 Tore
        ```

        Mit `GROUP BY Position`:
        ```
        Sturm      → [8, 5]      → AVG = 6.5, COUNT = 2
        Tor        → [0]         → AVG = 0.0, COUNT = 1
        Mittelfeld → [3, 12]     → AVG = 7.5, COUNT = 2
        ```

        **Goldene Regel:** Im `SELECT` dürfen nur stehen:
        1. Spalten, die in `GROUP BY` genannt sind
        2. Aggregatfunktionen (COUNT, SUM, AVG, MIN, MAX)

        ```sql
        SELECT Position, AVG(Tore) AS Schnitt_Tore
        FROM spieler
        GROUP BY Position
        ```
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Geführtes Beispiel: Gruppierung nach Position
    """)
    return


@app.cell(hide_code=True)
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT Position, COUNT(*) AS Anzahl, AVG(Tore) AS Schnitt_Tore
        FROM spieler
        GROUP BY Position
        ORDER BY Schnitt_Tore DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Probieren Sie selbst: GROUP BY

    Ändern Sie die Gruppierung! Probieren Sie `GROUP BY Verein` statt `GROUP BY Position`.
    Welcher Verein hat die meisten Spieler?
    """)
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT Verein, COUNT(*) AS Anzahl, AVG(Tore) AS Schnitt_Tore
        FROM spieler
        GROUP BY Verein
        ORDER BY Anzahl DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### SQL-Ausführungsreihenfolge

        SQL wird **nicht** in der Reihenfolge ausgeführt, in der wir es schreiben!

        ```
        1. FROM         ← Welche Tabelle?
        2. WHERE         ← Zeilen filtern (vor Gruppierung!)
        3. GROUP BY      ← Gruppen bilden
        4. HAVING        ← Gruppen filtern (nach Gruppierung!)
        5. SELECT        ← Spalten auswählen & berechnen
        6. ORDER BY      ← Sortieren
        7. LIMIT/OFFSET  ← Begrenzen
        ```

        Deshalb kann `WHERE` keine Aggregatfunktionen verwenden (die gibt es noch nicht!), aber `HAVING` schon.

        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 4.x**

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Phase 6: HAVING vs WHERE

        | | WHERE | HAVING |
        |---|-------|--------|
        | **Filtert** | Einzelne Zeilen | Ganze Gruppen |
        | **Wann** | Vor GROUP BY | Nach GROUP BY |
        | **Aggregat?** | Nein | Ja |
        | **Beispiel** | `WHERE Alter < 30` | `HAVING COUNT(*) > 3` |

        ```sql
        SELECT Verein, COUNT(*) AS Spieler
        FROM spieler
        WHERE "Alter" < 30          -- filtert Zeilen VOR Gruppierung
        GROUP BY Verein
        HAVING COUNT(*) >= 2         -- filtert Gruppen NACH Gruppierung
        ```
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Quiz: WHERE vs HAVING
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    quiz_where_having = mo.ui.radio(
        options={
            "correct": "WHERE filtert Zeilen vor GROUP BY, HAVING filtert Gruppen danach",
            "reversed": "HAVING filtert Zeilen vor GROUP BY, WHERE filtert Gruppen danach",
            "same": "WHERE und HAVING sind austauschbar — beide filtern Gruppen",
            "dtype": "WHERE ist für Zahlen, HAVING ist für Text",
        },
        label="**Quiz:** Was ist der Unterschied zwischen WHERE und HAVING?"
    )
    quiz_where_having
    return (quiz_where_having,)


@app.cell(hide_code=True)
def _(quiz_where_having, mo):
    if quiz_where_having.value == "correct":
        mo.output.replace(mo.md("✅ **Richtig!** WHERE filtert *einzelne Zeilen* bevor sie gruppiert werden. HAVING filtert *ganze Gruppen* nach der Aggregation. Deshalb kann HAVING Aggregatfunktionen wie COUNT(*) oder AVG() verwenden — WHERE nicht."))
    elif quiz_where_having.value == "reversed":
        mo.output.replace(mo.md("❌ Genau umgekehrt! **WHERE** filtert Zeilen *vor* GROUP BY, **HAVING** filtert Gruppen *danach*. Eselsbrücke: WHERE → WHERE are the rows (Zeilen), HAVING → HAVING grouped (Gruppen)."))
    elif quiz_where_having.value == "same":
        mo.output.replace(mo.md("❌ WHERE und HAVING sind **nicht** austauschbar. WHERE filtert *einzelne Zeilen* vor der Gruppierung und kann keine Aggregatfunktionen verwenden. HAVING filtert *Gruppen* nach der Aggregation und kann z.B. `COUNT(*) > 5` prüfen."))
    elif quiz_where_having.value == "dtype":
        mo.output.replace(mo.md("❌ Der Unterschied hat nichts mit Datentypen zu tun. WHERE filtert *einzelne Zeilen* vor GROUP BY (z.B. `WHERE Alter < 30`), HAVING filtert *ganze Gruppen* nach der Aggregation (z.B. `HAVING COUNT(*) > 3`)."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Vorhersage: Ungültige GROUP BY Abfrage
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    vorhersage_groupby = mo.ui.radio(
        options={
            "fehler": "Fehler — Position ohne GROUP BY ist nicht erlaubt",
            "alle_mit_avg": "Alle Positionen, jede mit dem gleichen AVG-Wert",
            "eine_zeile": "Nur eine Zeile mit einer zufälligen Position",
        },
        label="Was passiert bei `SELECT Position, AVG(Alter) FROM spieler` ohne GROUP BY?"
    )
    vorhersage_groupby
    return (vorhersage_groupby,)


@app.cell(hide_code=True)
def _(vorhersage_groupby, mo):
    if vorhersage_groupby.value == "fehler":
        mo.output.replace(mo.md("✅ **Richtig!** Ohne `GROUP BY Position` kann SQL nicht wissen, welche Position zur aggregierten Durchschnittszeile gehört. Die *Goldene Regel*: Im SELECT nur GROUP BY-Spalten oder Aggregatfunktionen! (Manche Datenbanken wie MySQL erlauben dies trotzdem, liefern aber undefinierte Ergebnisse.)"))
    elif vorhersage_groupby.value == "alle_mit_avg":
        mo.output.replace(mo.md("❌ Nicht ganz. Ohne GROUP BY wird nur **eine** Zeile berechnet (der Durchschnitt aller Spieler). Aber `Position` hat mehrere verschiedene Werte — SQL weiß nicht, welchen es in diese eine Zeile schreiben soll → **Fehler**."))
    elif vorhersage_groupby.value == "eine_zeile":
        mo.output.replace(mo.md("❌ Nah dran — es würde tatsächlich eine Zeile werden (AVG über alle). Aber SQL kann nicht 'zufällig' eine Position wählen. `Position` ist nicht aggregiert und nicht in GROUP BY → die meisten Datenbanken geben einen **Fehler** aus."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        **Jetzt zum Übungs-Notebook → Aufgaben 6.x**

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Visualisierung: Aggregierte Daten darstellen

    Aggregierte Daten mit `GROUP BY` eignen sich hervorragend für Balkendiagramme:
    - x-Achse: die Gruppierungsspalte (z.B. Position)
    - y-Achse: der aggregierte Wert (z.B. AVG(Tore))
    """)
    return


@app.cell(hide_code=True)
def _():
    import plotly.express as px
    return (px,)


@app.cell(hide_code=True)
def _(mo, px, spieler):
    tore_by_position = mo.sql(
        f"""
        SELECT Position, AVG(Tore) AS Schnitt_Tore
        FROM spieler
        GROUP BY Position
        ORDER BY Schnitt_Tore DESC
        """
    )

    fig = px.bar(
        tore_by_position,
        x="Position",
        y="Schnitt_Tore",
        title="Durchschnittliche Tore nach Position",
        labels={"Schnitt_Tore": "Ø Tore"},
        color="Position"
    )
    fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Viz-Choice: Den richtigen Charttyp wählen
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    viz_choice_3 = mo.ui.radio(
        options={
            "bar": "Balkendiagramm",
            "line": "Liniendiagramm",
            "scatter": "Streudiagramm",
            "histogram": "Histogramm",
        },
        label="Sie wollen das durchschnittliche Alter pro Position zeigen. Welcher Charttyp passt am besten?"
    )
    viz_choice_3
    return (viz_choice_3,)


@app.cell(hide_code=True)
def _(viz_choice_3, mo):
    if viz_choice_3.value == "bar":
        mo.output.replace(mo.md("✅ **Richtig!** Ein **Balkendiagramm** ist ideal zum **Vergleichen von Kategorien**. Die Positionen (Sturm, Mittelfeld, etc.) sind Kategorien, und der Durchschnittswert wird als Balkenhöhe dargestellt. Das macht Unterschiede sofort sichtbar."))
    elif viz_choice_3.value == "line":
        mo.output.replace(mo.md("❌ Nicht ganz. Ein Liniendiagramm zeigt **Entwicklungen über die Zeit**. Positionen haben keine natürliche Reihenfolge — ein **Balkendiagramm** eignet sich besser zum Vergleichen von Kategorien."))
    elif viz_choice_3.value == "scatter":
        mo.output.replace(mo.md("❌ Nicht ganz. Ein Streudiagramm zeigt den **Zusammenhang zwischen zwei numerischen Variablen**. Hier haben wir Kategorien (Positionen) und einen Wert (Ø Alter) — ein **Balkendiagramm** passt besser."))
    elif viz_choice_3.value == "histogram":
        mo.output.replace(mo.md("❌ Nicht ganz. Ein Histogramm zeigt die **Verteilung** einer Variable (z.B. wie viele Spieler sind 20-25 Jahre alt). Für den **Vergleich** von Kategorien (Positionen) eignet sich ein **Balkendiagramm** besser."))
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
    selbsttest_3 = mo.ui.radio(
        options={
            "where": "In die WHERE-Klausel",
            "having": "In die HAVING-Klausel",
            "select": "In die SELECT-Klausel",
        },
        label="Sie wollen nur Positionen mit mehr als 3 Spielern anzeigen. Wohin gehört `COUNT(*) > 3`?"
    )
    selbsttest_3
    return (selbsttest_3,)


@app.cell(hide_code=True)
def _(selbsttest_3, mo):
    if selbsttest_3.value == "having":
        mo.output.replace(mo.md("✅ **Richtig!** `HAVING` filtert **Gruppen** nach der Aggregation. `WHERE` kann keine Aggregatfunktionen verwenden, weil es **vor** GROUP BY ausgeführt wird."))
    elif selbsttest_3.value == "where":
        mo.output.replace(mo.md("❌ `WHERE` wird **vor** GROUP BY ausgeführt und kann daher keine Aggregatfunktionen wie `COUNT(*)` verwenden. Für Bedingungen auf Gruppen brauchen Sie `HAVING`."))
    elif selbsttest_3.value == "select":
        mo.output.replace(mo.md("❌ `SELECT` wählt Spalten aus, filtert aber nicht. Um Gruppen zu filtern, verwenden Sie `HAVING` — es wird nach GROUP BY ausgeführt und kann Aggregatfunktionen prüfen."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Zusammenfassung

        | Konzept | Syntax | Beispiel |
        |---------|--------|----------|
        | Zählen | `COUNT(*)` | `SELECT COUNT(*) FROM tabelle` |
        | Summe | `SUM(spalte)` | `SUM(Tore)` |
        | Durchschnitt | `AVG(spalte)` | `AVG(Punkte)` |
        | Minimum/Maximum | `MIN/MAX(spalte)` | `MIN(Alter), MAX(Alter)` |
        | Gruppieren | `GROUP BY spalte` | `GROUP BY Position` |
        | Gruppen filtern | `HAVING bedingung` | `HAVING COUNT(*) > 5` |

        ### Ausführungsreihenfolge

        ```
        FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
        ```

        ### Goldene Regel

        Im `SELECT` nur:
        1. Spalten aus `GROUP BY`
        2. Aggregatfunktionen

        ### Ausblick Session 4

        Nächste Woche: Strukturierte Datenanalyseprozesse (CRISP-DM, Fallstudie)
        """
    )
    return


if __name__ == "__main__":
    app.run()
