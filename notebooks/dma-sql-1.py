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

        try:
            tabellen = pd.read_html(url)
            df = tabellen[0]

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

        except Exception as e:
            # Fallback: Beispieldaten
            df = pd.DataFrame({
                "Mannschaft": ["Bayern München", "Bayer Leverkusen", "VfB Stuttgart",
                              "Borussia Dortmund", "RB Leipzig", "Eintracht Frankfurt",
                              "SC Freiburg", "TSG Hoffenheim", "Werder Bremen", "VfL Wolfsburg",
                              "1. FC Union Berlin", "FC Augsburg", "Borussia M'gladbach",
                              "1. FSV Mainz 05", "1. FC Heidenheim", "VfL Bochum",
                              "FC St. Pauli", "Holstein Kiel"],
                "Spiele": [17]*18,
                "Siege": [13, 12, 10, 9, 9, 8, 7, 7, 6, 6, 5, 5, 5, 4, 4, 3, 3, 2],
                "Unentschieden": [2, 3, 4, 4, 3, 5, 6, 4, 5, 4, 6, 5, 4, 6, 5, 4, 3, 4],
                "Niederlagen": [2, 2, 3, 4, 5, 4, 4, 6, 6, 7, 6, 7, 8, 7, 8, 10, 11, 11],
                "ToreGeschossen": [53, 41, 40, 38, 32, 35, 28, 32, 29, 31, 22, 21, 26, 24, 22, 17, 14, 18],
                "ToreKassiert": [18, 22, 25, 28, 22, 24, 26, 30, 32, 34, 24, 32, 33, 28, 35, 38, 25, 45],
                "Tordifferenz": [35, 19, 15, 10, 10, 11, 2, 2, -3, -3, -2, -11, -7, -4, -13, -21, -11, -27],
                "Punkte": [41, 39, 34, 31, 30, 29, 27, 25, 23, 22, 21, 20, 19, 18, 17, 13, 12, 10]
            })
            quelle = f"Offline-Beispieldaten (Fehler: {e})"

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
