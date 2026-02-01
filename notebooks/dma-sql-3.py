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
    app_title="DMA Session 3: Aggregation & Gruppierung",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 3: Aggregation & Gruppierung

        **Kursfahrplan:** **▸ I: SQL-Grundlagen (S1–4)** · II: Datenmodellierung (S5–8) · III: Fortgeschrittenes SQL (S9–10) · IV: Datenanalyse (S11–14)

        In dieser Session lernen Sie:

        - **Aggregatfunktionen**: COUNT, SUM, AVG, MIN, MAX
        - **Gruppierung** mit `GROUP BY`
        - **Filter auf Gruppen** mit `HAVING`
        - Unterschied zwischen `WHERE` und `HAVING`

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


@app.cell
def _():
    import polars as pl

    def lade_bundesliga_tabelle(saison: str = "2026"):
        """Lädt die aktuelle Bundesliga-Tabelle von fussballdaten.de."""
        import pandas as pd

        url = f"https://www.fussballdaten.de/bundesliga/{saison}/tabelle/"

        try:
            # Try different parsers for compatibility
            # html.parser is in stdlib, lxml/html5lib need installation
            for parser in ['html.parser', 'lxml', 'html5lib']:
                try:
                    tabellen = pd.read_html(url, flavor=parser)
                    df = tabellen[0]
                    break
                except Exception:
                    continue
            else:
                raise ImportError("No HTML parser available")

            spalten_mapping = {
                "Pts": "Punkte", "Pkt": "Punkte",
                "S": "Siege",
                "D": "Unentschieden", "U": "Unentschieden",
                "L": "Niederlagen", "V": "Niederlagen",
                "Sp.": "Spiele",
                "Goals": "Tore", "Tore": "Tore",
                "Diff.": "Tordifferenz"
            }
            df = df.rename(columns={k: v for k, v in spalten_mapping.items() if k in df.columns})

            if "Tordifferenz" not in df.columns and "Tore" in df.columns:
                df[["ToreGeschossen", "ToreKassiert"]] = df["Tore"].str.split(":", expand=True).astype(int)
                df["Tordifferenz"] = df["ToreGeschossen"] - df["ToreKassiert"]
            elif "Tordifferenz" in df.columns:
                df["Tordifferenz"] = pd.to_numeric(df["Tordifferenz"], errors="coerce").fillna(0).astype(int)
                if "Tore" in df.columns:
                    df[["ToreGeschossen", "ToreKassiert"]] = df["Tore"].str.split(":", expand=True).astype(int)

            gewünschte_spalten = ["Mannschaft", "Spiele", "Siege", "Unentschieden", "Niederlagen",
                                   "ToreGeschossen", "ToreKassiert", "Tordifferenz", "Punkte"]
            df = df[[c for c in gewünschte_spalten if c in df.columns]]
            quelle = f"Live von fussballdaten.de (Saison {saison})"

        except Exception as e:
            df = pd.DataFrame({
                "Mannschaft": ["Bayern München", "Borussia Dortmund", "VfB Stuttgart",
                              "RB Leipzig", "Bayer Leverkusen", "Eintracht Frankfurt",
                              "SC Freiburg", "TSG Hoffenheim", "Werder Bremen", "VfL Wolfsburg",
                              "1. FC Union Berlin", "FC Augsburg", "Borussia M'gladbach",
                              "1. FSV Mainz 05", "1. FC Heidenheim", "VfL Bochum",
                              "FC St. Pauli", "Holstein Kiel"],
                "Spiele": [19, 19, 19, 18, 18, 19, 18, 18, 19, 19, 18, 19, 18, 19, 19, 19, 18, 19],
                "Siege": [16, 12, 11, 11, 10, 9, 9, 11, 7, 6, 6, 6, 6, 5, 5, 3, 4, 3],
                "Unentschieden": [2, 6, 3, 2, 2, 6, 3, 3, 6, 7, 5, 5, 3, 6, 4, 5, 3, 3],
                "Niederlagen": [1, 1, 5, 5, 6, 4, 6, 4, 6, 6, 7, 8, 9, 8, 10, 11, 11, 13],
                "ToreGeschossen": [72, 38, 40, 32, 41, 35, 28, 38, 29, 31, 22, 21, 26, 24, 28, 17, 14, 18],
                "ToreKassiert": [16, 17, 30, 20, 31, 24, 26, 22, 32, 34, 24, 32, 33, 28, 40, 38, 25, 45],
                "Tordifferenz": [56, 21, 10, 12, 10, 11, 2, 16, -3, -3, -2, -11, -7, -4, -12, -21, -11, -27],
                "Punkte": [50, 42, 36, 35, 32, 33, 30, 36, 27, 25, 23, 23, 21, 21, 19, 14, 15, 12]
            })
            quelle = f"Offline-Beispieldaten"

        return pl.from_pandas(df), quelle

    bundesliga, daten_quelle = lade_bundesliga_tabelle("2026")
    return bundesliga, daten_quelle, lade_bundesliga_tabelle, pl


@app.cell
def _():
    import plotly.express as px
    return (px,)


