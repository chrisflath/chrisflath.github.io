import marimo

__generated_with = "0.13.0"
app = marimo.App(
    width="medium",
    app_title="DMA Session 2: SQL für Datenexploration",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Session 2: SQL für Datenexploration

        In dieser Session lernen Sie:

        - Ergebnisse **sortieren** mit `ORDER BY`
        - **Eindeutige Werte** finden mit `DISTINCT`
        - **Mustersuche** mit `LIKE`
        - Mit **NULL-Werten** umgehen

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


@app.cell
def _():
    import pandas as pd

    def lade_bundesliga_tabelle(saison: str = "2026") -> pd.DataFrame:
        """Lädt die aktuelle Bundesliga-Tabelle von fussballdaten.de."""
        url = f"https://www.fussballdaten.de/bundesliga/{saison}/tabelle/"

        # Fallback data function
        def get_fallback():
            return pd.DataFrame({
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
            }), "Offline-Beispieldaten (Saison 2024/25)"

        try:
            # Try different parsers for compatibility
            df = None
            for parser in ['html.parser', 'lxml', 'html5lib']:
                try:
                    tabellen = pd.read_html(url, flavor=parser)
                    df = tabellen[0]
                    break
                except:
                    continue

            if df is None:
                return get_fallback()

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

            gewuenschte_spalten = ["Mannschaft", "Spiele", "Siege", "Unentschieden", "Niederlagen",
                                   "ToreGeschossen", "ToreKassiert", "Tordifferenz", "Punkte"]
            df = df[[c for c in gewuenschte_spalten if c in df.columns]]
            quelle = f"Live von fussballdaten.de (Saison {saison})"

        except:
            return get_fallback()

        return df, quelle

    bundesliga, daten_quelle = lade_bundesliga_tabelle("2026")
    return bundesliga, daten_quelle, lade_bundesliga_tabelle, pd


@app.cell
def _(pd):
    # Spieler-Daten mit NULL-Werten für Übungen
    spieler = pd.DataFrame({
        "Name": ["Müller", "Neuer", "Kimmich", "Sané", "Musiala", "Gündogan",
                 "Havertz", "Wirtz", "Füllkrug", "Schlotterbeck", "Rüdiger", "Tah"],
        "Vorname": ["Thomas", "Manuel", "Joshua", "Leroy", "Jamal", "İlkay",
                    "Kai", "Florian", "Niclas", "Nico", "Antonio", "Jonathan"],
        "Position": ["Sturm", "Tor", "Mittelfeld", "Sturm", "Mittelfeld", "Mittelfeld",
                     "Sturm", "Mittelfeld", "Sturm", "Abwehr", "Abwehr", "Abwehr"],
        "Verein": ["Bayern München", "Bayern München", "Bayern München", "Bayern München",
                   "Bayern München", None, "Arsenal", "Bayer Leverkusen",
                   "West Ham", "Borussia Dortmund", "Real Madrid", "Bayer Leverkusen"],
        "Tore": [8, 0, 3, 5, 12, None, 9, 11, 6, 1, 2, None],
        "Vorlagen": [4, None, 8, 3, 7, 2, 5, 9, 2, None, 1, 0],
        "Spitzname": ["Mülli", None, "Jo", None, None, "Günni", None, "Flo", "Fülle", None, "Rüdi", None]
    })
    # Konvertiere zu nullable integer types
    spieler["Tore"] = spieler["Tore"].astype("Int64")
    spieler["Vorlagen"] = spieler["Vorlagen"].astype("Int64")
    spieler
    return (spieler,)


@app.cell(hide_code=True)
def _(daten_quelle, mo):
    mo.md(
        f"""
        **Datenquelle Bundesliga:** {daten_quelle}

        ---

        ## Phase 2: Daten sortieren mit ORDER BY

        ### Aufgabe 2.1: Einfache Sortierung

        Sortieren Sie die Bundesliga-Tabelle nach Punkten (absteigend):
        """
    )
    return


@app.cell
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
    mo.md(
        r"""
        ### Aufgabe 2.2: Aufsteigende Sortierung

        Zeigen Sie die Teams mit der schlechtesten Tordifferenz zuerst:
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Tordifferenz
        FROM bundesliga
        ORDER BY Tordifferenz ASC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 2.3: Mehrere Sortierkriterien

        Sortieren Sie nach Punkten (absteigend), bei Gleichstand nach Tordifferenz:
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte, Tordifferenz
        FROM bundesliga
        ORDER BY Punkte DESC, Tordifferenz DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 2.4: Top 5 mit LIMIT

        Zeigen Sie nur die Top 5 Teams:
        """
    )
    return


@app.cell
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
    mo.md(
        r"""
        ---

        ## Phase 4: DISTINCT und LIKE

        ### Aufgabe 4.1: Eindeutige Werte mit DISTINCT

        Welche verschiedenen Spielstände (Anzahl Spiele) gibt es?
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    _df = mo.sql(
        f"""
        SELECT DISTINCT Spiele
        FROM bundesliga
        ORDER BY Spiele
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 4.2: DISTINCT mit Spielerdaten

        Welche verschiedenen Positionen gibt es bei den Spielern?
        """
    )
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT DISTINCT Position
        FROM spieler
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 4.3: Mustersuche mit LIKE

        Finden Sie alle Teams, deren Name mit 'B' beginnt:
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
        ### Aufgabe 4.4: Komplexere Muster

        Finden Sie alle Spieler, deren Nachname auf 'er' endet:
        """
    )
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT Name, Vorname
        FROM spieler
        WHERE Name LIKE '%er'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 6: Umgang mit NULL-Werten

        ### Aufgabe 6.1: NULL-Werte finden

        Welche Spieler haben keinen Verein eingetragen (NULL)?
        """
    )
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT Name, Vorname, Verein
        FROM spieler
        WHERE Verein IS NULL
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 6.2: NOT NULL

        Welche Spieler haben Tore eingetragen (nicht NULL)?
        """
    )
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT Name, Tore
        FROM spieler
        WHERE Tore IS NOT NULL
        ORDER BY Tore DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 6.3: COALESCE - NULL ersetzen

        Zeigen Sie alle Spieler mit Toren, ersetzen Sie NULL durch 0:
        """
    )
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT
            Name,
            Tore AS Tore_Original,
            COALESCE(Tore, 0) AS Tore_Bereinigt
        FROM spieler
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 6.4: COALESCE mit mehreren Fallbacks

        Erstellen Sie einen Anzeigenamen: Spitzname > Vorname > Name
        """
    )
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT
            Name,
            Spitzname,
            Vorname,
            COALESCE(Spitzname, Vorname, Name) AS Anzeigename
        FROM spieler
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Aufgabe 6.5: Kombination

        Zeigen Sie Spieler mit Toren und Vorlagen, ersetzen Sie NULLs, berechnen Sie die Summe:
        """
    )
    return


@app.cell
def _(mo, spieler):
    _df = mo.sql(
        f"""
        SELECT
            Name,
            COALESCE(Tore, 0) AS Tore,
            COALESCE(Vorlagen, 0) AS Vorlagen,
            COALESCE(Tore, 0) + COALESCE(Vorlagen, 0) AS Scorerpunkte
        FROM spieler
        ORDER BY Scorerpunkte DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Freie Exploration

        Probieren Sie eigene Abfragen! Ideen:

        - Top 3 Torjäger
        - Spieler ohne Spitznamen, sortiert nach Position
        - Teams mit "burg" im Namen
        - Die 3 Teams mit den wenigsten Niederlagen
        """
    )
    return


@app.cell
def _(bundesliga, mo, spieler):
    # Ihre eigene Abfrage hier:
    _df = mo.sql(
        f"""
        SELECT *
        FROM spieler
        ORDER BY Name
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
        | Sortieren | `ORDER BY spalte [ASC\|DESC]` | `ORDER BY Punkte DESC` |
        | Begrenzen | `LIMIT n` | `LIMIT 5` |
        | Eindeutige Werte | `SELECT DISTINCT` | `SELECT DISTINCT Position` |
        | NULL prüfen | `IS NULL` / `IS NOT NULL` | `WHERE Tore IS NULL` |
        | NULL ersetzen | `COALESCE(wert, ersatz)` | `COALESCE(Tore, 0)` |

        **Nächste Session:** Aggregation & Gruppierung (COUNT, SUM, AVG, GROUP BY)
        """
    )
    return


if __name__ == "__main__":
    app.run()
