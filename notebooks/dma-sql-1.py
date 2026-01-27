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

        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Daten laden: Bundesliga-Tabelle

        Wir arbeiten mit aktuellen Bundesliga-Daten. Der folgende Code lädt die aktuelle Tabelle von fussballdaten.de und speichert sie in einer SQLite-Datenbank.
        """
    )
    return


@app.cell
def _():
    import pandas as pd

    def lade_bundesliga_tabelle(saison: str = "2026") -> pd.DataFrame:
        """
        Lädt die aktuelle Bundesliga-Tabelle von fussballdaten.de.
        Falls das fehlschlägt, wird eine lokale Backup-Datei verwendet.
        """
        url = f"https://www.fussballdaten.de/bundesliga/{saison}/tabelle/"

        # Use fallback data function
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

            # Spalten umbenennen (Website verwendet englische/deutsche Mix-Namen)
            spalten_mapping = {
                "Pts": "Punkte", "Pkt": "Punkte",
                "S": "Siege",
                "D": "Unentschieden", "U": "Unentschieden",
                "L": "Niederlagen", "V": "Niederlagen",
                "Sp.": "Spiele",
                "Goals": "Tore", "Tore": "Tore",
                "Diff.": "Tordifferenz"
            }

            # Nur vorhandene Spalten umbenennen
            df = df.rename(columns={k: v for k, v in spalten_mapping.items() if k in df.columns})

            # Tordifferenz berechnen falls nicht vorhanden
            if "Tordifferenz" not in df.columns and "Tore" in df.columns:
                df[["ToreGeschossen", "ToreKassiert"]] = df["Tore"].str.split(":", expand=True).astype(int)
                df["Tordifferenz"] = df["ToreGeschossen"] - df["ToreKassiert"]
            elif "Tordifferenz" in df.columns:
                # Tordifferenz als Integer
                df["Tordifferenz"] = pd.to_numeric(df["Tordifferenz"], errors="coerce").fillna(0).astype(int)
                # Tore aufsplitten falls vorhanden
                if "Tore" in df.columns:
                    df[["ToreGeschossen", "ToreKassiert"]] = df["Tore"].str.split(":", expand=True).astype(int)
                else:
                    df["ToreGeschossen"] = 0
                    df["ToreKassiert"] = 0

            # Relevante Spalten auswählen
            gewuenschte_spalten = ["Mannschaft", "Spiele", "Siege", "Unentschieden", "Niederlagen",
                                   "ToreGeschossen", "ToreKassiert", "Tordifferenz", "Punkte"]
            df = df[[c for c in gewuenschte_spalten if c in df.columns]]

            quelle = f"Live von fussballdaten.de (Saison {saison})"

        except:
            return get_fallback()

        return df, quelle

    bundesliga, daten_quelle = lade_bundesliga_tabelle("2026")
    bundesliga
    return bundesliga, daten_quelle, lade_bundesliga_tabelle, pd


@app.cell(hide_code=True)
def _(daten_quelle, mo):
    mo.md(
        f"""
        **Datenquelle:** {daten_quelle}

        ---

        ## Phase 2: Erste SELECT-Abfragen

        Jetzt können wir SQL verwenden! marimo unterstützt SQL direkt mit `mo.sql()`.

        ### Aufgabe 2.1: Alle Daten anzeigen

        Die einfachste Abfrage zeigt alle Spalten und Zeilen:
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
        ### Aufgabe 2.2: Bestimmte Spalten auswählen

        Wählen Sie nur Mannschaft und Punkte aus:
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
        ### Übung 2.3: Probieren Sie selbst!

        Schreiben Sie eine Abfrage, die folgende Spalten anzeigt:
        - Mannschaft
        - Siege
        - Niederlagen
        - Tordifferenz
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Ihre Lösung hier:
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Siege, Niederlagen, Tordifferenz
        FROM bundesliga
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 4: Filtern mit WHERE

        Mit `WHERE` können wir Zeilen filtern, die bestimmte Bedingungen erfüllen.

        ### Aufgabe 4.1: Teams mit mehr als 30 Punkten
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
        ### Aufgabe 4.2: Teams mit negativer Tordifferenz
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
        ### Übung 4.3: Probieren Sie selbst!

        Finden Sie alle Teams, die:
        1. Mindestens 10 Siege haben
        2. Weniger als 5 Niederlagen haben
        3. Genau 17 Spiele absolviert haben

        (Erstellen Sie drei separate Abfragen)
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Mindestens 10 Siege
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Siege
        FROM bundesliga
        WHERE Siege >= 10
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Weniger als 5 Niederlagen
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Niederlagen
        FROM bundesliga
        WHERE Niederlagen < 5
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Genau 17 Spiele
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Spiele
        FROM bundesliga
        WHERE Spiele = 17
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Phase 6: Komplexe Abfragen mit AND, OR, NOT

        Jetzt kombinieren wir mehrere Bedingungen!

        ### Aufgabe 6.1: AND - Beide Bedingungen müssen wahr sein

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
        ### Aufgabe 6.2: OR - Mindestens eine Bedingung muss wahr sein

        Teams, die entweder viele Punkte ODER eine positive Tordifferenz haben:
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
        ### Aufgabe 6.3: NOT - Bedingung negieren

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
        ### Aufgabe 6.4: BETWEEN und IN

        Weitere praktische Operatoren:
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # BETWEEN: Wertebereich (inklusiv)
    _df = mo.sql(
        f"""
        SELECT Mannschaft, Punkte
        FROM bundesliga
        WHERE Punkte BETWEEN 20 AND 30
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # IN: Liste von Werten
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
        ### Aufgabe 6.5: LIKE - Mustersuche

        Mit LIKE können wir nach Textmustern suchen:
        - `%` steht für beliebig viele Zeichen
        - `_` steht für genau ein Zeichen
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Teams, deren Name mit 'B' beginnt
    _df = mo.sql(
        f"""
        SELECT Mannschaft
        FROM bundesliga
        WHERE Mannschaft LIKE 'B%'
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Teams mit 'München' im Namen
    _df = mo.sql(
        f"""
        SELECT Mannschaft
        FROM bundesliga
        WHERE Mannschaft LIKE '%München%'
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---

        ## Freie Exploration

        Jetzt sind Sie dran! Stellen Sie eigene Fragen an die Daten.

        **Ideen:**
        - Welche Teams haben mehr Tore geschossen als kassiert?
        - Welche Teams haben mindestens halb so viele Punkte wie Spiele?
        - Welche Teams haben "Borussia" im Namen?
        - Welche Teams sind im Mittelfeld (Platz 6-12)?
        """
    )
    return


@app.cell
def _(bundesliga, mo):
    # Ihre eigene Abfrage hier:
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

        ## Zusammenfassung

        | Konzept | Syntax | Beispiel |
        |---------|--------|----------|
        | Alle Spalten | `SELECT *` | `SELECT * FROM tabelle` |
        | Bestimmte Spalten | `SELECT spalte1, spalte2` | `SELECT Mannschaft, Punkte FROM bundesliga` |
        | Filtern | `WHERE bedingung` | `WHERE Punkte > 30` |
        | Und-Verknüpfung | `AND` | `WHERE Siege > 10 AND Niederlagen < 5` |
        | Oder-Verknüpfung | `OR` | `WHERE Punkte > 30 OR Tordifferenz > 10` |
        | Negation | `NOT` | `WHERE NOT Mannschaft = 'Bayern'` |
        | Wertebereich | `BETWEEN` | `WHERE Punkte BETWEEN 20 AND 30` |
        | Werteliste | `IN` | `WHERE Mannschaft IN ('A', 'B', 'C')` |
        | Mustersuche | `LIKE` | `WHERE Mannschaft LIKE 'B%'` |

        **Nächste Session:** Sortieren, DISTINCT, NULL-Werte
        """
    )
    return


if __name__ == "__main__":
    app.run()