@app.cell
def _(pl):
    # Erweiterte Spieler-Daten für Aggregationsübungen
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
    spieler
    return (spieler,)


@app.cell(hide_code=True)
def _(daten_quelle, mo):
    mo.md(
        f"""
        **Datenquelle Bundesliga:** {daten_quelle}

        ---

        ## Phase 2: Aggregatfunktionen

        ### Aufgabe 2.1: COUNT - Zeilen zählen

        Wie viele Teams sind in der Bundesliga?
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT COUNT(*) AS Anzahl_Teams
        FROM bundesliga
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 2.2: SUM und AVG

        Wie viele Tore wurden insgesamt geschossen? Wie viele im Durchschnitt?
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT
            SUM(ToreGeschossen) AS Gesamttore,
            AVG(ToreGeschossen) AS Durchschnitt_Tore
        FROM bundesliga
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 2.3: MIN und MAX

        Welches ist die beste und schlechteste Tordifferenz?
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT
            MIN(Tordifferenz) AS Schlechteste,
            MAX(Tordifferenz) AS Beste,
            MAX(Tordifferenz) - MIN(Tordifferenz) AS Spannweite
        FROM bundesliga
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 2.4: Mehrere Aggregationen kombinieren

        Erstellen Sie eine Übersicht mit allen wichtigen Statistiken:
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT
            COUNT(*) AS Teams,
            SUM(Siege) AS Gesamtsiege,
            AVG(Punkte) AS Schnitt_Punkte,
            MIN(Punkte) AS Min_Punkte,
            MAX(Punkte) AS Max_Punkte
        FROM bundesliga
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 4: GROUP BY - Daten gruppieren

        > **Vorhersage:** Die Spieler-Tabelle hat 16 Einträge mit den Positionen Sturm, Tor, Mittelfeld und Abwehr. Wenn wir `GROUP BY Position` verwenden — wie viele Zeilen hat das Ergebnis? Überlegen Sie kurz, bevor Sie weiterscrollen.

        ### Aufgabe 4.1: Einfache Gruppierung

        Wie viele Spieler gibt es pro Position?
        """
    )
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT Position, COUNT(*) AS Anzahl
        FROM spieler
        GROUP BY Position
        ORDER BY Anzahl DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 4.2: Durchschnitt pro Gruppe

        Wie viele Tore schießen die verschiedenen Positionen im Durchschnitt?
        """
    )
    return


@app.cell
def _(mo, spieler):
    tore_by_position = mo.sql(
        f"""
        SELECT
            Position,
            COUNT(*) AS Spieler,
            AVG(Tore) AS Schnitt_Tore,
            SUM(Tore) AS Gesamt_Tore
        FROM spieler
        GROUP BY Position
        ORDER BY Schnitt_Tore DESC
        """
    )
    return (tore_by_position,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Visualisierung: Aggregierte Daten als Balkendiagramm

        Mit `GROUP BY` berechnete Werte lassen sich hervorragend als Balkendiagramm darstellen:
        """
    )
    return


@app.cell
def _(px, tore_by_position):
    px.bar(
        tore_by_position,
        x="Position",
        y="Schnitt_Tore",
        title="Durchschnittliche Tore nach Position",
        labels={"Position": "Position", "Schnitt_Tore": "Ø Tore"},
        color="Position"
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 4.3: Scaffolded — Gruppierung vervollständigen

        Welcher Verein hat die meisten Nationalspieler?
        Ergänzen Sie die `GROUP BY`-Spalte und die Sortierung:
        """
    )
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT
            Verein,
            COUNT(*) AS Nationalspieler
        FROM spieler
        -- Ergänzen Sie: Nach welcher Spalte gruppieren?
        GROUP BY ???
        -- Ergänzen Sie: Absteigend nach Anzahl sortieren
        ORDER BY ???
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    Verein,
    COUNT(*) AS Nationalspieler
FROM spieler
GROUP BY Verein
ORDER BY Nationalspieler DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 4.4: Scaffolded — Mehrere Aggregatfunktionen

        Erweitern Sie die Abfrage: Zeigen Sie pro Verein die Anzahl Spieler,
        die Gesamttore und das Durchschnittsalter.
        Ergänzen Sie die fehlenden Aggregatfunktionen:
        """
    )
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT
            Verein,
            COUNT(*) AS Nationalspieler,
            ???(Tore) AS Tore_Gesamt,
            ???("Alter") AS Durchschnittsalter
        FROM spieler
        GROUP BY Verein
        ORDER BY Nationalspieler DESC
        -- Tipp: SUM für Gesamttore, AVG für Durchschnitt
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"🔑 Musterlösung": mo.md("""
```sql
SELECT
    Verein,
    COUNT(*) AS Nationalspieler,
    SUM(Tore) AS Tore_Gesamt,
    AVG("Alter") AS Durchschnittsalter
FROM spieler
GROUP BY Verein
ORDER BY Nationalspieler DESC
```
""")})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 4.5: Bundesliga nach Spielanzahl gruppieren

        Welche Teams haben wie viele Spiele absolviert?
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT
            Spiele,
            COUNT(*) AS Anzahl_Teams,
            AVG(Punkte) AS Schnitt_Punkte
        FROM bundesliga
        GROUP BY Spiele
        ORDER BY Spiele
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 6: HAVING - Filter auf Gruppen

        ### Aufgabe 6.1: Gruppen filtern

        Welche Positionen haben mehr als 3 Spieler?
        """
    )
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT Position, COUNT(*) AS Anzahl
        FROM spieler
        GROUP BY Position
        HAVING COUNT(*) > 3
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 6.2: HAVING mit AVG

        Welche Positionen haben im Durchschnitt mehr als 5 Tore?
        """
    )
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT Position, AVG(Tore) AS Schnitt_Tore
        FROM spieler
        GROUP BY Position
        HAVING AVG(Tore) > 5
        ORDER BY Schnitt_Tore DESC
        """
    )
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
        mo.output.replace(mo.md("Richtig! WHERE filtert *einzelne Zeilen* bevor sie gruppiert werden. HAVING filtert *ganze Gruppen* nach der Aggregation. Deshalb kann HAVING Aggregatfunktionen wie COUNT(*) oder AVG() verwenden."))
    elif quiz_where_having.value:
        mo.output.replace(mo.md("Nicht ganz. Denken Sie an die Reihenfolge: Erst werden Zeilen gefiltert (WHERE), dann gruppiert (GROUP BY), dann werden Gruppen gefiltert (HAVING)."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 6.3: WHERE und HAVING kombinieren

        Welche Vereine haben mehr als 2 Spieler unter 30 Jahren?
        """
    )
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT Verein, COUNT(*) AS Junge_Spieler
        FROM spieler
        WHERE "Alter" < 30
        GROUP BY Verein
        HAVING COUNT(*) >= 2
        ORDER BY Junge_Spieler DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 6.4: Komplexe Analyse

        Finden Sie Vereine mit hoher Torbeteiligung (Tore + Vorlagen > 20):
        """
    )
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT
            Verein,
            SUM(Tore) AS Tore,
            SUM(Vorlagen) AS Vorlagen,
            SUM(Tore) + SUM(Vorlagen) AS Scorerpunkte
        FROM spieler
        GROUP BY Verein
        HAVING SUM(Tore) + SUM(Vorlagen) > 20
        ORDER BY Scorerpunkte DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 6.5: Bundesliga-Analyse

        Finden Sie alle Punktebereiche mit mehr als 3 Teams:
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT
            CASE
                WHEN Punkte >= 40 THEN 'Top (40+)'
                WHEN Punkte >= 30 THEN 'Oberes Mittelfeld (30-39)'
                WHEN Punkte >= 20 THEN 'Unteres Mittelfeld (20-29)'
                ELSE 'Abstiegskampf (<20)'
            END AS Punktebereich,
            COUNT(*) AS Teams
        FROM bundesliga
        GROUP BY Punktebereich
        HAVING COUNT(*) > 3
        ORDER BY MIN(Punkte) DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Visualisierung: Referenzlinien

        Ein häufiges Muster: Balkendiagramm mit **Durchschnittslinie** als Referenz.
        So sieht man sofort, welche Werte über/unter dem Durchschnitt liegen.
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    team_punkte = mo.sql(
        f"""
        SELECT Mannschaft, Punkte
        FROM bundesliga
        ORDER BY Punkte DESC
        """
    )
    return (team_punkte,)


@app.cell
def _(bundesliga, mo, px, team_punkte):
    # Durchschnitt berechnen
    avg_result = mo.sql(f"SELECT AVG(Punkte) AS avg FROM bundesliga")
    avg_punkte = avg_result.item(0, 0)

    # Balkendiagramm mit Referenzlinie
    fig = px.bar(
        team_punkte,
        x="Mannschaft",
        y="Punkte",
        title="Bundesliga: Punkte pro Team mit Liga-Durchschnitt",
        labels={"Mannschaft": "Team", "Punkte": "Punkte"}
    )

    # Durchschnittslinie hinzufügen
    fig.add_hline(
        y=avg_punkte,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Ø {avg_punkte:.1f}",
        annotation_position="right"
    )

    fig.update_layout(xaxis_tickangle=-45)
    fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        **Interpretation:** Teams über der roten Linie performen überdurchschnittlich.

        ---

        ## Freie Exploration

        Probieren Sie eigene Abfragen! Ideen:

        - Durchschnittsalter pro Position
        - Vereine mit mehr als 50 Länderspielen insgesamt
        - Teams mit mindestens 10 Siegen
        - Positionen sortiert nach Gesamtvorlagen
        """
    )
    return


@app.cell
def _(bundesliga, mo, spieler):
    # Ihre eigene Abfrage hier:
    _df = mo.sql(
        f"""
        SELECT Position, AVG("Alter") AS Durchschnittsalter
        FROM spieler
        GROUP BY Position
        ORDER BY Durchschnittsalter
        """
    )
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

        **Goldene Regel:** Im SELECT nur GROUP BY-Spalten oder Aggregatfunktionen!

        **Nächste Session:** Strukturierte Datenanalyseprozesse (CRISP-DM, Fallstudie)
        """
    )
    return


if __name__ == "__main__":
    app.run()
